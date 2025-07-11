"""
Web Research Retriever implementation for the Haive framework.

This module provides a configuration class for the Web Research retriever,
which performs advanced web research by combining web search with document
processing and retrieval. It searches the web, retrieves content from URLs,
processes the content, and provides comprehensive research results.

The WebResearchRetriever works by:
1. Using a web search API to find relevant URLs
2. Retrieving and processing content from those URLs
3. Chunking and embedding the retrieved content
4. Providing retrieval over the processed web content
5. Combining search results with retrieved document chunks

This retriever is particularly useful when:
- Need up-to-date information from the web
- Building research applications that require current data
- Combining web search with document retrieval
- Creating systems that need comprehensive web coverage
- Building fact-checking or research assistant applications

The implementation integrates with LangChain's WebResearchRetriever while
providing a consistent Haive configuration interface with secure API key management.
"""

from typing import Any, Dict, List, Optional, Tuple, Type

from langchain_core.documents import Document
from pydantic import Field, SecretStr

from haive.core.common.mixins.secure_config import SecureConfigMixin
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.engine.retriever.retriever import BaseRetrieverConfig
from haive.core.engine.retriever.types import RetrieverType
from haive.core.engine.vectorstore.vectorstore import VectorStoreConfig


@BaseRetrieverConfig.register(RetrieverType.WEB_RESEARCH)
class WebResearchRetrieverConfig(SecureConfigMixin, BaseRetrieverConfig):
    """
    Configuration for Web Research retriever in the Haive framework.

    This retriever performs comprehensive web research by searching the web,
    retrieving content, and providing retrieval capabilities over the collected data.

    Attributes:
        retriever_type (RetrieverType): The type of retriever (always WEB_RESEARCH).
        vectorstore_config (VectorStoreConfig): Vector store for indexing web content.
        llm_config (AugLLMConfig): LLM for processing and summarization.
        api_key (Optional[SecretStr]): API key for web search (auto-resolved).
        num_search_results (int): Number of web search results to process.
        num_web_pages (int): Number of web pages to retrieve content from.
        chunk_size (int): Size of text chunks for processing.
        chunk_overlap (int): Overlap between text chunks.

    Examples:
        >>> from haive.core.engine.retriever import WebResearchRetrieverConfig
        >>> from haive.core.engine.aug_llm import AugLLMConfig
        >>> from haive.core.engine.vectorstore.providers.ChromaVectorStoreConfig import ChromaVectorStoreConfig
        >>>
        >>> # Configure components
        >>> llm_config = AugLLMConfig(model_name="gpt-4", provider="openai")
        >>> vectorstore_config = ChromaVectorStoreConfig(
        ...     name="web_research_store",
        ...     collection_name="web_content"
        ... )
        >>>
        >>> # Create the web research retriever config
        >>> config = WebResearchRetrieverConfig(
        ...     name="web_research_retriever",
        ...     vectorstore_config=vectorstore_config,
        ...     llm_config=llm_config,
        ...     num_search_results=10,
        ...     num_web_pages=5
        ... )
        >>>
        >>> # Instantiate and use the retriever
        >>> retriever = config.instantiate()
        >>> docs = retriever.get_relevant_documents("latest AI research developments 2024")
    """

    retriever_type: RetrieverType = Field(
        default=RetrieverType.WEB_RESEARCH, description="The type of retriever"
    )

    # Core components
    vectorstore_config: VectorStoreConfig = Field(
        ..., description="Vector store configuration for indexing web content"
    )

    llm_config: AugLLMConfig = Field(
        ..., description="LLM configuration for processing and summarization"
    )

    # API configuration with SecureConfigMixin
    api_key: Optional[SecretStr] = Field(
        default=None,
        description="Web search API key (auto-resolved from GOOGLE_API_KEY or TAVILY_API_KEY)",
    )

    # Provider for SecureConfigMixin
    provider: str = Field(
        default="google", description="Search provider: 'google', 'tavily', 'bing'"
    )

    # Web search parameters
    num_search_results: int = Field(
        default=10, ge=1, le=50, description="Number of web search results to process"
    )

    num_web_pages: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Number of web pages to retrieve content from",
    )

    # Content processing parameters
    chunk_size: int = Field(
        default=1000, ge=100, le=4000, description="Size of text chunks for processing"
    )

    chunk_overlap: int = Field(
        default=200, ge=0, le=500, description="Overlap between text chunks"
    )

    # Search engine configuration
    search_engine: str = Field(
        default="google", description="Search engine to use: 'google', 'tavily', 'bing'"
    )

    def get_input_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return input field definitions for Web Research retriever."""
        return {
            "query": (
                str,
                Field(description="Research query for web search and retrieval"),
            ),
        }

    def get_output_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return output field definitions for Web Research retriever."""
        return {
            "documents": (
                List[Document],
                Field(default_factory=list, description="Documents from web research"),
            ),
        }

    def instantiate(self):
        """
        Create a Web Research retriever from this configuration.

        Returns:
            WebResearchRetriever: Instantiated retriever ready for web research.

        Raises:
            ImportError: If required packages are not available.
            ValueError: If API key or configuration is invalid.
        """
        try:
            from langchain_community.retrievers.web_research import WebResearchRetriever
            from langchain_community.utilities import GoogleSearchAPIWrapper
        except ImportError:
            raise ImportError(
                "WebResearchRetriever requires langchain-community package. "
                "Install with: pip install langchain-community google-search-results"
            )

        # Get search API key
        api_key = self.get_api_key()
        if not api_key and self.search_engine == "google":
            raise ValueError(
                "Google Search API key is required. Set GOOGLE_API_KEY environment variable "
                "or provide api_key parameter."
            )

        # Instantiate components
        vectorstore = self.vectorstore_config.instantiate()
        llm = self.llm_config.instantiate()

        # Configure search wrapper
        if self.search_engine == "google":
            search = GoogleSearchAPIWrapper(
                google_api_key=api_key,
                google_cse_id=None,  # Uses default or environment variable
            )
        else:
            # For other search engines, use appropriate wrappers
            search = GoogleSearchAPIWrapper()  # Fallback

        return WebResearchRetriever.from_llm(
            vectorstore=vectorstore,
            llm=llm,
            search=search,
            num_search_results=self.num_search_results,
            num_web_pages=self.num_web_pages,
        )
