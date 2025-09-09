# State Injection and Node Contracts

**Created**: 2025-01-30  
**Purpose**: Design state injection patterns and node type contracts  
**Focus**: Enable clean node-to-node state flow

## 🎯 Core Concept: State Injection Framework

Instead of nodes grabbing state randomly, we need **explicit state injection** with typed contracts.

## 📊 Current Problem: Uncontrolled State Access

```python
# CURRENT MESS - Nodes grab whatever they want
class SomeNode:
    def execute(self, state: dict):
        # Random state access
        messages = state.get("messages", [])
        context = state.get("context", {})
        # Who knows what fields exist?
        # Who owns these fields?
        # What if multiple nodes write to same field?
```

## ✅ Solution: State Injection with Node Types

### 1. Node Type Contracts

```python
from typing import Protocol, TypeVar
from pydantic import BaseModel

TInput = TypeVar("TInput", bound=BaseModel)
TOutput = TypeVar("TOutput", bound=BaseModel)
TState = TypeVar("TState", bound=BaseModel)

@protocol
class InjectableNode(Protocol[TInput, TOutput, TState]):
    """Node that receives injected state"""

    @property
    def input_contract(self) -> type[TInput]:
        """What this node needs as input"""
        ...

    @property
    def output_contract(self) -> type[TOutput]:
        """What this node produces"""
        ...

    @property
    def state_requirements(self) -> type[TState]:
        """What state fields this node needs"""
        ...

    def execute(self, input: TInput, state: TState) -> TOutput:
        """Execute with injected dependencies"""
        ...
```

### 2. Node Type Definitions

```python
# Define specific node types with clear contracts

class TransformNode(InjectableNode[TInput, TOutput, TState]):
    """Pure transformation - input to output"""
    pass

class AccumulatorNode(InjectableNode[TInput, TOutput, TState]):
    """Accumulates state over time"""
    def accumulate(self, current: TState, new: TOutput) -> TState:
        ...

class RouterNode(InjectableNode[TInput, str, TState]):
    """Routes to other nodes"""
    def get_route(self, input: TInput, state: TState) -> str:
        ...

class GeneratorNode(InjectableNode[None, TOutput, TState]):
    """Generates new data from state"""
    pass

class ValidatorNode(InjectableNode[TInput, TInput, TState]):
    """Validates and passes through"""
    def validate(self, input: TInput) -> bool:
        ...

class SinkNode(InjectableNode[TInput, None, TState]):
    """Consumes input, no output"""
    pass
```

### 3. State Injection Mechanism

```python
class StateInjector:
    """Manages state injection for nodes"""

    def __init__(self, global_state: BaseModel):
        self.global_state = global_state
        self.node_states: dict[str, BaseModel] = {}

    def inject_for_node(
        self,
        node: InjectableNode,
        input_data: BaseModel
    ) -> tuple[BaseModel, BaseModel]:
        """Inject required state for a node"""

        # Extract only what node needs from global state
        node_state = self._extract_requirements(
            self.global_state,
            node.state_requirements
        )

        # Validate input matches contract
        if not isinstance(input_data, node.input_contract):
            input_data = node.input_contract(**input_data.dict())

        return input_data, node_state

    def collect_output(
        self,
        node: InjectableNode,
        output: BaseModel
    ) -> None:
        """Collect node output back to state"""

        # Validate output matches contract
        assert isinstance(output, node.output_contract)

        # Merge back to global state with conflict resolution
        self._merge_output(output, node.output_contract)
```

### 4. Node Communication Patterns

```python
# Node-to-Node Communication via Contracts

class DocumentLoaderNode(TransformNode[PathInput, DocumentOutput, EmptyState]):
    """Loads documents from paths"""
    input_contract = PathInput
    output_contract = DocumentOutput
    state_requirements = EmptyState  # No state needed

class ChunkerNode(TransformNode[DocumentOutput, ChunksOutput, ConfigState]):
    """Chunks documents"""
    input_contract = DocumentOutput  # Takes DocumentLoaderNode output!
    output_contract = ChunksOutput
    state_requirements = ConfigState  # Needs config from state

class EmbedderNode(TransformNode[ChunksOutput, EmbeddingsOutput, EmptyState]):
    """Creates embeddings"""
    input_contract = ChunksOutput  # Takes ChunkerNode output!
    output_contract = EmbeddingsOutput
    state_requirements = EmptyState

# Clean pipeline with type safety!
pipeline = [DocumentLoaderNode, ChunkerNode, EmbedderNode]
```

