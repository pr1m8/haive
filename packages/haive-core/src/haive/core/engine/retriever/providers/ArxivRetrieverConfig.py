"""
Arxiv Retriever implementation for the Haive framework.

This module provides a configuration class for the Arxiv retriever, which
retrieves academic papers from the arXiv preprint repository.

The ArxivRetriever works by:
1. Taking a search query for academic papers
2. Searching the arXiv API for matching papers
3. Returning paper abstracts and metadata as documents

This retriever is particularly useful when:
- Working with academic or research content
- Need access to the latest preprint papers
- Building research-focused applications
- Combining with other retrievers in academic contexts

The implementation integrates with LangChain's ArxivRetriever while providing
a consistent Haive configuration interface.
"""

from typing import Any, Dict, List, Optional, Tuple, Type

from langchain_core.documents import Document
from pydantic import Field

from haive.core.engine.retriever.retriever import BaseRetrieverConfig
from haive.core.engine.retriever.types import RetrieverType


@BaseRetrieverConfig.register(RetrieverType.ARXIV)
class ArxivRetrieverConfig(BaseRetrieverConfig):
    """
    Configuration for Arxiv retriever in the Haive framework.

    This retriever searches the arXiv preprint repository for academic papers
    matching the query and returns their abstracts and metadata as documents.

    Attributes:
        retriever_type (RetrieverType): The type of retriever (always ARXIV).
        top_k_results (int): Maximum number of papers to retrieve (default: 3).
        load_max_docs (int): Maximum number of documents to load (default: 100).
        load_all_available_meta (bool): Whether to load all available metadata (default: False).

    Examples:
        >>> from haive.core.engine.retriever import ArxivRetrieverConfig
        >>>
        >>> # Create the arxiv retriever config
        >>> config = ArxivRetrieverConfig(
        ...     name="arxiv_retriever",
        ...     top_k_results=5,
        ...     load_max_docs=50
        ... )
        >>>
        >>> # Instantiate and use the retriever
        >>> retriever = config.instantiate()
        >>> docs = retriever.get_relevant_documents("machine learning transformers")
    """

    retriever_type: RetrieverType = Field(
        default=RetrieverType.ARXIV, description="The type of retriever"
    )

    top_k_results: int = Field(
        default=3, ge=1, le=100, description="Maximum number of papers to retrieve"
    )

    load_max_docs: int = Field(
        default=100, ge=1, description="Maximum number of documents to load"
    )

    load_all_available_meta: bool = Field(
        default=False, description="Whether to load all available metadata"
    )

    def get_input_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return input field definitions for Arxiv retriever."""
        return {
            "query": (str, Field(description="Search query for academic papers")),
        }

    def get_output_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return output field definitions for Arxiv retriever."""
        return {
            "documents": (
                List[Document],
                Field(default_factory=list, description="Academic papers from arXiv"),
            ),
        }

    def instantiate(self):
        """
        Create an Arxiv retriever from this configuration.

        Returns:
            ArxivRetriever: Instantiated retriever ready for document retrieval.

        Raises:
            ImportError: If required packages are not available.
        """
        try:
            from langchain_community.retrievers import ArxivRetriever
        except ImportError:
            raise ImportError(
                "ArxivRetriever requires arxiv package. Install with: pip install arxiv"
            )

        return ArxivRetriever(
            top_k_results=self.top_k_results,
            load_max_docs=self.load_max_docs,
            load_all_available_meta=self.load_all_available_meta,
        )
