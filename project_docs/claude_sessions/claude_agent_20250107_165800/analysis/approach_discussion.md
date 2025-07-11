# Dynamic Supervisor Approach Discussion

## Agent ID: claude_agent_20250107_165800

## The Confusion: Engines vs Agents and Base.py Usage

### 1. **Engine vs Agent Decision Matrix**

**Use Engines when:**

- Single-purpose functionality (LLM, retrieval, embedding)
- Stateless operations
- Reusable components across agents
- Tool execution without workflow

**Use Agents when:**

- Complex workflows with state management
- Multi-step reasoning (ReAct loops)
- Need for persistence/checkpointing
- Orchestrating multiple engines

### 2. **multi/base.py Purpose**

The `multi/base.py` is for **multi-agent orchestration**, NOT supervisor creation:

```python
# multi/base.py creates systems like:
SequentialAgent(agents=[planner, executor, reviewer])  # Pipeline
ParallelAgent(agents=[researcher1, researcher2])       # Consensus
ConditionalAgent(agents=[classifier, handler_a])       # Routing
```

**Key insight**: Multi-agents compose EXISTING agents, supervisors CREATE and MANAGE agents.

### 3. **Dynamic Supervisor Architecture**

The supervisor should use the **state-based approach** from `experiments/supervisor/`:

```
DynamicSupervisor (ReactAgent)
├── state.agents: Dict[str, SerializedAgent]  # Agents stored in state
├── Tools auto-created: handoff_to_X         # From state.agents
└── Engine tools sync when state changes     # Dynamic tool management
```

## How It Works

### 1. **Agent Storage in State**

```python
# Agents stored as serialized objects in LangGraph state
state.agents = {
    "research_agent": SerializedAgent(
        agent_class="SimpleAgent",
        agent_module="haive.agents.simple.agent",
        config={"name": "research_agent", "system_message": "..."},
        metadata=AgentMetadata(description="Research specialist")
    )
}
```

### 2. **Dynamic Tool Creation**

```python
# Tools created from state.agents automatically
def build_supervisor_tools(get_state_fn, update_state_fn):
    tools = []
    state = get_state_fn()

    for agent_name in state.agents:
        # Create handoff tool for each agent
        tool = create_supervisor_handoff_tool(agent_name, ...)
        tools.append(tool)

    return tools
```

### 3. **Tool Execution Flow**

```python
# When handoff_to_research_agent is called:
def handoff_to_research_agent(task: str):
    state = get_state()
    agent = state.agents["research_agent"].get_agent()  # Deserialize
    result = agent.invoke({"messages": [task]})
    return result
```

### 4. **Dynamic Agent Creation**

```python
# Supervisor can create new agents on demand:
@tool
def create_agent(name: str, description: str, agent_type: str):
    # Create agent instance
    if agent_type == "react":
        agent = ReactAgent(name=name)
    else:
        agent = SimpleAgent(name=name)

    # Store in state (triggers tool sync)
    state.register_agent(agent, metadata)

    # Tools automatically updated with new handoff_to_X
    return f"Created {name}, use handoff_to_{name}"
```

## Testing Strategy

### 1. **State Management Test**

```python
def test_agent_serialization():
    # Create supervisor
    supervisor = DynamicSupervisor()

    # Add agent to state
    agent = SimpleAgent(name="test_agent")
    supervisor.register_agent("test_agent", "Test agent", agent)

    # Verify state contains serialized agent
    state = supervisor.get_state()
    assert "test_agent" in state.agents

    # Verify tools include handoff
    tools = supervisor.get_all_tools()
    tool_names = [t.name for t in tools]
    assert "handoff_to_test_agent" in tool_names
```

### 2. **Dynamic Creation Test**

```python
def test_dynamic_creation():
    supervisor = DynamicSupervisor()

    # Use create_agent tool
    result = supervisor.invoke({
        "messages": [HumanMessage("Create a coding agent")]
    })

    # Should create agent and make it available
    state = supervisor.get_state()
    assert "coding_agent" in state.agents
```

### 3. **Output Demonstration**

```python
def test_supervisor_output():
    supervisor = DynamicSupervisor()

    with capture_logs() as logs:
        result = supervisor.invoke({
            "messages": [HumanMessage("I need help with Python code")]
        })

    # Should show decision process
    assert "Analyzing task requirements" in logs
    assert "Selected agent: coding_agent" in logs
    assert "Executing handoff" in logs
```

## Setup Approach

### 1. **Use experiments/supervisor/ as Base**

- `base_supervisor.py`: Core supervisor logic
- `state_models.py`: State schema with agent storage
- `tools.py`: Dynamic tool creation

### 2. **NOT multi/base.py**

The multi-agent base is for orchestrating existing agents, not creating a supervisor that manages agent lifecycle.

### 3. **Integration with ReactAgent**

```python
class DynamicSupervisor(BaseSupervisor):
    def __init__(self):
        super().__init__(
            state_schema=DynamicSupervisorState,  # Supports agent creation
            agent_factory=default_agent_factory   # For creating agents
        )
```

## Key Difference Summary

| Component                | Purpose                          | When to Use               |
| ------------------------ | -------------------------------- | ------------------------- |
| **SimpleAgent**          | Single LLM with tools            | Basic AI tasks            |
| **ReactAgent**           | Looping agent with reasoning     | Complex reasoning tasks   |
| **MultiAgent** (base.py) | Orchestrate existing agents      | Compose agent pipelines   |
| **DynamicSupervisor**    | Create/manage agents dynamically | Autonomous agent creation |

The supervisor is a special type of ReactAgent that can create other agents and manage them through state-based tool synchronization.
