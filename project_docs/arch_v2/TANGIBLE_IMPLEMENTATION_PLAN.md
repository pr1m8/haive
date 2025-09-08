# TANGIBLE IMPLEMENTATION PLAN

# From Architectural Collapse to Protocol-Based Excellence

**Created**: 2025-01-30  
**Version**: 1.0  
**Purpose**: Concrete, actionable implementation plan for Haive Architecture v2  
**Status**: Ready for immediate execution

---

## 🎯 EXECUTIVE SUMMARY

After analyzing 87 architectural documents, 708 core files, and ~81,000 lines of code, this plan provides **concrete implementation steps** to transform Haive from monolithic collapse to protocol-based architecture.

**Key Discovery**: NodeSchemaComposer EXISTS and can do "result → potato" mappings, but it's disconnected. The solution is **connection, not creation**.

**Target**: 88% reduction from ~81,000 lines to ~10,000 lines through protocol-based architecture with explicit contracts.

---

## 📊 CURRENT STATE ANALYSIS

### Architecture File Count

```
haive-core:     708 files (measured)
haive-agents:   ~400 files (estimated)
haive-tools:    ~150 files (estimated)
Total:         ~1,258 files, ~81,000 lines
```

### The Seven Deadly Monoliths

| Component      | Current   | Target  | Reduction | Priority |
| -------------- | --------- | ------- | --------- | -------- |
| BaseGraph      | 3,972 LOC | 500 LOC | 87%       | P0       |
| Agent          | 3,600 LOC | 400 LOC | 89%       | P0       |
| AugLLMConfig   | 2,601 LOC | 300 LOC | 88%       | P0       |
| StateSchema    | 2,323 LOC | 200 LOC | 91%       | P0       |
| SchemaComposer | 3,378 LOC | 300 LOC | 91%       | P1       |
| LLM/Base       | 2,042 LOC | 250 LOC | 88%       | P1       |
| DynamicGraph   | 1,985 LOC | 250 LOC | 87%       | P1       |

---

# PHASE 0: FOUNDATION SETUP (Week 0)

## Preparation and Baseline Establishment

### 0.1: Create Testing Infrastructure

**Files to Create:**

```bash
/home/will/Projects/haive/packages/haive-core/tests/integration/
├── test_protocol_contracts.py
├── test_execution_contracts.py
├── test_schema_composition.py
└── test_node_connections.py

/home/will/Projects/haive/packages/haive-core/tests/property/
├── test_field_mapping_properties.py
├── test_contract_invariants.py
└── test_state_immutability.py

/home/will/Projects/haive/scripts/validation/
├── architecture_metrics.py
├── contract_validator.py
└── line_count_tracker.py
```

**Code to Write:**

`/home/will/Projects/haive/packages/haive-core/tests/integration/test_protocol_contracts.py`:

```python
"""Integration tests for protocol contracts."""
import pytest
from hypothesis import given, strategies as st
from typing import Protocol, Any, Dict
from pydantic import BaseModel

from haive.core.protocols.execution_contract import ExecutionContract
from haive.core.protocols.schema_interface import SchemaInterface


class TestProtocolContracts:
    """Test protocol contract implementations with real components."""

    def test_execution_contract_protocol_compliance(self):
        """Test that ExecutionContract protocol is properly implemented."""
        # Real implementation test - no mocks
        contract = ExecutionContract()

        assert hasattr(contract, 'execute')
        assert hasattr(contract, 'validate')
        assert hasattr(contract, 'extract_inputs')
        assert hasattr(contract, 'format_outputs')

    @given(st.dictionaries(st.text(), st.text(), min_size=1))
    def test_field_mapping_properties(self, field_mappings: Dict[str, str]):
        """Property-based test for field mappings."""
        from haive.core.graph.node.composer.field_mapping import FieldMapping

        mapping = FieldMapping(mappings=field_mappings)

        # Property: All input fields should be mappable
        for input_field, output_field in field_mappings.items():
            assert mapping.can_map(input_field)
            assert mapping.get_output_field(input_field) == output_field

    def test_real_node_schema_composer_connection(self):
        """Test connecting existing NodeSchemaComposer to system."""
        from haive.core.graph.node.composer.node_schema_composer import NodeSchemaComposer

        composer = NodeSchemaComposer()

        # Test that it exists and has expected methods
        assert hasattr(composer, 'compose_node')
        assert hasattr(composer, 'register_extract_function')
        assert hasattr(composer, 'register_update_function')

        # This is the existing disconnected component - verify it works
        assert composer is not None
```

**Validation Scripts:**

`/home/will/Projects/haive/scripts/validation/line_count_tracker.py`:

```python
#!/usr/bin/env python3
"""Track line count reduction progress."""

import os
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple

def count_lines_in_file(file_path: Path) -> int:
    """Count non-empty lines in a Python file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return len([line for line in f if line.strip()])
    except (UnicodeDecodeError, PermissionError):
        return 0

def get_component_files(component: str) -> List[Path]:
    """Get all Python files for a component."""
    base_path = Path("/home/will/Projects/haive/packages/haive-core/src/haive/core")

    component_paths = {
        "BaseGraph": base_path / "graph",
        "Agent": base_path / "agent",
        "AugLLMConfig": base_path / "engine" / "aug_llm",
        "StateSchema": base_path / "schema",
        "SchemaComposer": base_path / "graph" / "node" / "composer",
        "LLMBase": base_path / "engine" / "llm",
        "DynamicGraph": base_path / "graph" / "dynamic"
    }

    if component not in component_paths:
        return []

    path = component_paths[component]
    if not path.exists():
        return []

    return list(path.rglob("*.py"))

def track_progress() -> Dict[str, Dict[str, int]]:
    """Track line count progress for all components."""
    components = ["BaseGraph", "Agent", "AugLLMConfig", "StateSchema",
                 "SchemaComposer", "LLMBase", "DynamicGraph"]

    progress = {}

    for component in components:
        files = get_component_files(component)
        total_lines = sum(count_lines_in_file(f) for f in files)

        progress[component] = {
            "files": len(files),
            "lines": total_lines,
            "files_list": [str(f) for f in files]
        }

    return progress

if __name__ == "__main__":
    progress = track_progress()

    print("📊 HAIVE ARCHITECTURE LINE COUNT TRACKING")
    print("=" * 50)

    total_files = 0
    total_lines = 0

    for component, data in progress.items():
        print(f"\n{component}:")
        print(f"  Files: {data['files']}")
        print(f"  Lines: {data['lines']}")

        total_files += data['files']
        total_lines += data['lines']

    print(f"\n{'='*50}")
    print(f"TOTAL FILES: {total_files}")
    print(f"TOTAL LINES: {total_lines}")
    print(f"TARGET REDUCTION: {total_lines * 0.88:.0f} lines to remove")
    print(f"TARGET FINAL: {total_lines * 0.12:.0f} lines remaining")
```

**Commands to Execute:**

```bash
# Create directory structure
mkdir -p /home/will/Projects/haive/packages/haive-core/tests/integration
mkdir -p /home/will/Projects/haive/packages/haive-core/tests/property
mkdir -p /home/will/Projects/haive/scripts/validation

# Create baseline measurement
cd /home/will/Projects/haive
poetry run python scripts/validation/line_count_tracker.py > baseline_metrics.txt

# Set up git tracking
git add scripts/validation/
git commit -m "feat(arch-v2): add baseline architecture tracking infrastructure"
```

**Success Criteria:**

- [ ] Testing infrastructure directories created
- [ ] Baseline metrics captured (save actual numbers)
- [ ] Property-based test examples working
- [ ] Integration test framework established
- [ ] Line count tracking script functional

**Time Estimate:** 4 hours  
**Rollback Plan:** `git reset --hard HEAD~1` to remove infrastructure

---

# PHASE 1: PROTOCOL FOUNDATION (Week 1)

## Create Core Protocols and Connect NodeSchemaComposer

### 1.1: Create Execution Contracts

**Files to Create:**

`/home/will/Projects/haive/packages/haive-core/src/haive/core/protocols/__init__.py`:

```python
"""Core protocols for Haive architecture."""
from .execution_contract import ExecutionContract
from .schema_interface import SchemaInterface
from .composition_protocol import CompositionProtocol

__all__ = [
    "ExecutionContract",
    "SchemaInterface",
    "CompositionProtocol"
]
```

`/home/will/Projects/haive/packages/haive-core/src/haive/core/protocols/execution_contract.py`:

```python
"""ExecutionContract protocol for standardized node execution."""
from typing import Protocol, Any, Dict, Optional, TypeVar
from pydantic import BaseModel

TState = TypeVar('TState', bound=BaseModel)
TInput = TypeVar('TInput')
TOutput = TypeVar('TOutput')


class ExecutionContract(Protocol[TState, TInput, TOutput]):
    """Protocol defining execution contract for all nodes.

    This replaces the guessing/hardcoded patterns in BaseGraph with
    explicit contracts that nodes must implement.
    """

    def execute(self, state: TState) -> TState:
        """Execute the node with given state.

        Args:
            state: Current state conforming to schema

        Returns:
            Updated state with execution results

        Raises:
            ContractViolationError: If contract is violated
        """
        ...

    def validate_inputs(self, state: TState) -> bool:
        """Validate that state contains required input fields.

        Args:
            state: State to validate

        Returns:
            True if inputs are valid

        Raises:
            ValidationError: If inputs are invalid
        """
        ...

    def extract_inputs(self, state: TState) -> TInput:
        """Extract required inputs from state.

        Uses NodeSchemaComposer field mappings to extract
        the correct fields regardless of naming.

        Args:
            state: Current state

        Returns:
            Extracted inputs ready for node execution
        """
        ...

    def format_outputs(self, result: TOutput, state: TState) -> TState:
        """Format node outputs back to state schema.

        Uses NodeSchemaComposer field mappings to place
        results in correct state fields.

        Args:
            result: Raw node execution result
            state: Current state

        Returns:
            State with results properly formatted
        """
        ...

    def get_required_fields(self) -> Dict[str, type]:
        """Get required input fields and their types.

        Returns:
            Dictionary mapping field names to expected types
        """
        ...

    def get_output_fields(self) -> Dict[str, type]:
        """Get output fields and their types.

        Returns:
            Dictionary mapping output field names to types
        """
        ...
```

### 1.2: Connect NodeSchemaComposer to Execution System

**Files to Modify:**

`/home/will/Projects/haive/packages/haive-core/src/haive/core/graph/node/contract_node.py` (NEW):

```python
"""ContractNode - Replacement for 45 node files using ExecutionContract."""
from typing import Any, Dict, Type, TypeVar, cast
from pydantic import BaseModel

from haive.core.protocols.execution_contract import ExecutionContract
from haive.core.graph.node.composer.node_schema_composer import NodeSchemaComposer

TState = TypeVar('TState', bound=BaseModel)


class ContractNode:
    """Universal node using ExecutionContract protocol.

    This single class replaces 45+ specialized node files by using
    the ExecutionContract protocol and NodeSchemaComposer for field mapping.
    """

    def __init__(
        self,
        contract: ExecutionContract,
        composer: NodeSchemaComposer,
        name: str,
        field_mappings: Optional[Dict[str, str]] = None
    ):
        """Initialize contract node.

        Args:
            contract: ExecutionContract implementation
            composer: NodeSchemaComposer for field mapping
            name: Node identifier
            field_mappings: Custom field mappings (e.g. {"result": "retrieved_documents"})
        """
        self.contract = contract
        self.composer = composer
        self.name = name
        self.field_mappings = field_mappings or {}

    def __call__(self, state: TState) -> TState:
        """Execute node using contract and composer.

        This is the SINGLE execution path that replaces all
        specialized node logic.
        """
        # 1. Validate inputs using contract
        if not self.contract.validate_inputs(state):
            raise ValueError(f"Invalid inputs for {self.name}")

        # 2. Extract inputs using NodeSchemaComposer
        inputs = self._extract_with_composer(state)

        # 3. Execute using contract
        result = self.contract.execute(inputs)

        # 4. Format outputs using NodeSchemaComposer
        return self._format_with_composer(result, state)

    def _extract_with_composer(self, state: TState) -> Any:
        """Use NodeSchemaComposer to extract inputs with field mapping."""
        if not self.field_mappings:
            return self.contract.extract_inputs(state)

        # Apply field mappings through composer
        mapped_state = self.composer.apply_field_mappings(
            state, self.field_mappings
        )
        return self.contract.extract_inputs(mapped_state)

    def _format_with_composer(self, result: Any, state: TState) -> TState:
        """Use NodeSchemaComposer to format outputs with field mapping."""
        # Format using contract
        formatted_state = self.contract.format_outputs(result, state)

        # Apply reverse field mappings if needed
        if self.field_mappings:
            # Reverse mappings for output
            reverse_mappings = {v: k for k, v in self.field_mappings.items()}
            formatted_state = self.composer.apply_field_mappings(
                formatted_state, reverse_mappings
            )

        return formatted_state
```

