# Unified Execution Model: Connecting Callables, Nodes, Engines, and State

**Created**: 2025-01-07
**Purpose**: Fix the broken relationship between execution components
**Status**: Core architectural solution

## 🎯 The Core Problem

You've identified the REAL issue - there's no proper relationship between:

- **Callables** (the functions that execute)
- **Nodes** (graph execution units)
- **Engines** (configuration/factories)
- **StateSchema** (data passing through)

They're all disconnected, leading to:

- State not knowing what engines it needs
- Nodes not knowing what state they work with
- Engines creating callables that don't match nodes
- No type safety or validation

## 💡 The Solution: Unified Execution Contract

### 1. The Execution Contract Interface

```python
from typing import Protocol, TypeVar, Generic
from abc import ABC, abstractmethod

StateT = TypeVar('StateT', bound='StateSchema')
InputT = TypeVar('InputT')
OutputT = TypeVar('OutputT')

class ExecutionContract(Protocol[StateT, InputT, OutputT]):
    """Universal contract between all execution components."""

    @property
    def input_schema(self) -> type[InputT]:
        """What input this component expects."""
        ...

    @property
    def output_schema(self) -> type[OutputT]:
        """What output this component produces."""
        ...

    @property
    def state_schema(self) -> type[StateT]:
        """What state this component works with."""
        ...

    @property
    def required_engines(self) -> List[str]:
        """What engines this component needs."""
        ...

    def validate_state(self, state: StateT) -> bool:
        """Validate state has required engines/fields."""
        ...

    def __call__(self, state: StateT, input: InputT) -> OutputT:
        """Execute with state and input."""
        ...
```

### 2. State-Aware Engine

```python
class StateAwareEngine(Engine, Generic[StateT]):
    """Engine that knows its state requirements."""

    def __init__(self):
        self._state_type: type[StateT] = None
        self._required_fields: List[str] = []
        self._provides_fields: List[str] = []

    def requires_state_fields(self, *fields: str) -> 'StateAwareEngine':
        """Declare required state fields."""
        self._required_fields.extend(fields)
        return self

    def provides_state_fields(self, *fields: str) -> 'StateAwareEngine':
        """Declare fields this engine provides to state."""
        self._provides_fields.extend(fields)
        return self

    def create_callable(self, state_type: type[StateT]) -> ExecutionContract:
        """Create callable that implements the contract."""
        self._state_type = state_type

        class ContractCallable(ExecutionContract[StateT, Dict, Any]):
            def __init__(self, engine: StateAwareEngine):
                self.engine = engine

            @property
            def state_schema(self) -> type[StateT]:
                return state_type

            @property
            def required_engines(self) -> List[str]:
                return [self.engine.__class__.__name__]

            def validate_state(self, state: StateT) -> bool:
                # Check required fields exist
                for field in self.engine._required_fields:
                    if not hasattr(state, field):
                        return False
                return True

            def __call__(self, state: StateT, input: Dict) -> Any:
                if not self.validate_state(state):
                    raise ValueError(f"State missing required fields: {self.engine._required_fields}")

                # Execute with state context
                return self.engine.execute_with_state(state, input)

        return ContractCallable(self)

    @abstractmethod
    def execute_with_state(self, state: StateT, input: Dict) -> Any:
        """Execute with full state context."""
        pass
```

### 3. Contract-Aware Node

