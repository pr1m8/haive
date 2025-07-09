"""
TF-IDF Retriever implementation for the Haive framework.

This module provides a configuration class for the TF-IDF (Term Frequency-Inverse Document Frequency)
retriever, which uses classical TF-IDF scoring for document retrieval. TF-IDF is a numerical
statistic that reflects how important a word is to a document in a collection of documents.

The TFIDFRetriever works by:
1. Computing term frequency (TF) for each term in each document
2. Computing inverse document frequency (IDF) for each term across the corpus
3. Calculating TF-IDF scores as the product of TF and IDF
4. Ranking documents by their TF-IDF similarity to the query

This retriever is particularly useful when:
- Working with text-based document collections
- Need classical information retrieval approaches
- Want interpretable term-based ranking
- Building baseline retrieval systems
- Comparing against modern neural approaches

The implementation integrates with LangChain's TFIDFRetriever while providing
a consistent Haive configuration interface.
"""

from typing import Any, Dict, List, Optional, Tuple, Type

from langchain_core.documents import Document
from pydantic import Field

from haive.core.engine.retriever.retriever import BaseRetrieverConfig
from haive.core.engine.retriever.types import RetrieverType


@BaseRetrieverConfig.register(RetrieverType.TFIDF)
class TFIDFRetrieverConfig(BaseRetrieverConfig):
    """
    Configuration for TF-IDF retriever in the Haive framework.

    This retriever uses Term Frequency-Inverse Document Frequency scoring to rank
    documents based on the importance of query terms in the document collection.

    Attributes:
        retriever_type (RetrieverType): The type of retriever (always TFIDF).
        documents (List[Document]): Documents to index for retrieval.
        k (int): Number of documents to retrieve (default: 4).
        tfidf_params (Optional[Dict]): Additional parameters for TF-IDF computation.

    Examples:
        >>> from haive.core.engine.retriever import TFIDFRetrieverConfig
        >>> from langchain_core.documents import Document
        >>>
        >>> # Create documents
        >>> docs = [
        ...     Document(page_content="Machine learning algorithms analyze data"),
        ...     Document(page_content="Deep learning networks process information"),
        ...     Document(page_content="Natural language models understand text")
        ... ]
        >>>
        >>> # Create the TF-IDF retriever config
        >>> config = TFIDFRetrieverConfig(
        ...     name="tfidf_retriever",
        ...     documents=docs,
        ...     k=2,
        ...     tfidf_params={"max_features": 1000, "stop_words": "english"}
        ... )
        >>>
        >>> # Instantiate and use the retriever
        >>> retriever = config.instantiate()
        >>> docs = retriever.get_relevant_documents("machine learning data analysis")
    """

    retriever_type: RetrieverType = Field(
        default=RetrieverType.TFIDF, description="The type of retriever"
    )

    # Documents to index
    documents: List[Document] = Field(
        default_factory=list, description="Documents to index for TF-IDF retrieval"
    )

    # Retrieval parameters
    k: int = Field(
        default=4, ge=1, le=100, description="Number of documents to retrieve"
    )

    # TF-IDF computation parameters
    tfidf_params: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional parameters for TF-IDF vectorizer (max_features, stop_words, etc.)",
    )

    def get_input_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return input field definitions for TF-IDF retriever."""
        return {
            "query": (str, Field(description="Text query for TF-IDF ranking")),
        }

    def get_output_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return output field definitions for TF-IDF retriever."""
        return {
            "documents": (
                List[Document],
                Field(
                    default_factory=list,
                    description="Documents ranked by TF-IDF scores",
                ),
            ),
        }

    def instantiate(self):
        """
        Create a TF-IDF retriever from this configuration.

        Returns:
            TFIDFRetriever: Instantiated retriever ready for text ranking.

        Raises:
            ImportError: If required packages are not available.
            ValueError: If documents list is empty.
        """
        try:
            from langchain_community.retrievers import TFIDFRetriever
        except ImportError:
            raise ImportError(
                "TFIDFRetriever requires langchain-community package. "
                "Install with: pip install langchain-community"
            )

        if not self.documents:
            raise ValueError(
                "TFIDFRetriever requires a non-empty list of documents. "
                "Provide documents in the configuration."
            )

        # Prepare TF-IDF parameters
        tfidf_kwargs = self.tfidf_params or {}

        return TFIDFRetriever.from_documents(
            documents=self.documents, k=self.k, tfidf_params=tfidf_kwargs
        )
