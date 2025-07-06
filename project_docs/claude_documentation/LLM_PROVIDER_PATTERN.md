# LLM Provider Pattern Implementation

## Overview

This document outlines the modular provider pattern implemented for LLM integrations in haive-core. This pattern provides a clean, extensible architecture for integrating multiple LangChain chat models with proper type checking, safe imports, backwards compatibility, and rate limiting capabilities.

## Architecture

### Key Components

1. **Provider Types** (`provider_types.py`) - Enum definitions for all supported providers
2. **Base Provider** (`providers/base.py`) - Abstract base class with common functionality
3. **Rate Limiting Mixin** (`rate_limiting_mixin.py`) - Cross-cutting rate limiting capabilities
4. **Individual Providers** (`providers/*.py`) - Specific implementations for each provider
5. **Factory Pattern** (`factory.py`) - Universal instantiation methods
6. **Safe Imports** (`providers/__init__.py`) - Lazy loading with error handling

### Method Resolution Order (MRO) Solution

**Critical Learning**: When using multiple inheritance with mixins and Pydantic BaseModel, the order matters:

```python
# CORRECT ORDER: Mixins first, then BaseModel
class BaseLLMProvider(SecureConfigMixin, ModelMetadataMixin, RateLimitingMixin, BaseModel):
    pass

# WRONG ORDER: Would cause MRO conflicts
class BaseLLMProvider(BaseModel, SecureConfigMixin, ModelMetadataMixin, RateLimitingMixin):
    pass
```

**Key Rules**:

- Mixins that don't inherit from BaseModel should come first
- Remove BaseModel inheritance from mixins to avoid conflicts
- Add required fields directly to base classes instead of relying on mixin inheritance

## Implementation Details

### 1. Provider Enum (`provider_types.py`)

```python
class LLMProvider(str, Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    # ... 20 total providers
```

### 2. Base Provider Class (`providers/base.py`)

```python
from abc import ABC, abstractmethod
from haive.core.common.mixins.secure_config import SecureConfigMixin
from haive.core.models.metadata_mixin import ModelMetadataMixin
from haive.core.models.llm.rate_limiting_mixin import RateLimitingMixin

class BaseLLMProvider(SecureConfigMixin, ModelMetadataMixin, RateLimitingMixin, BaseModel, ABC):
    """Abstract base for all LLM providers with rate limiting."""

    # Rate limiting fields (copied from mixin to avoid MRO issues)
    requests_per_second: Optional[float] = Field(default=None, ge=0)
    tokens_per_second: Optional[int] = Field(default=None, ge=0)
    tokens_per_minute: Optional[int] = Field(default=None, ge=0)
    # ... other rate limiting fields

    @abstractmethod
    def _get_chat_class(self):
        """Get the LangChain chat class for this provider."""
        pass

    @abstractmethod
    def _get_default_model(self) -> str:
        """Get the default model for this provider."""
        pass

    @abstractmethod
    def _get_import_package(self) -> str:
        """Get the package name for installation instructions."""
        pass
```

### 3. Rate Limiting Mixin (`rate_limiting_mixin.py`)

```python
class RateLimitingMixin:
    """Mixin for rate limiting capabilities - NO BaseModel inheritance."""

    def apply_rate_limiting(self, llm):
        """Apply rate limiting to an LLM instance."""
        try:
            from langchain_core.rate_limiters import InMemoryRateLimiter
            # ... implementation
        except ImportError:
            logger.warning("Rate limiting not available")
            return llm
```

### 4. Individual Providers (`providers/openai.py`, etc.)

```python
class OpenAIProvider(BaseLLMProvider):
    """OpenAI provider implementation."""

    provider: LLMProvider = Field(default=LLMProvider.OPENAI)
    temperature: float = Field(default=0.7, ge=0, le=2)
    max_tokens: Optional[int] = Field(default=None, gt=0)

    def _get_chat_class(self):
        from langchain_openai import ChatOpenAI
        return ChatOpenAI

    def _get_default_model(self) -> str:
        return "gpt-3.5-turbo"

    def _get_import_package(self) -> str:
        return "langchain-openai"
```

### 5. Safe Import System (`providers/__init__.py`)

```python
def _lazy_import_provider(provider_name: str):
    """Lazy import with error handling."""
    try:
        module = importlib.import_module(f".{provider_name}", __name__)
        return getattr(module, f"{provider_name.title()}Provider")
    except ImportError as e:
        logger.warning(f"Provider {provider_name} not available: {e}")
        return None

# Registry pattern
PROVIDER_REGISTRY = {
    LLMProvider.OPENAI: lambda: _lazy_import_provider("openai"),
    LLMProvider.ANTHROPIC: lambda: _lazy_import_provider("anthropic"),
    # ...
}
```

