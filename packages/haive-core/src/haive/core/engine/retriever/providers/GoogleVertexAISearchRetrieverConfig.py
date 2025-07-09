"""
Google Vertex AI Search Retriever implementation for the Haive framework.

This module provides a configuration class for the Google Vertex AI Search retriever,
which uses Google Cloud's Vertex AI Search (formerly Enterprise Search) service.
Vertex AI Search provides ML-powered search capabilities with natural language
understanding and enterprise-grade security and compliance.

The GoogleVertexAISearchRetriever works by:
1. Connecting to a Vertex AI Search data store
2. Executing search queries with ML understanding
3. Returning ranked results with relevance scoring
4. Supporting various data source types and formats

This retriever is particularly useful when:
- Building enterprise search on Google Cloud
- Need ML-powered query understanding
- Working with Google Cloud data sources
- Want enterprise security and compliance
- Building knowledge management systems

The implementation integrates with LangChain's GoogleVertexAISearchRetriever while
providing a consistent Haive configuration interface with secure GCP credential management.
"""

from typing import Any, Dict, List, Optional, Tuple, Type

from langchain_core.documents import Document
from pydantic import Field, SecretStr

from haive.core.common.mixins.secure_config import SecureConfigMixin
from haive.core.engine.retriever.retriever import BaseRetrieverConfig
from haive.core.engine.retriever.types import RetrieverType


@BaseRetrieverConfig.register(RetrieverType.GOOGLE_VERTEX_AI_SEARCH)
class GoogleVertexAISearchRetrieverConfig(SecureConfigMixin, BaseRetrieverConfig):
    """
    Configuration for Google Vertex AI Search retriever in the Haive framework.

    This retriever uses Google Cloud Vertex AI Search to provide ML-powered
    enterprise search with natural language understanding.

    Attributes:
        retriever_type (RetrieverType): The type of retriever (always GOOGLE_VERTEX_AI_SEARCH).
        project_id (str): Google Cloud project ID.
        data_store_id (str): Vertex AI Search data store ID.
        location_id (str): Google Cloud location ID.
        serving_config_id (str): Serving configuration ID.
        api_key (Optional[SecretStr]): Service account key (auto-resolved from GOOGLE_APPLICATION_CREDENTIALS).
        max_documents (int): Maximum number of documents to retrieve.

    Examples:
        >>> from haive.core.engine.retriever import GoogleVertexAISearchRetrieverConfig
        >>>
        >>> # Create the Vertex AI Search retriever config
        >>> config = GoogleVertexAISearchRetrieverConfig(
        ...     name="vertex_search_retriever",
        ...     project_id="my-gcp-project",
        ...     data_store_id="my-data-store",
        ...     location_id="global",
        ...     serving_config_id="default_config",
        ...     max_documents=10
        ... )
        >>>
        >>> # Instantiate and use the retriever
        >>> retriever = config.instantiate()
        >>> docs = retriever.get_relevant_documents("enterprise search capabilities")
        >>>
        >>> # Example with regional deployment
        >>> regional_config = GoogleVertexAISearchRetrieverConfig(
        ...     name="regional_vertex_search",
        ...     project_id="my-gcp-project",
        ...     data_store_id="my-data-store",
        ...     location_id="us-central1",
        ...     serving_config_id="custom_config"
        ... )
    """

    retriever_type: RetrieverType = Field(
        default=RetrieverType.GOOGLE_VERTEX_AI_SEARCH,
        description="The type of retriever",
    )

    # Google Cloud configuration
    project_id: str = Field(..., description="Google Cloud project ID")

    data_store_id: str = Field(..., description="Vertex AI Search data store ID")

    location_id: str = Field(
        default="global",
        description="Google Cloud location ID (e.g., 'global', 'us-central1')",
    )

    serving_config_id: str = Field(
        default="default_config", description="Serving configuration ID"
    )

    # API configuration with SecureConfigMixin
    api_key: Optional[SecretStr] = Field(
        default=None,
        description="Service account key path (auto-resolved from GOOGLE_APPLICATION_CREDENTIALS)",
    )

    # Provider for SecureConfigMixin
    provider: str = Field(
        default="google", description="Provider name for credential resolution"
    )

    # Search parameters
    max_documents: int = Field(
        default=10, ge=1, le=100, description="Maximum number of documents to retrieve"
    )

    # Advanced search parameters
    filter_expression: Optional[str] = Field(
        default=None, description="Filter expression for search results"
    )

    order_by: Optional[str] = Field(
        default=None, description="Order by expression for result ranking"
    )

    boost_spec: Optional[Dict[str, Any]] = Field(
        default=None, description="Boost specification for custom ranking"
    )

    # Query expansion and spell correction
    query_expansion_spec: Optional[Dict[str, Any]] = Field(
        default=None, description="Query expansion configuration"
    )

    spell_correction_spec: Optional[Dict[str, Any]] = Field(
        default=None, description="Spell correction configuration"
    )

    def get_input_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return input field definitions for Google Vertex AI Search retriever."""
        return {
            "query": (str, Field(description="Search query for Vertex AI Search")),
        }

    def get_output_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return output field definitions for Google Vertex AI Search retriever."""
        return {
            "documents": (
                List[Document],
                Field(
                    default_factory=list, description="Documents from Vertex AI Search"
                ),
            ),
        }

    def instantiate(self):
        """
        Create a Google Vertex AI Search retriever from this configuration.

        Returns:
            GoogleVertexAISearchRetriever: Instantiated retriever ready for enterprise search.

        Raises:
            ImportError: If required packages are not available.
            ValueError: If GCP credentials or configuration is invalid.
        """
        try:
            from langchain_google_vertexai import VertexAISearchRetriever
        except ImportError:
            raise ImportError(
                "GoogleVertexAISearchRetriever requires langchain-google-vertexai package. "
                "Install with: pip install langchain-google-vertexai"
            )

        # Prepare configuration
        config = {
            "project_id": self.project_id,
            "data_store_id": self.data_store_id,
            "location_id": self.location_id,
            "serving_config_id": self.serving_config_id,
            "max_documents": self.max_documents,
        }

        # Add optional search parameters
        if self.filter_expression:
            config["filter"] = self.filter_expression

        if self.order_by:
            config["order_by"] = self.order_by

        if self.boost_spec:
            config["boost_spec"] = self.boost_spec

        if self.query_expansion_spec:
            config["query_expansion_spec"] = self.query_expansion_spec

        if self.spell_correction_spec:
            config["spell_correction_spec"] = self.spell_correction_spec

        # Handle credentials
        credentials_path = self.get_api_key()
        if credentials_path:
            import os

            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

        return VertexAISearchRetriever(**config)
