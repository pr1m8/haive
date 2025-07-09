"""
Azure AI Search Retriever implementation for the Haive framework.

This module provides a configuration class for the Azure AI Search (formerly Azure Cognitive Search)
retriever, which retrieves documents from Azure's cloud search service.

The AzureAISearchRetriever works by:
1. Connecting to an Azure AI Search service
2. Executing search queries against indexed documents
3. Returning ranked search results as documents

This retriever is particularly useful when:
- Using Azure cloud infrastructure
- Need enterprise-grade search capabilities
- Working with large document collections in Azure
- Combining with other Azure AI services

The implementation integrates with LangChain's AzureAISearchRetriever while providing
a consistent Haive configuration interface with secure credential management.
"""

from typing import Any, Dict, List, Optional, Tuple, Type

from langchain_core.documents import Document
from pydantic import Field, SecretStr

from haive.core.common.mixins.secure_config import SecureConfigMixin
from haive.core.engine.retriever.retriever import BaseRetrieverConfig
from haive.core.engine.retriever.types import RetrieverType


@BaseRetrieverConfig.register(RetrieverType.AZURE_AI_SEARCH)
class AzureAISearchRetrieverConfig(SecureConfigMixin, BaseRetrieverConfig):
    """
    Configuration for Azure AI Search retriever in the Haive framework.

    This retriever searches documents in Azure AI Search service and returns
    ranked results. It requires Azure credentials and search service configuration.

    Attributes:
        retriever_type (RetrieverType): The type of retriever (always AZURE_AI_SEARCH).
        api_key (Optional[SecretStr]): Azure Search API key (auto-resolved from AZURE_SEARCH_API_KEY).
        azure_search_endpoint (str): Azure Search service endpoint URL.
        azure_search_index (str): Name of the search index to query.
        top_k (int): Number of documents to retrieve (default: 10).
        search_type (str): Type of search to perform (default: "similarity").
        semantic_configuration_name (Optional[str]): Name of semantic configuration to use.

    Examples:
        >>> from haive.core.engine.retriever import AzureAISearchRetrieverConfig
        >>>
        >>> # Create the azure ai search retriever config
        >>> config = AzureAISearchRetrieverConfig(
        ...     name="azure_search_retriever",
        ...     azure_search_endpoint="https://my-search-service.search.windows.net",
        ...     azure_search_index="documents-index",
        ...     top_k=5,
        ...     search_type="semantic"
        ... )
        >>>
        >>> # Instantiate and use the retriever
        >>> retriever = config.instantiate()
        >>> docs = retriever.get_relevant_documents("cloud computing benefits")
    """

    retriever_type: RetrieverType = Field(
        default=RetrieverType.AZURE_AI_SEARCH, description="The type of retriever"
    )

    # API configuration with SecureConfigMixin
    api_key: Optional[SecretStr] = Field(
        default=None,
        description="Azure Search API key (auto-resolved from AZURE_SEARCH_API_KEY)",
    )

    # Provider for SecureConfigMixin
    provider: str = Field(
        default="azure", description="Provider name for API key resolution"
    )

    # Azure Search configuration
    azure_search_endpoint: str = Field(
        ..., description="Azure Search service endpoint URL"
    )

    azure_search_index: str = Field(
        ..., description="Name of the search index to query"
    )

    top_k: int = Field(
        default=10, ge=1, le=50, description="Number of documents to retrieve"
    )

    search_type: str = Field(
        default="similarity",
        description="Type of search: 'similarity', 'semantic', 'hybrid'",
    )

    semantic_configuration_name: Optional[str] = Field(
        default=None, description="Name of semantic configuration for semantic search"
    )

    def get_input_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return input field definitions for Azure AI Search retriever."""
        return {
            "query": (str, Field(description="Search query for Azure AI Search")),
        }

    def get_output_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return output field definitions for Azure AI Search retriever."""
        return {
            "documents": (
                List[Document],
                Field(
                    default_factory=list, description="Documents from Azure AI Search"
                ),
            ),
        }

    def instantiate(self):
        """
        Create an Azure AI Search retriever from this configuration.

        Returns:
            AzureAISearchRetriever: Instantiated retriever ready for document retrieval.

        Raises:
            ImportError: If required packages are not available.
            ValueError: If API key or configuration is invalid.
        """
        try:
            from langchain_community.retrievers import AzureAISearchRetriever
        except ImportError:
            raise ImportError(
                "AzureAISearchRetriever requires azure-search-documents package. "
                "Install with: pip install azure-search-documents"
            )

        # Get API key using SecureConfigMixin
        api_key = self.get_api_key()
        if not api_key:
            raise ValueError(
                "Azure Search API key is required. Set AZURE_SEARCH_API_KEY environment variable "
                "or provide api_key parameter."
            )

        # Prepare configuration
        config = {
            "service_name": self.azure_search_endpoint.split("//")[1].split(".")[0],
            "index_name": self.azure_search_index,
            "api_key": api_key,
            "top_k": self.top_k,
            "search_type": self.search_type,
        }

        if self.semantic_configuration_name:
            config["semantic_configuration_name"] = self.semantic_configuration_name

        return AzureAISearchRetriever(**config)
