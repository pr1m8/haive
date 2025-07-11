"""Metal Retriever implementation for the Haive framework.

This module provides a configuration class for the Metal retriever,
which uses Metal's vector search infrastructure for high-performance
similarity search. Metal provides a managed vector database service
optimized for production use cases.

The MetalRetriever works by:
1. Connecting to a Metal index
2. Performing vector similarity search
3. Supporting metadata filtering and search
4. Providing production-ready vector infrastructure

This retriever is particularly useful when:
- Need managed vector search infrastructure
- Building production vector search applications
- Want optimized performance and scaling
- Need reliable vector database service
- Building recommendation or search systems

The implementation integrates with LangChain's MetalRetriever while
providing a consistent Haive configuration interface with secure API key management.
"""

from typing import Any, Dict, List, Optional, Tuple, Type

from langchain_core.documents import Document
from pydantic import Field, SecretStr

from haive.core.common.mixins.secure_config import SecureConfigMixin
from haive.core.engine.retriever.retriever import BaseRetrieverConfig
from haive.core.engine.retriever.types import RetrieverType


@BaseRetrieverConfig.register(RetrieverType.METAL)
class MetalRetrieverConfig(SecureConfigMixin, BaseRetrieverConfig):
    """Configuration for Metal retriever in the Haive framework.

    This retriever uses Metal's vector search infrastructure to provide
    high-performance similarity search with managed scaling and reliability.

    Attributes:
        retriever_type (RetrieverType): The type of retriever (always METAL).
        metal_api_key (Optional[SecretStr]): Metal API key (auto-resolved from METAL_API_KEY).
        metal_client_id (Optional[SecretStr]): Metal client ID (auto-resolved from METAL_CLIENT_ID).
        index_id (str): Metal index ID for the vector collection.
        k (int): Number of documents to retrieve.
        filters (Optional[Dict]): Metadata filters for search results.

    Examples:
        >>> from haive.core.engine.retriever import MetalRetrieverConfig
        >>>
        >>> # Create the Metal retriever config
        >>> config = MetalRetrieverConfig(
        ...     name="metal_retriever",
        ...     index_id="my-metal-index-123",
        ...     k=10
        ... )
        >>>
        >>> # Instantiate and use the retriever
        >>> retriever = config.instantiate()
        >>> docs = retriever.get_relevant_documents("machine learning algorithms")
        >>>
        >>> # Example with metadata filtering
        >>> filtered_config = MetalRetrieverConfig(
        ...     name="filtered_metal_retriever",
        ...     index_id="my-metal-index-123",
        ...     k=5,
        ...     filters={
        ...         "category": "technology",
        ...         "published_year": {"$gte": 2020}
        ...     }
        ... )
    """

    retriever_type: RetrieverType = Field(
        default=RetrieverType.METAL, description="The type of retriever"
    )

    # Metal configuration
    index_id: str = Field(..., description="Metal index ID for the vector collection")

    # API configuration with SecureConfigMixin
    api_key: SecretStr | None = Field(
        default=None, description="Metal API key (auto-resolved from METAL_API_KEY)"
    )

    metal_client_id: SecretStr | None = Field(
        default=None, description="Metal client ID (auto-resolved from METAL_CLIENT_ID)"
    )

    # Provider for SecureConfigMixin
    provider: str = Field(
        default="metal", description="Provider name for API key resolution"
    )

    # Search parameters
    k: int = Field(
        default=10, ge=1, le=100, description="Number of documents to retrieve"
    )

    filters: dict[str, Any] | None = Field(
        default=None, description="Metadata filters for search results"
    )

    # Advanced search parameters
    include_values: bool = Field(
        default=True, description="Whether to include vector values in response"
    )

    include_metadata: bool = Field(
        default=True, description="Whether to include metadata in response"
    )

    # Metal-specific parameters
    namespace: str | None = Field(
        default=None, description="Metal namespace for partitioning data"
    )

    top_k: int | None = Field(
        default=None, description="Alias for k parameter (for compatibility)"
    )

    def get_input_fields(self) -> dict[str, tuple[type, Any]]:
        """Return input field definitions for Metal retriever."""
        return {
            "query": (str, Field(description="Vector search query for Metal")),
        }

    def get_output_fields(self) -> dict[str, tuple[type, Any]]:
        """Return output field definitions for Metal retriever."""
        return {
            "documents": (
                list[Document],
                Field(
                    default_factory=list,
                    description="Documents from Metal vector search",
                ),
            ),
        }

    def instantiate(self):
        """Create a Metal retriever from this configuration.

        Returns:
            MetalRetriever: Instantiated retriever ready for vector search.

        Raises:
            ImportError: If required packages are not available.
            ValueError: If API key or configuration is invalid.
        """
        try:
            from langchain_community.retrievers import MetalRetriever
        except ImportError:
            raise ImportError(
                "MetalRetriever requires langchain-community and metal_sdk packages. "
                "Install with: pip install langchain-community metal_sdk"
            )

        # Get API credentials using SecureConfigMixin
        api_key = self.get_api_key()
        if not api_key:
            raise ValueError(
                "Metal API key is required. Set METAL_API_KEY environment variable "
                "or provide api_key parameter."
            )

        client_id = (
            self.metal_client_id.get_secret_value() if self.metal_client_id else None
        )
        if not client_id:
            raise ValueError(
                "Metal client ID is required. Set METAL_CLIENT_ID environment variable "
                "or provide metal_client_id parameter."
            )

        # Prepare configuration
        config = {
            "metal_api_key": api_key,
            "metal_client_id": client_id,
            "index_id": self.index_id,
            "k": self.k,
        }

        # Add optional parameters
        if self.filters:
            config["filters"] = self.filters

        if self.namespace:
            config["namespace"] = self.namespace

        config["include_values"] = self.include_values
        config["include_metadata"] = self.include_metadata

        # Use top_k if specified (compatibility)
        if self.top_k:
            config["k"] = self.top_k

        return MetalRetriever(**config)
