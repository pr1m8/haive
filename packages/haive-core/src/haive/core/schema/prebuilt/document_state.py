"""Document State Schema for the Haive Document Engine.

This module provides a comprehensive state schema for document processing workflows,
integrating with the document loader system and providing state management for
document loading, processing, and analysis operations.

Author: Claude (Haive AI Agent Framework)
Version: 1.0.0
"""

from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from langchain_core.documents import Document
from pydantic import Field

from haive.core.engine.document.config import (
    ChunkingStrategy,
    DocumentFormat,
    DocumentInput,
    DocumentOutput,
    DocumentSourceType,
    LoaderPreference,
    ProcessedDocument,
    ProcessingStrategy,
)
from haive.core.schema import StateSchema


class DocumentEngineInputSchema(StateSchema):
    """Input schema for document engine operations.

    This schema defines the input state for document loading and processing,
    supporting various source types and configuration options.

    Examples:
        Basic file loading::

            state = DocumentEngineInputSchema(
                source="/path/to/document.pdf",
                source_type=DocumentSourceType.FILE
            )

        Web scraping with options::

            state = DocumentEngineInputSchema(
                source="https://example.com",
                source_type=DocumentSourceType.URL,
                loader_options={"verify_ssl": True},
                processing_options={"extract_links": True}
            )

        Bulk loading configuration::

            state = DocumentEngineInputSchema(
                sources=["/path/to/doc1.pdf", "/path/to/doc2.docx"],
                loader_preference=LoaderPreference.QUALITY,
                chunking_strategy=ChunkingStrategy.SEMANTIC
            )
    """

    # Primary source(s)
    source: Optional[Union[str, Path, Dict[str, Any]]] = Field(
        default=None,
        description="Primary source to process (path, URL, or configuration dict)",
    )

    sources: Optional[List[Union[str, Path, Dict[str, Any]]]] = Field(
        default=None, description="Multiple sources for bulk processing"
    )

    # Source configuration
    source_type: Optional[DocumentSourceType] = Field(
        default=None, description="Explicit source type (auto-detected if not provided)"
    )

    loader_name: Optional[str] = Field(
        default=None,
        description="Specific loader to use (auto-selected if not provided)",
    )

    loader_preference: LoaderPreference = Field(
        default=LoaderPreference.BALANCED,
        description="Preference for loader selection (speed vs quality)",
    )

    # Processing configuration
    processing_strategy: ProcessingStrategy = Field(
        default=ProcessingStrategy.ENHANCED,
        description="Strategy for document processing",
    )

    chunking_strategy: ChunkingStrategy = Field(
        default=ChunkingStrategy.RECURSIVE, description="Strategy for document chunking"
    )

    chunk_size: int = Field(
        default=1000, ge=1, description="Size of chunks in characters"
    )

    chunk_overlap: int = Field(
        default=200, ge=0, description="Overlap between chunks in characters"
    )

    # Loading options
    recursive: bool = Field(
        default=True, description="Whether to recursively process directories"
    )

    max_documents: Optional[int] = Field(
        default=None, ge=1, description="Maximum number of documents to load"
    )

    use_async: bool = Field(
        default=False, description="Whether to use async loading when available"
    )

    parallel_processing: bool = Field(
        default=True, description="Whether to enable parallel processing"
    )

    max_workers: int = Field(
        default=4, ge=1, le=32, description="Maximum number of worker threads"
    )

    # Filtering options
    include_patterns: List[str] = Field(
        default_factory=list, description="Glob patterns for files to include"
    )

    exclude_patterns: List[str] = Field(
        default_factory=list, description="Glob patterns for files to exclude"
    )

    # Additional options
    loader_options: Dict[str, Any] = Field(
        default_factory=dict, description="Additional loader-specific options"
    )

    processing_options: Dict[str, Any] = Field(
        default_factory=dict, description="Additional processing options"
    )

    # Caching
    enable_caching: bool = Field(default=False, description="Enable document caching")

    cache_ttl: int = Field(
        default=3600, ge=60, description="Cache time-to-live in seconds"
    )


