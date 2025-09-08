# Node Consolidation Implementation Plan

**Domain**: Node Consolidation  
**Estimated Days**: 5-6 days  
**Target LOC**: 1,100 LOC (from 8,000 LOC - 62% reduction)  
**Dependencies**: [Contracts](../contracts/PROTOCOL_CONTRACTS_PLAN.md), [Engine](../engine/ENGINE_DECOMPOSITION_PLAN.md)

## 🎯 Overview

Consolidate 12+ scattered node types with overlapping functionality into 4 core, focused node types. This dramatically reduces complexity while providing clear separation of concerns for different execution patterns.

## 📊 Current State Analysis

### The Node Explosion Problem

```bash
# Current node structure (8,000 total LOC)
packages/haive-core/src/haive/core/graph/node/
├── agent_node.py                     # 800 LOC - Agent execution
├── agent_node_v2.py                  # 1,200 LOC - Enhanced agent
├── llm_node.py                       # 600 LOC - Direct LLM
├── tool_node.py                      # 700 LOC - Tool execution
├── validation_node.py                # 900 LOC - Validation logic
├── validation_node_v2.py             # 1,100 LOC - Enhanced validation
├── routing_node.py                   # 500 LOC - Routing decisions
├── conditional_node.py               # 450 LOC - Conditional logic
├── parallel_node.py                  # 400 LOC - Parallel execution
├── merge_node.py                     # 350 LOC - Result merging
├── start_node.py                     # 200 LOC - Graph entry
├── end_node.py                       # 200 LOC - Graph exit
└── custom_node.py                    # 500 LOC - Custom implementations
```

### Key Problems Identified

1. **Overlapping Functionality**: 6+ nodes doing similar validation/execution
2. **Version Proliferation**: Multiple "v2" versions without clear migration
3. **Mixed Concerns**: Single nodes handling execution + validation + routing
4. **Inconsistent Interfaces**: Each node has different method signatures
5. **Testing Complexity**: 12 different node types to test combinations

### Analysis of Current Node Responsibilities

| Current Node     | Execution | Validation | Routing | State Management |
| ---------------- | --------- | ---------- | ------- | ---------------- |
| AgentNode        | ✅        | ✅         | ❌      | ✅               |
| AgentNodeV2      | ✅        | ✅         | ✅      | ✅               |
| LLMNode          | ✅        | ❌         | ❌      | ❌               |
| ToolNode         | ✅        | ✅         | ❌      | ❌               |
| ValidationNode   | ❌        | ✅         | ❌      | ❌               |
| ValidationNodeV2 | ❌        | ✅         | ✅      | ❌               |
| RoutingNode      | ❌        | ❌         | ✅      | ❌               |
| ConditionalNode  | ✅        | ❌         | ✅      | ❌               |

**Problem**: Responsibilities scattered across 8+ node types with no clear pattern.

## 🏗️ Target Architecture

### Consolidated Structure (1,100 total LOC)

```
packages/haive-core/src/haive/core/graph/nodes/
├── __init__.py                       # Node exports (50 LOC)
├── base/
│   ├── __init__.py                  # Base exports (20 LOC)
│   ├── node_protocol.py             # Protocol implementation (150 LOC)
│   └── base_node.py                 # Common functionality (200 LOC)
├── execution_node.py                 # Pure execution (400 LOC)
├── validation_node.py                # Validation only (300 LOC)
├── routing_node.py                   # Routing logic (250 LOC)
├── terminal_node.py                  # Start/end nodes (150 LOC)
└── legacy/
    ├── __init__.py                  # Legacy exports (20 LOC)
    ├── node_facade.py               # Backward compatibility (300 LOC)
    └── migration_guide.md           # Migration documentation
```

**Total**: 8 files, ~1,100 LOC (62% reduction)

### Core Node Types (Single Responsibility)

