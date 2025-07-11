# Haive Schema System

## Overview

The Haive Schema System provides a powerful foundation for dynamic state management in AI agents and workflows. It extends Pydantic's model system with features specifically designed for graph-based AI workflows, including field sharing between graphs, reducer functions for state updates, and engine I/O tracking.

This system enables fully dynamic and serializable state schemas that can be composed, modified, and extended at runtime, making it ideal for complex agent architectures and nested workflows.

## Core Components

The schema system consists of six main components that work together:

1. **StateSchema**: Base class that extends Pydantic models with sharing, reducers, and I/O tracking
2. **SchemaComposer**: Utility for building schemas from components dynamically
3. **StateSchemaManager**: Tool for manipulating schemas at runtime
4. **FieldDefinition**: Representation of field type, default, and metadata
5. **FieldExtractor**: Utility for extracting fields from various sources
6. **Field Utilities**: Common functions for field manipulation

## Component Relationships

```
┌─────────────────────────────────────────────────────────────┐
│                        StateSchema                          │
│ ┌───────────────┐              │              ┌────────────┐│
│ │ Field Sharing │◄────────────┐│◄────────────►│ Reducers   ││
│ └───────────────┘             ││              └────────────┘│
│                               ▼│                            │
│ ┌───────────────┐    ┌──────────────────┐    ┌────────────┐│
│ │Serialization  │◄──►│  Schema Fields   │◄──►│Validation   ││
│ └───────────────┘    └──────────────────┘    └────────────┘│
└─────────────────────────────────────────────────────────────┘
                         ▲           ▲
                         │           │
┌────────────────────────┘           └──────────────────────┐
│                                                           │
│   ┌─────────────────────┐         ┌────────────────────┐  │
│   │   SchemaComposer    │         │ StateSchemaManager │  │
│   │ ┌─────────────────┐ │         │┌──────────────────┐│  │
│   │ │Component Extract│ │         ││   Field Editing  ││  │
│   │ └─────────────────┘ │         │└──────────────────┘│  │
│   │ ┌─────────────────┐ │         │┌──────────────────┐│  │
│   │ │Schema Generation│ │◄───────►││Method Attachment ││  │
│   │ └─────────────────┘ │         │└──────────────────┘│  │
│   │ ┌─────────────────┐ │         │┌──────────────────┐│  │
│   │ │ Reducer Setup   │ │         ││Schema Composition││  │
│   │ └─────────────────┘ │         │└──────────────────┘│  │
│   └─────────────────────┘         └────────────────────┘  │
│                                                           │
└───────────────────────────────────────────────────────────┘
                        │   │
                        ▼   ▼
┌───────────────────────────────────────────────────────────┐
│                                                           │
│         ┌─────────────────┐      ┌────────────────┐       │
│         │ FieldDefinition │      │ FieldExtractor │       │
│         └─────────────────┘      └────────────────┘       │
│                  │                      │                  │
│                  └──────────┬───────────┘                  │
│                             │                              │
│                    ┌──────────────────┐                    │
│                    │   Field Utils    │                    │
│                    └──────────────────┘                    │
│                                                           │
└───────────────────────────────────────────────────────────┘
```

## StateSchema

The `StateSchema` class is the foundation of the schema system, extending Pydantic's `BaseModel` with features for AI agent state management.

### Field Sharing

Field sharing allows fields to be shared between parent and child graphs, enabling state to flow between them.

```python
class SimpleState(StateSchema):
    messages: List[BaseMessage] = Field(default_factory=list)
    query: str = Field(default="")
    result: str = Field(default="")

    # Only messages will be shared with parent graphs
    __shared_fields__ = ["messages"]
```

### Reducer Functions

Reducers define how field values are combined during state updates.

```python
class StateWithReducers(StateSchema):
    messages: List[BaseMessage] = Field(default_factory=list)
    context: List[str] = Field(default_factory=list)
    count: int = Field(default=0)

    # Define reducer functions for each field
    __reducer_fields__ = {
        "messages": add_messages,  # From langgraph.graph
        "context": operator.add,    # Concatenate lists
        "count": operator.add      # Add numbers
    }
```

