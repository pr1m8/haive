# Protocol Contracts Implementation Plan

**Domain**: Contracts & Interfaces  
**Estimated Days**: 3-4 days  
**Target LOC**: 1,500 LOC (new)  
**Dependencies**: None (foundation layer)

## 🎯 Overview

Create clean protocol contracts that define interfaces between all major components. This establishes the foundation for the entire architecture transformation by defining clear boundaries and preventing circular dependencies.

## 📊 Current State Analysis

### Current Problems

- **No formal interfaces**: Components directly depend on implementations
- **Circular dependencies**: 15+ import cycles throughout codebase
- **Tight coupling**: Engine, nodes, and agents all directly reference each other
- **Mixed abstractions**: Protocol, implementation, and configuration mixed together

### Dependency Chaos Examples

```python
# Current circular imports
haive.core.engine → haive.core.graph.node → haive.core.engine  # Cycle!
haive.agents.base → haive.core.schema → haive.agents.base      # Cycle!
haive.core.engine → haive.core.common.mixins → haive.core.engine # Cycle!
```

## 🏗️ Target Architecture

### Protocol Hierarchy

```
packages/haive-core/src/haive/core/contracts/
├── __init__.py                    # Export all contracts (50 LOC)
├── engine/
│   ├── __init__.py               # Engine protocol exports (20 LOC)
│   ├── engine_protocol.py        # Core engine interface (120 LOC)
│   ├── tool_protocol.py          # Tool management interface (80 LOC)
│   └── llm_protocol.py           # LLM provider interface (100 LOC)
├── node/
│   ├── __init__.py               # Node protocol exports (20 LOC)
│   ├── node_protocol.py          # Base node interface (100 LOC)
│   ├── execution_protocol.py     # Execution semantics (80 LOC)
│   └── validation_protocol.py    # Validation interface (70 LOC)
├── agent/
│   ├── __init__.py               # Agent protocol exports (20 LOC)
│   ├── agent_protocol.py         # Core agent interface (150 LOC)
│   ├── workflow_protocol.py      # Workflow interface (120 LOC)
│   └── multi_agent_protocol.py   # Multi-agent coordination (100 LOC)
├── schema/
│   ├── __init__.py               # Schema protocol exports (20 LOC)
│   ├── state_protocol.py         # State management interface (80 LOC)
│   ├── message_protocol.py       # Message handling interface (60 LOC)
│   └── config_protocol.py        # Configuration interface (90 LOC)
└── graph/
    ├── __init__.py               # Graph protocol exports (20 LOC)
    ├── graph_protocol.py         # Graph construction interface (100 LOC)
    ├── builder_protocol.py       # Builder pattern interface (80 LOC)
    └── analyzer_protocol.py      # Analysis interface (60 LOC)
```

**Total**: 12 protocol files, ~1,500 LOC

## 📋 Detailed Implementation Steps

### Step 1: Engine Protocols (Day 1)

#### 1.1 Core Engine Protocol

**File**: `contracts/engine/engine_protocol.py`

```python
from typing import Protocol, TypeVar, Generic, Any, Dict, List
from typing_extensions import TypedDict

class EngineConfigDict(TypedDict, total=False):
    """Configuration dictionary for engines."""
    model: str
    temperature: float
    max_tokens: int
    tools: List[str]

class ToolExecutionResult(TypedDict):
    """Result of tool execution."""
    tool_name: str
    input: Dict[str, Any]
    output: Any
    execution_time_ms: int
    success: bool
    error: str | None

ConfigT = TypeVar('ConfigT', bound=EngineConfigDict)
StateT = TypeVar('StateT')
ResultT = TypeVar('ResultT')

class EngineProtocol(Protocol, Generic[ConfigT, StateT, ResultT]):
    """Core engine interface for all LLM engines."""

    @property
    def config(self) -> ConfigT:
        """Get current engine configuration."""
        ...

    def configure(self, **kwargs) -> None:
        """Update engine configuration."""
        ...

    def add_tool(self, tool: Any, name: str | None = None) -> None:
        """Add a tool to the engine."""
        ...

    def remove_tool(self, name: str) -> None:
        """Remove a tool from the engine."""
        ...

    async def arun(self, state: StateT) -> ResultT:
        """Execute engine with given state."""
        ...

    def run(self, state: StateT) -> ResultT:
        """Execute engine synchronously."""
        ...
```

#### 1.2 Tool Protocol

**File**: `contracts/engine/tool_protocol.py`

