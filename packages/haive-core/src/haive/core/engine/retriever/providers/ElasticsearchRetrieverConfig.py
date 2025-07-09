"""
Elasticsearch Retriever implementation for the Haive framework.

This module provides a configuration class for the Elasticsearch retriever,
which performs full-text search and retrieval using Elasticsearch. Elasticsearch
is a distributed, RESTful search and analytics engine capable of solving complex
search problems and providing real-time search capabilities.

The ElasticsearchRetriever works by:
1. Connecting to an Elasticsearch cluster
2. Executing search queries with various scoring methods
3. Supporting both keyword and vector-based search
4. Returning ranked search results as documents

This retriever is particularly useful when:
- Working with large-scale document collections
- Need advanced search capabilities (faceting, aggregations, etc.)
- Require real-time search and indexing
- Building enterprise search applications
- Need scalable and distributed search infrastructure

The implementation integrates with LangChain's ElasticsearchRetriever while
providing a consistent Haive configuration interface with secure connection management.
"""

from typing import Any, Dict, List, Optional, Tuple, Type

from langchain_core.documents import Document
from pydantic import Field, SecretStr

from haive.core.common.mixins.secure_config import SecureConfigMixin
from haive.core.engine.retriever.retriever import BaseRetrieverConfig
from haive.core.engine.retriever.types import RetrieverType


