# Dynamic Supervisor Implementation Details

## Overview

We built a dynamic supervisor system for Haive that can manage agents at runtime, similar to how LangGraph's tool_node manages tools. The supervisor can add, remove, activate, and deactivate agents dynamically while maintaining state across runs.

## Core Components

### 1. SupervisorState Architecture

```python
class SupervisorState(MessagesState):
    """State for dynamic supervisor with agent registry."""
    
    # Agent registry - Dict instead of List for O(1) lookups
    agents: Dict[str, AgentInfo] = Field(default_factory=dict)
    
    # Active agents - List instead of Set (sets aren't msgpack serializable!)
    active_agents: List[str] = Field(default_factory=list)
    
    # Routing control
    next_agent: Optional[str] = None
    agent_task: str = ""
    agent_response: Optional[str] = None
```

**Key Learning**: Python `set` types are NOT serializable with msgpack! This caused our initial serialization errors.

### 2. AgentInfo with Serialization Solution

```python
class AgentInfo(BaseModel):
    # The agent field is excluded from serialization!
    agent: Any = Field(..., exclude=True)
    name: str
    description: str
    active: bool = True
    
    # Serializable metadata (empty for now, could extend)
    agent_metadata: dict = Field(default_factory=dict)
```

**Critical Fix**: `exclude=True` prevents the agent object from being serialized, solving the ModelMetaclass serialization issue.

### 3. Dynamic Tool Generation

```python
class SupervisorStateWithTools(SupervisorState):
    """State with dynamic tool generation from agents."""
    
    def sync_agents(self):
        """Generate handoff tools from current agents."""
        self._update_choice_model()  # Update dynamic choice validation
        self._generate_tools_from_agents()  # Create handoff_to_X tools
```

Tools are generated dynamically:
- `handoff_to_search_agent`
- `handoff_to_math_agent`
- `choose_agent` (with dynamic validation)

### 4. Agent Execution Node Pattern

```python
class AgentExecutionNode:
    """Mirrors tool_node pattern but for agents."""
    
    def __call__(self, state: SupervisorStateWithTools):
        # 1. Get routing from state
        agent_name = state.next_agent
        task = state.agent_task
        
        # 2. Get agent from state.agents
        agent_info = state.agents[agent_name]
        agent = agent_info.get_agent()
        
        # 3. Execute agent
        result = agent.run(task)
        
        # 4. Return state update
        return {
            "agent_response": result,
            "next_agent": None,
            "agent_task": ""
        }
```

### 5. DynamicSupervisorAgent

```python
class DynamicSupervisorAgent(SimpleAgent):
    """Extends SimpleAgent with dynamic agent management."""
    
    def build_graph(self) -> BaseGraph:
        # Extend SimpleAgent graph
        graph = super().build_graph()
        
        # Add agent execution node
        agent_execution_node = create_agent_execution_node()
        graph.add_node("agent_execution", agent_execution_node)
        graph.add_edge("agent_execution", "agent_node")
        
        return graph
```

## Implementation Journey

### Phase 1: Initial Architecture (Components 1-3)
- Created `SupervisorState` with agent registry
- Built `AgentInfo` for agent metadata
- Implemented agent execution node

### Phase 2: Serialization Crisis
- Hit "Type is not msgpack serializable: ModelMetaclass" error
- Discovered agents contain Pydantic model classes (not serializable)
- Found that Python sets aren't serializable either

### Phase 3: Solutions
1. **Set → List**: Changed `active_agents: Set[str]` to `List[str]` with validation
2. **Exclude Agent**: Added `exclude=True` to agent field in AgentInfo
3. **Keep References**: Agents exist in memory but aren't checkpointed

### Phase 4: Dynamic Tools
- Implemented `sync_agents()` for dynamic tool generation
- Created handoff tools that route to agent_execution node
- Added DynamicChoiceModel for validated agent selection

### Phase 5: Testing & Validation
- Tested dynamic addition/removal of agents
- Verified supervisor identifies missing capabilities
- Confirmed multi-agent coordination works

## Key Patterns

### 1. State-Driven Tools
```python
# Tools generated from state, not hardcoded
state.sync_agents()  # Regenerates tools based on current agents
```

### 2. Agent Lifecycle Management
```python
state.add_agent(name, agent, description)      # Add new capability
state.remove_agent(name)                       # Remove completely
state.activate_agent(name)                     # Make available
state.deactivate_agent(name)                   # Hide but keep
```

### 3. Serialization Strategy
- **In Memory**: Full agent objects accessible
- **In Storage**: Only metadata serialized
- **On Load**: Agents reconstructed from registry

## Lessons Learned

1. **Serialization is Tricky**: Not everything can be serialized (sets, classes, complex objects)
2. **Exclude is Powerful**: Pydantic's `exclude=True` solves many serialization issues
3. **State vs Behavior**: Keep data in state, behaviors in registries
4. **Dynamic is Possible**: LangGraph supports dynamic tool/agent management with proper patterns
5. **Test Incrementally**: Build components separately, test serialization early

## Usage Example

```python
# Create supervisor
supervisor = DynamicSupervisorAgent(name="supervisor", engine=supervisor_engine)

# Create state with initial agents
state = SupervisorStateWithTools()
state.add_agent("search_agent", search_agent, "Web search specialist")
state.sync_agents()

# Run task - supervisor identifies missing capability
result = await supervisor.arun("Translate this to French")
# Supervisor: "I need a translation agent..."

# Add capability dynamically
state.add_agent("translator", translation_agent, "Language specialist")
state.sync_agents()

# Retry - now it works!
result = await supervisor.arun("Translate this to French")
```

## Future Enhancements

1. **Agent Builder Node**: Automatically create agents based on specifications
2. **Capability Discovery**: Supervisor describes needed capabilities in detail
3. **Agent Persistence**: Save/load agent configurations
4. **Tool Routing**: Custom routing for handoff tools
5. **Multi-Supervisor**: Supervisors managing supervisors