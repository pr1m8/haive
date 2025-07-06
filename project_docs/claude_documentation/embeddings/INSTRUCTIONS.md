# Embeddings Implementation Instructions

## Overview

This document provides complete instructions for implementing embedding providers in the Haive framework, based on the proven patterns from vector store and retriever implementations.

## Quick Start for New Agent

### 1. Study the Vector Store Implementation First

**Required Reading** (in order):

1. `../vector_stores/ENGINE_IMPLEMENTATION_GUIDE.md` - Complete implementation methodology
2. `../vector_stores/IMPLEMENTATION_PATTERNS_MEMORY.md` - Proven patterns and solutions
3. `../vector_stores/ENGINE_IMPLEMENTATION_QUICKREF.md` - Templates and commands
4. `../vector_stores/VECTOR_STORE_IMPLEMENTATION_STRATEGY.md` - Strategic approach

### 2. Understand the Current Codebase Structure

**Examine these existing files**:

```bash
# Study the existing embedding base class
Read: packages/haive-core/src/haive/core/models/embeddings/base.py

# Check current providers
LS: packages/haive-core/src/haive/core/models/embeddings/providers/

# See current types
Read: packages/haive-core/src/haive/core/models/embeddings/types.py
```

### 3. Discover Available Embedding Implementations

**Discovery Commands**:

```bash
# Find all embedding implementations in LangChain
find .venv -name "*.py" | xargs grep -l "class.*Embedding" | grep -v "__pycache__" | head -20

# Count total available
find .venv -name "*.py" -exec grep -l "class.*Embedding.*:" {} \; | wc -l

# Check specific providers
find .venv -name "*.py" | xargs grep -l "OpenAIEmbeddings\|AnthropicEmbeddings\|CohereEmbeddings"
```

## Implementation Architecture

### Current Structure (Analyze First)

```
packages/haive-core/src/haive/core/models/embeddings/
├── base.py                    # Base embedding configuration
├── types.py                   # Embedding provider types
└── providers/
    ├── __init__.py           # Provider registry
    └── [ProviderEmbeddingConfig.py files]
```

### Required Implementation Pattern

#### 1. Registry Pattern (CRITICAL)

**Study the vector store registry pattern and apply it**:

```python
# Move registry OUTSIDE class to avoid Pydantic conflicts
_EMBEDDING_REGISTRY: Dict[str, Type["BaseEmbeddingConfig"]] = {}

class BaseEmbeddingConfig(InvokableEngine):
    @classmethod
    def register(cls, embedding_type: Union[str, Any]) -> Any:
        def decorator(config_cls: Type[BaseEmbeddingConfig]) -> Type[BaseEmbeddingConfig]:
            type_str = str(embedding_type.value if hasattr(embedding_type, 'value') else embedding_type)
            _EMBEDDING_REGISTRY[type_str] = config_cls
            logger.info(f"Registered embedding config: {config_cls.__name__} as {type_str}")
            return config_cls
        return decorator
```

#### 2. Provider Implementation Template