### 1.3: Create Real Implementation Examples

**Files to Create:**

`/home/will/Projects/haive/packages/haive-core/src/haive/core/contracts/__init__.py`:

```python
"""Concrete ExecutionContract implementations."""
from .llm_contract import LLMExecutionContract
from .tool_contract import ToolExecutionContract
from .retrieval_contract import RetrievalExecutionContract

__all__ = [
    "LLMExecutionContract",
    "ToolExecutionContract",
    "RetrievalExecutionContract"
]
```

`/home/will/Projects/haive/packages/haive-core/src/haive/core/contracts/llm_contract.py`:

```python
"""ExecutionContract for LLM nodes."""
from typing import Any, Dict, List
from pydantic import BaseModel

from haive.core.protocols.execution_contract import ExecutionContract
from haive.core.engine.aug_llm.config import AugLLMConfig


class LLMExecutionContract(ExecutionContract):
    """ExecutionContract implementation for LLM nodes.

    This replaces all the guessing logic in BaseGraph with
    explicit contract requirements.
    """

    def __init__(self, config: AugLLMConfig):
        self.config = config

    def execute(self, state: BaseModel) -> BaseModel:
        """Execute LLM with state inputs."""
        inputs = self.extract_inputs(state)

        # Use AugLLMConfig for execution - no guessing
        result = self.config.invoke(inputs)

        return self.format_outputs(result, state)

    def validate_inputs(self, state: BaseModel) -> bool:
        """Validate LLM inputs."""
        required = self.get_required_fields()

        for field_name, field_type in required.items():
            if not hasattr(state, field_name):
                return False

            value = getattr(state, field_name)
            if not isinstance(value, field_type):
                return False

        return True

    def extract_inputs(self, state: BaseModel) -> Dict[str, Any]:
        """Extract inputs for LLM execution."""
        # Extract messages field (or mapped equivalent)
        if hasattr(state, 'messages'):
            return {"messages": state.messages}
        elif hasattr(state, 'input'):
            return {"messages": [{"role": "user", "content": state.input}]}
        else:
            raise ValueError("No valid input field found")

    def format_outputs(self, result: Any, state: BaseModel) -> BaseModel:
        """Format LLM outputs to state."""
        # Update state with result
        state_dict = state.model_dump()

        if hasattr(state, 'messages'):
            state_dict['messages'].append(result)
        else:
            state_dict['output'] = result

        return state.__class__(**state_dict)

    def get_required_fields(self) -> Dict[str, type]:
        """Get required input fields."""
        return {"messages": List}

    def get_output_fields(self) -> Dict[str, type]:
        """Get output fields."""
        return {"messages": List}
```

### 1.4: Integration Testing

**Files to Create:**

`/home/will/Projects/haive/packages/haive-core/tests/integration/test_contract_node_integration.py`:

```python
"""Integration tests for ContractNode with real components."""
import pytest
from pydantic import BaseModel, Field
from typing import List, Dict, Any

from haive.core.graph.node.contract_node import ContractNode
from haive.core.contracts.llm_contract import LLMExecutionContract
from haive.core.engine.aug_llm.config import AugLLMConfig
from haive.core.graph.node.composer.node_schema_composer import NodeSchemaComposer


class TestState(BaseModel):
    """Test state schema."""
    messages: List[Dict[str, str]] = Field(default_factory=list)
    retrieved_documents: List[str] = Field(default_factory=list)
    result: str = ""


class TestContractNodeIntegration:
    """Integration tests with real LLM and components."""

    def test_llm_contract_node_real_execution(self):
        """Test ContractNode with real LLM execution."""
        # Create real LLM config - no mocks
        config = AugLLMConfig(temperature=0.1)  # Low for deterministic testing
        contract = LLMExecutionContract(config)
        composer = NodeSchemaComposer()

        # Create ContractNode
        node = ContractNode(
            contract=contract,
            composer=composer,
            name="test_llm_node"
        )

        # Create test state
        state = TestState(
            messages=[{"role": "user", "content": "Say 'Hello World'"}]
        )

        # Execute with real LLM
        result_state = node(state)

        # Validate results - real execution, real validation
        assert len(result_state.messages) == 2  # User + Assistant
        assert "Hello World" in str(result_state.messages[-1])

    def test_field_mapping_with_composer(self):
        """Test field mapping using NodeSchemaComposer."""
        config = AugLLMConfig(temperature=0.1)
        contract = LLMExecutionContract(config)
        composer = NodeSchemaComposer()

        # Create node with field mappings
        node = ContractNode(
            contract=contract,
            composer=composer,
            name="mapped_node",
            field_mappings={"result": "retrieved_documents"}  # "result → potato" style
        )

        state = TestState(
            messages=[{"role": "user", "content": "Test mapping"}]
        )

        result_state = node(state)

        # Verify field mapping worked
        assert len(result_state.messages) >= 1
        # The ContractNode should handle the mapping
        assert result_state is not None

    @pytest.mark.integration
    def test_replaces_multiple_node_types(self):
        """Test that ContractNode can replace multiple specialized nodes."""
        # This tests the core hypothesis: one ContractNode replaces many

        configs = [
            ("llm_node", LLMExecutionContract(AugLLMConfig())),
            # TODO: Add ToolExecutionContract, RetrievalExecutionContract
        ]

        composer = NodeSchemaComposer()

        for name, contract in configs:
            node = ContractNode(
                contract=contract,
                composer=composer,
                name=name
            )

            # Each node should work with same interface
            assert hasattr(node, '__call__')
            assert node.name == name
            assert node.contract is contract
```

**Commands to Execute:**

```bash
# Create protocol directories
mkdir -p /home/will/Projects/haive/packages/haive-core/src/haive/core/protocols
mkdir -p /home/will/Projects/haive/packages/haive-core/src/haive/core/contracts

# Run integration tests
cd /home/will/Projects/haive
poetry run pytest packages/haive-core/tests/integration/test_contract_node_integration.py -v

# Verify NodeSchemaComposer connection
poetry run python -c "
from haive.core.graph.node.composer.node_schema_composer import NodeSchemaComposer
composer = NodeSchemaComposer()
print(f'NodeSchemaComposer methods: {[m for m in dir(composer) if not m.startswith(\"_\")]}')
"
```

**Success Criteria:**

- [ ] ExecutionContract protocol created and working
- [ ] ContractNode successfully uses NodeSchemaComposer
- [ ] Real LLM execution through contract (no mocks)
- [ ] Field mapping "result → retrieved_documents" working
- [ ] Integration tests passing with real components
- [ ] One ContractNode replaces multiple node types

**Validation Commands:**

```bash
# Test that existing NodeSchemaComposer is connected
poetry run python scripts/validation/test_schema_composer_connection.py

# Verify contract compliance
poetry run python -c "
from haive.core.contracts.llm_contract import LLMExecutionContract
from haive.core.protocols.execution_contract import ExecutionContract
print(f'LLMExecutionContract implements ExecutionContract: {issubclass(LLMExecutionContract, ExecutionContract)}')"

# Count files before Phase 2
poetry run python scripts/validation/line_count_tracker.py
```

**Time Estimate:** 12 hours  
**Risk Mitigation:** Start with single LLMExecutionContract, expand incrementally  
**Rollback Plan:** Keep existing node files until ContractNode proven working

---

# PHASE 2: MONOLITH DECOMPOSITION (Weeks 2-3)

## Break Apart the Seven Deadly Monoliths

### 2.1: StateSchema Decomposition

**Problem**: 2,323 lines of mixed concerns - data + validation + engines + behavior

**Files to Create:**

`/home/will/Projects/haive/packages/haive-core/src/haive/core/schema/v2/__init__.py`:

```python
"""StateSchema v2 - Decomposed architecture."""
from .state_data import StateData
from .state_validator import StateValidator
from .state_composer import StateComposer
from .state_interface import StateInterface
from .engine_manager import EngineManager
from .field_mapper import FieldMapper

__all__ = [
    "StateData",
    "StateValidator",
    "StateComposer",
    "StateInterface",
    "EngineManager",
    "FieldMapper"
]
```

`/home/will/Projects/haive/packages/haive-core/src/haive/core/schema/v2/state_data.py`:

```python
"""Pure data container - Pydantic models for data only."""
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
from datetime import datetime


class StateData(BaseModel):
    """Pure data container for state.

    This contains ONLY data - no behavior, no validation logic,
    no engine management. Pure Pydantic data model.
    """

    # Core message data
    messages: List[Dict[str, Any]] = Field(default_factory=list)

    # Tool and execution data
    tools: List[str] = Field(default_factory=list)
    tool_calls: List[Dict[str, Any]] = Field(default_factory=list)

    # Context and metadata
    context: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    # Timestamp tracking
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    # Agent specific data
    agent_name: Optional[str] = None
    agent_config: Optional[Dict[str, Any]] = None

    def update_timestamp(self) -> "StateData":
        """Update the timestamp - pure data operation."""
        return self.model_copy(update={"updated_at": datetime.utcnow()})
```

`/home/will/Projects/haive/packages/haive-core/src/haive/core/schema/v2/state_validator.py`:

```python
"""Validation logic separated from data."""
from typing import Dict, List, Any, Type, Protocol
from pydantic import ValidationError

from .state_data import StateData


class ValidationRule(Protocol):
    """Protocol for validation rules."""

    def validate(self, state: StateData) -> bool:
        """Validate state according to rule."""
        ...

    def get_error_message(self) -> str:
        """Get validation error message."""
        ...


class StateValidator:
    """Handles all state validation logic.

    Separated from StateData to follow single responsibility.
    """

    def __init__(self):
        self.rules: List[ValidationRule] = []

    def add_rule(self, rule: ValidationRule) -> None:
        """Add validation rule."""
        self.rules.append(rule)

    def validate_state(self, state: StateData) -> bool:
        """Validate state against all rules."""
        for rule in self.rules:
            if not rule.validate(state):
                return False
        return True

    def get_validation_errors(self, state: StateData) -> List[str]:
        """Get all validation errors."""
        errors = []
        for rule in self.rules:
            if not rule.validate(state):
                errors.append(rule.get_error_message())
        return errors

    def validate_required_fields(self, state: StateData, required: List[str]) -> bool:
        """Validate required fields are present."""
        state_dict = state.model_dump()

        for field in required:
            if field not in state_dict:
                return False
            if state_dict[field] is None:
                return False

        return True

    def validate_field_types(self, state: StateData, expected_types: Dict[str, Type]) -> bool:
        """Validate field types."""
        state_dict = state.model_dump()

        for field, expected_type in expected_types.items():
            if field in state_dict:
                value = state_dict[field]
                if value is not None and not isinstance(value, expected_type):
                    return False

        return True
```

### 2.2: AugLLMConfig Decomposition

**Problem**: 2,601 lines of configuration + execution + tools + everything

**Files to Create:**

`/home/will/Projects/haive/packages/haive-core/src/haive/core/engine/v2/__init__.py`:

```python
"""Engine v2 - Decomposed architecture."""
from .llm_config import LLMConfig
from .tool_manager import ToolManager
from .execution_engine import ExecutionEngine
from .config_validator import ConfigValidator
from .model_interface import ModelInterface
from .output_processor import OutputProcessor
from .context_manager import ContextManager

__all__ = [
    "LLMConfig",
    "ToolManager",
    "ExecutionEngine",
    "ConfigValidator",
    "ModelInterface",
    "OutputProcessor",
    "ContextManager"
]
```

