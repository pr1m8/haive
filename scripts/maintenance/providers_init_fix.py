#!/usr/bin/env python3
"""Show how to fix the providers/__init__.py to expose modules."""

from __future__ import annotations

CURRENT_BEGINNING = '''"""LLM Providers Module.


__all__ = [
    "AI21Provider",
    # ... list of classes ...
]

This module contains provider-specific implementations...
"""'''

FIXED_VERSION = '''"""LLM Providers Module.

This module contains provider-specific implementations for various Language Model
providers supported by the Haive framework. Each provider is implemented in its
own module with safe imports and proper error handling.

The module uses lazy imports to avoid requiring all provider dependencies to be
installed. Only the providers actually used will trigger dependency checks.

Available Providers:
    - OpenAI (GPT-3.5, GPT-4, etc.)
    - Anthropic (Claude models)
    - Google (Gemini, Vertex AI)
    - Azure OpenAI
    - AWS Bedrock
    - Mistral AI
    - Groq
    - Cohere
    - Together AI
    - Fireworks AI
    - Hugging Face
    - NVIDIA AI Endpoints
    - Ollama (local models)
    - Llama.cpp (local models)
    - And many more...

Examples:
    Safe import with error handling::

        from haive.core.models.llm.providers import get_provider

        try:
            provider_class = get_provider("openai")
            provider = provider_class(model="gpt-4")
            llm = provider.instantiate()
        except ImportError as e:
            print(f"Provider not available: {e}")

.. autosummary::
   :toctree: generated/

   get_provider
   list_providers
"""

import importlib
import logging

from haive.core.models.llm.provider_types import LLMProvider
from haive.core.models.llm.providers.base import BaseLLMProvider, ProviderImportError

logger = logging.getLogger(__name__)

# Provider modules available for import
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
    # Add any other provider modules here
]

# [Keep the existing __all__ list with all the class names]
__all__ = [
    # Provider modules (ADD THESE!)
    *_PROVIDER_MODULES,
    # Existing class exports
    "AI21Provider",
    "AnthropicProvider",
    "AzureOpenAIProvider",
    "BaseLLMProvider",
    "BedrockProvider",
    "CohereProvider",
    "FireworksProvider",
    "GeminiProvider",
    "GroqProvider",
    "HuggingFaceProvider",
    "MistralProvider",
    "NVIDIAProvider",
    "OllamaProvider",
    "OpenAIProvider",
    "ProviderImportError",
    "ReplicateProvider",
    "TogetherProvider",
    "VertexAIProvider",
    "XAIProvider",
    "create_graph_transformer",
    "get_models",
    "instantiate",
    "load_api_key",
    "set_defaults",
    "validate_endpoint",
    "validate_model_format",
    "validate_model_id",
]

# Provider registry - populated lazily
_PROVIDER_REGISTRY: dict[LLMProvider, type[BaseLLMProvider]] = {}

# ... [Keep all the existing functions: _lazy_import_provider, get_provider, list_providers] ...

# Enhance the existing __getattr__ to handle module access too
def __getattr__(name: str):
    """Handle dynamic attribute access for provider classes AND modules.

    This allows importing provider classes directly from the module
    while maintaining lazy loading and proper error messages.
    It also allows accessing provider modules like: providers.nvidia
    """
    # First check if it's a module name
    if name in _PROVIDER_MODULES:
        try:
            module = importlib.import_module(f".{name}", package=__name__)
            globals()[name] = module  # Cache it
            return module
        except ImportError as e:
            logger.debug(f"Failed to import provider module {name}: {e}")
            raise AttributeError(f"module '{__name__}' has no module '{name}'")

    # Then check if it's a class name (existing logic)
    class_to_provider = {
        "OpenAIProvider": LLMProvider.OPENAI,
        # ... [Keep all the existing class mappings] ...
    }

    if name in class_to_provider:
        # ... [Keep all the existing class loading logic] ...
        pass

    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
'''

print("The key changes needed:")
print("1. Move __all__ after the imports (Python style)")
print("2. Add _PROVIDER_MODULES list of module names")
print("3. Add module names to __all__ using *_PROVIDER_MODULES")
print("4. Enhance __getattr__ to handle module imports too")
print("\nThis allows:")
print("  from haive.core.models.llm.providers import nvidia")
print("  from haive.core.models.llm import providers")
print("  providers.nvidia  # Works!")
print(
    "  from haive.core.models.llm.providers.nvidia import NVIDIAProvider  # Still works!",
)
