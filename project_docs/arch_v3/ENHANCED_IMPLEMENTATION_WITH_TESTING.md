# ENHANCED IMPLEMENTATION ROADMAP WITH COMPREHENSIVE TESTING

# Complete Testing Process: Hypothesis, Golden Tests, and Fixtures

**Created**: 2025-01-30  
**Version**: 2.0  
**Purpose**: Enhanced implementation with complete testing strategies  
**Status**: Ready for execution with full testing coverage

---

## 🎯 EXECUTIVE SUMMARY

This enhanced roadmap adds comprehensive testing strategies to every phase of the Haive architecture transformation. Each component now has:

- **Property-based testing** with Hypothesis
- **Golden tests** for backward compatibility
- **Pytest fixtures** for component isolation
- **Integration test harnesses**
- **Performance benchmarks**

---

## 📊 TESTING PHILOSOPHY

### Three-Tier Testing Strategy

```
┌─────────────────────────────────────────┐
│         TIER 3: End-to-End Tests        │
│    (Complete workflows, real LLMs)      │
├─────────────────────────────────────────┤
│      TIER 2: Integration Tests          │
│   (Cross-component, real services)      │
├─────────────────────────────────────────┤
│        TIER 1: Unit Tests               │
│  (Hypothesis properties, fixtures)      │
└─────────────────────────────────────────┘
```

---

## 🧪 TESTING PATTERNS BY TYPE

### 1. HYPOTHESIS PROPERTY-BASED TESTING

#### Core Strategy Pattern

```python
# packages/haive-core/tests/property/test_execution_contract.py
from hypothesis import given, strategies as st, assume
from hypothesis.stateful import RuleBasedStateMachine, rule, invariant
import pytest

class ExecutionContractProperties(RuleBasedStateMachine):
    """Property-based testing for ExecutionContract protocol."""

    def __init__(self):
        super().__init__()
        self.contracts = []
        self.states = []

    @rule(
        input_schema=st.sampled_from([SchemaA, SchemaB, SchemaC]),
        output_schema=st.sampled_from([SchemaX, SchemaY, SchemaZ])
    )
    def create_contract(self, input_schema, output_schema):
        """Property: Any valid schema combination should create valid contract."""
        contract = ExecutionContract(
            input_schema=input_schema,
            output_schema=output_schema
        )
        self.contracts.append(contract)
        assert contract.validate()

    @rule(
        data=st.dictionaries(
            st.text(min_size=1),
            st.one_of(st.integers(), st.text(), st.lists(st.integers()))
        )
    )
    def test_extraction(self, data):
        """Property: Extract should handle any valid state structure."""
        if not self.contracts:
            return

        contract = self.contracts[-1]
        state = State(data)

        # Property: extraction should never raise for valid state
        result = contract.extract(state)

        # Property: extracted data matches input schema
        assert isinstance(result, contract.input_schema)

    @invariant()
    def contracts_remain_valid(self):
        """Invariant: All contracts remain valid throughout testing."""
        for contract in self.contracts:
            assert contract.validate()

# Run the state machine tests
TestContractStateMachine = ExecutionContractProperties.TestCase
```

#### Schema Composition Properties

```python
@given(
    schemas=st.lists(
        st.sampled_from([SchemaA, SchemaB, SchemaC]),
        min_size=2,
        max_size=5
    )
)
def test_schema_composition_associative(schemas):
    """Property: Schema composition is associative."""
    if len(schemas) < 3:
        return

    # (A + B) + C should equal A + (B + C)
    left_first = compose(compose(schemas[0], schemas[1]), schemas[2])
    right_first = compose(schemas[0], compose(schemas[1], schemas[2]))

    assert left_first.fields == right_first.fields
```

### 2. GOLDEN TESTS FOR COMPATIBILITY

#### Golden Test Infrastructure