### Engine I/O Tracking

Track which fields are inputs and outputs for which engines:

```python
class RAGState(StateSchema):
    query: str = Field(default="")
    context: List[str] = Field(default_factory=list)
    answer: str = Field(default="")

    # Map engines to their inputs and outputs
    __engine_io_mappings__ = {
        "retriever": {
            "inputs": ["query"],
            "outputs": ["context"]
        },
        "llm": {
            "inputs": ["query", "context"],
            "outputs": ["answer"]
        }
    }
```

### Key Methods

| Method                            | Description                             |
| --------------------------------- | --------------------------------------- |
| `to_dict()`                       | Convert state to dictionary             |
| `to_json()`                       | Convert state to JSON string            |
| `from_dict(data)`                 | Create state from dictionary            |
| `from_json(json_str)`             | Create state from JSON string           |
| `apply_reducers(other)`           | Apply updates using reducer functions   |
| `add_message(message)`            | Add a single message to messages field  |
| `add_messages(messages)`          | Add multiple messages to messages field |
| `prepare_for_engine(engine_name)` | Extract fields relevant to an engine    |
| `pretty_print()`                  | Format state for display                |
| `to_command(goto)`                | Convert to LangGraph Command            |
| `display_schema()`                | Show schema information                 |
| `to_python_code()`                | Generate Python code representation     |

## SchemaComposer

The `SchemaComposer` class provides a streamlined API for building state schemas from various components.

### Building a Schema

```python
from haive.core.schema.schema_composer import SchemaComposer
from typing import List
from langchain_core.messages import BaseMessage

# Create a new schema composer
composer = SchemaComposer(name="ConversationState")

# Add fields one by one
composer.add_field(
    name="messages",
    field_type=List[BaseMessage],
    default_factory=list,
    description="Conversation messages",
    shared=True,  # Will be shared with parent graphs
    reducer=add_messages  # Use langgraph's add_messages function
)

composer.add_field(
    name="query",
    field_type=str,
    default="",
    description="User query"
)

composer.add_field(
    name="response",
    field_type=str,
    default="",
    description="Final response"
)

# Build the schema
ConversationState = composer.build()
```

### Extracting from Components

```python
# Extract fields from a list of components (engines, models, etc.)
components = [retriever_engine, llm_engine, memory_engine]
StateSchema = SchemaComposer.from_components(
    components,
    name="RAGState"
)
```

### Key Methods

| Method                                    | Description                            |
| ----------------------------------------- | -------------------------------------- |
| `add_field(name, field_type, ...)`        | Add a field with comprehensive options |
| `add_fields_from_model(model)`            | Extract fields from a Pydantic model   |
| `add_fields_from_components(components)`  | Extract fields from components         |
| `add_fields_from_engine(engine)`          | Extract fields from an engine          |
| `add_fields_from_dict(fields_dict)`       | Add fields from a dictionary           |
| `configure_messages_field(...)`           | Set up messages field with reducer     |
| `build(use_annotated=True)`               | Build a StateSchema class              |
| `to_manager()`                            | Convert to a StateSchemaManager        |
| `merge(first, second)`                    | Merge two composers into a new one     |
| `from_components(components)`             | Create schema from components          |
| `compose_input_schema(components)`        | Create input schema from components    |
| `compose_output_schema(components)`       | Create output schema from components   |
| `create_message_state(additional_fields)` | Create schema with messages field      |

## StateSchemaManager

The `StateSchemaManager` class provides a more imperative API for creating and manipulating state schemas.

### Creating and Modifying a Schema

```python
from haive.core.schema.schema_manager import StateSchemaManager
from typing import List
from langchain_core.messages import BaseMessage

# Create a new manager
manager = StateSchemaManager(name="DynamicState")

# Add fields
manager.add_field(
    name="messages",
    field_type=List[BaseMessage],
    default_factory=list,
    shared=True
)

# Add field with reducer
manager.add_field(
    name="context",
    field_type=List[str],
    default_factory=list,
    reducer=operator.add  # Concatenate lists
)

# Modify an existing field
manager.modify_field(
    name="context",
    new_description="Retrieved document contexts",
    new_shared=True  # Change to shared
)

# Get the final schema
DynamicState = manager.get_model()
```

