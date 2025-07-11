"""Cohere embedding configuration."""

from typing import Any, Optional

from pydantic import Field, validator

from haive.core.engine.embedding.base import BaseEmbeddingConfig
from haive.core.engine.embedding.types import EmbeddingType


@BaseEmbeddingConfig.register(EmbeddingType.COHERE)
class CohereEmbeddingConfig(BaseEmbeddingConfig):
    """Configuration for Cohere embeddings.

    This configuration provides access to Cohere's embedding models including
    embed-english-v3.0, embed-multilingual-v3.0, and other specialized models.

    Examples:
        Basic usage::

            config = CohereEmbeddingConfig(
                name="cohere_embeddings",
                model="embed-english-v3.0",
                api_key="your-api-key"
            )

            embeddings = config.instantiate()

        With custom input type::

            config = CohereEmbeddingConfig(
                name="cohere_embeddings",
                model="embed-english-v3.0",
                input_type="search_document",
                api_key="your-api-key"
            )

        Using environment variables::

            # Set COHERE_API_KEY environment variable
            config = CohereEmbeddingConfig(
                name="cohere_embeddings",
                model="embed-english-v3.0"
            )

    Attributes:
        embedding_type: Always EmbeddingType.COHERE
        model: Cohere model name (e.g., "embed-english-v3.0")
        api_key: Cohere API key (auto-resolved from COHERE_API_KEY env var)
        input_type: Input type for embeddings (search_document, search_query, etc.)
        truncate: How to handle inputs longer than max length

    """

    embedding_type: EmbeddingType = Field(
        default=EmbeddingType.COHERE, description="The embedding provider type"
    )

    # Cohere-specific fields
    input_type: str | None = Field(
        default=None,
        description="Input type for embeddings (search_document, search_query, classification, clustering)",
    )
    truncate: str | None = Field(
        default=None,
        description="How to handle inputs longer than max length (NONE, START, END)",
    )
    max_retries: int = Field(
        default=3, description="Maximum number of retries for API calls"
    )
    request_timeout: float | None = Field(
        default=None, description="Timeout for API requests in seconds"
    )
    base_url: str | None = Field(
        default=None, description="Base URL for Cohere API (for custom endpoints)"
    )

    # SecureConfigMixin configuration
    provider: str = Field(
        default="cohere", description="Provider name for API key resolution"
    )

    @validator("model")
    @classmethod
    def validate_model(cls, v):
        """Validate the Cohere model name."""
        valid_models = {
            "embed-english-v3.0",
            "embed-multilingual-v3.0",
            "embed-english-light-v3.0",
            "embed-multilingual-light-v3.0",
            "embed-english-v2.0",
            "embed-multilingual-v2.0",
            "embed-english-light-v2.0",
            "embed-multilingual-light-v2.0",
        }
        if v not in valid_models:
            # Log warning but don't fail - new models may be added
            import logging

            logger = logging.getLogger(__name__)
            logger.warning(
                f"Unknown Cohere embedding model: {v}. Valid models: {valid_models}"
            )
        return v

    @validator("input_type")
    @classmethod
    def validate_input_type(cls, v):
        """Validate input type."""
        if v is None:
            return v

        valid_types = {
            "search_document",
            "search_query",
            "classification",
            "clustering",
        }

        if v not in valid_types:
            raise ValueError(f"Invalid input_type: {v}. Valid types: {valid_types}")

        return v

    @validator("truncate")
    @classmethod
    def validate_truncate(cls, v):
        """Validate truncate parameter."""
        if v is None:
            return v

        valid_options = {"NONE", "START", "END"}

        v = v.upper()
        if v not in valid_options:
            raise ValueError(f"Invalid truncate: {v}. Valid options: {valid_options}")

        return v

    def instantiate(self) -> Any:
        """Create a Cohere embeddings instance.

        Returns:
            CohereEmbeddings instance configured with the provided parameters

        Raises:
            ImportError: If langchain-cohere is not installed
            ValueError: If configuration is invalid

        """
        try:
            from langchain_cohere import CohereEmbeddings
        except ImportError:
            raise ImportError(
                "Cohere embeddings require the langchain-cohere package. "
                "Install with: pip install langchain-cohere"
            )

        # Validate configuration
        self.validate_configuration()

        # Get API key
        api_key = self.get_api_key()
        if not api_key:
            raise ValueError(
                "Cohere API key is required. Set COHERE_API_KEY environment variable "
                "or provide api_key parameter."
            )

        # Build kwargs
        kwargs = {
            "model": self.model,
            "cohere_api_key": api_key,
            "max_retries": self.max_retries,
        }

        # Add optional parameters
        if self.input_type:
            kwargs["input_type"] = self.input_type
        if self.truncate:
            kwargs["truncate"] = self.truncate
        if self.request_timeout:
            kwargs["request_timeout"] = self.request_timeout
        if self.base_url:
            kwargs["base_url"] = self.base_url

        return CohereEmbeddings(**kwargs)

    def get_default_model(self) -> str:
        """Get the default model for Cohere embeddings."""
        return "embed-english-v3.0"

    def get_supported_models(self) -> list[str]:
        """Get list of supported Cohere embedding models."""
        return [
            "embed-english-v3.0",
            "embed-multilingual-v3.0",
            "embed-english-light-v3.0",
            "embed-multilingual-light-v3.0",
            "embed-english-v2.0",
            "embed-multilingual-v2.0",
            "embed-english-light-v2.0",
            "embed-multilingual-light-v2.0",
        ]

    def get_model_info(self) -> dict:
        """Get information about the configured model."""
        model_info = {
            "embed-english-v3.0": {
                "dimensions": 1024,
                "max_input_tokens": 512,
                "languages": ["English"],
                "description": "Latest English embedding model with high performance",
            },
            "embed-multilingual-v3.0": {
                "dimensions": 1024,
                "max_input_tokens": 512,
                "languages": ["100+ languages"],
                "description": "Latest multilingual embedding model",
            },
            "embed-english-light-v3.0": {
                "dimensions": 384,
                "max_input_tokens": 512,
                "languages": ["English"],
                "description": "Lightweight English embedding model",
            },
            "embed-multilingual-light-v3.0": {
                "dimensions": 384,
                "max_input_tokens": 512,
                "languages": ["100+ languages"],
                "description": "Lightweight multilingual embedding model",
            },
            "embed-english-v2.0": {
                "dimensions": 4096,
                "max_input_tokens": 512,
                "languages": ["English"],
                "description": "Previous generation English embedding model",
            },
            "embed-multilingual-v2.0": {
                "dimensions": 768,
                "max_input_tokens": 512,
                "languages": ["100+ languages"],
                "description": "Previous generation multilingual embedding model",
            },
        }

        return model_info.get(
            self.model,
            {
                "dimensions": "unknown",
                "max_input_tokens": "unknown",
                "languages": "unknown",
                "description": "Cohere embedding model",
            },
        )

    def get_input_types(self) -> list[str]:
        """Get list of supported input types."""
        return ["search_document", "search_query", "classification", "clustering"]

    def get_truncate_options(self) -> list[str]:
        """Get list of supported truncate options."""
        return ["NONE", "START", "END"]