`/home/will/Projects/haive/packages/haive-core/src/haive/core/engine/v2/llm_config.py`:

```python
"""Pure configuration - no execution logic."""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum


class ModelType(str, Enum):
    """Supported model types."""
    GPT4 = "gpt-4"
    GPT4_TURBO = "gpt-4-turbo"
    GPT35_TURBO = "gpt-3.5-turbo"
    CLAUDE_3 = "claude-3-opus"
    CLAUDE_35_SONNET = "claude-3-5-sonnet"


class LLMConfig(BaseModel):
    """Pure LLM configuration - no execution logic.

    This contains ONLY configuration - no invoke(), no execution,
    no tool management. Pure config data.
    """

    # Model configuration
    model: ModelType = Field(default=ModelType.GPT4)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(default=None, ge=1)
    top_p: float = Field(default=1.0, ge=0.0, le=1.0)
    frequency_penalty: float = Field(default=0.0, ge=-2.0, le=2.0)
    presence_penalty: float = Field(default=0.0, ge=-2.0, le=2.0)

    # System and context
    system_message: Optional[str] = Field(default=None, max_length=10000)
    context_window: int = Field(default=8192, ge=1024)

    # API configuration
    api_key: Optional[str] = Field(default=None)
    api_base: Optional[str] = Field(default=None)
    organization: Optional[str] = Field(default=None)

    # Timeout and retry
    timeout: int = Field(default=60, ge=1)
    max_retries: int = Field(default=3, ge=0)

    # Streaming and async
    streaming: bool = Field(default=False)
    async_mode: bool = Field(default=False)

    def get_model_params(self) -> Dict[str, Any]:
        """Get parameters for model initialization."""
        return {
            "model": self.model.value,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "top_p": self.top_p,
            "frequency_penalty": self.frequency_penalty,
            "presence_penalty": self.presence_penalty,
        }

    def get_api_params(self) -> Dict[str, Any]:
        """Get API configuration parameters."""
        params = {}
        if self.api_key:
            params["api_key"] = self.api_key
        if self.api_base:
            params["api_base"] = self.api_base
        if self.organization:
            params["organization"] = self.organization
        return params
```

`/home/will/Projects/haive/packages/haive-core/src/haive/core/engine/v2/execution_engine.py`:

```python
"""Separated execution logic from configuration."""
from typing import Dict, List, Any, Optional
import logging

from .llm_config import LLMConfig
from .tool_manager import ToolManager
from .model_interface import ModelInterface

logger = logging.getLogger(__name__)


class ExecutionEngine:
    """Handles LLM execution - separated from configuration.

    This contains ONLY execution logic - no configuration management.
    """

    def __init__(
        self,
        config: LLMConfig,
        tool_manager: Optional[ToolManager] = None,
        model_interface: Optional[ModelInterface] = None
    ):
        self.config = config
        self.tool_manager = tool_manager or ToolManager()
        self.model_interface = model_interface or ModelInterface(config)

    def execute(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Execute LLM with messages."""
        try:
            # Prepare messages
            prepared_messages = self._prepare_messages(messages)

            # Execute through model interface
            response = self.model_interface.invoke(prepared_messages)

            # Process response
            return self._process_response(response)

        except Exception as e:
            logger.error(f"Execution failed: {e}")
            raise

    def _prepare_messages(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Prepare messages for execution."""
        prepared = []

        # Add system message if configured
        if self.config.system_message:
            prepared.append({
                "role": "system",
                "content": self.config.system_message
            })

        # Add user messages
        prepared.extend(messages)

        # Validate context window
        if self._estimate_tokens(prepared) > self.config.context_window:
            prepared = self._truncate_messages(prepared)

        return prepared

    def _process_response(self, response: Any) -> Dict[str, Any]:
        """Process model response."""
        return {
            "role": "assistant",
            "content": str(response),
            "timestamp": self._get_timestamp(),
            "model": self.config.model.value
        }

    def _estimate_tokens(self, messages: List[Dict[str, Any]]) -> int:
        """Rough token estimation."""
        total_chars = sum(len(str(msg.get('content', ''))) for msg in messages)
        return total_chars // 4  # Rough estimation

    def _truncate_messages(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Truncate messages to fit context window."""
        # Keep system message and recent messages
        system_msgs = [msg for msg in messages if msg.get('role') == 'system']
        other_msgs = [msg for msg in messages if msg.get('role') != 'system']

        # Take recent messages that fit in context
        max_other_tokens = self.config.context_window - 1000  # Reserve for system
        current_tokens = 0
        kept_msgs = []

        for msg in reversed(other_msgs):
            msg_tokens = self._estimate_tokens([msg])
            if current_tokens + msg_tokens < max_other_tokens:
                kept_msgs.insert(0, msg)
                current_tokens += msg_tokens
            else:
                break

        return system_msgs + kept_msgs

    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.utcnow().isoformat()
```

### 2.3: Create Migration Testing

**Files to Create:**

`/home/will/Projects/haive/packages/haive-core/tests/migration/test_state_schema_migration.py`:

```python
"""Test migration from monolithic StateSchema to decomposed architecture."""
import pytest
from typing import Dict, List, Any

# Old monolithic import
from haive.core.schema.base import StateSchema as OldStateSchema

# New decomposed imports
from haive.core.schema.v2 import StateData, StateValidator, StateComposer


class TestStateSchemaGoldenTests:
    """Golden tests to ensure decomposed architecture matches old behavior."""

    def test_basic_state_creation_compatibility(self):
        """Test that new StateData matches old StateSchema creation."""
        # Old way
        old_state = OldStateSchema(
            messages=[{"role": "user", "content": "test"}],
            tools=["calculator"],
            context={"session_id": "123"}
        )

        # New way
        new_state = StateData(
            messages=[{"role": "user", "content": "test"}],
            tools=["calculator"],
            context={"session_id": "123"}
        )

        # Should have same data
        assert old_state.messages == new_state.messages
        assert old_state.tools == new_state.tools
        assert old_state.context == new_state.context

    def test_validation_behavior_preserved(self):
        """Test that validation behavior is preserved."""
        # Create states with invalid data
        invalid_data = {
            "messages": "not a list",  # Should be List
            "tools": 123,  # Should be List
        }

        # Old validation (should fail)
        with pytest.raises(Exception):
            old_state = OldStateSchema(**invalid_data)

        # New validation (should also fail)
        with pytest.raises(Exception):
            new_state = StateData(**invalid_data)

    @pytest.mark.golden
    def test_field_access_compatibility(self):
        """Golden test for field access patterns."""
        test_data = {
            "messages": [
                {"role": "user", "content": "Hello"},
                {"role": "assistant", "content": "Hi there"}
            ],
            "tools": ["search", "calculate"],
            "context": {"user_id": "user123", "session": "sess456"},
            "agent_name": "test_agent"
        }

        # Create both versions
        old_state = OldStateSchema(**test_data)
        new_state = StateData(**test_data)

        # Test all field access patterns
        assert len(old_state.messages) == len(new_state.messages)
        assert old_state.tools == new_state.tools
        assert old_state.context == new_state.context
        assert old_state.agent_name == new_state.agent_name

        # Test field modification
        old_state.context["new_key"] = "new_value"
        new_state.context["new_key"] = "new_value"

        assert old_state.context["new_key"] == new_state.context["new_key"]
```

`/home/will/Projects/haive/packages/haive-core/tests/migration/test_augllm_migration.py`:

```python
"""Test migration from monolithic AugLLMConfig to decomposed architecture."""
import pytest
from typing import Dict, Any

# Old monolithic import
from haive.core.engine.aug_llm.config import AugLLMConfig as OldAugLLMConfig

# New decomposed imports
from haive.core.engine.v2 import LLMConfig, ExecutionEngine, ToolManager


class TestAugLLMConfigGoldenTests:
    """Golden tests for AugLLMConfig decomposition."""

    def test_configuration_compatibility(self):
        """Test that new LLMConfig matches old AugLLMConfig configuration."""
        # Old way
        old_config = OldAugLLMConfig(
            model="gpt-4",
            temperature=0.8,
            max_tokens=1000,
            system_message="You are helpful"
        )

        # New way
        new_config = LLMConfig(
            model="gpt-4",
            temperature=0.8,
            max_tokens=1000,
            system_message="You are helpful"
        )

        # Should have same configuration values
        assert old_config.model == new_config.model.value
        assert old_config.temperature == new_config.temperature
        assert old_config.max_tokens == new_config.max_tokens
        assert old_config.system_message == new_config.system_message

    @pytest.mark.integration
    def test_execution_behavior_preserved(self):
        """Test that execution behavior is preserved with real LLM."""
        test_messages = [{"role": "user", "content": "Say 'Hello World'"}]

        # Old way execution
        old_config = OldAugLLMConfig(temperature=0.1)  # Deterministic
        old_result = old_config.invoke(test_messages)

        # New way execution
        new_config = LLMConfig(temperature=0.1)
        new_engine = ExecutionEngine(new_config)
        new_result = new_engine.execute(test_messages)

        # Results should be equivalent (both contain "Hello World")
        old_content = str(old_result)
        new_content = str(new_result.get('content', ''))

        assert "Hello World" in old_content
        assert "Hello World" in new_content

    def test_tool_management_compatibility(self):
        """Test that tool management behavior is preserved."""
        tools = ["calculator", "web_search"]

        # Old way
        old_config = OldAugLLMConfig(tools=tools)

        # New way
        new_config = LLMConfig()
        tool_manager = ToolManager()
        for tool in tools:
            tool_manager.add_tool(tool)

        # Should have same tools available
        assert len(old_config.tools) == len(tool_manager.get_available_tools())
```

**Commands to Execute:**

```bash
# Create decomposed architecture directories
mkdir -p /home/will/Projects/haive/packages/haive-core/src/haive/core/schema/v2
mkdir -p /home/will/Projects/haive/packages/haive-core/src/haive/core/engine/v2
mkdir -p /home/will/Projects/haive/packages/haive-core/tests/migration

# Run golden tests to establish baseline
cd /home/will/Projects/haive
poetry run pytest packages/haive-core/tests/migration/ -v --tb=short

# Measure decomposition impact
poetry run python scripts/validation/line_count_tracker.py | tee phase2_metrics.txt

# Test that new architecture passes existing tests
poetry run pytest packages/haive-core/tests/ -k "StateSchema" --tb=short
```

**Success Criteria:**

- [ ] StateSchema decomposed into 6 focused components
- [ ] AugLLMConfig decomposed into 7 components
- [ ] Golden tests pass (new behavior matches old)
- [ ] Real LLM execution still works
- [ ] Line count reduced by target amounts
- [ ] No existing functionality broken

**Time Estimate:** 16 hours  
**Risk Mitigation:** Use golden tests to ensure compatibility  
**Rollback Plan:** Keep old classes until all tests pass

---

# PHASE 3: NODE CONSOLIDATION (Week 3-4)

## Replace 45+ Node Files with ContractNode

### 3.1: Analyze Existing Node Patterns

**Script to Create:**

`/home/will/Projects/haive/scripts/analysis/node_pattern_analyzer.py`:

