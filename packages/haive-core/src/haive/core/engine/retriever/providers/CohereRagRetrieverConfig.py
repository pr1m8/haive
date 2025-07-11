"""Cohere RAG Retriever implementation for the Haive framework.

This module provides a configuration class for the Cohere RAG retriever,
which uses Cohere's Retrieval-Augmented Generation API for document retrieval
and generation. Cohere RAG provides enterprise-grade retrieval with built-in
re-ranking, citation capabilities, and optimized retrieval performance.

The CohereRagRetriever works by:
1. Using Cohere's RAG API for retrieval and generation
2. Automatically re-ranking results for relevance
3. Providing citations and source attribution
4. Supporting various document sources and connectors

This retriever is particularly useful when:
- Need enterprise-grade RAG capabilities
- Want built-in re-ranking and citation features
- Building production RAG applications
- Need reliable and optimized retrieval performance
- Working with large document collections

The implementation integrates with LangChain's CohereRagRetriever while
providing a consistent Haive configuration interface with secure API key management.
"""

from typing import Any, Dict, List, Optional, Tuple, Type

from langchain_core.documents import Document
from pydantic import Field, SecretStr

from haive.core.common.mixins.secure_config import SecureConfigMixin
from haive.core.engine.retriever.retriever import BaseRetrieverConfig
from haive.core.engine.retriever.types import RetrieverType


@BaseRetrieverConfig.register(RetrieverType.COHERE_RAG)
class CohereRagRetrieverConfig(SecureConfigMixin, BaseRetrieverConfig):
    """Configuration for Cohere RAG retriever in the Haive framework.

    This retriever uses Cohere's RAG API to provide enterprise-grade retrieval
    with built-in re-ranking, citations, and optimized performance.

    Attributes:
        retriever_type (RetrieverType): The type of retriever (always COHERE_RAG).
        api_key (Optional[SecretStr]): Cohere API key (auto-resolved from COHERE_API_KEY).
        connectors (List[Dict]): Cohere connector configurations for data sources.
        top_k (int): Number of documents to retrieve.
        rerank (bool): Whether to use Cohere's re-ranking.
        max_tokens (int): Maximum tokens for generation.
        temperature (float): Temperature for generation.

    Examples:
        >>> from haive.core.engine.retriever import CohereRagRetrieverConfig
        >>>
        >>> # Create the Cohere RAG retriever config
        >>> config = CohereRagRetrieverConfig(
        ...     name="cohere_rag_retriever",
        ...     connectors=[
        ...         {
        ...             "id": "web-search",
        ...             "continue_on_failure": True,
        ...             "options": {"site": "wikipedia.org"}
        ...         }
        ...     ],
        ...     top_k=10,
        ...     rerank=True,
        ...     temperature=0.1
        ... )
        >>>
        >>> # Instantiate and use the retriever
        >>> retriever = config.instantiate()
        >>> docs = retriever.get_relevant_documents("explain quantum computing principles")
        >>>
        >>> # Example with custom connector
        >>> custom_config = CohereRagRetrieverConfig(
        ...     name="custom_cohere_rag",
        ...     connectors=[
        ...         {
        ...             "id": "custom-docs",
        ...             "user_access_token": "your-token",
        ...             "continue_on_failure": False
        ...         }
        ...     ],
        ...     top_k=5
        ... )
    """

    retriever_type: RetrieverType = Field(
        default=RetrieverType.COHERE_RAG, description="The type of retriever"
    )

    # API configuration with SecureConfigMixin
    api_key: SecretStr | None = Field(
        default=None, description="Cohere API key (auto-resolved from COHERE_API_KEY)"
    )

    # Provider for SecureConfigMixin
    provider: str = Field(
        default="cohere", description="Provider name for API key resolution"
    )

    # Cohere RAG configuration
    connectors: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Cohere connector configurations for data sources",
    )

    top_k: int = Field(
        default=10, ge=1, le=50, description="Number of documents to retrieve"
    )

    # Retrieval parameters
    rerank: bool = Field(
        default=True,
        description="Whether to use Cohere's re-ranking for better relevance",
    )

    # Generation parameters (for RAG)
    max_tokens: int = Field(
        default=1000, ge=1, le=4000, description="Maximum tokens for generation"
    )

    temperature: float = Field(
        default=0.1,
        ge=0.0,
        le=2.0,
        description="Temperature for generation (0.0 = deterministic, 2.0 = very random)",
    )

    # Search parameters
    search_queries_only: bool = Field(
        default=False,
        description="Whether to only return search queries without generation",
    )

    citation_quality: str = Field(
        default="accurate", description="Citation quality: 'fast', 'accurate'"
    )

    def get_input_fields(self) -> dict[str, tuple[type, Any]]:
        """Return input field definitions for Cohere RAG retriever."""
        return {
            "query": (
                str,
                Field(description="Query for Cohere RAG retrieval and generation"),
            ),
        }

    def get_output_fields(self) -> dict[str, tuple[type, Any]]:
        """Return output field definitions for Cohere RAG retriever."""
        return {
            "documents": (
                list[Document],
                Field(
                    default_factory=list,
                    description="Documents with citations from Cohere RAG",
                ),
            ),
        }

    def instantiate(self):
        """Create a Cohere RAG retriever from this configuration.

        Returns:
            CohereRagRetriever: Instantiated retriever ready for RAG operations.

        Raises:
            ImportError: If required packages are not available.
            ValueError: If API key or configuration is invalid.
        """
        try:
            from langchain_community.retrievers import CohereRagRetriever
        except ImportError:
            raise ImportError(
                "CohereRagRetriever requires langchain-community and cohere packages. "
                "Install with: pip install langchain-community cohere"
            )

        # Get API key using SecureConfigMixin
        api_key = self.get_api_key()
        if not api_key:
            raise ValueError(
                "Cohere API key is required. Set COHERE_API_KEY environment variable "
                "or provide api_key parameter."
            )

        if not self.connectors:
            # Default to web search if no connectors specified
            connectors = [{"id": "web-search", "continue_on_failure": True}]
        else:
            connectors = self.connectors

        # Prepare configuration
        config = {
            "llm": None,  # Will use Cohere's default
            "connectors": connectors,
            "top_k": self.top_k,
            "rerank": self.rerank,
        }

        # Add generation parameters
        if not self.search_queries_only:
            config.update(
                {
                    "max_tokens": self.max_tokens,
                    "temperature": self.temperature,
                    "citation_quality": self.citation_quality,
                }
            )

        return CohereRagRetriever(cohere_api_key=api_key, **config)
