# Multi-Agent Schema Architecture

## Current Multi-Agent Issues

### 1. State Composition Problems
- **Flat Composition**: All agent fields merged into single state
- **Field Conflicts**: Agents can have conflicting field names
- **No Isolation**: Agents can accidentally modify each other's state
- **Tool Routes Confusion**: Which agent owns which tools?

### 2. Message Flow Issues
- **No Clear Ownership**: Who added which message?
- **Engine Attribution Lost**: Which engine generated what?
- **Tool Call Routing**: Which agent should handle tool calls?

## Proposed Multi-Agent State Design

### Core Principle: Hierarchical Isolation

```python
class MultiAgentStateV2(BaseModel):
    """Root state for multi-agent systems."""
    
    # === SHARED LAYER ===
    # Always accessible by all agents (read-only by default)
    shared: SharedState = Field(
        description="Shared state accessible by all agents"
    )
    
    # === AGENT LAYER ===
    # Isolated state per agent
    agents: Dict[str, AgentPrivateState] = Field(
        default_factory=dict,
        description="Private state for each agent"
    )
    
    # === ROUTING LAYER ===
    routing: RoutingState = Field(
        description="Controls agent execution flow"
    )
    
    # === META LAYER ===
    meta: MetaState = Field(
        description="System metadata and execution history"
    )

class SharedState(BaseModel):
    """State shared across all agents."""
    messages: MessageList = Field(
        description="Global message history"
    )
    context: Dict[str, Any] = Field(
        default_factory=dict,
        description="Shared context"
    )
    global_tools: List[Any] = Field(
        default_factory=list,
        description="Tools available to all agents"
    )

class AgentPrivateState(BaseModel):
    """Private state for individual agent."""
    working_memory: Dict[str, Any] = Field(
        default_factory=dict,
        description="Agent's private working memory"
    )
    local_tools: List[Any] = Field(
        default_factory=list,
        description="Agent-specific tools"
    )
    tool_routes: Dict[str, str] = Field(
        default_factory=dict,
        description="Agent's tool routing"
    )
    engine: Optional[Any] = Field(
        default=None,
        description="Agent's engine if stateful"
    )

class RoutingState(BaseModel):
    """Controls multi-agent execution."""
    current_agent: Optional[str] = Field(
        description="Currently active agent"
    )
    next_agent: Optional[str] = Field(
        description="Next agent to execute"
    )
    execution_history: List[str] = Field(
        default_factory=list,
        description="Order of agent execution"
    )
    agent_outputs: Dict[str, Any] = Field(
        default_factory=dict,
        description="Captured outputs per agent"
    )
```

## Schema Composition Strategy

### 1. Agent Registration Pattern

```python
class MultiAgentComposer:
    """Composes schemas for multi-agent systems."""
    
    def register_agent(
        self,
        agent_name: str,
        agent: Agent,
        shared_fields: List[str],
        private_fields: List[str]
    ) -> None:
        """Register an agent with field declarations."""
        # Extract agent's schema
        agent_schema = agent.get_state_schema()
        
        # Separate fields
        for field_name in shared_fields:
            self._add_to_shared(field_name, agent_schema)
            
        for field_name in private_fields:
            self._add_to_private(agent_name, field_name, agent_schema)
```

### 2. Field Access Patterns

```python
class AgentStateAccessor:
    """Provides controlled access to multi-agent state."""
    
    def __init__(self, agent_name: str, state: MultiAgentStateV2):
        self.agent_name = agent_name
        self.state = state
        
    @property
    def messages(self) -> MessageList:
        """Read-only access to shared messages."""
        return self.state.shared.messages
        
    def add_message(self, message: BaseMessage) -> None:
        """Add message with agent attribution."""
        message.metadata = message.metadata or {}
        message.metadata["agent"] = self.agent_name
        self.state.shared.messages.append(message)
        
    @property
    def private(self) -> AgentPrivateState:
        """Access to agent's private state."""
        return self.state.agents[self.agent_name]
```

### 3. Parent-Child Communication

```python
class ParentChildProtocol:
    """Defines how parent and child agents communicate."""
    
    def child_to_parent_summary(
        self,
        child_state: AgentPrivateState
    ) -> Dict[str, Any]:
        """Extract summary from child for parent."""
        return {
            "status": child_state.working_memory.get("status"),
            "results": child_state.working_memory.get("final_results"),
            "errors": child_state.working_memory.get("errors", [])
        }
    
    def parent_to_child_context(
        self,
        parent_state: MultiAgentStateV2,
        child_name: str
    ) -> Dict[str, Any]:
        """Provide context from parent to child."""
        return {
            "messages": parent_state.shared.messages[-5:],  # Last 5 messages
            "parent_context": parent_state.shared.context,
            "sibling_status": self._get_sibling_status(parent_state, child_name)
        }
```

## Implementation Examples

### Sequential Multi-Agent

```python
class SequentialAgentV2(MultiAgent):
    """Sequential agent with proper state isolation."""
    
    def create_state_schema(self) -> Type[BaseModel]:
        """Create hierarchical state schema."""
        composer = MultiAgentComposer()
        
        for agent in self.agents:
            # Each agent declares what it needs
            shared_needs = agent.get_shared_field_requirements()
            private_needs = agent.get_private_field_requirements()
            
            composer.register_agent(
                agent.name,
                agent,
                shared_needs,
                private_needs
            )
            
        return composer.create_schema()
    
    def execute_agent(self, agent: Agent, state: MultiAgentStateV2) -> None:
        """Execute single agent with proper isolation."""
        # Create accessor for this agent
        accessor = AgentStateAccessor(agent.name, state)
        
        # Agent only sees its view of state
        agent_view = accessor.create_agent_view()
        
        # Execute
        result = agent.run(agent_view)
        
        # Update state through accessor
        accessor.update_from_result(result)
```

### Parallel Multi-Agent

```python
class ParallelAgentV2(MultiAgent):
    """Parallel execution with state isolation."""
    
    async def execute_agents(self, state: MultiAgentStateV2) -> None:
        """Execute agents in parallel with isolation."""
        tasks = []
        
        for agent in self.agents:
            # Each agent gets isolated view
            agent_state = self._create_isolated_state(agent.name, state)
            tasks.append(self._run_agent_isolated(agent, agent_state))
            
        # Wait for all
        results = await asyncio.gather(*tasks)
        
        # Merge results carefully
        self._merge_parallel_results(state, results)
```

## Migration Path

### Step 1: Add Compatibility Layer
```python
def convert_flat_to_hierarchical(flat_state: Dict[str, Any]) -> MultiAgentStateV2:
    """Convert old flat state to new hierarchical."""
    pass
```

### Step 2: Update Agents Gradually
- Add get_shared_field_requirements() method
- Add get_private_field_requirements() method
- Update to use AgentStateAccessor

### Step 3: New Features
- Add agent-specific tool routing
- Implement proper message attribution
- Enable true parallel execution