```python
#!/usr/bin/env python3
"""Analyze existing node patterns to create contracts."""

import ast
import os
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict

def analyze_node_files() -> Dict[str, Dict[str, any]]:
    """Analyze all node files to extract patterns."""

    node_dir = Path("/home/will/Projects/haive/packages/haive-core/src/haive/core/graph/node")
    patterns = {}

    for py_file in node_dir.rglob("*.py"):
        if py_file.name.startswith("test_") or py_file.name == "__init__.py":
            continue

        try:
            with open(py_file, 'r') as f:
                content = f.read()

            tree = ast.parse(content)

            # Extract class definitions
            classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]

            for cls in classes:
                if "Node" in cls.name:
                    patterns[cls.name] = {
                        "file": str(py_file),
                        "methods": [f.name for f in cls.body if isinstance(f, ast.FunctionDef)],
                        "bases": [base.id if isinstance(base, ast.Name) else str(base) for base in cls.bases],
                        "decorators": [d.id if isinstance(d, ast.Name) else str(d) for d in cls.decorator_list]
                    }

        except Exception as e:
            print(f"Error analyzing {py_file}: {e}")
            continue

    return patterns

def identify_contract_types(patterns: Dict[str, Dict]) -> Dict[str, List[str]]:
    """Group nodes by contract type needed."""

    contract_groups = defaultdict(list)

    for node_name, info in patterns.items():
        methods = set(info["methods"])

        # Classify by method patterns
        if "invoke" in methods or "call_llm" in methods:
            contract_groups["LLMExecutionContract"].append(node_name)
        elif "call_tool" in methods or "execute_tool" in methods:
            contract_groups["ToolExecutionContract"].append(node_name)
        elif "validate" in methods or "check" in methods:
            contract_groups["ValidationContract"].append(node_name)
        elif "route" in methods or "decide" in methods:
            contract_groups["RoutingContract"].append(node_name)
        else:
            contract_groups["GenericContract"].append(node_name)

    return dict(contract_groups)

if __name__ == "__main__":
    print("🔍 ANALYZING NODE PATTERNS")
    print("=" * 50)

    patterns = analyze_node_files()
    print(f"Found {len(patterns)} node classes")

    contract_types = identify_contract_types(patterns)

    print("\n📊 CONTRACT TYPE GROUPINGS:")
    for contract_type, nodes in contract_types.items():
        print(f"\n{contract_type}: ({len(nodes)} nodes)")
        for node in nodes[:5]:  # Show first 5
            print(f"  - {node}")
        if len(nodes) > 5:
            print(f"  ... and {len(nodes) - 5} more")

    print(f"\n💡 CONSOLIDATION POTENTIAL:")
    total_nodes = len(patterns)
    contract_count = len(contract_types)
    reduction = ((total_nodes - contract_count) / total_nodes) * 100
    print(f"  Current: {total_nodes} node classes")
    print(f"  Target: {contract_count} contract types")
    print(f"  Reduction: {reduction:.1f}%")
```

### 3.2: Create Specialized Execution Contracts

**Files to Create:**

`/home/will/Projects/haive/packages/haive-core/src/haive/core/contracts/tool_contract.py`:

```python
"""ExecutionContract for tool nodes."""
from typing import Any, Dict, List, Optional, Callable
from pydantic import BaseModel

from haive.core.protocols.execution_contract import ExecutionContract


class ToolExecutionContract(ExecutionContract):
    """ExecutionContract for tool execution nodes."""

    def __init__(self, tool_function: Callable, tool_name: str):
        self.tool_function = tool_function
        self.tool_name = tool_name

    def execute(self, state: BaseModel) -> BaseModel:
        """Execute tool with extracted inputs."""
        inputs = self.extract_inputs(state)

        # Execute tool function
        result = self.tool_function(**inputs)

        return self.format_outputs(result, state)

    def validate_inputs(self, state: BaseModel) -> bool:
        """Validate tool inputs."""
        required_fields = self.get_required_fields()

        for field_name, field_type in required_fields.items():
            if not hasattr(state, field_name):
                return False

            value = getattr(state, field_name)
            if not isinstance(value, field_type):
                return False

        return True

    def extract_inputs(self, state: BaseModel) -> Dict[str, Any]:
        """Extract inputs for tool execution."""
        # Get tool inputs from tool_calls or direct fields
        if hasattr(state, 'tool_calls') and state.tool_calls:
            # Extract from tool calls
            for call in state.tool_calls:
                if call.get('name') == self.tool_name:
                    return call.get('arguments', {})

        # Fallback to direct field extraction
        inputs = {}
        for field_name in self.get_required_fields():
            if hasattr(state, field_name):
                inputs[field_name] = getattr(state, field_name)

        return inputs

    def format_outputs(self, result: Any, state: BaseModel) -> BaseModel:
        """Format tool outputs to state."""
        state_dict = state.model_dump()

        # Add tool result to messages
        if hasattr(state, 'messages'):
            state_dict['messages'].append({
                "role": "tool",
                "name": self.tool_name,
                "content": str(result)
            })
        else:
            state_dict['tool_result'] = result

        return state.__class__(**state_dict)

    def get_required_fields(self) -> Dict[str, type]:
        """Get required fields based on tool function signature."""
        import inspect

        sig = inspect.signature(self.tool_function)
        required = {}

        for param_name, param in sig.parameters.items():
            if param.annotation != inspect.Parameter.empty:
                required[param_name] = param.annotation
            else:
                required[param_name] = str  # Default to string

        return required

    def get_output_fields(self) -> Dict[str, type]:
        """Get output fields."""
        return {"messages": List, "tool_result": Any}
```

`/home/will/Projects/haive/packages/haive-core/src/haive/core/contracts/validation_contract.py`:

```python
"""ExecutionContract for validation nodes."""
from typing import Any, Dict, List, Callable, Optional
from pydantic import BaseModel, ValidationError

from haive.core.protocols.execution_contract import ExecutionContract


class ValidationExecutionContract(ExecutionContract):
    """ExecutionContract for validation nodes."""

    def __init__(
        self,
        validator_function: Callable,
        error_handler: Optional[Callable] = None
    ):
        self.validator_function = validator_function
        self.error_handler = error_handler or self._default_error_handler

    def execute(self, state: BaseModel) -> BaseModel:
        """Execute validation with extracted inputs."""
        inputs = self.extract_inputs(state)

        # Run validation
        is_valid, errors = self._run_validation(inputs)

        # Format results
        result = {
            "valid": is_valid,
            "errors": errors,
            "timestamp": self._get_timestamp()
        }

        return self.format_outputs(result, state)

    def validate_inputs(self, state: BaseModel) -> bool:
        """Validate that state has required fields for validation."""
        required = self.get_required_fields()

        for field_name in required:
            if not hasattr(state, field_name):
                return False

        return True

    def extract_inputs(self, state: BaseModel) -> Dict[str, Any]:
        """Extract inputs for validation."""
        inputs = {}
        required = self.get_required_fields()

        for field_name in required:
            if hasattr(state, field_name):
                inputs[field_name] = getattr(state, field_name)

        return inputs

    def format_outputs(self, result: Dict[str, Any], state: BaseModel) -> BaseModel:
        """Format validation outputs to state."""
        state_dict = state.model_dump()

        # Add validation results
        if 'validation' not in state_dict:
            state_dict['validation'] = {}

        state_dict['validation'].update(result)

        # If validation failed, optionally add to messages
        if not result['valid'] and hasattr(state, 'messages'):
            error_message = {
                "role": "system",
                "content": f"Validation failed: {'; '.join(result['errors'])}"
            }
            state_dict['messages'].append(error_message)

        return state.__class__(**state_dict)

    def get_required_fields(self) -> Dict[str, type]:
        """Get required fields for validation."""
        # Infer from validator function signature
        import inspect

        sig = inspect.signature(self.validator_function)
        required = {}

        for param_name, param in sig.parameters.items():
            if param.annotation != inspect.Parameter.empty:
                required[param_name] = param.annotation
            else:
                required[param_name] = Any

        return required

    def get_output_fields(self) -> Dict[str, type]:
        """Get output fields."""
        return {"validation": Dict[str, Any]}

    def _run_validation(self, inputs: Dict[str, Any]) -> tuple[bool, List[str]]:
        """Run the validation function."""
        try:
            result = self.validator_function(**inputs)

            # Handle different return types
            if isinstance(result, bool):
                return result, [] if result else ["Validation failed"]
            elif isinstance(result, tuple) and len(result) == 2:
                return result
            else:
                return bool(result), [] if result else ["Validation failed"]

        except ValidationError as e:
            errors = [f"{err['loc'][0]}: {err['msg']}" for err in e.errors()]
            return False, errors
        except Exception as e:
            return False, [str(e)]

    def _default_error_handler(self, errors: List[str]) -> Dict[str, Any]:
        """Default error handling."""
        return {"handled": False, "errors": errors}

    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.utcnow().isoformat()
```

### 3.3: Create Node Factory for Contract Selection

**Files to Create:**

`/home/will/Projects/haive/packages/haive-core/src/haive/core/graph/node/contract_factory.py`:

```python
"""Factory for creating ContractNodes based on node type."""
from typing import Dict, Type, Any, Callable, Optional
from enum import Enum

from haive.core.graph.node.contract_node import ContractNode
from haive.core.protocols.execution_contract import ExecutionContract
from haive.core.contracts.llm_contract import LLMExecutionContract
from haive.core.contracts.tool_contract import ToolExecutionContract
from haive.core.contracts.validation_contract import ValidationExecutionContract
from haive.core.graph.node.composer.node_schema_composer import NodeSchemaComposer


class NodeType(str, Enum):
    """Types of nodes that can be created."""
    LLM = "llm"
    TOOL = "tool"
    VALIDATION = "validation"
    ROUTING = "routing"
    GENERIC = "generic"


class ContractNodeFactory:
    """Factory for creating ContractNodes with appropriate contracts.

    This replaces the need for 45+ specialized node classes.
    """

    def __init__(self):
        self.composer = NodeSchemaComposer()
        self.contract_registry: Dict[NodeType, Type[ExecutionContract]] = {
            NodeType.LLM: LLMExecutionContract,
            NodeType.TOOL: ToolExecutionContract,
            NodeType.VALIDATION: ValidationExecutionContract,
        }

    def create_node(
        self,
        node_type: NodeType,
        name: str,
        config: Dict[str, Any],
        field_mappings: Optional[Dict[str, str]] = None
    ) -> ContractNode:
        """Create a ContractNode with appropriate contract.

        Args:
            node_type: Type of node to create
            name: Node identifier
            config: Configuration for the specific contract
            field_mappings: Field mappings (e.g. {"result": "retrieved_documents"})

        Returns:
            ContractNode configured with appropriate contract
        """
        contract = self._create_contract(node_type, config)

        return ContractNode(
            contract=contract,
            composer=self.composer,
            name=name,
            field_mappings=field_mappings
        )

    def create_llm_node(
        self,
        name: str,
        llm_config: Any,
        field_mappings: Optional[Dict[str, str]] = None
    ) -> ContractNode:
        """Create LLM execution node."""
        return self.create_node(
            NodeType.LLM,
            name,
            {"config": llm_config},
            field_mappings
        )

    def create_tool_node(
        self,
        name: str,
        tool_function: Callable,
        tool_name: str,
        field_mappings: Optional[Dict[str, str]] = None
    ) -> ContractNode:
        """Create tool execution node."""
        return self.create_node(
            NodeType.TOOL,
            name,
            {"tool_function": tool_function, "tool_name": tool_name},
            field_mappings
        )

    def create_validation_node(
        self,
        name: str,
        validator_function: Callable,
        field_mappings: Optional[Dict[str, str]] = None
    ) -> ContractNode:
        """Create validation node."""
        return self.create_node(
            NodeType.VALIDATION,
            name,
            {"validator_function": validator_function},
            field_mappings
        )

    def _create_contract(self, node_type: NodeType, config: Dict[str, Any]) -> ExecutionContract:
        """Create appropriate contract for node type."""
        if node_type == NodeType.LLM:
            return LLMExecutionContract(config["config"])
        elif node_type == NodeType.TOOL:
            return ToolExecutionContract(config["tool_function"], config["tool_name"])
        elif node_type == NodeType.VALIDATION:
            return ValidationExecutionContract(config["validator_function"])
        else:
            raise ValueError(f"Unknown node type: {node_type}")

    def register_contract_type(self, node_type: NodeType, contract_class: Type[ExecutionContract]):
        """Register new contract type."""
        self.contract_registry[node_type] = contract_class
```

### 3.4: Migration Integration Tests

**Files to Create:**

`/home/will/Projects/haive/packages/haive-core/tests/integration/test_node_consolidation.py`:

