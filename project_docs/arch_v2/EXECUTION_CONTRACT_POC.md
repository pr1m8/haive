# Execution Contract Proof-of-Concept

**Created**: 2025-01-07
**Purpose**: Demonstrate how execution contracts solve the callable/node/engine/state disconnect
**Status**: Implementation blueprint

## 🎯 The Vision

Replace 15,000+ lines of guessing code with ~1,000 lines of explicit contracts.

## 💻 Core Implementation

### 1. The Execution Contract Protocol

```python
# haive/core/contracts/execution_contract.py
from typing import Protocol, TypeVar, Generic, List, Dict, Any, Type
from abc import abstractmethod
from pydantic import BaseModel

StateT = TypeVar('StateT', bound='StateSchema')
InputT = TypeVar('InputT')
OutputT = TypeVar('OutputT')

class ExecutionContract(Protocol[StateT, InputT, OutputT]):
    """Universal contract for all executable components.

    This contract creates the missing link between:
    - Engines and their requirements
    - Nodes and their execution
    - State and its structure
    - Callables and their I/O
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique name for this contract."""
        ...

    @property
    @abstractmethod
    def input_schema(self) -> Type[InputT]:
        """The input type this component expects."""
        ...

    @property
    @abstractmethod
    def output_schema(self) -> Type[OutputT]:
        """The output type this component produces."""
        ...

    @property
    @abstractmethod
    def state_schema(self) -> Type[StateT]:
        """The state type this component works with."""
        ...

    @property
    @abstractmethod
    def required_state_fields(self) -> List[str]:
        """State fields this component needs to read."""
        ...

    @property
    @abstractmethod
    def output_state_fields(self) -> List[str]:
        """State fields this component will update."""
        ...

    @property
    @abstractmethod
    def required_engines(self) -> List[str]:
        """Engine names this component depends on."""
        ...

    @abstractmethod
    def validate_state(self, state: StateT) -> bool:
        """Check if state has everything needed."""
        ...

    @abstractmethod
    def extract_input(self, state: StateT) -> InputT:
        """Extract input from state (no guessing!)."""
        ...

    @abstractmethod
    def format_output(self, output: OutputT, state: StateT) -> Dict[str, Any]:
        """Format output for state update (explicit!)."""
        ...

    @abstractmethod
    def __call__(self, state: StateT, input: InputT) -> OutputT:
        """Execute with validated input."""
        ...
```

### 2. Base Implementation

```python
# haive/core/contracts/base_contract.py
from typing import Type, List, Dict, Any, Generic
from pydantic import BaseModel

class BaseExecutionContract(Generic[StateT, InputT, OutputT]):
    """Base implementation with common patterns."""

    def __init__(
        self,
        name: str,
        input_schema: Type[InputT],
        output_schema: Type[OutputT],
        state_schema: Type[StateT],
        required_fields: List[str] = None,
        output_fields: List[str] = None,
        required_engines: List[str] = None
    ):
        self._name = name
        self._input_schema = input_schema
        self._output_schema = output_schema
        self._state_schema = state_schema
        self._required_fields = required_fields or []
        self._output_fields = output_fields or []
        self._required_engines = required_engines or []

    @property
    def name(self) -> str:
        return self._name

    @property
    def input_schema(self) -> Type[InputT]:
        return self._input_schema

    @property
    def output_schema(self) -> Type[OutputT]:
        return self._output_schema

    @property
    def state_schema(self) -> Type[StateT]:
        return self._state_schema

    @property
    def required_state_fields(self) -> List[str]:
        return self._required_fields

    @property
    def output_state_fields(self) -> List[str]:
        return self._output_fields

    @property
    def required_engines(self) -> List[str]:
        return self._required_engines

    def validate_state(self, state: StateT) -> bool:
        """Default validation - check required fields exist."""
        for field in self._required_fields:
            if not hasattr(state, field):
                return False
        return True

    def extract_input(self, state: StateT) -> InputT:
        """Default extraction - map state fields to input schema."""
        if self._input_schema == Dict:
            # Extract as dictionary
            return {
                field: getattr(state, field)
                for field in self._required_fields
                if hasattr(state, field)
            }
        else:
            # Try to construct input type from state
            kwargs = {}
            for field_name in self._input_schema.model_fields:
                if hasattr(state, field_name):
                    kwargs[field_name] = getattr(state, field_name)
            return self._input_schema(**kwargs)

    def format_output(self, output: OutputT, state: StateT) -> Dict[str, Any]:
        """Default formatting - map output to state fields."""
        if isinstance(output, BaseModel):
            # Pydantic model - extract fields
            result = {}
            for field in self._output_fields:
                if hasattr(output, field):
                    result[field] = getattr(output, field)
            return result
        elif isinstance(output, dict):
            # Dictionary - filter to output fields
            return {
                k: v for k, v in output.items()
                if k in self._output_fields
            }
        else:
            # Single value - map to first output field
            if self._output_fields:
                return {self._output_fields[0]: output}
            return {"result": output}
```

### 3. Engine Contract Implementation