```python
# packages/haive-core/tests/golden/conftest.py
import json
import pickle
from pathlib import Path
import pytest

class GoldenTestManager:
    """Manages golden test files for backward compatibility."""

    def __init__(self, golden_dir="tests/golden/data"):
        self.golden_dir = Path(golden_dir)
        self.golden_dir.mkdir(parents=True, exist_ok=True)

    def save_golden(self, name: str, data: Any, format="json"):
        """Save golden test data."""
        path = self.golden_dir / f"{name}.golden.{format}"

        if format == "json":
            with open(path, "w") as f:
                json.dump(data, f, indent=2, default=str)
        elif format == "pickle":
            with open(path, "wb") as f:
                pickle.dump(data, f)

    def load_golden(self, name: str, format="json"):
        """Load golden test data."""
        path = self.golden_dir / f"{name}.golden.{format}"

        if not path.exists():
            pytest.skip(f"Golden file {path} not found")

        if format == "json":
            with open(path) as f:
                return json.load(f)
        elif format == "pickle":
            with open(path, "rb") as f:
                return pickle.load(f)

    def assert_golden_match(self, name: str, actual: Any, update=False):
        """Assert that actual matches golden data."""
        if update or not (self.golden_dir / f"{name}.golden.json").exists():
            self.save_golden(name, actual)
            return

        expected = self.load_golden(name)
        assert actual == expected, f"Golden test {name} failed"

@pytest.fixture
def golden():
    """Fixture for golden test management."""
    return GoldenTestManager()
```

#### AugLLMConfig Golden Tests

```python
# packages/haive-core/tests/golden/test_aug_llm_config_compatibility.py
def test_aug_llm_config_serialization_compatibility(golden):
    """Ensure AugLLMConfig serialization remains compatible."""

    # Current implementation
    config = AugLLMConfig(
        temperature=0.7,
        max_tokens=1000,
        tools=[calculator_tool, search_tool],
        structured_output_model=ResponseModel
    )

    # Serialize current format
    serialized = config.model_dump()

    # Check against golden data
    golden.assert_golden_match(
        "aug_llm_config_v1",
        serialized,
        update=False  # Set to True to update golden
    )

def test_state_schema_backwards_compatible(golden):
    """Ensure StateSchema can load old formats."""

    # Load old format from golden
    old_data = golden.load_golden("state_schema_v1")

    # Should be able to load with new implementation
    state = StateSchema.model_validate(old_data)

    # Verify critical fields preserved
    assert "messages" in state.fields
    assert state.version == old_data.get("version", 1)
```

### 3. PYTEST FIXTURE HIERARCHIES

#### Base Fixture Architecture

```python
# packages/haive-core/tests/conftest.py
import pytest
from typing import Generator
import asyncio

# Level 1: Infrastructure Fixtures
@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
def test_llm_config():
    """Shared LLM config for all tests."""
    return AugLLMConfig(
        temperature=0.1,  # Low for reproducibility
        max_tokens=100,   # Small for speed
        model="gpt-4o-mini"  # Cheap, fast model
    )

# Level 2: Component Fixtures
@pytest.fixture
def execution_contract():
    """Create a standard execution contract."""
    return ExecutionContract(
        input_schema=MessagesSchema,
        output_schema=ResponseSchema
    )

@pytest.fixture
def node_schema_composer():
    """Create configured NodeSchemaComposer."""
    composer = NodeSchemaComposer()
    composer.register_schema(MessagesSchema)
    composer.register_schema(ResponseSchema)
    return composer

# Level 3: Integration Fixtures
@pytest.fixture
def contract_node(execution_contract, node_schema_composer):
    """Create a complete ContractNode."""
    return ContractNode(
        contract=execution_contract,
        composer=node_schema_composer,
        name="test_node"
    )

@pytest.fixture
async def simple_agent(test_llm_config):
    """Create a configured SimpleAgent."""
    agent = SimpleAgent(
        name="test_agent",
        engine=test_llm_config
    )
    await agent.initialize()
    yield agent
    await agent.cleanup()

# Level 4: Workflow Fixtures
@pytest.fixture
async def multi_agent_system(simple_agent):
    """Create complete multi-agent system."""
    agents = [
        simple_agent,
        ReactAgent(name="reactor", engine=test_llm_config),
        PlannerAgent(name="planner", engine=test_llm_config)
    ]

    system = MultiAgentCoordinator(agents=agents)
    await system.initialize()
    yield system
    await system.cleanup()
```

#### Parametrized Fixture Testing

```python
# Test multiple configurations with fixtures
@pytest.fixture(params=[
    {"temperature": 0.1, "max_tokens": 100},
    {"temperature": 0.7, "max_tokens": 500},
    {"temperature": 1.0, "max_tokens": 1000}
])
def llm_config_variants(request):
    """Test with different LLM configurations."""
    return AugLLMConfig(**request.param)

@pytest.mark.parametrize("agent_type", [
    SimpleAgent,
    ReactAgent,
    PlannerAgent
])
def test_all_agents_with_contracts(agent_type, execution_contract):
    """Test all agent types work with execution contracts."""
    agent = agent_type(
        name="test",
        contract=execution_contract
    )
    assert agent.validate_contract()
```