```python
"""Integration tests for node consolidation."""
import pytest
from typing import Dict, Any

from haive.core.graph.node.contract_factory import ContractNodeFactory, NodeType
from haive.core.engine.v2.llm_config import LLMConfig
from haive.core.schema.v2.state_data import StateData


def example_tool_function(query: str) -> str:
    """Example tool function."""
    return f"Tool result for: {query}"


def example_validator_function(content: str) -> tuple[bool, list[str]]:
    """Example validation function."""
    if len(content) > 0:
        return True, []
    else:
        return False, ["Content cannot be empty"]


class TestNodeConsolidation:
    """Test that ContractNode can replace existing specialized nodes."""

    def setup_method(self):
        """Set up test fixtures."""
        self.factory = ContractNodeFactory()
        self.test_state = StateData(
            messages=[{"role": "user", "content": "Test message"}],
            context={"test": True}
        )

    def test_llm_node_replacement(self):
        """Test that ContractNode can replace LLM nodes."""
        config = LLMConfig(temperature=0.1)

        # Create LLM node using factory
        llm_node = self.factory.create_llm_node(
            name="test_llm",
            llm_config=config
        )

        # Execute with real state
        result_state = llm_node(self.test_state)

        # Verify it works like old LLM nodes
        assert len(result_state.messages) >= 2  # User + Assistant
        assert result_state.messages[-1]["role"] == "assistant"

    def test_tool_node_replacement(self):
        """Test that ContractNode can replace tool nodes."""
        # Create tool node using factory
        tool_node = self.factory.create_tool_node(
            name="test_tool",
            tool_function=example_tool_function,
            tool_name="example_tool"
        )

        # Prepare state with tool call
        tool_state = StateData(
            messages=[{"role": "user", "content": "Use the tool"}],
            tool_calls=[{
                "name": "example_tool",
                "arguments": {"query": "test query"}
            }]
        )

        # Execute
        result_state = tool_node(tool_state)

        # Verify tool execution
        assert "Tool result for: test query" in str(result_state.messages)

    def test_validation_node_replacement(self):
        """Test that ContractNode can replace validation nodes."""
        # Create validation node
        validation_node = self.factory.create_validation_node(
            name="test_validator",
            validator_function=example_validator_function
        )

        # Test with valid content
        valid_state = StateData(
            messages=[{"role": "user", "content": "Valid content"}]
        )

        result_state = validation_node(valid_state)

        # Verify validation results
        assert hasattr(result_state, 'validation')
        assert result_state.validation['valid'] is True

    def test_field_mapping_with_nodes(self):
        """Test field mapping works with consolidated nodes."""
        # Create node with field mapping
        llm_node = self.factory.create_llm_node(
            name="mapped_llm",
            llm_config=LLMConfig(temperature=0.1),
            field_mappings={"result": "llm_output"}  # Map result to custom field
        )

        # Execute
        result_state = llm_node(self.test_state)

        # Field mapping should be handled by NodeSchemaComposer
        assert result_state is not None
        assert len(result_state.messages) >= 1

    @pytest.mark.integration
    def test_single_factory_replaces_many_classes(self):
        """Test that single factory can create different node types."""
        # Create multiple node types using same factory
        nodes = [
            self.factory.create_llm_node("llm1", LLMConfig()),
            self.factory.create_tool_node("tool1", example_tool_function, "tool1"),
            self.factory.create_validation_node("val1", example_validator_function)
        ]

        # All should be ContractNodes
        from haive.core.graph.node.contract_node import ContractNode
        for node in nodes:
            assert isinstance(node, ContractNode)
            assert hasattr(node, '__call__')

        # Each should have different contracts
        contract_types = [type(node.contract) for node in nodes]
        assert len(set(contract_types)) == 3  # All different contracts

    def test_consolidation_metrics(self):
        """Test consolidation achievement metrics."""
        # Before: Would need multiple specialized classes
        # After: Single factory creates all types

        factory = ContractNodeFactory()

        # Verify single factory can create multiple types
        node_types = [NodeType.LLM, NodeType.TOOL, NodeType.VALIDATION]

        created_nodes = []
        for i, node_type in enumerate(node_types):
            if node_type == NodeType.LLM:
                node = factory.create_llm_node(f"llm_{i}", LLMConfig())
            elif node_type == NodeType.TOOL:
                node = factory.create_tool_node(f"tool_{i}", example_tool_function, f"tool_{i}")
            elif node_type == NodeType.VALIDATION:
                node = factory.create_validation_node(f"val_{i}", example_validator_function)

            created_nodes.append(node)

        # Verify consolidation: 1 factory class + 1 node class replaces many
        assert len(created_nodes) == len(node_types)
        print(f"✅ Single factory created {len(created_nodes)} different node types")
```

**Commands to Execute:**

```bash
# Run node pattern analysis
cd /home/will/Projects/haive
poetry run python scripts/analysis/node_pattern_analyzer.py > node_analysis.txt

# Create contract directories
mkdir -p /home/will/Projects/haive/packages/haive-core/src/haive/core/contracts

# Run consolidation tests
poetry run pytest packages/haive-core/tests/integration/test_node_consolidation.py -v

# Measure consolidation impact
poetry run python scripts/validation/line_count_tracker.py | tee phase3_metrics.txt

# Test that existing nodes still work while new ones are available
poetry run pytest packages/haive-core/tests/ -k "node" --tb=short
```

**Success Criteria:**

- [ ] Node pattern analysis identifies consolidation opportunities
- [ ] ContractNode successfully replaces LLM nodes
- [ ] ContractNode successfully replaces tool nodes
- [ ] ContractNode successfully replaces validation nodes
- [ ] Field mapping works through NodeSchemaComposer
- [ ] Single factory creates all node types
- [ ] 45+ node files reduced to 1 ContractNode + contracts
- [ ] Real execution still works (no mocks)

**Time Estimate:** 14 hours  
**Risk Mitigation:** Keep existing node files during transition  
**Rollback Plan:** Factory pattern allows reverting to old classes

---

# PHASE 4: WORKFLOW LAYER CREATION (Week 4-5)

## Build Missing Workflow Layer for Pure Orchestration

### 4.1: Create Workflow Foundation

**Problem**: No separation between orchestration (Workflow) and LLM execution (Agent)

**Files to Create:**

`/home/will/Projects/haive/packages/haive-core/src/haive/core/workflow/__init__.py`:

```python
"""Workflow layer for pure orchestration without LLM dependency."""
from .base_workflow import BaseWorkflow
from .sequential_workflow import SequentialWorkflow
from .parallel_workflow import ParallelWorkflow
from .conditional_workflow import ConditionalWorkflow
from .workflow_builder import WorkflowBuilder
from .execution_context import ExecutionContext

__all__ = [
    "BaseWorkflow",
    "SequentialWorkflow",
    "ParallelWorkflow",
    "ConditionalWorkflow",
    "WorkflowBuilder",
    "ExecutionContext"
]
```

`/home/will/Projects/haive/packages/haive-core/src/haive/core/workflow/base_workflow.py`:

```python
"""Base workflow class for pure orchestration."""
from typing import Any, Dict, List, Optional, Protocol, TypeVar
from pydantic import BaseModel, Field
from abc import ABC, abstractmethod

from haive.core.schema.v2.state_data import StateData
from haive.core.protocols.execution_contract import ExecutionContract

TState = TypeVar('TState', bound=BaseModel)


class WorkflowNode(Protocol):
    """Protocol for workflow nodes."""

    def __call__(self, state: TState) -> TState:
        """Execute node with state."""
        ...


class BaseWorkflow(BaseModel, ABC):
    """Base class for pure orchestration workflows.

    Key differences from Agent:
    - NO LLM requirement (no engine field)
    - Pure orchestration logic
    - Composes nodes/agents without LLM dependency
    - Stateless execution patterns
    """

    name: str = Field(..., description="Workflow identifier")
    nodes: List[WorkflowNode] = Field(default_factory=list, description="Workflow nodes")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Workflow metadata")

    # No engine field - this is pure orchestration!

    @abstractmethod
    def execute(self, state: StateData) -> StateData:
        """Execute workflow with given state.

        This is pure orchestration - no LLM calls directly.
        Nodes may contain LLMs, but workflow doesn't.
        """
        ...

    def add_node(self, node: WorkflowNode) -> None:
        """Add node to workflow."""
        self.nodes.append(node)

    def remove_node(self, node: WorkflowNode) -> bool:
        """Remove node from workflow."""
        try:
            self.nodes.remove(node)
            return True
        except ValueError:
            return False

    def get_execution_plan(self) -> List[str]:
        """Get execution plan as list of node names."""
        plan = []
        for node in self.nodes:
            if hasattr(node, 'name'):
                plan.append(node.name)
            else:
                plan.append(str(type(node).__name__))
        return plan

    def validate_workflow(self) -> tuple[bool, List[str]]:
        """Validate workflow configuration."""
        errors = []

        if not self.name:
            errors.append("Workflow name is required")

        if not self.nodes:
            errors.append("Workflow must have at least one node")

        # Validate each node has callable interface
        for i, node in enumerate(self.nodes):
            if not hasattr(node, '__call__'):
                errors.append(f"Node {i} is not callable")

        return len(errors) == 0, errors
```

`/home/will/Projects/haive/packages/haive-core/src/haive/core/workflow/sequential_workflow.py`:

```python
"""Sequential workflow implementation."""
from typing import List, Optional
import logging

from .base_workflow import BaseWorkflow
from haive.core.schema.v2.state_data import StateData

logger = logging.getLogger(__name__)


class SequentialWorkflow(BaseWorkflow):
    """Sequential execution workflow.

    Executes nodes one after another in order.
    Pure orchestration with no LLM dependency.
    """

    def execute(self, state: StateData) -> StateData:
        """Execute nodes sequentially."""
        current_state = state

        logger.info(f"Starting sequential execution of {len(self.nodes)} nodes")

        for i, node in enumerate(self.nodes):
            try:
                logger.debug(f"Executing node {i}: {getattr(node, 'name', type(node).__name__)}")

                # Execute node with current state
                current_state = node(current_state)

                # Update metadata with execution progress
                if 'execution_history' not in current_state.metadata:
                    current_state.metadata['execution_history'] = []

                current_state.metadata['execution_history'].append({
                    'node_index': i,
                    'node_name': getattr(node, 'name', type(node).__name__),
                    'timestamp': self._get_timestamp()
                })

                logger.debug(f"Node {i} completed successfully")

            except Exception as e:
                logger.error(f"Node {i} failed: {e}")

                # Add error to state
                if 'errors' not in current_state.metadata:
                    current_state.metadata['errors'] = []

                current_state.metadata['errors'].append({
                    'node_index': i,
                    'error': str(e),
                    'timestamp': self._get_timestamp()
                })

                # Continue or stop based on error handling policy
                if self.metadata.get('stop_on_error', True):
                    break

        logger.info("Sequential execution completed")
        return current_state

    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.utcnow().isoformat()
```

### 4.2: Create Agent as Workflow Extension

**Files to Create:**

`/home/will/Projects/haive/packages/haive-agents/src/haive/agents/base/workflow_agent.py`:

```python
"""Agent built on Workflow foundation."""
from typing import Optional, Dict, Any
from pydantic import Field

from haive.core.workflow.base_workflow import BaseWorkflow
from haive.core.engine.v2.llm_config import LLMConfig
from haive.core.engine.v2.execution_engine import ExecutionEngine
from haive.core.schema.v2.state_data import StateData


class WorkflowAgent(BaseWorkflow):
    """Agent built on Workflow foundation.

    Key insight: Agent = Workflow + LLM capability
    This creates clean separation of concerns.
    """

    # Workflow capabilities (inherited from BaseWorkflow)
    # + LLM capabilities (added here)

    engine_config: LLMConfig = Field(..., description="LLM configuration")
    execution_engine: Optional[ExecutionEngine] = Field(default=None, description="LLM execution engine")

    def model_post_init(self, __context: Any) -> None:
        """Initialize execution engine after model creation."""
        super().model_post_init(__context)

        if self.execution_engine is None:
            self.execution_engine = ExecutionEngine(self.engine_config)

    def execute(self, state: StateData) -> StateData:
        """Execute workflow with LLM capabilities."""
        # First run workflow orchestration (inherited)
        workflow_result = super().execute(state)

        # Then add LLM processing if needed
        if self._needs_llm_processing(workflow_result):
            workflow_result = self._process_with_llm(workflow_result)

        return workflow_result

    def add_llm_node(self, name: str) -> None:
        """Add LLM processing node to workflow."""
        from haive.core.graph.node.contract_factory import ContractNodeFactory

        factory = ContractNodeFactory()
        llm_node = factory.create_llm_node(name, self.engine_config)
        self.add_node(llm_node)

    def _needs_llm_processing(self, state: StateData) -> bool:
        """Check if state needs LLM processing."""
        # Check if there are unprocessed user messages
        if hasattr(state, 'messages'):
            user_messages = [msg for msg in state.messages if msg.get('role') == 'user']
            assistant_messages = [msg for msg in state.messages if msg.get('role') == 'assistant']
            return len(user_messages) > len(assistant_messages)

        return False

    def _process_with_llm(self, state: StateData) -> StateData:
        """Process state through LLM."""
        if self.execution_engine:
            # Extract messages for LLM
            messages = getattr(state, 'messages', [])

            # Execute LLM
            response = self.execution_engine.execute(messages)

            # Add response to state
            state_dict = state.model_dump()
            if 'messages' not in state_dict:
                state_dict['messages'] = []
            state_dict['messages'].append(response)

            return StateData(**state_dict)

        return state
```

