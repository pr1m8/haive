"""Google Vertex AI embedding configuration."""

from typing import Any

from pydantic import Field, validator

from haive.core.engine.embedding.base import BaseEmbeddingConfig
from haive.core.engine.embedding.types import EmbeddingType


@BaseEmbeddingConfig.register(EmbeddingType.GOOGLE_VERTEX_AI)
class GoogleVertexAIEmbeddingConfig(BaseEmbeddingConfig):
    """Configuration for Google Vertex AI embeddings.

    This configuration provides access to Google's Vertex AI embedding models
    including text-embedding-004, text-multilingual-embedding-002, and others.

    Examples:
        Basic usage::

            config = GoogleVertexAIEmbeddingConfig(
                name="vertex_embeddings",
                model="text-embedding-004",
                project="your-project-id",
                location="us-central1"
            )

            embeddings = config.instantiate()

        With custom task type::

            config = GoogleVertexAIEmbeddingConfig(
                name="vertex_embeddings",
                model="text-embedding-004",
                project="your-project-id",
                location="us-central1",
                task_type="SEMANTIC_SIMILARITY"
            )

        Using service account::

            config = GoogleVertexAIEmbeddingConfig(
                name="vertex_embeddings",
                model="text-embedding-004",
                project="your-project-id",
                location="us-central1",
                credentials_path="/path/to/service-account.json"
            )

    Attributes:
        embedding_type: Always EmbeddingType.GOOGLE_VERTEX_AI
        model: Vertex AI model name (e.g., "text-embedding-004")
        project: Google Cloud project ID
        location: Google Cloud location/region
        task_type: Task type for embeddings
        credentials_path: Path to service account credentials

    """

    embedding_type: EmbeddingType = Field(
        default=EmbeddingType.GOOGLE_VERTEX_AI,
        description="The embedding provider type",
    )

    # Google Vertex AI specific fields
    project: str = Field(..., description="Google Cloud project ID")
    location: str = Field(
        default="us-central1", description="Google Cloud location/region"
    )
    task_type: str | None = Field(
        default=None,
        description="Task type for embeddings (RETRIEVAL_QUERY, RETRIEVAL_DOCUMENT, etc.)",
    )
    title: str | None = Field(default=None, description="Title for the embedding task")
    credentials_path: str | None = Field(
        default=None, description="Path to service account credentials JSON file"
    )
    max_retries: int = Field(
        default=3, description="Maximum number of retries for API calls"
    )
    request_timeout: float | None = Field(
        default=None, description="Timeout for API requests in seconds"
    )

    # SecureConfigMixin configuration
    provider: str = Field(
        default="google", description="Provider name for API key resolution"
    )

    @validator("model")
    @classmethod
    def validate_model(cls, v):
        """Validate the Vertex AI model name."""
        valid_models = {
            "text-embedding-004",
            "text-multilingual-embedding-002",
            "text-embedding-preview-0409",
            "text-multilingual-embedding-preview-0409",
            "textembedding-gecko@001",
            "textembedding-gecko@003",
            "textembedding-gecko-multilingual@001",
        }
        if v not in valid_models:
            # Log warning but don't fail - new models may be added
            import logging

            logger = logging.getLogger(__name__)
            logger.warning(
                f"Unknown Vertex AI embedding model: {v}. Valid models: {valid_models}"
            )
        return v

    @validator("task_type")
    @classmethod
    def validate_task_type(cls, v):
        """Validate task type."""
        if v is None:
            return v

        valid_types = {
            "RETRIEVAL_QUERY",
            "RETRIEVAL_DOCUMENT",
            "SEMANTIC_SIMILARITY",
            "CLASSIFICATION",
            "CLUSTERING",
        }

        if v not in valid_types:
            raise ValueError(f"Invalid task_type: {v}. Valid types: {valid_types}")

        return v

    @validator("location")
    @classmethod
    def validate_location(cls, v):
        """Validate Google Cloud location."""
        if not v or not v.strip():
            raise ValueError("Location is required")
        return v.strip()

    @validator("project")
    @classmethod
    def validate_project(cls, v):
        """Validate Google Cloud project ID."""
        if not v or not v.strip():
            raise ValueError("Project ID is required")
        return v.strip()

    def instantiate(self) -> Any:
        """Create a Google Vertex AI embeddings instance.

        Returns:
            VertexAIEmbeddings instance configured with the provided parameters

        Raises:
            ImportError: If langchain-google-vertexai is not installed
            ValueError: If configuration is invalid

        """
        try:
            from langchain_google_vertexai import VertexAIEmbeddings
        except ImportError:
            raise ImportError(
                "Google Vertex AI embeddings require the langchain-google-vertexai package. "
                "Install with: pip install langchain-google-vertexai"
            )

        # Validate configuration
        self.validate_configuration()

        # Build kwargs
        kwargs = {
            "model_name": self.model,
            "project": self.project,
            "location": self.location,
            "max_retries": self.max_retries,
        }

        # Add optional parameters
        if self.task_type:
            kwargs["task_type"] = self.task_type
        if self.title:
            kwargs["title"] = self.title
        if self.request_timeout:
            kwargs["request_timeout"] = self.request_timeout
        if self.credentials_path:
            kwargs["credentials"] = self.credentials_path

        return VertexAIEmbeddings(**kwargs)

    def validate_configuration(self) -> None:
        """Validate the configuration before instantiation."""
        super().validate_configuration()

        if not self.project:
            raise ValueError("Project ID is required")
        if not self.location:
            raise ValueError("Location is required")

    def get_default_model(self) -> str:
        """Get the default model for Vertex AI embeddings."""
        return "text-embedding-004"

    def get_supported_models(self) -> list[str]:
        """Get list of supported Vertex AI embedding models."""
        return [
            "text-embedding-004",
            "text-multilingual-embedding-002",
            "text-embedding-preview-0409",
            "text-multilingual-embedding-preview-0409",
            "textembedding-gecko@001",
            "textembedding-gecko@003",
            "textembedding-gecko-multilingual@001",
        ]

    def get_model_info(self) -> dict:
        """Get information about the configured model."""
        model_info = {
            "text-embedding-004": {
                "dimensions": 768,
                "max_input_tokens": 3072,
                "languages": ["English", "100+ languages"],
                "description": "Latest text embedding model with high performance",
            },
            "text-multilingual-embedding-002": {
                "dimensions": 768,
                "max_input_tokens": 2048,
                "languages": ["100+ languages"],
                "description": "Multilingual text embedding model",
            },
            "textembedding-gecko@001": {
                "dimensions": 768,
                "max_input_tokens": 2048,
                "languages": ["English", "100+ languages"],
                "description": "Gecko text embedding model",
            },
            "textembedding-gecko@003": {
                "dimensions": 768,
                "max_input_tokens": 2048,
                "languages": ["English", "100+ languages"],
                "description": "Gecko text embedding model v3",
            },
            "textembedding-gecko-multilingual@001": {
                "dimensions": 768,
                "max_input_tokens": 2048,
                "languages": ["100+ languages"],
                "description": "Multilingual Gecko text embedding model",
            },
        }

        return model_info.get(
            self.model,
            {
                "dimensions": "unknown",
                "max_input_tokens": "unknown",
                "languages": "unknown",
                "description": "Vertex AI embedding model",
            },
        )

    def get_task_types(self) -> list[str]:
        """Get list of supported task types."""
        return [
            "RETRIEVAL_QUERY",
            "RETRIEVAL_DOCUMENT",
            "SEMANTIC_SIMILARITY",
            "CLASSIFICATION",
            "CLUSTERING",
        ]

    def get_supported_locations(self) -> list[str]:
        """Get list of supported Google Cloud locations."""
        return [
            "us-central1",
            "us-east1",
            "us-west1",
            "us-west4",
            "europe-west1",
            "europe-west4",
            "asia-east1",
            "asia-northeast1",
            "asia-southeast1",
        ]
