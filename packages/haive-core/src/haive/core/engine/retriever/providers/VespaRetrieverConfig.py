"""
Vespa Retriever implementation for the Haive framework.

This module provides a configuration class for the Vespa retriever,
which uses Vespa search engine for advanced search and retrieval capabilities.
Vespa is a fully featured search engine and vector database which supports
vector search, lexical search, and hybrid ranking in a single query.

The VespaRetriever works by:
1. Connecting to a Vespa application
2. Supporting both vector and text search simultaneously
3. Providing advanced ranking and filtering capabilities
4. Enabling real-time search and content updates

This retriever is particularly useful when:
- Need hybrid search combining vector and text search
- Require real-time search with continuous updates
- Want advanced ranking and relevance tuning
- Building large-scale search applications
- Need both structured and unstructured data search

The implementation integrates with LangChain's Vespa retriever while
providing a consistent Haive configuration interface.
"""

from typing import Any, Dict, List, Optional, Tuple, Type

from langchain_core.documents import Document
from pydantic import Field

from haive.core.engine.retriever.retriever import BaseRetrieverConfig
from haive.core.engine.retriever.types import RetrieverType


@BaseRetrieverConfig.register(RetrieverType.VESPA)
class VespaRetrieverConfig(BaseRetrieverConfig):
    """
    Configuration for Vespa retriever in the Haive framework.

    This retriever uses Vespa search engine to perform hybrid search
    combining vector similarity and text search capabilities.

    Attributes:
        retriever_type (RetrieverType): The type of retriever (always VESPA).
        url (str): Vespa application URL.
        content_field (str): Field containing document content.
        k (int): Number of documents to retrieve.
        metadata_fields (List[str]): Fields to include in metadata.
        vespa_query_body (Optional[Dict]): Custom Vespa query configuration.

    Examples:
        >>> from haive.core.engine.retriever import VespaRetrieverConfig
        >>>
        >>> # Create the Vespa retriever config
        >>> config = VespaRetrieverConfig(
        ...     name="vespa_retriever",
        ...     url="http://localhost:8080",
        ...     content_field="content",
        ...     k=10,
        ...     metadata_fields=["title", "author", "category"],
        ...     vespa_query_body={
        ...         "yql": "select * from sources * where userQuery()",
        ...         "hits": 10,
        ...         "ranking": "bm25"
        ...     }
        ... )
        >>>
        >>> # Instantiate and use the retriever
        >>> retriever = config.instantiate()
        >>> docs = retriever.get_relevant_documents("machine learning neural networks")
        >>>
        >>> # Example with hybrid search
        >>> hybrid_config = VespaRetrieverConfig(
        ...     name="vespa_hybrid_retriever",
        ...     url="http://localhost:8080",
        ...     content_field="content",
        ...     vespa_query_body={
        ...         "yql": "select * from sources * where ({targetHits:10}nearestNeighbor(embedding,q)) or userQuery()",
        ...         "ranking": "hybrid",
        ...         "input.query(q)": "embed(@query)"
        ...     }
        ... )
    """

    retriever_type: RetrieverType = Field(
        default=RetrieverType.VESPA, description="The type of retriever"
    )

    # Vespa connection configuration
    url: str = Field(
        ..., description="Vespa application URL (e.g., 'http://localhost:8080')"
    )

    content_field: str = Field(
        default="content", description="Field containing document content"
    )

    # Search parameters
    k: int = Field(
        default=10, ge=1, le=100, description="Number of documents to retrieve"
    )

    metadata_fields: List[str] = Field(
        default_factory=list,
        description="List of fields to include in document metadata",
    )

    # Vespa query configuration
    vespa_query_body: Optional[Dict[str, Any]] = Field(
        default=None, description="Custom Vespa query body configuration"
    )

    # Advanced parameters
    ranking_profile: str = Field(
        default="default", description="Vespa ranking profile to use"
    )

    query_model: str = Field(
        default="simple", description="Query model: 'simple', 'all', 'any', 'weakAnd'"
    )

    timeout: float = Field(
        default=30.0, ge=0.1, le=300.0, description="Query timeout in seconds"
    )

    def get_input_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return input field definitions for Vespa retriever."""
        return {
            "query": (str, Field(description="Search query for Vespa")),
        }

    def get_output_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return output field definitions for Vespa retriever."""
        return {
            "documents": (
                List[Document],
                Field(default_factory=list, description="Documents from Vespa search"),
            ),
        }

    def instantiate(self):
        """
        Create a Vespa retriever from this configuration.

        Returns:
            VespaRetriever: Instantiated retriever ready for hybrid search.

        Raises:
            ImportError: If required packages are not available.
            ValueError: If configuration is invalid.
        """
        try:
            from langchain_community.retrievers import VespaRetriever
        except ImportError:
            raise ImportError(
                "VespaRetriever requires langchain-community and pyvespa packages. "
                "Install with: pip install langchain-community pyvespa"
            )

        # Prepare configuration
        config = {"url": self.url, "content_field": self.content_field, "k": self.k}

        # Add metadata fields if specified
        if self.metadata_fields:
            config["metadata_fields"] = self.metadata_fields

        # Configure query body
        if self.vespa_query_body:
            query_body = self.vespa_query_body.copy()
        else:
            # Default query body
            query_body = {
                "yql": f"select * from sources * where userQuery()",
                "hits": self.k,
                "ranking": self.ranking_profile,
                "type": self.query_model,
                "timeout": f"{int(self.timeout * 1000)}ms",
            }

        config["vespa_query_body"] = query_body

        return VespaRetriever(**config)
