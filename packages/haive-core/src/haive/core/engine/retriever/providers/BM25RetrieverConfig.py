"""
BM25 Retriever implementation for the Haive framework.

This module provides a configuration class for the BM25 (Best Matching 25) retriever,
which uses the BM25 ranking function for text retrieval. BM25 is a probabilistic
ranking function used by search engines to estimate the relevance of documents
to a given search query.

The BM25Retriever works by:
1. Tokenizing and preprocessing documents and queries
2. Computing BM25 scores for each document-query pair
3. Ranking documents by their BM25 scores
4. Returning the top-k most relevant documents

This retriever is particularly useful when:
- Working with text-based document collections
- Need precise keyword matching and term frequency analysis
- Want interpretable ranking scores
- Building traditional information retrieval systems
- Combining with vector search in hybrid approaches

The implementation integrates with LangChain's BM25Retriever while providing
a consistent Haive configuration interface.
"""

from typing import Any, Dict, List, Optional, Tuple, Type

from langchain_core.documents import Document
from pydantic import Field

from haive.core.engine.retriever.retriever import BaseRetrieverConfig
from haive.core.engine.retriever.types import RetrieverType


@BaseRetrieverConfig.register(RetrieverType.BM25)
class BM25RetrieverConfig(BaseRetrieverConfig):
    """
    Configuration for BM25 retriever in the Haive framework.

    This retriever uses the BM25 ranking function to score documents based on
    term frequency, inverse document frequency, and document length normalization.

    Attributes:
        retriever_type (RetrieverType): The type of retriever (always BM25).
        documents (List[Document]): Documents to index for retrieval.
        k (int): Number of documents to retrieve (default: 4).
        k1 (float): BM25 parameter controlling term frequency saturation (default: 1.2).
        b (float): BM25 parameter controlling document length normalization (default: 0.75).
        epsilon (float): BM25 parameter for IDF calculation (default: 0.25).

    Examples:
        >>> from haive.core.engine.retriever import BM25RetrieverConfig
        >>> from langchain_core.documents import Document
        >>>
        >>> # Create documents
        >>> docs = [
        ...     Document(page_content="Machine learning is a subset of AI"),
        ...     Document(page_content="Deep learning uses neural networks"),
        ...     Document(page_content="Natural language processing handles text")
        ... ]
        >>>
        >>> # Create the BM25 retriever config
        >>> config = BM25RetrieverConfig(
        ...     name="bm25_retriever",
        ...     documents=docs,
        ...     k=2,
        ...     k1=1.5,  # Higher term frequency saturation
        ...     b=0.8    # More document length normalization
        ... )
        >>>
        >>> # Instantiate and use the retriever
        >>> retriever = config.instantiate()
        >>> docs = retriever.get_relevant_documents("machine learning algorithms")
    """

    retriever_type: RetrieverType = Field(
        default=RetrieverType.BM25, description="The type of retriever"
    )

    # Documents to index
    documents: List[Document] = Field(
        default_factory=list, description="Documents to index for BM25 retrieval"
    )

    # Retrieval parameters
    k: int = Field(
        default=4, ge=1, le=100, description="Number of documents to retrieve"
    )

    # BM25 algorithm parameters
    k1: float = Field(
        default=1.2,
        ge=0.0,
        le=3.0,
        description="BM25 k1 parameter controlling term frequency saturation",
    )

    b: float = Field(
        default=0.75,
        ge=0.0,
        le=1.0,
        description="BM25 b parameter controlling document length normalization",
    )

    epsilon: float = Field(
        default=0.25,
        ge=0.0,
        le=1.0,
        description="BM25 epsilon parameter for IDF calculation",
    )

    def get_input_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return input field definitions for BM25 retriever."""
        return {
            "query": (str, Field(description="Text query for BM25 ranking")),
        }

    def get_output_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return output field definitions for BM25 retriever."""
        return {
            "documents": (
                List[Document],
                Field(
                    default_factory=list, description="Documents ranked by BM25 scores"
                ),
            ),
        }

    def instantiate(self):
        """
        Create a BM25 retriever from this configuration.

        Returns:
            BM25Retriever: Instantiated retriever ready for text ranking.

        Raises:
            ImportError: If required packages are not available.
            ValueError: If documents list is empty.
        """
        try:
            from langchain_community.retrievers import BM25Retriever
        except ImportError:
            raise ImportError(
                "BM25Retriever requires langchain-community package. "
                "Install with: pip install langchain-community"
            )

        if not self.documents:
            raise ValueError(
                "BM25Retriever requires a non-empty list of documents. "
                "Provide documents in the configuration."
            )

        return BM25Retriever.from_documents(
            documents=self.documents,
            k=self.k,
            k1=self.k1,
            b=self.b,
            epsilon=self.epsilon,
        )
