# Engine Implementation Quick Reference

## Instant Setup Commands

```bash
# 1. Discover implementations
find .venv -name "*.py" | xargs grep -l "class.*Embedding" | head -20

# 2. Test current registry
poetry run python -c "
from haive.core.engine.TARGET.base import BaseTargetConfig
print(f'Registered: {len(BaseTargetConfig.list_registered_types())}')"

# 3. Create todo list
poetry run python -c "
from haive.core.utils.todo import TodoWrite
todos = [
    {'content': 'Discover embeddings', 'status': 'pending', 'priority': 'high'},
    {'content': 'Categorize into phases', 'status': 'pending', 'priority': 'high'}
]
TodoWrite(todos=todos)"
```

## File Templates

### 1. Base Class Template

```python
# File: packages/haive-core/src/haive/core/engine/embeddings/base.py
_EMBEDDING_REGISTRY: Dict[str, Type["BaseEmbeddingConfig"]] = {}

class BaseEmbeddingConfig(InvokableEngine):
    engine_type: EngineType = Field(default=EngineType.EMBEDDING)

    @classmethod
    def register(cls, embedding_type: Union[str, Any]) -> Any:
        def decorator(config_cls: Type[BaseEmbeddingConfig]) -> Type[BaseEmbeddingConfig]:
            type_str = str(embedding_type.value if hasattr(embedding_type, 'value') else embedding_type)
            _EMBEDDING_REGISTRY[type_str] = config_cls
            logger.info(f"Registered embedding config: {config_cls.__name__} as {type_str}")
            return config_cls
        return decorator

    @abstractmethod
    def instantiate(self):
        raise NotImplementedError("Subclasses must implement instantiate()")
```

### 2. Provider Template

```python
# File: packages/haive-core/src/haive/core/engine/embeddings/providers/OpenAIEmbeddingConfig.py
@BaseEmbeddingConfig.register(EmbeddingType.OPENAI)
class OpenAIEmbeddingConfig(SecureConfigMixin, BaseEmbeddingConfig):
    """OpenAI embedding configuration."""

    model: str = Field(default="text-embedding-3-small")
    api_key: Optional[str] = Field(default=None)
    provider: str = Field(default="openai")

    @validator("model")
    def validate_model(cls, v):
        valid_models = ["text-embedding-3-small", "text-embedding-3-large"]
        if v not in valid_models:
            raise ValueError(f"model must be one of {valid_models}")
        return v

    def instantiate(self):
        try:
            from langchain_openai import OpenAIEmbeddings
        except ImportError:
            raise ImportError("Install: pip install langchain-openai")

        api_key = self.get_api_key()
        if not api_key:
            raise ValueError("OpenAI API key required")

        return OpenAIEmbeddings(
            model=self.model,
            openai_api_key=api_key
        )
```

### 3. Types Template

```python
# File: packages/haive-core/src/haive/core/engine/embeddings/types.py
class EmbeddingType(str, Enum):
    # Core providers
    OPENAI = "OpenAI"
    ANTHROPIC = "Anthropic"
    COHERE = "Cohere"
    HUGGINGFACE = "HuggingFace"

    # Local models
    SENTENCE_TRANSFORMERS = "SentenceTransformers"
    OLLAMA = "Ollama"
```

### 4. Registry Template

```python
# File: packages/haive-core/src/haive/core/engine/embeddings/providers/__init__.py
from .OpenAIEmbeddingConfig import OpenAIEmbeddingConfig
from .AnthropicEmbeddingConfig import AnthropicEmbeddingConfig

__all__ = [
    "OpenAIEmbeddingConfig",
    "AnthropicEmbeddingConfig",
]
```

## Testing Template

```python
# Standard test pattern
test_script = '''
from haive.core.engine.embeddings.base import BaseEmbeddingConfig
from haive.core.engine.embeddings.providers import OpenAIEmbeddingConfig
from haive.core.engine.embeddings.types import EmbeddingType

print("Testing embedding configuration...")

# Test 1: Registration
registered = BaseEmbeddingConfig.list_registered_types()
print(f"Total registered: {len(registered)}")

# Test 2: Class retrieval
config_class = BaseEmbeddingConfig.get_config_class(EmbeddingType.OPENAI)
print(f"Config class: {config_class.__name__}")

# Test 3: Configuration
config = OpenAIEmbeddingConfig(
    model="text-embedding-3-small"
)
print(f"Model: {config.model}")

# Test 4: Fields
input_fields = config.get_input_fields()
output_fields = config.get_output_fields()
print(f"Input fields: {list(input_fields.keys())}")
print(f"Output fields: {list(output_fields.keys())}")

print("✅ Test passed!")
'''

poetry run python -c test_script
```

