# AgentSchemaComposer

Enhanced schema composer for building dynamic state schemas from multiple agents with intelligent field management and message preservation.

## Overview

The `AgentSchemaComposer` extends the base `SchemaComposer` with agent-specific functionality to handle complex multi-agent state management. It provides intelligent schema composition with support for various build modes and field separation strategies.

### Key Features

- **Automatic Schema Composition**: Compose schemas from multiple agent instances
- **Message Preservation**: Custom reducer prevents loss of fields like `tool_call_id`
- **Smart Field Separation**: Intelligent handling of shared vs. private fields
- **Build Modes**: Support for sequential, parallel, hierarchical execution patterns
- **Engine I/O Tracking**: Automatic tracking of input/output relationships

## Quick Start

```python
from haive.core.schema.agent_schema_composer import AgentSchemaComposer
from haive.agents.react.agent import ReactAgent
from haive.agents.simple.agent import SimpleAgent

# Create agents
react_agent = ReactAgent(name="Calculator", engine=calc_engine)
simple_agent = SimpleAgent(name="Planner", engine=plan_engine)

# Compose schema from agents
MultiAgentState = AgentSchemaComposer.from_agents(
    agents=[react_agent, simple_agent],
    name="MultiAgentState",
    separation="smart",  # Intelligent field separation
    build_mode=BuildMode.SEQUENCE  # Sequential execution
)

# Create state instance
state = MultiAgentState()
```

## API Reference

### AgentSchemaComposer

```python
class AgentSchemaComposer(SchemaComposer):
    """Enhanced schema composer that understands agents."""

    @classmethod
    def from_agents(
        cls,
        agents: List[Agent],
        name: Optional[str] = None,
        include_meta: bool = None,
        separation: str = "smart",
        build_mode: Optional[BuildMode] = None,
    ) -> Type[StateSchema]:
        """Compose schema from agents with smart defaults.

        Args:
            agents: List of agent instances to compose from
            name: Name for the composed schema (auto-generated if None)
            include_meta: Whether to include MetaAgentState (auto-detected if None)
            separation: Field separation strategy ("smart", "shared", "namespaced")
            build_mode: Execution mode (auto-detected if None)

        Returns:
            Composed StateSchema class ready for instantiation
        """
```

### Build Modes

```python
class BuildMode(str, Enum):
    """Build modes for agent schema composition."""
    PARALLEL = "parallel"      # All agents execute independently
    SEQUENCE = "sequence"      # Agents execute in sequence
    HIERARCHICAL = "hierarchical"  # Parent-child relationships
    CUSTOM = "custom"         # User-defined mode
```

### Field Separation Strategies

#### Smart Separation (Default)

Automatically determines field sharing based on usage patterns:

- Fields used by multiple agents are shared
- Fields prefixed with `shared_` are always shared
- Single-agent fields are namespaced in multi-agent contexts

#### Shared Separation

All fields are shared between agents without namespacing.

#### Namespaced Separation

Every field gets an agent-specific prefix to avoid conflicts.

## Message Preservation

The AgentSchemaComposer uses a custom `preserve_messages_reducer` that maintains BaseMessage objects intact:

```python
# This preserves all fields including tool_call_id
def add_messages(current_msgs: List[AnyMessage], new_msgs: List[AnyMessage]) -> List[AnyMessage]:
    """Combine message lists while preserving BaseMessage objects."""
    return preserve_messages_reducer(current_msgs, new_msgs)
```

## Examples

### Sequential Multi-Agent System

```python
# Create sequential multi-agent system
system = SequentialAgent(
    name="Research and Writing System",
    agents=[research_agent, writing_agent]
)

# The schema automatically handles:
# - Message flow between agents
# - Tool result preservation
# - State transitions
```

### Custom Field Configuration

```python
composer = AgentSchemaComposer(name="CustomState")

# Add custom fields with specific behavior
composer.add_field(
    "shared_context",
    Dict[str, Any],
    default_factory=dict,
    shared=True,
    description="Context shared between all agents"
)

# Build the schema
CustomState = composer.build()
```

## Best Practices

1. **Always use smart separation** unless you have specific requirements
2. **Let the composer handle message fields** - it automatically adds proper reducers
3. **Don't manually copy engines** - the composer handles serialization
4. **Use descriptive agent names** - they're used in field namespacing

## Troubleshooting

### Missing tool_call_id

Ensure the schema is using `preserve_messages_reducer` (automatically configured by AgentSchemaComposer).

### Field conflicts

Use `separation="namespaced"` for agents with conflicting field names.

### Serialization errors

The composer automatically serializes engines. Don't store raw engine objects in state.
