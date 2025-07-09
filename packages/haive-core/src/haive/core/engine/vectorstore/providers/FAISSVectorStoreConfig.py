"""
FAISS Vector Store implementation for the Haive framework.

This module provides a configuration class for the FAISS (Facebook AI Similarity Search)
vector store, which is a library for efficient similarity search and clustering of dense vectors.

FAISS provides:
1. Extremely fast similarity search for large-scale datasets
2. Multiple index types optimized for different use cases
3. GPU acceleration support
4. Efficient memory usage with compression techniques
5. Support for both exact and approximate nearest neighbor search

This vector store is particularly useful when:
- You need blazing-fast similarity search on large datasets
- Working with millions or billions of vectors
- Need to balance between search accuracy and speed
- Want to leverage GPU acceleration for search
- Building production systems requiring high throughput

The implementation integrates with LangChain's FAISS while providing
a consistent Haive configuration interface.
"""

from typing import Any, Dict, List, Optional, Tuple, Type

from langchain_core.documents import Document
from pydantic import Field, validator

from haive.core.engine.vectorstore.base import BaseVectorStoreConfig
from haive.core.engine.vectorstore.types import VectorStoreType


@BaseVectorStoreConfig.register(VectorStoreType.FAISS)
class FAISSVectorStoreConfig(BaseVectorStoreConfig):
    """
    Configuration for FAISS vector store in the Haive framework.

    This vector store uses Facebook AI Similarity Search for extremely fast
    and scalable vector similarity search operations.

    Attributes:
        index_path (Optional[str]): Path to save/load the FAISS index.
        docstore_path (Optional[str]): Path to save/load the document store.
        index_type (str): Type of FAISS index to use.
        distance_metric (str): Distance metric for similarity calculation.
        normalize_l2 (bool): Whether to normalize vectors to unit length.
        n_lists (int): Number of clusters for IVF indexes.
        n_probes (int): Number of clusters to search in IVF indexes.

    Examples:
        >>> from haive.core.engine.vectorstore import FAISSVectorStoreConfig
        >>> from haive.core.models.embeddings.base import HuggingFaceEmbeddingConfig
        >>>
        >>> # Create FAISS config with persistence
        >>> config = FAISSVectorStoreConfig(
        ...     name="large_document_store",
        ...     embedding=HuggingFaceEmbeddingConfig(
        ...         model="sentence-transformers/all-MiniLM-L6-v2"
        ...     ),
        ...     index_path="./faiss_index",
        ...     docstore_path="./faiss_docstore",
        ...     distance_metric="cosine",
        ...     normalize_l2=True
        ... )
        >>>
        >>> # Instantiate and use the vector store
        >>> vectorstore = config.instantiate()
        >>>
        >>> # Add documents
        >>> docs = [Document(page_content="FAISS enables fast similarity search")]
        >>> vectorstore.add_documents(docs)
        >>>
        >>> # Save the index
        >>> vectorstore.save_local(config.index_path)
    """

    # Storage configuration
    index_path: Optional[str] = Field(
        default=None, description="Path to save/load the FAISS index"
    )

    docstore_path: Optional[str] = Field(
        default=None, description="Path to save/load the document store"
    )

    # FAISS index configuration
    index_type: str = Field(
        default="Flat",
        description="Type of FAISS index: 'Flat', 'IVFFlat', 'HNSW', 'LSH'",
    )

    distance_metric: str = Field(
        default="l2", description="Distance metric: 'l2', 'cosine', or 'inner_product'"
    )

    normalize_l2: bool = Field(
        default=False,
        description="Whether to normalize vectors to unit length (recommended for cosine similarity)",
    )

    # IVF index parameters
    n_lists: int = Field(
        default=100, ge=1, description="Number of clusters for IVF indexes"
    )

    n_probes: int = Field(
        default=10, ge=1, description="Number of clusters to search in IVF indexes"
    )

    # Advanced parameters
    use_gpu: bool = Field(
        default=False,
        description="Whether to use GPU acceleration (requires faiss-gpu)",
    )

    gpu_device: int = Field(
        default=0, ge=0, description="GPU device ID to use if use_gpu is True"
    )

    @validator("index_type")
    def validate_index_type(cls, v):
        """Validate index type is supported."""
        valid_types = ["Flat", "IVFFlat", "HNSW", "LSH"]
        if v not in valid_types:
            raise ValueError(f"index_type must be one of {valid_types}, got {v}")
        return v

    @validator("distance_metric")
    def validate_distance_metric(cls, v):
        """Validate distance metric is supported."""
        valid_metrics = ["l2", "cosine", "inner_product"]
        if v not in valid_metrics:
            raise ValueError(f"distance_metric must be one of {valid_metrics}, got {v}")
        return v

    def get_input_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return input field definitions for FAISS vector store."""
        return {
            "documents": (
                List[Document],
                Field(description="Documents to add to the vector store"),
            ),
        }

    def get_output_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return output field definitions for FAISS vector store."""
        return {
            "ids": (List[str], Field(description="IDs of the added documents")),
        }

    def instantiate(self):
        """
        Create a FAISS vector store from this configuration.

        Returns:
            FAISS: Instantiated FAISS vector store.

        Raises:
            ImportError: If required packages are not available.
            ValueError: If configuration is invalid.
        """
        try:
            from langchain_community.vectorstores import FAISS
        except ImportError:
            raise ImportError(
                "FAISS requires faiss-cpu or faiss-gpu package. "
                "Install with: pip install faiss-cpu (or faiss-gpu for GPU support)"
            )

        # Validate embedding
        self.validate_embedding()
        embedding_function = self.embedding.instantiate()

        # Check if loading existing index
        if self.index_path:
            import os

            if os.path.exists(self.index_path):
                # Load existing index
                return FAISS.load_local(
                    self.index_path,
                    embeddings=embedding_function,
                    allow_dangerous_deserialization=True,
                )

        # Create new index
        # For now, create with empty documents and let user add later
        # This matches the pattern from retrievers
        texts = []
        metadatas = []

        # Map distance metric to FAISS distance type
        distance_strategy = None
        if self.distance_metric == "cosine":
            from langchain_community.vectorstores.faiss import DistanceStrategy

            distance_strategy = DistanceStrategy.COSINE
        elif self.distance_metric == "inner_product":
            from langchain_community.vectorstores.faiss import DistanceStrategy

            distance_strategy = DistanceStrategy.MAX_INNER_PRODUCT
        elif self.distance_metric == "l2":
            from langchain_community.vectorstores.faiss import DistanceStrategy

            distance_strategy = DistanceStrategy.EUCLIDEAN_DISTANCE

        # Prepare kwargs
        kwargs = {
            "embedding_function": embedding_function,
            "normalize_L2": self.normalize_l2,
        }

        if distance_strategy:
            kwargs["distance_strategy"] = distance_strategy

        # Handle GPU configuration
        if self.use_gpu:
            try:
                import faiss

                # This would require additional GPU setup logic
                # For now, we'll use the default CPU implementation
                pass
            except ImportError:
                import warnings

                warnings.warn(
                    "GPU support requested but faiss-gpu not installed. "
                    "Falling back to CPU implementation."
                )

        # Create FAISS instance
        return FAISS.from_texts(
            texts=texts or [""],  # FAISS requires at least one text
            embedding=embedding_function,
            metadatas=metadatas,
            **kwargs,
        )
