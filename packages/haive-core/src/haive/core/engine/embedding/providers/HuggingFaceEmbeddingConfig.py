"""HuggingFace embedding configuration."""

import os
from typing import Any, Dict, Optional

from pydantic import Field, validator

from haive.core.engine.embedding.base import BaseEmbeddingConfig
from haive.core.engine.embedding.types import EmbeddingType


@BaseEmbeddingConfig.register(EmbeddingType.HUGGINGFACE)
class HuggingFaceEmbeddingConfig(BaseEmbeddingConfig):
    """Configuration for HuggingFace embeddings.

    This configuration provides access to HuggingFace embedding models including
    sentence transformers and other transformer-based embedding models.

    Examples:
        Basic usage::

            config = HuggingFaceEmbeddingConfig(
                name="hf_embeddings",
                model="sentence-transformers/all-MiniLM-L6-v2"
            )

            embeddings = config.instantiate()

        With GPU support::

            config = HuggingFaceEmbeddingConfig(
                name="hf_embeddings",
                model="sentence-transformers/all-mpnet-base-v2",
                model_kwargs={"device": "cuda"},
                encode_kwargs={"normalize_embeddings": True}
            )

        With caching::

            config = HuggingFaceEmbeddingConfig(
                name="hf_embeddings",
                model="sentence-transformers/all-MiniLM-L6-v2",
                use_cache=True,
                cache_folder="./embedding_cache"
            )

    Attributes:
        embedding_type: Always EmbeddingType.HUGGINGFACE
        model: HuggingFace model name or path
        model_kwargs: Additional arguments for model initialization
        encode_kwargs: Additional arguments for encoding
        use_cache: Whether to use embedding caching
        cache_folder: Directory for caching embeddings

    """

    embedding_type: EmbeddingType = Field(
        default=EmbeddingType.HUGGINGFACE, description="The embedding provider type"
    )

    # HuggingFace-specific fields
    model_kwargs: dict[str, Any] = Field(
        default_factory=lambda: {"device": "cpu"},
        description="Additional arguments for model initialization",
    )
    encode_kwargs: dict[str, Any] = Field(
        default_factory=dict, description="Additional arguments for encoding"
    )
    multi_process: bool = Field(
        default=False, description="Whether to use multi-processing for encoding"
    )
    show_progress: bool = Field(
        default=False, description="Whether to show progress bar during encoding"
    )
    use_cache: bool = Field(
        default=True, description="Whether to use embedding caching"
    )
    cache_folder: str | None = Field(
        default=None, description="Directory for caching embeddings"
    )

    # Trust remote code (for custom models)
    trust_remote_code: bool = Field(
        default=False, description="Whether to trust remote code for custom models"
    )

    # SecureConfigMixin configuration
    provider: str = Field(
        default="huggingface", description="Provider name for API key resolution"
    )

    @validator("model")
    @classmethod
    def validate_model(cls, v):
        """Validate the HuggingFace model name."""
        if not v or not v.strip():
            raise ValueError("Model name is required and cannot be empty")
        return v.strip()

    @validator("model_kwargs")
    @classmethod
    def validate_model_kwargs(cls, v):
        """Validate and set default model kwargs."""
        if not v:
            v = {}

        # Auto-detect device if not specified
        if "device" not in v:
            try:
                import torch

                v["device"] = "cuda" if torch.cuda.is_available() else "cpu"
            except ImportError:
                v["device"] = "cpu"

        return v

    @validator("cache_folder")
    @classmethod
    def validate_cache_folder(cls, v, values):
        """Set default cache folder if not specified."""
        if v is None and values.get("use_cache", True):
            # Use a default cache folder
            v = os.path.expanduser("~/.cache/haive/embeddings")
        return v

    def instantiate(self) -> Any:
        """Create a HuggingFace embeddings instance.

        Returns:
            HuggingFaceEmbeddings instance configured with the provided parameters

        Raises:
            ImportError: If required packages are not installed
            ValueError: If configuration is invalid

        """
        try:
            from langchain_huggingface import HuggingFaceEmbeddings
        except ImportError:
            raise ImportError(
                "HuggingFace embeddings require the langchain-huggingface package. "
                "Install with: pip install langchain-huggingface"
            )

        # Validate configuration
        self.validate_configuration()

        # Build kwargs
        kwargs = {
            "model_name": self.model,
            "model_kwargs": self.model_kwargs,
            "encode_kwargs": self.encode_kwargs,
            "multi_process": self.multi_process,
            "show_progress": self.show_progress,
        }

        # Add cache folder if specified
        if self.cache_folder:
            kwargs["cache_folder"] = self.cache_folder

        # Add trust remote code if specified
        if self.trust_remote_code:
            kwargs["trust_remote_code"] = self.trust_remote_code

        # Create base embeddings
        embeddings = HuggingFaceEmbeddings(**kwargs)

        # Add caching if enabled
        if self.use_cache and self.cache_folder:
            try:
                from langchain.embeddings import CacheBackedEmbeddings
                from langchain.storage import LocalFileStore

                # Create cache store
                store = LocalFileStore(self.cache_folder)

                # Wrap with cache
                embeddings = CacheBackedEmbeddings.from_bytes_store(
                    embeddings,
                    document_embedding_cache=store,
                    query_embedding_cache=True,
                    namespace=self.model.replace("/", "_"),
                )
            except ImportError:
                # If caching dependencies not available, continue without caching
                import logging

                logger = logging.getLogger(__name__)
                logger.warning("Caching not available - continuing without cache")

        return embeddings

    def validate_configuration(self) -> None:
        """Validate the configuration before instantiation."""
        super().validate_configuration()

        if not self.model:
            raise ValueError("Model name is required")

        # Validate cache folder if caching is enabled
        if self.use_cache and self.cache_folder:
            try:
                os.makedirs(self.cache_folder, exist_ok=True)
            except OSError as e:
                raise ValueError(f"Cannot create cache folder {self.cache_folder}: {e}")

    def get_default_model(self) -> str:
        """Get the default model for HuggingFace embeddings."""
        return "sentence-transformers/all-MiniLM-L6-v2"

    def get_supported_models(self) -> list[str]:
        """Get list of popular HuggingFace embedding models."""
        return [
            "sentence-transformers/all-MiniLM-L6-v2",
            "sentence-transformers/all-mpnet-base-v2",
            "sentence-transformers/all-roberta-large-v1",
            "sentence-transformers/multi-qa-MiniLM-L6-cos-v1",
            "sentence-transformers/multi-qa-mpnet-base-cos-v1",
            "sentence-transformers/paraphrase-MiniLM-L6-v2",
            "sentence-transformers/paraphrase-mpnet-base-v2",
            "sentence-transformers/msmarco-distilbert-base-v4",
            "BAAI/bge-large-en-v1.5",
            "BAAI/bge-base-en-v1.5",
            "BAAI/bge-small-en-v1.5",
            "intfloat/e5-large-v2",
            "intfloat/e5-base-v2",
            "intfloat/e5-small-v2",
            "thenlper/gte-large",
            "thenlper/gte-base",
        ]

    def get_model_info(self) -> dict:
        """Get information about the configured model."""
        # Common model information
        model_info = {
            "sentence-transformers/all-MiniLM-L6-v2": {
                "dimensions": 384,
                "max_seq_length": 256,
                "description": "Fast, lightweight model with good performance",
            },
            "sentence-transformers/all-mpnet-base-v2": {
                "dimensions": 768,
                "max_seq_length": 384,
                "description": "High-quality all-round model",
            },
            "sentence-transformers/all-roberta-large-v1": {
                "dimensions": 1024,
                "max_seq_length": 512,
                "description": "Large model with high performance",
            },
            "BAAI/bge-large-en-v1.5": {
                "dimensions": 1024,
                "max_seq_length": 512,
                "description": "BAAI's large English embedding model",
            },
            "BAAI/bge-base-en-v1.5": {
                "dimensions": 768,
                "max_seq_length": 512,
                "description": "BAAI's base English embedding model",
            },
            "BAAI/bge-small-en-v1.5": {
                "dimensions": 384,
                "max_seq_length": 512,
                "description": "BAAI's small English embedding model",
            },
            "intfloat/e5-large-v2": {
                "dimensions": 1024,
                "max_seq_length": 512,
                "description": "E5 large model with strong performance",
            },
            "intfloat/e5-base-v2": {
                "dimensions": 768,
                "max_seq_length": 512,
                "description": "E5 base model with good balance",
            },
            "thenlper/gte-large": {
                "dimensions": 1024,
                "max_seq_length": 512,
                "description": "GTE large model with high performance",
            },
        }

        return model_info.get(
            self.model,
            {
                "dimensions": "unknown",
                "max_seq_length": "unknown",
                "description": "HuggingFace embedding model",
            },
        )