### 6. Universal Factory (`factory.py`)

```python
class LLMFactory:
    """Universal factory for creating LLM instances."""

    @staticmethod
    def create(provider: Union[str, LLMProvider], **kwargs):
        """Create LLM with provider string or enum."""
        provider_enum = LLMProvider(provider) if isinstance(provider, str) else provider

        # Extract rate limiting params
        rate_limit_params = {k: v for k, v in kwargs.items()
                           if k in ['requests_per_second', 'tokens_per_minute', ...]}

        # Get provider class and instantiate
        provider_class = get_provider(provider_enum)
        provider_instance = provider_class(**kwargs)
        return provider_instance.instantiate()

# Convenience functions
def create_llm(provider: Union[str, LLMProvider], **kwargs):
    """Global convenience function."""
    return LLMFactory.create(provider, **kwargs)
```

## Key Lessons Learned

### 1. MRO (Method Resolution Order) Conflicts

**Problem**: `TypeError: Cannot create a consistent method resolution order (MRO)`

**Solution**:

- Order inheritance correctly: mixins first, BaseModel last
- Remove BaseModel from mixins
- Add required fields directly to base classes

### 2. Pydantic Field Overrides

**Problem**: `Field 'provider' defined on a base class was overridden`

**Solution**: Use proper field annotations:

```python
# CORRECT
provider: LLMProvider = Field(default=LLMProvider.OPENAI)

# WRONG
provider = LLMProvider.OPENAI
```

### 3. Test Organization

**Problem**: Tests importing full haive stack causing circular imports

**Solution**:

- Create minimal conftest.py for LLM tests
- Run tests from haive root: `poetry run pytest packages/haive-core/tests/...`
- Use proper test isolation

### 4. Rate Limiting Integration

**Key Points**:

- LangChain's `InMemoryRateLimiter` requires specific parameter names
- Not all LLMs support `.with_rate_limiter()` method
- Graceful fallback when rate limiting fails

## Benefits of This Pattern

1. **Modularity**: Each provider is in its own file
2. **Type Safety**: Full type checking with mypy
3. **Safe Imports**: Optional dependencies don't break the system
4. **Backwards Compatibility**: Existing code continues to work
5. **Rate Limiting**: Universal rate limiting for all providers
6. **Extensibility**: Easy to add new providers
7. **Factory Pattern**: Universal creation methods
8. **Error Handling**: Graceful handling of missing dependencies

## Testing Strategy

### 1. MRO Tests

- Verify inheritance order works correctly
- Test instantiation without conflicts

### 2. Rate Limiting Tests

- Test with and without rate limits
- Mock LangChain rate limiter
- Test error handling

### 3. Provider Tests

- Test each provider individually
- Mock import errors
- Test parameter validation

### 4. Factory Tests

- Test string and enum provider creation
- Test parameter passing
- Test error scenarios

## Usage Examples

### Basic Usage

```python
from haive.core.models.llm.factory import create_llm

# Using string provider
llm = create_llm("openai", model="gpt-4", temperature=0.8)

# Using enum
from haive.core.models.llm.provider_types import LLMProvider
llm = create_llm(LLMProvider.ANTHROPIC, model="claude-3-sonnet-20240229")
```

### With Rate Limiting

```python
llm = create_llm(
    "openai",
    model="gpt-4",
    requests_per_second=10,
    tokens_per_minute=100000
)
```

### Backwards Compatibility

```python
# Old style still works
from haive.core.models.llm.base import LLMConfig
config = LLMConfig(provider=LLMProvider.OPENAI, model="gpt-4")
llm = config.instantiate()
```

## Next Steps

This pattern should be applied to:

1. **Retrievers** - Vector store and document retrievers
2. **Embeddings** - Text embedding models
3. **Vector Stores** - Vector database providers
4. **Tools** - External tool integrations

Each implementation should follow the same architectural patterns:

- Provider enums and base classes
- Safe import system with lazy loading
- Factory pattern for universal creation
- Proper MRO ordering for mixins
- Comprehensive testing strategy
- Rate limiting where applicable

## Dependencies

Add provider-specific dependencies to `pyproject.toml`:

```toml
[tool.poetry.extras]
openai = ["langchain-openai"]
anthropic = ["langchain-anthropic"]
google = ["langchain-google-genai"]
all-providers = ["langchain-openai", "langchain-anthropic", ...]
```

This allows users to install only the providers they need:

```bash
poetry install --extras "openai anthropic"
```
