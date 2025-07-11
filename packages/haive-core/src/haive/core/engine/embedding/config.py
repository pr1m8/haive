"""Embedding configuration factory and utilities."""

import logging
from typing import Any, Dict, Union

from .base import BaseEmbeddingConfig
from .types import EmbeddingType

logger = logging.getLogger(__name__)


class EmbeddingConfigFactory:
    """Factory class for creating embedding configurations.

    This factory provides a convenient way to create embedding configurations
    without needing to import specific provider classes.

    Examples:
        Create OpenAI configuration::

            factory = EmbeddingConfigFactory()
            config = factory.create(
                provider="OpenAI",
                model="text-embedding-3-large",
                name="my_embeddings"
            )

        List available providers::

            factory = EmbeddingConfigFactory()
            providers = factory.list_providers()

        Get provider information::

            factory = EmbeddingConfigFactory()
            info = factory.get_provider_info("OpenAI")

    """

    @staticmethod
    def create(
        provider: str | EmbeddingType,
        model: str,
        name: str = "default_embedding",
        **kwargs,
    ) -> BaseEmbeddingConfig:
        """Create an embedding configuration.

        Args:
            provider: Provider name or EmbeddingType enum
            model: Model name for the provider
            name: Configuration name
            **kwargs: Additional provider-specific parameters

        Returns:
            Configured embedding instance

        Raises:
            ValueError: If provider is not found or configuration is invalid

        Examples:
            Create OpenAI config::

                config = EmbeddingConfigFactory.create(
                    provider="OpenAI",
                    model="text-embedding-3-large",
                    api_key="sk-..."
                )

            Create HuggingFace config::

                config = EmbeddingConfigFactory.create(
                    provider="HuggingFace",
                    model="sentence-transformers/all-MiniLM-L6-v2",
                    use_cache=True
                )

        """
        # Convert string to EmbeddingType if needed
        if isinstance(provider, str):
            try:
                provider_enum = EmbeddingType(provider)
            except ValueError:
                # Try to find by name
                provider_enum = None
                for enum_val in EmbeddingType:
                    if enum_val.value == provider:
                        provider_enum = enum_val
                        break
                if provider_enum is None:
                    available = [e.value for e in EmbeddingType]
                    raise ValueError(
                        f"Unknown provider: {provider}. Available: {available}"
                    )
        else:
            provider_enum = provider

        # Get the configuration class
        config_class = BaseEmbeddingConfig.get_config_class(provider_enum)
        if config_class is None:
            raise ValueError(
                f"No configuration class found for provider: {provider_enum}"
            )

        # Create configuration
        try:
            config = config_class(name=name, model=model, **kwargs)
            return config
        except Exception as e:
            raise ValueError(f"Failed to create {provider_enum} configuration: {e}")

    @staticmethod
    def list_providers() -> list[str]:
        """List all available embedding providers.

        Returns:
            List of provider names

        """
        registered = BaseEmbeddingConfig.list_registered_types()
        return list(registered.keys())

    @staticmethod
    def get_provider_info(provider: str | EmbeddingType) -> dict[str, Any]:
        """Get information about a specific provider.

        Args:
            provider: Provider name or EmbeddingType enum

        Returns:
            Dictionary with provider information

        """
        # Convert to string for lookup
        provider_str = str(provider.value if hasattr(provider, "value") else provider)

        config_class = BaseEmbeddingConfig.get_config_class(provider_str)
        if config_class is None:
            return {}

        # Get basic information without instantiation to avoid dependency issues
        info = {
            "provider": provider_str,
            "class": config_class.__name__,
            "description": (
                config_class.__doc__.split("\n")[0]
                if config_class.__doc__
                else "Embedding provider configuration"
            ),
            "supported_models": [],
            "default_model": "unknown",
        }

        # Try to get additional info from class methods if available
        try:
            # Some methods might be available as class methods or static methods
            if hasattr(config_class, "get_supported_models"):
                method = config_class.get_supported_models
                if callable(method):
                    try:
                        models = method()
                        if isinstance(models, list):
                            info["supported_models"] = models
                    except:
                        pass

            if hasattr(config_class, "get_default_model"):
                method = config_class.get_default_model
                if callable(method):
                    try:
                        default = method()
                        if isinstance(default, str):
                            info["default_model"] = default
                    except:
                        pass
        except Exception:
            pass

        return info

    @staticmethod
    def validate_provider(provider: str | EmbeddingType) -> bool:
        """Check if a provider is available.

        Args:
            provider: Provider name or EmbeddingType enum

        Returns:
            True if provider is available, False otherwise

        """
        try:
            provider_str = str(
                provider.value if hasattr(provider, "value") else provider
            )
            config_class = BaseEmbeddingConfig.get_config_class(provider_str)
            return config_class is not None
        except Exception:
            return False


def create_embedding_config(
    provider: str | EmbeddingType,
    model: str,
    name: str = "default_embedding",
    **kwargs,
) -> BaseEmbeddingConfig:
    """Create an embedding configuration using the factory.

    This is a convenience function that wraps EmbeddingConfigFactory.create().

    Args:
        provider: Provider name or EmbeddingType enum
        model: Model name for the provider
        name: Configuration name
        **kwargs: Additional provider-specific parameters

    Returns:
        Configured embedding instance

    Examples:
        Create OpenAI config::

            config = create_embedding_config(
                provider="OpenAI",
                model="text-embedding-3-large"
            )

        Create with custom parameters::

            config = create_embedding_config(
                provider="HuggingFace",
                model="sentence-transformers/all-MiniLM-L6-v2",
                use_cache=True,
                cache_folder="./my_cache"
            )

    """
    return EmbeddingConfigFactory.create(
        provider=provider, model=model, name=name, **kwargs
    )


def list_embedding_providers() -> list[str]:
    """List all available embedding providers.

    Returns:
        List of provider names

    Examples:
        List providers::

            providers = list_embedding_providers()
            print(f"Available: {providers}")

    """
    return EmbeddingConfigFactory.list_providers()


def get_embedding_provider_info(provider: str | EmbeddingType) -> dict[str, Any]:
    """Get information about an embedding provider.

    Args:
        provider: Provider name or EmbeddingType enum

    Returns:
        Dictionary with provider information

    Examples:
        Get provider info::

            info = get_embedding_provider_info("OpenAI")
            print(f"Default model: {info['default_model']}")
            print(f"Supported models: {info['supported_models']}")

    """
    return EmbeddingConfigFactory.get_provider_info(provider)


def validate_embedding_provider(provider: str | EmbeddingType) -> bool:
    """Check if an embedding provider is available.

    Args:
        provider: Provider name or EmbeddingType enum

    Returns:
        True if provider is available, False otherwise

    Examples:
        Check provider availability::

            if validate_embedding_provider("OpenAI"):
                print("OpenAI provider is available")
            else:
                print("OpenAI provider not found")

    """
    return EmbeddingConfigFactory.validate_provider(provider)
