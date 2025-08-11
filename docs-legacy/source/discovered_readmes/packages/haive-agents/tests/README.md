# Haive Agents Test Suite

This directory contains comprehensive tests for the Haive Agents package.

## Test Organization

### Unit Tests (`unit/`)

- **Purpose**: Test individual components in isolation
- **Scope**: Single functions, classes, or small modules
- **Examples**: Simple agent tests, schema tests, individual mixin tests

### Integration Tests (`integration/`)

- **Purpose**: Test component interactions and end-to-end workflows
- **Scope**: Multiple components working together
- **Examples**: Agent workflows, database persistence, tool integration

### Package-Level Tests (Root)

- **Purpose**: Package-wide functionality and cross-component tests
- **Scope**: Full agent scenarios, serialization, configuration

## Key Test Categories

### Agent Tests

- **Simple Agents** (`simple/`): Basic agent functionality
- **RAG Agents** (`rag/`): Retrieval-augmented generation workflows
- **ReAct Agents** (`react/`): Reasoning and acting patterns
- **Multi-Agent** (`multi/`): Agent collaboration and communication
- **Research Agents** (`research/`): Deep research and analysis patterns

### Persistence & Configuration

- **Supabase Integration** (`integration/supabase/`): Database persistence testing
- **Configuration** (various): Agent configuration and state management

### Specialized Features

- **Document Processing** (`document/`): Document analysis and modification
- **Tool Integration** (various): External tool usage and management
- **Discovery** (`discovery/`): Dynamic tool and capability discovery

## Supabase Integration Tests

### Location: `integration/supabase/`

**Purpose**: Verify Haive agents properly integrate with Supabase for conversation persistence.

**Key Features Tested**:

- ✅ Automatic Supabase configuration detection
- ✅ Conversation persistence across sessions
- ✅ Thread ID-based conversation management
- ✅ Recursion limit handling
- ✅ Error resilience (prepared statement errors)

**Prerequisites**:

```bash
export POSTGRES_CONNECTION_STRING="postgresql://postgres.{project}:{password}@aws-0-{region}.pooler.supabase.com:6543/postgres"
```

**Run Tests**:

```bash
# All Supabase tests
poetry run pytest packages/haive-agents/tests/integration/supabase/ -v

# Specific test
poetry run pytest packages/haive-agents/tests/integration/supabase/test_supabase_integration.py -v

# Manual scripts
poetry run python packages/haive-agents/tests/integration/supabase/test_supabase_complete.py
```

## Running Tests

### Full Test Suite

```bash
# All tests
poetry run pytest packages/haive-agents/tests/ -v

# Specific category
poetry run pytest packages/haive-agents/tests/integration/ -v
poetry run pytest packages/haive-agents/tests/unit/ -v
```

### Test Selection

```bash
# By pattern
poetry run pytest packages/haive-agents/tests/ -k "supabase" -v
poetry run pytest packages/haive-agents/tests/ -k "simple_agent" -v

# By marker (if defined)
poetry run pytest packages/haive-agents/tests/ -m "integration" -v
```

### Debug Mode

```bash
# Verbose output with print statements
poetry run pytest packages/haive-agents/tests/ -v -s

# Stop on first failure
poetry run pytest packages/haive-agents/tests/ -x

# Run specific test with debugging
poetry run pytest packages/haive-agents/tests/integration/supabase/test_supabase_integration.py::TestSupabaseIntegration::test_data_persistence -v -s
```

## Test Configuration

### Environment Variables

Tests may require these environment variables:

- `POSTGRES_CONNECTION_STRING`: Supabase/PostgreSQL connection
- `OPENAI_API_KEY`: For LLM-based tests
- `ANTHROPIC_API_KEY`: For Claude-based tests

### Test Fixtures

Common fixtures are defined in:

- `conftest.py`: Package-wide fixtures
- `integration/supabase/conftest.py`: Supabase-specific fixtures
- `fixtures/`: Shared test data and utilities

### Test Data

- Mock data and fixtures in `fixtures/`
- Test outputs in `logs/` and `resources/`
- Temporary test data cleaned up automatically

## Writing Tests

### Test Structure

```python
import pytest
from haive.agents.simple.agent import SimpleAgent

class TestMyFeature:
    """Test suite for specific feature."""

    def test_basic_functionality(self):
        """Test basic case."""
        agent = SimpleAgent()
        result = agent.run(...)
        assert result is not None

    @pytest.mark.asyncio
    async def test_async_functionality(self):
        """Test async operations."""
        # async test code
```

### Best Practices

1. **Isolation**: Each test should be independent
2. **Cleanup**: Use fixtures to ensure cleanup
3. **Assertions**: Clear, specific assertions
4. **Documentation**: Docstrings explaining test purpose
5. **Error Handling**: Test both success and failure cases

### Test Categories

Use these patterns for organization:

- `test_basic_*`: Fundamental functionality
- `test_integration_*`: Component interaction
- `test_error_*`: Error handling
- `test_edge_*`: Edge cases and boundaries

## Continuous Integration

Tests are designed to work in CI environments:

```yaml
# GitHub Actions example
- name: Run Haive Agents Tests
  env:
    POSTGRES_CONNECTION_STRING: ${{ secrets.SUPABASE_CONNECTION_STRING }}
  run: |
    poetry run pytest packages/haive-agents/tests/ \
      --ignore=packages/haive-agents/tests/integration/supabase/ \
      -v

# Run Supabase tests only if connection available
- name: Run Supabase Integration Tests
  if: env.POSTGRES_CONNECTION_STRING != ''
  run: |
    poetry run pytest packages/haive-agents/tests/integration/supabase/ -v
```

## Troubleshooting

### Common Issues

**Import Errors**:

```bash
# Ensure package is installed in development mode
poetry install
```

**Environment Variables**:

```bash
# Check required variables are set
echo $POSTGRES_CONNECTION_STRING
```

**Database Connection**:

```bash
# Test Supabase connectivity
poetry run python packages/haive-agents/tests/integration/supabase/test_direct_write.py
```

**Test Discovery**:

```bash
# List all discovered tests
poetry run pytest packages/haive-agents/tests/ --collect-only
```

### Performance

- Some tests may be slow due to LLM API calls
- Use `pytest-xdist` for parallel execution:
  ```bash
  poetry add --group dev pytest-xdist
  poetry run pytest packages/haive-agents/tests/ -n auto
  ```

## Related Documentation

- [Supabase Integration Guide](../../project_docs/SUPABASE_INTEGRATION.md)
- [Agent Mixins Documentation](../src/haive/agents/base/mixins/README.md)
- [Troubleshooting Guide](../../project_docs/TROUBLESHOOTING_PREPARED_STATEMENTS.md)
