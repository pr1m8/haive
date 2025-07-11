# Build and Test Guide - Haive Framework

**Version**: 1.0  
**Purpose**: Comprehensive build, test, and quality assurance procedures  
**Last Updated**: 2025-01-09

## 🚨 NEVER Rush Implementation

### Research First, Code Second

```bash
# ALWAYS research before implementing
# 1. Check existing codebase for patterns
find packages/ -name "*.py" | xargs grep -l "YourPattern" | head -5

# 2. Check documentation for existing solutions
grep -r "your_topic" project_docs/ | head -10

# 3. Look at similar implementations
find packages/ -name "*.py" -path "*/similar_module/*" | head -5
```

### Common Rushing Mistakes

- **Skipping Pydantic research** - Not checking existing model patterns
- **Ignoring existing utilities** - Reinventing wheels that exist
- **Missing validation patterns** - Not following established schemas
- **Bypassing build tools** - Not using trunk for quality checks

## 🛠️ Build System Overview

### Core Tools

- **Trunk**: Code linting, formatting, and quality checks
- **Poetry**: Dependency management and virtual environments
- **Pytest**: Testing framework with real component testing

### Quality Pipeline

```bash
# Complete quality check pipeline
trunk check --all                    # Lint and format
poetry run mypy packages/            # Type checking
poetry run pytest                    # Run tests
poetry run ruff check packages/      # Additional linting
```

## 🔧 Essential Build Commands

### Development Workflow

```bash
# 1. Install dependencies
poetry install --all-extras

# 2. Check code quality (ALWAYS run before commits)
trunk check --all

# 3. Run tests
poetry run pytest packages/haive-{package}/tests/ -v

# 4. Type checking
poetry run mypy packages/haive-{package}/src/

# 5. Build documentation (when system is ready)
poetry run sphinx-build -b html docs/source docs/build
```

### Trunk Usage (Primary Quality Tool)

```bash
# Check all files
trunk check --all

# Check specific files
trunk check path/to/file.py

# Fix auto-fixable issues
trunk check --fix --all

# Check only changed files
trunk check --upstream origin/main

# Run specific linters
trunk check --filter=mypy,black
```

### Documentation Commands

```bash
# Build documentation (when system is ready)
poetry run sphinx-build -b html docs/source docs/build

# Alternative manual build
cd docs && make html
```

## 📊 Testing Standards

### Testing Commands

```bash
# Run all tests
poetry run pytest

# Run specific package tests
poetry run pytest packages/haive-agents/tests/ -v

# Run with coverage
poetry run pytest --cov=haive --cov-report=html

# Run specific test file
poetry run pytest packages/haive-agents/tests/test_simple.py -v

# Run tests matching pattern
poetry run pytest -k "test_agent" -v
```

### Test Configuration

The project uses pytest with these paths configured:

```toml
[tool.pytest.ini_options]
pythonpath = [
  "packages/haive-core/src",
  "packages/haive-agents/src",
  "packages/haive-tools/src",
  "packages/haive-games/src",
  "packages/haive-dataflow/src",
  "packages/haive-prebuilt/src",
]
```

## 🔍 Pydantic Best Practices

### 🚨 Common Pydantic Mistakes to Avoid

#### 1. Manual **init** Override (DON'T DO THIS)

```python
# ❌ WRONG - Overriding __init__ breaks Pydantic
class AgentConfig(BaseModel):
    name: str
    temperature: float

    def __init__(self, name, temperature):  # ❌ BREAKS PYDANTIC
        self.name = name
        self.temperature = temperature
```

#### 2. Not Using Field Validation

```python
# ❌ WRONG - No validation
class AgentConfig(BaseModel):
    name: str
    temperature: float

# ✅ CORRECT - Proper validation
class AgentConfig(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
```

#### 3. Ignoring Existing Patterns

```bash
# ALWAYS check existing Pydantic patterns before creating new ones
find packages/ -name "*.py" | xargs grep -l "class.*BaseModel" | head -5
grep -r "Field(" packages/ | head -10
```

### ✅ Proper Pydantic Usage

#### Research Existing Patterns First

```bash
# Check existing config patterns
find packages/ -name "*config*.py" | head -5

# Look at existing BaseModel usage
grep -r "class.*BaseModel" packages/ | head -10

# Check field validation patterns
grep -r "Field(" packages/ | head -10
```

#### Proper Model Definition

