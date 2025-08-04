# Base Engine System Review

## Current Architecture Overview

The engine system follows a configuration/factory pattern with clear type hierarchies:

### 1. Core Type Hierarchy

```python
# Base abstract class
class Engine(ABC, BaseModel, Generic[TIn, TOut]):
    """Configuration/factory for creating runtime objects"""

    # Core identification
    id: str
    name: str
    engine_type: EngineType
    description: Optional[str]

    # Optional explicit schemas
    input_schema: Optional[Type[BaseModel]]
    output_schema: Optional[Type[BaseModel]]

    # Abstract methods that subclasses must implement
    @abstractmethod
    def get_input_fields(self) -> Dict[str, Tuple[Type, Any]]

    @abstractmethod
    def get_output_fields(self) -> Dict[str, Tuple[Type, Any]]

    @abstractmethod
    def create_runnable(self, config: Optional[RunnableConfig] = None) -> Any

# Two main branches
class InvokableEngine(Engine[TIn, TOut]):
    """Creates runtime objects that can be invoked (LLM, Retriever, VectorStore)"""

    def invoke(self, input_data: TIn, config=None) -> TOut:
        # Creates runnable and invokes it

    async def ainvoke(self, input_data: TIn, config=None) -> TOut:
        # Async version

class NonInvokableEngine(Engine[TIn, TOut]):
    """Creates utility objects (Embeddings, DocumentLoader, etc.)"""
    pass  # Just inherits from Engine
```

### 2. Engine Types (11 Total)

```python
class EngineType(str, Enum):
    LLM = "llm"                           # Text generation
    VECTOR_STORE = "vector_store"         # Vector storage/search
    RETRIEVER = "retriever"               # Information retrieval
    TOOL = "tool"                         # Function execution
    EMBEDDINGS = "embeddings"             # Text → vectors
    AGENT = "agent"                       # Autonomous agents
    DOCUMENT_LOADER = "document_loader"   # Load documents
    DOCUMENT_TRANSFORMER = "document_transformer"  # Transform docs
    DOCUMENT_SPLITTER = "document_splitter"       # Split docs
    OUTPUT_PARSER = "output_parser"       # Parse LLM output
    PROMPT = "prompt"                     # Prompt templates
```

### 3. Protocol System

```python
@runtime_checkable
class Invocable(Protocol[I, O]):
    def invoke(self, input_data: I, **kwargs) -> O: ...

@runtime_checkable
class AsyncInvokable(Protocol[I, O]):
    async def ainvoke(self, input_data: I, **kwargs) -> O: ...
```

## Strengths of Current System

### 1. **Clear Separation of Concerns**

- Engines are configuration objects, not runtime objects
- Runtime objects created by `create_runnable()`
- Type safety through generics `Engine[TIn, TOut]`

### 2. **Good Type System Foundation**

- Generic types `TIn`/`TOut` for input/output
- Protocol-based invocation contracts
- Runtime type checking with `@runtime_checkable`

### 3. **Comprehensive Engine Types**

- Covers all major AI/ML components
- Clear categorization (invocable vs non-invocable)
- Extensible enum system

### 4. **Registration & Discovery**

- Central `EngineRegistry` for lookup
- Support for ID, name, and type-based retrieval
- Serialization support with `to_dict()`/`from_dict()`

### 5. **Configuration Management**

- Hierarchical config application (ID > name > type)
- `apply_runnable_config()` extracts relevant parameters
- Support for runtime configuration overrides

## Issues & Areas for Improvement

### 1. **Type Information Loss**

**Problem**: Generic types are lost in schema derivation

```python
# Engine defines TIn/TOut
class MyEngine(InvokableEngine[InputModel, OutputModel]): ...

# But derive_input_schema() returns generic BaseModel
def derive_input_schema(self) -> Type[BaseModel]:  # Lost TIn!
    fields = self.get_input_fields()  # Dict[str, Tuple[Type, Any]]
    return create_model(f"{self.__class__.__name__}Input", **fields)
```

**Impact**:

- No compile-time type checking
- Runtime type validation only
- IDE doesn't know actual types

### 2. **Field Definition Complexity**

**Current Approach**: Abstract methods return field dictionaries

```python
def get_input_fields(self) -> Dict[str, Tuple[Type, Any]]:
    return {
        "prompt": (str, ""),
        "temperature": (float, 0.7),
        "max_tokens": (int, 1000)
    }
```

**Issues**:

- Manual field definition (error-prone)
- No IDE support for field names
- Redundant with Pydantic model fields
- Type information as strings/tuples

### 3. **Schema Integration Gaps**

**Missing Connections**:

