"""
Weaviate Hybrid Search Retriever implementation for the Haive framework.

This module provides a configuration class for the Weaviate Hybrid Search retriever,
which combines vector similarity search with keyword search using Weaviate's
hybrid search capabilities. Weaviate is an open-source vector database that
supports both vector and keyword search in a single query.

The WeaviateHybridSearchRetriever works by:
1. Connecting to a Weaviate instance
2. Performing both vector and keyword search simultaneously
3. Combining results using Weaviate's hybrid ranking algorithm
4. Supporting advanced filtering and where clauses

This retriever is particularly useful when:
- Need both semantic and keyword search
- Want optimized hybrid search performance
- Building applications with diverse query types
- Using Weaviate as the vector database
- Need flexible filtering capabilities

The implementation integrates with LangChain's WeaviateHybridSearchRetriever while
providing a consistent Haive configuration interface with secure API key management.
"""

from typing import Any, Dict, List, Optional, Tuple, Type

from langchain_core.documents import Document
from pydantic import Field, SecretStr

from haive.core.common.mixins.secure_config import SecureConfigMixin
from haive.core.engine.retriever.retriever import BaseRetrieverConfig
from haive.core.engine.retriever.types import RetrieverType


@BaseRetrieverConfig.register(RetrieverType.WEAVIATE_HYBRID_SEARCH)
class WeaviateHybridSearchRetrieverConfig(SecureConfigMixin, BaseRetrieverConfig):
    """
    Configuration for Weaviate Hybrid Search retriever in the Haive framework.

    This retriever uses Weaviate's hybrid search capabilities to combine vector
    similarity search with keyword search for comprehensive retrieval.

    Attributes:
        retriever_type (RetrieverType): The type of retriever (always WEAVIATE_HYBRID_SEARCH).
        weaviate_url (str): Weaviate instance URL.
        index_name (str): Name of the Weaviate class/index.
        api_key (Optional[SecretStr]): Weaviate API key (auto-resolved from WEAVIATE_API_KEY).
        k (int): Number of documents to retrieve.
        alpha (float): Balance between vector and keyword search.
        where_filter (Optional[Dict]): Weaviate where clause for filtering.

    Examples:
        >>> from haive.core.engine.retriever import WeaviateHybridSearchRetrieverConfig
        >>>
        >>> # Create the Weaviate hybrid search retriever config
        >>> config = WeaviateHybridSearchRetrieverConfig(
        ...     name="weaviate_hybrid_retriever",
        ...     weaviate_url="https://my-cluster.weaviate.network",
        ...     index_name="Document",
        ...     k=10,
        ...     alpha=0.5  # Equal weight to vector and keyword search
        ... )
        >>>
        >>> # Instantiate and use the retriever
        >>> retriever = config.instantiate()
        >>> docs = retriever.get_relevant_documents("machine learning algorithms")
        >>>
        >>> # Example with filtering
        >>> filtered_config = WeaviateHybridSearchRetrieverConfig(
        ...     name="filtered_weaviate_hybrid",
        ...     weaviate_url="https://my-cluster.weaviate.network",
        ...     index_name="Document",
        ...     where_filter={
        ...         "path": ["category"],
        ...         "operator": "Equal",
        ...         "valueText": "technology"
        ...     }
        ... )
    """

    retriever_type: RetrieverType = Field(
        default=RetrieverType.WEAVIATE_HYBRID_SEARCH,
        description="The type of retriever",
    )

    # Weaviate connection configuration
    weaviate_url: str = Field(
        ...,
        description="Weaviate instance URL (e.g., 'https://my-cluster.weaviate.network')",
    )

    index_name: str = Field(
        ..., description="Name of the Weaviate class/index to search"
    )

    # API configuration with SecureConfigMixin
    api_key: Optional[SecretStr] = Field(
        default=None,
        description="Weaviate API key (auto-resolved from WEAVIATE_API_KEY)",
    )

    # Provider for SecureConfigMixin
    provider: str = Field(
        default="weaviate", description="Provider name for API key resolution"
    )

    # Search parameters
    k: int = Field(
        default=10, ge=1, le=100, description="Number of documents to retrieve"
    )

    alpha: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Balance between vector (1.0) and keyword (0.0) search",
    )

    # Filtering and where clauses
    where_filter: Optional[Dict[str, Any]] = Field(
        default=None, description="Weaviate where clause for filtering results"
    )

    # Advanced search parameters
    text_key: str = Field(
        default="text", description="Property name containing the text content"
    )

    attributes: Optional[List[str]] = Field(
        default=None, description="List of properties to return in results"
    )

    # Connection parameters
    timeout_config: Optional[Tuple[int, int]] = Field(
        default=None,
        description="Timeout configuration as (connect_timeout, read_timeout)",
    )

    additional_headers: Optional[Dict[str, str]] = Field(
        default=None, description="Additional headers for Weaviate requests"
    )

    def get_input_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return input field definitions for Weaviate Hybrid Search retriever."""
        return {
            "query": (str, Field(description="Hybrid search query for Weaviate")),
        }

    def get_output_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return output field definitions for Weaviate Hybrid Search retriever."""
        return {
            "documents": (
                List[Document],
                Field(
                    default_factory=list,
                    description="Documents from Weaviate hybrid search",
                ),
            ),
        }

    def instantiate(self):
        """
        Create a Weaviate Hybrid Search retriever from this configuration.

        Returns:
            WeaviateHybridSearchRetriever: Instantiated retriever ready for hybrid search.

        Raises:
            ImportError: If required packages are not available.
            ValueError: If API key or configuration is invalid.
        """
        try:
            import weaviate
            from langchain_weaviate.retrievers import WeaviateHybridSearchRetriever
        except ImportError:
            raise ImportError(
                "WeaviateHybridSearchRetriever requires langchain-weaviate and weaviate-client packages. "
                "Install with: pip install langchain-weaviate weaviate-client"
            )

        # Get API key using SecureConfigMixin
        api_key = self.get_api_key()

        # Prepare connection configuration
        auth_config = None
        if api_key:
            auth_config = weaviate.AuthApiKey(api_key=api_key)

        # Additional connection parameters
        additional_config = {}
        if self.timeout_config:
            additional_config["timeout_config"] = self.timeout_config

        if self.additional_headers:
            additional_config["additional_headers"] = self.additional_headers

        # Create Weaviate client
        client = weaviate.Client(
            url=self.weaviate_url, auth_client_secret=auth_config, **additional_config
        )

        # Prepare retriever configuration
        config = {
            "client": client,
            "index_name": self.index_name,
            "text_key": self.text_key,
            "k": self.k,
            "alpha": self.alpha,
        }

        # Add optional parameters
        if self.where_filter:
            config["where_filter"] = self.where_filter

        if self.attributes:
            config["attributes"] = self.attributes

        return WeaviateHybridSearchRetriever(**config)