```python
# File: packages/haive-core/src/haive/core/models/embeddings/providers/OpenAIEmbeddingConfig.py

from typing import Any, Dict, List, Optional, Tuple, Type
from pydantic import Field, validator, SecretStr
from haive.core.common.mixins.secure_config import SecureConfigMixin
from haive.core.models.embeddings.base import BaseEmbeddingConfig
from haive.core.models.embeddings.types import EmbeddingType

@BaseEmbeddingConfig.register(EmbeddingType.OPENAI)
class OpenAIEmbeddingConfig(SecureConfigMixin, BaseEmbeddingConfig):
    """
    Configuration for OpenAI embedding models in the Haive framework.

    This embedding provider uses OpenAI's text-embedding models for
    generating high-quality vector representations of text.

    OpenAI embeddings provide:
    1. High-quality text representations
    2. Multiple model sizes (small, large)
    3. Consistent API and performance
    4. Well-documented and stable

    This embedding provider is particularly useful when:
    - You need production-ready, high-quality embeddings
    - Want consistent performance and reliability
    - Building commercial applications
    - Need good multilingual support

    Attributes:
        model (str): OpenAI model name.
        api_key (Optional[str]): OpenAI API key (auto-resolved).
        dimensions (Optional[int]): Output dimensions (model-dependent).

    Examples:
        >>> from haive.core.models.embeddings import OpenAIEmbeddingConfig
        >>>
        >>> # Create config
        >>> config = OpenAIEmbeddingConfig(
        ...     model="text-embedding-3-small"
        ... )
        >>>
        >>> # Instantiate and use
        >>> embeddings = config.instantiate()
        >>> vectors = embeddings.embed_documents(["Hello world", "Another doc"])
        >>>
        >>> # Single embedding
        >>> vector = embeddings.embed_query("Search query")
    """

    # Model configuration
    model: str = Field(
        default="text-embedding-3-small",
        description="OpenAI embedding model name"
    )

    # API configuration (SecureConfigMixin)
    api_key: Optional[SecretStr] = Field(
        default=None,
        description="OpenAI API key (auto-resolved from OPENAI_API_KEY)"
    )

    # Provider for SecureConfigMixin
    provider: str = Field(default="openai", description="Provider name for API key resolution")

    # Model-specific parameters
    dimensions: Optional[int] = Field(
        default=None,
        description="Number of dimensions for embedding output (model-dependent)"
    )

    # Performance settings
    chunk_size: int = Field(
        default=1000,
        ge=1,
        le=2048,
        description="Number of texts to embed in each batch"
    )

    max_retries: int = Field(
        default=3,
        ge=0,
        le=10,
        description="Maximum number of retries for failed requests"
    )

    request_timeout: Optional[float] = Field(
        default=None,
        gt=0,
        description="Request timeout in seconds"
    )

    # Advanced settings
    show_progress_bar: bool = Field(
        default=False,
        description="Whether to show progress bar for batch operations"
    )

    @validator("model")
    def validate_model(cls, v):
        """Validate OpenAI model name."""
        valid_models = [
            "text-embedding-3-small",
            "text-embedding-3-large",
            "text-embedding-ada-002"
        ]
        if v not in valid_models:
            raise ValueError(f"model must be one of {valid_models}, got {v}")
        return v

    @validator("dimensions")
    def validate_dimensions(cls, v, values):
        """Validate dimensions for specific models."""
        if v is not None:
            model = values.get("model", "")
            if model == "text-embedding-3-small" and v > 1536:
                raise ValueError("text-embedding-3-small max dimensions: 1536")
            elif model == "text-embedding-3-large" and v > 3072:
                raise ValueError("text-embedding-3-large max dimensions: 3072")
        return v

    def get_input_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return input field definitions for OpenAI embeddings."""
        return {
            "texts": (List[str], Field(description="Texts to embed")),
        }

    def get_output_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return output field definitions for OpenAI embeddings."""
        return {
            "embeddings": (List[List[float]], Field(description="Generated embeddings")),
        }

    def instantiate(self):
        """
        Create an OpenAI embeddings instance from this configuration.

        Returns:
            OpenAIEmbeddings: Instantiated OpenAI embeddings.

        Raises:
            ImportError: If required packages are not available.
            ValueError: If configuration is invalid.
        """
        try:
            from langchain_openai import OpenAIEmbeddings
        except ImportError:
            raise ImportError(
                "OpenAI embeddings require langchain-openai package. "
                "Install with: pip install langchain-openai"
            )

        # Get API key using SecureConfigMixin
        api_key = self.get_api_key()
        if not api_key:
            import os
            api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ValueError(
                "OpenAI API key is required. Set OPENAI_API_KEY environment variable "
                "or provide api_key parameter."
            )

        # Prepare kwargs
        kwargs = {
            "openai_api_key": api_key,
            "model": self.model,
            "chunk_size": self.chunk_size,
            "max_retries": self.max_retries,
            "show_progress_bar": self.show_progress_bar,
        }

        # Add optional parameters
        if self.dimensions:
            kwargs["dimensions"] = self.dimensions

        if self.request_timeout:
            kwargs["request_timeout"] = self.request_timeout

        # Create OpenAI embeddings instance
        return OpenAIEmbeddings(**kwargs)
```

## Step-by-Step Implementation Process

### Phase 1: Setup (CRITICAL)

1. **Create Todo List**

