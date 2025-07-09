"""
Parent Document Retriever implementation for the Haive framework.

This module provides a configuration class for the Parent Document retriever,
which retrieves small chunks for embedding similarity but returns larger parent
documents containing those chunks, providing better context while maintaining
search precision.

The ParentDocumentRetriever works by:
1. Splitting documents into small chunks for embedding and similarity search
2. Storing these chunks in a vector store with references to parent documents
3. Storing full parent documents in a separate document store
4. When querying, finding similar chunks but returning their parent documents

This retriever is particularly useful when:
- Need precise similarity search on small chunks
- Want to return full context from larger parent documents
- Building systems that balance search precision with context completeness
- Dealing with long documents that need chunk-level search

The implementation integrates with LangChain's ParentDocumentRetriever while
providing a consistent Haive configuration interface with flexible chunking options.
"""

from typing import Any, Dict, List, Optional, Tuple, Type

from pydantic import Field, validator

from haive.core.engine.retriever.retriever import BaseRetrieverConfig
from haive.core.engine.retriever.types import RetrieverType
from haive.core.engine.vectorstore.vectorstore import VectorStoreConfig


@BaseRetrieverConfig.register(RetrieverType.PARENT_DOCUMENT)
class ParentDocumentRetrieverConfig(BaseRetrieverConfig):
    """
    Configuration for Parent Document retriever in the Haive framework.

    This retriever retrieves small chunks for similarity search but returns larger
    parent documents, providing better context while maintaining search precision.

    Attributes:
        retriever_type (RetrieverType): The type of retriever (always PARENT_DOCUMENT).
        vectorstore_config (VectorStoreConfig): Vector store for storing child chunks.
        docstore_type (str): Type of document store for parent documents.
        child_chunk_size (int): Size of child chunks for embedding.
        child_chunk_overlap (int): Overlap between child chunks.
        k (int): Number of child chunks to retrieve (returns their parents).

    Examples:
        >>> from haive.core.engine.retriever import ParentDocumentRetrieverConfig
        >>> from haive.core.engine.vectorstore.providers.ChromaVectorStoreConfig import ChromaVectorStoreConfig
        >>>
        >>> # Create vector store config
        >>> vs_config = ChromaVectorStoreConfig(
        ...     name="parent_doc_store",
        ...     collection_name="child_chunks"
        ... )
        >>>
        >>> # Create parent document retriever
        >>> config = ParentDocumentRetrieverConfig(
        ...     name="parent_doc_retriever",
        ...     vectorstore_config=vs_config,
        ...     child_chunk_size=200,
        ...     child_chunk_overlap=20,
        ...     k=4
        ... )
        >>>
        >>> # Instantiate and use the retriever
        >>> retriever = config.instantiate()
        >>> docs = retriever.get_relevant_documents("machine learning algorithms")
    """

    retriever_type: RetrieverType = Field(
        default=RetrieverType.PARENT_DOCUMENT, description="The type of retriever"
    )

    # Core configuration
    vectorstore_config: VectorStoreConfig = Field(
        ..., description="Vector store configuration for storing child chunks"
    )

    # Document storage configuration
    docstore_type: str = Field(
        default="in_memory",
        description="Type of document store for parent documents: 'in_memory', 'file_system'",
    )

    docstore_path: Optional[str] = Field(
        default=None,
        description="Path for file system document store (required if docstore_type='file_system')",
    )

    # Child chunk parameters
    child_chunk_size: int = Field(
        default=200,
        ge=50,
        le=2000,
        description="Size of child chunks for embedding and similarity search",
    )

    child_chunk_overlap: int = Field(
        default=20, ge=0, le=500, description="Overlap between child chunks"
    )

    # Retrieval parameters
    k: int = Field(
        default=4,
        ge=1,
        le=100,
        description="Number of child chunks to retrieve (returns their parent documents)",
    )

    @validator("docstore_type")
    def validate_docstore_type(cls, v):
        """Validate document store type."""
        valid_types = ["in_memory", "file_system"]
        if v not in valid_types:
            raise ValueError(f"docstore_type must be one of {valid_types}, got {v}")
        return v

    @validator("child_chunk_overlap")
    def validate_child_chunk_overlap(cls, v, values):
        """Validate that child chunk overlap is less than chunk size."""
        chunk_size = values.get("child_chunk_size", 200)
        if v >= chunk_size:
            raise ValueError(
                f"child_chunk_overlap ({v}) must be less than child_chunk_size ({chunk_size})"
            )
        return v

    @validator("docstore_path")
    def validate_docstore_path(cls, v, values):
        """Validate docstore path is provided when needed."""
        docstore_type = values.get("docstore_type", "")
        if docstore_type == "file_system" and not v:
            raise ValueError(
                "docstore_path is required when docstore_type='file_system'"
            )
        return v

    def get_input_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return input field definitions for Parent Document retriever."""
        return {
            "query": (str, Field(description="Query for parent document retrieval")),
        }

    def get_output_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return output field definitions for Parent Document retriever."""
        return {
            "documents": (
                List[Any],  # List[Document] but avoiding import
                Field(
                    default_factory=list,
                    description="Parent documents of retrieved child chunks",
                ),
            ),
        }

    def instantiate(self):
        """
        Create a Parent Document retriever from this configuration.

        Returns:
            ParentDocumentRetriever: Instantiated retriever ready for parent document retrieval.

        Raises:
            ImportError: If required packages are not available.
            ValueError: If configuration is invalid.
        """
        try:
            from langchain.retrievers import ParentDocumentRetriever
            from langchain.storage import InMemoryStore
            from langchain.text_splitter import RecursiveCharacterTextSplitter
        except ImportError:
            raise ImportError(
                "ParentDocumentRetriever requires langchain package. "
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

        # Create child splitter
        child_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.child_chunk_size,
            chunk_overlap=self.child_chunk_overlap,
        )

        return ParentDocumentRetriever(
            vectorstore=vectorstore,
            docstore=docstore,
            child_splitter=child_splitter,
            search_kwargs={"k": self.k},
        )
