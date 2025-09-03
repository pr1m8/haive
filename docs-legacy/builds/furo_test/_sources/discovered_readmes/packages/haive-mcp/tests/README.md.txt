# MCP Tests

Comprehensive test suite for the haive-mcp package.

## Test Structure

```
tests/
├── unit/                    # Unit tests for individual components
│   ├── test_config.py      # Configuration model tests
│   ├── test_manager.py     # Manager functionality tests
│   └── test_discovery.py   # Discovery system tests
├── integration/            # Integration tests
│   ├── test_mcp_servers.py # Server integration tests
│   ├── test_agents.py      # Agent integration tests
│   └── test_dataflow.py    # Dataflow integration tests
├── fixtures/               # Test fixtures and mocks
└── conftest.py            # Pytest configuration
```

## Running Tests

### All Tests

```bash
poetry run pytest
```

### Specific Test Category

```bash
poetry run pytest tests/unit/
poetry run pytest tests/integration/
```

### With Coverage

```bash
poetry run pytest --cov=haive.mcp --cov-report=html
```

### Verbose Output

```bash
poetry run pytest -v
```

## Test Categories

### Unit Tests

- Fast, isolated tests
- Mock external dependencies
- Test individual functions/classes

### Integration Tests

- Test component interactions
- May use real MCP servers
- Test with haive-dataflow

### End-to-End Tests

- Full workflow tests
- Test real-world scenarios
- May require external services

## Writing Tests

### Test Structure

```python
import pytest
from haive.mcp import MCPManager

class TestMCPManager:
    """Test suite for MCPManager.

    Tests cover:
    - Server addition and removal
    - Tool discovery
    - Health monitoring
    - Error handling
    """

    @pytest.fixture
    def manager(self):
        """Create test manager instance."""
        return MCPManager()

    async def test_add_server(self, manager):
        """Test adding an MCP server.

        Verifies:
        - Server is added successfully
        - Tools are discovered
        - Status is updated correctly
        """
        result = await manager.add_server("test", config)
        assert result.success
        assert result.tools_count > 0
```

### Fixtures

Common fixtures are available in `conftest.py`:

- `mock_mcp_client`: Mock MCP client
- `test_server_config`: Test server configuration
- `test_engine`: Test LLM engine

## Test Data

Test data is stored in `fixtures/`:

- `mock_servers.json`: Mock server definitions
- `test_responses.json`: Mock API responses

## Continuous Integration

Tests run automatically on:

- Pull requests
- Main branch commits
- Release tags

## Debugging Tests

### Run Single Test

```bash
poetry run pytest tests/unit/test_manager.py::TestMCPManager::test_add_server -v
```

### Debug Mode

```bash
poetry run pytest --pdb
```

### Show Output

```bash
poetry run pytest -s
```
