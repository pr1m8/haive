# Schema Composer Analysis

**Memory Tag**: [MEM-101-B]  
**Parent**: [MEM-101] Schema Analysis  
**Related**: [MEM-101-A] State Schema Patterns, [MEM-102] Agent Patterns  
**Date**: 2025-01-06

## 🎯 Purpose

Deep understanding of SchemaComposer - the dynamic schema building system that creates state schemas from various components.

## 📊 SchemaComposer Overview

### Core Concept

SchemaComposer provides a streamlined API for building state schemas dynamically by:

- Extracting fields from multiple components (engines, models, dicts)
- Managing field definitions with comprehensive metadata
- Handling field sharing, reducers, and engine I/O mappings
- Creating complex state schemas through composition

### Key Components

```python
class SchemaComposer:
    """Dynamic schema builder for the Haive framework."""

    def __init__(self, name: str = "DynamicSchema"):
        self.name = name
        self.fields: Dict[str, FieldDefinition] = {}
        self.base_classes = []

    def add_field(
        self,
        name: str,
        field_type: Type,
        default=None,
        default_factory=None,
        description="",
        shared=False,
        reducer=None,
        engine_inputs=None,
        engine_outputs=None
    ):
        """Add a single field with full metadata."""

    def add_fields_from_model(self, model: Type[BaseModel]):
        """Extract and add fields from a Pydantic model."""

    def add_fields_from_components(self, components: List[Any]):
        """Extract fields from multiple components."""

    def build(self) -> Type[StateSchema]:
        """Build the final StateSchema class."""
```

## 🔍 Field Extraction Process

### 1. Component Analysis

```python
# Components can be:
- Engine instances (LLM, Retriever, etc.)
- Pydantic models
- Dictionaries with field definitions
- Other StateSchema classes
```

### 2. Field Definition Creation

```python
class FieldDefinition:
    """Complete field metadata."""
    name: str
    field_type: Type
    default: Any
    default_factory: Optional[Callable]
    description: str
    shared: bool = False
    reducer: Optional[Union[str, Callable]]
    engine_inputs: List[str] = []
    engine_outputs: List[str] = []
```

### 3. Schema Building

```python
# Building process:
1. Collect all field definitions
2. Create Pydantic field specs
3. Generate class attributes (__shared_fields__, etc.)
4. Use create_model() to build final class
5. Return StateSchema subclass
```

## 💡 Key Patterns

### Automatic Field Discovery

```python
# From engines
composer.add_fields_from_components([llm_engine, retriever_engine])
# Automatically extracts:
# - Input fields (query, context, etc.)
# - Output fields (response, documents, etc.)
# - State fields (messages, history, etc.)
```

### Field Sharing Configuration

```python
# Shared fields are accessible to parent/child graphs
composer.add_field(
    name="messages",
    field_type=List[BaseMessage],
    default_factory=list,
    shared=True,  # Available to parent graphs
    reducer="add_messages"  # How to merge updates
)
```

### Engine I/O Mapping

```python
# Track which fields are inputs/outputs for engines
composer.add_field(
    name="query",
    field_type=str,
    engine_inputs=["retriever", "llm"],  # Used by these engines
    engine_outputs=[]  # Not produced by engines
)
```

## 🏗️ Common Usage Patterns

### 1. Building from Engines

```python
# Agent with multiple engines
composer = SchemaComposer("AgentState")
composer.add_fields_from_components([
    llm_engine,      # Adds: messages, response
    retriever,       # Adds: query, documents
    memory_store     # Adds: history, context
])
state_schema = composer.build()
```

### 2. Manual Field Addition

```python
# Custom fields with metadata
composer.add_field(
    name="tool_results",
    field_type=List[Dict],
    default_factory=list,
    description="Results from tool execution",
    shared=True,
    reducer=lambda a, b: a + b
)
```

### 3. Extending Existing Schemas

```python
# Build on existing schema
composer = SchemaComposer("ExtendedState")
composer.add_fields_from_model(MessagesState)
composer.add_field("custom_field", str, default="")
extended_schema = composer.build()
```

## 🐛 Common Issues

### 1. Field Type Conflicts

**Problem**: Different components define same field with different types  
**Solution**: SchemaComposer handles by:

- Using Union types when compatible
- Preferring more specific types
- Warning on incompatible types

### 2. Missing Reducers

**Problem**: Shared fields without reducers cause merge issues  
**Solution**: Always specify reducer for shared fields

```python
composer.add_field(
    name="items",
    field_type=List[str],
    shared=True,
    reducer=operator.add  # Concatenate lists
)
```

### 3. Circular Dependencies

**Problem**: Components reference each other  
**Solution**: Extract fields in dependency order

## 🎯 Best Practices

1. **Name schemas descriptively**: "ConversationState" not "State1"
2. **Document fields**: Use description parameter
3. **Configure sharing explicitly**: Mark shared fields
4. **Define reducers**: For all list/dict fields
5. **Track engine I/O**: Document data flow

## 🔗 Integration with Agent System

### In Agent Base Class

```python
class Agent:
    def _setup_schemas(self):
        # Use SchemaComposer to build from engines
        self.state_schema = SchemaComposer.from_components(
            components=engine_list,
            name=f"{self.__class__.__name__}State"
        )
```

### In Multi-Agent Systems

```python
# AgentSchemaComposer extends SchemaComposer
# Handles sub-agent schemas specially
schema = AgentSchemaComposer.from_agents(
    agents=[agent1, agent2],
    separation="smart"  # Avoid field conflicts
)
```

## 📈 Advanced Features

### 1. Smart Field Merging

- Detects compatible types
- Merges descriptions
- Combines engine mappings

### 2. Reducer Inference

- Common patterns auto-detected
- List fields → operator.add
- Message fields → add_messages

### 3. Visualization

```python
composer.display()  # Rich table of fields
composer.visualize()  # Tree structure
```

## 🔗 Cross-References

- StateSchema base: [MEM-101-A]
- Agent schema generation: [MEM-102-A]
- Multi-agent composition: [MEM-101-D]
- Field utilities: [MEM-104-A]

---

**Status**: Core understanding documented
**Last Updated**: 2025-01-06
