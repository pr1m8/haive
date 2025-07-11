"""InMemory Vector Store implementation for the Haive framework.

This module provides a configuration class for the InMemory vector store,
which provides simple in-memory vector operations for development and testing.

InMemory provides:
1. Simple dictionary-based storage
2. Cosine similarity search using numpy
3. No external dependencies beyond langchain-core
4. Fast development and testing setup
5. Document filtering capabilities
6. Maximal marginal relevance search

This vector store is particularly useful when:
- You need quick development and testing
- Want no external dependencies
- Building prototypes and proofs of concept
- Need simple vector operations
- Testing vector search functionality

The implementation integrates with LangChain's InMemoryVectorStore while providing
a consistent Haive configuration interface.
"""

from typing import Any, Dict, List, Optional, Tuple, Type

from langchain_core.documents import Document
from pydantic import Field

from haive.core.engine.vectorstore.base import BaseVectorStoreConfig
from haive.core.engine.vectorstore.types import VectorStoreType


@BaseVectorStoreConfig.register(VectorStoreType.IN_MEMORY)
class InMemoryVectorStoreConfig(BaseVectorStoreConfig):
    """Configuration for InMemory vector store in the Haive framework.

    This vector store uses simple in-memory storage with cosine similarity
    for development and testing purposes.

    Examples:
        >>> from haive.core.engine.vectorstore import InMemoryVectorStoreConfig
        >>> from haive.core.models.embeddings.base import OpenAIEmbeddingConfig
        >>>
        >>> # Create InMemory config
        >>> config = InMemoryVectorStoreConfig(
        ...     name="memory_vectors",
        ...     embedding=OpenAIEmbeddingConfig()
        ... )
        >>>
        >>> # Instantiate and use
        >>> vectorstore = config.instantiate()
        >>> docs = [Document(page_content="InMemory provides simple vector search")]
        >>> vectorstore.add_documents(docs)
        >>>
        >>> # Simple similarity search
        >>> results = vectorstore.similarity_search("simple search", k=5)
        >>>
        >>> # Search with custom filter
        >>> def filter_func(doc):
        ...     return doc.metadata.get("category") == "test"
        >>> filtered_results = vectorstore.similarity_search(
        ...     "search query", k=5, filter=filter_func
        ... )
    """

    def get_input_fields(self) -> dict[str, tuple[type, Any]]:
        """Return input field definitions for InMemory vector store."""
        return {
            "documents": (
                list[Document],
                Field(description="Documents to add to the vector store"),
            ),
        }

    def get_output_fields(self) -> dict[str, tuple[type, Any]]:
        """Return output field definitions for InMemory vector store."""
        return {
            "ids": (
                list[str],
                Field(description="IDs of the added documents in InMemory store"),
            ),
        }

    def instantiate(self):
        """Create an InMemory vector store from this configuration.

        Returns:
            InMemoryVectorStore: Instantiated InMemory vector store.

        Raises:
            ImportError: If required packages are not available.
            ValueError: If configuration is invalid.
        """
        try:
            from langchain_core.vectorstores import InMemoryVectorStore
        except ImportError:
            raise ImportError(
                "InMemory vector store requires langchain-core package. "
                "This should be available as it's a core dependency."
            )

        # Validate embedding
        self.validate_embedding()
        embedding_function = self.embedding.instantiate()

        # Create InMemory vector store
        try:
            vectorstore = InMemoryVectorStore(embedding=embedding_function)
        except Exception as e:
            raise ValueError(f"Failed to create InMemory vector store: {e}")

        return vectorstore