1. **ExecutionNode**: Pure execution without validation/routing
2. **ValidationNode**: Validation only, no execution
3. **RoutingNode**: Routing decisions only, no execution
4. **TerminalNode**: Start/end markers with minimal logic

## 📋 Detailed Implementation Steps

### Step 1: Create Base Node Infrastructure (Day 1)

#### 1.1 Node Protocol Implementation

**File**: `base/node_protocol.py`

```python
from typing import Any, Dict, Optional, TypeVar, Generic
from haive.core.contracts.node.node_protocol import NodeProtocol, NodeMetadata
from haive.core.contracts.node.execution_protocol import ExecutionContext, ExecutionStatus

InputT = TypeVar('InputT')
OutputT = TypeVar('OutputT')
StateT = TypeVar('StateT')

class BaseNodeProtocol(NodeProtocol[InputT, OutputT, StateT]):
    """Base implementation of node protocol."""

    def __init__(self, name: str, node_type: str):
        self._name = name
        self._node_type = node_type
        self._metadata = NodeMetadata(node_type=node_type)
        self._execution_status = ExecutionStatus.PENDING

    @property
    def name(self) -> str:
        """Node identifier."""
        return self._name

    @property
    def node_type(self) -> str:
        """Type of node for routing."""
        return self._node_type

    def validate_input(self, input_data: InputT) -> bool:
        """Validate input before execution."""
        # Base validation - override in subclasses
        return input_data is not None

    async def aexecute(self, input_data: InputT, state: StateT) -> OutputT:
        """Execute node asynchronously."""
        raise NotImplementedError("Subclasses must implement aexecute")

    def execute(self, input_data: InputT, state: StateT) -> OutputT:
        """Execute node synchronously."""
        import asyncio
        return asyncio.run(self.aexecute(input_data, state))

    def get_metadata(self) -> NodeMetadata:
        """Get execution metadata."""
        return self._metadata

    def update_metadata(self, **kwargs) -> None:
        """Update metadata fields."""
        for key, value in kwargs.items():
            if key in self._metadata:
                self._metadata[key] = value
```

#### 1.2 Base Node Implementation

**File**: `base/base_node.py`

```python
import time
from typing import Any, Dict, Optional
from .node_protocol import BaseNodeProtocol

class BaseNode(BaseNodeProtocol[Dict[str, Any], Dict[str, Any], Dict[str, Any]]):
    """Common functionality for all nodes."""

    def __init__(self, name: str, node_type: str, timeout_seconds: int = 30):
        super().__init__(name, node_type)
        self.timeout_seconds = timeout_seconds
        self._start_time: Optional[float] = None

    async def aexecute(self, input_data: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute with timing and error handling."""
        self._start_time = time.time()
        self._execution_status = ExecutionStatus.RUNNING

        try:
            # Validate input
            if not self.validate_input(input_data):
                raise ValueError(f"Invalid input for {self.name}: {input_data}")

            # Execute core logic (implemented by subclasses)
            result = await self._execute_core(input_data, state)

            # Update metadata
            execution_time = int((time.time() - self._start_time) * 1000)
            self.update_metadata(
                execution_time_ms=execution_time,
                error=None
            )

            self._execution_status = ExecutionStatus.COMPLETED
            return result

        except Exception as e:
            execution_time = int((time.time() - self._start_time) * 1000)
            self.update_metadata(
                execution_time_ms=execution_time,
                error=str(e)
            )
            self._execution_status = ExecutionStatus.FAILED
            raise

    async def _execute_core(self, input_data: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, Any]:
        """Core execution logic - implement in subclasses."""
        raise NotImplementedError("Subclasses must implement _execute_core")

    def get_execution_status(self) -> ExecutionStatus:
        """Get current execution status."""
        return self._execution_status
```

### Step 2: Create Core Node Types (Days 2-3)

#### 2.1 Execution Node (Pure Execution)

**File**: `execution_node.py`