```python
# Use TodoWrite to plan implementation
todos = [
    {"content": "Discover all available embedding implementations", "status": "pending", "priority": "high"},
    {"content": "Categorize embeddings into implementation phases", "status": "pending", "priority": "high"},
    {"content": "Implement OpenAI embeddings", "status": "pending", "priority": "high"},
    {"content": "Test OpenAI implementation", "status": "pending", "priority": "high"},
    # Add more as needed
]
```

2. **Study Existing Structure**

```bash
# Check what already exists
Read: packages/haive-core/src/haive/core/models/embeddings/base.py
Read: packages/haive-core/src/haive/core/models/embeddings/types.py
LS: packages/haive-core/src/haive/core/models/embeddings/providers/
```

3. **Discover Available Implementations**

```bash
# Find all embedding implementations
find .venv -name "*.py" | xargs grep -l "class.*Embedding" | head -30
```

### Phase 2: Implementation Loop

**For each embedding provider:**

1. **Research LangChain Implementation**

```bash
# Study the source
Read: .venv/lib/python3.12/site-packages/langchain_openai/embeddings/base.py
Read: .venv/lib/python3.12/site-packages/langchain_community/embeddings/openai.py
```

2. **Create Configuration Class**

- Follow the template above
- Include comprehensive docstring
- Add proper validation
- Use SecureConfigMixin for API keys

3. **Update Types (if needed)**

```python
# Add to types.py if new type
class EmbeddingType(str, Enum):
    OPENAI = "OpenAI"
    # ... add new type
```

4. **Update Provider Registry**

```python
# Add to providers/__init__.py
from .OpenAIEmbeddingConfig import OpenAIEmbeddingConfig

__all__ = [
    "OpenAIEmbeddingConfig",
    # ... existing configs
]
```

5. **Test Implementation**

```python
# Standard test script
test_script = '''
from haive.core.models.embeddings.base import BaseEmbeddingConfig
from haive.core.models.embeddings.providers import OpenAIEmbeddingConfig
from haive.core.models.embeddings.types import EmbeddingType

print("Testing OpenAI embedding configuration...")

# Test registration
registered = BaseEmbeddingConfig.list_registered_types()
print(f"Total registered: {len(registered)}")

# Test configuration
config = OpenAIEmbeddingConfig(
    model="text-embedding-3-small"
)
print(f"Model: {config.model}")

# Test fields
input_fields = config.get_input_fields()
output_fields = config.get_output_fields()
print(f"Input fields: {list(input_fields.keys())}")
print(f"Output fields: {list(output_fields.keys())}")

print("✅ Test passed!")
'''

poetry run python -c test_script
```

6. **Update Progress**

```python
# Mark tasks as completed in todo list
# Update progress documentation
```

## Recommended Implementation Phases

### Phase 1: Core API Providers (Priority 1)

**Target**: 4-5 implementations

1. **OpenAI** - Most popular, well-documented
2. **Anthropic** - High-quality alternative
3. **Cohere** - Specialized in embeddings
4. **Azure OpenAI** - Enterprise OpenAI
5. **Google (Vertex AI)** - Google ecosystem

### Phase 2: Open Source Models (Priority 2)

**Target**: 6-8 implementations

1. **HuggingFace** - Huge model ecosystem
2. **Sentence Transformers** - Popular local embeddings
3. **Ollama** - Local model serving
4. **ONNX** - Cross-platform inference
5. **TensorFlow Hub** - Google's model hub
6. **Torch** - PyTorch models
7. **Spacy** - NLP library embeddings
8. **FastText** - Facebook's word embeddings

### Phase 3: Specialized Providers (Priority 3)

**Target**: 5-7 implementations

1. **Jina** - Multi-modal embeddings
2. **Voyage AI** - Embedding-focused API
3. **BGE** - BAAI general embeddings
4. **E5** - Microsoft embeddings
5. **Instructor** - Instruction-tuned embeddings
6. **Nomic** - Atlas embeddings
7. **Gradient** - Gradient embeddings

## Testing Strategy

### 1. Registration Testing

```python
# Verify registration works
registered_types = BaseEmbeddingConfig.list_registered_types()
assert "OpenAI" in registered_types
```

### 2. Configuration Testing

