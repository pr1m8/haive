# Protocol Contracts Proposal - Haive v3.0

**Created**: 2025-01-30  
**Purpose**: Define clear protocol contracts for all components  
**Goal**: Reduce complexity from 82🔥 to <20🔥

## 🎯 Core Protocols

### 1. Executable Protocol

```python
from typing import Protocol, TypeVar, Generic
from pydantic import BaseModel

TInput = TypeVar("TInput", bound=BaseModel)
TOutput = TypeVar("TOutput", bound=BaseModel)

class Executable(Protocol[TInput, TOutput]):
    """Anything that can execute with typed I/O"""

    def execute(self, input: TInput) -> TOutput:
        """Execute the operation"""
        ...

    async def aexecute(self, input: TInput) -> TOutput:
        """Async execution"""
        ...
```

### 2. Factory Protocol

```python
TProduct = TypeVar("TProduct")

class Factory(Protocol[TProduct]):
    """Creates instances of a type"""

    def create(self, **config) -> TProduct:
        """Create an instance"""
        ...

    def get_config_schema(self) -> type[BaseModel]:
        """Get configuration schema"""
        ...
```

### 3. Schema Provider Protocol

```python
class SchemaProvider(Protocol):
    """Provides schema information"""

    @property
    def input_schema(self) -> type[BaseModel]:
        """Input schema for this component"""
        ...

    @property
    def output_schema(self) -> type[BaseModel]:
        """Output schema for this component"""
        ...

    def validate_input(self, input: Any) -> BaseModel:
        """Validate and coerce input"""
        ...

    def validate_output(self, output: Any) -> BaseModel:
        """Validate and coerce output"""
        ...
```

### 4. State Manager Protocol

```python
TState = TypeVar("TState", bound=BaseModel)

class StateManager(Protocol[TState]):
    """Manages state lifecycle"""

    def get_state(self) -> TState:
        """Get current state"""
        ...

    def update_state(self, updates: dict) -> TState:
        """Update state with changes"""
        ...

    def reset_state(self) -> TState:
        """Reset to initial state"""
        ...

    def checkpoint(self) -> str:
        """Create state checkpoint"""
        ...

    def restore(self, checkpoint_id: str) -> TState:
        """Restore from checkpoint"""
        ...
```

### 5. Injectable Protocol

```python
class Injectable(Protocol[TInput, TOutput, TState]):
    """Component that receives injected dependencies"""

    @property
    def dependencies(self) -> dict[str, type]:
        """Required dependencies"""
        ...

    def inject(self, **deps) -> None:
        """Inject dependencies"""
        ...

    def execute_with_injection(
        self,
        input: TInput,
        state: TState
    ) -> TOutput:
        """Execute with injected state"""
        ...
```

## 🔧 Component Contracts

### Engine Contract

```python
class EngineContract(Factory[Executable], SchemaProvider):
    """Engines are factories that create executables"""

    engine_type: str
    name: str

    # From Factory
    def create(self, **config) -> Executable:
        """Create an executable instance"""
        ...

    # From SchemaProvider
    @property
    def input_schema(self) -> type[BaseModel]:
        ...

    @property
    def output_schema(self) -> type[BaseModel]:
        ...

    # Engine specific
    def validate_config(self, config: dict) -> bool:
        """Validate engine configuration"""
        ...
```

### Node Contract

```python
class NodeContract(
    Executable[TInput, TOutput],
    Injectable[TInput, TOutput, TState],
    SchemaProvider
):
    """Nodes are executable, injectable components"""

    node_type: str
    name: str

    # From Executable
    def execute(self, input: TInput) -> TOutput:
        ...

    # From Injectable
    def execute_with_injection(
        self,
        input: TInput,
        state: TState
    ) -> TOutput:
        ...

    # Node specific
    def get_next_node(self, output: TOutput) -> str | None:
        """Determine next node in graph"""
        ...
```

### Agent Contract