```python
from typing import Any, Dict, Callable, Optional
from .base.base_node import BaseNode
from haive.core.contracts.engine.engine_protocol import EngineProtocol

class ExecutionNode(BaseNode):
    """Pure execution node without validation or routing."""

    def __init__(
        self,
        name: str,
        engine: Optional[EngineProtocol] = None,
        executor: Optional[Callable] = None,
        **kwargs
    ):
        super().__init__(name, "execution", **kwargs)
        self.engine = engine
        self.executor = executor

        if not engine and not executor:
            raise ValueError("ExecutionNode requires either engine or executor")

    async def _execute_core(self, input_data: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute using engine or custom executor."""

        if self.engine:
            # Use engine execution
            result = await self.engine.arun(state)
            return {"result": result, "execution_type": "engine"}

        elif self.executor:
            # Use custom executor
            if asyncio.iscoroutinefunction(self.executor):
                result = await self.executor(input_data, state)
            else:
                result = self.executor(input_data, state)
            return {"result": result, "execution_type": "custom"}

        else:
            raise RuntimeError("No execution method available")

    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Basic input validation."""
        return isinstance(input_data, dict)
```

#### 2.2 Validation Node (Validation Only)

**File**: `validation_node.py`

```python
from typing import Any, Dict, List, Callable, Optional, Union
from pydantic import BaseModel
from .base.base_node import BaseNode

ValidationRule = Callable[[Any], bool]
ValidationModel = Union[type[BaseModel], BaseModel]

class ValidationNode(BaseNode):
    """Pure validation node without execution."""

    def __init__(
        self,
        name: str,
        validation_rules: Optional[List[ValidationRule]] = None,
        validation_model: Optional[ValidationModel] = None,
        **kwargs
    ):
        super().__init__(name, "validation", **kwargs)
        self.validation_rules = validation_rules or []
        self.validation_model = validation_model

    async def _execute_core(self, input_data: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, Any]:
        """Validate input and return validation result."""
        validation_results = []

        # Rule-based validation
        for i, rule in enumerate(self.validation_rules):
            try:
                is_valid = rule(input_data)
                validation_results.append({
                    "rule_index": i,
                    "valid": is_valid,
                    "error": None
                })
            except Exception as e:
                validation_results.append({
                    "rule_index": i,
                    "valid": False,
                    "error": str(e)
                })

        # Model-based validation
        model_validation_result = None
        if self.validation_model:
            try:
                if isinstance(self.validation_model, type):
                    validated_data = self.validation_model.model_validate(input_data)
                else:
                    validated_data = self.validation_model.__class__.model_validate(input_data)

                model_validation_result = {
                    "valid": True,
                    "validated_data": validated_data.model_dump(),
                    "error": None
                }
            except Exception as e:
                model_validation_result = {
                    "valid": False,
                    "validated_data": None,
                    "error": str(e)
                }

        # Overall validation result
        all_rules_valid = all(result["valid"] for result in validation_results)
        model_valid = model_validation_result is None or model_validation_result["valid"]

        return {
            "valid": all_rules_valid and model_valid,
            "rule_validations": validation_results,
            "model_validation": model_validation_result,
            "original_data": input_data
        }

    def add_validation_rule(self, rule: ValidationRule) -> None:
        """Add validation rule."""
        self.validation_rules.append(rule)

    def set_validation_model(self, model: ValidationModel) -> None:
        """Set validation model."""
        self.validation_model = model
```

#### 2.3 Routing Node (Routing Only)

**File**: `routing_node.py`

