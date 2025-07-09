"""
Core models module for the Haive framework.

This module provides a comprehensive set of model abstractions and implementations
for working with large language models (LLMs), embeddings, retrievers, and vector
stores. The models are designed to be modular, extensible, and optimized for
use within the Haive agent ecosystem.

Key Components:
    - LLM: Large Language Model abstractions and implementations
    - Embeddings: Text embedding models for vector representations
    - Retrievers: Components for retrieving relevant information
    - Vectorstores: Storage systems for embedding vectors with similarity search
    - Metadata: Utilities for working with model metadata

Typical usage example:
    ```python
    from haive.core.models.llm import BaseLLM
    from haive.core.models.embeddings import BaseEmbeddings
    from haive.core.models.retriever import BaseRetriever
    from haive.core.models.vectorstore import BaseVectorStore
    ```
"""

# Import submodules
from haive.core.models import (
    embeddings,
    llm,
    retriever,
    vectorstore,
)

# Model metadata utilities
from haive.core.models.metadata import ModelMetadata
from haive.core.models.metadata_mixin import ModelMetadataMixin as MetadataMixin

__all__ = [
    "ModelMetadata",
    "MetadataMixin",
    "llm",
    "embeddings",
    "retriever",
    "vectorstore",
]
