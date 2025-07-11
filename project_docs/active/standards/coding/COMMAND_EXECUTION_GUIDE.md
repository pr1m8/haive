# Command Execution Guide - Haive Framework

**Version**: 1.0  
**Purpose**: Critical guide for ALL command execution in Haive  
**Last Updated**: 2025-01-09

## 🚨 GOLDEN RULE: Always Use `poetry run`

**EVERY Python command in this project MUST use `poetry run` prefix.**

### Why This Matters

- Poetry manages virtual environments and dependencies
- Direct Python execution will use wrong dependencies
- Import errors and version conflicts without `poetry run`
- ALL developers have made this mistake

## ✅ CORRECT Command Patterns

### Python Scripts

```bash
# ✅ CORRECT
poetry run python scripts/my_script.py
poetry run python -m haive.agents.simple
poetry run python examples/agent_example.py

# ❌ WRONG - NEVER DO THIS
python scripts/my_script.py
python -m haive.agents.simple
python examples/agent_example.py
```

### Testing

```bash
# ✅ CORRECT
poetry run pytest
poetry run pytest packages/haive-agents/tests/ -v
poetry run pytest -k "test_simple_agent"

# ❌ WRONG
pytest
pytest packages/haive-agents/tests/ -v
```

### Type Checking

```bash
# ✅ CORRECT
poetry run mypy packages/
poetry run mypy packages/haive-agents/src/

# ❌ WRONG
mypy packages/
```

### Linting

```bash
# ✅ CORRECT (with poetry)
poetry run ruff check packages/
poetry run black packages/

# ✅ ALSO CORRECT (trunk is external)
trunk check --all
trunk check --fix --all
```

### Documentation

```bash
# ✅ CORRECT
poetry run sphinx-build -b html docs/source docs/build

# ❌ WRONG
sphinx-build -b html docs/source docs/build
```

### Interactive Python

```bash
# ✅ CORRECT
poetry run python
poetry run ipython
poetry run jupyter notebook

# ❌ WRONG
python
ipython
jupyter notebook
```

## 🔧 Using Nox (External Tool)

Nox runs outside poetry but uses poetry internally:

```bash
# ✅ CORRECT - Nox is external
nox -s docs
nox -s test
nox -s lint

# Inside noxfile.py, nox MUST use poetry run:
@nox.session
def test(session):
    # ✅ CORRECT in noxfile.py
    session.run("poetry", "install", external=True)
    session.run("poetry", "run", "pytest", external=True)

    # ❌ WRONG in noxfile.py
    session.run("pytest")  # Will fail!
```

## 📋 Quick Import Test

Before starting work, ALWAYS test imports:

```bash
# Test core imports work
poetry run python -c "from haive.core import *; print('✅ Core imports work')"

# Test agent imports
poetry run python -c "from haive.agents.simple import SimpleAgent; print('✅ Agent imports work')"

# Test your specific imports
poetry run python -c "from haive.your.module import YourClass; print('✅ Import works')"
```

## 🚨 Common Execution Mistakes

### 1. Running scripts directly

```bash
# ❌ WRONG - Extremely common mistake
python examples/simple_agent.py

# Error: ModuleNotFoundError: No module named 'haive'

# ✅ CORRECT
poetry run python examples/simple_agent.py
```

### 2. Testing without poetry

```bash
# ❌ WRONG
pytest tests/

# Error: ImportError: cannot import name 'SimpleAgent'

# ✅ CORRECT
poetry run pytest tests/
```

### 3. Running modules

```bash
# ❌ WRONG
python -m haive.agents.simple

# ✅ CORRECT
poetry run python -m haive.agents.simple
```

### 4. Quick scripts

```bash
# ❌ WRONG - Even for one-liners!
python -c "import haive; print(haive.__version__)"

# ✅ CORRECT
poetry run python -c "import haive; print(haive.__version__)"
```

## 🔍 Debugging Import Errors

If you get import errors:

```bash
# 1. Check you're using poetry run
which python  # Should show .venv path

# 2. Verify poetry environment
poetry env info

# 3. Check Python path
poetry run python -c "import sys; print('\n'.join(sys.path))"

# 4. Reinstall if needed
poetry install --all-extras
```

## 📊 Environment Verification

### Check Your Setup

```bash
# Verify poetry installation
poetry --version

# Check virtual environment
poetry env info

# List installed packages
poetry show

# Check Python version
poetry run python --version
```

### Fix Common Issues

```bash
# Rebuild environment
poetry env remove python
poetry install --all-extras

# Update dependencies
poetry update

# Clear caches
poetry cache clear pypi --all
```

## 🎯 Integration with Tools

### VS Code

```json
// .vscode/settings.json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "python.terminal.activateEnvironment": true,
  "python.testing.pytestArgs": ["--no-cov"],
  "python.testing.unittestEnabled": false,
  "python.testing.pytestEnabled": true
}
```

### PyCharm

- Set interpreter to: `{project}/.venv/bin/python`
- Enable "Use Poetry" in project settings
- Configure run configurations with poetry

### Command Aliases (Optional)

```bash
# In your shell config (.bashrc, .zshrc)
alias pr='poetry run'
alias prp='poetry run python'
alias prt='poetry run pytest'

# Usage
prp my_script.py
prt packages/haive-agents/tests/
```

## 📝 Summary

**REMEMBER**: If you're typing `python` without `poetry run`, you're doing it wrong!

- **ALWAYS**: `poetry run python`
- **NEVER**: just `python`
- **External tools** (trunk, nox): Can run directly
- **Inside nox**: Must use `poetry run`

When in doubt: `poetry run` everything!
