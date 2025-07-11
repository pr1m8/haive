"""K-Nearest Neighbors Retriever implementation for the Haive framework.

This module provides a configuration class for the KNN (K-Nearest Neighbors) retriever,
which uses k-nearest neighbors algorithm for document retrieval based on vector similarity.
KNN finds the k most similar documents to a query by computing distances in the embedding space.

The KNNRetriever works by:
1. Embedding documents and queries using a specified embedding model
2. Computing similarity/distance metrics between query and document embeddings
3. Finding the k nearest neighbors based on the distance metric
4. Returning the k most similar documents

This retriever is particularly useful when:
- Working with small to medium-sized document collections
- Need simple but effective similarity-based retrieval
- Want interpretable distance-based ranking
- Building baseline vector retrieval systems
- Comparing against more complex vector databases

The implementation integrates with LangChain's KNNRetriever while providing
a consistent Haive configuration interface.
"""

from typing import Any, Dict, List, Optional, Tuple, Type

from langchain_core.documents import Document
from pydantic import Field

from haive.core.engine.retriever.retriever import BaseRetrieverConfig
from haive.core.engine.retriever.types import RetrieverType


@BaseRetrieverConfig.register(RetrieverType.KNN)
class KNNRetrieverConfig(BaseRetrieverConfig):
    """Configuration for K-Nearest Neighbors retriever in the Haive framework.

    This retriever uses the KNN algorithm to find the most similar documents
    based on vector embeddings and distance metrics.

    Attributes:
        retriever_type (RetrieverType): The type of retriever (always KNN).
        documents (List[Document]): Documents to index for retrieval.
        k (int): Number of nearest neighbors to retrieve (default: 4).
        distance_metric (str): Distance metric to use ("cosine", "euclidean", "manhattan").
        embedding_model (Optional[str]): Embedding model to use for vectorization.

    Examples:
        >>> from haive.core.engine.retriever import KNNRetrieverConfig
        >>> from langchain_core.documents import Document
        >>>
        >>> # Create documents
        >>> docs = [
        ...     Document(page_content="Machine learning trains models on data"),
        ...     Document(page_content="Deep learning uses neural network architectures"),
        ...     Document(page_content="Natural language processing analyzes text patterns")
        ... ]
        >>>
        >>> # Create the KNN retriever config
        >>> config = KNNRetrieverConfig(
        ...     name="knn_retriever",
        ...     documents=docs,
        ...     k=2,
        ...     distance_metric="cosine",
        ...     embedding_model="sentence-transformers/all-MiniLM-L6-v2"
        ... )
        >>>
        >>> # Instantiate and use the retriever
        >>> retriever = config.instantiate()
        >>> docs = retriever.get_relevant_documents("machine learning training process")
    """

    retriever_type: RetrieverType = Field(
        default=RetrieverType.KNN, description="The type of retriever"
    )

    # Documents to index
    documents: list[Document] = Field(
        default_factory=list, description="Documents to index for KNN retrieval"
    )

    # Retrieval parameters
    k: int = Field(
        default=4, ge=1, le=100, description="Number of nearest neighbors to retrieve"
    )

    # KNN algorithm parameters
    distance_metric: str = Field(
        default="cosine",
        description="Distance metric: 'cosine', 'euclidean', 'manhattan', 'hamming'",
    )

    embedding_model: str | None = Field(
        default=None,
        description="Embedding model for vectorization (e.g., 'sentence-transformers/all-MiniLM-L6-v2')",
    )

    # Additional KNN parameters
    algorithm: str = Field(
        default="auto",
        description="KNN algorithm: 'auto', 'ball_tree', 'kd_tree', 'brute'",
    )

    def get_input_fields(self) -> dict[str, tuple[type, Any]]:
        """Return input field definitions for KNN retriever."""
        return {
            "query": (str, Field(description="Text query for KNN similarity search")),
        }

    def get_output_fields(self) -> dict[str, tuple[type, Any]]:
        """Return output field definitions for KNN retriever."""
        return {
            "documents": (
                list[Document],
                Field(default_factory=list, description="K nearest neighbor documents"),
            ),
        }

    def instantiate(self):
        """Create a KNN retriever from this configuration.

        Returns:
            KNNRetriever: Instantiated retriever ready for similarity search.

        Raises:
            ImportError: If required packages are not available.
            ValueError: If documents list is empty.
        """
        try:
            from langchain_community.retrievers import KNNRetriever
        except ImportError:
            raise ImportError(
                "KNNRetriever requires langchain-community package. "
                "Install with: pip install langchain-community"
            )

        if not self.documents:
            raise ValueError(
                "KNNRetriever requires a non-empty list of documents. "
                "Provide documents in the configuration."
            )

        # Create KNN retriever with configuration
        return KNNRetriever.from_documents(
            documents=self.documents,
            k=self.k,
            distance_metric=self.distance_metric,
            embedding_model=self.embedding_model,
            algorithm=self.algorithm,
        )