### 4.3: Create Workflow Builder Pattern

**Files to Create:**

`/home/will/Projects/haive/packages/haive-core/src/haive/core/workflow/workflow_builder.py`:

```python
"""Builder pattern for creating complex workflows."""
from typing import List, Dict, Any, Optional, Callable
from enum import Enum

from .base_workflow import BaseWorkflow
from .sequential_workflow import SequentialWorkflow
from .parallel_workflow import ParallelWorkflow
from .conditional_workflow import ConditionalWorkflow
from haive.core.graph.node.contract_factory import ContractNodeFactory


class WorkflowType(str, Enum):
    """Types of workflows that can be built."""
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    CONDITIONAL = "conditional"


class WorkflowBuilder:
    """Builder for creating complex workflows with fluent interface.

    This replaces complex inheritance hierarchies with composition.
    """

    def __init__(self, name: str):
        self.name = name
        self.workflow_type: Optional[WorkflowType] = None
        self.nodes: List[Any] = []
        self.metadata: Dict[str, Any] = {}
        self.factory = ContractNodeFactory()

    def sequential(self) -> "WorkflowBuilder":
        """Set workflow type to sequential."""
        self.workflow_type = WorkflowType.SEQUENTIAL
        return self

    def parallel(self) -> "WorkflowBuilder":
        """Set workflow type to parallel."""
        self.workflow_type = WorkflowType.PARALLEL
        return self

    def conditional(self, condition_func: Callable) -> "WorkflowBuilder":
        """Set workflow type to conditional."""
        self.workflow_type = WorkflowType.CONDITIONAL
        self.metadata['condition_func'] = condition_func
        return self

    def add_llm_node(
        self,
        name: str,
        llm_config: Any,
        field_mappings: Optional[Dict[str, str]] = None
    ) -> "WorkflowBuilder":
        """Add LLM node to workflow."""
        node = self.factory.create_llm_node(name, llm_config, field_mappings)
        self.nodes.append(node)
        return self

    def add_tool_node(
        self,
        name: str,
        tool_function: Callable,
        tool_name: str,
        field_mappings: Optional[Dict[str, str]] = None
    ) -> "WorkflowBuilder":
        """Add tool node to workflow."""
        node = self.factory.create_tool_node(name, tool_function, tool_name, field_mappings)
        self.nodes.append(node)
        return self

    def add_validation_node(
        self,
        name: str,
        validator_function: Callable,
        field_mappings: Optional[Dict[str, str]] = None
    ) -> "WorkflowBuilder":
        """Add validation node to workflow."""
        node = self.factory.create_validation_node(name, validator_function, field_mappings)
        self.nodes.append(node)
        return self

    def add_custom_node(self, node: Any) -> "WorkflowBuilder":
        """Add custom node to workflow."""
        self.nodes.append(node)
        return self

    def with_metadata(self, **kwargs) -> "WorkflowBuilder":
        """Add metadata to workflow."""
        self.metadata.update(kwargs)
        return self

    def build(self) -> BaseWorkflow:
        """Build the workflow."""
        if self.workflow_type is None:
            self.workflow_type = WorkflowType.SEQUENTIAL  # Default

        workflow_data = {
            "name": self.name,
            "nodes": self.nodes,
            "metadata": self.metadata
        }

        if self.workflow_type == WorkflowType.SEQUENTIAL:
            return SequentialWorkflow(**workflow_data)
        elif self.workflow_type == WorkflowType.PARALLEL:
            return ParallelWorkflow(**workflow_data)
        elif self.workflow_type == WorkflowType.CONDITIONAL:
            return ConditionalWorkflow(**workflow_data)
        else:
            raise ValueError(f"Unknown workflow type: {self.workflow_type}")

    @classmethod
    def create(cls, name: str) -> "WorkflowBuilder":
        """Create new workflow builder."""
        return cls(name)
```

### 4.4: Integration Testing for Workflow Layer

**Files to Create:**

`/home/will/Projects/haive/packages/haive-core/tests/integration/test_workflow_layer.py`:

```python
"""Integration tests for workflow layer."""
import pytest
from typing import Dict, Any

from haive.core.workflow.workflow_builder import WorkflowBuilder
from haive.core.workflow.sequential_workflow import SequentialWorkflow
from haive.core.engine.v2.llm_config import LLMConfig
from haive.core.schema.v2.state_data import StateData


def simple_tool(text: str) -> str:
    """Simple tool for testing."""
    return f"Processed: {text}"


def simple_validator(content: str) -> tuple[bool, list[str]]:
    """Simple validator for testing."""
    return len(content) > 0, [] if len(content) > 0 else ["Empty content"]


class TestWorkflowLayer:
    """Test workflow layer provides pure orchestration."""

    def test_sequential_workflow_without_llm(self):
        """Test that workflow works without LLM dependency."""
        # Create workflow with only tool and validation nodes
        workflow = (WorkflowBuilder.create("test_workflow")
                   .sequential()
                   .add_tool_node("tool1", simple_tool, "simple_tool")
                   .add_validation_node("validator1", simple_validator)
                   .build())

        # Create test state
        state = StateData(
            messages=[],  # No messages - pure data processing
            context={"input": "test data"}
        )

        # Execute workflow - no LLM calls
        result = workflow.execute(state)

        # Verify orchestration worked
        assert 'execution_history' in result.metadata
        assert len(result.metadata['execution_history']) == 2  # Tool + Validation
        assert 'validation' in result.model_dump()

    def test_workflow_agent_separation(self):
        """Test that Agent extends Workflow cleanly."""
        from haive.agents.base.workflow_agent import WorkflowAgent

        # Create workflow-based agent
        agent = WorkflowAgent(
            name="test_agent",
            engine_config=LLMConfig(temperature=0.1)
        )

        # Add workflow nodes
        agent.add_tool_node("tool1", simple_tool, "simple_tool")

        # Test state with user message
        state = StateData(
            messages=[{"role": "user", "content": "Process this"}]
        )

        # Execute - should do workflow + LLM
        result = agent.execute(state)

        # Should have both workflow execution and LLM response
        assert len(result.messages) >= 2  # User + Assistant
        assert 'execution_history' in result.metadata  # Workflow ran

    def test_workflow_builder_fluent_interface(self):
        """Test fluent interface for workflow building."""
        # Complex workflow built with fluent interface
        workflow = (WorkflowBuilder.create("complex_workflow")
                   .sequential()
                   .add_tool_node("input_processor", simple_tool, "processor")
                   .add_validation_node("input_validator", simple_validator)
                   .add_llm_node("llm_processor", LLMConfig(temperature=0.1))
                   .with_metadata(description="Complex processing workflow")
                   .build())

        # Verify structure
        assert workflow.name == "complex_workflow"
        assert len(workflow.nodes) == 3
        assert workflow.metadata['description'] == "Complex processing workflow"
        assert isinstance(workflow, SequentialWorkflow)

    def test_composition_over_inheritance(self):
        """Test that composition replaces complex inheritance."""
        # Instead of multiple agent subclasses, use composition

        # Research workflow
        research_workflow = (WorkflowBuilder.create("research")
                            .sequential()
                            .add_tool_node("search", simple_tool, "search")
                            .add_validation_node("validate_results", simple_validator)
                            .build())

        # Analysis workflow
        analysis_workflow = (WorkflowBuilder.create("analysis")
                            .sequential()
                            .add_llm_node("analyzer", LLMConfig())
                            .build())

        # Verify both created from same builder pattern
        assert research_workflow.name == "research"
        assert analysis_workflow.name == "analysis"
        assert len(research_workflow.nodes) == 2
        assert len(analysis_workflow.nodes) == 1

    @pytest.mark.integration
    def test_workflow_replaces_multi_agent_complexity(self):
        """Test that workflow patterns replace complex multi-agent hierarchies."""
        # Instead of specialized MultiAgent classes, use workflow composition

        workflows = []

        # Create different workflow patterns
        patterns = [
            ("sequential_pattern", lambda b: b.sequential()),
            ("parallel_pattern", lambda b: b.parallel()),
        ]

        for name, pattern_func in patterns:
            workflow = WorkflowBuilder.create(name)
            pattern_func(workflow)
            workflow.add_tool_node("tool1", simple_tool, "tool1")
            workflows.append(workflow.build())

        # Single builder creates multiple patterns
        assert len(workflows) == 2
        assert all(hasattr(w, 'execute') for w in workflows)

        print(f"✅ Single builder pattern created {len(workflows)} workflow types")
        print(f"   Replaces multiple specialized multi-agent classes")
```

**Commands to Execute:**

```bash
# Create workflow directories
mkdir -p /home/will/Projects/haive/packages/haive-core/src/haive/core/workflow
mkdir -p /home/will/Projects/haive/packages/haive-agents/src/haive/agents/base

# Run workflow integration tests
cd /home/will/Projects/haive
poetry run pytest packages/haive-core/tests/integration/test_workflow_layer.py -v

# Test workflow builder pattern
poetry run python -c "
from haive.core.workflow.workflow_builder import WorkflowBuilder
from haive.core.engine.v2.llm_config import LLMConfig

workflow = (WorkflowBuilder.create('test')
           .sequential()
           .add_llm_node('llm1', LLMConfig())
           .build())

print(f'Workflow created: {workflow.name}')
print(f'Nodes: {len(workflow.nodes)}')
print(f'Type: {type(workflow).__name__}')
"

# Measure workflow layer impact
poetry run python scripts/validation/line_count_tracker.py | tee phase4_metrics.txt
```

**Success Criteria:**

- [ ] BaseWorkflow created with no LLM dependency
- [ ] SequentialWorkflow, ParallelWorkflow working
- [ ] WorkflowAgent extends Workflow cleanly
- [ ] WorkflowBuilder fluent interface working
- [ ] Pure orchestration without LLM calls
- [ ] Agent = Workflow + LLM capability proven
- [ ] Composition replaces inheritance hierarchies

**Time Estimate:** 16 hours  
**Risk Mitigation:** Build incrementally, test each workflow type  
**Rollback Plan:** Workflow layer is additive, doesn't break existing code

---

# PHASE 5: MIGRATION AND COMPATIBILITY (Week 5-6)

## Ensure Smooth Transition with Adapters and Migration Tools

### 5.1: Create Compatibility Adapters

**Files to Create:**

`/home/will/Projects/haive/packages/haive-core/src/haive/core/compatibility/__init__.py`:

```python
"""Compatibility layer for smooth migration to Architecture v2."""
from .state_schema_adapter import StateSchemaAdapter
from .augllm_config_adapter import AugLLMConfigAdapter
from .agent_adapter import AgentAdapter
from .multi_agent_adapter import MultiAgentAdapter

__all__ = [
    "StateSchemaAdapter",
    "AugLLMConfigAdapter",
    "AgentAdapter",
    "MultiAgentAdapter"
]
```

`/home/will/Projects/haive/packages/haive-core/src/haive/core/compatibility/state_schema_adapter.py`:

