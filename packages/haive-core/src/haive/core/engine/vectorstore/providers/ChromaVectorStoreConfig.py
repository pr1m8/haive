"""Chroma Vector Store implementation for the Haive framework.

This module provides a configuration class for the Chroma vector store,
which is an open-source embedding database designed for AI applications.

Chroma provides:
1. Simple, fast semantic search and retrieval
2. Persistent storage with automatic saving/loading
3. Metadata filtering capabilities
4. Multiple distance metrics (cosine, L2, IP)
5. Easy integration with various embedding models

This vector store is particularly useful when:
- You need a lightweight, embedded vector database
- Want persistent storage without external dependencies
- Need metadata filtering on your searches
- Building prototypes or small to medium-scale applications

The implementation integrates with LangChain's Chroma while providing
a consistent Haive configuration interface.
"""

from typing import Any, Dict, List, Optional, Tuple, Type

from langchain_core.documents import Document
from pydantic import Field, validator

from haive.core.engine.vectorstore.base import BaseVectorStoreConfig
from haive.core.engine.vectorstore.types import VectorStoreType


@BaseVectorStoreConfig.register(VectorStoreType.CHROMA)
class ChromaVectorStoreConfig(BaseVectorStoreConfig):
    """Configuration for Chroma vector store in the Haive framework.

    This vector store uses Chroma for efficient semantic search with
    persistent storage and metadata filtering capabilities.

    Attributes:
        persist_directory (Optional[str]): Directory to persist the Chroma database.
        collection_metadata (Dict[str, Any]): Metadata for the collection.
        distance_metric (str): Distance metric to use (cosine, l2, ip).
        n_results (int): Default number of results to return.

    Examples:
        >>> from haive.core.engine.vectorstore import ChromaVectorStoreConfig
        >>> from haive.core.models.embeddings.base import OpenAIEmbeddingConfig
        >>>
        >>> # Create Chroma config with persistence
        >>> config = ChromaVectorStoreConfig(
        ...     name="document_store",
        ...     embedding=OpenAIEmbeddingConfig(),
        ...     persist_directory="./chroma_db",
        ...     collection_name="my_documents",
        ...     distance_metric="cosine"
        ... )
        >>>
        >>> # Instantiate and use the vector store
        >>> vectorstore = config.instantiate()
        >>>
        >>> # Add documents
        >>> docs = [Document(page_content="AI is transforming the world")]
        >>> vectorstore.add_documents(docs)
        >>>
        >>> # Search
        >>> results = vectorstore.similarity_search("artificial intelligence", k=5)
    """

    # Chroma-specific configuration
    persist_directory: str | None = Field(
        default=None,
        description="Directory to persist the database. If None, data will be ephemeral",
    )

    collection_metadata: dict[str, Any] = Field(
        default_factory=dict, description="Metadata to associate with the collection"
    )

    distance_metric: str = Field(
        default="cosine",
        description="Distance metric: 'cosine', 'l2', or 'ip' (inner product)",
    )

    # ChromaDB settings
    chroma_settings: dict[str, Any] | None = Field(
        default=None, description="Additional ChromaDB settings"
    )

    # HTTP settings (for client-server mode)
    chroma_server_host: str | None = Field(
        default=None, description="Chroma server host for HTTP client mode"
    )

    chroma_server_port: int | None = Field(
        default=None, description="Chroma server port for HTTP client mode"
    )

    chroma_server_ssl: bool = Field(
        default=False, description="Use SSL for Chroma server connection"
    )

    @validator("distance_metric")
    def validate_distance_metric(self, v):
        """Validate distance metric is supported."""
        valid_metrics = ["cosine", "l2", "ip"]
        if v not in valid_metrics:
            raise ValueError(f"distance_metric must be one of {valid_metrics}, got {v}")
        return v

    def get_input_fields(self) -> dict[str, tuple[type, Any]]:
        """Return input field definitions for Chroma vector store."""
        return {
            "documents": (
                list[Document],
                Field(description="Documents to add to the vector store"),
            ),
        }

    def get_output_fields(self) -> dict[str, tuple[type, Any]]:
        """Return output field definitions for Chroma vector store."""
        return {
            "ids": (list[str], Field(description="IDs of the added documents")),
        }

    def instantiate(self):
        """Create a Chroma vector store from this configuration.

        Returns:
            Chroma: Instantiated Chroma vector store.

        Raises:
            ImportError: If required packages are not available.
            ValueError: If configuration is invalid.
        """
        try:
            from langchain_chroma import Chroma
        except ImportError:
            try:
                from langchain_community.vectorstores import Chroma
            except ImportError:
                raise ImportError(
                    "Chroma requires chromadb package. "
                    "Install with: pip install chromadb"
                )

        # Validate embedding
        self.validate_embedding()
        embedding_function = self.embedding.instantiate()

        # Prepare Chroma client settings if using server mode
        client_settings = None
        if self.chroma_server_host:
            try:
                import chromadb
                from chromadb.config import Settings

                client_settings = Settings(
                    chroma_server_host=self.chroma_server_host,
                    chroma_server_port=self.chroma_server_port or 8000,
                    chroma_server_ssl_enabled=self.chroma_server_ssl,
                )
            except ImportError:
                raise ImportError(
                    "Server mode requires chromadb package. "
                    "Install with: pip install chromadb"
                )

        # Map distance metric to Chroma's expected format

        # Prepare kwargs
        kwargs = {
            "embedding_function": embedding_function,
            "collection_name": self.collection_name,
            "collection_metadata": self.collection_metadata or None,
        }

        if self.persist_directory:
            kwargs["persist_directory"] = self.persist_directory

        if client_settings:
            kwargs["client_settings"] = client_settings
        elif self.chroma_settings:
            # Use custom settings if provided
            from chromadb.config import Settings

            kwargs["client_settings"] = Settings(**self.chroma_settings)

        # Create Chroma instance
        return Chroma(**kwargs)
