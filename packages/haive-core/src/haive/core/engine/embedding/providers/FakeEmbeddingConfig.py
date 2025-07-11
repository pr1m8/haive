"""Fake embedding configuration for testing."""

from typing import Any

from pydantic import Field, validator

from haive.core.engine.embedding.base import BaseEmbeddingConfig
from haive.core.engine.embedding.types import EmbeddingType


@BaseEmbeddingConfig.register(EmbeddingType.FAKE)
class FakeEmbeddingConfig(BaseEmbeddingConfig):
    """Configuration for fake embeddings (testing purposes).

    This configuration provides fake embeddings for testing and development
    purposes. It generates random embeddings without requiring external APIs.

    Examples:
        Basic usage::

            config = FakeEmbeddingConfig(
                name="fake_embeddings",
                model="fake-model",
                size=768
            )

            embeddings = config.instantiate()

        With custom dimensions::

            config = FakeEmbeddingConfig(
                name="fake_embeddings",
                model="fake-model",
                size=1024
            )

    Attributes:
        embedding_type: Always EmbeddingType.FAKE
        model: Fake model name (can be any string)
        size: Dimension of the fake embeddings

    """

    embedding_type: EmbeddingType = Field(
        default=EmbeddingType.FAKE, description="The embedding provider type"
    )

    # Fake embedding specific fields
    size: int = Field(default=768, description="Dimension of the fake embeddings")

    # SecureConfigMixin configuration (not needed for fake embeddings)
    provider: str = Field(
        default="fake", description="Provider name for API key resolution"
    )

    @validator("size")
    @classmethod
    def validate_size(cls, v):
        """Validate embedding size."""
        if v <= 0:
            raise ValueError("Embedding size must be positive")
        if v > 4096:
            raise ValueError("Embedding size too large (max 4096)")
        return v

    @validator("model")
    @classmethod
    def validate_model(cls, v):
        """Validate fake model name."""
        if not v or not v.strip():
            raise ValueError("Model name is required")
        return v.strip()

    def instantiate(self) -> Any:
        """Create a fake embeddings instance.

        Returns:
            FakeEmbeddings instance configured with the provided parameters

        Raises:
            ImportError: If langchain-community is not installed
            ValueError: If configuration is invalid

        """
        try:
            from langchain_community.embeddings import FakeEmbeddings
        except ImportError:
            raise ImportError(
                "Fake embeddings require the langchain-community package. "
                "Install with: pip install langchain-community"
            )

        # Validate configuration
        self.validate_configuration()

        # Build kwargs
        kwargs = {
            "size": self.size,
        }

        return FakeEmbeddings(**kwargs)

    def get_default_model(self) -> str:
        """Get the default model for fake embeddings."""
        return "fake-model"

    def get_supported_models(self) -> list[str]:
        """Get list of supported fake embedding models."""
        return ["fake-model", "fake-small", "fake-large", "fake-test"]

    def get_model_info(self) -> dict:
        """Get information about the configured model."""
        return {
            "dimensions": self.size,
            "description": "Fake embedding model for testing",
            "provider": "fake",
            "cost": 0.0,
        }
