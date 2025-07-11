"""
Pinecone Hybrid Search Retriever implementation for the Haive framework.

This module provides a configuration class for the Pinecone Hybrid Search retriever,
which combines vector similarity search with keyword search using Pinecone's
hybrid search capabilities.

The PineconeHybridSearchRetriever works by:
1. Connecting to a Pinecone index
2. Performing both vector and keyword search
3. Combining results using Pinecone's hybrid scoring

This retriever is particularly useful when:
- Using Pinecone as the vector database
- Need both semantic and keyword search
- Want Pinecone's optimized hybrid search performance
- Building applications that benefit from combined search approaches

The implementation integrates with LangChain's PineconeHybridSearchRetriever while
providing a consistent Haive configuration interface with secure API key management.
"""

from typing import Any, Dict, List, Optional, Tuple, Type

from langchain_core.documents import Document
from pydantic import Field, SecretStr

from haive.core.common.mixins.secure_config import SecureConfigMixin
from haive.core.engine.retriever.retriever import BaseRetrieverConfig
from haive.core.engine.retriever.types import RetrieverType


@BaseRetrieverConfig.register(RetrieverType.PINECONE)
class PineconeHybridSearchRetrieverConfig(SecureConfigMixin, BaseRetrieverConfig):
    """
    Configuration for Pinecone Hybrid Search retriever in the Haive framework.

    This retriever uses Pinecone's hybrid search capabilities to combine vector
    similarity search with keyword search for better retrieval performance.

    Attributes:
        retriever_type (RetrieverType): The type of retriever (always PINECONE).
        api_key (Optional[SecretStr]): Pinecone API key (auto-resolved from PINECONE_API_KEY).
        index_name (str): Name of the Pinecone index to search.
        environment (str): Pinecone environment (e.g., "us-east1-gcp").
        top_k (int): Number of documents to retrieve (default: 10).
        alpha (float): Weight for vector vs sparse search (0.0 = sparse only, 1.0 = vector only).

    Examples:
        >>> from haive.core.engine.retriever import PineconeHybridSearchRetrieverConfig
        >>>
        >>> # Create the pinecone hybrid search retriever config
        >>> config = PineconeHybridSearchRetrieverConfig(
        ...     name="pinecone_hybrid_retriever",
        ...     index_name="my-hybrid-index",
        ...     environment="us-east1-gcp",
        ...     top_k=5,
        ...     alpha=0.5  # Equal weight to vector and sparse search
        ... )
        >>>
        >>> # Instantiate and use the retriever
        >>> retriever = config.instantiate()
        >>> docs = retriever.get_relevant_documents("machine learning algorithms")
    """

    retriever_type: RetrieverType = Field(
        default=RetrieverType.PINECONE, description="The type of retriever"
    )

    # API configuration with SecureConfigMixin
    api_key: Optional[SecretStr] = Field(
        default=None,
        description="Pinecone API key (auto-resolved from PINECONE_API_KEY)",
    )

    # Provider for SecureConfigMixin
    provider: str = Field(
        default="pinecone", description="Provider name for API key resolution"
    )

    # Pinecone configuration
    index_name: str = Field(..., description="Name of the Pinecone index to search")

    environment: str = Field(
        ..., description="Pinecone environment (e.g., 'us-east1-gcp')"
    )

    top_k: int = Field(
        default=10, ge=1, le=100, description="Number of documents to retrieve"
    )

    alpha: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Weight for vector vs sparse search (0.0 = sparse only, 1.0 = vector only)",
    )

    def get_input_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return input field definitions for Pinecone Hybrid Search retriever."""
        return {
            "query": (str, Field(description="Hybrid search query for Pinecone")),
        }

    def get_output_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return output field definitions for Pinecone Hybrid Search retriever."""
        return {
            "documents": (
                List[Document],
                Field(
                    default_factory=list,
                    description="Documents from Pinecone hybrid search",
                ),
            ),
        }

    def instantiate(self):
        """
        Create a Pinecone Hybrid Search retriever from this configuration.

        Returns:
            PineconeHybridSearchRetriever: Instantiated retriever ready for hybrid search.

        Raises:
            ImportError: If required packages are not available.
            ValueError: If API key or configuration is invalid.
        """
        try:
            from langchain_community.retrievers import PineconeHybridSearchRetriever
        except ImportError:
            raise ImportError(
                "PineconeHybridSearchRetriever requires pinecone-client package. "
                "Install with: pip install pinecone-client"
            )

        # Get API key using SecureConfigMixin
        api_key = self.get_api_key()
        if not api_key:
            raise ValueError(
                "Pinecone API key is required. Set PINECONE_API_KEY environment variable "
                "or provide api_key parameter."
            )

        return PineconeHybridSearchRetriever(
            api_key=api_key,
            environment=self.environment,
            index_name=self.index_name,
            top_k=self.top_k,
            alpha=self.alpha,
        )