---

## 🏗️ ENHANCED IMPLEMENTATION PHASES

### PHASE 1: CONTRACT FOUNDATION WITH TESTING

#### Subplan 1.1: Protocol Definition

```python
# Day 1-2: Create core protocols with property tests
# File: packages/haive-core/src/haive/core/protocols/execution.py

from typing import Protocol, TypeVar, Generic
from abc import abstractmethod

T_Input = TypeVar("T_Input")
T_Output = TypeVar("T_Output")

class ExecutionContract(Protocol, Generic[T_Input, T_Output]):
    """Core execution contract with testable properties."""

    @property
    @abstractmethod
    def input_schema(self) -> type[T_Input]:
        """Input schema for validation."""
        ...

    @property
    @abstractmethod
    def output_schema(self) -> type[T_Output]:
        """Output schema for validation."""
        ...

    @abstractmethod
    def extract(self, state: State) -> T_Input:
        """Extract input from state."""
        ...

    @abstractmethod
    def update(self, state: State, output: T_Output) -> State:
        """Update state with output."""
        ...

# Hypothesis test for protocol
@given(
    input_type=st.sampled_from([dict, list, str, int]),
    output_type=st.sampled_from([dict, list, str, int])
)
def test_contract_type_safety(input_type, output_type):
    """Property: Contracts maintain type safety."""
    contract = create_contract(input_type, output_type)

    # Generate random data of correct type
    input_data = generate_data(input_type)

    # Property: extract returns correct type
    extracted = contract.extract(State(input_data))
    assert type(extracted) == input_type
```

#### Subplan 1.2: Integration Testing

```python
# Day 3-4: Integration tests with real components
# File: packages/haive-core/tests/integration/test_contract_integration.py

@pytest.mark.integration
async def test_contract_with_real_llm(test_llm_config, execution_contract):
    """Test contracts with real LLM execution."""

    # Create node with contract
    node = ContractNode(
        contract=execution_contract,
        engine=test_llm_config
    )

    # Real execution
    state = State(messages=[HumanMessage("Test")])
    result = await node.execute(state)

    # Verify contract maintained
    assert execution_contract.validate_output(result)
```

### PHASE 2: ENGINE DECOMPOSITION WITH GOLDEN TESTS

#### Subplan 2.1: Preserve Compatibility

```python
# Day 5-6: Decompose while maintaining compatibility
# File: packages/haive-core/tests/golden/test_engine_compatibility.py

def test_aug_llm_config_decomposition_compatible(golden):
    """Ensure decomposed engine maintains compatibility."""

    # Old monolithic way
    old_config = AugLLMConfig(
        temperature=0.7,
        tools=[tool1, tool2]
    )
    old_result = old_config.invoke("test")

    # New decomposed way
    new_config = LLMConfig(temperature=0.7)
    tool_manager = ToolManager([tool1, tool2])
    executor = LLMExecutor(new_config, tool_manager)
    new_result = executor.invoke("test")

    # Results should be compatible
    golden.assert_golden_match("engine_output", {
        "old": old_result,
        "new": new_result
    })
```

### PHASE 3: NODE CONSOLIDATION WITH FIXTURES

#### Subplan 3.1: Node Testing Hierarchy

```python
# Day 7-8: Consolidate nodes with fixture hierarchy
# File: packages/haive-core/tests/fixtures/node_fixtures.py

@pytest.fixture
def base_node():
    """Base node for testing."""
    return ContractNode(name="base")

@pytest.fixture
def engine_node(base_node, test_llm_config):
    """Engine node extends base."""
    base_node.engine = test_llm_config
    return base_node

@pytest.fixture
def agent_node(engine_node, simple_agent):
    """Agent node wraps agent."""
    return AgentNode(
        agent=simple_agent,
        base_node=engine_node
    )

# Test node hierarchy
def test_node_hierarchy(base_node, engine_node, agent_node):
    """Test nodes maintain proper hierarchy."""
    assert isinstance(agent_node, AgentNode)
    assert isinstance(agent_node.base_node, ContractNode)
    assert agent_node.engine == engine_node.engine
```

---

## 📊 TESTING METRICS & COVERAGE

### Target Coverage by Component

