"""
DocArray Vector Store implementation for the Haive framework.

This module provides a configuration class for the DocArray vector store,
which offers multiple storage backends for document-oriented vector operations.

DocArray provides:
1. Multiple storage backends (in-memory, HNSW, Weaviate, etc.)
2. Document-oriented data model with rich metadata
3. Multi-modal support (text, images, audio, etc.)
4. High-performance vector operations
5. Flexible schema definition
6. Built-in data processing pipelines

This vector store is particularly useful when:
- You need document-oriented vector operations
- Want multi-modal data support
- Need flexible storage backends
- Building ML pipelines with rich metadata
- Require high-performance exact or approximate search

The implementation integrates with LangChain's DocArray while providing
a consistent Haive configuration interface.
"""

from typing import Any, Dict, List, Optional, Tuple, Type

from langchain_core.documents import Document
from pydantic import Field, validator

from haive.core.engine.vectorstore.base import BaseVectorStoreConfig
from haive.core.engine.vectorstore.types import VectorStoreType


@BaseVectorStoreConfig.register(VectorStoreType.DOCARRAY)
class DocArrayVectorStoreConfig(BaseVectorStoreConfig):
    """
    Configuration for DocArray vector store in the Haive framework.

    This vector store uses DocArray for document-oriented vector operations
    with multiple storage backend options.

    Attributes:
        backend (str): Storage backend to use ('in_memory' or 'hnsw').
        metric (str): Distance metric for similarity search.
        work_dir (str): Working directory for HNSW backend.
        n_dim (int): Vector dimension (auto-detected if not specified).

    Examples:
        >>> from haive.core.engine.vectorstore import DocArrayVectorStoreConfig
        >>> from haive.core.models.embeddings.base import OpenAIEmbeddingConfig
        >>>
        >>> # Create DocArray config (in-memory)
        >>> config = DocArrayVectorStoreConfig(
        ...     name="docarray_memory",
        ...     embedding=OpenAIEmbeddingConfig(),
        ...     backend="in_memory",
        ...     metric="cosine_sim"
        ... )
        >>>
        >>> # Create DocArray config (HNSW)
        >>> config = DocArrayVectorStoreConfig(
        ...     name="docarray_hnsw",
        ...     embedding=OpenAIEmbeddingConfig(),
        ...     backend="hnsw",
        ...     work_dir="/tmp/docarray_hnsw",
        ...     metric="cosine",
        ...     max_elements=10000
        ... )
        >>>
        >>> # Instantiate and use
        >>> vectorstore = config.instantiate()
        >>> docs = [Document(page_content="DocArray supports multi-modal data")]
        >>> vectorstore.add_documents(docs)
        >>>
        >>> # Document-oriented vector search
        >>> results = vectorstore.similarity_search("multi-modal search", k=5)
    """

    # Backend configuration
    backend: str = Field(
        default="in_memory", description="Storage backend: 'in_memory' or 'hnsw'"
    )

    # Distance metric configuration
    metric: str = Field(
        default="cosine_sim", description="Distance metric for similarity search"
    )

    # HNSW-specific configuration
    work_dir: Optional[str] = Field(
        default=None,
        description="Working directory for HNSW backend (required for HNSW)",
    )

    n_dim: Optional[int] = Field(
        default=None, description="Vector dimension (auto-detected if not specified)"
    )

    max_elements: int = Field(
        default=1024,
        ge=1,
        le=1000000,
        description="Maximum number of vectors for HNSW backend",
    )

    # HNSW performance parameters
    ef_construction: int = Field(
        default=200,
        ge=10,
        le=2000,
        description="HNSW construction time/accuracy trade-off",
    )

    ef: int = Field(
        default=10, ge=1, le=1000, description="HNSW query time/accuracy trade-off"
    )

    M: int = Field(
        default=16,
        ge=2,
        le=100,
        description="HNSW maximum outgoing connections in graph",
    )

    # HNSW advanced settings
    allow_replace_deleted: bool = Field(
        default=True, description="Allow replacing deleted elements with new ones"
    )

    num_threads: int = Field(
        default=1, ge=1, le=64, description="Number of CPU threads to use"
    )

    index_enabled: bool = Field(
        default=True, description="Whether to build index for the field"
    )

    @validator("backend")
    def validate_backend(cls, v):
        """Validate backend is supported."""
        valid_backends = ["in_memory", "hnsw"]
        if v not in valid_backends:
            raise ValueError(f"backend must be one of {valid_backends}, got {v}")
        return v

    @validator("metric")
    def validate_metric(cls, v, values):
        """Validate metric is supported for the backend."""
        backend = values.get("backend", "in_memory")

        if backend == "in_memory":
            valid_metrics = ["cosine_sim", "euclidian_dist", "sgeuclidean_dist"]
        else:  # hnsw
            valid_metrics = ["cosine", "ip", "l2"]

        if v not in valid_metrics:
            raise ValueError(
                f"metric for {backend} backend must be one of {valid_metrics}, got {v}"
            )
        return v

    @validator("work_dir")
    def validate_work_dir(cls, v, values):
        """Validate work_dir is provided for HNSW backend."""
        backend = values.get("backend", "in_memory")
        if backend == "hnsw" and not v:
            raise ValueError("work_dir is required for HNSW backend")
        return v

    def get_input_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return input field definitions for DocArray vector store."""
        return {
            "documents": (
                List[Document],
                Field(description="Documents to add to the vector store"),
            ),
        }

    def get_output_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return output field definitions for DocArray vector store."""
        return {
            "ids": (
                List[str],
                Field(description="IDs of the added documents in DocArray"),
            ),
        }

    def instantiate(self):
        """
        Create a DocArray vector store from this configuration.

        Returns:
            DocArrayIndex: Instantiated DocArray vector store.

        Raises:
            ImportError: If required packages are not available.
            ValueError: If configuration is invalid.
        """
        try:
            if self.backend == "in_memory":
                from langchain_community.vectorstores.docarray import (
                    DocArrayInMemorySearch as DocArrayStore,
                )
            else:  # hnsw
                from langchain_community.vectorstores.docarray import (
                    DocArrayHnswSearch as DocArrayStore,
                )
        except ImportError:
            raise ImportError(
                "DocArray requires docarray package. "
                "Install with: pip install docarray"
            )

        # Validate embedding
        self.validate_embedding()
        embedding_function = self.embedding.instantiate()

        # Get vector dimensions if not specified
        n_dim = self.n_dim
        if not n_dim:
            try:
                sample_embedding = embedding_function.embed_query("sample")
                n_dim = len(sample_embedding)
            except Exception:
                n_dim = 1536  # Default dimension

        # Prepare kwargs based on backend
        if self.backend == "in_memory":
            kwargs = {
                "embedding": embedding_function,
                "metric": self.metric,
            }

            # Create in-memory DocArray store
            vectorstore = DocArrayStore.from_params(**kwargs)

        else:  # hnsw backend
            kwargs = {
                "embedding": embedding_function,
                "work_dir": self.work_dir,
                "n_dim": n_dim,
                "dist_metric": self.metric,
                "max_elements": self.max_elements,
                "index": self.index_enabled,
                "ef_construction": self.ef_construction,
                "ef": self.ef,
                "M": self.M,
                "allow_replace_deleted": self.allow_replace_deleted,
                "num_threads": self.num_threads,
            }

            # Create HNSW DocArray store
            vectorstore = DocArrayStore.from_params(**kwargs)

        return vectorstore
