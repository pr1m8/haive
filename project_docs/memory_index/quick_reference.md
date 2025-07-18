# Quick Reference - Most Used Memories

## 🚨 Critical Rules

1. **Always use `poetry run`** → @memory_index/by_task/poetry_run_everything.md
2. **NO MOCKS EVER in tests** → @memory_index/by_pattern/no_mocks_testing.md
3. **Never override `__init__` in Pydantic** → @memory_index/by_error/pydantic_init_override.md
4. **Use explicit imports** → `from haive.core.engine import X`

## 🔧 Common Fixes

### Documentation Build Errors

```bash
# KeyError in AutoAPI
find . -name "*\ *" -o -name "*(*" -o -name "*)*"  # Find bad filenames
# See: @memory_index/by_error/containers_tilebag_keyerror.md

# Syntax errors in examples
find packages -name "*.py" -exec python -m py_compile {} \;
# See: @memory_index/by_task/documentation_97_percent_fix.md
```

### Import Errors

```bash
# Always test imports first
poetry run python -c "from haive.core import *; print('OK')"

# Fix with
poetry install --all-extras
```

### Test Failures

```python
# NO MOCKS pattern
config = AugLLMConfig()  # Real config
agent = SimpleAgent(engine=config)  # Real agent
result = agent.run("test")  # Real execution
```

## 📋 Common Patterns

### Agent Creation

```python
# SimpleAgent
from haive.agents.simple import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig

config = AugLLMConfig(temperature=0.7)
agent = SimpleAgent(name="my_agent", engine=config)

# ReactAgent with tools
from haive.agents.react import ReactAgent
agent = ReactAgent(name="react", engine=config, tools=[tool1, tool2])
```

### Pydantic Models

```python
# NEVER override __init__
class MyConfig(BaseModel):
    name: str = Field(..., min_length=1)
    value: float = Field(default=0.0, ge=0.0)

    # Use validators instead
    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        return v
```

### Documentation Build

```bash
# Standard build
nox -s docs

# Quick test
poetry run sphinx-build -b html docs/source docs/build/html

# View locally
python -m http.server 8003 --directory docs/build/html/
```

## 🗺️ Navigation Shortcuts

- **By Error Type**: @memory_index/by_error/
- **By Date**: @memory_index/by_date/
- **By Agent**: @memory_index/by_agent/
- **By Package**: @memory_index/by_package/
- **By Task**: @memory_index/by_task/

## 🏷️ Most Referenced Tags

#no-mocks #poetry-run #documentation #import-errors #pydantic-patterns