## Implementation Checklist

### Per Implementation

- [ ] Research LangChain source in `.venv`
- [ ] Create `ProviderNameConfig.py` file
- [ ] Add to `types.py` if new type needed
- [ ] Add import to `providers/__init__.py`
- [ ] Add to `__all__` list
- [ ] Test with standard test script
- [ ] Update todo list (mark completed)
- [ ] Document in memory files

### Phase Completion

- [ ] All implementations tested
- [ ] Progress documented
- [ ] Memory files updated
- [ ] Next phase planned
- [ ] Todo list updated

## Memory File Locations

```
project_docs/claude_documentation/
├── ENGINE_IMPLEMENTATION_GUIDE.md          # Main guide (this file's sibling)
├── ENGINE_IMPLEMENTATION_QUICKREF.md       # This file
├── EMBEDDING_IMPLEMENTATION_STRATEGY.md    # Strategy for embeddings
├── EMBEDDING_PROGRESS_LOG.md               # Progress tracking
├── EMBEDDING_MEMORY.md                     # Implementation notes
└── EMBEDDING_TESTING_RESULTS.md            # Test results
```

## Common Commands

```bash
# Discovery
find .venv -name "*.py" | xargs grep -l "class.*Target"

# Testing
poetry run python -c "test_script_here"

# Check imports
poetry run python -c "from haive.core.engine.TARGET.providers import *"

# List registered
poetry run python -c "from haive.core.engine.TARGET.base import Base; print(Base.list_registered_types())"

# Update todos
poetry run python -c "from haive.core.utils.todo import TodoWrite; TodoWrite(todos=[...])"
```

## Implementation Statistics Tracking

### Template for Progress Files

```markdown
# Embedding Implementation Progress

## Phase 1: Core Providers (Target: 5)

- [x] OpenAI - 2024-01-01 - Standard API key pattern
- [x] Anthropic - 2024-01-01 - Different field names
- [ ] Cohere - In progress
- [ ] HuggingFace - Pending
- [ ] SentenceTransformers - Pending

## Statistics

- **Available**: 30+ implementations found
- **Completed**: 2/5 Phase 1
- **Success Rate**: 100%
- **Average Time**: 15 minutes
- **Issues**: None
```

## Quick Error Resolution

### Registry Not Working

```python
# WRONG - inside class
class BaseConfig:
    _registry = {}

# RIGHT - outside class
_REGISTRY = {}
class BaseConfig:
    pass
```

### API Key Issues

```python
# Use SecureConfigMixin
class Config(SecureConfigMixin, BaseConfig):
    provider: str = Field(default="provider_name")
    api_key: Optional[str] = Field(default=None)
```

### Import Errors

```python
# Graceful handling
try:
    from langchain_provider import Provider
except ImportError:
    raise ImportError("Install: pip install langchain-provider")
```

## File Path Quick Reference

```
# Base classes
packages/haive-core/src/haive/core/engine/ENGINE_TYPE/base.py

# Types
packages/haive-core/src/haive/core/engine/ENGINE_TYPE/types.py

# Providers
packages/haive-core/src/haive/core/engine/ENGINE_TYPE/providers/
├── __init__.py
└── ProviderConfig.py

# Documentation
project_docs/claude_documentation/
├── ENGINE_IMPLEMENTATION_GUIDE.md
├── ENGINE_IMPLEMENTATION_QUICKREF.md
├── ENGINE_STRATEGY.md
├── ENGINE_PROGRESS.md
└── ENGINE_MEMORY.md

# Tests
packages/haive-core/tests/engine/ENGINE_TYPE/
```

## Success Pattern Summary

1. **Discovery** → Find implementations in `.venv`
2. **Planning** → Create todos and categorize phases
3. **Implementation** → Follow template pattern
4. **Testing** → Use standard test script
5. **Documentation** → Update memory files
6. **Iteration** → Repeat for each implementation

**Key Success Factors:**

- Systematic approach with todo tracking
- Consistent naming and patterns
- Comprehensive testing after each implementation
- Detailed memory and progress documentation
- Following established SecureConfigMixin patterns