```python
from typing import Protocol, Any, Dict, List
from typing_extensions import TypedDict

class ToolMetadata(TypedDict, total=False):
    """Tool metadata for routing and execution."""
    route: str
    description: str
    schema: Dict[str, Any]
    is_async: bool

class ToolProtocol(Protocol):
    """Interface for executable tools."""

    @property
    def name(self) -> str:
        """Tool identifier."""
        ...

    @property
    def metadata(self) -> ToolMetadata:
        """Tool execution metadata."""
        ...

    def execute(self, input_data: Any) -> Any:
        """Execute tool with input data."""
        ...

    async def aexecute(self, input_data: Any) -> Any:
        """Execute tool asynchronously."""
        ...

class ToolManagerProtocol(Protocol):
    """Interface for managing tools."""

    def register_tool(self, tool: ToolProtocol) -> None:
        """Register a tool for use."""
        ...

    def get_tool(self, name: str) -> ToolProtocol:
        """Get tool by name."""
        ...

    def list_tools(self) -> List[str]:
        """List all registered tool names."""
        ...

    def execute_tool(self, name: str, input_data: Any) -> Any:
        """Execute tool by name."""
        ...
```

### Step 2: Node Protocols (Day 1.5)

#### 2.1 Base Node Protocol

**File**: `contracts/node/node_protocol.py`

```python
from typing import Protocol, TypeVar, Generic, Any, Dict
from typing_extensions import TypedDict

class NodeMetadata(TypedDict, total=False):
    """Node execution metadata."""
    node_type: str
    execution_time_ms: int
    memory_usage_mb: float
    error: str | None

InputT = TypeVar('InputT')
OutputT = TypeVar('OutputT')
StateT = TypeVar('StateT')

class NodeProtocol(Protocol, Generic[InputT, OutputT, StateT]):
    """Base interface for all graph nodes."""

    @property
    def name(self) -> str:
        """Node identifier."""
        ...

    @property
    def node_type(self) -> str:
        """Type of node for routing."""
        ...

    def validate_input(self, input_data: InputT) -> bool:
        """Validate input before execution."""
        ...

    async def aexecute(self, input_data: InputT, state: StateT) -> OutputT:
        """Execute node asynchronously."""
        ...

    def execute(self, input_data: InputT, state: StateT) -> OutputT:
        """Execute node synchronously."""
        ...

    def get_metadata(self) -> NodeMetadata:
        """Get execution metadata."""
        ...
```

#### 2.2 Execution Protocol

**File**: `contracts/node/execution_protocol.py`

```python
from typing import Protocol, Any, Dict
from enum import Enum

class ExecutionStatus(str, Enum):
    """Node execution status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class ExecutionContext(TypedDict):
    """Context for node execution."""
    node_name: str
    execution_id: str
    start_time: float
    timeout_seconds: int
    retry_count: int

class ExecutableNodeProtocol(Protocol):
    """Interface for nodes that can be executed."""

    def prepare_execution(self, context: ExecutionContext) -> None:
        """Prepare for execution."""
        ...

    async def execute_with_context(self, input_data: Any, context: ExecutionContext) -> Any:
        """Execute with full context tracking."""
        ...

    def cleanup_execution(self, context: ExecutionContext) -> None:
        """Cleanup after execution."""
        ...

    def get_execution_status(self) -> ExecutionStatus:
        """Get current execution status."""
        ...
```

### Step 3: Agent Protocols (Day 2)

#### 3.1 Core Agent Protocol

**File**: `contracts/agent/agent_protocol.py`

```python
from typing import Protocol, TypeVar, Generic, Any, Dict, List
from typing_extensions import TypedDict

class AgentMetadata(TypedDict):
    """Agent metadata and capabilities."""
    name: str
    agent_type: str
    capabilities: List[str]
    version: str

InputT = TypeVar('InputT')
OutputT = TypeVar('OutputT')
ConfigT = TypeVar('ConfigT')
StateT = TypeVar('StateT')

class AgentProtocol(Protocol, Generic[InputT, OutputT, ConfigT, StateT]):
    """Core agent interface."""

    @property
    def name(self) -> str:
        """Agent identifier."""
        ...

    @property
    def metadata(self) -> AgentMetadata:
        """Agent metadata."""
        ...

    @property
    def config(self) -> ConfigT:
        """Agent configuration."""
        ...

    def configure(self, **kwargs) -> None:
        """Update agent configuration."""
        ...

    async def arun(self, input_data: InputT, state: StateT | None = None) -> OutputT:
        """Execute agent asynchronously."""
        ...

    def run(self, input_data: InputT, state: StateT | None = None) -> OutputT:
        """Execute agent synchronously."""
        ...

    def as_tool(self, name: str | None = None, description: str | None = None) -> Any:
        """Convert agent to a tool."""
        ...
```

#### 3.2 Workflow Protocol

**File**: `contracts/agent/workflow_protocol.py`