@BaseRetrieverConfig.register(RetrieverType.ELASTICSEARCH)
class ElasticsearchRetrieverConfig(SecureConfigMixin, BaseRetrieverConfig):
    """
    Configuration for Elasticsearch retriever in the Haive framework.

    This retriever performs full-text search using Elasticsearch with support
    for various search types including keyword, vector, and hybrid search.

    Attributes:
        retriever_type (RetrieverType): The type of retriever (always ELASTICSEARCH).
        elasticsearch_url (str): Elasticsearch cluster URL.
        index_name (str): Name of the Elasticsearch index to search.
        username (Optional[str]): Username for Elasticsearch authentication.
        password (Optional[SecretStr]): Password for authentication (auto-resolved).
        k (int): Number of documents to retrieve.
        search_type (str): Type of search to perform.
        custom_query (Optional[Dict]): Custom Elasticsearch query DSL.

    Examples:
        >>> from haive.core.engine.retriever import ElasticsearchRetrieverConfig
        >>>
        >>> # Create the Elasticsearch retriever config
        >>> config = ElasticsearchRetrieverConfig(
        ...     name="elasticsearch_retriever",
        ...     elasticsearch_url="https://localhost:9200",
        ...     index_name="documents",
        ...     username="elastic",
        ...     k=10,
        ...     search_type="match"
        ... )
        >>>
        >>> # Instantiate and use the retriever
        >>> retriever = config.instantiate()
        >>> docs = retriever.get_relevant_documents("machine learning algorithms")
        >>>
        >>> # Example with custom query
        >>> custom_config = ElasticsearchRetrieverConfig(
        ...     name="custom_elasticsearch_retriever",
        ...     elasticsearch_url="https://localhost:9200",
        ...     index_name="documents",
        ...     custom_query={
        ...         "bool": {
        ...             "must": [{"match": {"content": "{query}"}}],
        ...             "filter": [{"range": {"date": {"gte": "2023-01-01"}}}]
        ...         }
        ...     }
        ... )
    """

    retriever_type: RetrieverType = Field(
        default=RetrieverType.ELASTICSEARCH, description="The type of retriever"
    )

    # Elasticsearch connection configuration
    elasticsearch_url: str = Field(
        ..., description="Elasticsearch cluster URL (e.g., 'https://localhost:9200')"
    )

    index_name: str = Field(
        ..., description="Name of the Elasticsearch index to search"
    )

    # Authentication with SecureConfigMixin
    username: Optional[str] = Field(
        default=None, description="Username for Elasticsearch authentication"
    )

    api_key: Optional[SecretStr] = Field(
        default=None,
        description="Elasticsearch API key or password (auto-resolved from ELASTICSEARCH_API_KEY)",
    )

    # Provider for SecureConfigMixin
    provider: str = Field(
        default="elasticsearch", description="Provider name for credential resolution"
    )

    # Search configuration
    k: int = Field(
        default=10, ge=1, le=100, description="Number of documents to retrieve"
    )

    search_type: str = Field(
        default="match",
        description="Search type: 'match', 'multi_match', 'bool', 'fuzzy', 'custom'",
    )

    # Advanced configuration
    custom_query: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Custom Elasticsearch query DSL (overrides search_type)",
    )

    source_fields: Optional[List[str]] = Field(
        default=None, description="Specific fields to retrieve from documents"
    )

    # Connection parameters
    verify_certs: bool = Field(
        default=True, description="Whether to verify SSL certificates"
    )

    timeout: int = Field(
        default=30, ge=1, le=300, description="Request timeout in seconds"
    )

    def get_input_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return input field definitions for Elasticsearch retriever."""
        return {
            "query": (str, Field(description="Search query for Elasticsearch")),
        }

    def get_output_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return output field definitions for Elasticsearch retriever."""
        return {
            "documents": (
                List[Document],
                Field(
                    default_factory=list,
                    description="Documents from Elasticsearch search",
                ),
            ),
        }

    def instantiate(self):
        """
        Create an Elasticsearch retriever from this configuration.

        Returns:
            ElasticsearchRetriever: Instantiated retriever ready for search.

        Raises:
            ImportError: If required packages are not available.
            ValueError: If connection configuration is invalid.
        """
        try:
            from elasticsearch import Elasticsearch
            from langchain_community.retrievers import ElasticsearchRetriever
        except ImportError:
            raise ImportError(
                "ElasticsearchRetriever requires langchain-community and elasticsearch packages. "
                "Install with: pip install langchain-community elasticsearch"
            )

        # Prepare connection configuration
        es_config = {
            "hosts": [self.elasticsearch_url],
            "verify_certs": self.verify_certs,
            "timeout": self.timeout,
        }

        # Add authentication if provided
        if self.username:
            api_key = self.get_api_key()
            if api_key:
                es_config["basic_auth"] = (self.username, api_key)
            else:
                es_config["basic_auth"] = (
                    self.username,
                    self.api_key.get_secret_value() if self.api_key else "",
                )

        # Create Elasticsearch client
        es_client = Elasticsearch(**es_config)

        # Prepare retriever configuration
        retriever_config = {
            "es_client": es_client,
            "index_name": self.index_name,
            "k": self.k,
        }

        # Add search configuration
        if self.custom_query:
            retriever_config["body_func"] = lambda query: self._build_custom_query(
                query
            )
        else:
            retriever_config["body_func"] = lambda query: self._build_standard_query(
                query
            )

        if self.source_fields:
            retriever_config["source_fields"] = self.source_fields

        return ElasticsearchRetriever(**retriever_config)

    def _build_standard_query(self, query: str) -> Dict[str, Any]:
        """Build standard Elasticsearch query based on search_type."""
        if self.search_type == "match":
            return {"query": {"match": {"content": query}}}
        elif self.search_type == "multi_match":
            return {
                "query": {
                    "multi_match": {
                        "query": query,
                        "fields": ["title^2", "content", "keywords"],
                    }
                }
            }
        elif self.search_type == "fuzzy":
            return {
                "query": {"fuzzy": {"content": {"value": query, "fuzziness": "AUTO"}}}
            }
        else:
            # Default to match
            return {"query": {"match": {"content": query}}}

    def _build_custom_query(self, query: str) -> Dict[str, Any]:
        """Build custom Elasticsearch query from template."""
        import json

        # Replace {query} placeholder in custom query
        query_str = json.dumps(self.custom_query)
        query_str = query_str.replace("{query}", query)
        return json.loads(query_str)