| Component  | Unit Tests | Integration | E2E | Property Tests | Golden Tests |
| ---------- | ---------- | ----------- | --- | -------------- | ------------ |
| Contracts  | 95%        | 90%         | 80% | 100%           | N/A          |
| Engine     | 90%        | 85%         | 75% | 80%            | 100%         |
| Node       | 90%        | 85%         | 75% | 85%            | 90%          |
| Schema     | 95%        | 90%         | 80% | 100%           | 100%         |
| Graph      | 85%        | 80%         | 70% | 70%            | 80%          |
| Agent      | 85%        | 90%         | 85% | 75%            | 90%          |
| MultiAgent | 80%        | 85%         | 90% | 70%            | 85%          |

### Performance Benchmarks

```python
# packages/haive-core/tests/benchmarks/test_performance.py
import pytest
from pytest_benchmark.fixture import BenchmarkFixture

@pytest.mark.benchmark(group="contracts")
def test_contract_extraction_performance(benchmark: BenchmarkFixture):
    """Benchmark contract extraction performance."""
    contract = ExecutionContract(...)
    state = create_large_state()  # 10MB state

    result = benchmark(contract.extract, state)

    # Performance assertions
    assert benchmark.stats["mean"] < 0.001  # < 1ms average
    assert benchmark.stats["max"] < 0.010   # < 10ms worst case
```

---

## 🚀 IMPLEMENTATION TIMELINE WITH TESTING

### Week 1: Foundation & Testing Setup

- **Day 1-2**: Set up testing infrastructure (Hypothesis, Golden, Fixtures)
- **Day 3-4**: Create ExecutionContract with property tests
- **Day 5**: Establish golden test baselines

### Week 2: Engine Decomposition

- **Day 1-2**: Break apart AugLLMConfig with compatibility tests
- **Day 3-4**: Create golden tests for serialization
- **Day 5**: Integration tests with real LLMs

### Week 3: Node Consolidation

- **Day 1-2**: Implement ContractNode with fixture hierarchy
- **Day 3-4**: Property tests for node composition
- **Day 5**: End-to-end workflow tests

### Week 4: Schema Modularization

- **Day 1-2**: Separate StateSchema with backward compatibility
- **Day 3-4**: Property tests for schema composition
- **Day 5**: Golden tests for state persistence

### Week 5: Graph & Workflow

- **Day 1-2**: Simplify BaseGraph with regression tests
- **Day 3-4**: Create Workflow layer with integration tests
- **Day 5**: Performance benchmarks

### Week 6: Agent Cleanup

- **Day 1-2**: Consolidate agents with compatibility layer
- **Day 3-4**: Multi-agent integration tests
- **Day 5**: End-to-end system tests

### Week 7: Integration & Polish

- **Day 1-2**: Full system integration tests
- **Day 3-4**: Performance optimization
- **Day 5**: Documentation and handoff

---

## 🎯 SUCCESS CRITERIA

### Testing Success Metrics

- ✅ **100% backward compatibility** via golden tests
- ✅ **Zero regressions** in functionality
- ✅ **<100ms p99 latency** for all operations
- ✅ **90%+ code coverage** across all components
- ✅ **All property tests passing** with 10,000+ examples
- ✅ **Real LLM integration** tests passing

### Quality Gates

1. **PR Gate**: All unit tests + property tests must pass
2. **Integration Gate**: Golden tests + integration tests must pass
3. **Release Gate**: E2E tests + performance benchmarks must pass

---

## 📚 TESTING RESOURCES

### Required Dependencies

```toml
[tool.poetry.dev-dependencies]
hypothesis = "^6.0"
pytest = "^7.0"
pytest-asyncio = "^0.21"
pytest-benchmark = "^4.0"
pytest-cov = "^4.0"
pytest-golden = "^0.2"
pytest-xdist = "^3.0"  # Parallel testing
```

### Test Execution Commands

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=haive --cov-report=html

# Run property tests with more examples
poetry run pytest -k property --hypothesis-profile=thorough

# Update golden tests
poetry run pytest --golden-update

# Run benchmarks
poetry run pytest --benchmark-only

# Parallel execution
poetry run pytest -n auto
```

---

**This enhanced implementation roadmap provides the complete testing process with Hypothesis for property-based testing, Golden tests for compatibility, and pytest fixtures for component testing. Each phase now has comprehensive testing strategies to ensure quality and prevent regressions.**