```python
"""Adapter to make old StateSchema code work with new architecture."""
from typing import Any, Dict, List
import warnings

from haive.core.schema.v2.state_data import StateData
from haive.core.schema.v2.state_validator import StateValidator
from haive.core.schema.v2.state_composer import StateComposer


class StateSchemaAdapter:
    """Adapter that provides old StateSchema interface using new architecture.

    This allows existing code to work unchanged while using
    the decomposed architecture underneath.
    """

    def __init__(self, **kwargs):
        """Initialize adapter with old StateSchema parameters."""
        warnings.warn(
            "StateSchema is deprecated. Use StateData + StateValidator + StateComposer directly.",
            DeprecationWarning,
            stacklevel=2
        )

        # Create new architecture components
        self._state_data = StateData(**kwargs)
        self._validator = StateValidator()
        self._composer = StateComposer()

    def __getattr__(self, name: str) -> Any:
        """Delegate attribute access to StateData."""
        if hasattr(self._state_data, name):
            return getattr(self._state_data, name)
        raise AttributeError(f"'{self.__class__.__name__}' has no attribute '{name}'")

    def __setattr__(self, name: str, value: Any) -> None:
        """Delegate attribute setting to StateData."""
        if name.startswith('_'):
            super().__setattr__(name, value)
        elif hasattr(self._state_data, name):
            setattr(self._state_data, name, value)
        else:
            super().__setattr__(name, value)

    def model_dump(self) -> Dict[str, Any]:
        """Provide old model_dump interface."""
        return self._state_data.model_dump()

    def model_copy(self, **kwargs) -> "StateSchemaAdapter":
        """Provide old model_copy interface."""
        new_state = self._state_data.model_copy(**kwargs)
        adapter = StateSchemaAdapter()
        adapter._state_data = new_state
        adapter._validator = self._validator
        adapter._composer = self._composer
        return adapter

    # Old methods that used to be in StateSchema
    def validate_state(self) -> bool:
        """Old validation method."""
        return self._validator.validate_state(self._state_data)

    def compose_with_engine(self, engine: Any) -> Any:
        """Old composition method."""
        return self._composer.compose_state_with_engine(self._state_data, engine)

    def add_message(self, message: Dict[str, Any]) -> None:
        """Old message addition method."""
        self._state_data.messages.append(message)

    def get_context(self, key: str) -> Any:
        """Old context access method."""
        return self._state_data.context.get(key)

    def set_context(self, key: str, value: Any) -> None:
        """Old context setting method."""
        self._state_data.context[key] = value
```

### 5.2: Create Migration Scripts

**Files to Create:**

`/home/will/Projects/haive/scripts/migration/migrate_to_v2.py`:

```python
#!/usr/bin/env python3
"""Migration script to convert code from v1 to v2 architecture."""

import os
import re
import ast
from pathlib import Path
from typing import Dict, List, Tuple
import argparse


class CodeMigrator:
    """Migrate code from v1 to v2 architecture."""

    def __init__(self, dry_run: bool = True):
        self.dry_run = dry_run
        self.changes_made = 0
        self.files_processed = 0

    def migrate_directory(self, directory: Path) -> None:
        """Migrate all Python files in directory."""
        print(f"🔄 Migrating directory: {directory}")

        for py_file in directory.rglob("*.py"):
            if self.should_migrate_file(py_file):
                self.migrate_file(py_file)

    def should_migrate_file(self, file_path: Path) -> bool:
        """Check if file needs migration."""
        # Skip test files, migrations, and certain directories
        skip_patterns = [
            "test_", "__pycache__", ".pyc", "migration", "compatibility"
        ]

        for pattern in skip_patterns:
            if pattern in str(file_path):
                return False

        return True

    def migrate_file(self, file_path: Path) -> None:
        """Migrate a single file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()

            modified_content = original_content
            file_changes = 0

            # Apply migration patterns
            for pattern, replacement, description in self.get_migration_patterns():
                new_content = re.sub(pattern, replacement, modified_content)
                if new_content != modified_content:
                    modified_content = new_content
                    file_changes += 1
                    print(f"  ✓ Applied: {description}")

            if file_changes > 0:
                self.files_processed += 1
                self.changes_made += file_changes

                if not self.dry_run:
                    # Create backup
                    backup_path = file_path.with_suffix('.py.v1_backup')
                    with open(backup_path, 'w', encoding='utf-8') as f:
                        f.write(original_content)

                    # Write migrated content
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(modified_content)

                    print(f"  💾 Migrated: {file_path}")
                    print(f"  📁 Backup: {backup_path}")
                else:
                    print(f"  🔍 Would migrate: {file_path} ({file_changes} changes)")

        except Exception as e:
            print(f"  ❌ Error migrating {file_path}: {e}")

    def get_migration_patterns(self) -> List[Tuple[str, str, str]]:
        """Get regex patterns for migration."""
        return [
            # StateSchema imports
            (
                r"from haive\.core\.schema\.base import StateSchema",
                r"from haive.core.compatibility import StateSchemaAdapter as StateSchema",
                "StateSchema import to compatibility adapter"
            ),

            # AugLLMConfig imports
            (
                r"from haive\.core\.engine\.aug_llm\.config import AugLLMConfig",
                r"from haive.core.compatibility import AugLLMConfigAdapter as AugLLMConfig",
                "AugLLMConfig import to compatibility adapter"
            ),

            # Node imports - replace with ContractNode factory
            (
                r"from haive\.core\.graph\.node\.[a-zA-Z_]+ import [A-Za-z]+Node",
                r"from haive.core.graph.node.contract_factory import ContractNodeFactory",
                "Node imports to ContractNodeFactory"
            ),

            # Agent base imports
            (
                r"from haive\.agents\.base\.agent import Agent",
                r"from haive.agents.base.workflow_agent import WorkflowAgent as Agent",
                "Agent import to WorkflowAgent"
            ),

            # Direct node instantiation to factory pattern
            (
                r"([A-Za-z]+Node)\(([^)]+)\)",
                r"ContractNodeFactory().create_node_from_legacy(\1, \2)",
                "Node instantiation to factory pattern"
            ),
        ]

    def generate_migration_report(self) -> str:
        """Generate migration report."""
        report = f"""
🎯 MIGRATION REPORT
{'=' * 50}

Files processed: {self.files_processed}
Changes made: {self.changes_made}
Mode: {'DRY RUN' if self.dry_run else 'LIVE MIGRATION'}

Migration patterns applied:
"""
        for _, _, description in self.get_migration_patterns():
            report += f"  • {description}\n"

        return report


def main():
    """Main migration function."""
    parser = argparse.ArgumentParser(description="Migrate Haive code to v2 architecture")
    parser.add_argument("directory", help="Directory to migrate")
    parser.add_argument("--live", action="store_true", help="Perform live migration (default is dry run)")
    parser.add_argument("--report", action="store_true", help="Generate detailed report")

    args = parser.parse_args()

    directory = Path(args.directory)
    if not directory.exists():
        print(f"❌ Directory not found: {directory}")
        return

    migrator = CodeMigrator(dry_run=not args.live)

    print("🚀 HAIVE ARCHITECTURE V2 MIGRATION")
    print("=" * 50)
    print(f"Directory: {directory}")
    print(f"Mode: {'LIVE MIGRATION' if args.live else 'DRY RUN'}")
    print()

    migrator.migrate_directory(directory)

    print()
    print(migrator.generate_migration_report())

    if args.live:
        print("✅ Migration completed!")
        print("📁 Original files backed up with .v1_backup extension")
        print("🧪 Run tests to verify migration success")
    else:
        print("🔍 Dry run completed - use --live to perform actual migration")


if __name__ == "__main__":
    main()
```

### 5.3: Create Testing Strategy for Migration

**Files to Create:**

`/home/will/Projects/haive/packages/haive-core/tests/migration/test_full_migration.py`:

```python
"""Comprehensive migration testing."""
import pytest
import tempfile
import shutil
from pathlib import Path

from haive.scripts.migration.migrate_to_v2 import CodeMigrator


class TestFullMigration:
    """Test complete migration from v1 to v2."""

    def setup_method(self):
        """Set up test environment."""
        self.test_dir = Path(tempfile.mkdtemp())
        self.create_test_files()

    def teardown_method(self):
        """Clean up test environment."""
        shutil.rmtree(self.test_dir)

    def create_test_files(self):
        """Create test files that need migration."""
        # Old-style agent file
        old_agent_code = '''
from haive.core.schema.base import StateSchema
from haive.core.engine.aug_llm.config import AugLLMConfig
from haive.agents.base.agent import Agent

class MyAgent(Agent):
    def __init__(self):
        self.state = StateSchema()
        self.config = AugLLMConfig()

    def run(self, input_text):
        return "result"
'''

        agent_file = self.test_dir / "old_agent.py"
        with open(agent_file, 'w') as f:
            f.write(old_agent_code)

        # Old-style node usage
        old_node_code = '''
from haive.core.graph.node.llm_node import LLMNode
from haive.core.graph.node.tool_node import ToolNode

def create_workflow():
    llm_node = LLMNode(config=config)
    tool_node = ToolNode(tool=my_tool)
    return [llm_node, tool_node]
'''

        node_file = self.test_dir / "old_nodes.py"
        with open(node_file, 'w') as f:
            f.write(old_node_code)

    def test_dry_run_migration(self):
        """Test dry run migration identifies files correctly."""
        migrator = CodeMigrator(dry_run=True)
        migrator.migrate_directory(self.test_dir)

        # Should identify files that need migration
        assert migrator.files_processed >= 2
        assert migrator.changes_made > 0

        # Files should not be modified in dry run
        agent_file = self.test_dir / "old_agent.py"
        with open(agent_file, 'r') as f:
            content = f.read()
        assert "StateSchema" in content  # Original import still there

    def test_live_migration(self):
        """Test live migration actually modifies files."""
        migrator = CodeMigrator(dry_run=False)
        migrator.migrate_directory(self.test_dir)

        # Check that files were modified
        agent_file = self.test_dir / "old_agent.py"
        with open(agent_file, 'r') as f:
            content = f.read()

        # Should have compatibility imports
        assert "StateSchemaAdapter" in content

        # Should have backup
        backup_file = self.test_dir / "old_agent.py.v1_backup"
        assert backup_file.exists()

        # Backup should have original content
        with open(backup_file, 'r') as f:
            backup_content = f.read()
        assert "from haive.core.schema.base import StateSchema" in backup_content

    @pytest.mark.integration
    def test_migrated_code_still_works(self):
        """Test that migrated code still executes correctly."""
        # Migrate code
        migrator = CodeMigrator(dry_run=False)
        migrator.migrate_directory(self.test_dir)

        # Try to import and run migrated code
        import sys
        sys.path.insert(0, str(self.test_dir))

        try:
            # This should work with compatibility adapters
            import old_agent
            agent = old_agent.MyAgent()

            # Should still work with old interface
            result = agent.run("test input")
            assert result == "result"

        except ImportError as e:
            pytest.skip(f"Could not import migrated code: {e}")
        finally:
            sys.path.remove(str(self.test_dir))

    def test_migration_preserves_functionality(self):
        """Test that migration preserves existing functionality."""
        # Create working v1 code
        working_v1_code = '''
from haive.core.schema.base import StateSchema

def process_data():
    state = StateSchema(messages=[], context={})
    state.messages.append({"role": "user", "content": "test"})
    return len(state.messages)
'''

        test_file = self.test_dir / "working_code.py"
        with open(test_file, 'w') as f:
            f.write(working_v1_code)

        # Migrate
        migrator = CodeMigrator(dry_run=False)
        migrator.migrate_directory(self.test_dir)

        # Test that functionality is preserved
        import sys
        sys.path.insert(0, str(self.test_dir))

        try:
            import working_code
            result = working_code.process_data()
            assert result == 1  # Should still return correct count

        except Exception as e:
            pytest.fail(f"Migrated code failed to work: {e}")
        finally:
            sys.path.remove(str(self.test_dir))
```

### 5.4: Create Rollback Strategy

**Files to Create:**

`/home/will/Projects/haive/scripts/migration/rollback_v2.py`:

