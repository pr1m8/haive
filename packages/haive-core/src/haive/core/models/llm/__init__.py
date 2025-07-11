"""Haive LLM Module.

This module provides comprehensive abstractions and implementations for working with
Large Language Models (LLMs) from various providers. It includes configuration classes,
provider-specific implementations, and utilities for model metadata.

The module supports a wide range of LLM providers including OpenAI, Anthropic, Google,
Azure, Mistral, and many others, with a consistent interface for configuration and use.

Key Components:
    - Base Classes: Abstract base classes for LLM configurations
    - Provider Types: Enumeration of supported LLM providers
    - Provider Implementations: Provider-specific configuration classes
    - Metadata: Utilities for accessing model capabilities and context windows

Typical usage example:
    ```python
    from haive.core.models.llm.base import OpenAILLMConfig

    # Configure an LLM
    config = OpenAILLMConfig(
        model="gpt-4",
        cache_enabled=True
    )

    # Instantiate the LLM
    llm = config.instantiate()

    # Generate text
    response = llm.generate("Explain quantum computing")
    ```
"""

# Import base classes
from haive.core.models.llm.base import LLMConfig

# Import factory functions
from haive.core.models.llm.factory import (
    LLMFactory,
    create_llm,
    get_available_providers,
    get_provider_models,
)
from haive.core.models.llm.provider_types import LLMProvider

# Import provider management
from haive.core.models.llm.providers import get_provider, list_providers

# Import base provider class
from haive.core.models.llm.providers.base import BaseLLMProvider, ProviderImportError
from haive.core.models.llm.rate_limiting_mixin import RateLimitingMixin

__all__ = [
    "BaseLLMProvider",
    "LLMConfig",
    # Factory
    "LLMFactory",
    # Core types
    "LLMProvider",
    "ProviderImportError",
    "RateLimitingMixin",
    "create_llm",
    "get_available_providers",
    # Provider management
    "get_provider",
    "get_provider_models",
    "list_providers",
]