### Key Methods

| Method                                | Description                 |
| ------------------------------------- | --------------------------- |
| `add_field(name, field_type, ...)`    | Add a field with options    |
| `remove_field(name)`                  | Remove a field              |
| `modify_field(name, ...)`             | Update field properties     |
| `has_field(name)`                     | Check if field exists       |
| `get_model(...)`                      | Create Pydantic model       |
| `mark_as_input_field(field, engine)`  | Mark field as engine input  |
| `mark_as_output_field(field, engine)` | Mark field as engine output |
| `to_composer()`                       | Convert to SchemaComposer   |
| `merge(other)`                        | Merge with another schema   |
| `add_method(method, ...)`             | Add a method to the schema  |
| `from_components(components)`         | Create from components      |

## FieldDefinition

The `FieldDefinition` class represents a complete field definition including type, default, and metadata.

```python
from haive.core.schema.field_definition import FieldDefinition
from typing import List

# Create a field definition
field_def = FieldDefinition(
    name="context",
    field_type=List[str],
    default_factory=list,
    description="Retrieved document contexts",
    shared=True,
    reducer=operator.add,
    input_for=["llm_engine"],
    output_from=["retriever_engine"]
)

# Get field info for model creation
field_type, field_info = field_def.to_field_info()

# Get annotated field with embedded metadata
field_type, field_info = field_def.to_annotated_field()
```

## FieldExtractor

The `FieldExtractor` class provides utilities for extracting field information from various sources.

```python
from haive.core.schema.field_extractor import FieldExtractor

# Extract from a list of components
field_defs, engine_io_mappings, structured_model_fields, structured_models = (
    FieldExtractor.extract_from_components([retriever_engine, llm_engine])
)

# Extract from an engine
fields, descriptions, io_mappings, in_fields, out_fields = (
    FieldExtractor.extract_from_engine(llm_engine)
)

# Extract from a Pydantic model
fields, descriptions, shared_fields, reducer_names, reducer_functions, io_mappings, input_fields, output_fields = (
    FieldExtractor.extract_from_model(MyModelClass)
)
```

## Field Utilities

The `field_utils.py` module provides common functions for field manipulation:

```python
from haive.core.schema.field_utils import (
    create_field, create_annotated_field, extract_type_metadata,
    infer_field_type, get_common_reducers, resolve_reducer
)

# Create a field
field_type, field_info = create_field(
    field_type=List[str],
    default_factory=list,
    description="My field",
    shared=True
)

# Create field with Annotated type for metadata
field_type, field_info = create_annotated_field(
    field_type=List[str],
    default_factory=list,
    description="My field",
    shared=True,
    reducer=operator.add
)

# Extract metadata from a type
base_type, metadata = extract_type_metadata(field_type)

# Infer type from a value
inferred_type = infer_field_type([1, 2, 3])  # Returns List[int]

# Get common reducers
reducers = get_common_reducers()

# Resolve a reducer from its name
reducer_func = resolve_reducer("operator.add")
```

## Schema UI

The `SchemaUI` class provides rich visualizations and representations of schemas:

```python
from haive.core.schema.ui import SchemaUI

# Display schema information
SchemaUI.display_schema(MyStateSchema)

# Generate Python code
code = SchemaUI.schema_to_code(MyStateSchema)

# Display schema as code
SchemaUI.display_schema_code(MyStateSchema)

# Compare two schemas
SchemaUI.compare_schemas(StateA, StateB)
```

## Advanced Usage

### Field Sharing Between Graphs

Field sharing enables parent and child graphs to share state:

