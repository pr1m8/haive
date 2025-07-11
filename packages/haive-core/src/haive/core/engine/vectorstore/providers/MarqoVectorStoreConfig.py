"""Marqo Vector Store implementation for the Haive framework.

This module provides a configuration class for the Marqo vector store,
which is an open-source tensor search engine with multimodal capabilities.

Marqo provides:
1. End-to-end vector search with built-in models
2. Multimodal search (text and images)
3. Built-in embedding models including CLIP for multimodal
4. Automatic model selection and management
5. Weighted queries for advanced search
6. No need for separate embedding infrastructure
7. Simple API with powerful features

This vector store is particularly useful when:
- You need multimodal search (text + images)
- Want built-in embedding models without external dependencies
- Building applications that search across different media types
- Need weighted and complex queries
- Want a simple setup without managing embeddings separately
- Require open-source solution with enterprise features

The implementation integrates with LangChain's Marqo while providing
a consistent Haive configuration interface.
"""

from collections.abc import Callable
from typing import Any, Dict, List, Optional, Tuple, Type

from langchain_core.documents import Document
from pydantic import Field, validator

from haive.core.engine.vectorstore.base import BaseVectorStoreConfig
from haive.core.engine.vectorstore.types import VectorStoreType


@BaseVectorStoreConfig.register(VectorStoreType.MARQO)
class MarqoVectorStoreConfig(BaseVectorStoreConfig):
    """Configuration for Marqo vector store in the Haive framework.

    This vector store uses Marqo's tensor search engine for multimodal search
    with built-in embedding models and automatic model management.

    Attributes:
        marqo_url (str): URL of the Marqo server.
        index_name (str): Name of the Marqo index.
        api_key (Optional[str]): API key for Marqo Cloud (if using cloud version).
        model (str): Model to use for embeddings (e.g., 'hf/all_datasets_v4_MiniLM-L6').
        normalize_embeddings (bool): Whether to normalize embeddings.
        treat_urls_and_pointers_as_images (bool): Enable multimodal indexing.

    Examples:
        >>> from haive.core.engine.vectorstore import MarqoVectorStoreConfig
        >>>
        >>> # Create Marqo config (local deployment)
        >>> config = MarqoVectorStoreConfig(
        ...     name="marqo_search",
        ...     marqo_url="http://localhost:8882",
        ...     index_name="documents",
        ...     model="hf/all_datasets_v4_MiniLM-L6"
        ... )
        >>>
        >>> # Create Marqo config for multimodal search
        >>> config = MarqoVectorStoreConfig(
        ...     name="marqo_multimodal",
        ...     marqo_url="http://localhost:8882",
        ...     index_name="multimodal_docs",
        ...     model="open_clip/ViT-B-32/openai",
        ...     treat_urls_and_pointers_as_images=True
        ... )
        >>>
        >>> # Note: Marqo manages embeddings internally, so embedding config is optional
        >>>
        >>> # Instantiate and use
        >>> import marqo
        >>> client = marqo.Client(url=config.marqo_url)
        >>> vectorstore = config.instantiate(client=client)
        >>>
        >>> # Add documents
        >>> docs = [Document(page_content="Marqo provides multimodal search")]
        >>> vectorstore.add_documents(docs)
        >>>
        >>> # Search with weighted queries
        >>> results = vectorstore.similarity_search(
        ...     {"search term": 1.0, "another term": 0.5},
        ...     k=5
        ... )
    """

    # Marqo configuration
    marqo_url: str = Field(
        default="http://localhost:8882", description="URL of the Marqo server"
    )

    index_name: str = Field(..., description="Name of the Marqo index (required)")

    api_key: str | None = Field(
        default=None,
        description="API key for Marqo Cloud (optional, for cloud deployments)",
    )

    # Model configuration
    model: str = Field(
        default="hf/all_datasets_v4_MiniLM-L6",
        description="Model to use for embeddings (e.g., 'hf/all_datasets_v4_MiniLM-L6', 'open_clip/ViT-B-32/openai')",
    )

    normalize_embeddings: bool = Field(
        default=True, description="Whether to normalize embeddings"
    )

    # Index settings
    treat_urls_and_pointers_as_images: bool = Field(
        default=False, description="Enable multimodal indexing for images"
    )

    # Search settings
    searchable_attributes: list[str] | None = Field(
        default=None, description="List of attributes to make searchable"
    )

    # Document settings
    document_batch_size: int = Field(
        default=1024, ge=1, le=10000, description="Batch size for document operations"
    )

    # Advanced settings
    add_documents_settings: dict[str, Any] | None = Field(
        default=None, description="Additional settings for add_documents operations"
    )

    page_content_builder: Callable[[dict[str, Any]], str] | None = Field(
        default=None,
        description="Custom function to build page content from Marqo results",
    )

    @validator("marqo_url")
    def validate_marqo_url(self, v):
        """Validate Marqo URL format."""
        if not v.startswith(("http://", "https://")):
            raise ValueError("marqo_url must start with http:// or https://")
        return v

    @validator("index_name")
    def validate_index_name(self, v):
        """Validate index name format."""
        if not v or len(v.strip()) == 0:
            raise ValueError("index_name cannot be empty")
        # Basic validation for index naming
        import re

        if not re.match(r"^[a-zA-Z0-9_-]+$", v):
            raise ValueError(
                "index_name must contain only letters, numbers, hyphens, and underscores"
            )
        return v

    @validator("model")
    def validate_model(self, v):
        """Validate model format."""
        if not v or len(v.strip()) == 0:
            raise ValueError("model cannot be empty")
        # Common model prefixes in Marqo
        valid_prefixes = ["hf/", "open_clip/", "onnx/", "sentence-transformers/"]
        if not any(v.startswith(prefix) for prefix in valid_prefixes):
            # Allow custom models but warn
            import logging

            logging.warning(
                f"Model '{v}' doesn't start with common prefixes {valid_prefixes}. "
                "Make sure it's a valid Marqo model."
            )
        return v

    def validate_embedding(self):
        """Override to make embedding optional for Marqo.

        Marqo manages its own embeddings internally based on the specified model,
        so we don't require an embedding configuration.
        """
        # Marqo doesn't need external embeddings

    def get_input_fields(self) -> dict[str, tuple[type, Any]]:
        """Return input field definitions for Marqo vector store."""
        return {
            "documents": (
                list[Document],
                Field(description="Documents to add to Marqo"),
            ),
        }

    def get_output_fields(self) -> dict[str, tuple[type, Any]]:
        """Return output field definitions for Marqo vector store."""
        return {
            "ids": (list[str], Field(description="Document IDs in Marqo")),
        }

    def instantiate(self, client=None):
        """Create a Marqo vector store from this configuration.

        Args:
            client: Optional pre-configured Marqo client. If not provided,
                    one will be created from the configuration.

        Returns:
            Marqo: Instantiated Marqo vector store.

        Raises:
            ImportError: If required packages are not available.
            ValueError: If configuration is invalid.
        """
        try:
            import marqo
            from langchain_community.vectorstores import Marqo
        except ImportError as e:
            raise ImportError(
                "Marqo requires marqo package. Install with: pip install marqo"
            ) from e

        # Create Marqo client if not provided
        if client is None:
            client_kwargs = {
                "url": self.marqo_url,
            }
            if self.api_key:
                client_kwargs["api_key"] = self.api_key

            try:
                client = marqo.Client(**client_kwargs)
            except Exception as e:
                raise ValueError(f"Failed to create Marqo client: {e}") from e

        # Ensure index exists with proper settings
        try:
            # Check if index exists
            existing_indexes = client.get_indexes()
            index_exists = any(
                idx["indexName"] == self.index_name
                for idx in existing_indexes["results"]
            )

            if not index_exists:
                # Create index with specified model and settings
                index_settings = {
                    "model": self.model,
                    "normalizeEmbeddings": self.normalize_embeddings,
                    "treatUrlsAndPointersAsImages": self.treat_urls_and_pointers_as_images,
                }
                client.create_index(self.index_name, settings_dict=index_settings)
        except Exception as e:
            # Index might already exist or other error
            import logging

            logging.warning(f"Could not ensure index exists: {e}")

        # Create Marqo vector store
        try:
            vectorstore = Marqo(
                client=client,
                index_name=self.index_name,
                add_documents_settings=self.add_documents_settings,
                searchable_attributes=self.searchable_attributes,
                page_content_builder=self.page_content_builder,
            )
            # Override document batch size if specified
            if self.document_batch_size != 1024:
                vectorstore._document_batch_size = self.document_batch_size
        except Exception as e:
            raise ValueError(f"Failed to create Marqo vector store: {e}") from e

        return vectorstore
