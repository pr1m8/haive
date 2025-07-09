"""
USearch Vector Store implementation for the Haive framework.

This module provides a configuration class for the USearch vector store,
which offers high-performance universal similarity search.

USearch provides:
1. Universal similarity search for multiple data types
2. High-performance C++ implementation with Python bindings
3. Multiple distance metrics (cosine, euclidean, etc.)
4. Memory-efficient operations
5. Support for adding documents after index creation
6. Cross-platform compatibility

This vector store is particularly useful when:
- You need high-performance similarity search
- Want universal support for different data types
- Need memory-efficient vector operations
- Building performance-critical applications
- Require fast similarity computations

The implementation integrates with LangChain's USearch while providing
a consistent Haive configuration interface.
"""

from typing import Any, Dict, List, Optional, Tuple, Type

from langchain_core.documents import Document
from pydantic import Field, validator

from haive.core.engine.vectorstore.base import BaseVectorStoreConfig
from haive.core.engine.vectorstore.types import VectorStoreType


@BaseVectorStoreConfig.register(VectorStoreType.USEARCH)
class USearchVectorStoreConfig(BaseVectorStoreConfig):
    """
    Configuration for USearch vector store in the Haive framework.

    This vector store uses USearch for high-performance universal
    similarity search operations.

    Attributes:
        metric (str): Distance metric for similarity search.
        ndim (int): Number of dimensions (auto-detected if not specified).

    Examples:
        >>> from haive.core.engine.vectorstore import USearchVectorStoreConfig
        >>> from haive.core.models.embeddings.base import OpenAIEmbeddingConfig
        >>>
        >>> # Create USearch config
        >>> config = USearchVectorStoreConfig(
        ...     name="usearch_vectors",
        ...     embedding=OpenAIEmbeddingConfig(),
        ...     metric="cos"
        ... )
        >>>
        >>> # Instantiate and use
        >>> vectorstore = config.instantiate()
        >>> docs = [Document(page_content="USearch provides universal similarity search")]
        >>> vectorstore.add_documents(docs)
        >>>
        >>> # High-performance similarity search
        >>> results = vectorstore.similarity_search("universal search", k=5)
        >>>
        >>> # Can add more documents after creation
        >>> more_docs = [Document(page_content="Additional documents")]
        >>> vectorstore.add_documents(more_docs)
    """

    # Distance metric configuration
    metric: str = Field(
        default="cos",
        description="Distance metric: 'cos' (cosine), 'l2sq' (squared euclidean), 'ip' (inner product)",
    )

    # Vector dimension configuration
    ndim: Optional[int] = Field(
        default=None,
        description="Number of dimensions (auto-detected from embedding if not specified)",
    )

    @validator("metric")
    def validate_metric(cls, v):
        """Validate distance metric is supported by USearch."""
        valid_metrics = ["cos", "l2sq", "ip"]
        if v not in valid_metrics:
            raise ValueError(f"metric must be one of {valid_metrics}, got {v}")
        return v

    @validator("ndim")
    def validate_ndim(cls, v):
        """Validate ndim is positive if specified."""
        if v is not None and v <= 0:
            raise ValueError("ndim must be a positive integer")
        return v

    def get_input_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return input field definitions for USearch vector store."""
        return {
            "documents": (
                List[Document],
                Field(description="Documents to add to the vector store"),
            ),
        }

    def get_output_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return output field definitions for USearch vector store."""
        return {
            "ids": (
                List[str],
                Field(description="IDs of the added documents in USearch"),
            ),
        }

    def instantiate(self):
        """
        Create a USearch vector store from this configuration.

        Returns:
            USearch: Instantiated USearch vector store.

        Raises:
            ImportError: If required packages are not available.
            ValueError: If configuration is invalid.
        """
        try:
            from langchain_community.vectorstores import USearch
        except ImportError:
            raise ImportError(
                "USearch requires usearch package. " "Install with: pip install usearch"
            )

        # Validate embedding
        self.validate_embedding()
        embedding_function = self.embedding.instantiate()

        # Get vector dimensions if not specified
        ndim = self.ndim
        if not ndim:
            try:
                sample_embedding = embedding_function.embed_query("sample")
                ndim = len(sample_embedding)
            except Exception:
                ndim = 1536  # Default dimension

        # Import USearch index
        try:
            import usearch.index
        except ImportError:
            raise ImportError(
                "USearch requires usearch package. " "Install with: pip install usearch"
            )

        # Create USearch index
        try:
            index = usearch.index.Index(ndim=ndim, metric=self.metric)
        except Exception as e:
            raise ValueError(f"Failed to create USearch index: {e}")

        # Create docstore
        from langchain_community.docstore.in_memory import InMemoryDocstore

        docstore = InMemoryDocstore({})

        # Create USearch vector store
        vectorstore = USearch(
            embedding=embedding_function, index=index, docstore=docstore, ids=[]
        )

        return vectorstore