```python
# Parent graph state
class ParentState(StateSchema):
    messages: List[BaseMessage] = Field(default_factory=list)
    query: str = Field(default="")
    response: str = Field(default="")

# Child graph state
class ChildState(StateSchema):
    messages: List[BaseMessage] = Field(default_factory=list)  # Shared with parent
    context: List[str] = Field(default_factory=list)

    __shared_fields__ = ["messages"]  # Only messages is shared
```

When the parent graph invokes the child graph, updates to the `messages` field in either graph will be propagated to the other.

### State Updates with Reducers

Reducers allow customizing how values are combined during state updates:

```python
# Define a state with reducers
class ReducerState(StateSchema):
    messages: List[BaseMessage] = Field(default_factory=list)
    context: List[str] = Field(default_factory=list)
    counter: int = Field(default=0)

    __reducer_fields__ = {
        "messages": add_messages,
        "context": operator.add,     # Concatenate lists
        "counter": operator.add      # Add numbers
    }

# Create initial state
state = ReducerState()

# Apply update using reducers
update = {
    "messages": [HumanMessage(content="Hello")],
    "context": ["Additional context"],
    "counter": 1
}
state.apply_reducers(update)

# Result:
# state.messages == [HumanMessage(content="Hello")]
# state.context == ["Additional context"]
# state.counter == 1

# Apply second update
update2 = {
    "messages": [AIMessage(content="Hi there")],
    "context": ["More context"],
    "counter": 2
}
state.apply_reducers(update2)

# Result:
# state.messages == [HumanMessage(content="Hello"), AIMessage(content="Hi there")]
# state.context == ["Additional context", "More context"]
# state.counter == 3
```

### Engine I/O Preparation

The schema system tracks which fields each engine uses:

```python
# Prepare state for specific engine
retriever_input = state.prepare_for_engine("retriever")
# Returns only fields marked as inputs for retriever

# Merge engine output into state
retriever_output = {"context": ["Document 1", "Document 2"]}
state.merge_engine_output("retriever", retriever_output)
```

### Dynamic Schema Creation from Components

Create schemas by analyzing components:

```python
# Create from a list of engines
components = [
    retriever_engine,
    llm_engine,
    memory_engine
]

# Build schema directly
RAGState = SchemaComposer.from_components(components, name="RAGState")

# Or build with more control
composer = SchemaComposer(name="RAGState")
composer.add_fields_from_components(components)
composer.add_field("extra_field", str, default="")
RAGState = composer.build()
```

### Converting to LangGraph Command

Convert state to a LangGraph Command for graph control flow:

```python
# Create state
state = MyState(query="Hello", context=["Document 1"])

# Convert to Command with goto node
command = state.to_command(goto="generate_response")
# Returns Command(update={"query": "Hello", "context": ["Document 1"]}, goto="generate_response")
```

### Schema Merging

Merge schemas from different sources:

```python
# Create two schemas
retriever_schema = SchemaComposer.from_components([retriever_engine])
llm_schema = SchemaComposer.from_components([llm_engine])

# Merge into a single schema
merged = SchemaComposer.merge(retriever_schema, llm_schema, name="CombinedState")
CombinedState = merged.build()
```

### Adding Custom Methods

Add custom methods to schemas:

```python
# Define a custom method
def count_tokens(self):
    """Count tokens in all messages."""
    total = 0
    for message in self.messages:
        total += len(message.content.split())
    return total

# Add method to schema manager
manager = StateSchemaManager(name="EnhancedState")
manager.add_field("messages", List[BaseMessage], default_factory=list)
manager.add_method(count_tokens)

# Build schema
EnhancedState = manager.get_model()

# Use custom method
state = EnhancedState()
state.messages = [HumanMessage(content="This is a test message")]
token_count = state.count_tokens()  # Returns 5
```

## Integration with Engine System

The schema system integrates with the Engine system through several mechanisms:

### Engine Field Discovery

Engines define their input and output fields:

```python
def get_input_fields(self) -> Dict[str, Tuple[Type, Any]]:
    """Define input field requirements."""
    return {
        "query": (str, Field(default="")),
        "history": (List[Tuple[str, str]], Field(default_factory=list))
    }

def get_output_fields(self) -> Dict[str, Tuple[Type, Any]]:
    """Define output field requirements."""
    return {
        "response": (str, Field(default="")),
        "sources": (List[Dict[str, Any]], Field(default_factory=list))
    }
```