```python
from typing import Protocol, TypeVar, Generic, Any, Dict, List
from enum import Enum

class WorkflowMode(str, Enum):
    """Workflow execution modes."""
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    CONDITIONAL = "conditional"
    LOOP = "loop"

WorkflowInputT = TypeVar('WorkflowInputT')
WorkflowOutputT = TypeVar('WorkflowOutputT')

class WorkflowProtocol(Protocol, Generic[WorkflowInputT, WorkflowOutputT]):
    """Pure orchestration workflow interface."""

    @property
    def mode(self) -> WorkflowMode:
        """Workflow execution mode."""
        ...

    def add_step(self, step: Any, name: str) -> None:
        """Add step to workflow."""
        ...

    def remove_step(self, name: str) -> None:
        """Remove step from workflow."""
        ...

    async def aexecute(self, input_data: WorkflowInputT) -> WorkflowOutputT:
        """Execute workflow asynchronously."""
        ...

    def execute(self, input_data: WorkflowInputT) -> WorkflowOutputT:
        """Execute workflow synchronously."""
        ...
```

### Step 4: Schema Protocols (Day 2.5)

#### 4.1 State Protocol

**File**: `contracts/schema/state_protocol.py`

```python
from typing import Protocol, TypeVar, Any, Dict
from typing_extensions import TypedDict

class StateSnapshot(TypedDict):
    """Immutable state snapshot."""
    timestamp: float
    state_hash: str
    data: Dict[str, Any]

StateT = TypeVar('StateT')

class StateProtocol(Protocol, Generic[StateT]):
    """Interface for state management."""

    def get_state(self) -> StateT:
        """Get current state."""
        ...

    def update_state(self, updates: Dict[str, Any]) -> None:
        """Update state with new values."""
        ...

    def reset_state(self) -> None:
        """Reset to initial state."""
        ...

    def create_snapshot(self) -> StateSnapshot:
        """Create immutable snapshot."""
        ...

    def restore_snapshot(self, snapshot: StateSnapshot) -> None:
        """Restore from snapshot."""
        ...
```

#### 4.2 Message Protocol

**File**: `contracts/schema/message_protocol.py`

```python
from typing import Protocol, Any, Dict, List
from enum import Enum

class MessageRole(str, Enum):
    """Message roles in conversation."""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"

class MessageProtocol(Protocol):
    """Interface for conversation messages."""

    @property
    def role(self) -> MessageRole:
        """Message role."""
        ...

    @property
    def content(self) -> str:
        """Message content."""
        ...

    @property
    def metadata(self) -> Dict[str, Any]:
        """Additional message metadata."""
        ...

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        ...

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MessageProtocol':
        """Create from dictionary."""
        ...
```

### Step 5: Graph Protocols (Day 3)

#### 5.1 Graph Protocol

**File**: `contracts/graph/graph_protocol.py`

```python
from typing import Protocol, TypeVar, Any, Dict, List, Set

NodeT = TypeVar('NodeT')
EdgeT = TypeVar('EdgeT')

class GraphProtocol(Protocol, Generic[NodeT, EdgeT]):
    """Interface for graph construction and management."""

    def add_node(self, node: NodeT, name: str) -> None:
        """Add node to graph."""
        ...

    def remove_node(self, name: str) -> None:
        """Remove node from graph."""
        ...

    def add_edge(self, from_node: str, to_node: str, condition: Any = None) -> None:
        """Add edge between nodes."""
        ...

    def remove_edge(self, from_node: str, to_node: str) -> None:
        """Remove edge between nodes."""
        ...

    def get_nodes(self) -> Dict[str, NodeT]:
        """Get all nodes."""
        ...

    def get_edges(self) -> List[EdgeT]:
        """Get all edges."""
        ...

    def validate_graph(self) -> bool:
        """Validate graph structure."""
        ...

    async def acompile(self) -> Any:
        """Compile graph for execution."""
        ...
```

#### 5.2 Builder Protocol

**File**: `contracts/graph/builder_protocol.py`

```python
from typing import Protocol, TypeVar, Any, Dict

GraphT = TypeVar('GraphT')
ConfigT = TypeVar('ConfigT')

class GraphBuilderProtocol(Protocol, Generic[GraphT, ConfigT]):
    """Interface for graph builders."""

    def create_graph(self, config: ConfigT) -> GraphT:
        """Create new graph from configuration."""
        ...

    def add_standard_nodes(self, graph: GraphT) -> None:
        """Add standard node patterns."""
        ...

    def connect_sequential(self, graph: GraphT, node_names: List[str]) -> None:
        """Connect nodes in sequence."""
        ...

    def connect_parallel(self, graph: GraphT, node_names: List[str], merge_node: str) -> None:
        """Connect nodes in parallel."""
        ...

    def optimize_graph(self, graph: GraphT) -> GraphT:
        """Optimize graph structure."""
        ...
```

