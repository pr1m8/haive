"""PubMed Retriever implementation for the Haive framework.

This module provides a configuration class for the PubMed retriever,
which retrieves biomedical and life science literature from the PubMed database.
PubMed is a free search engine accessing primarily the MEDLINE database of references
and abstracts on life sciences and biomedical topics.

The PubMedRetriever works by:
1. Connecting to the PubMed API (via NCBI E-utilities)
2. Executing search queries against the PubMed database
3. Retrieving article abstracts and metadata
4. Returning formatted documents with biomedical literature

This retriever is particularly useful when:
- Building medical or healthcare applications
- Researching biomedical topics and treatments
- Creating evidence-based medicine tools
- Developing clinical decision support systems
- Building scientific literature review applications

The implementation integrates with LangChain's PubMedRetriever while providing
a consistent Haive configuration interface.
"""

from typing import Any, Dict, List, Optional, Tuple, Type

from langchain_core.documents import Document
from pydantic import Field

from haive.core.engine.retriever.retriever import BaseRetrieverConfig
from haive.core.engine.retriever.types import RetrieverType


@BaseRetrieverConfig.register(RetrieverType.PUBMED)
class PubMedRetrieverConfig(BaseRetrieverConfig):
    """Configuration for PubMed retriever in the Haive framework.

    This retriever searches the PubMed database for biomedical literature
    and returns article abstracts and metadata as documents.

    Attributes:
        retriever_type (RetrieverType): The type of retriever (always PUBMED).
        top_k_results (int): Number of articles to retrieve (default: 3).
        load_max_docs (int): Maximum number of documents to load (default: 25).
        load_all_available_meta (bool): Whether to load all available metadata.
        doc_content_chars_max (int): Maximum characters per document.
        email (Optional[str]): Email for NCBI API (recommended for higher rate limits).

    Examples:
        >>> from haive.core.engine.retriever import PubMedRetrieverConfig
        >>>
        >>> # Create the PubMed retriever config
        >>> config = PubMedRetrieverConfig(
        ...     name="pubmed_retriever",
        ...     top_k_results=5,
        ...     load_max_docs=20,
        ...     load_all_available_meta=True,
        ...     email="researcher@university.edu"  # Optional but recommended
        ... )
        >>>
        >>> # Instantiate and use the retriever
        >>> retriever = config.instantiate()
        >>> docs = retriever.get_relevant_documents("COVID-19 vaccine effectiveness")
        >>>
        >>> # Example with specific medical query
        >>> docs = retriever.get_relevant_documents("CRISPR gene editing cancer treatment")
    """

    retriever_type: RetrieverType = Field(
        default=RetrieverType.PUBMED, description="The type of retriever"
    )

    # Search parameters
    top_k_results: int = Field(
        default=3,
        ge=1,
        le=100,
        description="Number of articles to retrieve from PubMed",
    )

    load_max_docs: int = Field(
        default=25, ge=1, le=200, description="Maximum number of documents to load"
    )

    # Content parameters
    load_all_available_meta: bool = Field(
        default=False, description="Whether to load all available metadata fields"
    )

    doc_content_chars_max: int = Field(
        default=4000,
        ge=500,
        le=10000,
        description="Maximum characters per document content",
    )

    # API configuration
    email: str | None = Field(
        default=None,
        description="Email address for NCBI API (recommended for higher rate limits)",
    )

    # Search filters
    min_year: int | None = Field(
        default=None, ge=1900, le=2030, description="Minimum publication year filter"
    )

    max_year: int | None = Field(
        default=None, ge=1900, le=2030, description="Maximum publication year filter"
    )

    def get_input_fields(self) -> dict[str, tuple[type, Any]]:
        """Return input field definitions for PubMed retriever."""
        return {
            "query": (str, Field(description="Biomedical search query for PubMed")),
        }

    def get_output_fields(self) -> dict[str, tuple[type, Any]]:
        """Return output field definitions for PubMed retriever."""
        return {
            "documents": (
                list[Document],
                Field(
                    default_factory=list, description="Biomedical articles from PubMed"
                ),
            ),
        }

    def instantiate(self):
        """Create a PubMed retriever from this configuration.

        Returns:
            PubMedRetriever: Instantiated retriever ready for biomedical literature search.

        Raises:
            ImportError: If required packages are not available.
        """
        try:
            from langchain_community.retrievers import PubMedRetriever
        except ImportError:
            raise ImportError(
                "PubMedRetriever requires langchain-community package. "
                "Install with: pip install langchain-community"
            )

        # Prepare configuration parameters
        config_params = {
            "top_k_results": self.top_k_results,
            "load_max_docs": self.load_max_docs,
            "load_all_available_meta": self.load_all_available_meta,
            "doc_content_chars_max": self.doc_content_chars_max,
        }

        # Add optional parameters
        if self.email:
            config_params["email"] = self.email

        # Note: PubMed date filtering is typically done in the query string
        # e.g., "COVID-19 AND 2020:2024[dp]" for date range

        return PubMedRetriever(**config_params)
