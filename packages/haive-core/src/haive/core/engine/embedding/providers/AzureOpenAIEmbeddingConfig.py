"""Azure OpenAI embedding configuration."""

import os
from typing import Any, Optional

from pydantic import Field, validator

from haive.core.engine.embedding.base import BaseEmbeddingConfig
from haive.core.engine.embedding.types import EmbeddingType


@BaseEmbeddingConfig.register(EmbeddingType.AZURE_OPENAI)
class AzureOpenAIEmbeddingConfig(BaseEmbeddingConfig):
    """Configuration for Azure OpenAI embeddings.

    This configuration provides access to OpenAI embedding models deployed
    on Azure OpenAI Service. It supports both standard and data zone deployments.

    Examples:
        Basic usage::

            config = AzureOpenAIEmbeddingConfig(
                name="azure_embeddings",
                model="text-embedding-3-large",
                deployment_name="text-embedding-3-large",
                azure_endpoint="https://your-resource.openai.azure.com/",
                api_key="your-api-key"
            )

            embeddings = config.instantiate()

        Using environment variables::

            # Set AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, etc.
            config = AzureOpenAIEmbeddingConfig(
                name="azure_embeddings",
                model="text-embedding-3-large",
                deployment_name="text-embedding-3-large"
            )

        With custom API version::

            config = AzureOpenAIEmbeddingConfig(
                name="azure_embeddings",
                model="text-embedding-3-large",
                deployment_name="text-embedding-3-large",
                api_version="2024-02-15-preview"
            )

    Attributes:
        embedding_type: Always EmbeddingType.AZURE_OPENAI
        deployment_name: Azure deployment name for the model
        azure_endpoint: Azure OpenAI service endpoint URL
        api_version: Azure OpenAI API version
        api_key: Azure OpenAI API key
        dimensions: Output dimensions (optional, model-dependent)

    """

    embedding_type: EmbeddingType = Field(
        default=EmbeddingType.AZURE_OPENAI, description="The embedding provider type"
    )

    # Azure-specific required fields
    deployment_name: str = Field(
        ..., description="Azure deployment name for the embedding model"
    )
    azure_endpoint: str = Field(
        default_factory=lambda: os.getenv("AZURE_OPENAI_ENDPOINT", ""),
        description="Azure OpenAI service endpoint URL",
    )

    # Azure-specific optional fields
    api_version: str = Field(
        default_factory=lambda: os.getenv(
            "AZURE_OPENAI_API_VERSION", "2024-02-15-preview"
        ),
        description="Azure OpenAI API version",
    )
    max_retries: int = Field(
        default=3, description="Maximum number of retries for API calls"
    )
    request_timeout: float | None = Field(
        default=None, description="Timeout for API requests in seconds"
    )

    # SecureConfigMixin configuration
    provider: str = Field(
        default="azure", description="Provider name for API key resolution"
    )

    @validator("azure_endpoint")
    @classmethod
    def validate_azure_endpoint(cls, v):
        """Validate Azure OpenAI endpoint format."""
        if not v:
            raise ValueError(
                "Azure endpoint is required. Set AZURE_OPENAI_ENDPOINT environment variable "
                "or provide azure_endpoint parameter."
            )

        if not v.startswith("https://"):
            raise ValueError("Azure endpoint must start with 'https://'")

        if not v.endswith("/"):
            v = v + "/"

        return v

    @validator("deployment_name")
    @classmethod
    def validate_deployment_name(cls, v):
        """Validate deployment name."""
        if not v or not v.strip():
            raise ValueError("Deployment name is required and cannot be empty")
        return v.strip()

    @validator("api_version")
    @classmethod
    def validate_api_version(cls, v):
        """Validate API version format."""
        if not v:
            raise ValueError("API version is required")

        # Check format (YYYY-MM-DD or YYYY-MM-DD-preview)
        import re

        if not re.match(r"^\d{4}-\d{2}-\d{2}(-preview)?$", v):
            raise ValueError(
                "API version must be in format YYYY-MM-DD or YYYY-MM-DD-preview"
            )

        return v

    def instantiate(self) -> Any:
        """Create an Azure OpenAI embeddings instance.

        Returns:
            AzureOpenAIEmbeddings instance configured with the provided parameters

        Raises:
            ImportError: If langchain-openai is not installed
            ValueError: If configuration is invalid

        """
        try:
            from langchain_openai import AzureOpenAIEmbeddings
        except ImportError:
            raise ImportError(
                "Azure OpenAI embeddings require the langchain-openai package. "
                "Install with: pip install langchain-openai"
            )

        # Validate configuration
        self.validate_configuration()

        # Get API key
        api_key = self.get_api_key()
        if not api_key:
            raise ValueError(
                "Azure OpenAI API key is required. Set AZURE_OPENAI_API_KEY environment variable "
                "or provide api_key parameter."
            )

        # Build kwargs
        kwargs = {
            "model": self.deployment_name,  # Azure uses deployment name as model
            "azure_deployment": self.deployment_name,
            "azure_endpoint": self.azure_endpoint,
            "api_key": api_key,
            "api_version": self.api_version,
            "max_retries": self.max_retries,
        }

        # Add optional parameters
        if self.request_timeout is not None:
            kwargs["timeout"] = self.request_timeout
        if self.dimensions:
            kwargs["dimensions"] = self.dimensions

        return AzureOpenAIEmbeddings(**kwargs)

    def validate_configuration(self) -> None:
        """Validate the configuration before instantiation."""
        super().validate_configuration()

        if not self.deployment_name:
            raise ValueError("Deployment name is required")
        if not self.azure_endpoint:
            raise ValueError("Azure endpoint is required")
        if not self.api_version:
            raise ValueError("API version is required")

    def get_default_model(self) -> str:
        """Get the default model for Azure OpenAI embeddings."""
        return "text-embedding-3-large"

    def get_supported_models(self) -> list[str]:
        """Get list of supported Azure OpenAI embedding models."""
        return [
            "text-embedding-3-large",
            "text-embedding-3-small",
            "text-embedding-ada-002",
        ]

    def get_model_info(self) -> dict:
        """Get information about the configured model."""
        model_info = {
            "text-embedding-3-large": {
                "dimensions": 3072,
                "max_dimensions": 3072,
                "context_length": 8192,
                "description": "Most capable Azure OpenAI embedding model",
            },
            "text-embedding-3-small": {
                "dimensions": 1536,
                "max_dimensions": 1536,
                "context_length": 8192,
                "description": "Smaller, faster Azure OpenAI embedding model",
            },
            "text-embedding-ada-002": {
                "dimensions": 1536,
                "max_dimensions": 1536,
                "context_length": 8192,
                "description": "Legacy Azure OpenAI embedding model",
            },
        }

        return model_info.get(
            self.model,
            {
                "dimensions": "unknown",
                "context_length": "unknown",
                "description": "Azure OpenAI embedding model",
            },
        )