### Step 6: Integration & Testing (Day 4)

#### 6.1 Contract Validation

Create validation utilities to ensure implementations comply with contracts:

**File**: `contracts/validation.py`

```python
from typing import Any, Type, Protocol
import inspect

def validate_protocol_implementation(implementation: Any, protocol: Type[Protocol]) -> List[str]:
    """Validate that implementation satisfies protocol contract."""
    errors = []

    # Check all protocol methods are implemented
    for name, method in inspect.getmembers(protocol, inspect.isfunction):
        if not hasattr(implementation, name):
            errors.append(f"Missing method: {name}")
        else:
            impl_method = getattr(implementation, name)
            if not callable(impl_method):
                errors.append(f"Method {name} is not callable")

    return errors

def check_circular_imports() -> List[str]:
    """Check for circular import dependencies."""
    # Implementation to detect cycles
    ...
```

#### 6.2 Protocol Testing Framework

**File**: `contracts/testing.py`

```python
from typing import Protocol, TypeVar, Any
import pytest

ProtocolT = TypeVar('ProtocolT', bound=Protocol)

class ProtocolTestSuite:
    """Base test suite for protocol implementations."""

    def test_protocol_compliance(self, implementation: Any, protocol: ProtocolT):
        """Test that implementation satisfies protocol."""
        errors = validate_protocol_implementation(implementation, protocol)
        assert not errors, f"Protocol violations: {errors}"

    def test_method_signatures(self, implementation: Any, protocol: ProtocolT):
        """Test method signatures match protocol."""
        # Compare method signatures
        ...

    def test_return_types(self, implementation: Any, protocol: ProtocolT):
        """Test return types match protocol."""
        # Validate return types
        ...
```

## 🧪 Testing Strategy

### 1. Protocol Compliance Tests

- Validate all implementations satisfy their contracts
- Check method signatures and return types
- Verify protocol inheritance chains

### 2. Circular Import Detection

- Automated checking for import cycles
- Integration with CI/CD to prevent regressions
- Clear error messages showing cycle paths

### 3. Integration Testing

- Test protocol boundaries work correctly
- Validate dependency injection patterns
- Ensure clean separation of concerns

## 📊 Success Metrics

### Technical Metrics

- [ ] **Zero circular imports** in final codebase
- [ ] **100% protocol coverage** for all major components
- [ ] **All contracts validated** with automated tests
- [ ] **Clean dependency graph** with proper layering

### Quality Metrics

- [ ] **Single responsibility** - each protocol has one clear purpose
- [ ] **Interface segregation** - narrow, focused contracts
- [ ] **Dependency inversion** - implementations depend on abstractions
- [ ] **Substitutability** - any implementation can replace another

## 🔗 Integration Points

### With Engine Domain

- Engine implementations must satisfy `EngineProtocol`
- Tool management through `ToolProtocol`
- Configuration via `EngineConfigDict`

### With Node Domain

- All nodes implement `NodeProtocol`
- Execution semantics via `ExecutableNodeProtocol`
- Validation through `ValidationProtocol`

### With Agent Domain

- Agents implement `AgentProtocol`
- Workflows implement `WorkflowProtocol`
- Multi-agents use coordination protocols

### With Schema Domain

- State management via `StateProtocol`
- Messages via `MessageProtocol`
- Configuration schemas as TypedDict

## 🚨 Common Pitfalls

### 1. Over-specifying Protocols

**Problem**: Making protocols too specific breaks substitutability
**Solution**: Focus on essential interface, not implementation details

### 2. Leaking Implementation Details

**Problem**: Protocols exposing internal structure
**Solution**: Only expose necessary public interface

### 3. Circular Protocol Dependencies

**Problem**: Protocols referencing each other in cycles
**Solution**: Use forward references and composition

### 4. Missing Protocol Methods

**Problem**: Forgetting edge cases in protocol definition
**Solution**: Comprehensive test coverage for all scenarios

## 🔄 Rollback Strategy

### If Implementation Issues Arise

1. **Isolate problem domain**: Each protocol is independent
2. **Revert specific protocol**: Roll back individual files
3. **Maintain compatibility**: Keep existing interfaces during rollback
4. **Re-evaluate approach**: Adjust protocol design based on lessons learned

### Risk Mitigation

- Start with least risky protocols (schema, message)
- Validate each protocol before dependent implementations
- Maintain backward compatibility during transition
- Comprehensive testing before any rollout

---

**Next Steps**:

1. Implement engine protocols first (most foundational)
2. Add comprehensive testing for each protocol
3. Begin refactoring existing code to use protocols
4. Validate circular import elimination
