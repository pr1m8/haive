"""Document state schema for Haive document agents.

This module provides the state schema classes for document operations in Haive agents.
It includes classes for representing document sources, loaded documents, and the
overall document state for use in document processing agents.

This module is a simplified wrapper around the more comprehensive document_models.py,
providing backward compatibility while encouraging the use of the new models.
"""

from __future__ import annotations

# For backward compatibility
from haive.core.schema.base import StateSchema

from .document_models import (  # Enums; Configuration models; Document models; State models; Converter functions
    ChunkingOptions, ChunkingStrategy, Document, DocumentChunk,
    DocumentCollection, DocumentCredential, DocumentError, DocumentFormat,
    DocumentSource, DocumentSourceMetadata, DocumentSourceType, DocumentState,
    EmbeddingModel, EmbeddingOptions, LoadingOptions, LoadingStrategy,
    ProcessingStage, ProcessingStatistics, chunks_to_langchain,
    documents_to_langchain, lc_documents_to_document_collection)

# Ensure DocumentState is a StateSchema if the import succeeded
try:
    if not issubclass(DocumentState, StateSchema):
        # Dynamically update the DocumentState class to inherit from StateSchema
        DocumentState.__bases__ = (StateSchema, *DocumentState.__bases__)
except (NameError, TypeError):
    # If StateSchema is not available, we're likely in a standalone environment
    pass

__all__ = [
    "ChunkingOptions",
    "ChunkingStrategy",
    "Document",
    "DocumentChunk",
    "DocumentCollection",
    "DocumentCredential",
    "DocumentError",
    "DocumentFormat",
    "DocumentSource",
    # Document models
    "DocumentSourceMetadata",
    # Enums
    "DocumentSourceType",
    # State models
    "DocumentState",
    "EmbeddingModel",
    "EmbeddingOptions",
    # Configuration models
    "LoadingOptions",
    "LoadingStrategy",
    "ProcessingStage",
    "ProcessingStatistics",
    "chunks_to_langchain",
    "documents_to_langchain",
    # Converter functions
    "lc_documents_to_document_collection",
]
