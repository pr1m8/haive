# Advanced Pydantic Patterns for Schema Refactoring

## Overview

This document explores advanced Pydantic v2 features that can solve our schema refactoring challenges, particularly around field management, inheritance, and type adaptation.

## 1. Model Post-Init for Field Registration

### **The Pattern**

```python
from pydantic import BaseModel
from typing import Any, Dict

class ImprovedStateSchema(BaseModel):
    """Use model_post_init for automatic field registration"""

    def model_post_init(self, __context: Any) -> None:
        """Runs AFTER all validation - perfect for our needs!"""
        # Register fields automatically
        self._register_fields()
        # Setup field priorities
        self._setup_field_priorities()
        # Sync with parent schemas
        self._sync_inherited_fields()

    def _register_fields(self) -> None:
        """Auto-register all fields with their metadata"""
        for field_name, field_info in self.model_fields.items():
            # Access field metadata
            alias = field_info.alias
            default = field_info.default
            annotation = field_info.annotation

            # Register in our improved system
            FieldRegistry.register(
                name=field_name,
                alias=alias,
                type=annotation,
                metadata=field_info.metadata
            )
```

**Why This Helps**: Solves the "lack of standard way to register fields" problem!

## 2. TypeAdapter for Standalone Field Management

### **The Pattern**

```python
from pydantic import TypeAdapter
from typing import Dict, Any, Type

# Create reusable field validators WITHOUT full models
class FieldTypeAdapter:
    """Lightweight field validation without BaseModel overhead"""

    def __init__(self):
        self.adapters: Dict[str, TypeAdapter] = {}

    def register_field_type(self, name: str, field_type: Type) -> None:
        """Register a field type for validation"""
        self.adapters[name] = TypeAdapter(field_type)

    def validate_field(self, name: str, value: Any) -> Any:
        """Validate a single field value"""
        if name not in self.adapters:
            raise ValueError(f"Unknown field: {name}")
        return self.adapters[name].validate_python(value)

# Use for engine I/O validation without full schemas!
field_adapter = FieldTypeAdapter()
field_adapter.register_field_type("messages", List[str])
validated = field_adapter.validate_field("messages", raw_messages)
```

**Why This Helps**: Solves standalone field validation without schema overhead!

## 3. Discriminated Unions for Node Types

### **The Pattern**

```python
from typing import Literal, Union, Annotated
from pydantic import BaseModel, Field, Discriminator

# Clear node type hierarchy with type safety!
class EngineNode(BaseModel):
    node_type: Literal['engine'] = 'engine'
    engine_ref: str
    input_mapping: Dict[str, str]
    output_mapping: Dict[str, str]

class AgentNode(BaseModel):
    node_type: Literal['agent'] = 'agent'
    agent_ref: str
    state_mapping: Dict[str, str]

class SubgraphNode(BaseModel):
    node_type: Literal['subgraph'] = 'subgraph'
    subgraph: 'BaseGraph'  # Forward reference
    parent_to_sub_mapping: Dict[str, str]
    sub_to_parent_mapping: Dict[str, str]

# Type-safe node union
Node = Annotated[
    Union[EngineNode, AgentNode, SubgraphNode],
    Field(discriminator='node_type')
]

# Now graph nodes are type-safe!
class TypeSafeGraph(BaseModel):
    nodes: Dict[str, Node]  # Not Any!
```

**Why This Helps**: Solves the "graph accepts anything" problem with type-safe nodes!

## 4. Computed Fields for Dynamic Schema Composition

### **The Pattern**

```python
from pydantic import BaseModel, computed_field
from functools import cached_property

class DynamicSchema(BaseModel):
    """Schema with dynamic field composition"""
    base_fields: Dict[str, FieldDefinition]
    inherited_fields: Dict[str, FieldDefinition] = {}
    mixin_fields: Dict[str, FieldDefinition] = {}

    @computed_field
    @cached_property
    def all_fields(self) -> Dict[str, FieldDefinition]:
        """Dynamically compute all fields with priority resolution"""
        # Merge with priority: mixin > base > inherited
        merged = {**self.inherited_fields}
        merged.update(self.base_fields)
        merged.update(self.mixin_fields)
        return merged

    @computed_field
    @property
    def shared_fields(self) -> Set[str]:
        """Compute shared fields dynamically"""
        return {
            name for name, field in self.all_fields.items()
            if field.metadata.get('shared', False)
        }
```

**Why This Helps**: Dynamic schema composition without monolithic classes!

## 5. Advanced Validators with Context

### **The Pattern**

```python
from pydantic import BaseModel, field_validator, model_validator
from pydantic.functional_validators import ValidationInfo

class ContextAwareSchema(BaseModel):
    fields: Dict[str, Any]
    context: str = "default"

    @field_validator('fields', mode='before')
    @classmethod
    def adapt_fields_for_context(cls, v: Any, info: ValidationInfo) -> Any:
        """Adapt fields based on context before validation"""
        context = info.data.get('context', 'default')

        if context == 'llm_input':
            # Transform field names for LLM
            return {to_llm_name(k): v for k, v in v.items()}
        elif context == 'api_output':
            # Transform for API
            return {to_api_name(k): v for k, v in v.items()}

        return v

    @model_validator(mode='after')
    def validate_field_consistency(self) -> 'ContextAwareSchema':
        """Post-validation consistency checks"""
        # Validate field relationships
        # Check for required field combinations
        # Ensure no conflicting fields
        return self
```