```python
# haive/core/contracts/engine_contract.py
from typing import Dict, Any
from langchain_core.messages import BaseMessage, AIMessage

class LLMEngineContract(BaseExecutionContract):
    """Contract for LLM engines."""

    def __init__(self, engine):
        self.engine = engine
        super().__init__(
            name=f"{engine.name}_contract",
            input_schema=Dict[str, Any],  # Flexible input
            output_schema=BaseMessage,     # Always returns message
            state_schema=StateSchema,
            required_fields=["messages"],
            output_fields=["messages"],
            required_engines=[]
        )

    def extract_input(self, state: StateSchema) -> Dict[str, Any]:
        """Extract messages and context for LLM."""
        return {
            "messages": state.messages,
            "context": getattr(state, "context", {})
        }

    def format_output(self, output: BaseMessage, state: StateSchema) -> Dict[str, Any]:
        """Append message to messages list."""
        messages = list(state.messages)
        messages.append(output)
        return {"messages": messages}

    def __call__(self, state: StateSchema, input: Dict[str, Any]) -> BaseMessage:
        """Execute LLM engine."""
        result = self.engine.invoke(input)
        if isinstance(result, str):
            return AIMessage(content=result)
        return result


class RetrieverEngineContract(BaseExecutionContract):
    """Contract for retriever engines."""

    def __init__(self, engine):
        self.engine = engine
        super().__init__(
            name=f"{engine.name}_contract",
            input_schema=str,  # Query string
            output_schema=List[str],  # Documents
            state_schema=StateSchema,
            required_fields=["query"],
            output_fields=["documents"],
            required_engines=[]
        )

    def extract_input(self, state: StateSchema) -> str:
        """Extract query from state."""
        return state.query or ""

    def format_output(self, output: List[str], state: StateSchema) -> Dict[str, Any]:
        """Store documents in state."""
        return {"documents": output}

    def __call__(self, state: StateSchema, input: str) -> List[str]:
        """Execute retriever."""
        return self.engine.invoke(input)
```

### 4. The Simple Contract Node

```python
# haive/core/graph/node/contract_node.py
from typing import Optional
from langgraph.types import Command
from haive.core.contracts.execution_contract import ExecutionContract

class ContractNode:
    """A node that uses execution contracts - simple and explicit!

    This replaces 900+ lines of EngineNode with ~50 lines.
    """

    def __init__(
        self,
        name: str,
        contract: ExecutionContract,
        goto: Optional[str] = None
    ):
        self.name = name
        self.contract = contract
        self.goto = goto

    def __call__(self, state: StateSchema, config: Optional[Dict] = None) -> Command:
        """Execute using the contract - no guessing!"""

        # Step 1: Validate state
        if not self.contract.validate_state(state):
            raise ValueError(
                f"State missing requirements for {self.contract.name}: "
                f"{self.contract.required_state_fields}"
            )

        # Step 2: Extract input (contract knows how!)
        input_data = self.contract.extract_input(state)

        # Step 3: Execute (type-safe!)
        output = self.contract(state, input_data)

        # Step 4: Format output (contract knows how!)
        update = self.contract.format_output(output, state)

        # Step 5: Return command
        return Command(update=update, goto=self.goto)

    def __repr__(self) -> str:
        return f"ContractNode(name='{self.name}', contract='{self.contract.name}')"
```

### 5. Callable Contracts

```python
# haive/core/contracts/callable_contract.py
from typing import Callable, Dict, Any
import inspect

class CallableContract(BaseExecutionContract):
    """Wrap any callable with a contract."""

    def __init__(
        self,
        func: Callable,
        state_fields: Dict[str, str] = None,  # param -> state field
        output_field: str = "result"
    ):
        self.func = func
        self.param_mapping = state_fields or {}

        # Infer requirements from signature
        sig = inspect.signature(func)
        required_fields = []
        for param in sig.parameters:
            field = self.param_mapping.get(param, param)
            required_fields.append(field)

        super().__init__(
            name=f"{func.__name__}_contract",
            input_schema=Dict[str, Any],
            output_schema=Any,
            state_schema=StateSchema,
            required_fields=required_fields,
            output_fields=[output_field]
        )

    def extract_input(self, state: StateSchema) -> Dict[str, Any]:
        """Extract parameters from state using mapping."""
        sig = inspect.signature(self.func)
        kwargs = {}

        for param in sig.parameters:
            state_field = self.param_mapping.get(param, param)
            if hasattr(state, state_field):
                kwargs[param] = getattr(state, state_field)

        return kwargs

    def __call__(self, state: StateSchema, input: Dict[str, Any]) -> Any:
        """Execute the callable."""
        return self.func(**input)

# Usage example:
def calculate_score(messages: List, threshold: int = 100) -> int:
    return len(messages) * threshold

# Wrap with contract
calc_contract = CallableContract(
    calculate_score,
    state_fields={"messages": "messages", "threshold": "score_threshold"},
    output_field="score"
)

# Use in node
calc_node = ContractNode("calculate", calc_contract)
```

## 🔄 Graph Builder with Contracts