```python
class AgentContract(StateManager[TState]):
    """Agents orchestrate execution with state management"""

    name: str

    # Core orchestration
    def orchestrate(self, input: BaseModel) -> BaseModel:
        """Main orchestration logic"""
        ...

    # Graph management
    def get_graph(self) -> GraphContract:
        """Get execution graph"""
        ...

    # Engine management
    def get_engine(self, name: str) -> EngineContract:
        """Get named engine"""
        ...

    # From StateManager
    def get_state(self) -> TState:
        ...

    def update_state(self, updates: dict) -> TState:
        ...
```

### Document Contract

```python
class DocumentContract(Protocol):
    """Document processing contract"""

    @property
    def source(self) -> str:
        """Document source"""
        ...

    @property
    def content(self) -> str:
        """Document content"""
        ...

    @property
    def metadata(self) -> dict:
        """Document metadata"""
        ...

    def chunk(self, size: int, overlap: int) -> list["DocumentContract"]:
        """Split into chunks"""
        ...

    def transform(self, transformer: Callable) -> "DocumentContract":
        """Apply transformation"""
        ...
```

## 🔄 Integration Patterns

### 1. Engine-Node Integration

```python
# Engines create executables for nodes
class LLMNode(NodeContract):
    engine: EngineContract

    def execute(self, input: TInput) -> TOutput:
        # Engine creates executable
        llm_executable = self.engine.create(
            temperature=0.7,
            max_tokens=1000
        )
        # Node uses executable
        return llm_executable.execute(input)
```

### 2. Node-State Integration

```python
# Nodes receive injected state
class StatefulNode(NodeContract):
    def execute_with_injection(
        self,
        input: TInput,
        state: TState
    ) -> TOutput:
        # Use injected state
        config = state.config
        context = state.context

        # Process with state
        result = self.process(input, config, context)

        # Update state if needed
        state.last_result = result

        return result
```

### 3. Agent-Graph Integration

```python
# Agents orchestrate graphs
class GraphAgent(AgentContract):
    def orchestrate(self, input: BaseModel) -> BaseModel:
        # Get graph
        graph = self.get_graph()

        # Get state
        state = self.get_state()

        # Execute graph with state
        result = graph.execute(input, state)

        # Update state
        self.update_state({"last_execution": result})

        return result
```

## 📋 Migration Strategy

### Phase 1: Define Protocols (Week 1)

1. Create protocol definitions
2. Add to `haive.core.protocols` module
3. No breaking changes yet

### Phase 2: Implement Contracts (Week 2-3)

1. Make existing components implement protocols
2. Add adapter classes for backwards compatibility
3. Gradual typing improvements

### Phase 3: Refactor Components (Week 4-5)

1. Remove circular dependencies
2. Separate concerns based on protocols
3. Clean up inheritance mess

### Phase 4: Type Everything (Week 6)

1. Full type annotations
2. Runtime type checking
3. Complete protocol compliance

## 🎯 Success Metrics

| Component     | Before                        | After                       |
| ------------- | ----------------------------- | --------------------------- |
| Engine        | Factory + Config + Executable | Factory[Executable]         |
| Node          | Unclear responsibilities      | Executable + Injectable     |
| Agent         | IS Engine + HAS Engine        | StateManager + Orchestrator |
| Document      | Engine + Tool + Loader        | DocumentContract            |
| Type Safety   | ~0%                           | 100%                        |
| Circular Deps | Many                          | 0                           |

## 💡 Key Benefits

1. **Clear Responsibilities**: Each protocol has ONE job
2. **Composability**: Mix and match protocols as needed
3. **Type Safety**: Full typing with generics
4. **Testability**: Test against protocols, not implementations
5. **Flexibility**: Multiple implementations of same protocol
6. **No Surprises**: Explicit contracts, no hidden behavior

## 🚦 Next Steps

1. **Review and refine protocols**
2. **Create proof-of-concept implementations**
3. **Test with real use cases**
4. **Plan backwards compatibility**
5. **Begin gradual migration**

The protocols provide the **contracts** that will untangle the current 82🔥 mess into a clean, understandable system.