```python
from typing import Any, Dict, Callable, Optional, List
from .base.base_node import BaseNode

RoutingCondition = Callable[[Dict[str, Any]], bool]
RoutingFunction = Callable[[Dict[str, Any]], str]

class Route:
    """Single routing rule."""

    def __init__(self, name: str, condition: RoutingCondition, destination: str):
        self.name = name
        self.condition = condition
        self.destination = destination

class RoutingNode(BaseNode):
    """Pure routing node without execution."""

    def __init__(
        self,
        name: str,
        routes: Optional[List[Route]] = None,
        routing_function: Optional[RoutingFunction] = None,
        default_route: str = "default",
        **kwargs
    ):
        super().__init__(name, "routing", **kwargs)
        self.routes = routes or []
        self.routing_function = routing_function
        self.default_route = default_route

    async def _execute_core(self, input_data: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, Any]:
        """Determine routing destination."""

        # Use custom routing function if provided
        if self.routing_function:
            destination = self.routing_function(input_data)
            return {
                "destination": destination,
                "routing_type": "function",
                "matched_route": None,
                "original_data": input_data
            }

        # Use rule-based routing
        for route in self.routes:
            try:
                if route.condition(input_data):
                    return {
                        "destination": route.destination,
                        "routing_type": "rule",
                        "matched_route": route.name,
                        "original_data": input_data
                    }
            except Exception as e:
                # Log error but continue to next route
                print(f"Error in routing condition {route.name}: {e}")

        # Use default route if no matches
        return {
            "destination": self.default_route,
            "routing_type": "default",
            "matched_route": None,
            "original_data": input_data
        }

    def add_route(self, name: str, condition: RoutingCondition, destination: str) -> None:
        """Add routing rule."""
        self.routes.append(Route(name, condition, destination))

    def set_routing_function(self, func: RoutingFunction) -> None:
        """Set custom routing function."""
        self.routing_function = func
```

#### 2.4 Terminal Node (Start/End)

**File**: `terminal_node.py`

```python
from typing import Any, Dict, Optional
from .base.base_node import BaseNode
from enum import Enum

class TerminalType(str, Enum):
    """Types of terminal nodes."""
    START = "start"
    END = "end"

class TerminalNode(BaseNode):
    """Start and end nodes with minimal logic."""

    def __init__(
        self,
        name: str,
        terminal_type: TerminalType,
        initial_state: Optional[Dict[str, Any]] = None,
        **kwargs
    ):
        super().__init__(name, f"terminal_{terminal_type.value}", **kwargs)
        self.terminal_type = terminal_type
        self.initial_state = initial_state or {}

    async def _execute_core(self, input_data: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, Any]:
        """Minimal terminal node logic."""

        if self.terminal_type == TerminalType.START:
            # Initialize state with initial values
            result_state = {**state, **self.initial_state}
            return {
                "state": result_state,
                "terminal_type": "start",
                "input_data": input_data
            }

        elif self.terminal_type == TerminalType.END:
            # Finalize execution
            return {
                "final_result": input_data,
                "final_state": state,
                "terminal_type": "end",
                "execution_complete": True
            }

        else:
            raise ValueError(f"Unknown terminal type: {self.terminal_type}")

    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Terminal nodes accept any input."""
        return True
```

### Step 3: Create Backward Compatibility Layer (Day 4)

#### 3.1 Node Facade for Legacy Compatibility

**File**: `legacy/node_facade.py`