```python
# Test valid configuration
config = OpenAIEmbeddingConfig(model="text-embedding-3-small")
assert config.model == "text-embedding-3-small"

# Test validation
try:
    bad_config = OpenAIEmbeddingConfig(model="invalid-model")
    assert False, "Should fail validation"
except ValueError:
    pass  # Expected
```

### 3. Schema Testing

```python
# Test input/output fields
input_fields = config.get_input_fields()
output_fields = config.get_output_fields()
assert "texts" in input_fields
assert "embeddings" in output_fields
```

## Memory and Documentation Requirements

### Create These Files

```
project_docs/claude_documentation/embeddings/
├── INSTRUCTIONS.md                          # This file
├── EMBEDDING_IMPLEMENTATION_STRATEGY.md     # Strategic planning
├── EMBEDDING_PROGRESS_LOG.md               # Progress tracking
├── EMBEDDING_IMPLEMENTATION_MEMORY.md      # Implementation notes
└── EMBEDDING_TESTING_RESULTS.md           # Test results
```

### Document These Patterns

1. **API Key Resolution**: How each provider handles authentication
2. **Model Validation**: Provider-specific model name patterns
3. **Parameter Mapping**: LangChain parameter to config field mapping
4. **Error Handling**: Common errors and solutions
5. **Performance Notes**: Batch sizes, timeout settings

## Common Patterns to Follow

### 1. Authentication Patterns

- **API Key Providers**: Use SecureConfigMixin with `api_key` field
- **Local Models**: No authentication needed
- **Enterprise**: May need additional authentication fields

### 2. Model Configuration

- **Model Names**: Validate against known model lists
- **Dimensions**: Validate against model capabilities
- **Context Length**: Consider token limits for input

### 3. Performance Settings

- **Batch Size**: Optimize for provider limits
- **Retries**: Handle rate limiting gracefully
- **Timeouts**: Set reasonable defaults

### 4. Error Handling

- **Import Errors**: Clear installation instructions
- **Authentication Errors**: Helpful API key guidance
- **Model Errors**: Suggest valid alternatives

## Expected Outcomes

### Quantitative Goals

- **Implementation Success Rate**: 100% (following vector store pattern)
- **Test Coverage**: 100% (all implementations tested)
- **Documentation Coverage**: 100% (comprehensive docs)

### Qualitative Goals

- **Code Consistency**: Follow established patterns
- **User Experience**: Clear errors and examples
- **Maintainability**: Well-organized codebase

## File Path Reference

### Implementation Files

```
packages/haive-core/src/haive/core/models/embeddings/
├── base.py                                  # Base class (may need updates)
├── types.py                                 # Types enum (add new types)
└── providers/
    ├── __init__.py                         # Registry (add imports)
    ├── OpenAIEmbeddingConfig.py           # New implementations
    ├── AnthropicEmbeddingConfig.py        # New implementations
    └── ...                                 # More implementations
```

### Documentation Files

```
project_docs/claude_documentation/embeddings/
├── INSTRUCTIONS.md                          # This file
├── EMBEDDING_IMPLEMENTATION_STRATEGY.md     # Strategy document
├── EMBEDDING_PROGRESS_LOG.md               # Progress tracking
└── EMBEDDING_IMPLEMENTATION_MEMORY.md      # Implementation memory
```

## Success Indicators

You'll know you're successful when:

1. **All implementations register correctly** (no registry conflicts)
2. **All tests pass** (configuration, validation, fields)
3. **Error handling works** (graceful failures with helpful messages)
4. **Documentation is comprehensive** (examples work, fields documented)
5. **Patterns are consistent** (follows vector store patterns exactly)

## Get Started Commands

```bash
# 1. Create your todo list
poetry run python -c "from haive.core.utils.todo import TodoWrite; TodoWrite(todos=[...])"

# 2. Discover implementations
find .venv -name "*.py" | xargs grep -l "class.*Embedding" | head -20

# 3. Study existing code
Read: packages/haive-core/src/haive/core/models/embeddings/base.py

# 4. Start with OpenAI (most straightforward)
# Create: packages/haive-core/src/haive/core/models/embeddings/providers/OpenAIEmbeddingConfig.py

# 5. Test your first implementation
poetry run python -c "test_script_here"
```

**Remember**: The vector store implementation achieved 100% success rate by following systematic patterns. Apply the same methodology to embeddings for guaranteed success.
