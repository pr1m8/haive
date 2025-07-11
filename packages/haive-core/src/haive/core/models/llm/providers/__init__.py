"""LLM Providers Module.

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
   OpenAIProvider
   AnthropicProvider
   AzureOpenAIProvider
   GeminiProvider
   VertexAIProvider
   MistralProvider
   GroqProvider
   CohereProvider
"""

import logging
from typing import Dict, List, Optional, Type

from haive.core.models.llm.provider_types import LLMProvider
from haive.core.models.llm.providers.base import BaseLLMProvider, ProviderImportError

logger = logging.getLogger(__name__)

# Provider registry - populated lazily
_PROVIDER_REGISTRY: dict[LLMProvider, type[BaseLLMProvider]] = {}


def _lazy_import_provider(provider: LLMProvider) -> type[BaseLLMProvider] | None:
    """Lazily import a provider class.

    Args:
        provider: The provider to import

    Returns:
        The provider class, or None if import fails
    """
    # Check if already imported
    if provider in _PROVIDER_REGISTRY:
        return _PROVIDER_REGISTRY[provider]

    # Map providers to their modules
    provider_modules = {
        LLMProvider.OPENAI: "openai",
        LLMProvider.ANTHROPIC: "anthropic",
        LLMProvider.AZURE: "azure",
        LLMProvider.GEMINI: "google",
        LLMProvider.VERTEX_AI: "google",
        LLMProvider.MISTRALAI: "mistral",
        LLMProvider.GROQ: "groq",
        LLMProvider.COHERE: "cohere",
        LLMProvider.TOGETHER_AI: "together",
        LLMProvider.FIREWORKS_AI: "fireworks",
        LLMProvider.HUGGINGFACE: "huggingface",
        LLMProvider.AI21: "ai21",
        LLMProvider.BEDROCK: "bedrock",
        LLMProvider.NVIDIA: "nvidia",
        LLMProvider.OLLAMA: "ollama",
        LLMProvider.LLAMACPP: "llamacpp",
        LLMProvider.UPSTAGE: "upstage",
        LLMProvider.DATABRICKS: "databricks",
        LLMProvider.WATSONX: "watsonx",
        LLMProvider.XAI: "xai",
        LLMProvider.DEEPSEEK: "deepseek",
        LLMProvider.PERPLEXITY: "perplexity",
        LLMProvider.ALEPH_ALPHA: "aleph_alpha",
        LLMProvider.GOOSEAI: "gooseai",
        LLMProvider.MOSAICML: "mosaicml",
        LLMProvider.NLP_CLOUD: "nlp_cloud",
        LLMProvider.OPENLM: "openlm",
        LLMProvider.PETALS: "petals",
        LLMProvider.REPLICATE: "replicate",
    }

    # Map providers to their class names
    provider_classes = {
        LLMProvider.OPENAI: "OpenAIProvider",
        LLMProvider.ANTHROPIC: "AnthropicProvider",
        LLMProvider.AZURE: "AzureOpenAIProvider",
        LLMProvider.GEMINI: "GeminiProvider",
        LLMProvider.VERTEX_AI: "VertexAIProvider",
        LLMProvider.MISTRALAI: "MistralProvider",
        LLMProvider.GROQ: "GroqProvider",
        LLMProvider.COHERE: "CohereProvider",
        LLMProvider.TOGETHER_AI: "TogetherProvider",
        LLMProvider.FIREWORKS_AI: "FireworksProvider",
        LLMProvider.HUGGINGFACE: "HuggingFaceProvider",
        LLMProvider.AI21: "AI21Provider",
        LLMProvider.BEDROCK: "BedrockProvider",
        LLMProvider.NVIDIA: "NVIDIAProvider",
        LLMProvider.OLLAMA: "OllamaProvider",
        LLMProvider.LLAMACPP: "LlamaCppProvider",
        LLMProvider.UPSTAGE: "UpstageProvider",
        LLMProvider.DATABRICKS: "DatabricksProvider",
        LLMProvider.WATSONX: "WatsonxProvider",
        LLMProvider.XAI: "XAIProvider",
        LLMProvider.DEEPSEEK: "DeepSeekProvider",
        LLMProvider.PERPLEXITY: "PerplexityProvider",
        LLMProvider.ALEPH_ALPHA: "AlephAlphaProvider",
        LLMProvider.GOOSEAI: "GooseAIProvider",
        LLMProvider.MOSAICML: "MosaicMLProvider",
        LLMProvider.NLP_CLOUD: "NLPCloudProvider",
        LLMProvider.OPENLM: "OpenLMProvider",
        LLMProvider.PETALS: "PetalsProvider",
        LLMProvider.REPLICATE: "ReplicateProvider",
    }

    module_name = provider_modules.get(provider)
    class_name = provider_classes.get(provider)

    if not module_name or not class_name:
        logger.warning(f"No module mapping for provider: {provider}")
        return None

    try:
        # Dynamic import
        import importlib

        module = importlib.import_module(f".{module_name}", package=__name__)
        provider_class = getattr(module, class_name)

        # Cache for future use
        _PROVIDER_REGISTRY[provider] = provider_class

        return provider_class
    except ImportError as e:
        logger.debug(f"Failed to import {provider.value} provider: {e}")
        return None
    except AttributeError as e:
        logger.exception(
            f"Provider class {class_name} not found in module {module_name}: {e}"
        )
        return None


