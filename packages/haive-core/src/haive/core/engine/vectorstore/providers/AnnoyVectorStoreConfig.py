"""
Annoy Vector Store implementation for the Haive framework.

This module provides a configuration class for the Annoy vector store,
which provides memory-efficient approximate nearest neighbor search.

Annoy provides:
1. Memory-efficient approximate nearest neighbor search
2. Fast querying with small memory footprint
3. Multiple distance metrics (angular, euclidean, manhattan, etc.)
4. Index building with configurable trees for speed/accuracy trade-offs
5. Read-only after index building (immutable indices)
6. No dependencies on large external libraries

This vector store is particularly useful when:
- You need memory-efficient vector search
- Want fast approximate nearest neighbor search
- Have a static dataset that doesn't need frequent updates
- Building applications with resource constraints
- Need deterministic search results

The implementation integrates with LangChain's Annoy while providing
a consistent Haive configuration interface.

Note: Annoy indices are immutable after building - no new documents
can be added once the index is created.
"""

from typing import Any, Dict, List, Optional, Tuple, Type

from langchain_core.documents import Document
from pydantic import Field, validator

from haive.core.engine.vectorstore.base import BaseVectorStoreConfig
from haive.core.engine.vectorstore.types import VectorStoreType


@BaseVectorStoreConfig.register(VectorStoreType.ANNOY)
class AnnoyVectorStoreConfig(BaseVectorStoreConfig):
    """
    Configuration for Annoy vector store in the Haive framework.

    This vector store uses Annoy for memory-efficient approximate
    nearest neighbor search with immutable indices.

    Attributes:
        metric (str): Distance metric for similarity search.
        trees (int): Number of trees to build for indexing.
        n_jobs (int): Number of parallel jobs for index building.
        search_k (int): Number of nodes to inspect during search.

    Examples:
        >>> from haive.core.engine.vectorstore import AnnoyVectorStoreConfig
        >>> from haive.core.models.embeddings.base import OpenAIEmbeddingConfig
        >>>
        >>> # Create Annoy config
        >>> config = AnnoyVectorStoreConfig(
        ...     name="annoy_vectors",
        ...     embedding=OpenAIEmbeddingConfig(),
        ...     metric="angular",
        ...     trees=100,
        ...     n_jobs=-1
        ... )
        >>>
        >>> # Instantiate with documents (immutable after creation)
        >>> from langchain_core.documents import Document
        >>> docs = [Document(page_content="Annoy provides fast approximate search")]
        >>> vectorstore = config.instantiate(documents=docs)
        >>>
        >>> # Fast approximate search
        >>> results = vectorstore.similarity_search("fast search", k=5)
        >>>
        >>> # Note: Cannot add more documents after index is built
        >>> # vectorstore.add_documents(more_docs)  # This will raise NotImplementedError
    """

    # Distance metric configuration
    metric: str = Field(
        default="angular",
        description="Distance metric: 'angular', 'euclidean', 'manhattan', 'hamming', or 'dot'",
    )

    # Index building parameters
    trees: int = Field(
        default=100,
        ge=1,
        le=1000,
        description="Number of trees to build for indexing (more trees = better accuracy, slower build)",
    )

    n_jobs: int = Field(
        default=-1,
        ge=-1,
        description="Number of parallel jobs for building index (-1 = use all cores)",
    )

    # Search parameters
    search_k: int = Field(
        default=-1,
        ge=-1,
        description="Number of nodes to inspect during search (-1 = trees * n_items)",
    )

    # Advanced parameters
    build_on_instantiate: bool = Field(
        default=True, description="Whether to build index immediately on instantiation"
    )

    @validator("metric")
    def validate_metric(cls, v):
        """Validate distance metric is supported by Annoy."""
        valid_metrics = ["angular", "euclidean", "manhattan", "hamming", "dot"]
        if v not in valid_metrics:
            raise ValueError(f"metric must be one of {valid_metrics}, got {v}")
        return v

    @validator("n_jobs")
    def validate_n_jobs(cls, v):
        """Validate n_jobs parameter."""
        if v < -1 or v == 0:
            raise ValueError("n_jobs must be -1 (all cores) or positive integer")
        return v

    def get_input_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return input field definitions for Annoy vector store."""
        return {
            "documents": (
                List[Document],
                Field(description="Documents to build Annoy index from"),
            ),
        }

    def get_output_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return output field definitions for Annoy vector store."""
        return {
            "index": (Any, Field(description="Built Annoy index (immutable)")),
        }

    def instantiate(self, documents: Optional[List[Document]] = None):
        """
        Create an Annoy vector store from this configuration.

        Args:
            documents: Documents to build the index from. Required for Annoy
                      since it cannot add documents after index is built.

        Returns:
            Annoy: Instantiated Annoy vector store with built index.

        Raises:
            ImportError: If required packages are not available.
            ValueError: If configuration is invalid or documents not provided.
        """
        try:
            from langchain_community.vectorstores import Annoy
        except ImportError:
            raise ImportError(
                "Annoy requires annoy package. " "Install with: pip install annoy"
            )

        # Validate embedding
        self.validate_embedding()
        embedding_function = self.embedding.instantiate()

        # Annoy requires documents at creation time since index is immutable
        if not documents:
            raise ValueError(
                "Annoy requires documents at instantiation time since indices are immutable. "
                "Pass documents to the instantiate() method."
            )

        if not isinstance(documents, list) or len(documents) == 0:
            raise ValueError("documents must be a non-empty list of Document objects")

        # Extract texts and metadata from documents
        texts = [doc.page_content for doc in documents]
        metadatas = [doc.metadata for doc in documents]

        # Prepare kwargs for Annoy creation
        kwargs = {
            "texts": texts,
            "embedding": embedding_function,
            "metadatas": metadatas,
            "metric": self.metric,
            "trees": self.trees,
            "n_jobs": self.n_jobs,
        }

        # Create Annoy vector store with built index
        try:
            vectorstore = Annoy.from_texts(**kwargs)
        except Exception as e:
            raise ValueError(f"Failed to create Annoy index: {e}")

        return vectorstore

    def create_runnable(self, runnable_config: Optional[Dict[str, Any]] = None):
        """
        Create a runnable Annoy vector store instance.

        Note: For Annoy, documents must be provided in runnable_config
        since the index is immutable after creation.

        Args:
            runnable_config: Configuration containing 'documents' key.

        Returns:
            Annoy: Instantiated Annoy vector store.
        """
        documents = None
        if runnable_config and "documents" in runnable_config:
            documents = runnable_config["documents"]

        return self.instantiate(documents=documents)
