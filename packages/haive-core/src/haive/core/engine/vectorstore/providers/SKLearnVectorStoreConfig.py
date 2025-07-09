"""
SKLearn Vector Store implementation for the Haive framework.

This module provides a configuration class for the SKLearn vector store,
which provides ML-integrated nearest neighbor search using scikit-learn.

SKLearn provides:
1. Scikit-learn NearestNeighbors integration
2. Multiple distance metrics and algorithms
3. Persistent storage in multiple formats (JSON, BSON, Parquet)
4. In-memory vector operations
5. ML-friendly interface and integration
6. Cross-platform compatibility

This vector store is particularly useful when:
- You need ML framework integration
- Want familiar scikit-learn interface
- Need persistent storage capabilities
- Building ML pipelines with vector search
- Require flexible distance metrics

The implementation integrates with LangChain's SKLearn while providing
a consistent Haive configuration interface.
"""

from typing import Any, Dict, List, Optional, Tuple, Type

from langchain_core.documents import Document
from pydantic import Field, validator

from haive.core.engine.vectorstore.base import BaseVectorStoreConfig
from haive.core.engine.vectorstore.types import VectorStoreType


@BaseVectorStoreConfig.register(VectorStoreType.SKLEARN)
class SKLearnVectorStoreConfig(BaseVectorStoreConfig):
    """
    Configuration for SKLearn vector store in the Haive framework.

    This vector store uses scikit-learn's NearestNeighbors for
    ML-integrated similarity search operations.

    Attributes:
        metric (str): Distance metric for similarity search.
        algorithm (str): Algorithm for neighbor search.
        persist_path (str): Path for persistent storage.
        serializer (str): Serialization format.

    Examples:
        >>> from haive.core.engine.vectorstore import SKLearnVectorStoreConfig
        >>> from haive.core.models.embeddings.base import OpenAIEmbeddingConfig
        >>>
        >>> # Create SKLearn config
        >>> config = SKLearnVectorStoreConfig(
        ...     name="sklearn_vectors",
        ...     embedding=OpenAIEmbeddingConfig(),
        ...     metric="cosine",
        ...     algorithm="auto"
        ... )
        >>>
        >>> # Create with persistence
        >>> config = SKLearnVectorStoreConfig(
        ...     name="sklearn_persistent",
        ...     embedding=OpenAIEmbeddingConfig(),
        ...     persist_path="/tmp/sklearn_vectors.json",
        ...     serializer="json"
        ... )
        >>>
        >>> # Instantiate and use
        >>> vectorstore = config.instantiate()
        >>> docs = [Document(page_content="SKLearn provides ML-integrated search")]
        >>> vectorstore.add_documents(docs)
        >>>
        >>> # ML-friendly similarity search
        >>> results = vectorstore.similarity_search("ML integration", k=5)
    """

    # Distance metric configuration
    metric: str = Field(
        default="cosine",
        description="Distance metric: 'cosine', 'euclidean', 'manhattan', etc.",
    )

    # Algorithm configuration
    algorithm: str = Field(
        default="auto", description="Algorithm: 'auto', 'ball_tree', 'kd_tree', 'brute'"
    )

    # Persistence configuration
    persist_path: Optional[str] = Field(
        default=None, description="Path for persistent storage (optional)"
    )

    serializer: str = Field(
        default="json", description="Serialization format: 'json', 'bson', 'parquet'"
    )

    # Performance parameters
    leaf_size: int = Field(
        default=30, ge=1, le=1000, description="Leaf size for tree algorithms"
    )

    n_jobs: Optional[int] = Field(
        default=None, description="Number of parallel jobs (-1 for all cores)"
    )

    @validator("metric")
    def validate_metric(cls, v):
        """Validate distance metric is supported by scikit-learn."""
        # Common scikit-learn metrics - not exhaustive
        valid_metrics = [
            "cosine",
            "euclidean",
            "manhattan",
            "chebyshev",
            "minkowski",
            "l1",
            "l2",
            "cityblock",
            "braycurtis",
            "canberra",
            "correlation",
            "hamming",
            "jaccard",
            "dice",
        ]
        if v not in valid_metrics:
            # Allow custom metrics but warn
            import warnings

            warnings.warn(f"metric '{v}' may not be supported by scikit-learn")
        return v

    @validator("algorithm")
    def validate_algorithm(cls, v):
        """Validate algorithm is supported by scikit-learn."""
        valid_algorithms = ["auto", "ball_tree", "kd_tree", "brute"]
        if v not in valid_algorithms:
            raise ValueError(f"algorithm must be one of {valid_algorithms}, got {v}")
        return v

    @validator("serializer")
    def validate_serializer(cls, v):
        """Validate serializer is supported."""
        valid_serializers = ["json", "bson", "parquet"]
        if v not in valid_serializers:
            raise ValueError(f"serializer must be one of {valid_serializers}, got {v}")
        return v

    @validator("n_jobs")
    def validate_n_jobs(cls, v):
        """Validate n_jobs parameter."""
        if v is not None and v < -1:
            raise ValueError("n_jobs must be None, -1, or positive integer")
        return v

    def get_input_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return input field definitions for SKLearn vector store."""
        return {
            "documents": (
                List[Document],
                Field(description="Documents to add to the vector store"),
            ),
        }

    def get_output_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return output field definitions for SKLearn vector store."""
        return {
            "ids": (
                List[str],
                Field(description="IDs of the added documents in SKLearn store"),
            ),
        }

    def instantiate(self):
        """
        Create a SKLearn vector store from this configuration.

        Returns:
            SKLearnVectorStore: Instantiated SKLearn vector store.

        Raises:
            ImportError: If required packages are not available.
            ValueError: If configuration is invalid.
        """
        try:
            from langchain_community.vectorstores import SKLearnVectorStore
        except ImportError:
            raise ImportError(
                "SKLearn vector store requires scikit-learn package. "
                "Install with: pip install scikit-learn"
            )

        # Validate embedding
        self.validate_embedding()
        embedding_function = self.embedding.instantiate()

        # Prepare kwargs for SKLearnVectorStore
        kwargs = {
            "embedding": embedding_function,
            "metric": self.metric,
            "algorithm": self.algorithm,
            "leaf_size": self.leaf_size,
        }

        # Add persistence configuration if specified
        if self.persist_path:
            kwargs["persist_path"] = self.persist_path
            kwargs["serializer"] = self.serializer

        # Add parallel processing configuration
        if self.n_jobs is not None:
            kwargs["n_jobs"] = self.n_jobs

        # Create SKLearn vector store
        try:
            vectorstore = SKLearnVectorStore(**kwargs)
        except Exception as e:
            raise ValueError(f"Failed to create SKLearn vector store: {e}")

        return vectorstore