### Automatic Schema Composition

When building a graph, `SchemaComposer.from_components()` extracts and combines field requirements from all engines.

### State Preparation for Engines

The StateSchema provides methods to prepare inputs and process outputs for engines:

```python
# Prepare input for a specific engine
engine_input = state.prepare_for_engine("llm")

# Process output from an engine
state.merge_engine_output("llm", engine_output)
```

## Common Patterns

### Pattern 1: Message-Based State

The most common pattern for conversational agents:

```python
from haive.core.schema import create_message_state

# Quick creation with message field
ConversationState = create_message_state({
    "topic": (str, Field(default="general chat")),
    "speaker_count": (int, Field(default=0))
})

# Use in your agent
state = ConversationState()
state.add_message(HumanMessage(content="Hello!"))
state.add_messages([AIMessage(content="Hi there!")])
```

### Pattern 2: Multi-Engine State

For complex workflows with multiple engines:

```python
from haive.core.schema import SchemaComposer

# Compose from engines
engines = [retriever_engine, reranker_engine, llm_engine]
RAGState = SchemaComposer.from_components(
    engines,
    name="RAGState",
    additional_fields={
        "metadata": (Dict[str, Any], Field(default_factory=dict))
    }
)
```

### Pattern 3: Hierarchical State

For parent-child graph relationships:

```python
# Parent state
class ParentState(StateSchema):
    messages: List[BaseMessage] = Field(default_factory=list)
    global_context: str = Field(default="")
    results: List[str] = Field(default_factory=list)

    __shared_fields__ = ["messages", "global_context"]

# Child state
class ChildState(StateSchema):
    messages: List[BaseMessage] = Field(default_factory=list)  # From parent
    global_context: str = Field(default="")  # From parent
    local_data: str = Field(default="")  # Local only

    __shared_fields__ = ["messages", "global_context"]
    __reducer_fields__ = {
        "messages": add_messages,
        "results": operator.add
    }
```

### Pattern 4: Streaming State

For real-time streaming applications:

```python
class StreamingState(StateSchema):
    chunks: List[str] = Field(default_factory=list)
    buffer: str = Field(default="")
    is_complete: bool = Field(default=False)

    __reducer_fields__ = {
        "chunks": operator.add,
        "buffer": lambda old, new: new,  # Replace buffer
        "is_complete": lambda old, new: old or new  # Once true, stays true
    }

    def flush_buffer(self) -> str:
        """Flush buffer and return content."""
        content = self.buffer
        self.buffer = ""
        return content
```

### Pattern 5: Validation State

For states requiring complex validation:

```python
from pydantic import validator

class ValidatedState(StateSchema):
    email: str = Field(default="")
    age: int = Field(default=0)
    tags: List[str] = Field(default_factory=list)

    @validator("email")
    def validate_email(cls, v):
        if v and "@" not in v:
            raise ValueError("Invalid email format")
        return v

    @validator("age")
    def validate_age(cls, v):
        if v < 0 or v > 150:
            raise ValueError("Age must be between 0 and 150")
        return v

    @validator("tags")
    def validate_tags(cls, v):
        return list(set(v))  # Remove duplicates
```

## Best Practices

### 1. Schema Definition

**Define Schemas Declaratively** when possible for clarity:

```python
class MyState(StateSchema):
    messages: List[BaseMessage] = Field(default_factory=list)
    query: str = Field(default="")
```

**Use Type Aliases** for complex types:

```python
from typing import TypeAlias

DocumentType: TypeAlias = Dict[str, Union[str, List[str], Dict[str, Any]]]

class DocumentState(StateSchema):
    documents: List[DocumentType] = Field(default_factory=list)
```

### 2. Dynamic Composition

**Use SchemaComposer** for runtime schema building:

