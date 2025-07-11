"""Qdrant Sparse Vector Retriever implementation for the Haive framework.

This module provides a configuration class for the Qdrant Sparse Vector retriever,
which uses Qdrant's sparse vector capabilities for keyword-based and hybrid search.
Qdrant supports both dense and sparse vectors, enabling efficient text search
using sparse embeddings like BM25 or TF-IDF representations.

The QdrantSparseVectorRetriever works by:
1. Connecting to a Qdrant instance
2. Using sparse vector representations for text search
3. Supporting efficient keyword matching and retrieval
4. Enabling hybrid dense + sparse vector search

This retriever is particularly useful when:
- Need efficient keyword-based search with Qdrant
- Want to combine dense and sparse vector search
- Building hybrid retrieval systems
- Using Qdrant for production vector search
- Need high-performance text matching

The implementation integrates with LangChain's QdrantSparseVectorRetriever while
providing a consistent Haive configuration interface with secure API key management.
"""

from typing import Any, Dict, List, Optional, Tuple, Type

from langchain_core.documents import Document
from pydantic import Field, SecretStr

from haive.core.common.mixins.secure_config import SecureConfigMixin
from haive.core.engine.retriever.retriever import BaseRetrieverConfig
from haive.core.engine.retriever.types import RetrieverType


@BaseRetrieverConfig.register(RetrieverType.QDRANT_SPARSE_VECTOR)
class QdrantSparseVectorRetrieverConfig(SecureConfigMixin, BaseRetrieverConfig):
    """Configuration for Qdrant Sparse Vector retriever in the Haive framework.

    This retriever uses Qdrant's sparse vector capabilities to provide efficient
    keyword-based search and hybrid dense + sparse vector retrieval.

    Attributes:
        retriever_type (RetrieverType): The type of retriever (always QDRANT_SPARSE_VECTOR).
        qdrant_url (str): Qdrant instance URL.
        collection_name (str): Name of the Qdrant collection.
        api_key (Optional[SecretStr]): Qdrant API key (auto-resolved from QDRANT_API_KEY).
        k (int): Number of documents to retrieve.
        sparse_vector_name (str): Name of the sparse vector field.
        enable_hybrid_search (bool): Whether to combine with dense vectors.

    Examples:
        >>> from haive.core.engine.retriever import QdrantSparseVectorRetrieverConfig
        >>>
        >>> # Create the Qdrant sparse vector retriever config
        >>> config = QdrantSparseVectorRetrieverConfig(
        ...     name="qdrant_sparse_retriever",
        ...     qdrant_url="https://my-cluster.qdrant.tech",
        ...     collection_name="documents",
        ...     k=10,
        ...     sparse_vector_name="sparse_text",
        ...     enable_hybrid_search=False
        ... )
        >>>
        >>> # Instantiate and use the retriever
        >>> retriever = config.instantiate()
        >>> docs = retriever.get_relevant_documents("machine learning algorithms")
        >>>
        >>> # Example with hybrid search
        >>> hybrid_config = QdrantSparseVectorRetrieverConfig(
        ...     name="qdrant_hybrid_retriever",
        ...     qdrant_url="https://my-cluster.qdrant.tech",
        ...     collection_name="documents",
        ...     enable_hybrid_search=True,
        ...     hybrid_fusion_method="rrf"
        ... )
    """

    retriever_type: RetrieverType = Field(
        default=RetrieverType.QDRANT_SPARSE_VECTOR, description="The type of retriever"
    )

    # Qdrant connection configuration
    qdrant_url: str = Field(
        ..., description="Qdrant instance URL (e.g., 'https://my-cluster.qdrant.tech')"
    )

    collection_name: str = Field(
        ..., description="Name of the Qdrant collection to search"
    )

    # API configuration with SecureConfigMixin
    api_key: SecretStr | None = Field(
        default=None, description="Qdrant API key (auto-resolved from QDRANT_API_KEY)"
    )

    # Provider for SecureConfigMixin
    provider: str = Field(
        default="qdrant", description="Provider name for API key resolution"
    )

    # Search parameters
    k: int = Field(
        default=10, ge=1, le=100, description="Number of documents to retrieve"
    )

    sparse_vector_name: str = Field(
        default="sparse_text", description="Name of the sparse vector field in Qdrant"
    )

    # Hybrid search configuration
    enable_hybrid_search: bool = Field(
        default=False,
        description="Whether to combine sparse vectors with dense vectors",
    )

    dense_vector_name: str = Field(
        default="dense",
        description="Name of the dense vector field (used in hybrid search)",
    )

    hybrid_fusion_method: str = Field(
        default="rrf",
        description="Fusion method for hybrid search: 'rrf' (Reciprocal Rank Fusion), 'linear'",
    )

    # Search filtering
    filter_conditions: dict[str, Any] | None = Field(
        default=None, description="Qdrant filter conditions for search results"
    )

    # Advanced parameters
    score_threshold: float | None = Field(
        default=None, ge=0.0, le=1.0, description="Minimum score threshold for results"
    )

    sparse_encoder_model: str | None = Field(
        default=None, description="Sparse encoder model name (e.g., 'splade++', 'bm25')"
    )

    # Connection parameters
    timeout: float | None = Field(
        default=60.0, ge=1.0, le=300.0, description="Request timeout in seconds"
    )

    def get_input_fields(self) -> dict[str, tuple[type, Any]]:
        """Return input field definitions for Qdrant Sparse Vector retriever."""
        return {
            "query": (str, Field(description="Sparse vector search query for Qdrant")),
        }

    def get_output_fields(self) -> dict[str, tuple[type, Any]]:
        """Return output field definitions for Qdrant Sparse Vector retriever."""
        return {
            "documents": (
                list[Document],
                Field(
                    default_factory=list,
                    description="Documents from Qdrant sparse vector search",
                ),
            ),
        }

    def instantiate(self):
        """Create a Qdrant Sparse Vector retriever from this configuration.

        Returns:
            QdrantSparseVectorRetriever: Instantiated retriever ready for sparse vector search.

        Raises:
            ImportError: If required packages are not available.
            ValueError: If API key or configuration is invalid.
        """
        try:
            from langchain_qdrant.retrievers import QdrantSparseVectorRetriever
            from qdrant_client import QdrantClient
        except ImportError:
            raise ImportError(
                "QdrantSparseVectorRetriever requires langchain-qdrant and qdrant-client packages. "
                "Install with: pip install langchain-qdrant qdrant-client"
            )

        # Get API key using SecureConfigMixin
        api_key = self.get_api_key()

        # Create Qdrant client
        client_kwargs = {"url": self.qdrant_url, "timeout": self.timeout}

        if api_key:
            client_kwargs["api_key"] = api_key

        client = QdrantClient(**client_kwargs)

        # Prepare retriever configuration
        config = {
            "client": client,
            "collection_name": self.collection_name,
            "sparse_vector_name": self.sparse_vector_name,
            "k": self.k,
        }

        # Add hybrid search configuration
        if self.enable_hybrid_search:
            config["enable_hybrid"] = True
            config["dense_vector_name"] = self.dense_vector_name
            config["fusion_method"] = self.hybrid_fusion_method

        # Add optional parameters
        if self.filter_conditions:
            config["filter"] = self.filter_conditions

        if self.score_threshold:
            config["score_threshold"] = self.score_threshold

        if self.sparse_encoder_model:
            config["sparse_encoder"] = self.sparse_encoder_model

        return QdrantSparseVectorRetriever(**config)