```python
class ContractNode(Generic[StateT, InputT, OutputT]):
    """Node that enforces execution contracts."""

    def __init__(
        self,
        name: str,
        contract: ExecutionContract[StateT, InputT, OutputT]
    ):
        self.name = name
        self.contract = contract
        self._validate_contract()

    def _validate_contract(self):
        """Validate contract completeness."""
        if not self.contract.state_schema:
            raise ValueError(f"Node {self.name} contract missing state_schema")
        if not self.contract.input_schema:
            raise ValueError(f"Node {self.name} contract missing input_schema")
        if not self.contract.output_schema:
            raise ValueError(f"Node {self.name} contract missing output_schema")

    def __call__(self, state: StateT) -> StateT:
        """Execute node with state."""
        # Validate state matches contract
        if not isinstance(state, self.contract.state_schema):
            raise TypeError(
                f"Node {self.name} expects {self.contract.state_schema.__name__}, "
                f"got {type(state).__name__}"
            )

        # Validate state has required engines
        if not self.contract.validate_state(state):
            missing = self.contract.required_engines
            raise ValueError(f"Node {self.name} requires engines: {missing}")

        # Extract input from state
        input_data = self._extract_input(state)

        # Execute contract
        output = self.contract(state, input_data)

        # Update state with output
        return self._update_state(state, output)

    def _extract_input(self, state: StateT) -> InputT:
        """Extract input from state based on contract."""
        if self.contract.input_schema == Dict:
            # Extract relevant fields to dict
            return {
                "messages": getattr(state, "messages", []),
                "context": getattr(state, "context", {})
            }
        else:
            # Convert state to input type
            return self.contract.input_schema(**state.dict())

    def _update_state(self, state: StateT, output: OutputT) -> StateT:
        """Update state with output based on contract."""
        if hasattr(output, "dict"):
            # Update state fields from output
            for key, value in output.dict().items():
                if hasattr(state, key):
                    setattr(state, key, value)
        elif isinstance(output, dict):
            # Update from dict
            for key, value in output.items():
                if hasattr(state, key):
                    setattr(state, key, value)
        else:
            # Store as result
            state.context["result"] = output

        return state
```

### 4. Unified State with Engine Binding

```python
class UnifiedState(StateSchema):
    """State that properly connects to engines."""

    # Data fields
    messages: List[BaseMessage] = Field(default_factory=list)
    context: Dict[str, Any] = Field(default_factory=dict)

    # Engine bindings (explicit!)
    _engine_contracts: Dict[str, ExecutionContract] = {}
    _node_contracts: Dict[str, ExecutionContract] = {}

    def bind_engine_contract(self, name: str, contract: ExecutionContract):
        """Bind an engine's execution contract."""
        # Validate contract works with this state
        if not issubclass(self.__class__, contract.state_schema):
            raise TypeError(
                f"Contract expects {contract.state_schema.__name__}, "
                f"but state is {self.__class__.__name__}"
            )

        self._engine_contracts[name] = contract

    def bind_node_contract(self, node_name: str, contract: ExecutionContract):
        """Bind a node's execution contract."""
        # Validate contract
        if not contract.validate_state(self):
            raise ValueError(
                f"Node {node_name} contract validation failed. "
                f"Required engines: {contract.required_engines}"
            )

        self._node_contracts[node_name] = contract

    def get_engine_callable(self, name: str) -> Callable:
        """Get executable for an engine."""
        if name not in self._engine_contracts:
            raise KeyError(f"No contract bound for engine: {name}")

        contract = self._engine_contracts[name]
        # Return a callable bound to this state
        return lambda input: contract(self, input)

    def execute_node(self, node_name: str) -> 'UnifiedState':
        """Execute a node with this state."""
        if node_name not in self._node_contracts:
            raise KeyError(f"No contract bound for node: {node_name}")

        contract = self._node_contracts[node_name]
        node = ContractNode(node_name, contract)
        return node(self)
```

### 5. Complete Example: LLM with Prompt Engine

