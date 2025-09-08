# Contract Type System & Relationships

**Created**: 2025-01-07
**Purpose**: Define the type-safe contract system with formal relationships
**Status**: Type system specification for contracts

## 🎯 Core Type Hierarchy

```python
from typing import TypeVar, Generic, Protocol, Type, Callable, Any, Dict, List, Optional
from abc import ABC, abstractmethod
from pydantic import BaseModel, Field

# Type variables for contract generics
StateT = TypeVar('StateT', bound='BaseState')
InputT = TypeVar('InputT', bound=BaseModel)
OutputT = TypeVar('OutputT', bound=BaseModel)
ResourceT = TypeVar('ResourceT', bound='ResourceSpec')

# Protocol for anything that can be contracted
class Contractable(Protocol):
    """Protocol for components that can have contracts."""

    def get_input_schema(self) -> Type[BaseModel]:
        """Return input schema."""
        ...

    def get_output_schema(self) -> Type[BaseModel]:
        """Return output schema."""
        ...

    def execute(self, input: Any) -> Any:
        """Execute the component."""
        ...
```

## 📐 Base Contract Types

```python
class Contract(ABC, Generic[StateT, InputT, OutputT]):
    """Base contract with full type safety."""

    # Type declarations
    state_type: Type[StateT]
    input_type: Type[InputT]
    output_type: Type[OutputT]

    @abstractmethod
    def extract(self, state: StateT) -> InputT:
        """Extract typed input from state."""
        ...

    @abstractmethod
    def execute(self, input: InputT) -> OutputT:
        """Execute with typed input/output."""
        ...

    @abstractmethod
    def update(self, state: StateT, output: OutputT) -> StateT:
        """Update state with typed output."""
        ...

    def __rshift__(self, other: 'Contract') -> 'SequentialContract':
        """Type-safe sequential composition."""
        # Type checker ensures OutputT of self matches InputT of other
        return SequentialContract(self, other)

    def __or__(self, other: 'Contract') -> 'ParallelContract':
        """Type-safe parallel composition."""
        return ParallelContract(self, other)

    def __and__(self, other: 'Contract') -> 'MergedContract':
        """Type-safe contract merging."""
        return MergedContract(self, other)
```

## 🔗 Relationship Types

### 1. Field Relationships

```python
class FieldSpec(Generic[T], BaseModel):
    """Specification for a field with type safety."""

    # Core type information
    type: Type[T]
    source: str  # Path in state (e.g., "state.messages")
    destination: Optional[str] = None  # Where to write

    # Constraints
    required: bool = True
    default: Optional[T] = None
    default_factory: Optional[Callable[[], T]] = None

    # Transformations
    transform: Optional[Callable[[Any], T]] = None
    validator: Optional[Callable[[T], bool]] = None

    # Optimization hints
    access_pattern: AccessPattern = AccessPattern.READ
    cache_strategy: CacheStrategy = CacheStrategy.NONE

class FieldMapping(Generic[StateT, T], BaseModel):
    """Type-safe field mapping."""

    spec: FieldSpec[T]
    extractor: Callable[[StateT], T]
    updater: Callable[[StateT, T], StateT]

    def extract(self, state: StateT) -> T:
        """Extract with type safety."""
        value = self.extractor(state)
        if self.spec.validator and not self.spec.validator(value):
            raise ContractViolation(f"Field {self.spec.source} validation failed")
        return value

    def update(self, state: StateT, value: T) -> StateT:
        """Update with type safety."""
        if self.spec.transform:
            value = self.spec.transform(value)
        return self.updater(state, value)
```

### 2. State Relationships

```python
class StateRelationship(Generic[StateT], BaseModel):
    """Defines how contracts relate to state."""

    state_type: Type[StateT]
    required_fields: Set[str]
    optional_fields: Set[str]
    computed_fields: Dict[str, Callable[[StateT], Any]]

    def validate(self, state: StateT) -> ValidationResult:
        """Validate state against contract requirements."""
        errors = []

        # Check required fields
        for field in self.required_fields:
            if not hasattr(state, field):
                errors.append(f"Missing required field: {field}")

        # Validate computed fields
        for field, compute in self.computed_fields.items():
            try:
                compute(state)
            except Exception as e:
                errors.append(f"Computed field {field} failed: {e}")

        return ValidationResult(valid=len(errors) == 0, errors=errors)

class SharedStateContract(Generic[StateT], BaseModel):
    """Contract for shared state between components."""

    shared_fields: Set[str]
    private_fields: Dict[str, str]  # component_name -> field

    def project(self, state: StateT, component: str) -> Dict[str, Any]:
        """Project state for specific component."""
        projection = {}

        # Include shared fields
        for field in self.shared_fields:
            if hasattr(state, field):
                projection[field] = getattr(state, field)

        # Include component's private fields
        if component in self.private_fields:
            field = self.private_fields[component]
            if hasattr(state, field):
                projection[field] = getattr(state, field)

        return projection
```