### 5. Advanced Node Types

```python
class StatefulNode(InjectableNode[TInput, TOutput, TState]):
    """Node with internal state management"""

    internal_state: BaseModel

    def pre_execute(self, state: TState) -> None:
        """Setup before execution"""
        self.internal_state = self.load_state(state)

    def post_execute(self, output: TOutput, state: TState) -> TState:
        """Update state after execution"""
        return self.merge_state(state, self.internal_state)

class ConditionalNode(RouterNode[TInput, str, TState]):
    """Routes based on conditions"""

    conditions: dict[str, Callable[[TInput, TState], bool]]

    def get_route(self, input: TInput, state: TState) -> str:
        for route, condition in self.conditions.items():
            if condition(input, state):
                return route
        return "default"

class ParallelNode(InjectableNode[TInput, list[TOutput], TState]):
    """Executes multiple nodes in parallel"""

    sub_nodes: list[InjectableNode]

    async def execute_parallel(
        self,
        input: TInput,
        state: TState
    ) -> list[TOutput]:
        tasks = [node.execute(input, state) for node in self.sub_nodes]
        return await asyncio.gather(*tasks)
```

### 6. Document System with State Injection

```python
# Specific example for Document pipeline

class DocumentState(BaseModel):
    """Shared state for document processing"""
    config: DocumentConfig
    metadata: dict[str, Any]
    errors: list[str]

class DocumentPipelineNode(InjectableNode):
    """Base for all document nodes"""
    state_requirements = DocumentState

class LoaderNode(DocumentPipelineNode):
    input_contract = PathListInput
    output_contract = DocumentsOutput

    def execute(self, input: PathListInput, state: DocumentState):
        docs = []
        for path in input.paths:
            try:
                doc = self.load(path, state.config)
                docs.append(doc)
            except Exception as e:
                state.errors.append(f"Failed to load {path}: {e}")
        return DocumentsOutput(documents=docs)

class SplitterNode(DocumentPipelineNode):
    input_contract = DocumentsOutput
    output_contract = ChunksOutput

    def execute(self, input: DocumentsOutput, state: DocumentState):
        chunks = []
        for doc in input.documents:
            doc_chunks = self.split(
                doc,
                chunk_size=state.config.chunk_size,
                overlap=state.config.overlap
            )
            chunks.extend(doc_chunks)
        return ChunksOutput(chunks=chunks)
```

## 🔄 State Flow Patterns

### 1. Sequential Flow

```
Node A → Node B → Node C
(Each output becomes next input)
```

### 2. Branching Flow

```
Node A → Router → [Node B | Node C]
(Router decides path based on state)
```

### 3. Parallel Flow

```
Node A → [Node B, Node C, Node D] → Merger
(Parallel execution with merge)
```

### 4. Accumulator Flow

```
Node A → Accumulator → Node A (loop)
(State accumulates over iterations)
```

## 🎯 Benefits of State Injection

1. **Type Safety**: Know exactly what each node needs and produces
2. **Testability**: Test nodes in isolation with injected state
3. **Composability**: Nodes can be composed based on contracts
4. **No Surprises**: No hidden state access or mutations
5. **Clear Dependencies**: Explicit about what state is needed
6. **Parallel Safe**: No race conditions on state access

## 📋 Implementation Priority

1. **Define base node type protocols**
2. **Create state injector mechanism**
3. **Convert existing nodes to contracts**
4. **Implement Document system with injection**
5. **Add validation and type checking**
6. **Create node composition helpers**

## 💡 Key Principle

**"Nodes don't take state, state is given to nodes"**

This inversion of control makes the system predictable, testable, and maintainable.
