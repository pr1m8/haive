"""
Tavily Search API Retriever implementation for the Haive framework.

This module provides a configuration class for the Tavily Search API retriever, which
retrieves web search results using the Tavily search API service.

The TavilySearchAPIRetriever works by:
1. Taking a search query
2. Sending it to the Tavily Search API
3. Returning web search results as documents

This retriever is particularly useful when:
- Need access to current web information
- Building applications that require real-time search
- Combining web search with other retrieval methods
- Providing up-to-date information beyond training data

The implementation integrates with LangChain's TavilySearchAPIRetriever while providing
a consistent Haive configuration interface with secure API key management.
"""

from typing import Any, Dict, List, Optional, Tuple, Type

from langchain_core.documents import Document
from pydantic import Field, SecretStr

from haive.core.common.mixins.secure_config import SecureConfigMixin
from haive.core.engine.retriever.retriever import BaseRetrieverConfig
from haive.core.engine.retriever.types import RetrieverType


@BaseRetrieverConfig.register(RetrieverType.TAVILY_SEARCH_API)
class TavilySearchAPIRetrieverConfig(SecureConfigMixin, BaseRetrieverConfig):
    """
    Configuration for Tavily Search API retriever in the Haive framework.

    This retriever searches the web using the Tavily Search API and returns
    web search results as documents. It requires a Tavily API key.

    Attributes:
        retriever_type (RetrieverType): The type of retriever (always TAVILY_SEARCH_API).
        api_key (Optional[SecretStr]): Tavily API key (auto-resolved from TAVILY_API_KEY env var).
        k (int): Maximum number of search results to retrieve (default: 10).
        include_domains (Optional[List[str]]): Domains to include in search.
        exclude_domains (Optional[List[str]]): Domains to exclude from search.
        include_answer (bool): Whether to include answer in results (default: False).
        include_raw_content (bool): Whether to include raw content (default: False).

    Examples:
        >>> from haive.core.engine.retriever import TavilySearchAPIRetrieverConfig
        >>>
        >>> # Create the tavily search retriever config
        >>> config = TavilySearchAPIRetrieverConfig(
        ...     name="tavily_retriever",
        ...     k=5,
        ...     include_answer=True,
        ...     exclude_domains=["example.com"]
        ... )
        >>>
        >>> # Instantiate and use the retriever
        >>> retriever = config.instantiate()
        >>> docs = retriever.get_relevant_documents("latest AI developments 2024")
    """

    retriever_type: RetrieverType = Field(
        default=RetrieverType.TAVILY_SEARCH_API, description="The type of retriever"
    )

    # API configuration with SecureConfigMixin
    api_key: Optional[SecretStr] = Field(
        default=None, description="Tavily API key (auto-resolved from TAVILY_API_KEY)"
    )

    # Provider for SecureConfigMixin
    provider: str = Field(
        default="tavily", description="Provider name for API key resolution"
    )

    # Search configuration
    k: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Maximum number of search results to retrieve",
    )

    include_domains: Optional[List[str]] = Field(
        default=None, description="List of domains to include in search results"
    )

    exclude_domains: Optional[List[str]] = Field(
        default=None, description="List of domains to exclude from search results"
    )

    include_answer: bool = Field(
        default=False, description="Whether to include answer in search results"
    )

    include_raw_content: bool = Field(
        default=False, description="Whether to include raw content from web pages"
    )

    def get_input_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return input field definitions for Tavily Search API retriever."""
        return {
            "query": (str, Field(description="Web search query")),
        }

    def get_output_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return output field definitions for Tavily Search API retriever."""
        return {
            "documents": (
                List[Document],
                Field(
                    default_factory=list, description="Web search results from Tavily"
                ),
            ),
        }

    def instantiate(self):
        """
        Create a Tavily Search API retriever from this configuration.

        Returns:
            TavilySearchAPIRetriever: Instantiated retriever ready for web search.

        Raises:
            ImportError: If required packages are not available.
            ValueError: If API key is not available.
        """
        try:
            from langchain_community.retrievers import TavilySearchAPIRetriever
        except ImportError:
            raise ImportError(
                "TavilySearchAPIRetriever requires tavily-python package. "
                "Install with: pip install tavily-python"
            )

        # Get API key using SecureConfigMixin
        api_key = self.get_api_key()
        if not api_key:
            raise ValueError(
                "Tavily API key is required. Set TAVILY_API_KEY environment variable "
                "or provide api_key parameter."
            )

        # Prepare configuration
        config = {
            "api_key": api_key,
            "k": self.k,
            "include_answer": self.include_answer,
            "include_raw_content": self.include_raw_content,
        }

        if self.include_domains:
            config["include_domains"] = self.include_domains

        if self.exclude_domains:
            config["exclude_domains"] = self.exclude_domains

        return TavilySearchAPIRetriever(**config)