class DocumentEngineOutputSchema(StateSchema):
    """Output schema for document engine operations.

    This schema defines the output state from document loading and processing,
    containing loaded documents, metadata, and processing statistics.

    Examples:
        Successful loading result::

            output = DocumentEngineOutputSchema(
                documents=[ProcessedDocument(...)],
                total_documents=10,
                successful_documents=10,
                operation_time=5.2
            )

        Partial success with errors::

            output = DocumentEngineOutputSchema(
                documents=[...],
                total_documents=10,
                successful_documents=8,
                failed_documents=2,
                errors=[
                    {"source": "bad.pdf", "error": "Corrupted file"},
                    {"source": "missing.docx", "error": "File not found"}
                ]
            )
    """

    # Loaded documents
    documents: List[ProcessedDocument] = Field(
        default_factory=list, description="List of processed documents"
    )

    # Raw documents (langchain format)
    raw_documents: List[Document] = Field(
        default_factory=list, description="Raw langchain Document objects"
    )

    # Operation metadata
    total_documents: int = Field(default=0, description="Total documents processed")

    successful_documents: int = Field(
        default=0, description="Successfully processed documents"
    )

    failed_documents: int = Field(default=0, description="Failed document count")

    # Timing information
    operation_time: float = Field(
        default=0.0, description="Total operation time in seconds"
    )

    average_processing_time: float = Field(
        default=0.0, description="Average processing time per document"
    )

    # Source information
    original_source: Optional[str] = Field(
        default=None, description="Original source path/URL"
    )

    source_type: Optional[DocumentSourceType] = Field(
        default=None, description="Detected or specified source type"
    )

    # Processing information
    loader_names: List[str] = Field(
        default_factory=list, description="Names of loaders used"
    )

    processing_strategy: Optional[ProcessingStrategy] = Field(
        default=None, description="Processing strategy used"
    )

    chunking_strategy: Optional[ChunkingStrategy] = Field(
        default=None, description="Chunking strategy used"
    )

    # Statistics
    total_chunks: int = Field(default=0, description="Total number of chunks created")

    total_characters: int = Field(
        default=0, description="Total character count across all documents"
    )

    total_words: int = Field(default=0, description="Estimated total word count")

    # Errors and warnings
    errors: List[Dict[str, Any]] = Field(
        default_factory=list, description="Errors encountered during processing"
    )

    warnings: List[Dict[str, Any]] = Field(
        default_factory=list, description="Warnings generated during processing"
    )

    # Additional metadata
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Additional operation metadata"
    )

    def add_document(self, document: ProcessedDocument) -> None:
        """Add a processed document to the output.

        Args:
            document: ProcessedDocument to add
        """
        self.documents.append(document)
        self.total_documents += 1
        self.successful_documents += 1
        self.total_chunks += document.chunk_count
        self.total_characters += document.character_count
        self.total_words += document.word_count

        if document.loader_name not in self.loader_names:
            self.loader_names.append(document.loader_name)

    def add_error(
        self, source: str, error: str, details: Optional[Dict[str, Any]] = None
    ) -> None:
        """Add an error to the output.

        Args:
            source: Source that caused the error
            error: Error message
            details: Optional additional error details
        """
        error_entry = {
            "source": source,
            "error": error,
            "timestamp": None,  # Would be set by the engine
        }
        if details:
            error_entry.update(details)

        self.errors.append(error_entry)
        self.failed_documents += 1
        self.total_documents += 1

    def calculate_statistics(self) -> None:
        """Calculate aggregate statistics from loaded documents."""
        if self.successful_documents > 0:
            self.average_processing_time = (
                self.operation_time / self.successful_documents
            )

        # Update totals from documents
        self.total_chunks = sum(doc.chunk_count for doc in self.documents)
        self.total_characters = sum(doc.character_count for doc in self.documents)
        self.total_words = sum(doc.word_count for doc in self.documents)


class DocumentState(StateSchema):
    """Complete document processing state.

    This schema combines input and output states for complete document
    processing workflows, maintaining the full context of document operations.

    Examples:
        Complete workflow state::

            state = DocumentState(
                # Input configuration
                source="/documents/",
                source_type=DocumentSourceType.DIRECTORY,
                recursive=True,

                # Processing results
                documents=[...],
                total_documents=50,
                successful_documents=48,

                # Workflow metadata
                processing_stage="completed",
                last_processed_index=50
            )
    """

    # Input state (inherited from DocumentEngineInputSchema)
    source: Optional[Union[str, Path, Dict[str, Any]]] = Field(
        default=None, description="Primary source to process"
    )

    sources: Optional[List[Union[str, Path, Dict[str, Any]]]] = Field(
        default=None, description="Multiple sources for bulk processing"
    )

    source_type: Optional[DocumentSourceType] = Field(
        default=None, description="Source type"
    )

    loader_preference: LoaderPreference = Field(
        default=LoaderPreference.BALANCED, description="Loader preference"
    )

    processing_strategy: ProcessingStrategy = Field(
        default=ProcessingStrategy.ENHANCED, description="Processing strategy"
    )

    # Output state (inherited from DocumentEngineOutputSchema)
    documents: List[ProcessedDocument] = Field(
        default_factory=list,
        description="Processed documents",
        shared=True,  # Shared across workflow nodes
    )

    raw_documents: List[Document] = Field(
        default_factory=list, description="Raw langchain documents", shared=True
    )

    total_documents: int = Field(default=0, description="Total documents", shared=True)

    successful_documents: int = Field(
        default=0, description="Successful documents", shared=True
    )

    errors: List[Dict[str, Any]] = Field(
        default_factory=list, description="Processing errors", shared=True
    )

    # Workflow state
    processing_stage: str = Field(
        default="initialized", description="Current processing stage", shared=True
    )

    last_processed_index: int = Field(
        default=0, description="Index of last processed document", shared=True
    )

    # Additional workflow metadata
    workflow_metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Workflow-specific metadata", shared=True
    )
