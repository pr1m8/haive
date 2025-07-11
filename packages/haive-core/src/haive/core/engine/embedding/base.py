"""Base embedding engine configuration and registry."""

import logging
from abc import abstractmethod
from typing import Any, Dict, Optional, Type, Union

from pydantic import Field, SecretStr

from haive.core.common.mixins.secure_config import SecureConfigMixin
from haive.core.engine.base import InvokableEngine
from haive.core.engine.base.types import EngineType
from haive.core.engine.embedding.types import EmbeddingType

logger = logging.getLogger(__name__)

# Global registry to avoid Pydantic conflicts
_EMBEDDING_REGISTRY: dict[str, type["BaseEmbeddingConfig"]] = {}


class BaseEmbeddingConfig(SecureConfigMixin, InvokableEngine):
    """Base configuration for all embedding implementations.

    This class provides the foundation for all embedding provider configurations
    in the Haive framework. It includes registration capabilities, secure configuration
    management, and the required interface for creating embedding instances.

    Examples:
        Basic usage with a provider::

            from haive.core.engine.embedding.providers import OpenAIEmbeddingConfig

            config = OpenAIEmbeddingConfig(
                name="my_embeddings",
                model="text-embedding-3-large",
                api_key="sk-..."
            )

            embeddings = config.instantiate()

        Using with configuration discovery::

            # List all available providers
            providers = BaseEmbeddingConfig.list_registered_types()

            # Get specific provider class
            provider_class = BaseEmbeddingConfig.get_config_class(EmbeddingType.OPENAI)

    Attributes:
        embedding_type: The type of embedding provider
        name: Human-readable name for this configuration
        model: Model name/identifier for the embedding provider
        dimensions: Optional output dimensions for the embeddings

    """

    # Required by base Engine class
    engine_type: EngineType = Field(
        default=EngineType.EMBEDDINGS,
        description="Engine type - always EMBEDDINGS for embedding providers",
    )

    # Embedding-specific fields
    embedding_type: EmbeddingType = Field(
        ..., description="The specific embedding provider type"
    )
    model: str = Field(
        ..., description="Model name/identifier for the embedding provider"
    )
    dimensions: int | None = Field(
        default=None, description="Output dimensions for the embeddings (if supported)"
    )

    # API key field for SecureConfigMixin
    api_key: SecretStr | None = Field(
        default=None, description="API key for the embedding provider"
    )

    @classmethod
    def register(cls, embedding_type: str | EmbeddingType) -> Any:
        """Register an embedding configuration class.

        This decorator registers embedding configuration classes with the global
        registry, allowing them to be discovered and instantiated dynamically.

        Args:
            embedding_type: The embedding type to register this class for

        Returns:
            The decorator function

        Examples:
            Registering a new provider::

                @BaseEmbeddingConfig.register(EmbeddingType.OPENAI)
                class OpenAIEmbeddingConfig(BaseEmbeddingConfig):
                    # Implementation here
                    pass

        """

        def decorator(
            config_cls: type["BaseEmbeddingConfig"],
        ) -> type["BaseEmbeddingConfig"]:
            type_str = str(
                embedding_type.value
                if hasattr(embedding_type, "value")
                else embedding_type
            )
            _EMBEDDING_REGISTRY[type_str] = config_cls
            logger.info(
                f"Registered embedding config: {config_cls.__name__} as {type_str}"
            )
            return config_cls

        return decorator

    @classmethod
    def get_config_class(
        cls, embedding_type: str | EmbeddingType
    ) -> type["BaseEmbeddingConfig"] | None:
        """Get the configuration class for a specific embedding type.

        Args:
            embedding_type: The embedding type to get the config class for

        Returns:
            The configuration class if found, None otherwise

        Examples:
            Getting a provider class::

                config_class = BaseEmbeddingConfig.get_config_class(EmbeddingType.OPENAI)
                if config_class:
                    config = config_class(model="text-embedding-3-large")

        """
        type_str = str(
            embedding_type.value if hasattr(embedding_type, "value") else embedding_type
        )
        return _EMBEDDING_REGISTRY.get(type_str)

    @classmethod
    def list_registered_types(cls) -> dict[str, type["BaseEmbeddingConfig"]]:
        """List all registered embedding configuration types.

        Returns:
            Dictionary mapping type names to configuration classes

        Examples:
            Listing all providers::

                providers = BaseEmbeddingConfig.list_registered_types()
                for name, config_class in providers.items():
                    print(f"Available provider: {name}")

        """
        return _EMBEDDING_REGISTRY.copy()

    @abstractmethod
    def instantiate(self) -> Any:
        """Create an embedding instance from this configuration.

        This method must be implemented by each provider-specific configuration
        class to create the actual embedding instance.

        Returns:
            The embedding instance (typically a LangChain embedding object)

        Raises:
            NotImplementedError: If not implemented by subclass
            ImportError: If required dependencies are not installed
            ValueError: If configuration is invalid

        Examples:
            Implementing instantiate method::

                def instantiate(self) -> OpenAIEmbeddings:
                    try:
                        from langchain_openai import OpenAIEmbeddings
                    except ImportError:
                        raise ImportError("Install: pip install langchain-openai")

                    return OpenAIEmbeddings(
                        model=self.model,
                        api_key=self.get_api_key()
                    )

        """
        raise NotImplementedError("Subclasses must implement instantiate()")

    def get_input_fields(self) -> dict[str, tuple]:
        """Define the input schema for this embedding configuration.

        Returns:
            Dictionary mapping field names to (type, Field) tuples

        """
        return {
            "text": (str, Field(description="Text to embed")),
            "documents": (
                list,
                Field(description="List of documents to embed", default=None),
            ),
        }

    def get_output_fields(self) -> dict[str, tuple]:
        """Define the output schema for this embedding configuration.

        Returns:
            Dictionary mapping field names to (type, Field) tuples

        """
        return {
            "embeddings": (list, Field(description="List of embedding vectors")),
            "dimensions": (int, Field(description="Embedding vector dimensions")),
        }

    def validate_configuration(self) -> None:
        """Validate the configuration before instantiation.

        This method can be overridden by subclasses to add provider-specific
        validation logic.

        Raises:
            ValueError: If configuration is invalid

        """
        if not self.model:
            raise ValueError("Model name is required")

    def create_runnable(self, runnable_config: dict[str, Any] | None = None) -> Any:
        """Create a runnable embedding instance.

        This method is required by the InvokableEngine interface and provides
        a standardized way to create embedding instances.

        Args:
            runnable_config: Optional configuration for the runnable

        Returns:
            The embedding instance

        """
        return self.instantiate()

    def get_provider_info(self) -> dict[str, Any]:
        """Get information about this embedding provider.

        Returns:
            Dictionary containing provider information

        """
        return {
            "provider": self.embedding_type,
            "name": self.name,
            "model": self.model,
            "dimensions": self.dimensions,
            "class": self.__class__.__name__,
        }