```python
from typing import Any, Dict, Optional
from ..execution_node import ExecutionNode
from ..validation_node import ValidationNode
from ..routing_node import RoutingNode
from ..terminal_node import TerminalNode, TerminalType

class AgentNode:
    """Backward compatibility facade for AgentNode."""

    def __init__(self, agent, name: str = None, **kwargs):
        """Initialize with legacy parameters."""
        self.agent = agent
        self.name = name or getattr(agent, 'name', 'agent_node')

        # Create execution node with agent
        self._execution_node = ExecutionNode(
            name=self.name,
            engine=getattr(agent, 'engine', None),
            **kwargs
        )

    async def aexecute(self, input_data: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute agent through execution node."""
        return await self._execution_node.aexecute(input_data, state)

    def execute(self, input_data: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute agent synchronously."""
        return self._execution_node.execute(input_data, state)

class ValidationNodeV2:
    """Backward compatibility facade for ValidationNodeV2."""

    def __init__(self, validation_rules=None, **kwargs):
        """Initialize with legacy parameters."""
        self._validation_node = ValidationNode(
            name=kwargs.get('name', 'validation_node'),
            validation_rules=validation_rules,
            **kwargs
        )

        # Legacy property access
        self.validation_rules = self._validation_node.validation_rules

    async def aexecute(self, input_data: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute validation through validation node."""
        return await self._validation_node.aexecute(input_data, state)

class ToolNode:
    """Backward compatibility facade for ToolNode."""

    def __init__(self, tool_config, **kwargs):
        """Initialize with legacy parameters."""
        self._execution_node = ExecutionNode(
            name=kwargs.get('name', 'tool_node'),
            engine=tool_config,  # Assuming tool_config is an engine
            **kwargs
        )

    async def aexecute(self, input_data: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute tool through execution node."""
        return await self._execution_node.aexecute(input_data, state)

# Additional facade classes as needed...
```

### Step 4: Integration & Testing (Days 5-6)

#### 4.1 Comprehensive Node Testing

**Unit Tests**: Test each node type in isolation

```python
# tests/graph/nodes/test_execution_node.py
import pytest
from haive.core.graph.nodes.execution_node import ExecutionNode

@pytest.mark.asyncio
class TestExecutionNode:
    async def test_custom_executor_execution(self):
        """Test execution with custom executor."""
        def simple_executor(input_data, state):
            return {"processed": input_data["value"] * 2}

        node = ExecutionNode(
            name="test_executor",
            executor=simple_executor
        )

        input_data = {"value": 5}
        state = {}

        result = await node.aexecute(input_data, state)

        assert result["result"]["processed"] == 10
        assert result["execution_type"] == "custom"

    async def test_async_executor(self):
        """Test execution with async executor."""
        async def async_executor(input_data, state):
            return {"async_result": input_data["data"]}

        node = ExecutionNode(
            name="test_async",
            executor=async_executor
        )

        result = await node.aexecute({"data": "test"}, {})
        assert result["result"]["async_result"] == "test"

    async def test_execution_timing(self):
        """Test execution timing metadata."""
        def slow_executor(input_data, state):
            import time
            time.sleep(0.1)  # 100ms delay
            return {"done": True}

        node = ExecutionNode(
            name="slow_node",
            executor=slow_executor
        )

        await node.aexecute({}, {})
        metadata = node.get_metadata()

        assert metadata["execution_time_ms"] >= 100
        assert metadata["error"] is None
```

**Integration Tests**: Test node combinations

```python
# tests/graph/nodes/test_node_integration.py
import pytest
from haive.core.graph.nodes.validation_node import ValidationNode
from haive.core.graph.nodes.execution_node import ExecutionNode
from haive.core.graph.nodes.routing_node import RoutingNode

@pytest.mark.asyncio
class TestNodeIntegration:
    async def test_validation_to_execution_flow(self):
        """Test validation followed by execution."""
        # Create validation node
        validation_node = ValidationNode(
            name="validator",
            validation_rules=[lambda x: "value" in x, lambda x: x["value"] > 0]
        )

        # Create execution node
        execution_node = ExecutionNode(
            name="executor",
            executor=lambda input_data, state: {"result": input_data["value"] * 2}
        )

        # Test valid data flow
        input_data = {"value": 5}

        # Validate first
        validation_result = await validation_node.aexecute(input_data, {})
        assert validation_result["valid"] is True

        # Execute if valid
        if validation_result["valid"]:
            execution_result = await execution_node.aexecute(input_data, {})
            assert execution_result["result"]["result"] == 10

    async def test_routing_based_execution(self):
        """Test routing determining execution path."""
        # Create routing node
        routing_node = RoutingNode(
            name="router",
            default_route="default_path"
        )
        routing_node.add_route(
            "positive",
            lambda x: x.get("value", 0) > 0,
            "positive_path"
        )
        routing_node.add_route(
            "negative",
            lambda x: x.get("value", 0) < 0,
            "negative_path"
        )

        # Test different routing paths
        positive_result = await routing_node.aexecute({"value": 5}, {})
        assert positive_result["destination"] == "positive_path"
        assert positive_result["matched_route"] == "positive"

        negative_result = await routing_node.aexecute({"value": -3}, {})
        assert negative_result["destination"] == "negative_path"
        assert negative_result["matched_route"] == "negative"

        default_result = await routing_node.aexecute({"value": 0}, {})
        assert default_result["destination"] == "default_path"
        assert default_result["matched_route"] is None
```

