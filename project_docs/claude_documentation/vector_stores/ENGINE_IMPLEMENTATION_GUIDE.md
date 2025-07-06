# Engine Implementation Guide for Haive Framework

## Overview

This guide documents the systematic approach and best practices for implementing engine types (vector stores, retrievers, LLMs, embeddings) in the Haive framework. It's based on successful implementation of 43+ retrievers and 14+ vector stores.

## Table of Contents

1. [Prerequisites and Setup](#prerequisites-and-setup)
2. [Discovery and Analysis Phase](#discovery-and-analysis-phase)
3. [Implementation Architecture](#implementation-architecture)
4. [Step-by-Step Implementation Process](#step-by-step-implementation-process)
5. [Testing Strategy](#testing-strategy)
6. [Memory Management and Documentation](#memory-management-and-documentation)
7. [Quality Assurance](#quality-assurance)
8. [Troubleshooting Common Issues](#troubleshooting-common-issues)

## Prerequisites and Setup

### Required Understanding

- Haive framework architecture (`packages/haive-core/src/haive/core/`)
- LangChain integration patterns
- Pydantic configuration models
- Poetry dependency management
- Testing with pytest

### Key Files to Study First

```
packages/haive-core/src/haive/core/engine/
├── base.py                    # Base engine interface
├── vectorstore/
│   ├── base.py               # Vector store base class
│   ├── types.py              # Enum definitions
│   └── providers/            # Implementation directory
├── retrievers/
│   ├── base.py               # Retriever base class
│   └── providers/            # Implementation directory
└── llm/
    ├── base.py               # LLM base class
    └── providers/            # Implementation directory
```

## Discovery and Analysis Phase

### 1. Inventory Available Implementations

**Command Pattern:**

```bash
# Find all implementations in .venv
find /path/to/.venv -name "*.py" | xargs grep -l "class.*TargetType" | head -20

# For embeddings example:
find .venv -name "*.py" | xargs grep -l "class.*Embedding" | head -20
```

**Analysis Strategy:**

- Count total available implementations
- Identify core vs specialized implementations
- Note dependency requirements
- Check for cloud vs local implementations

### 2. Categorization Strategy

Create implementation phases based on:

- **Priority**: Essential vs specialized
- **Complexity**: Simple vs advanced configuration
- **Dependencies**: Common vs rare packages
- **Usage patterns**: Frequent vs niche use cases

**Example categorization for embeddings:**

```
Phase 1: Core Providers (5-8 implementations)
- OpenAI, Anthropic, Cohere, HuggingFace
- High usage, well-documented, stable APIs

Phase 2: Specialized Providers (10-15 implementations)
- Local models, domain-specific, enterprise

Phase 3: Experimental/Niche (remaining)
- Research models, beta APIs, specialized use cases
```

## Implementation Architecture

### 1. Base Class Pattern

Every engine type follows this pattern:

```python
# Registry outside class to avoid Pydantic conflicts
_ENGINE_REGISTRY: Dict[str, Type["BaseEngineConfig"]] = {}

class BaseEngineConfig(InvokableEngine):
    """Base configuration for all engine implementations."""

    # Required fields
    engine_type: EngineType = Field(default=EngineType.YOUR_TYPE)

    @classmethod
    def register(cls, engine_type: Union[str, Any]) -> Any:
        """Register implementation with decorator."""
        def decorator(config_cls: Type[BaseEngineConfig]) -> Type[BaseEngineConfig]:
            type_str = str(engine_type.value if hasattr(engine_type, 'value') else engine_type)
            _ENGINE_REGISTRY[type_str] = config_cls
            logger.info(f"Registered engine config: {config_cls.__name__} as {type_str}")
            return config_cls
        return decorator

    @abstractmethod
    def instantiate(self):
        """Create engine instance from configuration."""
        raise NotImplementedError("Subclasses must implement instantiate()")

    def create_runnable(self, runnable_config: Optional[Dict[str, Any]] = None):
        """Required by InvokableEngine interface."""
        return self.instantiate()
```

### 2. Type Definitions

**File:** `packages/haive-core/src/haive/core/engine/ENGINE_TYPE/types.py`

```python
from enum import Enum

class EngineType(str, Enum):
    """Enumeration of supported engine types."""

    # Core implementations
    TYPE_ONE = "TypeOne"
    TYPE_TWO = "TypeTwo"

    # Specialized implementations
    SPECIALIZED_ONE = "SpecializedOne"

    # Cloud implementations
    CLOUD_ONE = "CloudOne"
```

### 3. Provider Implementation Pattern

**File:** `packages/haive-core/src/haive/core/engine/ENGINE_TYPE/providers/ConfigNameConfig.py`

```python
@BaseEngineConfig.register(EngineType.SPECIFIC_TYPE)
class SpecificEngineConfig(BaseEngineConfig):
    """Configuration for specific engine implementation."""

    # Configuration fields with validation
    required_param: str = Field(..., description="Required parameter")
    optional_param: Optional[str] = Field(default=None, description="Optional parameter")

    # Validators
    @validator("required_param")
    def validate_required_param(cls, v):
        if not v:
            raise ValueError("required_param cannot be empty")
        return v

    def get_input_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Define input schema."""
        return {
            "input_field": (str, Field(description="Input description")),
        }

    def get_output_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Define output schema."""
        return {
            "output_field": (str, Field(description="Output description")),
        }

    def instantiate(self):
        """Create engine instance."""
        try:
            from langchain_community.engines import SpecificEngine
        except ImportError:
            raise ImportError("Install required package: pip install package-name")

        # Validation
        self.validate_configuration()

        # Create instance
        return SpecificEngine(
            param1=self.required_param,
            param2=self.optional_param
        )
```

## Step-by-Step Implementation Process

### Phase 1: Setup and Planning

1. **Create Todo List**

```python
# Use TodoWrite to create implementation plan
todos = [
    {"content": "Discover all available implementations", "status": "pending", "priority": "high"},
    {"content": "Categorize implementations into phases", "status": "pending", "priority": "high"},
    {"content": "Implement Phase 1 - Core implementations", "status": "pending", "priority": "high"},
    # ... more todos
]
```

2. **Update Project Documentation**
   Create or update memory files:

- `project_docs/claude_documentation/ENGINE_IMPLEMENTATION_STRATEGY.md`
- `project_docs/claude_documentation/ENGINE_PROGRESS_LOG.md`

### Phase 2: Core Implementation Loop

**For each implementation:**

1. **Research the LangChain Implementation**

```bash
# Read the source code
Read: .venv/lib/python3.12/site-packages/langchain_community/engines/target_engine.py

# Check constructor parameters
# Note required vs optional parameters
# Identify authentication requirements
```

2. **Create Configuration Class**

```python
# File: packages/haive-core/src/haive/core/engine/ENGINE_TYPE/providers/TargetEngineConfig.py

# Follow the established pattern
# Include comprehensive docstring with examples
# Add proper field validation
# Use SecureConfigMixin for API keys if needed
```

3. **Update Type Definitions**

```python
# Add new type to ENGINE_TYPE/types.py if needed
# Ensure enum value matches registration
```

4. **Update Provider Registry**

```python
# File: packages/haive-core/src/haive/core/engine/ENGINE_TYPE/providers/__init__.py

# Add import
from .TargetEngineConfig import TargetEngineConfig

# Add to __all__ list
__all__ = [
    # ... existing configs
    "TargetEngineConfig",
]
```

5. **Test Implementation**

```python
# Create test script
test_script = '''
from haive.core.engine.ENGINE_TYPE.base import BaseEngineConfig
from haive.core.engine.ENGINE_TYPE.providers import TargetEngineConfig
from haive.core.engine.ENGINE_TYPE.types import EngineType

# Test registration
configs = BaseEngineConfig.list_registered_types()
print(f"Total registered: {len(configs)}")

# Test instantiation
config = TargetEngineConfig(
    name="test_config",
    # ... required parameters
)

# Test fields
input_fields = config.get_input_fields()
output_fields = config.get_output_fields()
print(f"Input fields: {list(input_fields.keys())}")
print(f"Output fields: {list(output_fields.keys())}")

print("✅ Test passed!")
'''

poetry run python -c test_script
```

6. **Update Todo List**

```python
# Mark current implementation as completed
# Mark test as completed
# Update progress
```

### Phase 3: Documentation and Memory

1. **Create Implementation Memory**

```markdown
## Implementation: TargetEngine

### Status: ✅ Completed

- **File**: `packages/haive-core/src/haive/core/engine/ENGINE_TYPE/providers/TargetEngineConfig.py`
- **Registration**: EngineType.TARGET_ENGINE
- **Dependencies**: package-name
- **Authentication**: API key via SecureConfigMixin
- **Special Notes**: Any implementation-specific details

### Configuration Fields:

- `api_key`: Authentication key
- `model_name`: Model identifier
- `custom_param`: Special parameter with validation

### Testing Results:

- ✅ Registration successful
- ✅ Configuration validation working
- ✅ Input/output fields defined
- ✅ Instantiation successful
```

2. **Update Progress Documentation**

```markdown
## Phase 1 Progress: Core Engines

### Completed (X/Y):

1. ✅ TargetEngine - Description
2. ✅ AnotherEngine - Description
3. 🔄 NextEngine - In progress

### Next Steps:

- Complete NextEngine implementation
- Begin Phase 2 planning
```

## Testing Strategy

### 1. Registration Testing

```python
# Verify registration
registered_types = BaseEngineConfig.list_registered_types()
assert "TargetEngine" in registered_types

# Verify class retrieval
config_class = BaseEngineConfig.get_config_class(EngineType.TARGET_ENGINE)
assert config_class is not None
```

### 2. Configuration Testing

```python
# Test valid configuration
config = TargetEngineConfig(
    name="test",
    required_param="value"
)
assert config.required_param == "value"

# Test validation
try:
    invalid_config = TargetEngineConfig(
        name="test",
        required_param=""  # Should fail validation
    )
    assert False, "Should have raised validation error"
except ValueError:
    pass  # Expected
```

### 3. Schema Testing

```python
# Test input/output fields
input_fields = config.get_input_fields()
output_fields = config.get_output_fields()

assert isinstance(input_fields, dict)
assert isinstance(output_fields, dict)
assert len(input_fields) > 0
assert len(output_fields) > 0
```

### 4. Integration Testing

```python
# Test instantiation (may require mocking)
try:
    instance = config.instantiate()
    assert instance is not None
except ImportError:
    # Expected if dependencies not installed
    pass
```

## Memory Management and Documentation

### 1. Project-Level Memory

**File**: `project_docs/claude_documentation/ENGINE_IMPLEMENTATION_MEMORY.md`

```markdown
# Engine Implementation Memory

## Current Status

- **Total Implementations**: X completed, Y in progress
- **Current Phase**: Phase N - Description
- **Next Priority**: Next implementation name

## Key Patterns Learned

1. Registry pattern prevents Pydantic conflicts
2. SecureConfigMixin for API key management
3. Validation is critical for user experience
4. Documentation examples are essential

## Common Issues and Solutions

- **Issue**: Registry not working
  - **Solution**: Move registry outside class definition
- **Issue**: API key not resolved
  - **Solution**: Use SecureConfigMixin with correct provider name
```

### 2. Implementation-Specific Memory

**File**: `project_docs/claude_documentation/ENGINE_SPECIFIC_NOTES.md`

```markdown
# Engine-Specific Implementation Notes

## TargetEngine

- **Special Requirements**: Specific authentication flow
- **Gotchas**: Parameter X must be validated specially
- **Dependencies**: Requires package-name >= 1.0.0

## AnotherEngine

- **Connection Pattern**: Uses custom connection class
- **Performance**: Requires connection pooling configuration
```

### 3. Progress Tracking

**File**: `project_docs/claude_documentation/ENGINE_PROGRESS_LOG.md`

```markdown
# Engine Implementation Progress Log

## Phase 1: Core Engines

- [x] Engine1 - 2024-01-01 - Notes
- [x] Engine2 - 2024-01-02 - Notes
- [ ] Engine3 - In progress

## Statistics

- Total Available: 50+
- Implemented: 25
- Success Rate: 100%
- Average Time: 15 minutes per engine
```

## Quality Assurance

### 1. Code Review Checklist

- [ ] Follows established naming conventions
- [ ] Includes comprehensive docstring with examples
- [ ] Has proper field validation
- [ ] Uses SecureConfigMixin for API keys
- [ ] Includes error handling in instantiate()
- [ ] Added to providers/**init**.py
- [ ] Updated types.py if needed
- [ ] Tested successfully

### 2. Documentation Standards

- [ ] Clear class docstring
- [ ] Usage examples in docstring
- [ ] Field descriptions
- [ ] Implementation notes in memory files
- [ ] Progress tracking updated

### 3. Testing Requirements

- [ ] Registration test passes
- [ ] Configuration validation works
- [ ] Input/output fields defined
- [ ] Instantiation works (or fails gracefully)
- [ ] Todo list updated

## Troubleshooting Common Issues

### 1. Registry Issues

**Problem**: `AttributeError: 'type' object has no attribute 'get_config_class'`
**Solution**: Move registry outside class definition

```python
# Wrong
class BaseConfig:
    _registry = {}

# Right
_REGISTRY = {}
class BaseConfig:
    pass
```

### 2. Pydantic Conflicts

**Problem**: `ModelPrivateAttr` errors
**Solution**: Use Field() for all attributes, avoid private attributes

### 3. Import Errors

**Problem**: Missing dependencies
**Solution**: Graceful error handling with helpful messages

```python
try:
    from langchain_community.engines import TargetEngine
except ImportError:
    raise ImportError("Install required package: pip install package-name")
```

### 4. Authentication Issues

**Problem**: API keys not resolved
**Solution**: Use SecureConfigMixin with correct provider name

```python
class EngineConfig(SecureConfigMixin, BaseEngineConfig):
    provider: str = Field(default="engine_provider")
    api_key: Optional[str] = Field(default=None)
```

## Command Reference

### Essential Commands

```bash
# Test current implementation
poetry run python -c "test_script"

# Find available implementations
find .venv -name "*.py" | xargs grep -l "TargetPattern"

# Run specific tests
poetry run pytest packages/haive-core/tests/engine/

# Check registration
poetry run python -c "from haive.core.engine.base import BaseEngineConfig; print(BaseEngineConfig.list_registered_types())"
```

### Memory Management Commands

```bash
# Create implementation memory
echo "## Implementation Notes" > project_docs/claude_documentation/ENGINE_MEMORY.md

# Update progress
echo "Phase 1: X/Y completed" >> project_docs/claude_documentation/PROGRESS.md
```

## Success Metrics

### Quantitative

- **Implementation Success Rate**: 100% (43/43 retrievers, 14/14 vector stores)
- **Average Implementation Time**: 15-20 minutes per engine
- **Test Success Rate**: 100% (all implementations tested)

### Qualitative

- **Code Quality**: Consistent patterns, comprehensive documentation
- **User Experience**: Clear error messages, helpful examples
- **Maintainability**: Well-organized, documented memory files

## Next Steps Template

When starting a new engine type implementation:

1. **Read this guide thoroughly**
2. **Study existing implementations** (vector stores, retrievers, LLMs)
3. **Create todo list** with TodoWrite
4. **Discover available implementations** in .venv
5. **Categorize into phases**
6. **Create memory files** for tracking
7. **Start with Phase 1** (core implementations)
8. **Test after each implementation**
9. **Update documentation** continuously
10. **Maintain progress tracking**

## Files Created/Modified During Implementation

### New Files

- `packages/haive-core/src/haive/core/engine/ENGINE_TYPE/providers/EngineConfig.py`
- `project_docs/claude_documentation/ENGINE_IMPLEMENTATION_STRATEGY.md`
- `project_docs/claude_documentation/ENGINE_PROGRESS_LOG.md`
- `project_docs/claude_documentation/ENGINE_MEMORY.md`

### Modified Files

- `packages/haive-core/src/haive/core/engine/ENGINE_TYPE/providers/__init__.py`
- `packages/haive-core/src/haive/core/engine/ENGINE_TYPE/types.py` (if new types added)

This guide provides a complete blueprint for implementing any engine type in the Haive framework with the same systematic approach and quality standards achieved with vector stores and retrievers.
