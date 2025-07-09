"""
Wikipedia Retriever implementation for the Haive framework.

This module provides a configuration class for the Wikipedia retriever, which
retrieves articles from Wikipedia based on search queries.

The WikipediaRetriever works by:
1. Taking a search query
2. Searching Wikipedia for matching articles
3. Returning article content as documents

This retriever is particularly useful when:
- Need access to encyclopedic knowledge
- Building general knowledge applications
- Combining with other retrievers for comprehensive coverage
- Providing factual background information

The implementation integrates with LangChain's WikipediaRetriever while providing
a consistent Haive configuration interface.
"""

from typing import Any, Dict, List, Optional, Tuple, Type

from langchain_core.documents import Document
from pydantic import Field

from haive.core.engine.retriever.retriever import BaseRetrieverConfig
from haive.core.engine.retriever.types import RetrieverType


@BaseRetrieverConfig.register(RetrieverType.WIKIPEDIA)
class WikipediaRetrieverConfig(BaseRetrieverConfig):
    """
    Configuration for Wikipedia retriever in the Haive framework.

    This retriever searches Wikipedia for articles matching the query and returns
    their content as documents.

    Attributes:
        retriever_type (RetrieverType): The type of retriever (always WIKIPEDIA).
        top_k_results (int): Maximum number of articles to retrieve (default: 3).
        lang (str): Language code for Wikipedia (default: "en").
        load_max_docs (int): Maximum number of documents to load (default: 100).
        load_all_available_meta (bool): Whether to load all available metadata (default: False).

    Examples:
        >>> from haive.core.engine.retriever import WikipediaRetrieverConfig
        >>>
        >>> # Create the wikipedia retriever config
        >>> config = WikipediaRetrieverConfig(
        ...     name="wikipedia_retriever",
        ...     top_k_results=5,
        ...     lang="en"
        ... )
        >>>
        >>> # Instantiate and use the retriever
        >>> retriever = config.instantiate()
        >>> docs = retriever.get_relevant_documents("artificial intelligence")
    """

    retriever_type: RetrieverType = Field(
        default=RetrieverType.WIKIPEDIA, description="The type of retriever"
    )

    top_k_results: int = Field(
        default=3,
        ge=1,
        le=20,
        description="Maximum number of Wikipedia articles to retrieve",
    )

    lang: str = Field(
        default="en", description="Language code for Wikipedia (e.g., 'en', 'es', 'fr')"
    )

    load_max_docs: int = Field(
        default=100, ge=1, description="Maximum number of documents to load"
    )

    load_all_available_meta: bool = Field(
        default=False, description="Whether to load all available metadata"
    )

    def get_input_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return input field definitions for Wikipedia retriever."""
        return {
            "query": (str, Field(description="Search query for Wikipedia articles")),
        }

    def get_output_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return output field definitions for Wikipedia retriever."""
        return {
            "documents": (
                List[Document],
                Field(default_factory=list, description="Wikipedia articles"),
            ),
        }

    def instantiate(self):
        """
        Create a Wikipedia retriever from this configuration.

        Returns:
            WikipediaRetriever: Instantiated retriever ready for document retrieval.

        Raises:
            ImportError: If required packages are not available.
        """
        try:
            from langchain_community.retrievers import WikipediaRetriever
        except ImportError:
            raise ImportError(
                "WikipediaRetriever requires wikipedia package. Install with: pip install wikipedia"
            )

        return WikipediaRetriever(
            top_k_results=self.top_k_results,
            lang=self.lang,
            load_max_docs=self.load_max_docs,
            load_all_available_meta=self.load_all_available_meta,
        )
