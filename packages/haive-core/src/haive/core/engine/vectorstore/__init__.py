"""
Vector store module for the Haive framework.

This module provides a comprehensive interface for working with vector databases
in the Haive framework. It includes configuration models, utility functions, and
abstractions for creating and interacting with vector stores through a unified API.

Key components:
- VectorStoreConfig: Main configuration class for vector stores
- VectorStoreProvider: Enumeration of supported vector store providers
- Utility functions for creating vector stores and retrievers

The vector store system supports various backends (FAISS, Chroma, Pinecone, etc.)
and provides a consistent interface for embedding, storing, and retrieving documents
using vector similarity.

Examples:
    >>> from haive.core.engine.vectorstore import (
    ...     VectorStoreConfig,
    ...     VectorStoreProvider,
    ...     create_vs_from_documents
    ... )
    >>> from langchain_core.documents import Document
    >>>
    >>> # Create documents
    >>> documents = [
    ...     Document(page_content="Apple iPhone 13 with A15 Bionic chip"),
    ...     Document(page_content="Samsung Galaxy S21 with Exynos processor")
    ... ]
    >>>
    >>> # Create a vector store directly
    >>> vectorstore = create_vs_from_documents(
    ...     documents,
    ...     vector_store_provider=VectorStoreProvider.FAISS
    ... )
    >>>
    >>> # Search for similar documents
    >>> results = vectorstore.similarity_search("smartphone with fast processor")
"""

from haive.core.engine.vectorstore.vectorstore import (
    VectorStoreConfig,
    VectorStoreProvider,
    VectorStoreProviderRegistry,
    create_retriever,
    create_retriever_from_documents,
    create_vectorstore,
    create_vs_config_from_documents,
    create_vs_from_documents,
)

__all__ = [
    "VectorStoreConfig",
    "VectorStoreProvider",
    "VectorStoreProviderRegistry",
    "create_retriever",
    "create_retriever_from_documents",
    "create_vectorstore",
    "create_vs_config_from_documents",
    "create_vs_from_documents",
]
