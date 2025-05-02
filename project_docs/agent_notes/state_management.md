# State Management in Haive

## Core Concepts

State management in Haive focuses on creating structured, type-safe state schemas to encapsulate all information needed during agent execution. This approach ensures schema validation, proper serialization, and clear contract definition.

## StateSchema vs. Plain BaseModel

Haive's specialized `StateSchema` class extends Pydantic's `BaseModel` with additional capabilities:

```python
from haive.core.schema.state_schema import StateSchema
from pydantic import Field
from typing import List, Dict, Any

class MyAgentState(StateSchema):
    messages: List[Dict[str, Any]] = Field(default_factory=list)
    context: Dict[str, Any] = Field(default_factory=dict)

    # Define reducers for state merging
    __reducer_fields__ = {
        "messages": operator.add
    }

    # Helper methods can be added directly to the schema
    def add_message(self, message):
        self.messages.append(message)
        return self
```

Benefits of `StateSchema` over standard `BaseModel`:

- Built-in reducer support for field merging in branches
- Field sharing configuration for parent/child graph communication
- Engine I/O mapping for automatic field routing
- Integration with schema composition utilities

## Field Reducers

Reducers define how fields are combined when merging state from parallel branches:

```python
from typing import Annotated
import operator

# Method 1: Using Annotated type
class MyState(StateSchema):
    messages: Annotated[List[BaseMessage], operator.add]
    counter: Annotated[int, operator.add]

# Method 2: Using __reducer_fields__ dictionary
class MyState(StateSchema):
    messages: List[BaseMessage] = Field(default_factory=list)
    counter: int = 0

    __reducer_fields__ = {
        "messages": operator.add,
        "counter": operator.add
    }
```

Common reducers:

- `operator.add`: Concatenates lists, adds numbers
- `operator.or_`: Merges dictionaries
- `max`, `min`: Takes maximum/minimum value
- Custom reducers for complex merge logic

## Schema Composition

The `SchemaComposer` utility allows dynamic creation of state schemas from multiple components:

```python
from haive.core.schema.schema_composer import SchemaComposer

# Create a composer
composer = SchemaComposer("ComposedState")

# Add fields from different sources
composer.add_field(
    name="messages",
    field_type=List[BaseMessage],
    shared=True,
    reducer=operator.add
)

composer.add_field(
    name="results",
    field_type=List[Dict[str, Any]],
    default_factory=list
)

# Create the composed schema
composed_schema = composer.create_schema()
```

## Engine-Aware Schemas

State schemas in Haive can define explicit I/O mappings for engines:

```python
composer.add_field(
    name="query",
    field_type=str,
    input_for=["retriever", "llm"]  # This field is input for these engines
)

composer.add_field(
    name="documents",
    field_type=List[Document],
    output_from=["retriever"]  # This field is output from the retriever
)
```

These mappings enable automatic field routing when engines are used in nodes.

## State Schema Manager

For more complex state schema manipulation:

```python
from haive.core.schema.schema_manager import StateSchemaManager

manager = StateSchemaManager()

# Add fields programmatically
manager.add_field("query", str)
manager.add_field("context", Dict[str, Any], default_factory=dict)

# Mark fields as shared
manager.mark_shared("context")

# Add reducers
manager.add_reducer("messages", operator.add)

# Create schema
schema_class = manager.create_schema("MySchema")
```

## Serialization and Persistence

All state schemas in Haive support serialization for persistence:

```python
# Convert to dict
state_dict = state.model_dump()

# Convert to JSON
state_json = state.model_dump_json()

# Create from dict
new_state = MySchema.model_validate(state_dict)
```

For persistence with checkpointers:

```python
# State serialization happens automatically with checkpointers
from haive.core.engine.agent.persistence.memory_config import MemoryCheckpointerConfig

checkpointer_config = MemoryCheckpointerConfig(
    trace_history=True,
    checkpoint_interval=5
)
```
