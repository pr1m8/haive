# Example **init**.py Structure for haive-core

## 1. `/haive/core/__init__.py` (Already Good! ✅)

This one already uses the `__getattr__` pattern correctly:

```python
"""Haive Core - Foundation for the Haive AI Agent Framework.

[... docstring ...]
"""

import importlib
import logging
import os
import pkgutil
from pathlib import Path

# Core modules to expose (in order of importance)
_CORE_MODULES = [
    "engine",     # Engine system - most important
    "graph",      # Graph building
    "schema",     # Schema management
    "tools",      # Tool system
    "types",      # Type definitions
    "utils",      # Utilities
    "models",     # Model configurations  <-- This is exposed!
    "registry",   # Component registry
    "runtime",    # Runtime system
    "persistence",# State persistence
    "config",     # Configuration
    "common",     # Common utilities
    "errors",     # Error types
]

def __getattr__(name: str):
    """Lazy load modules and their contents on demand."""
    if name in _CORE_MODULES:
        module = importlib.import_module(f".{name}", package=__name__)
        globals()[name] = module
        return module

    # ... handle specific class imports ...

__all__ = [
    # Modules
    "engine",
    "graph",
    "schema",
    "tools",
    "types",
    "utils",
    "models",     # <-- Module is in __all__
    "registry",
    "runtime",
    "persistence",
    "config",
    "common",
    "errors",
    # Common classes for convenience
    "AugLLMConfig",
    "AugLLMFactory",
    "BaseGraph",
    # ...
]
```

**This allows**: `from haive.core import models` ✅

## 2. `/haive/core/models/__init__.py` (Needs Module Exposure)

**CURRENT** (imports classes but not submodules):

```python
"""Core models module for the Haive framework.

[... docstring ...]
"""

# Embeddings module imports - with most commonly used configs
from haive.core.models.embeddings import (
    BaseEmbeddingConfig,
    EmbeddingProvider,
    HuggingFaceEmbeddingConfig,
    OpenAIEmbeddingConfig,
    create_embeddings,
)

# LLM module imports - comprehensive provider support
from haive.core.models.llm import (
    LLMConfig,
    LLMFactory,
    LLMProvider,
    create_llm,
)

# ... more imports ...

__all__ = [
    # Metadata utilities
    "ModelMetadata",
    "MetadataMixin",
    # LLM components
    "LLMConfig",
    "LLMFactory",
    "LLMProvider",
    # ... etc (NO MODULES HERE!) ...
]
```

**SHOULD BE** (with module exposure):

```python
"""Core models module for the Haive framework.

[... keep existing docstring ...]
"""

import importlib

# Submodules available for lazy loading
_SUBMODULES = [
    "embeddings",
    "llm",
    "metadata",
    "metadata_mixin",
    "retriever",
    "vectorstore",
]

# Keep existing imports for backward compatibility
from haive.core.models.embeddings import (
    BaseEmbeddingConfig,
    EmbeddingProvider,
    HuggingFaceEmbeddingConfig,
    OpenAIEmbeddingConfig,
    create_embeddings,
)

from haive.core.models.llm import (
    LLMConfig,
    LLMFactory,
    LLMProvider,
    create_llm,
)

# ... keep other imports ...

def __getattr__(name: str):
    """Lazy load submodules on demand."""
    if name in _SUBMODULES:
        module = importlib.import_module(f".{name}", package=__name__)
        globals()[name] = module
        return module
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

__all__ = [
    # Submodules (ADD THESE!)
    "embeddings",
    "llm",
    "metadata",
    "metadata_mixin",
    "retriever",
    "vectorstore",
    # Keep existing exports
    "ModelMetadata",
    "MetadataMixin",
    "LLMConfig",
    "LLMFactory",
    "LLMProvider",
    # ... rest of existing __all__ ...
]
```

**This allows**:

- `from haive.core.models import llm` ✅
- `from haive.core.models import embeddings` ✅
- `from haive.core.models.llm import LLMConfig` (still works) ✅