### 3. Engine Relationships

```python
class EngineRelationship(Generic[InputT, OutputT], BaseModel):
    """Defines engine-contract relationship."""

    engine_type: str
    input_contract: Type[InputT]
    output_contract: Type[OutputT]

    # Engine capabilities
    supports_streaming: bool = False
    supports_async: bool = False
    supports_batch: bool = False

    # Resource requirements
    resources: ResourceSpec = Field(default_factory=ResourceSpec)

    def create_contract(self, engine: Any) -> Contract[Any, InputT, OutputT]:
        """Create contract for engine."""
        return EngineContract(
            engine=engine,
            input_type=self.input_contract,
            output_type=self.output_contract,
            resources=self.resources
        )

class EngineContract(Contract[StateT, InputT, OutputT]):
    """Contract wrapping an engine."""

    def __init__(
        self,
        engine: Any,
        input_type: Type[InputT],
        output_type: Type[OutputT],
        resources: ResourceSpec
    ):
        self.engine = engine
        self.input_type = input_type
        self.output_type = output_type
        self.resources = resources
        self._compile_accessors()

    def _compile_accessors(self):
        """Pre-compile field accessors for performance."""
        self.field_getters = {}
        self.field_setters = {}

        for field_name, field_info in self.input_type.model_fields.items():
            # Create optimized getter
            self.field_getters[field_name] = operator.attrgetter(field_name)

        for field_name, field_info in self.output_type.model_fields.items():
            # Create optimized setter
            self.field_setters[field_name] = lambda obj, val, f=field_name: setattr(obj, f, val)
```

## 🔄 Composition Relationships

### 1. Sequential Composition Type Safety

```python
class SequentialContract(Contract[StateT, InputT, OutputT]):
    """Type-safe sequential composition."""

    def __init__(
        self,
        first: Contract[StateT, InputT, MiddleT],
        second: Contract[StateT, MiddleT, OutputT]
    ):
        # Type system ensures first.output_type == second.input_type
        self.first = first
        self.second = second
        self.input_type = first.input_type
        self.output_type = second.output_type

    def execute(self, input: InputT) -> OutputT:
        """Execute sequentially with type flow."""
        middle: MiddleT = self.first.execute(input)
        output: OutputT = self.second.execute(middle)
        return output

# Type-safe composition example
contract1: Contract[State, Query, Documents]
contract2: Contract[State, Documents, Answer]

# This compiles - types match!
pipeline: Contract[State, Query, Answer] = contract1 >> contract2

# This won't compile - type mismatch!
# bad_pipeline = contract2 >> contract1  # Error: Documents != Query
```

### 2. Parallel Composition Type Safety

```python
class ParallelContract(Contract[StateT, InputT, Tuple[OutputT, ...]]):
    """Type-safe parallel composition."""

    def __init__(self, *contracts: Contract[StateT, InputT, Any]):
        # All contracts must accept the same input type
        self.contracts = contracts
        self.input_type = contracts[0].input_type

        # Output is tuple of all outputs
        self.output_types = tuple(c.output_type for c in contracts)

    def execute(self, input: InputT) -> Tuple[Any, ...]:
        """Execute in parallel."""
        results = []
        for contract in self.contracts:
            results.append(contract.execute(input))
        return tuple(results)

# Usage with type safety
retriever: Contract[State, Query, Documents]
reranker: Contract[State, Query, Scores]

parallel: Contract[State, Query, Tuple[Documents, Scores]] = retriever | reranker
```

### 3. Conditional Composition Type Safety

```python
class ConditionalContract(Contract[StateT, InputT, OutputT]):
    """Type-safe conditional execution."""

    def __init__(
        self,
        condition: Contract[StateT, InputT, bool],
        if_true: Contract[StateT, InputT, OutputT],
        if_false: Contract[StateT, InputT, OutputT]
    ):
        # Both branches must produce the same output type
        self.condition = condition
        self.if_true = if_true
        self.if_false = if_false
        self.input_type = condition.input_type
        self.output_type = if_true.output_type

    def execute(self, input: InputT) -> OutputT:
        """Execute conditionally."""
        if self.condition.execute(input):
            return self.if_true.execute(input)
        else:
            return self.if_false.execute(input)
```

## 🎯 Type-Safe Contract Builder

