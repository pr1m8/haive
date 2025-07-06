# Engine-State Mapping Analysis

## Current State of the System

Based on my research, here's how the engine/state/node system currently works:

### 1. Three Overlapping Systems

```python
# 1. StateSchema - Defines engine I/O mappings at the schema level
class StateSchema:
    __engine_io_mappings__ = {
        "retriever": {
            "inputs": ["query"],
            "outputs": ["context"]
        },
        "llm": {
            "inputs": ["query", "context", "messages"],
            "outputs": ["response"]
        }
    }

# 2. NodeFactory - Extracts/maps state at runtime
class NodeFactory:
    def _extract_input(cls, state, input_mapping: dict[str, str]):
        # Maps state fields to engine input
        # e.g., {"query": "user_question"} maps state.query to engine's user_question

    def _process_result(cls, result, state, output_mapping: dict[str, str]):
        # Maps engine output back to state
        # e.g., {"response": "assistant_message"}

# 3. Engine - Defines its own I/O schema
class Engine(Generic[TIn, TOut]):
    def get_input_fields(self) -> Dict[str, Tuple[Type, Any]]:
        # Returns field definitions like {"prompt": (str, ""), "temperature": (float, 0.7)}

    def derive_input_schema(self) -> Type[BaseModel]:
        # Creates Pydantic model from fields - loses generic type info!
```

### 2. The Type Safety Problem

The current system loses type information at multiple levels:

```python
# Engine defines generic types
class MyEngine(InvokableEngine[InputModel, OutputModel]):
    # TIn = InputModel, TOut = OutputModel
    pass

# But when deriving schemas:
def derive_input_schema(self) -> Type[BaseModel]:
    fields = self.get_input_fields()  # Dict[str, Tuple[Type, Any]]
    return create_model(f"{self.__class__.__name__}Input", **fields)
    # Returns Type[BaseModel], not Type[InputModel]!

# And in NodeFactory:
def _extract_input(cls, state, input_mapping) -> Any:  # Returns Any!
    # No type preservation
```

### 3. State Mapping Duplication

The same mapping logic exists in multiple places:

```python
# In StateSchema
__engine_io_mappings__ = {
    "engine_name": {
        "inputs": ["field1", "field2"],
        "outputs": ["result"]
    }
}

# In NodeConfig/NodeFactory
input_mapping = {"state_field": "engine_field"}
output_mapping = {"engine_output": "state_field"}

# In SchemaComposer
# Tracks field mappings during schema composition
```

## Key Issues

### 1. **No Single Source of Truth**

- StateSchema has `__engine_io_mappings__`
- NodeFactory has `input_mapping`/`output_mapping`
- Engines have `get_input_fields()`/`get_output_fields()`
- All can conflict!

### 2. **Type Information Lost**

- Engine generics (`TIn`, `TOut`) not preserved
- Everything becomes `Any` or `BaseModel`
- No compile-time type safety

### 3. **Complex State Extraction**

The `_extract_input` method has to handle:

- Pydantic v1 models (`.dict()`)
- Pydantic v2 models (`.model_dump()`)
- Plain dicts
- Other objects
- Special cases for single fields

### 4. **Node as State Adapter**

Nodes are essentially state adapters that:

1. Extract data from state using mappings
2. Convert to engine input format
3. Call engine
4. Convert output back to state format

## Proposed Solutions

### Solution 1: Unified Type-Safe Mapping

```python
from typing import Protocol, TypeVar, Generic
from pydantic import BaseModel, TypeAdapter

TState = TypeVar("TState", bound=BaseModel)
TInput = TypeVar("TInput", bound=BaseModel)
TOutput = TypeVar("TOutput", bound=BaseModel)

class StateMapping(Generic[TState, TInput, TOutput]):
    """Type-safe state mapping definition."""

    def __init__(
        self,
        state_type: type[TState],
        input_type: type[TInput],
        output_type: type[TOutput],
        input_mapping: dict[str, str] | Callable[[TState], TInput],
        output_mapping: dict[str, str] | Callable[[TState, TOutput], TState],
    ):
        self.state_adapter = TypeAdapter(state_type)
        self.input_adapter = TypeAdapter(input_type)
        self.output_adapter = TypeAdapter(output_type)
        self.input_mapping = input_mapping
        self.output_mapping = output_mapping

    def extract_input(self, state: TState) -> TInput:
        """Type-safe input extraction."""
        if callable(self.input_mapping):
            return self.input_mapping(state)

        # Field mapping
        input_dict = {}
        for state_field, input_field in self.input_mapping.items():
            value = getattr(state, state_field)
            input_dict[input_field] = value

        return self.input_adapter.validate_python(input_dict)

    def merge_output(self, state: TState, output: TOutput) -> TState:
        """Type-safe output merging."""
        if callable(self.output_mapping):
            return self.output_mapping(state, output)

        # Field mapping
        state_dict = state.model_dump()
        for output_field, state_field in self.output_mapping.items():
            value = getattr(output, output_field)
            state_dict[state_field] = value

        return self.state_adapter.validate_python(state_dict)
```

### Solution 2: Engine-Aware Nodes

```python
class TypedNode(Generic[TState, TInput, TOutput]):
    """Node that preserves type information."""

    def __init__(
        self,
        engine: Engine[TInput, TOutput],
        mapping: StateMapping[TState, TInput, TOutput],
    ):
        self.engine = engine
        self.mapping = mapping

    async def execute(self, state: TState) -> TState:
        """Execute with full type safety."""
        # Extract input with types preserved
        input_data = self.mapping.extract_input(state)

        # Execute engine - types match!
        output = await self.engine.invoke(input_data)

        # Merge back with types preserved
        return self.mapping.merge_output(state, output)
```

### Solution 3: Declarative Mapping

```python
from typing import Annotated

class MyState(StateSchema):
    # Use annotations to declare mappings
    user_query: Annotated[str, EngineInput("llm", "prompt")]
    assistant_response: Annotated[str, EngineOutput("llm", "response")]
    documents: Annotated[list[Document], EngineOutput("retriever", "results")]

    # No more __engine_io_mappings__ needed!
```

### Solution 4: Simplified Node Creation

```python
@node_from_engine(
    engine=my_llm_engine,
    extract_input=lambda state: {"prompt": state.query},
    merge_output=lambda state, output: state.model_copy(
        update={"response": output.text}
    )
)
async def llm_node(state: MyState) -> MyState:
    # Decorator handles all the mapping
    pass
```

## Recommendations

1. **Start with StateMapping Protocol** - Define a clear interface for state mapping
2. **Use TypeAdapter** - Leverage Pydantic v2's TypeAdapter for conversions
3. **Preserve Generic Types** - Keep TIn/TOut through the entire flow
4. **Single Mapping Definition** - One place to define how state maps to engines
5. **Backwards Compatibility** - Adapter pattern for old-style mappings

## Next Steps

1. Create proof-of-concept StateMapping implementation
2. Test with existing engines
3. Create adapters for legacy mappings
4. Gradually migrate nodes to new system