```python
# haive/core/graph/builder/contract_graph_builder.py
from typing import Dict, List, Type
from haive.core.contracts.execution_contract import ExecutionContract

class ContractGraphBuilder:
    """Build graphs with contract validation."""

    def __init__(self, state_schema: Type[StateSchema]):
        self.state_schema = state_schema
        self.contracts: Dict[str, ExecutionContract] = {}
        self.nodes: Dict[str, ContractNode] = {}
        self.edges: List[Tuple[str, str]] = []

    def add_contract_node(
        self,
        name: str,
        contract: ExecutionContract,
        goto: Optional[str] = None
    ) -> 'ContractGraphBuilder':
        """Add node with contract validation."""

        # Validate contract matches state schema
        if not issubclass(self.state_schema, contract.state_schema):
            raise TypeError(
                f"Contract expects {contract.state_schema.__name__}, "
                f"but graph uses {self.state_schema.__name__}"
            )

        # Check required fields exist in state schema
        for field in contract.required_state_fields:
            if field not in self.state_schema.model_fields:
                raise ValueError(
                    f"Contract requires field '{field}' not in state schema"
                )

        # Create and store node
        node = ContractNode(name, contract, goto)
        self.nodes[name] = node
        self.contracts[name] = contract

        return self

    def add_edge(self, from_node: str, to_node: str) -> 'ContractGraphBuilder':
        """Add edge with contract compatibility check."""

        if from_node in self.contracts and to_node in self.contracts:
            from_contract = self.contracts[from_node]
            to_contract = self.contracts[to_node]

            # Check output of 'from' satisfies input of 'to'
            from_outputs = set(from_contract.output_state_fields)
            to_inputs = set(to_contract.required_state_fields)

            missing = to_inputs - from_outputs
            if missing and to_node != "END":
                logger.warning(
                    f"Edge {from_node} -> {to_node}: "
                    f"Target needs fields not provided: {missing}"
                )

        self.edges.append((from_node, to_node))
        return self

    def compile(self) -> Callable:
        """Compile to executable graph."""
        # Implementation details...
        pass
```

## 🎯 Real-World Example: RAG Pipeline

```python
# Using contracts for a complete RAG pipeline

# 1. Define contracts for each component
retriever_contract = RetrieverEngineContract(retriever_engine)
prompt_contract = CallableContract(
    format_prompt,
    state_fields={"documents": "documents", "query": "query"},
    output_field="prompt"
)
llm_contract = LLMEngineContract(llm_engine)
parser_contract = CallableContract(
    parse_response,
    state_fields={"messages": "messages"},
    output_field="answer"
)

# 2. Build graph with contracts
builder = ContractGraphBuilder(RAGState)
graph = (
    builder
    .add_contract_node("retrieve", retriever_contract)
    .add_contract_node("format", prompt_contract)
    .add_contract_node("generate", llm_contract)
    .add_contract_node("parse", parser_contract)
    .add_edge("START", "retrieve")
    .add_edge("retrieve", "format")
    .add_edge("format", "generate")
    .add_edge("generate", "parse")
    .add_edge("parse", "END")
    .compile()
)

# 3. Execute with confidence
state = RAGState(query="What is machine learning?")
result = graph(state)
print(result.answer)  # Type-safe, validated, explicit!
```

## 📊 The Transformation

### Before (Current System)

```python
# EngineNode: 900 lines of guessing
# AgentNodeV3: 850 lines of projection
# CallableNode: 274 lines of extraction
# Multiple versions still trying...
# Total: ~15,000 lines across 45 files
```

### After (With Contracts)

```python
# ContractNode: 50 lines
# BaseExecutionContract: 100 lines
# Engine contracts: 200 lines (all types)
# Callable contracts: 100 lines
# Graph builder: 150 lines
# Total: ~600 lines, 10 files
```

## 🚀 Migration Path

### Phase 1: Add Contracts to Engines

```python
# Wrap existing engines
class EngineWithContract(Engine):
    def get_contract(self) -> ExecutionContract:
        return EngineContract(self)
```

### Phase 2: Create Contract Nodes

```python
# Use alongside existing nodes
if hasattr(engine, 'get_contract'):
    node = ContractNode(name, engine.get_contract())
else:
    node = EngineNode(name, engine)  # Fallback
```

### Phase 3: Gradual Migration

```python
# Replace node by node
# Old: EngineNode with 900 lines
# New: ContractNode with 50 lines
```

## 🎯 The Key Benefits

1. **Explicit**: No guessing what components need
2. **Type-safe**: Contracts enforce types
3. **Validated**: Check at build time, not runtime
4. **Simple**: 50 lines vs 900 lines
5. **Composable**: Contracts can be combined
6. **Testable**: Test contracts in isolation
7. **Maintainable**: Change contract, not 45 files

## 💡 The Bottom Line

Execution contracts turn 15,000 lines of guessing into 600 lines of explicit, type-safe, validated code. This is the missing link that connects engines, nodes, callables, and state properly!

---

**This proof-of-concept shows that with execution contracts, we can reduce the node module from 45 files and ~15,000 lines to 10 files and ~600 lines while gaining type safety, validation, and clarity.**