#### 4.2 Performance Testing

```python
# tests/graph/nodes/test_node_performance.py
import time
import pytest
from haive.core.graph.nodes.execution_node import ExecutionNode

def test_node_instantiation_performance():
    """Test node creation performance."""
    start_time = time.time()

    nodes = []
    for i in range(1000):
        node = ExecutionNode(
            name=f"node_{i}",
            executor=lambda x, s: {"result": x}
        )
        nodes.append(node)

    end_time = time.time()
    avg_time_ms = (end_time - start_time) * 1000 / 1000

    # Should be fast - target <0.1ms per node
    assert avg_time_ms < 0.1

@pytest.mark.asyncio
async def test_execution_overhead():
    """Test node execution overhead."""
    def minimal_executor(input_data, state):
        return input_data

    node = ExecutionNode(name="minimal", executor=minimal_executor)

    # Measure execution overhead
    input_data = {"test": "data"}
    state = {}

    start_time = time.time()
    for _ in range(100):
        await node.aexecute(input_data, state)
    end_time = time.time()

    avg_execution_ms = (end_time - start_time) * 1000 / 100

    # Should have minimal overhead - target <1ms per execution
    assert avg_execution_ms < 1.0
```

## 🧪 Testing Strategy

### 1. Property-Based Testing (Hypothesis)

```python
from hypothesis import given, strategies as st
from haive.core.graph.nodes.validation_node import ValidationNode

@given(
    input_dict=st.dictionaries(
        st.text(min_size=1, max_size=10),
        st.integers() | st.text() | st.booleans()
    )
)
@pytest.mark.asyncio
async def test_validation_node_properties(input_dict):
    """Property-based testing for validation node."""
    # Create validation node with simple rule
    node = ValidationNode(
        name="prop_validator",
        validation_rules=[lambda x: isinstance(x, dict)]
    )

    result = await node.aexecute(input_dict, {})

    # Properties that should always hold
    assert "valid" in result
    assert "rule_validations" in result
    assert "original_data" in result
    assert result["original_data"] == input_dict

    # Since input is always a dict, validation should pass
    assert result["valid"] is True
```

### 2. Golden Tests

```python
# tests/graph/nodes/golden/test_golden_node_outputs.py
import json
import pytest

def test_golden_execution_node_output():
    """Test against golden execution node output."""
    def test_executor(input_data, state):
        return {
            "processed_value": input_data["value"] * 2,
            "timestamp": "2025-01-08T00:00:00Z"  # Fixed for golden test
        }

    node = ExecutionNode(name="golden_test", executor=test_executor)

    # Load golden output
    with open("tests/graph/nodes/golden/execution_node_output.json") as f:
        expected_result = json.load(f)

    result = await node.aexecute({"value": 10}, {})

    # Compare against golden (excluding timing-dependent fields)
    assert result["result"] == expected_result["result"]
    assert result["execution_type"] == expected_result["execution_type"]
```

### 3. System Integration Tests

