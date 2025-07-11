"""Multi-Vector Retriever implementation for the Haive framework.

This module provides a configuration class for the Multi-Vector retriever,
which stores multiple vectors per document to enable more nuanced and accurate
retrieval by representing different aspects or summaries of each document.

The MultiVectorRetriever works by:
1. Storing multiple vector representations for each document (summaries, chunks, etc.)
2. Retrieving documents based on these multiple vector representations
3. Supporting different indexing strategies (by summary, by chunks, by hypothetical docs)
4. Providing flexible mapping between vectors and source documents

This retriever is particularly useful when:
- Documents have multiple aspects that should be searchable separately
- Need to index both summaries and full content
- Want to improve retrieval precision with multi-faceted representations
- Building systems that need granular document understanding

The implementation integrates with LangChain's MultiVectorRetriever while
providing a consistent Haive configuration interface with flexible vector storage.
"""

from typing import Any, Dict, List, Optional, Tuple, Type

from pydantic import Field, validator

from haive.core.engine.retriever.retriever import BaseRetrieverConfig
from haive.core.engine.retriever.types import RetrieverType
from haive.core.engine.vectorstore.vectorstore import VectorStoreConfig


@BaseRetrieverConfig.register(RetrieverType.MULTI_VECTOR)
class MultiVectorRetrieverConfig(BaseRetrieverConfig):
    """Configuration for Multi-Vector retriever in the Haive framework.

    This retriever stores multiple vectors per document to enable more nuanced
    and accurate retrieval by representing different aspects of each document.

    Attributes:
        retriever_type (RetrieverType): The type of retriever (always MULTI_VECTOR).
        vectorstore_config (VectorStoreConfig): Vector store for storing multiple vectors.
        docstore_type (str): Type of document store ('in_memory', 'file_system').
        indexing_strategy (str): How to create multiple vectors ('summary', 'chunks', 'hypothetical').
        k (int): Number of documents to return.
        search_kwargs (dict): Additional search parameters for the vector store.

    Examples:
        >>> from haive.core.engine.retriever import MultiVectorRetrieverConfig
        >>> from haive.core.engine.vectorstore.providers.ChromaVectorStoreConfig import ChromaVectorStoreConfig
        >>>
        >>> # Create vector store config
        >>> vs_config = ChromaVectorStoreConfig(
        ...     name="multi_vector_store",
        ...     collection_name="documents"
        ... )
        >>>
        >>> # Create multi-vector retriever
        >>> config = MultiVectorRetrieverConfig(
        ...     name="multi_vector_retriever",
        ...     vectorstore_config=vs_config,
        ...     indexing_strategy="summary",
        ...     k=5
        ... )
        >>>
        >>> # Instantiate and use the retriever
        >>> retriever = config.instantiate()
        >>> docs = retriever.get_relevant_documents("machine learning algorithms")
    """

    retriever_type: RetrieverType = Field(
        default=RetrieverType.MULTI_VECTOR, description="The type of retriever"
    )

    # Core configuration
    vectorstore_config: VectorStoreConfig = Field(
        ..., description="Vector store configuration for storing multiple vectors"
    )

    # Document storage configuration
    docstore_type: str = Field(
        default="in_memory",
        description="Type of document store: 'in_memory', 'file_system'",
    )

    docstore_path: str | None = Field(
        default=None,
        description="Path for file system document store (required if docstore_type='file_system')",
    )

    # Indexing strategy
    indexing_strategy: str = Field(
        default="chunks",
        description="How to create multiple vectors: 'summary', 'chunks', 'hypothetical'",
    )

    # Retrieval parameters
    k: int = Field(default=4, ge=1, le=100, description="Number of documents to return")

    # Vector search configuration
    search_type: str = Field(
        default="similarity",
        description="Type of search to perform: 'similarity', 'mmr'",
    )

    search_kwargs: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional search parameters for the vector store",
    )

    # Multi-vector specific options
    id_key: str = Field(
        default="doc_id", description="Key used to map vectors to documents"
    )

    @validator("docstore_type")
    def validate_docstore_type(self, v):
        """Validate document store type."""
        valid_types = ["in_memory", "file_system"]
        if v not in valid_types:
            raise ValueError(f"docstore_type must be one of {valid_types}, got {v}")
        return v

    @validator("indexing_strategy")
    def validate_indexing_strategy(self, v):
        """Validate indexing strategy."""
        valid_strategies = ["summary", "chunks", "hypothetical"]
        if v not in valid_strategies:
            raise ValueError(
                f"indexing_strategy must be one of {valid_strategies}, got {v}"
            )
        return v

    @validator("search_type")
    def validate_search_type(self, v):
        """Validate search type."""
        valid_types = ["similarity", "mmr"]
        if v not in valid_types:
            raise ValueError(f"search_type must be one of {valid_types}, got {v}")
        return v

    @validator("docstore_path")
    def validate_docstore_path(self, v, values):
        """Validate docstore path is provided when needed."""
        docstore_type = values.get("docstore_type", "")
        if docstore_type == "file_system" and not v:
            raise ValueError(
                "docstore_path is required when docstore_type='file_system'"
            )
        return v

    def get_input_fields(self) -> dict[str, tuple[type, Any]]:
        """Return input field definitions for Multi-Vector retriever."""
        return {
            "query": (str, Field(description="Query for multi-vector retrieval")),
        }

    def get_output_fields(self) -> dict[str, tuple[type, Any]]:
        """Return output field definitions for Multi-Vector retriever."""
        return {
            "documents": (
                list[Any],  # List[Document] but avoiding import
                Field(
                    default_factory=list,
                    description="Documents retrieved via multi-vector search",
                ),
            ),
        }

    def instantiate(self):
        """Create a Multi-Vector retriever from this configuration.

        Returns:
            MultiVectorRetriever: Instantiated retriever ready for multi-vector retrieval.

        Raises:
            ImportError: If required packages are not available.
            ValueError: If configuration is invalid.
        """
        try:
            from langchain.retrievers import MultiVectorRetriever
            from langchain.storage import InMemoryStore
        except ImportError:
            raise ImportError(
                "MultiVectorRetriever requires langchain package. "
                "Install with: pip install langchain"
            )

        # Instantiate the vector store
        try:
            vectorstore = self.vectorstore_config.instantiate()
        except Exception as e:
            raise ValueError(f"Failed to instantiate vector store: {e}")

        # Create the document store
        if self.docstore_type == "in_memory":
            docstore = InMemoryStore()
        elif self.docstore_type == "file_system":
            try:
                from langchain.storage import LocalFileStore

                if not self.docstore_path:
                    raise ValueError(
                        "docstore_path is required for file_system docstore"
                    )
                docstore = LocalFileStore(self.docstore_path)
            except ImportError:
                raise ImportError(
                    "File system document store requires additional packages. "
                    "Install with: pip install langchain[storage]"
                )
        else:
            raise ValueError(f"Unsupported docstore_type: {self.docstore_type}")

        # Create search kwargs
        search_kwargs = dict(self.search_kwargs)
        search_kwargs["k"] = self.k

        if self.search_type == "mmr":
            search_kwargs["search_type"] = "mmr"

        return MultiVectorRetriever(
            vectorstore=vectorstore,
            docstore=docstore,
            id_key=self.id_key,
            search_kwargs=search_kwargs,
        )
