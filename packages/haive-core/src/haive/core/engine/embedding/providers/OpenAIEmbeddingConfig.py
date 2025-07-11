"""OpenAI embedding configuration."""

from typing import Any

from pydantic import Field, validator

from haive.core.engine.embedding.base import BaseEmbeddingConfig
from haive.core.engine.embedding.types import EmbeddingType


@BaseEmbeddingConfig.register(EmbeddingType.OPENAI)
class OpenAIEmbeddingConfig(BaseEmbeddingConfig):
    """Configuration for OpenAI embeddings.

    This configuration provides access to OpenAI's embedding models including
    the latest text-embedding-3-large and text-embedding-3-small models.

    Examples:
        Basic usage::

            config = OpenAIEmbeddingConfig(
                name="openai_embeddings",
                model="text-embedding-3-large",
                api_key="sk-..."
            )

            embeddings = config.instantiate()

        With custom dimensions::

            config = OpenAIEmbeddingConfig(
                name="openai_embeddings",
                model="text-embedding-3-large",
                dimensions=1536,
                api_key="sk-..."
            )

        Using environment variables::

            # Set OPENAI_API_KEY environment variable
            config = OpenAIEmbeddingConfig(
                name="openai_embeddings",
                model="text-embedding-3-large"
            )

    Attributes:
        embedding_type: Always EmbeddingType.OPENAI
        model: OpenAI model name (e.g., "text-embedding-3-large")
        api_key: OpenAI API key (auto-resolved from OPENAI_API_KEY env var)
        dimensions: Output dimensions (optional, model-dependent)
        max_retries: Maximum number of retries for API calls
        request_timeout: Timeout for API requests in seconds

    """

    embedding_type: EmbeddingType = Field(
        default=EmbeddingType.OPENAI, description="The embedding provider type"
    )

    # OpenAI-specific fields
    max_retries: int = Field(
        default=3, description="Maximum number of retries for API calls"
    )
    request_timeout: float | None = Field(
        default=None, description="Timeout for API requests in seconds"
    )
    base_url: str | None = Field(
        default=None, description="Base URL for OpenAI API (for custom endpoints)"
    )
    organization: str | None = Field(default=None, description="OpenAI organization ID")

    # SecureConfigMixin configuration
    provider: str = Field(
        default="openai", description="Provider name for API key resolution"
    )

    @validator("model")
    @classmethod
    def validate_model(cls, v):
        """Validate the OpenAI model name."""
        valid_models = {
            "text-embedding-3-large",
            "text-embedding-3-small",
            "text-embedding-ada-002",
            "text-embedding-ada-001",  # legacy
        }
        if v not in valid_models:
            # Log warning but don't fail - new models may be added
            import logging

            logger = logging.getLogger(__name__)
            logger.warning(
                f"Unknown OpenAI embedding model: {v}. Valid models: {valid_models}"
            )
        return v

    @validator("dimensions")
    @classmethod
    def validate_dimensions(cls, v, values):
        """Validate dimensions based on model."""
        if v is None:
            return v

        model = values.get("model")
        if model == "text-embedding-3-large" and v > 3072:
            raise ValueError("text-embedding-3-large maximum dimensions: 3072")
        if model == "text-embedding-3-small" and v > 1536:
            raise ValueError("text-embedding-3-small maximum dimensions: 1536")
        if model == "text-embedding-ada-002" and v != 1536:
            raise ValueError("text-embedding-ada-002 dimensions must be 1536")

        return v

    def instantiate(self) -> Any:
        """Create an OpenAI embeddings instance.

        Returns:
            OpenAIEmbeddings instance configured with the provided parameters

        Raises:
            ImportError: If langchain-openai is not installed
            ValueError: If configuration is invalid

        """
        try:
            from langchain_openai import OpenAIEmbeddings
        except ImportError:
            raise ImportError(
                "OpenAI embeddings require the langchain-openai package. "
                "Install with: pip install langchain-openai"
            )

        # Validate configuration
        self.validate_configuration()

        # Get API key
        api_key = self.get_api_key()
        if not api_key:
            raise ValueError(
                "OpenAI API key is required. Set OPENAI_API_KEY environment variable "
                "or provide api_key parameter."
            )

        # Build kwargs
        kwargs = {
            "model": self.model,
            "api_key": api_key,
            "max_retries": self.max_retries,
        }

        # Add optional parameters
        if self.request_timeout is not None:
            kwargs["timeout"] = self.request_timeout
        if self.base_url:
            kwargs["base_url"] = self.base_url
        if self.organization:
            kwargs["organization"] = self.organization
        if self.dimensions:
            kwargs["dimensions"] = self.dimensions

        return OpenAIEmbeddings(**kwargs)

    def get_default_model(self) -> str:
        """Get the default model for OpenAI embeddings."""
        return "text-embedding-3-large"

    def get_supported_models(self) -> list[str]:
        """Get list of supported OpenAI embedding models."""
        return [
            "text-embedding-3-large",
            "text-embedding-3-small",
            "text-embedding-ada-002",
            "text-embedding-ada-001",
        ]

    def get_model_info(self) -> dict:
        """Get information about the configured model."""
        model_info = {
            "text-embedding-3-large": {
                "dimensions": 3072,
                "max_dimensions": 3072,
                "context_length": 8192,
                "description": "Most capable OpenAI embedding model",
            },
            "text-embedding-3-small": {
                "dimensions": 1536,
                "max_dimensions": 1536,
                "context_length": 8192,
                "description": "Smaller, faster OpenAI embedding model",
            },
            "text-embedding-ada-002": {
                "dimensions": 1536,
                "max_dimensions": 1536,
                "context_length": 8192,
                "description": "Legacy OpenAI embedding model",
            },
            "text-embedding-ada-001": {
                "dimensions": 1024,
                "max_dimensions": 1024,
                "context_length": 2048,
                "description": "Legacy OpenAI embedding model",
            },
        }

        return model_info.get(
            self.model,
            {
                "dimensions": "unknown",
                "context_length": "unknown",
                "description": "OpenAI embedding model",
            },
        )
