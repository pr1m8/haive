"""
You.com Retriever implementation for the Haive framework.

This module provides a configuration class for the You.com retriever,
which retrieves web search results using You.com's search API. You.com
provides AI-powered search capabilities with real-time web results
and summarization features.

The YouRetriever works by:
1. Connecting to You.com's search API
2. Executing search queries against the web
3. Retrieving and processing search results
4. Returning formatted documents with web content

This retriever is particularly useful when:
- Need real-time web search capabilities
- Building applications requiring current information
- Want AI-enhanced search results
- Creating research or fact-checking tools
- Need alternative to traditional search engines

The implementation integrates with LangChain's YouRetriever while
providing a consistent Haive configuration interface with secure API key management.
"""

from typing import Any, Dict, List, Optional, Tuple, Type

from langchain_core.documents import Document
from pydantic import Field, SecretStr

from haive.core.common.mixins.secure_config import SecureConfigMixin
from haive.core.engine.retriever.retriever import BaseRetrieverConfig
from haive.core.engine.retriever.types import RetrieverType


@BaseRetrieverConfig.register(RetrieverType.YOU)
class YouRetrieverConfig(SecureConfigMixin, BaseRetrieverConfig):
    """
    Configuration for You.com retriever in the Haive framework.

    This retriever searches the web using You.com's API and returns
    AI-enhanced search results and summaries.

    Attributes:
        retriever_type (RetrieverType): The type of retriever (always YOU).
        api_key (Optional[SecretStr]): You.com API key (auto-resolved from YOU_API_KEY).
        num_web_results (int): Number of web results to retrieve.
        safesearch (str): Safe search setting.
        country (str): Country code for localized results.
        search_lang (str): Language for search results.

    Examples:
        >>> from haive.core.engine.retriever import YouRetrieverConfig
        >>>
        >>> # Create the You.com retriever config
        >>> config = YouRetrieverConfig(
        ...     name="you_retriever",
        ...     num_web_results=10,
        ...     safesearch="moderate",
        ...     country="US",
        ...     search_lang="en"
        ... )
        >>>
        >>> # Instantiate and use the retriever
        >>> retriever = config.instantiate()
        >>> docs = retriever.get_relevant_documents("latest AI developments 2024")
        >>>
        >>> # Example with specific search parameters
        >>> tech_config = YouRetrieverConfig(
        ...     name="tech_you_retriever",
        ...     num_web_results=5,
        ...     safesearch="off",
        ...     country="US"
        ... )
    """

    retriever_type: RetrieverType = Field(
        default=RetrieverType.YOU, description="The type of retriever"
    )

    # API configuration with SecureConfigMixin
    api_key: Optional[SecretStr] = Field(
        default=None, description="You.com API key (auto-resolved from YOU_API_KEY)"
    )

    # Provider for SecureConfigMixin
    provider: str = Field(
        default="you", description="Provider name for API key resolution"
    )

    # Search parameters
    num_web_results: int = Field(
        default=10, ge=1, le=50, description="Number of web results to retrieve"
    )

    safesearch: str = Field(
        default="moderate",
        description="Safe search setting: 'strict', 'moderate', 'off'",
    )

    country: str = Field(
        default="US",
        description="Country code for localized results (e.g., 'US', 'GB', 'DE')",
    )

    search_lang: str = Field(
        default="en", description="Language for search results (e.g., 'en', 'es', 'fr')"
    )

    # Advanced search options
    ui_lang: str = Field(
        default="en", description="UI language for the search interface"
    )

    spellcheck: bool = Field(
        default=True, description="Whether to enable spell checking for queries"
    )

    def get_input_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return input field definitions for You.com retriever."""
        return {
            "query": (str, Field(description="Search query for You.com")),
        }

    def get_output_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return output field definitions for You.com retriever."""
        return {
            "documents": (
                List[Document],
                Field(
                    default_factory=list, description="Web search results from You.com"
                ),
            ),
        }

    def instantiate(self):
        """
        Create a You.com retriever from this configuration.

        Returns:
            YouRetriever: Instantiated retriever ready for web search.

        Raises:
            ImportError: If required packages are not available.
            ValueError: If API key or configuration is invalid.
        """
        try:
            from langchain_community.retrievers import YouRetriever
        except ImportError:
            raise ImportError(
                "YouRetriever requires langchain-community package. "
                "Install with: pip install langchain-community"
            )

        # Get API key using SecureConfigMixin
        api_key = self.get_api_key()
        if not api_key:
            raise ValueError(
                "You.com API key is required. Set YOU_API_KEY environment variable "
                "or provide api_key parameter."
            )

        return YouRetriever(
            ydc_api_key=api_key,
            num_web_results=self.num_web_results,
            safesearch=self.safesearch,
            country=self.country,
            search_lang=self.search_lang,
            ui_lang=self.ui_lang,
            spellcheck=self.spellcheck,
        )