def get_provider(provider: LLMProvider) -> type[BaseLLMProvider]:
    """Get a provider class by enum value.

    Args:
        provider: The provider enum value

    Returns:
        The provider class

    Raises:
        ValueError: If provider is not supported
        ImportError: If provider dependencies are not installed
    """
    provider_class = _lazy_import_provider(provider)

    if provider_class is None:
        raise ValueError(
            f"Provider {provider.value} is not available or not implemented"
        )

    return provider_class


def list_providers() -> list[str]:
    """List all available provider names.

    Returns:
        List of provider names that can be imported
    """
    available = []

    for provider in LLMProvider:
        if _lazy_import_provider(provider) is not None:
            available.append(provider.value)

    return available


# Convenience imports with error handling
def __getattr__(name: str):
    """Handle dynamic attribute access for provider classes.

    This allows importing provider classes directly from the module
    while maintaining lazy loading and proper error messages.
    """
    # Map class names to providers
    class_to_provider = {
        "OpenAIProvider": LLMProvider.OPENAI,
        "AnthropicProvider": LLMProvider.ANTHROPIC,
        "AzureOpenAIProvider": LLMProvider.AZURE,
        "GeminiProvider": LLMProvider.GEMINI,
        "VertexAIProvider": LLMProvider.VERTEX_AI,
        "MistralProvider": LLMProvider.MISTRALAI,
        "GroqProvider": LLMProvider.GROQ,
        "CohereProvider": LLMProvider.COHERE,
        "TogetherProvider": LLMProvider.TOGETHER_AI,
        "FireworksProvider": LLMProvider.FIREWORKS_AI,
        "HuggingFaceProvider": LLMProvider.HUGGINGFACE,
        "AI21Provider": LLMProvider.AI21,
        "BedrockProvider": LLMProvider.BEDROCK,
        "NVIDIAProvider": LLMProvider.NVIDIA,
        "OllamaProvider": LLMProvider.OLLAMA,
        "LlamaCppProvider": LLMProvider.LLAMACPP,
        "UpstageProvider": LLMProvider.UPSTAGE,
        "DatabricksProvider": LLMProvider.DATABRICKS,
        "WatsonxProvider": LLMProvider.WATSONX,
        "XAIProvider": LLMProvider.XAI,
        "DeepSeekProvider": LLMProvider.DEEPSEEK,
        "PerplexityProvider": LLMProvider.PERPLEXITY,
        "AlephAlphaProvider": LLMProvider.ALEPH_ALPHA,
        "GooseAIProvider": LLMProvider.GOOSEAI,
        "MosaicMLProvider": LLMProvider.MOSAICML,
        "NLPCloudProvider": LLMProvider.NLP_CLOUD,
        "OpenLMProvider": LLMProvider.OPENLM,
        "PetalsProvider": LLMProvider.PETALS,
        "ReplicateProvider": LLMProvider.REPLICATE,
    }

    if name in class_to_provider:
        provider = class_to_provider[name]
        provider_class = _lazy_import_provider(provider)

        if provider_class is None:
            # Get the module name for better error message
            module_mapping = {
                LLMProvider.OPENAI: "langchain-openai",
                LLMProvider.ANTHROPIC: "langchain-anthropic",
                LLMProvider.AZURE: "langchain-openai",
                LLMProvider.GEMINI: "langchain-google-genai",
                LLMProvider.VERTEX_AI: "langchain-google-vertexai",
                LLMProvider.MISTRALAI: "langchain-mistralai",
                LLMProvider.GROQ: "langchain-groq",
                LLMProvider.COHERE: "langchain-cohere",
                LLMProvider.TOGETHER_AI: "langchain-together",
                LLMProvider.FIREWORKS_AI: "langchain-fireworks",
                LLMProvider.HUGGINGFACE: "langchain-huggingface",
                LLMProvider.AI21: "langchain-ai21",
                LLMProvider.BEDROCK: "langchain-aws",
                LLMProvider.NVIDIA: "langchain-nvidia-ai-endpoints",
                LLMProvider.OLLAMA: "langchain-ollama",
                LLMProvider.LLAMACPP: "langchain-community",
                LLMProvider.UPSTAGE: "langchain-upstage",
                LLMProvider.DATABRICKS: "langchain-databricks",
                LLMProvider.WATSONX: "langchain-ibm",
                LLMProvider.XAI: "langchain-xai",
            }

            package = module_mapping.get(provider, "unknown")
            raise ProviderImportError(
                provider=provider.value,
                package=package,
                message=f"{name} requires {package}. Install with: pip install {package}",
            )

        return provider_class

    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