```python
# tests/graph/nodes/system/test_full_node_workflow.py
@pytest.mark.asyncio
async def test_complete_node_workflow():
    """Test complete workflow using all node types."""
    # Create a complete workflow: Start → Validate → Route → Execute → End

    start_node = TerminalNode("start", TerminalType.START, {"initialized": True})

    validation_node = ValidationNode(
        "validator",
        validation_rules=[lambda x: x.get("value", 0) > 0]
    )

    routing_node = RoutingNode("router")
    routing_node.add_route(
        "process", lambda x: x["validation"]["valid"], "execution"
    )

    execution_node = ExecutionNode(
        "executor",
        executor=lambda input_data, state: {"final_value": input_data["value"] * 10}
    )

    end_node = TerminalNode("end", TerminalType.END)

    # Execute workflow
    input_data = {"value": 5}
    state = {}

    # Start
    start_result = await start_node.aexecute(input_data, state)
    state.update(start_result["state"])

    # Validate
    validation_result = await validation_node.aexecute(input_data, state)

    # Route
    routing_input = {"value": input_data["value"], "validation": validation_result}
    routing_result = await routing_node.aexecute(routing_input, state)

    # Execute if routed correctly
    if routing_result["destination"] == "execution":
        execution_result = await execution_node.aexecute(input_data, state)

        # End
        final_result = await end_node.aexecute(execution_result["result"], state)

        assert final_result["execution_complete"] is True
        assert final_result["final_result"]["final_value"] == 50
```

## 📊 Success Metrics

### Technical Metrics

- [ ] **62% LOC reduction** (8,000 → 1,100 LOC)
- [ ] **4 core node types** (from 12+ scattered types)
- [ ] **Single responsibility** - each node has one clear purpose
- [ ] **100% test coverage** for all new node types
- [ ] **<0.1ms node instantiation** time

### Quality Metrics

- [ ] **Protocol compliance** - all nodes implement NodeProtocol
- [ ] **Consistent interfaces** - same method signatures across nodes
- [ ] **Clear separation** - no mixed concerns in single nodes
- [ ] **Backward compatibility** - all legacy nodes work through facades

### Performance Metrics

- [ ] **<1ms execution overhead** per node
- [ ] **Memory efficiency** - 50% reduction in object creation
- [ ] **Startup time** - 60% faster graph compilation

## 🔗 Integration Points

### With Contracts Domain

- All nodes implement `NodeProtocol` interface
- Execution semantics via `ExecutableNodeProtocol`
- Validation contracts via `ValidationProtocol`

### With Engine Domain

- Execution nodes use engine protocols
- Configuration passed through node execution
- Tool routing coordinates with node validation

### With Graph Domain

- Simplified graph construction with 4 node types
- Clear composition patterns for complex workflows
- Optimized graph compilation with focused nodes

### With Agent Domain

- Agent nodes use execution node internally
- Agent state management through node protocols
- Multi-agent coordination via routing nodes

## 🚨 Common Pitfalls

### 1. Regression in Functionality

**Problem**: Consolidated nodes missing features from original nodes
**Solution**: Comprehensive feature matrix and migration testing

### 2. Performance Overhead

**Problem**: Multiple small nodes slower than integrated nodes
**Solution**: Performance benchmarking and optimization

### 3. Complex Node Combinations

**Problem**: Simple tasks requiring multiple nodes
**Solution**: Composite node patterns and convenience factories

### 4. Backward Compatibility Issues

**Problem**: Existing graphs breaking with new node types
**Solution**: Gradual migration and comprehensive facade layer

## 🔄 Rollback Strategy

### If Consolidation Issues Arise

1. **Isolate problem node type**: Each node is independent
2. **Revert specific node**: Keep original implementations available
3. **Gradual rollback**: Restore one node type at a time
4. **Feature analysis**: Identify missing functionality and add back

### Risk Mitigation

- Maintain original node implementations during transition
- Comprehensive testing of all node combinations
- Performance monitoring to catch regressions
- Feature flags for new vs old node usage

---

**Next Steps**:

1. Start with ExecutionNode (most straightforward)
2. Add comprehensive testing for each node type
3. Build facade layer for backward compatibility
4. Validate performance improvements