```python
# From components
schema = SchemaComposer.from_components(components)

# With builder pattern
composer = SchemaComposer(name="CustomState")
composer.add_field("field1", str, default="")
composer.add_field("field2", int, default=0)
schema = composer.build()
```

### 3. Field Management

**Always Configure Message Fields** with appropriate reducers:

```python
composer.configure_messages_field(with_reducer=True)
```

**Use Appropriate Reducers** for different field types:

- `add_messages` for message lists
- `operator.add` for regular lists and numbers
- Custom lambdas for replace behavior
- Custom functions for complex merging

### 4. State Sharing

**Mark Shared Fields Explicitly** to control parent-child communication:

```python
__shared_fields__ = ["messages", "context"]
```

**Consider Reducer Behavior** when sharing fields:

```python
# Shared fields should have compatible reducers
__reducer_fields__ = {
    "messages": add_messages,  # Standard for messages
    "context": operator.add    # Accumulate context
}
```

### 5. Engine Integration

**Track Engine I/O Relationships**:

```python
__engine_io_mappings__ = {
    "retriever": {
        "inputs": ["query"],
        "outputs": ["context", "sources"]
    },
    "llm": {
        "inputs": ["query", "context"],
        "outputs": ["response"]
    }
}
```

**Prepare State for Engines**:

```python
# Extract only relevant fields
engine_input = state.prepare_for_engine("retriever")

# Merge results back
state.merge_engine_output("retriever", {"context": [...]})
```

### 6. Validation and Safety

**Validate Before Creation**:

```python
try:
    state = MyState.model_validate(data)
except ValidationError as e:
    logger.error(f"Invalid state data: {e}")
    # Handle error appropriately
```

**Use Type Guards**:

```python
from typing import TypeGuard

def is_valid_state(obj: Any) -> TypeGuard[MyState]:
    return (
        hasattr(obj, "messages") and
        hasattr(obj, "query") and
        isinstance(obj.messages, list)
    )
```

### 7. Serialization

**Use Built-in Methods**:

```python
# To JSON
json_data = state.to_json()

# From JSON
restored = MyState.from_json(json_data)

# To dict
state_dict = state.to_dict()

# From dict
restored = MyState.from_dict(state_dict)
```

**Handle Complex Types**:

```python
# Custom serialization for non-standard types
class CustomState(StateSchema):
    data: CustomType = Field(default_factory=CustomType)

    class Config:
        json_encoders = {
            CustomType: lambda v: v.to_dict()
        }
```

### 8. Performance Optimization

**Minimize Field Count**:

```python
# Bad: Too many fields
class OverloadedState(StateSchema):
    field1: str = Field(default="")
    field2: str = Field(default="")
    # ... 50 more fields

# Good: Group related fields
class OrganizedState(StateSchema):
    config: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    messages: List[BaseMessage] = Field(default_factory=list)
```

**Use Lazy Loading**:

```python
class LazyState(StateSchema):
    _large_data: Optional[LargeData] = None

    @property
    def large_data(self) -> LargeData:
        if self._large_data is None:
            self._large_data = self._load_large_data()
        return self._large_data
```

### 9. Testing Schemas

**Create Test Factories**:

```python
def create_test_state(**overrides) -> MyState:
    """Create state with test defaults."""
    defaults = {
        "messages": [HumanMessage(content="Test")],
        "query": "test query"
    }
    defaults.update(overrides)
    return MyState(**defaults)
```

**Test Reducer Behavior**:

```python
def test_message_reducer():
    state = MyState()
    state.apply_reducers({
        "messages": [HumanMessage(content="Hello")]
    })
    assert len(state.messages) == 1

    state.apply_reducers({
        "messages": [AIMessage(content="Hi")]
    })
    assert len(state.messages) == 2
```

## Troubleshooting

### Common Issues

#### 1. Field Name Conflicts

**Problem**: Multiple engines define the same field with different types.

**Solution**:

```python
# Use prefixing
composer = SchemaComposer()
composer.add_fields_from_engine(engine1, prefix="eng1_")
composer.add_fields_from_engine(engine2, prefix="eng2_")
```