```python
class ContractBuilder(Generic[StateT]):
    """Fluent builder for contracts with type safety."""

    def __init__(self, state_type: Type[StateT]):
        self.state_type = state_type
        self.input_fields: Dict[str, FieldSpec] = {}
        self.output_fields: Dict[str, FieldSpec] = {}
        self.validators: List[Callable] = []

    def with_input(self, name: str, spec: FieldSpec[T]) -> 'ContractBuilder[StateT]':
        """Add input field with type."""
        self.input_fields[name] = spec
        return self

    def with_output(self, name: str, spec: FieldSpec[T]) -> 'ContractBuilder[StateT]':
        """Add output field with type."""
        self.output_fields[name] = spec
        return self

    def with_validator(self, validator: Callable[[StateT], bool]) -> 'ContractBuilder[StateT]':
        """Add state validator."""
        self.validators.append(validator)
        return self

    def build(self) -> Contract[StateT, Any, Any]:
        """Build the contract with full type checking."""
        # Create input/output models dynamically
        input_model = create_model(
            'ContractInput',
            **{name: (spec.type, Field(default=spec.default))
               for name, spec in self.input_fields.items()}
        )

        output_model = create_model(
            'ContractOutput',
            **{name: (spec.type, Field(default=spec.default))
               for name, spec in self.output_fields.items()}
        )

        return BuiltContract(
            state_type=self.state_type,
            input_type=input_model,
            output_type=output_model,
            input_fields=self.input_fields,
            output_fields=self.output_fields,
            validators=self.validators
        )

# Usage with type safety
contract = (
    ContractBuilder(MyState)
    .with_input("query", FieldSpec(type=str, source="state.query"))
    .with_input("k", FieldSpec(type=int, source="state.k", default=5))
    .with_output("results", FieldSpec(type=List[str], destination="state.results"))
    .with_validator(lambda s: len(s.query) > 0)
    .build()
)
```

## 🔥 Advanced Type Relationships

### 1. Contract Inheritance

```python
class BaseAgentContract(Contract[StateT, InputT, OutputT], ABC):
    """Base contract for all agents."""

    @abstractmethod
    def get_tools(self) -> List[ToolContract]:
        """Get tool contracts."""
        ...

class ReactAgentContract(BaseAgentContract[State, Query, Answer]):
    """Contract for ReAct agents."""

    def get_tools(self) -> List[ToolContract]:
        return self.tool_contracts

    def execute(self, input: Query) -> Answer:
        # ReAct-specific execution with tools
        pass
```

### 2. Contract Mixins

```python
class CacheableContract(Contract[StateT, InputT, OutputT]):
    """Mixin for cacheable contracts."""

    cache: Dict[InputT, OutputT] = Field(default_factory=dict)

    def execute(self, input: InputT) -> OutputT:
        if input in self.cache:
            return self.cache[input]

        output = super().execute(input)
        self.cache[input] = output
        return output

class RetryableContract(Contract[StateT, InputT, OutputT]):
    """Mixin for retryable contracts."""

    max_retries: int = 3

    def execute(self, input: InputT) -> OutputT:
        for i in range(self.max_retries):
            try:
                return super().execute(input)
            except Exception as e:
                if i == self.max_retries - 1:
                    raise
                continue
```

### 3. Contract Adapters

```python
class ContractAdapter(Contract[StateT, InputT, OutputT]):
    """Adapt between incompatible contracts."""

    def __init__(
        self,
        source: Contract[StateT, InputT, MiddleT],
        target: Contract[StateT, DifferentInputT, OutputT],
        adapter: Callable[[MiddleT], DifferentInputT]
    ):
        self.source = source
        self.target = target
        self.adapter = adapter

    def execute(self, input: InputT) -> OutputT:
        middle = self.source.execute(input)
        adapted = self.adapter(middle)
        return self.target.execute(adapted)

# Usage - adapt incompatible contracts
contract1: Contract[State, str, Document]
contract2: Contract[State, List[Document], Summary]

adapter = ContractAdapter(
    source=contract1,
    target=contract2,
    adapter=lambda doc: [doc]  # Convert single doc to list
)
```

## 📊 Type Safety Benefits

### Compile-Time Guarantees

```python
# Type checker catches errors before runtime
pipeline: Contract[State, Query, Answer] = (
    retriever >>  # Contract[State, Query, Documents]
    augmenter >>  # Contract[State, Documents, Prompt]
    generator     # Contract[State, Prompt, Answer]
)
# ✅ Types flow correctly!

# This won't compile
bad_pipeline = (
    generator >>  # Contract[State, Prompt, Answer]
    retriever     # Contract[State, Query, Documents]
)
# ❌ Error: Answer is not compatible with Query
```

### IDE Support

```python
# Full autocomplete and type hints
contract: Contract[RAGState, Query, Answer]
result = contract.execute(query)  # IDE knows result is Answer type
result.  # Autocomplete shows Answer fields!
```

### Refactoring Safety

```python
# Change a contract type
class OldContract(Contract[State, str, str]): ...
# to
class NewContract(Contract[State, Query, Answer]): ...

# Type checker finds all places that need updating!
```

---

**This type system ensures complete type safety throughout the contract relationships, catching errors at compile time and enabling powerful IDE support.**
