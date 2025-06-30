# CLAUDE Quick Reference

## Essential Commands

### Testing
```bash
# Run tests for a specific package
poetry run pytest packages/haive-agents/tests/

# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=haive
```

### Documentation
```bash
# Build documentation
poetry run nox -s docs

# Serve documentation with auto-reload
poetry run nox -s docs_serve

# Check documentation links
poetry run nox -s docs_check
```

### Development
```bash
# Install all dependencies
poetry install --all-extras

# Run linting
poetry run nox -s lint

# Run type checking
poetry run nox -s typecheck
```

## Project Structure

```
/home/will/Projects/haive/backend/haive/
├── packages/                    # All Haive packages
│   ├── haive-core/             # Core functionality
│   ├── haive-agents/           # Agent implementations
│   ├── haive-tools/            # Tool implementations
│   ├── haive-games/            # Game implementations
│   ├── haive-dataflow/         # Dataflow and streaming
│   ├── haive-mcp/              # MCP integration
│   └── haive-prebuilt/         # Prebuilt components
├── docs/                       # User documentation
│   └── source/                 # Sphinx source files
├── project_docs/               # Developer documentation
│   └── claude_documentation/   # Claude-specific docs
└── noxfile.py                  # Build automation
```

## Common Patterns

### Agent Development
```python
from haive.core.agent import BaseAgent
from haive.core.schema import AgentSchema

class MyAgent(BaseAgent):
    """Custom agent implementation."""
    
    async def process(self, input_data):
        # Agent logic here
        return result
```

### Tool Creation
```python
from haive.core.tool import BaseTool
from haive.core.schema import ToolSchema

class MyTool(BaseTool):
    """Custom tool implementation."""
    
    async def execute(self, **kwargs):
        # Tool logic here
        return result
```

## Key Locations

- **Agents**: `packages/haive-agents/src/haive/agents/`
- **Tools**: `packages/haive-tools/src/haive/tools/`
- **Games**: `packages/haive-games/src/haive/games/`
- **Tests**: `packages/{package-name}/tests/`
- **Examples**: `docs/source/examples/`

## Environment Variables

```bash
# API Keys
OPENAI_API_KEY=your-key
ANTHROPIC_API_KEY=your-key

# Database
DATABASE_URL=postgresql://user:pass@localhost/haive

# Development
DEBUG=True
LOG_LEVEL=DEBUG
```

## Debugging Tips

1. **Import Issues**: Check `__init__.py` files and package dependencies
2. **Test Failures**: Run with `-vv` for verbose output
3. **Documentation Build**: Check for missing docstrings or malformed RST
4. **Type Errors**: Use `mypy --show-error-codes` for detailed errors

## Useful Git Commands

```bash
# Check status excluding .history
git status --porcelain | grep -v "\.history"

# Stage all changes except .history
git add . ':!.history'

# Commit with descriptive message
git commit -m "feat: reorganize documentation structure"
```