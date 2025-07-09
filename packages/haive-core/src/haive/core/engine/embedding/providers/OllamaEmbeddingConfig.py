"""Ollama embedding configuration."""

from typing import Any, Dict, Optional

from pydantic import Field, validator

from haive.core.engine.embedding.base import BaseEmbeddingConfig
from haive.core.engine.embedding.types import EmbeddingType


@BaseEmbeddingConfig.register(EmbeddingType.OLLAMA)
class OllamaEmbeddingConfig(BaseEmbeddingConfig):
    """Configuration for Ollama embeddings.

    This configuration provides access to locally hosted Ollama embedding models
    including nomic-embed-text, mxbai-embed-large, and other supported models.

    Examples:
        Basic usage::

            config = OllamaEmbeddingConfig(
                name="ollama_embeddings",
                model="nomic-embed-text",
                base_url="http://localhost:11434"
            )

            embeddings = config.instantiate()

        With custom headers::

            config = OllamaEmbeddingConfig(
                name="ollama_embeddings",
                model="mxbai-embed-large",
                base_url="http://localhost:11434",
                headers={"Authorization": "Bearer token"}
            )

        With custom options::

            config = OllamaEmbeddingConfig(
                name="ollama_embeddings",
                model="nomic-embed-text",
                base_url="http://localhost:11434",
                model_options={"temperature": 0.1}
            )

    Attributes:
        embedding_type: Always EmbeddingType.OLLAMA
        model: Ollama model name (e.g., "nomic-embed-text")
        base_url: Ollama server URL
        headers: Optional HTTP headers for requests
        model_options: Optional model-specific options

    """

    embedding_type: EmbeddingType = Field(
        default=EmbeddingType.OLLAMA, description="The embedding provider type"
    )

    # Ollama-specific fields
    base_url: str = Field(
        default="http://localhost:11434", description="Ollama server URL"
    )
    headers: Optional[Dict[str, str]] = Field(
        default=None, description="Optional HTTP headers for requests"
    )
    model_options: Optional[Dict[str, Any]] = Field(
        default=None, description="Optional model-specific options"
    )
    request_timeout: Optional[float] = Field(
        default=None, description="Timeout for API requests in seconds"
    )

    # SecureConfigMixin configuration (not typically needed for local Ollama)
    provider: str = Field(
        default="ollama", description="Provider name for API key resolution"
    )

    @validator("model")
    def validate_model(cls, v):
        """Validate the Ollama model name."""
        popular_models = {
            "nomic-embed-text",
            "mxbai-embed-large",
            "snowflake-arctic-embed",
            "all-minilm",
            "llama2:7b",
            "mistral:7b",
            "codellama:7b",
        }
        if v not in popular_models:
            # Log info but don't fail - Ollama supports many models
            import logging

            logger = logging.getLogger(__name__)
            logger.info(f"Using Ollama model: {v}. Popular models: {popular_models}")
        return v

    @validator("base_url")
    def validate_base_url(cls, v):
        """Validate Ollama server URL."""
        if not v or not v.strip():
            raise ValueError("Base URL is required")

        v = v.strip()
        if not v.startswith(("http://", "https://")):
            raise ValueError("Base URL must start with 'http://' or 'https://'")

        # Remove trailing slash
        if v.endswith("/"):
            v = v[:-1]

        return v

    def instantiate(self) -> Any:
        """Create an Ollama embeddings instance.

        Returns:
            OllamaEmbeddings instance configured with the provided parameters

        Raises:
            ImportError: If langchain-ollama is not installed
            ValueError: If configuration is invalid

        """
        try:
            from langchain_ollama import OllamaEmbeddings
        except ImportError:
            raise ImportError(
                "Ollama embeddings require the langchain-ollama package. "
                "Install with: pip install langchain-ollama"
            )

        # Validate configuration
        self.validate_configuration()

        # Build kwargs
        kwargs = {
            "model": self.model,
            "base_url": self.base_url,
        }

        # Add optional parameters
        if self.headers:
            kwargs["headers"] = self.headers
        if self.model_options:
            kwargs["model_kwargs"] = self.model_options
        if self.request_timeout:
            kwargs["timeout"] = self.request_timeout

        return OllamaEmbeddings(**kwargs)

    def validate_configuration(self) -> None:
        """Validate the configuration before instantiation."""
        super().validate_configuration()

        if not self.base_url:
            raise ValueError("Base URL is required")

    def get_default_model(self) -> str:
        """Get the default model for Ollama embeddings."""
        return "nomic-embed-text"

    def get_supported_models(self) -> list[str]:
        """Get list of popular Ollama embedding models."""
        return [
            "nomic-embed-text",
            "mxbai-embed-large",
            "snowflake-arctic-embed",
            "all-minilm",
            "bge-large",
            "bge-base",
            "e5-large",
            "e5-base",
            "gte-large",
            "gte-base",
        ]

    def get_model_info(self) -> dict:
        """Get information about the configured model."""
        model_info = {
            "nomic-embed-text": {
                "dimensions": 768,
                "description": "Nomic's text embedding model, good for general use",
            },
            "mxbai-embed-large": {
                "dimensions": 1024,
                "description": "Mixedbread AI's large embedding model",
            },
            "snowflake-arctic-embed": {
                "dimensions": 1024,
                "description": "Snowflake's Arctic embedding model",
            },
            "all-minilm": {
                "dimensions": 384,
                "description": "Lightweight sentence transformer model",
            },
            "bge-large": {
                "dimensions": 1024,
                "description": "BAAI's large embedding model",
            },
            "bge-base": {
                "dimensions": 768,
                "description": "BAAI's base embedding model",
            },
            "e5-large": {
                "dimensions": 1024,
                "description": "Microsoft's E5 large embedding model",
            },
            "e5-base": {
                "dimensions": 768,
                "description": "Microsoft's E5 base embedding model",
            },
        }

        return model_info.get(
            self.model,
            {"dimensions": "unknown", "description": "Ollama embedding model"},
        )

    def test_connection(self) -> bool:
        """Test connection to Ollama server.

        Returns:
            True if connection is successful, False otherwise

        """
        try:
            import requests

            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except Exception:
            return False

    def list_available_models(self) -> list[str]:
        """List models available on the Ollama server.

        Returns:
            List of model names available on the server

        """
        try:
            import requests

            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return [model["name"] for model in data.get("models", [])]
            return []
        except Exception:
            return []
