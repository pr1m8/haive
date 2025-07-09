"""LLM Factory Module for Haive Framework.

This module provides a universal factory pattern for creating Language Model instances
from various providers with a consistent interface. It supports dynamic provider detection,
optional dependency handling, and rate limiting capabilities.

The factory pattern allows for clean instantiation of LLMs from 20+ different providers
including OpenAI, Anthropic, Google, AWS, and many others, with automatic configuration
and error handling.

Examples:
    Basic usage with provider enum::

        from haive.core.models.llm.factory import create_llm
        from haive.core.models.llm.provider_types import LLMProvider

        # Create an OpenAI model
        llm = create_llm(
            provider=LLMProvider.OPENAI,
            model="gpt-4",
            api_key="your-api-key"
        )

    Using string provider name::

        # Provider can also be specified as string
        llm = create_llm(
            provider="anthropic",
            model="claude-3-opus-20240229",
            rate_limiting={"requests_per_second": 10}
        )

    With rate limiting::

        # Add rate limiting to any provider
        llm = create_llm(
            provider=LLMProvider.GROQ,
            model="llama3-70b-8192",
            requests_per_second=5,
            tokens_per_minute=10000
        )

Module Structure:
    - :class:`LLMFactory`: Main factory class for creating LLM instances
    - :func:`create_llm`: Convenience function for creating LLMs
    - :func:`get_available_providers`: List all available providers
    - :func:`get_provider_models`: Get available models for a provider

.. autosummary::
   :toctree: generated/

   LLMFactory
   create_llm
   get_available_providers
   get_provider_models
"""

import logging
import os
from typing import Any, Dict, List, Optional, Type, Union

from pydantic import BaseModel, Field

from haive.core.models.llm.provider_types import LLMProvider
from haive.core.models.llm.providers import get_provider, list_providers
from haive.core.models.llm.providers.base import BaseLLMProvider, ProviderImportError

logger = logging.getLogger(__name__)


class LLMFactory:
    """Factory class for creating Language Model instances.

    This class provides a centralized way to create LLM instances from various
    providers with consistent configuration and error handling. It supports
    dynamic import of provider-specific dependencies and graceful fallback
    when dependencies are not installed.

    The factory maintains a registry of provider configurations and handles
    the complexity of instantiating models with provider-specific parameters
    while presenting a unified interface.

    Attributes:
        _provider_configs: Internal registry mapping providers to config classes
        _provider_imports: Internal registry of required imports per provider

    Examples:
        Creating models from different providers::

            factory = LLMFactory()

            # OpenAI
            openai_llm = factory.create(
                provider=LLMProvider.OPENAI,
                model="gpt-4",
                temperature=0.7
            )

            # Anthropic with rate limiting
            anthropic_llm = factory.create(
                provider=LLMProvider.ANTHROPIC,
                model="claude-3-opus-20240229",
                requests_per_second=10
            )

            # Local Ollama model
            ollama_llm = factory.create(
                provider=LLMProvider.OLLAMA,
                model="llama3",
                base_url="http://localhost:11434"
            )
    """

    def __init__(self):
        """Initialize the LLM Factory."""
        # No need for internal registries - we use the providers module

    def create(
        self, provider: Union[LLMProvider, str], model: Optional[str] = None, **kwargs
    ) -> Any:
        """Create an LLM instance for the specified provider.

        This method creates and configures an LLM instance based on the provider
        and parameters. It handles provider-specific configuration, optional
        imports, and rate limiting if specified.

        Args:
            provider: The LLM provider (enum or string)
            model: The model name/ID (provider-specific)
            **kwargs: Additional configuration parameters including:
                - api_key: API key for the provider
                - temperature: Sampling temperature
                - max_tokens: Maximum tokens to generate
                - requests_per_second: Rate limiting parameter
                - tokens_per_minute: Rate limiting parameter
                - Any provider-specific parameters

        Returns:
            Configured LLM instance ready for use

        Raises:
            ValueError: If provider is not supported or required config missing
            ImportError: If provider dependencies are not installed
            RuntimeError: If LLM instantiation fails

        Examples:
            Basic creation::

                llm = factory.create(
                    provider="openai",
                    model="gpt-4",
                    temperature=0.7
                )

            With rate limiting::

                llm = factory.create(
                    provider=LLMProvider.ANTHROPIC,
                    model="claude-3-sonnet-20240229",
                    api_key="your-key",
                    requests_per_second=10,
                    tokens_per_minute=100000
                )
        """
        # Convert string to enum if needed
        if isinstance(provider, str):
            try:
                provider = LLMProvider(provider.lower())
            except ValueError:
                raise ValueError(
                    f"Unknown provider: {provider}. "
                    f"Available providers: {', '.join([p.value for p in LLMProvider])}"
                )

        # Get provider class
        try:
            provider_class = get_provider(provider)
        except (ValueError, ImportError) as e:
            raise ValueError(f"Provider {provider} not available: {str(e)}")

        # Extract rate limiting parameters
        rate_limit_params = {}
        for param in [
            "requests_per_second",
            "tokens_per_second",
            "tokens_per_minute",
            "max_retries",
            "retry_delay",
            "check_every_n_seconds",
            "burst_size",
        ]:
            if param in kwargs:
                rate_limit_params[param] = kwargs.pop(param)

        # Create provider instance with all parameters
        provider_params = {}
        if model:
            provider_params["model"] = model
        provider_params.update(kwargs)
        provider_params.update(rate_limit_params)

        try:
            provider_instance = provider_class(**provider_params)
        except Exception as e:
            raise ValueError(f"Failed to create provider for {provider}: {str(e)}")

        # Create LLM instance
        try:
            llm = provider_instance.instantiate()
        except ProviderImportError:
            # Re-raise with original clear message
            raise
        except Exception as e:
            raise RuntimeError(
                f"Failed to create {provider.value} LLM: {str(e)}"
            ) from e

        return llm

    def get_available_providers(self) -> List[str]:
        """Get list of all available LLM providers.

        Returns:
            List of provider names as strings

        Examples:
            List available providers::

                factory = LLMFactory()
                providers = factory.get_available_providers()
                print(providers)
                # ['openai', 'anthropic', 'azure', ...]
        """
        return list_providers()

    def get_provider_info(self, provider: Union[LLMProvider, str]) -> Dict[str, Any]:
        """Get information about a specific provider.

        Args:
            provider: The provider to get info for

        Returns:
            Dictionary containing provider information including:
                - name: Provider name
                - config_class: Configuration class name
                - import_required: Required import package
                - available: Whether dependencies are installed

        Examples:
            Get provider information::

                info = factory.get_provider_info("openai")
                print(info)
                # {
                #     'name': 'openai',
                #     'config_class': 'OpenAILLMConfig',
                #     'import_required': 'langchain-openai',
                #     'available': True
                # }
        """
        # Convert string to enum if needed
        if isinstance(provider, str):
            try:
                provider = LLMProvider(provider.lower())
            except ValueError:
                raise ValueError(f"Unknown provider: {provider}")

        # Try to get the provider class
        try:
            provider_class = get_provider(provider)
            available = True
            class_name = provider_class.__name__
        except (ValueError, ImportError):
            available = False
            class_name = "Not Implemented"

        # Get package info from provider if available
        if available:
            try:
                temp_instance = provider_class()
                package = temp_instance._get_import_package()
            except:
                package = "Unknown"
        else:
            package = "Unknown"

        return {
            "name": provider.value,
            "config_class": class_name,
            "import_required": package,
            "available": available,
        }