#### 2. Reducer Not Applied

**Problem**: Field updates overwrite instead of reducing.

**Solution**:

```python
# Ensure reducer is defined
__reducer_fields__ = {
    "my_field": operator.add  # Don't forget this!
}

# Or use apply_reducers method
state.apply_reducers(update_dict)
```

#### 3. Shared Fields Not Syncing

**Problem**: Updates in child graph don't appear in parent.

**Solution**:

```python
# Both parent and child must list the field
__shared_fields__ = ["messages"]  # In BOTH schemas
```

#### 4. Serialization Errors

**Problem**: Custom types fail to serialize.

**Solution**:

```python
class MyState(StateSchema):
    custom: CustomType = Field(...)

    class Config:
        json_encoders = {
            CustomType: lambda v: v.to_dict(),
            datetime: lambda v: v.isoformat()
        }
```

#### 5. Performance Issues

**Problem**: Large states causing slowdowns.

**Solution**:

```python
# Use selective field updates
state.model_validate_assignment = False  # Disable validation
state.messages.append(msg)  # Direct append
state.model_validate_assignment = True  # Re-enable

# Or use update with specific fields
state.model_update({"messages": new_messages})
```

## Examples

For complete working examples, see the [example.py](example.py) file which demonstrates:

- Basic schema creation and usage
- Dynamic schema composition from engines
- Parent-child state sharing
- Custom reducers and validators
- Schema merging and extension
- Real-world agent state patterns

## API Quick Reference

### StateSchema

| Method                     | Description                |
| -------------------------- | -------------------------- |
| `to_dict()`                | Convert to dictionary      |
| `to_json()`                | Convert to JSON string     |
| `from_dict(data)`          | Create from dictionary     |
| `from_json(json_str)`      | Create from JSON           |
| `apply_reducers(update)`   | Apply update with reducers |
| `add_message(msg)`         | Add single message         |
| `add_messages(msgs)`       | Add multiple messages      |
| `prepare_for_engine(name)` | Get engine inputs          |
| `to_command(goto)`         | Convert to Command         |

### SchemaComposer

| Method                           | Description                |
| -------------------------------- | -------------------------- |
| `add_field(...)`                 | Add single field           |
| `add_fields_from_model(model)`   | Import from Pydantic model |
| `add_fields_from_engine(engine)` | Import from engine         |
| `from_components(components)`    | Create from component list |
| `build()`                        | Generate StateSchema class |
| `merge(composer1, composer2)`    | Merge two composers        |

### StateSchemaManager

| Method                 | Description              |
| ---------------------- | ------------------------ |
| `add_field(...)`       | Add field to schema      |
| `remove_field(name)`   | Remove field             |
| `modify_field(...)`    | Update field properties  |
| `get_model()`          | Get Pydantic model class |
| `add_method(func)`     | Add custom method        |
| `from_components(...)` | Build from components    |

## Conclusion

The Haive Schema System provides a comprehensive foundation for state management in AI agents and workflows. It enables dynamic composition, serialization, and manipulation of schemas at runtime, making it well-suited for complex agent architectures and graph-based workflows.

Key strengths include:

- **Field Sharing**: Enables seamless state flow between parent and child graphs
- **Reducer Functions**: Customizable state update behavior
- **Dynamic Composition**: Build schemas from components at runtime
- **Engine Integration**: Track field-to-engine relationships
- **Serialization**: Full support for serializing and deserializing schemas and states
- **Visualization**: Rich utilities for displaying and working with schemas
- **Type Safety**: Full type hints and runtime validation
- **Extensibility**: Add custom methods, validators, and reducers

By leveraging these capabilities, you can build sophisticated agent systems with clean state management and dynamic behavior. The schema system serves as the backbone for state management across the entire Haive framework.

## See Also

- [Engine System](../engine/README.md) - How engines integrate with schemas
- [Graph System](../graph/README.md) - Using schemas in graphs
- [Agent Base](../../../haive-agents/src/haive/agents/base/README.md) - Schema usage in agents
