"""
DocArray Retriever implementation for the Haive framework.

This module provides a configuration class for the DocArray retriever,
which uses DocArray's vector search capabilities for document retrieval.
DocArray is a library for representing, sending, and searching multimodal
data, providing efficient vector operations and search.

The DocArrayRetriever works by:
1. Using DocArray's DocumentArray for document storage
2. Performing vector similarity search with various metrics
3. Supporting efficient in-memory and persisted search
4. Enabling multimodal document processing

This retriever is particularly useful when:
- Working with multimodal documents (text, images, etc.)
- Need efficient in-memory vector search
- Want lightweight vector operations
- Building prototypes or smaller datasets
- Using DocArray for document processing

The implementation integrates with LangChain's DocArrayRetriever while
providing a consistent Haive configuration interface.
"""

from typing import Any, Dict, List, Optional, Tuple, Type

from langchain_core.documents import Document
from pydantic import Field

from haive.core.engine.retriever.retriever import BaseRetrieverConfig
from haive.core.engine.retriever.types import RetrieverType


@BaseRetrieverConfig.register(RetrieverType.DOC_ARRAY)
class DocArrayRetrieverConfig(BaseRetrieverConfig):
    """
    Configuration for DocArray retriever in the Haive framework.

    This retriever uses DocArray's vector search capabilities to provide
    efficient document similarity search with support for multimodal data.

    Attributes:
        retriever_type (RetrieverType): The type of retriever (always DOC_ARRAY).
        documents (List[Document]): Documents to index for retrieval.
        k (int): Number of documents to retrieve.
        similarity_metric (str): Distance metric for similarity calculation.
        embedding_model (Optional[str]): Embedding model for vectorization.
        persist_path (Optional[str]): Path to persist the DocumentArray.

    Examples:
        >>> from haive.core.engine.retriever import DocArrayRetrieverConfig
        >>> from langchain_core.documents import Document
        >>>
        >>> # Create documents
        >>> docs = [
        ...     Document(page_content="Machine learning is a subset of AI"),
        ...     Document(page_content="Deep learning uses neural networks"),
        ...     Document(page_content="Natural language processing handles text")
        ... ]
        >>>
        >>> # Create the DocArray retriever config
        >>> config = DocArrayRetrieverConfig(
        ...     name="docarray_retriever",
        ...     documents=docs,
        ...     k=5,
        ...     similarity_metric="cosine",
        ...     embedding_model="sentence-transformers/all-MiniLM-L6-v2"
        ... )
        >>>
        >>> # Instantiate and use the retriever
        >>> retriever = config.instantiate()
        >>> docs = retriever.get_relevant_documents("neural networks in AI")
        >>>
        >>> # Example with persistence
        >>> persistent_config = DocArrayRetrieverConfig(
        ...     name="persistent_docarray_retriever",
        ...     documents=docs,
        ...     persist_path="./docarray_index",
        ...     similarity_metric="euclidean"
        ... )
    """

    retriever_type: RetrieverType = Field(
        default=RetrieverType.DOC_ARRAY, description="The type of retriever"
    )

    # Documents to index
    documents: List[Document] = Field(
        default_factory=list, description="Documents to index for DocArray retrieval"
    )

    # Search parameters
    k: int = Field(
        default=10, ge=1, le=100, description="Number of documents to retrieve"
    )

    similarity_metric: str = Field(
        default="cosine",
        description="Distance metric: 'cosine', 'euclidean', 'manhattan', 'hamming'",
    )

    # Embedding configuration
    embedding_model: Optional[str] = Field(
        default=None,
        description="Embedding model for vectorization (e.g., 'sentence-transformers/all-MiniLM-L6-v2')",
    )

    # Persistence configuration
    persist_path: Optional[str] = Field(
        default=None, description="Path to persist the DocumentArray index"
    )

    # DocArray specific parameters
    embedding_dimensions: Optional[int] = Field(
        default=None, ge=1, le=4096, description="Embedding vector dimensions"
    )

    index_type: str = Field(
        default="exact", description="Index type for search: 'exact', 'approximate'"
    )

    # Advanced parameters
    batch_size: int = Field(
        default=32, ge=1, le=1000, description="Batch size for embedding computation"
    )

    normalize_embeddings: bool = Field(
        default=True, description="Whether to normalize embeddings"
    )

    def get_input_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return input field definitions for DocArray retriever."""
        return {
            "query": (str, Field(description="Query for DocArray similarity search")),
        }

    def get_output_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return output field definitions for DocArray retriever."""
        return {
            "documents": (
                List[Document],
                Field(
                    default_factory=list, description="Documents from DocArray search"
                ),
            ),
        }

    def instantiate(self):
        """
        Create a DocArray retriever from this configuration.

        Returns:
            DocArrayRetriever: Instantiated retriever ready for multimodal search.

        Raises:
            ImportError: If required packages are not available.
            ValueError: If documents list is empty or configuration is invalid.
        """
        try:
            from langchain_community.retrievers import DocArrayRetriever
        except ImportError:
            raise ImportError(
                "DocArrayRetriever requires langchain-community and docarray packages. "
                "Install with: pip install langchain-community docarray"
            )

        if not self.documents:
            raise ValueError(
                "DocArrayRetriever requires a non-empty list of documents. "
                "Provide documents in the configuration."
            )

        # Prepare configuration
        config = {
            "docs": self.documents,
            "k": self.k,
            "similarity": self.similarity_metric,
        }

        # Add embedding configuration
        if self.embedding_model:
            config["embedding_model"] = self.embedding_model

        if self.embedding_dimensions:
            config["embedding_dimensions"] = self.embedding_dimensions

        # Add persistence configuration
        if self.persist_path:
            config["persist_path"] = self.persist_path

        # Add advanced parameters
        config["index_type"] = self.index_type
        config["batch_size"] = self.batch_size
        config["normalize_embeddings"] = self.normalize_embeddings

        return DocArrayRetriever.from_documents(**config)