# Convenience functions
_factory = LLMFactory()


def create_llm(
    provider: Union[LLMProvider, str], model: Optional[str] = None, **kwargs
) -> Any:
    """Create an LLM instance using the global factory.

    This is a convenience function that uses a global LLMFactory instance
    to create LLM instances. It provides a simpler interface for common use cases.

    Args:
        provider: The LLM provider (enum or string)
        model: The model name/ID (provider-specific)
        **kwargs: Additional configuration parameters

    Returns:
        Configured LLM instance

    Raises:
        ValueError: If provider is not supported
        ImportError: If provider dependencies are not installed
        RuntimeError: If LLM instantiation fails

    Examples:
        Create OpenAI model::

            llm = create_llm("openai", "gpt-4", temperature=0.7)

        Create Anthropic model with rate limiting::

            llm = create_llm(
                provider=LLMProvider.ANTHROPIC,
                model="claude-3-opus-20240229",
                requests_per_second=5
            )

        Create local Ollama model::

            llm = create_llm("ollama", "llama3", base_url="http://localhost:11434")
    """
    return _factory.create(provider=provider, model=model, **kwargs)


def get_available_providers() -> List[str]:
    """Get list of all available LLM providers.

    Returns:
        List of provider names as strings

    Examples:
        List providers::

            providers = get_available_providers()
            print(f"Available providers: {', '.join(providers)}")
    """
    return list_providers()


def get_provider_models(provider: Union[LLMProvider, str]) -> List[str]:
    """Get available models for a specific provider.

    This function attempts to retrieve the list of available models
    from the provider's API. Not all providers support this functionality.

    Args:
        provider: The provider to get models for

    Returns:
        List of available model names

    Raises:
        ValueError: If provider is not supported
        NotImplementedError: If provider doesn't support listing models

    Examples:
        Get OpenAI models::

            models = get_provider_models("openai")
            print(f"OpenAI models: {models}")
    """
    # Convert string to enum if needed
    if isinstance(provider, str):
        try:
            provider = LLMProvider(provider.lower())
        except ValueError:
            raise ValueError(f"Unknown provider: {provider}")

    # Get provider class
    try:
        provider_class = get_provider(provider)
    except (ValueError, ImportError) as e:
        raise ValueError(f"Provider {provider} not available: {str(e)}")

    # Check if get_models method exists
    if hasattr(provider_class, "get_models"):
        try:
            return provider_class.get_models()
        except Exception as e:
            logger.warning(f"Failed to get models for {provider}: {str(e)}")
            raise
    else:
        raise NotImplementedError(
            f"Provider {provider.value} does not support listing models"
        )