## 3. `/haive/core/models/llm/__init__.py` (Also Needs Submodules)

**CURRENT**:

```python
"""LLM module providing abstractions for Large Language Models.

[... docstring ...]
"""

from haive.core.models.llm.base import LLMConfig
from haive.core.models.llm.factory import LLMFactory, create_llm
from haive.core.models.llm.provider_types import LLMProvider
# ... more imports ...

__all__ = [
    "LLMConfig",
    "LLMFactory",
    "LLMProvider",
    # ... (NO SUBMODULES!)
]
```

**SHOULD BE**:

```python
"""LLM module providing abstractions for Large Language Models.

[... keep existing docstring ...]
"""

import importlib

# Submodules available
_SUBMODULES = [
    "base",
    "factory",
    "provider_types",
    "providers",  # This is a subpackage with provider implementations
    "rate_limiting_mixin",
]

# Keep existing imports
from haive.core.models.llm.base import LLMConfig
from haive.core.models.llm.factory import LLMFactory, create_llm
from haive.core.models.llm.provider_types import LLMProvider
# ... keep other imports ...

def __getattr__(name: str):
    """Lazy load submodules on demand."""
    if name in _SUBMODULES:
        module = importlib.import_module(f".{name}", package=__name__)
        globals()[name] = module
        return module
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

__all__ = [
    # Submodules
    "base",
    "factory",
    "provider_types",
    "providers",
    "rate_limiting_mixin",
    # Keep existing exports
    "LLMConfig",
    "LLMFactory",
    "LLMProvider",
    # ... rest of existing __all__ ...
]
```

**This allows**:

- `from haive.core.models.llm import providers` ✅
- `from haive.core.models.llm.providers import OpenAIProvider` ✅

## 4. `/haive/core/models/llm/providers/__init__.py`

**CURRENT** (from your earlier script output - has 27 exports but no module exposure):

**SHOULD BE**:

```python
"""LLM provider implementations.

This module contains specific provider implementations for various LLM services.
"""

import importlib

# Provider modules
_PROVIDER_MODULES = [
    "ai21",
    "anthropic",
    "azure",
    "base",
    "bedrock",
    "cohere",
    "fireworks",
    "google",
    "groq",
    "huggingface",
    "mistral",
    "nvidia",
    "ollama",
    "openai",
    "replicate",
    "together",
    "xai",
]

def __getattr__(name: str):
    """Lazy load provider modules on demand."""
    if name in _PROVIDER_MODULES:
        module = importlib.import_module(f".{name}", package=__name__)
        globals()[name] = module
        return module
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

# You can also import specific classes if commonly used
from haive.core.models.llm.providers.openai import OpenAIProvider
from haive.core.models.llm.providers.anthropic import AnthropicProvider

__all__ = [
    # Provider modules
    *_PROVIDER_MODULES,
    # Commonly used classes
    "OpenAIProvider",
    "AnthropicProvider",
]
```

## Complete Import Chain Example

With this structure, all these imports work:

```python
# 1. Import the models module
from haive.core import models

# 2. Access llm submodule (lazy loaded)
llm_module = models.llm

# 3. Access providers from llm (lazy loaded)
providers = models.llm.providers

# 4. Access specific provider (lazy loaded)
openai_provider = models.llm.providers.openai

# 5. Direct imports still work
from haive.core.models import LLMConfig
from haive.core.models.llm import LLMFactory
from haive.core.models.llm.providers import OpenAIProvider

# 6. This is what Sphinx AutoAPI expects to work
import haive.core.models.llm.providers.nvidia  # Should find NVIDIAProvider
```

## Key Pattern

The pattern is consistent at each level:

1. Define `_SUBMODULES` list
2. Add `__getattr__` for lazy loading
3. Keep existing imports for backward compatibility
4. Add submodules to `__all__`

This makes the module structure "discoverable" by Sphinx AutoAPI while maintaining lazy loading for performance.
