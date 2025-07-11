# Code Evolution: From Problem to Solution

## The Journey

### Stage 1: Initial Problem

**Error**: "Type is not msgpack serializable: ModelMetaclass"

We were storing full agent objects in state, which contained:

- Pydantic model classes (state_schema, input_schema)
- LangChain tools with schemas
- Complex engine configurations

### Stage 2: Debugging Serialization

Created `debug_serialization.py` to identify exactly what wasn't serializable:

```python
# Findings:
❌ agent.state_schema: NOT SERIALIZABLE - ModelMetaclass
❌ agent.engine.tools: NOT SERIALIZABLE - StructuredTool
❌ active_agents: Set[str]: NOT SERIALIZABLE - set type
✅ agent.name: SERIALIZABLE
✅ state.model_dump(): SERIALIZABLE (after fixes)
```

### Stage 3: The Set Discovery

Initial error was actually about sets!

```python
# Before
active_agents: Set[str] = Field(default_factory=set)

# After
active_agents: List[str] = Field(default_factory=list)

# With validation to ensure uniqueness
@field_validator('active_agents')
def ensure_unique_agents(cls, v: List[str]) -> List[str]:
    return list(set(v)) if v else []
```

### Stage 4: The Exclude Solution

```python
class AgentInfo(BaseModel):
    # The breakthrough - exclude complex objects!
    agent: Any = Field(..., exclude=True)
    name: str
    description: str
    active: bool
```

### Stage 5: Dynamic Tools Implementation

```python
class SupervisorStateWithTools(SupervisorState):
    def sync_agents(self):
        """Regenerate tools whenever agents change."""
        # Update dynamic choice model
        for agent_name in self.agents.keys():
            self.agent_choice_model.add_option(agent_name)

        # Generate handoff tools
        for agent_name, agent_info in self.agents.items():
            tool_name = f"handoff_to_{agent_name}"
            # Tool created dynamically!
```

### Stage 6: Agent Execution Node

Mirrors the tool_node pattern:

```python
def create_agent_execution_node():
    def agent_execution(state):
        # Get agent from state (like tool_node gets tools)
        agent = state.agents[state.next_agent].get_agent()

        # Execute agent
        result = agent.run(state.agent_task)

        # Return update
        return {"agent_response": result}

    return agent_execution
```

### Stage 7: Final Architecture

```
SupervisorState
├── agents: Dict[str, AgentInfo]  # Registry with excluded agents
├── active_agents: List[str]      # Serializable list
├── messages: List[BaseMessage]   # Standard messages
└── tools: List[str]              # Generated dynamically

DynamicSupervisorAgent(SimpleAgent)
├── Inherits SimpleAgent behavior
├── Adds agent_execution node
└── Routes handoff tools → agent_execution
```

## Key Code Snippets

### The Working Test

```python
# Create supervisor
supervisor = DynamicSupervisorAgent(
    name="supervisor",
    engine=supervisor_engine
)

# Add agents to state
state = SupervisorStateWithTools()
state.add_agent("search", search_agent, "Web search")
state.sync_agents()  # Generate tools!

# Run - tools are available
result = await supervisor.arun(state)
```

### Dynamic Addition

```python
# Supervisor identifies missing capability
"I need translation but don't have that agent..."

# Add dynamically
state.add_agent("translator", translation_agent, "Languages")
state.sync_agents()

# Now it works!
"Using translation agent to translate to French..."
```

## Final Working Implementation

All components work together:

1. Agents stored in state (but excluded from serialization)
2. Tools generated dynamically from active agents
3. Agent execution node handles routing
4. Supervisor can identify missing capabilities
5. Full lifecycle management (add/remove/activate/deactivate)

The pattern successfully extends LangGraph's tool_node concept to agents!