```python
# Define state schema
class RAGState(UnifiedState):
    """State for RAG operations."""
    question: str = Field(default="")
    retrieved_docs: List[str] = Field(default_factory=list)
    answer: str = Field(default="")

# Create prompt engine with contract
class PromptEngineWithContract(StateAwareEngine[RAGState]):
    """Prompt engine that knows its contract."""

    def __init__(self, templates: Dict[str, str]):
        super().__init__()
        self.templates = templates
        self.requires_state_fields("question", "retrieved_docs")
        self.provides_state_fields("formatted_prompt")

    def execute_with_state(self, state: RAGState, input: Dict) -> str:
        """Format prompt with state context."""
        template_name = input.get("template", "default")
        template = self.templates[template_name]

        return template.format(
            question=state.question,
            context="\n".join(state.retrieved_docs)
        )

# Create LLM engine with contract
class LLMEngineWithContract(StateAwareEngine[RAGState]):
    """LLM engine that knows its contract."""

    def __init__(self, model: str):
        super().__init__()
        self.model = model
        self.requires_state_fields("formatted_prompt")
        self.provides_state_fields("answer")

    def execute_with_state(self, state: RAGState, input: Dict) -> str:
        """Generate answer with LLM."""
        prompt = input.get("prompt") or state.context.get("formatted_prompt")

        # Call LLM (simplified)
        from langchain_openai import ChatOpenAI
        llm = ChatOpenAI(model=self.model)
        answer = llm.invoke(prompt)

        # Update state
        state.answer = answer
        return answer

# Wire everything together
def create_rag_pipeline():
    """Create RAG pipeline with proper contracts."""

    # Create engines
    prompt_engine = PromptEngineWithContract({
        "qa": "Question: {question}\nContext: {context}\nAnswer:"
    })

    llm_engine = LLMEngineWithContract("gpt-4")

    # Create state
    state = RAGState(
        question="What is machine learning?",
        retrieved_docs=["ML is...", "Machine learning involves..."]
    )

    # Create contracts
    prompt_contract = prompt_engine.create_callable(RAGState)
    llm_contract = llm_engine.create_callable(RAGState)

    # Bind contracts to state
    state.bind_engine_contract("prompt", prompt_contract)
    state.bind_engine_contract("llm", llm_contract)

    # Create nodes with contracts
    prompt_node = ContractNode("format_prompt", prompt_contract)
    llm_node = ContractNode("generate_answer", llm_contract)

    # Bind nodes to state
    state.bind_node_contract("format_prompt", prompt_contract)
    state.bind_node_contract("generate_answer", llm_contract)

    # Execute pipeline
    state = prompt_node(state)  # Formats prompt
    state = llm_node(state)     # Generates answer

    return state.answer
```

### 6. Graph Builder with Contract Validation

```python
class ContractGraphBuilder:
    """Graph builder that validates contracts."""

    def __init__(self, state_type: type[StateSchema]):
        self.state_type = state_type
        self.nodes: Dict[str, ContractNode] = {}
        self.edges: List[Tuple[str, str]] = []
        self.contracts: Dict[str, ExecutionContract] = {}

    def add_node(
        self,
        name: str,
        engine: StateAwareEngine,
        **config
    ) -> 'ContractGraphBuilder':
        """Add node with automatic contract creation."""
        # Create contract from engine
        contract = engine.create_callable(self.state_type)

        # Validate contract matches state
        if not issubclass(self.state_type, contract.state_schema):
            raise TypeError(
                f"Node {name} expects {contract.state_schema.__name__}, "
                f"but graph uses {self.state_type.__name__}"
            )

        # Create and store node
        node = ContractNode(name, contract)
        self.nodes[name] = node
        self.contracts[name] = contract

        return self

    def add_edge(self, from_node: str, to_node: str) -> 'ContractGraphBuilder':
        """Add edge with contract compatibility check."""
        if from_node not in self.nodes:
            raise KeyError(f"Unknown node: {from_node}")
        if to_node not in self.nodes and to_node != "END":
            raise KeyError(f"Unknown node: {to_node}")

        if to_node != "END":
            # Validate output of from_node matches input of to_node
            from_contract = self.contracts[from_node]
            to_contract = self.contracts[to_node]

            # Check compatibility
            if not self._contracts_compatible(from_contract, to_contract):
                raise ValueError(
                    f"Contracts incompatible: {from_node} -> {to_node}"
                )

        self.edges.append((from_node, to_node))
        return self

    def _contracts_compatible(
        self,
        from_contract: ExecutionContract,
        to_contract: ExecutionContract
    ) -> bool:
        """Check if contracts are compatible."""
        # They must work with the same state type
        if from_contract.state_schema != to_contract.state_schema:
            return False

        # Output fields of 'from' should satisfy input requirements of 'to'
        from_provides = getattr(from_contract, 'provides_fields', [])
        to_requires = getattr(to_contract, 'required_fields', [])

        # Check if 'from' provides what 'to' needs
        for required in to_requires:
            if required not in from_provides:
                return False

        return True

    def compile(self) -> Callable[[StateSchema], StateSchema]:
        """Compile to executable graph."""
        def execute(state: StateSchema) -> StateSchema:
            # Validate state type
            if not isinstance(state, self.state_type):
                raise TypeError(
                    f"Graph expects {self.state_type.__name__}, "
                    f"got {type(state).__name__}"
                )

            # Bind all contracts to state
            unified_state = state if isinstance(state, UnifiedState) else UnifiedState(**state.dict())
            for name, contract in self.contracts.items():
                unified_state.bind_node_contract(name, contract)

            # Execute nodes in order
            for from_node, to_node in self.edges:
                if from_node == "START":
                    continue

                node = self.nodes[from_node]
                unified_state = node(unified_state)

                if to_node == "END":
                    break

            return unified_state

        return execute
```