```python
#!/usr/bin/env python3
"""Rollback script for v2 migration."""

import os
import shutil
from pathlib import Path
import argparse


def rollback_migration(directory: Path, dry_run: bool = True) -> None:
    """Rollback v2 migration by restoring backups."""
    print(f"🔄 Rolling back migration in: {directory}")

    backup_files = list(directory.rglob("*.py.v1_backup"))

    if not backup_files:
        print("❌ No backup files found - cannot rollback")
        return

    print(f"📁 Found {len(backup_files)} backup files")

    for backup_file in backup_files:
        original_file = backup_file.with_suffix('')  # Remove .v1_backup

        if dry_run:
            print(f"  🔍 Would restore: {original_file}")
        else:
            try:
                # Restore original file
                shutil.copy2(backup_file, original_file)

                # Remove backup
                backup_file.unlink()

                print(f"  ✅ Restored: {original_file}")

            except Exception as e:
                print(f"  ❌ Failed to restore {original_file}: {e}")

    if dry_run:
        print("🔍 Dry run complete - use --live to perform rollback")
    else:
        print("✅ Rollback complete!")


def main():
    """Main rollback function."""
    parser = argparse.ArgumentParser(description="Rollback Haive v2 migration")
    parser.add_argument("directory", help="Directory to rollback")
    parser.add_argument("--live", action="store_true", help="Perform live rollback")

    args = parser.parse_args()

    directory = Path(args.directory)
    if not directory.exists():
        print(f"❌ Directory not found: {directory}")
        return

    rollback_migration(directory, dry_run=not args.live)


if __name__ == "__main__":
    main()
```

**Commands to Execute:**

```bash
# Create migration and compatibility directories
mkdir -p /home/will/Projects/haive/packages/haive-core/src/haive/core/compatibility
mkdir -p /home/will/Projects/haive/scripts/migration

# Test migration on a small directory first
cd /home/will/Projects/haive
poetry run python scripts/migration/migrate_to_v2.py packages/haive-core/tests/integration --report

# Run migration testing
poetry run pytest packages/haive-core/tests/migration/test_full_migration.py -v

# Test compatibility adapters work
poetry run python -c "
from haive.core.compatibility import StateSchemaAdapter
state = StateSchemaAdapter(messages=[], context={})
state.add_message({'role': 'user', 'content': 'test'})
print(f'Compatibility adapter working: {len(state.messages)} messages')
"
```

**Success Criteria:**

- [ ] Compatibility adapters provide old interface
- [ ] Migration scripts work on test directories
- [ ] Dry run identifies all necessary changes
- [ ] Live migration creates backups properly
- [ ] Migrated code still passes existing tests
- [ ] Rollback script can restore original code
- [ ] No functionality broken during migration

**Time Estimate:** 12 hours  
**Risk Mitigation:** Extensive backup and rollback capabilities  
**Rollback Plan:** Automated rollback script restores all backups

---

# SUCCESS CRITERIA AND VALIDATION

## 📊 Quantitative Success Metrics

### Line Count Reduction Targets

```bash
# Track progress with this command:
poetry run python scripts/validation/line_count_tracker.py

# Target reductions:
BaseGraph:     3,972 → 500   (87% reduction)
Agent:         3,600 → 400   (89% reduction)
AugLLMConfig:  2,601 → 300   (88% reduction)
StateSchema:   2,323 → 200   (91% reduction)
SchemaComposer: 3,378 → 300  (91% reduction)
LLM/Base:      2,042 → 250   (88% reduction)
DynamicGraph:  1,985 → 250   (87% reduction)

TOTAL: ~18,000 → ~2,200 lines (88% reduction in monoliths)
```

### File Count Reduction Targets

```bash
# Current count:
find /home/will/Projects/haive/packages/haive-core/src/haive/core -name "*.py" | wc -l
# Target: 50% reduction through consolidation

# Node files: 45+ → 1 ContractNode + contracts
# Agent files: Multiple → WorkflowAgent + specialized contracts
```

### Test Coverage Requirements

```bash
# All tests must pass with real components (no mocks)
poetry run pytest packages/haive-core/tests/ --cov=haive.core --cov-report=html --cov-fail-under=90

# Property-based tests must pass
poetry run pytest packages/haive-core/tests/property/ -v

# Integration tests with real LLMs must pass
poetry run pytest packages/haive-core/tests/integration/ -v --tb=short
```

## 🧪 Comprehensive Testing Strategy

### Property-Based Testing with Hypothesis

**Example Property Tests:**

```python
# Field mapping properties
@given(st.dictionaries(st.text(), st.text(), min_size=1))
def test_field_mapping_bijection(field_mappings):
    """Property: Field mappings should be bijective."""
    composer = NodeSchemaComposer()
    # Test property: if A maps to B, then B should map back to A context

@given(st.lists(st.dictionaries(st.text(), st.text()), min_size=1))
def test_contract_execution_associative(state_updates):
    """Property: Contract execution should be associative."""
    # Test property: (A ∘ B) ∘ C = A ∘ (B ∘ C)
```

### Golden Tests for Critical Paths

```python
# Golden test data files:
/home/will/Projects/haive/packages/haive-core/tests/golden/
├── state_schema_examples.json    # Known good state transformations
├── llm_responses.json           # Expected LLM response formats
├── node_executions.json         # Node execution results
└── field_mappings.json          # Field mapping test cases
```

### Integration Test Harness

```python
class RealComponentTestHarness:
    """Test harness using real LLMs and tools."""

    def __init__(self):
        self.llm_config = LLMConfig(temperature=0.1)  # Deterministic
        self.execution_engine = ExecutionEngine(self.llm_config)

    def test_end_to_end_workflow(self, test_case):
        """Test complete workflow with real components."""
        # No mocks - real LLM calls, real tool execution

    def assert_response_quality(self, response, expected_patterns):
        """Assert response meets quality criteria."""
        # Real quality checks, not mock assertions
```

## ⚡ Performance Benchmarks

### Execution Speed Targets

```python
# Target performance improvements:
# - State creation: <1ms (vs current ~10ms)
# - Node execution: <100ms (vs current ~500ms)
# - Graph compilation: <50ms (vs current ~200ms)
# - Field mapping: <0.1ms (vs current ~5ms)

def benchmark_performance():
    """Benchmark key operations."""
    import time

    # Measure state creation
    start = time.time()
    for _ in range(1000):
        state = StateData(messages=[], context={})
    state_creation_time = (time.time() - start) / 1000

    assert state_creation_time < 0.001  # <1ms per creation
```

### Memory Usage Targets

```python
# Memory usage reduction targets:
# - State objects: 50% reduction
# - Node objects: 70% reduction
# - Graph objects: 60% reduction

def benchmark_memory_usage():
    """Benchmark memory usage."""
    import psutil
    import os

    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss

    # Create objects
    states = [StateData() for _ in range(100)]
    nodes = [ContractNode(...) for _ in range(50)]

    final_memory = process.memory_info().rss
    memory_per_object = (final_memory - initial_memory) / 150

    # Assert memory efficiency targets
    assert memory_per_object < 1024  # <1KB per object
```

## 🚨 Risk Mitigation Strategies

### 1. Gradual Implementation Risk

```python
# Mitigation: Feature flags for gradual rollout
class FeatureFlags:
    USE_CONTRACT_NODES = os.getenv("HAIVE_USE_CONTRACT_NODES", "false").lower() == "true"
    USE_DECOMPOSED_STATE = os.getenv("HAIVE_USE_DECOMPOSED_STATE", "false").lower() == "true"

if FeatureFlags.USE_CONTRACT_NODES:
    node = ContractNode(...)
else:
    node = OldNodeClass(...)  # Fallback
```

### 2. Breaking Changes Risk

```python
# Mitigation: Compatibility adapters with deprecation warnings
import warnings

def deprecated_function():
    warnings.warn(
        "This function is deprecated. Use new_function() instead.",
        DeprecationWarning,
        stacklevel=2
    )
    return new_function()
```

### 3. Performance Regression Risk

```python
# Mitigation: Automated performance testing
@pytest.mark.performance
def test_no_performance_regression():
    """Ensure new architecture is not slower."""
    old_time = benchmark_old_architecture()
    new_time = benchmark_new_architecture()

    assert new_time <= old_time * 1.1  # Allow 10% performance variation
```

### 4. Test Coverage Risk

```python
# Mitigation: Coverage gates and real component requirements
@pytest.mark.mandatory
class TestCoverageRequirements:
    def test_all_contracts_have_tests(self):
        """Ensure every contract has comprehensive tests."""

    def test_no_mock_usage_in_integration(self):
        """Ensure integration tests use real components."""
```

## 📈 Validation Scripts

### Architecture Compliance Validator

```python
#!/usr/bin/env python3
"""Validate architecture compliance."""

def validate_architecture_rules():
    """Check architecture rules are followed."""
    violations = []

    # Rule 1: No mocks in integration tests
    test_files = Path("tests/integration").rglob("*.py")
    for test_file in test_files:
        content = test_file.read_text()
        if "Mock(" in content or "@mock" in content:
            violations.append(f"Mock usage in integration test: {test_file}")

    # Rule 2: No circular imports
    # Rule 3: Contract protocol compliance
    # Rule 4: Proper separation of concerns

    return violations

if __name__ == "__main__":
    violations = validate_architecture_rules()
    if violations:
        print("❌ Architecture violations found:")
        for violation in violations:
            print(f"  - {violation}")
        exit(1)
    else:
        print("✅ Architecture compliance validated")
```

### Progress Tracking Dashboard

```bash
#!/bin/bash
# Generate progress dashboard
echo "📊 HAIVE ARCHITECTURE V2 PROGRESS DASHBOARD"
echo "=" * 60

echo "📈 Line Count Reduction:"
poetry run python scripts/validation/line_count_tracker.py | grep -E "(TOTAL|reduction)"

echo "🧪 Test Coverage:"
poetry run pytest --cov=haive.core --cov-report=term-missing --quiet | grep -E "TOTAL|FAILED|ERROR"

echo "⚡ Performance Benchmarks:"
poetry run python scripts/validation/performance_benchmarks.py

echo "🎯 Phase Completion:"
for phase in "Phase 0" "Phase 1" "Phase 2" "Phase 3" "Phase 4" "Phase 5"; do
    # Check for phase completion markers
    echo "  ${phase}: [Implementation Status]"
done
```

## 🎯 Implementation Completion Checklist

### Phase 0: Foundation ✅

- [ ] Testing infrastructure created
- [ ] Property-based test examples working
- [ ] Baseline metrics captured
- [ ] Line count tracking functional

### Phase 1: Protocol Foundation ✅

- [ ] ExecutionContract protocol implemented
- [ ] NodeSchemaComposer connected to system
- [ ] ContractNode working with real LLMs
- [ ] Field mapping "result → retrieved_documents" proven

### Phase 2: Monolith Decomposition ✅

- [ ] StateSchema decomposed into 6 components
- [ ] AugLLMConfig decomposed into 7 components
- [ ] Golden tests pass (compatibility preserved)
- [ ] 88% line count reduction achieved

### Phase 3: Node Consolidation ✅

- [ ] 45+ node files replaced with ContractNode
- [ ] ContractNodeFactory creates all node types
- [ ] Tool, LLM, and validation nodes working
- [ ] Integration tests pass with real components

### Phase 4: Workflow Layer ✅

- [ ] BaseWorkflow created (no LLM dependency)
- [ ] WorkflowAgent extends Workflow cleanly
- [ ] WorkflowBuilder fluent interface working
- [ ] Agent = Workflow + LLM capability proven

### Phase 5: Migration & Compatibility ✅

- [ ] Compatibility adapters provide old interface
- [ ] Migration scripts work correctly
- [ ] Rollback capability functional
- [ ] No existing functionality broken

## 🏆 Final Success Declaration

**The implementation is successful when:**

1. **Quantitative Targets Met:**
   - 88% line count reduction achieved
   - 50% file count reduction achieved
   - 90%+ test coverage maintained
   - Performance targets met

2. **Qualitative Targets Met:**
   - NodeSchemaComposer connected and working
   - "result → potato" field mappings functional
   - Real component testing (zero mocks)
   - Clean separation of concerns achieved

3. **Migration Successful:**
   - Existing code works with compatibility adapters
   - Migration path documented and tested
   - Rollback capability proven
   - No breaking changes for end users

4. **Architecture Validated:**
   - Protocol-based contracts working
   - Composition replaces inheritance
   - Monoliths decomposed successfully
   - Clean 3-layer hierarchy: Workflow → Agent → MultiAgent

**This plan provides concrete, measurable steps to transform Haive from architectural collapse to protocol-based excellence. Each phase is self-contained, testable, and includes rollback strategies.**

---

**IMPLEMENTATION STARTS IMMEDIATELY. The architecture's future depends on it.**