```python
from pydantic import BaseModel, Field, field_validator, model_validator
from typing import List, Optional, Dict, Any
from enum import Enum

class ModelType(str, Enum):
    """Use enums for constrained choices."""
    GPT4 = "gpt-4"
    GPT4_TURBO = "gpt-4-turbo"
    CLAUDE_3 = "claude-3"

class AgentConfig(BaseModel):
    """Agent configuration with comprehensive validation.

    Always include:
    - Full docstring with examples
    - Field validation with constraints
    - Custom validators when needed
    - Configuration class for Pydantic settings
    """

    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        use_enum_values=True,
        extra="forbid"  # Prevent unknown fields
    )

    name: str = Field(
        ...,
        min_length=3,
        max_length=50,
        pattern=r"^[a-zA-Z0-9_]+$",
        description="Agent identifier (alphanumeric + underscore)"
    )

    model: ModelType = Field(
        default=ModelType.GPT4,
        description="LLM model selection"
    )

    temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=2.0,
        description="Sampling temperature"
    )

    tools: List[str] = Field(
        default_factory=list,
        description="Available tool names"
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate agent name format."""
        if not v.replace("_", "").isalnum():
            raise ValueError("Name must be alphanumeric with underscores only")
        return v

    @field_validator("tools")
    @classmethod
    def validate_tools(cls, v: List[str]) -> List[str]:
        """Validate tool names against known tools."""
        # Check against existing tool registry
        from haive.core.tools import get_available_tools
        available = get_available_tools()
        invalid = set(v) - set(available)
        if invalid:
            raise ValueError(f"Unknown tools: {', '.join(invalid)}")
        return v

    @model_validator(mode="after")
    def validate_compatibility(self) -> "AgentConfig":
        """Validate cross-field compatibility."""
        # Example: certain models don't support certain tools
        if self.model == ModelType.CLAUDE_3 and "code_execution" in self.tools:
            raise ValueError("Claude-3 doesn't support code execution tools")
        return self
```

#### Using Existing Patterns

```python
# ALWAYS check if similar configs exist
from haive.core.config import BaseEngineConfig  # Check if this exists

# Inherit from existing patterns when possible
class MyAgentConfig(BaseEngineConfig):
    """Extend existing config patterns."""
    my_specific_field: str = Field(...)
```

## 🔍 Research Methodology

### Before Writing ANY Code

```bash
# 1. Check existing implementations
find packages/ -name "*.py" | xargs grep -l "similar_concept" | head -5

# 2. Read existing documentation
grep -r "your_topic" project_docs/ | head -5

# 3. Look at tests for usage patterns
find packages/ -name "test_*.py" | xargs grep -l "similar_concept" | head -5

# 4. Check import patterns
grep -r "from.*import.*YourConcept" packages/ | head -5
```

### Research Checklist

- [ ] **Existing implementations**: Are there similar classes/functions?
- [ ] **Documentation**: Is this already documented somewhere?
- [ ] **Test patterns**: How are similar things tested?
- [ ] **Import patterns**: How are similar things imported?
- [ ] **Configuration**: Are there existing config patterns?
- [ ] **Validation**: How is similar data validated?

## 📋 Quality Checklist

### Before Committing

```bash
# 1. Research existing patterns
find packages/ -name "*.py" | xargs grep -l "your_pattern"

# 2. Run full quality pipeline
trunk check --all
poetry run mypy packages/
poetry run pytest
poetry run ruff check packages/

# 3. Check imports work
poetry run python -c "from haive.core import *; print('OK')"

# 4. Verify documentation builds (when system is ready)
poetry run sphinx-build -b html docs/source docs/build
```

### Code Quality Standards

- [ ] **No rushing**: Researched existing patterns first
- [ ] **Proper Pydantic**: No manual **init**, proper Field usage
- [ ] **Type hints**: All public functions fully typed
- [ ] **Documentation**: Google-style docstrings
- [ ] **Testing**: Real components, no mocks
- [ ] **Validation**: Proper error handling
- [ ] **Imports**: Explicit package references

## 🚨 Build Failure Recovery

### Common Issues and Solutions

```bash
# Import errors
poetry run python -c "import sys; print(sys.path)"
poetry install --all-extras

# Test failures
poetry run pytest --tb=short  # Shorter traceback
poetry run pytest --lf        # Last failed only

# Type errors
poetry run mypy packages/your-package/src/ --show-error-codes

# Trunk errors
trunk check --fix --all       # Auto-fix what's possible
```

### Environment Issues

```bash
# Clean environment
poetry env remove python
poetry install --all-extras

# Check Python path
poetry run python -c "import sys; print('\n'.join(sys.path))"

# Verify package installation
poetry show --tree
```

## 📊 Performance Monitoring

### Build Performance

```bash
# Time commands for performance monitoring
time trunk check --all
time poetry run pytest
time poetry run mypy packages/
```

### Quality Metrics

- **Lint time**: <30 seconds for full check
- **Test time**: <5 minutes for full suite
- **Type check**: <2 minutes for full codebase
- **Doc build**: <3 minutes for full docs

---

**Remember**: Quality tools are your safety net. Always use them before committing. Take time to research - it prevents major bugs and rework later!