- No direct link between Engine generics and StateSchema
- Node mappings separate from engine schemas
- No automatic state extraction based on engine types

### 4. **Tool Engine Confusion**

**Problem**: Tools are engines but also called by engines

```python
# Is this a tool that IS an engine?
class CalculatorTool(InvokableEngine[dict, dict]):
    engine_type = EngineType.TOOL

# Or an engine that USES tools?
class ToolEngine(InvokableEngine):
    tools: List[SomeTool]
```

## Proposed Improvements

### 1. **Preserve Generic Types Through Schema Generation**

```python
class TypeSafeEngine(Engine[TIn, TOut]):
    """Engine that preserves type information through schema derivation."""

    # Explicitly typed schemas (preserve generics)
    input_type: Type[TIn] = Field(..., exclude=True)
    output_type: Type[TOut] = Field(..., exclude=True)

    def derive_input_schema(self) -> Type[TIn]:  # Returns TIn, not BaseModel!
        if self.input_schema:
            return self.input_schema
        return self.input_type

    def derive_output_schema(self) -> Type[TOut]:  # Returns TOut!
        if self.output_schema:
            return self.output_schema
        return self.output_type

    # Auto-generate fields from type annotations
    def get_input_fields(self) -> Dict[str, Tuple[Type, Any]]:
        if hasattr(self.input_type, "model_fields"):
            return {
                name: (field.annotation, field.default)
                for name, field in self.input_type.model_fields.items()
            }
        return {}
```

### 2. **Schema-Aware Engine Base**

```python
from typing import get_type_hints

class SchemaAwareEngine(TypeSafeEngine[TIn, TOut]):
    """Engine that integrates with schema registry."""

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        # Auto-extract type parameters
        hints = get_type_hints(cls)
        if hasattr(cls, "__orig_bases__"):
            for base in cls.__orig_bases__:
                if hasattr(base, "__args__") and len(base.__args__) == 2:
                    cls.input_type = base.__args__[0]
                    cls.output_type = base.__args__[1]
                    break

        # Auto-register schemas
        from haive.core.schema.registry import SchemaRegistry
        registry = SchemaRegistry.get_instance()

        engine_name = cls.engine_type.value
        registry.register_schema(f"{engine_name}.input", cls.input_type, "engine")
        registry.register_schema(f"{engine_name}.output", cls.output_type, "engine")
```

### 3. **Simplified Engine Definition**

```python
# Instead of manual field definitions:
class LLMEngine(SchemaAwareEngine[LLMInput, LLMOutput]):
    engine_type = EngineType.LLM

    # No need for get_input_fields/get_output_fields!
    # Auto-derived from type parameters

    def create_runnable(self, config=None):
        # Just implement this
        return SomeLLM(...)

# Type-safe usage:
engine = LLMEngine(name="gpt-4")
input_schema = engine.derive_input_schema()  # Returns Type[LLMInput]
input_data = input_schema(prompt="Hello", temperature=0.7)
output = engine.invoke(input_data)  # Type: LLMOutput
```

### 4. **Registry Integration**

```python
# Engines auto-register their schemas
@engine_type(EngineType.LLM)
class GPT4Engine(SchemaAwareEngine[LLMInput, LLMOutput]):
    model: str = "gpt-4"
    temperature: float = 0.7

    # Auto-registers:
    # - "llm.input" -> LLMInput
    # - "llm.output" -> LLMOutput
    # - Engine instance in registry

# Usage with registry
engine = EngineRegistry.get(EngineType.LLM, "gpt-4")
input_schema = SchemaRegistry.get("llm.input")  # Type[LLMInput]
```

## Compatibility Strategy

### 1. **Gradual Migration**

- Keep existing `Engine` base class
- Add `SchemaAwareEngine` as optional upgrade path
- Provide adapters for old-style engines

### 2. **Backwards Compatibility**

```python
class LegacyEngineAdapter(SchemaAwareEngine):
    """Adapter for old-style engines."""

    def __init__(self, legacy_engine: Engine):
        self.legacy = legacy_engine
        # Convert field definitions to types
        input_fields = legacy_engine.get_input_fields()
        self.input_type = create_model("Input", **input_fields)
        # etc.
```

## Next Steps

1. **Implement TypeSafeEngine** - Preserve generics through schema generation
2. **Create SchemaAwareEngine** - Auto-registration and type extraction
3. **Build registry integration** - Seamless schema/engine lookup
4. **Create adapters** - Support existing engines
5. **Update NodeFactory** - Use type-safe engines with nodes

Would you like me to start implementing the `TypeSafeEngine` or focus on a different aspect?
