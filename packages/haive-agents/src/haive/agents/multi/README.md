# Multi-Agent System

This module provides a framework for creating multi-agent systems where multiple agents can work together to solve complex tasks. The implementation uses the Haive Schema System for proper state management, field sharing, and serialization.

## Key Features

- **Serializable Agents**: Agents are stored directly in state and can be fully serialized/deserialized
- **Coordination Strategies**: Support for sequential, parallel, and adaptive agent coordination
- **Dynamic Schema Composition**: Uses SchemaComposer and AgentSchemaComposer for dynamic schema creation
- **State Sharing**: Proper field sharing between agents with reducer functions
- **Tool Collection**: Automatic collection and deduplication of tools from all agents

## Components

### MultiAgentState

A state schema for multi-agent systems that extends StateSchema and provides:

- Storage for agent instances indexed by ID
- Active agent tracking
- Output collection
- Shared state for inter-agent communication
- Tool routing information
- Field sharing and reducer functions

```python
class MultiAgentState(StateSchema):
    # Main state fields
    messages: List[BaseMessage] = Field(...)
    agents: Dict[str, Agent] = Field(...)
    active_agent_id: Optional[str] = Field(...)
    outputs: Dict[str, Any] = Field(...)
    shared_state: Dict[str, Any] = Field(...)

    # Define shared fields for parent-child graph communication
    __shared_fields__ = ["messages", "active_agent_id", "shared_state"]

    # Define reducers for merging field values during updates
    __reducer_fields__ = {
        "messages": add_messages,
    }
```

### MultiAgent

A coordinator agent that manages multiple agent instances and provides:

- Agent selection logic
- Work delegation
- Result processing
- Schema composition
- Graph construction

```python
class MultiAgent(Agent):
    # Configuration
    default_agent_type: str = Field(...)
    coordination_strategy: Literal["sequential", "parallel", "adaptive"] = Field(...)
```

## Usage Examples

### Creating a Multi-Agent System

```python
from haive.agents.simple.agent import SimpleAgent
from haive.agents.react.agent import ReactAgent
from haive.agents.multi.agent import MultiAgent

# Create some agents
research_agent = SimpleAgent(name="Research Agent")
writing_agent = ReactAgent(name="Writing Agent")

# Create multi-agent system
system = MultiAgent.with_agents(
    agents=[research_agent, writing_agent],
    name="Research-Writing System",
    coordination_strategy="sequential"
)

# Run the system
input_data = {
    "messages": [
        HumanMessage(content="Tell me about multi-agent systems.")
    ]
}
output = system.invoke(input_data)
```

### Serialization and Deserialization

The multi-agent system can be fully serialized and deserialized:

```python
# Serialize the state
state_json = system._state_instance.to_json()

# Create a new state from the serialized data
new_state = MultiAgentState.from_json(state_json)

# All agents and their state are preserved
agent = new_state.get_agent()
```

### Schema Composition

You can compose schemas from multiple agents:

```python
# Compose schema from agents
schema = MultiAgent.compose_schema_from_agents(
    agents=[agent1, agent2],
    name="CustomSchema",
    separation="smart"  # Options: "smart", "shared", "namespaced"
)

# Create instance of the schema
state = schema()
```

## Coordination Strategies

The `MultiAgent` supports different coordination strategies:

- **Sequential**: Agents run one after another in sequence
- **Parallel**: (Future) Agents run in parallel and results are combined
- **Adaptive**: (Future) Agent selection based on context and message content

## Advanced Features

### Field Sharing

Shared fields allow state to be synchronized between parent and child graphs:

```python
# Defined in MultiAgentState
__shared_fields__ = ["messages", "active_agent_id", "shared_state"]
```

### Reducer Functions

Reducers define how field values are combined during state updates:

```python
# Defined in MultiAgentState
__reducer_fields__ = {
    "messages": add_messages,
}
```

### Schema Composition

Multiple schema composition strategies are available:

- **Smart**: Automatically determines which fields to share based on usage patterns
- **Shared**: All fields are shared between parent and child graphs
- **Namespaced**: Fields are namespaced by agent name to avoid conflicts

### Tool Collection

Tools from all agents are automatically collected and deduplicated:

```python
# Get all unique tools
tools = state.collect_all_tools()
```

## Integration with Haive Schema System

The implementation leverages the Haive Schema System:

- **StateSchema**: For field sharing, reducers, and engine I/O tracking
- **SchemaComposer**: For dynamic schema creation and field management
- **AgentSchemaComposer**: For agent-specific schema composition

## Example Files

- `example.py`: Full examples of different multi-agent configurations
- `test_multi_agent.py`: Tests for the MultiAgent implementation