**Why This Helps**: Context-aware validation for different use cases!

## 6. Custom Serialization for Field Syncing

### **The Pattern**

```python
from pydantic import BaseModel, field_serializer, model_serializer

class SyncableSchema(BaseModel):
    """Schema with field syncing capabilities"""
    fields: Dict[str, Any]
    _sync_rules: Dict[str, List[str]] = {}  # Private attribute
    _field_aliases: Dict[str, str] = {}

    @field_serializer('fields')
    def serialize_with_sync_info(self, fields: Dict[str, Any]) -> Dict[str, Any]:
        """Include sync metadata in serialization"""
        serialized = {}
        for name, value in fields.items():
            serialized[name] = {
                'value': value,
                'syncs_with': self._sync_rules.get(name, []),
                'aliases': [self._field_aliases.get(name, name)]
            }
        return serialized

    def sync_field(self, source: str, targets: List[str]) -> None:
        """Register field sync rule"""
        self._sync_rules[source] = targets
```

**Why This Helps**: Built-in field syncing without external systems!

## 7. Generic Models for Type-Safe Schemas

### **The Pattern**

```python
from typing import Generic, TypeVar
from pydantic import BaseModel

TState = TypeVar('TState', bound=BaseModel)
TInput = TypeVar('TInput', bound=BaseModel)
TOutput = TypeVar('TOutput', bound=BaseModel)

class TypeSafeAgent(BaseModel, Generic[TState, TInput, TOutput]):
    """Agent with full type safety"""
    state_schema: Type[TState]
    input_schema: Type[TInput]
    output_schema: Type[TOutput]

    def validate_state(self, data: Dict[str, Any]) -> TState:
        """Type-safe state validation"""
        return self.state_schema.model_validate(data)

    def transform_input(self, state: TState) -> TInput:
        """Type-safe input transformation"""
        # Transform with type safety
        pass

# Use with specific types
class MyState(BaseModel):
    messages: List[str]

class MyInput(BaseModel):
    query: str

class MyOutput(BaseModel):
    response: str

agent = TypeSafeAgent[MyState, MyInput, MyOutput](
    state_schema=MyState,
    input_schema=MyInput,
    output_schema=MyOutput
)
```

**Why This Helps**: Full type safety through the entire system!

## 8. RootModel for Lightweight Field Containers

### **The Pattern**

```python
from pydantic import RootModel
from typing import Dict, Any

class FieldCollection(RootModel[Dict[str, FieldDefinition]]):
    """Lightweight field container without BaseModel overhead"""

    def add_field(self, name: str, field: FieldDefinition) -> None:
        self.root[name] = field

    def merge_with_priority(self, other: 'FieldCollection') -> 'FieldCollection':
        """Merge with another collection respecting priorities"""
        merged = self.root.copy()
        for name, field in other.root.items():
            if name not in merged or field.priority > merged[name].priority:
                merged[name] = field
        return FieldCollection(merged)

    def filter_shared(self) -> 'FieldCollection':
        """Get only shared fields"""
        shared = {k: v for k, v in self.root.items() if v.shared}
        return FieldCollection(shared)
```

**Why This Helps**: Efficient field management without full model overhead!

## 9. Improved Mixin Pattern with model_post_init

### **The Pattern**

```python
class FieldManagementMixin:
    """Consistent mixin pattern using model_post_init"""

    def model_post_init(self, __context: Any) -> None:
        # ALWAYS call parent first
        try:
            super().model_post_init(__context)
        except AttributeError:
            pass

        # Then do mixin initialization
        self._init_field_management()

    def _init_field_management(self):
        """Initialize field management capabilities"""
        self._field_registry = {}
        self._register_existing_fields()

class EngineAccessMixin:
    """Another mixin following same pattern"""

    def model_post_init(self, __context: Any) -> None:
        try:
            super().model_post_init(__context)
        except AttributeError:
            pass

        self._init_engine_access()

# Combine consistently!
class ImprovedSchema(FieldManagementMixin, EngineAccessMixin, BaseModel):
    """All mixins initialize properly through model_post_init chain"""
    fields: Dict[str, Any] = {}
```

**Why This Helps**: Consistent mixin initialization pattern!

## 10. Forward References and Deferred Building

### **The Pattern**

```python
from pydantic import BaseModel
from typing import Optional, ForwardRef

# Define with forward reference
class GraphNode(BaseModel):
    subgraph: Optional['Graph'] = None  # Forward reference

    model_config = {
        # Allow forward references
        'defer_build': True
    }

class Graph(BaseModel):
    nodes: Dict[str, GraphNode]

# Update forward references after all classes defined
GraphNode.model_rebuild()
```

**Why This Helps**: Handle circular dependencies in graph structures!

## How These Patterns Solve Our Problems

### **1. Field Registration**

- `model_post_init` provides standard initialization point
- TypeAdapter enables standalone validation
- RootModel for lightweight containers

### **2. Type Safety**

- Discriminated unions for node types
- Generic models for type parameters
- Forward references for circular dependencies

### **3. Dynamic Composition**

- Computed fields for dynamic schema assembly
- Context-aware validators
- Custom serializers for field syncing

### **4. Inheritance Consistency**

- Standard mixin pattern with model_post_init
- Clear initialization order
- No more random mixin application

### **5. Advanced Features**

- Built-in field priorities
- Automatic sync rules
- Context-aware adaptation

These Pydantic v2 features provide the foundation for a robust, type-safe schema refactoring that solves the core architectural issues!