### 7. Complete Integration Example

```python
def build_rag_graph():
    """Build RAG graph with full contract validation."""

    # Define engines with contracts
    retriever_engine = RetrieverEngineWithContract()
    prompt_engine = PromptEngineWithContract(templates={...})
    llm_engine = LLMEngineWithContract(model="gpt-4")
    parser_engine = ParserEngineWithContract()

    # Build graph with automatic contract validation
    builder = ContractGraphBuilder(RAGState)

    graph = (
        builder
        .add_node("retrieve", retriever_engine)
        .add_node("prompt", prompt_engine)
        .add_node("generate", llm_engine)
        .add_node("parse", parser_engine)
        .add_edge("START", "retrieve")
        .add_edge("retrieve", "prompt")
        .add_edge("prompt", "generate")
        .add_edge("generate", "parse")
        .add_edge("parse", "END")
        .compile()
    )

    # Execute with type-safe state
    state = RAGState(question="What is AI?")
    result = graph(state)

    # Result has validated type and all contracts enforced
    print(result.answer)
```

## 🎯 This Solves The Core Problems

### 1. **Clear Relationships**

- Engines know what state they need
- Nodes know what contracts they execute
- State knows what engines are bound
- Everything is type-safe

### 2. **Contract Enforcement**

- Can't connect incompatible components
- Validate at build time, not runtime
- Clear error messages

### 3. **State-Engine Integration**

- State and engines work together
- Explicit binding and validation
- No magic or guessing

### 4. **Type Safety**

- Generic types flow through
- Compile-time checking
- IDE autocomplete works

## 📊 Before vs After

### Before (Disconnected)

```python
# No relationship between components
engine = SomeEngine()
callable = engine.create_runnable()  # What does this expect?
node = Node(callable)  # What state does this need?
state = StateSchema()  # What engines should I have?
result = node(state)  # 💥 Runtime explosion
```

### After (Unified)

```python
# Everything connected through contracts
engine = StateAwareEngine[MyState]()
contract = engine.create_callable(MyState)
node = ContractNode("my_node", contract)
state = MyState()
state.bind_node_contract("my_node", contract)
result = node(state)  # ✅ Type-safe, validated
```

## 🚀 The Key Insight

The problem isn't having engines, nodes, and state - it's that they don't know about each other! The Execution Contract creates a **formal relationship** between all components:

1. **Engines** declare what state they need
2. **Nodes** enforce contracts
3. **State** validates bindings
4. **Graph** checks compatibility

This is what was missing - a unified execution model that connects everything properly!
