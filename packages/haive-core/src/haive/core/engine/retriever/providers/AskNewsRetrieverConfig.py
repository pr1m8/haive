"""
AskNews Retriever implementation for the Haive framework.

This module provides a configuration class for the AskNews retriever,
which retrieves news articles and current events using AskNews API.
AskNews provides access to real-time news content from various sources
with filtering and categorization capabilities.

The AskNewsRetriever works by:
1. Connecting to the AskNews API
2. Executing news search queries with filters
3. Retrieving relevant news articles and metadata
4. Returning formatted documents with news content

This retriever is particularly useful when:
- Building news aggregation applications
- Need real-time current events information
- Creating content monitoring systems
- Building fact-checking or research tools
- Want categorized and filtered news content

The implementation integrates with LangChain's AskNewsRetriever while
providing a consistent Haive configuration interface with secure API key management.
"""

from typing import Any, Dict, List, Optional, Tuple, Type

from langchain_core.documents import Document
from pydantic import Field, SecretStr

from haive.core.common.mixins.secure_config import SecureConfigMixin
from haive.core.engine.retriever.retriever import BaseRetrieverConfig
from haive.core.engine.retriever.types import RetrieverType


@BaseRetrieverConfig.register(RetrieverType.ASK_NEWS)
class AskNewsRetrieverConfig(SecureConfigMixin, BaseRetrieverConfig):
    """
    Configuration for AskNews retriever in the Haive framework.

    This retriever searches news articles using AskNews API and returns
    relevant news content with metadata and categorization.

    Attributes:
        retriever_type (RetrieverType): The type of retriever (always ASK_NEWS).
        api_key (Optional[SecretStr]): AskNews API key (auto-resolved from ASKNEWS_API_KEY).
        k (int): Number of news articles to retrieve.
        categories (Optional[List[str]]): News categories to filter by.
        sources (Optional[List[str]]): Specific news sources to include.
        hours_back (int): How many hours back to search for news.

    Examples:
        >>> from haive.core.engine.retriever import AskNewsRetrieverConfig
        >>>
        >>> # Create the AskNews retriever config
        >>> config = AskNewsRetrieverConfig(
        ...     name="news_retriever",
        ...     k=10,
        ...     categories=["technology", "science"],
        ...     hours_back=24
        ... )
        >>>
        >>> # Instantiate and use the retriever
        >>> retriever = config.instantiate()
        >>> docs = retriever.get_relevant_documents("artificial intelligence breakthrough")
        >>>
        >>> # Example with specific sources
        >>> tech_config = AskNewsRetrieverConfig(
        ...     name="tech_news_retriever",
        ...     k=5,
        ...     sources=["techcrunch", "wired", "arstechnica"],
        ...     hours_back=12
        ... )
    """

    retriever_type: RetrieverType = Field(
        default=RetrieverType.ASK_NEWS, description="The type of retriever"
    )

    # API configuration with SecureConfigMixin
    api_key: Optional[SecretStr] = Field(
        default=None, description="AskNews API key (auto-resolved from ASKNEWS_API_KEY)"
    )

    # Provider for SecureConfigMixin
    provider: str = Field(
        default="asknews", description="Provider name for API key resolution"
    )

    # Search parameters
    k: int = Field(
        default=10, ge=1, le=100, description="Number of news articles to retrieve"
    )

    categories: Optional[List[str]] = Field(
        default=None,
        description="News categories to filter by (e.g., ['technology', 'science', 'business'])",
    )

    sources: Optional[List[str]] = Field(
        default=None,
        description="Specific news sources to include (e.g., ['reuters', 'bbc', 'cnn'])",
    )

    hours_back: int = Field(
        default=24,
        ge=1,
        le=168,  # 1 week max
        description="How many hours back to search for news",
    )

    # Advanced filtering
    language: str = Field(
        default="en",
        description="Language code for news articles (e.g., 'en', 'es', 'fr')",
    )

    sort_by: str = Field(
        default="relevance", description="Sort order: 'relevance', 'date', 'popularity'"
    )

    include_domains: Optional[List[str]] = Field(
        default=None, description="Specific domains to include in search"
    )

    exclude_domains: Optional[List[str]] = Field(
        default=None, description="Specific domains to exclude from search"
    )

    def get_input_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return input field definitions for AskNews retriever."""
        return {
            "query": (str, Field(description="News search query for AskNews")),
        }

    def get_output_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return output field definitions for AskNews retriever."""
        return {
            "documents": (
                List[Document],
                Field(default_factory=list, description="News articles from AskNews"),
            ),
        }

    def instantiate(self):
        """
        Create an AskNews retriever from this configuration.

        Returns:
            AskNewsRetriever: Instantiated retriever ready for news search.

        Raises:
            ImportError: If required packages are not available.
            ValueError: If API key or configuration is invalid.
        """
        try:
            from langchain_community.retrievers import AskNewsRetriever
        except ImportError:
            raise ImportError(
                "AskNewsRetriever requires langchain-community package. "
                "Install with: pip install langchain-community"
            )

        # Get API key using SecureConfigMixin
        api_key = self.get_api_key()
        if not api_key:
            raise ValueError(
                "AskNews API key is required. Set ASKNEWS_API_KEY environment variable "
                "or provide api_key parameter."
            )

        # Prepare configuration
        config = {
            "api_key": api_key,
            "k": self.k,
            "hours_back": self.hours_back,
            "language": self.language,
            "sort_by": self.sort_by,
        }

        # Add optional filters
        if self.categories:
            config["categories"] = self.categories

        if self.sources:
            config["sources"] = self.sources

        if self.include_domains:
            config["include_domains"] = self.include_domains

        if self.exclude_domains:
            config["exclude_domains"] = self.exclude_domains

        return AskNewsRetriever(**config)
