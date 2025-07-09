"""
Retriever module for the Haive framework.

This module provides a comprehensive interface for document retrieval in the Haive
framework. It includes configuration classes, type definitions, and utilities for
creating and using various types of document retrievers, with support for different
retrieval strategies and extensibility mechanisms.

Key components:
- BaseRetrieverConfig: Base configuration class for all retrievers
- VectorStoreRetrieverConfig: Configuration for vector store-based retrievers
- RetrieverType: Enumeration of supported retriever types
- Utility functions for creating and using retrievers

The retriever system is designed to be highly extensible, with a plugin architecture
that allows new retriever implementations to be added simply by registering them
with the appropriate type. The system includes built-in support for vector store-based
retrievers, ensemble retrievers, and various specialized retrieval strategies.

Examples:
    >>> from haive.core.engine.retriever import BaseRetrieverConfig, RetrieverType
    >>> from haive.core.engine.vectorstore import VectorStoreConfig
    >>>
    >>> # Create a vector store config
    >>> vs_config = VectorStoreConfig(name="document_store")
    >>>
    >>> # Create a retriever config
    >>> retriever_config = BaseRetrieverConfig.from_retriever_type(
    ...     RetrieverType.VECTOR_STORE,
    ...     name="my_retriever",
    ...     vector_store_config=vs_config,
    ...     k=5
    ... )
    >>>
    >>> # Create and use the retriever
    >>> retriever = retriever_config.instantiate()
    >>> documents = retriever.get_relevant_documents("What is machine learning?")
"""

from haive.core.engine.retriever.retriever import (
    BaseRetrieverConfig,
    VectorStoreRetrieverConfig,
    create_retriever_config,
    create_retriever_from_vectorstore,
)
from haive.core.engine.retriever.types import RetrieverType

__all__ = [
    "BaseRetrieverConfig",
    "VectorStoreRetrieverConfig",
    "RetrieverType",
    "create_retriever_config",
    "create_retriever_from_vectorstore",
]
