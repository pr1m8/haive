# Supervisor Tests

This directory contains comprehensive tests for all supervisor implementations, organized by category and testing approach.

## Test Organization

### Core Tests (This Directory)

- **test_dynamic_multi_agent.py** - Multi-agent coordination tests
- **test_with_registry.py** - Agent registry functionality
- **test_rebuild_verification.py** - Dynamic rebuild testing
- **test_compatibility.py** - Compatibility between supervisor versions
- **test_registry_demo.py** - Registry demonstration tests
- **test_registry_real.py** - Real registry implementation tests
- **test_advanced_prebuilt.py** - Advanced prebuilt configurations
- **test_post_compile_addition.py** - Post-compilation agent addition
- **test_dynamic_addition_fixed.py** - Dynamic agent addition fixes

### Subdirectories

#### `/components/`

Component-specific tests focusing on individual supervisor components:

- **test_component_1_state.py** - State management testing
- **test_component_2_tools.py** - Tool generation and management
- **test_component_3_agent_execution.py** - Agent execution patterns
- **test_component_4_multiagent.py** - Multi-agent components
- **test_component_4_supervisor.py** - Supervisor component integration

#### `/experiments/`

Experimental pattern tests and research implementations:

- **test_dynamic_supervisor.py** - Dynamic supervisor patterns
- **test_multiagent_minimal.py** - Minimal multi-agent implementations
- **test_simple_flow.py** - Simple execution flow tests
- **test_natural_flow.py** - Natural language flow tests
- **test_full_dynamic_flow.py** - Complete dynamic workflow tests
- And many more experimental tests...

## Running Tests

### All Supervisor Tests

```bash
poetry run pytest tests/supervisor/ -v
```

### Specific Categories

```bash
# Core supervisor tests
poetry run pytest tests/supervisor/test_*.py -v

# Component tests
poetry run pytest tests/supervisor/components/ -v

# Experimental tests
poetry run pytest tests/supervisor/experiments/ -v
```

### Individual Tests

```bash
# Run specific test file
poetry run pytest tests/supervisor/test_registry_real.py -v

# Run specific test function
poetry run pytest tests/supervisor/test_registry_real.py::test_specific_function -v
```

## Test Categories

### 1. Registry Tests

Tests for agent registry functionality:

- Agent registration and retrieval
- Dynamic agent addition/removal
- Registry persistence and state management
- Agent metadata and capabilities

### 2. State Management Tests

Tests for supervisor state handling:

- State transitions and updates
- Multi-agent state coordination
- State persistence and recovery
- Custom state schema validation

### 3. Tool Integration Tests

Tests for supervisor tool generation:

- Dynamic tool creation
- Tool synchronization with state
- Handoff tool functionality
- Tool error handling

### 4. Agent Execution Tests

Tests for agent execution patterns:

- Agent routing and selection
- Execution flow management
- Error handling and recovery
- Performance and timing

### 5. Multi-Agent Coordination Tests

Tests for multi-agent workflows:

- Agent communication patterns
- Task distribution and coordination
- Conflict resolution
- Parallel vs sequential execution

## Testing Philosophy

### Real Component Testing

All tests follow the **no-mocks** principle:

- Use real LLM integrations
- Test with actual agent implementations
- Validate real state transitions
- Test actual tool executions

### Comprehensive Coverage

Tests cover:

- **Happy path scenarios** - Normal operation
- **Edge cases** - Boundary conditions
- **Error conditions** - Failure modes
- **Performance scenarios** - Load and stress testing

### Test Structure

```python
def test_supervisor_functionality():
    \"\"\"Test supervisor with real components.\"\"\"
    # Arrange - Create real supervisor and agents
    supervisor = create_real_supervisor()
    agents = create_real_agents()

    # Act - Execute real operation
    result = supervisor.coordinate_agents(task)

    # Assert - Verify real outcomes
    assert result.success
    assert result.agents_used == expected_agents
```

## Test Data and Fixtures

### Common Fixtures

- **real_supervisor** - Production supervisor instances
- **test_agents** - Various agent types for testing
- **sample_tasks** - Representative task scenarios
- **test_state** - Various state configurations

### Test Data

- **Agent configurations** - Different agent setups
- **Task scenarios** - Various task types and complexities
- **State examples** - Different state configurations
- **Tool definitions** - Standard tool sets for testing

## Writing New Tests

### Test Naming Convention

```python
def test_supervisor_[functionality]_[scenario]():
    \"\"\"Test supervisor [functionality] in [scenario] condition.\"\"\"
    # Test implementation
```

### Test Structure Template

```python
import pytest
from haive.agents.supervisor import SupervisorAgent

class TestSupervisorFeature:
    \"\"\"Test suite for supervisor feature.\"\"\"

    @pytest.fixture
    def supervisor(self):
        \"\"\"Create test supervisor.\"\"\"
        return SupervisorAgent(config)

    def test_feature_happy_path(self, supervisor):
        \"\"\"Test feature under normal conditions.\"\"\"
        # Test implementation

    def test_feature_edge_case(self, supervisor):
        \"\"\"Test feature with edge case input.\"\"\"
        # Test implementation

    def test_feature_error_handling(self, supervisor):
        \"\"\"Test feature error handling.\"\"\"
        # Test implementation
```

### Best Practices

1. **Use descriptive test names** that explain the scenario
2. **Test real components** - no mocks or stubs
3. **Include error scenarios** - test failure modes
4. **Use appropriate fixtures** - reuse common setup
5. **Assert meaningful outcomes** - verify actual behavior

## Test Maintenance

### Regular Tasks

- Update tests when supervisor APIs change
- Add tests for new features and patterns
- Review and clean up outdated tests
- Update test data and fixtures

### Performance Monitoring

- Monitor test execution time
- Identify slow tests that need optimization
- Track test coverage and completeness
- Review test reliability and flakiness

## Related Documentation

- [Supervisor Implementation](../../src/haive/agents/supervisor/) - Main supervisor code
- [Dynamic Supervisor](../../src/haive/agents/dynamic_supervisor/) - Dynamic supervisor implementation
- [Examples](../../examples/supervisor/) - Usage examples
- [Documentation](../../docs/supervisor/) - Architecture and patterns

## Contributing

When adding new tests:

1. Follow the existing test structure and naming conventions
2. Use real components - no mocks
3. Include comprehensive test scenarios
4. Update this README if adding new test categories
5. Ensure tests pass in CI/CD pipeline
