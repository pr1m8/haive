"""Enhanced Document Engine Configuration.

This module provides comprehensive configuration models for the document engine,
integrating with the existing Haive engine framework while adding enhanced
functionality for document loading, processing, and management.
"""

from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Union

from langchain_core.documents import Document
from pydantic import BaseModel, Field, field_validator, model_validator

from haive.core.common.mixins.tool_route_mixin import ToolRouteMixin
from haive.core.engine.base import InvokableEngine
from haive.core.engine.base.types import EngineType


class LoaderPreference(str, Enum):
    """Preference for loader selection when multiple are available."""

    SPEED = "speed"
    QUALITY = "quality"
    BALANCED = "balanced"


class ProcessingStrategy(str, Enum):
    """Strategy for document processing."""

    SIMPLE = "simple"
    ENHANCED = "enhanced"
    PARALLEL = "parallel"


class ChunkingStrategy(str, Enum):
    """Strategy for document chunking."""

    NONE = "none"
    FIXED_SIZE = "fixed_size"
    RECURSIVE = "recursive"
    PARAGRAPH = "paragraph"
    SENTENCE = "sentence"
    SEMANTIC = "semantic"


class DocumentFormat(str, Enum):
    """Document format classification."""

    PDF = "pdf"
    DOCX = "docx"
    TXT = "txt"
    HTML = "html"
    MARKDOWN = "markdown"
    JSON = "json"
    CSV = "csv"
    XML = "xml"
    UNKNOWN = "unknown"


class DocumentSourceType(str, Enum):
    """Document source type classification."""

    FILE = "file"
    DIRECTORY = "directory"
    URL = "url"
    DATABASE = "database"
    CLOUD = "cloud"
    STREAM = "stream"
    TEXT = "text"
    UNKNOWN = "unknown"


class DocumentEngineConfig(BaseModel):
    """Enhanced configuration for the document engine.

    This configuration extends the basic document loader config with enhanced
    processing capabilities, chunking strategies, and integration options.
    """

    # Engine identification
    engine_type: EngineType = Field(
        default=EngineType.DOCUMENT_LOADER, description="Type of the engine"
    )

    name: str = Field(
        default="document_engine", description="Name of the engine instance"
    )

    # Source configuration
    source_type: Optional[DocumentSourceType] = Field(
        default=None, description="Explicit source type (auto-detected if not provided)"
    )

    # Loader configuration
    loader_name: Optional[str] = Field(
        default=None,
        description="Specific loader to use (auto-selected if not provided)",
    )

    loader_preference: LoaderPreference = Field(
        default=LoaderPreference.BALANCED, description="Preference for loader selection"
    )

    # Processing configuration
    processing_strategy: ProcessingStrategy = Field(
        default=ProcessingStrategy.ENHANCED,
        description="Strategy for document processing",
    )

    # Chunking configuration
    chunking_strategy: ChunkingStrategy = Field(
        default=ChunkingStrategy.RECURSIVE, description="Strategy for document chunking"
    )

    chunk_size: int = Field(
        default=1000, description="Size of chunks in characters", ge=1
    )

    chunk_overlap: int = Field(
        default=200, description="Overlap between chunks in characters", ge=0
    )

    # Loading options
    recursive: bool = Field(
        default=True, description="Whether to recursively process directories"
    )

    max_documents: Optional[int] = Field(
        default=None, description="Maximum number of documents to load", ge=1
    )

    use_async: bool = Field(
        default=False, description="Whether to use async loading when available"
    )

    parallel_processing: bool = Field(
        default=True, description="Whether to enable parallel processing"
    )

    max_workers: int = Field(
        default=4, description="Maximum number of worker threads", ge=1, le=32
    )

    # Filtering options
    include_patterns: List[str] = Field(
        default_factory=list, description="Glob patterns for files to include"
    )

    exclude_patterns: List[str] = Field(
        default_factory=list, description="Glob patterns for files to exclude"
    )

    supported_formats: List[DocumentFormat] = Field(
        default_factory=lambda: list(DocumentFormat),
        description="Supported document formats",
    )

    # Content processing
    extract_metadata: bool = Field(
        default=True, description="Whether to extract document metadata"
    )

    normalize_content: bool = Field(
        default=True, description="Whether to normalize content (whitespace, encoding)"
    )

    detect_language: bool = Field(
        default=False, description="Whether to detect document language"
    )

    # Error handling
    raise_on_error: bool = Field(
        default=False,
        description="Whether to raise exceptions on individual document errors",
    )

    skip_invalid: bool = Field(
        default=True, description="Whether to skip invalid documents"
    )

    # Caching
    enable_caching: bool = Field(
        default=False, description="Whether to enable document caching"
    )

    cache_ttl: int = Field(default=3600, description="Cache TTL in seconds", ge=0)

    # Additional options
    loader_options: Dict[str, Any] = Field(
        default_factory=dict, description="Additional options passed to loaders"
    )

    processing_options: Dict[str, Any] = Field(
        default_factory=dict, description="Additional options for processing"
    )

    @field_validator("chunk_overlap")
    @classmethod
    def validate_chunk_overlap(cls, v: int, info) -> int:
        """Validate that chunk overlap is less than chunk size."""
        if hasattr(info, "data") and "chunk_size" in info.data:
            chunk_size = info.data["chunk_size"]
            if v >= chunk_size:
                raise ValueError("chunk_overlap must be less than chunk_size")
        return v


class DocumentInput(BaseModel):
    """Input model for document operations."""

    # Primary source
    source: Union[str, Path, Dict[str, Any]] = Field(
        ..., description="Source to process (path, URL, or configuration dict)"
    )

    # Override options
    source_type: Optional[DocumentSourceType] = Field(
        default=None, description="Override source type for this operation"
    )

    loader_name: Optional[str] = Field(
        default=None, description="Override loader for this operation"
    )

    # Processing overrides
    chunking_strategy: Optional[ChunkingStrategy] = Field(
        default=None, description="Override chunking strategy"
    )

    chunk_size: Optional[int] = Field(
        default=None, description="Override chunk size", ge=1
    )

    chunk_overlap: Optional[int] = Field(
        default=None, description="Override chunk overlap", ge=0
    )

    # Filtering overrides
    include_patterns: Optional[List[str]] = Field(
        default=None, description="Override include patterns"
    )

    exclude_patterns: Optional[List[str]] = Field(
        default=None, description="Override exclude patterns"
    )

    # Additional options
    loader_options: Dict[str, Any] = Field(
        default_factory=dict, description="Additional loader options"
    )

    processing_options: Dict[str, Any] = Field(
        default_factory=dict, description="Additional processing options"
    )


class DocumentChunk(BaseModel):
    """Model for a document chunk."""

    content: str = Field(..., description="Chunk content")

    metadata: Dict[str, Any] = Field(default_factory=dict, description="Chunk metadata")

    chunk_index: int = Field(..., description="Index of this chunk in the document")

    chunk_id: Optional[str] = Field(
        default=None, description="Unique identifier for this chunk"
    )

    start_char: Optional[int] = Field(
        default=None, description="Start character position in original document"
    )

    end_char: Optional[int] = Field(
        default=None, description="End character position in original document"
    )


class ProcessedDocument(BaseModel):
    """Model for a processed document with chunks."""

    # Original document info
    source: str = Field(..., description="Source of the document")
    source_type: DocumentSourceType = Field(..., description="Type of source")
    format: DocumentFormat = Field(..., description="Document format")

    # Content
    content: str = Field(..., description="Full document content")
    chunks: List[DocumentChunk] = Field(
        default_factory=list, description="Document chunks"
    )

    # Metadata
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Document metadata"
    )

    # Processing info
    loader_name: str = Field(..., description="Loader used")
    processing_time: float = Field(..., description="Processing time in seconds")
    chunk_count: int = Field(default=0, description="Number of chunks")

    # Statistics
    character_count: int = Field(default=0, description="Total character count")
    word_count: int = Field(default=0, description="Estimated word count")

    @model_validator(mode="after")
    def update_statistics(self) -> "ProcessedDocument":
        """Update statistics based on content and chunks."""
        self.chunk_count = len(self.chunks)
        self.character_count = len(self.content)
        self.word_count = len(self.content.split()) if self.content else 0
        return self


class DocumentOutput(BaseModel):
    """Output model for document operations."""

    # Processed documents
    documents: List[ProcessedDocument] = Field(
        default_factory=list, description="Processed documents"
    )

    # Operation metadata
    total_documents: int = Field(0, description="Total documents processed")
    successful_documents: int = Field(0, description="Successfully processed documents")
    failed_documents: int = Field(0, description="Failed document count")

    # Timing
    operation_time: float = Field(0.0, description="Total operation time in seconds")
    average_processing_time: float = Field(
        0.0, description="Average processing time per document"
    )

    # Source info
    original_source: str = Field(..., description="Original source")
    source_type: DocumentSourceType = Field(..., description="Source type used")

    # Processing info
    loader_names: List[str] = Field(default_factory=list, description="Loaders used")

    processing_strategy: ProcessingStrategy = Field(
        ..., description="Processing strategy used"
    )

    # Errors and warnings
    errors: List[Dict[str, Any]] = Field(
        default_factory=list, description="Errors encountered"
    )

    warnings: List[Dict[str, Any]] = Field(
        default_factory=list, description="Warnings generated"
    )

    has_errors: bool = Field(False, description="Whether errors occurred")
    has_warnings: bool = Field(False, description="Whether warnings occurred")

    # Statistics
    total_chunks: int = Field(0, description="Total chunks across all documents")
    total_characters: int = Field(0, description="Total characters processed")
    total_words: int = Field(0, description="Total estimated words")

    @model_validator(mode="after")
    def update_statistics(self) -> "DocumentOutput":
        """Update statistics based on processed documents."""
        self.total_documents = len(self.documents)
        self.successful_documents = len([d for d in self.documents if d.content])
        self.failed_documents = self.total_documents - self.successful_documents

        if self.documents:
            self.average_processing_time = sum(
                d.processing_time for d in self.documents
            ) / len(self.documents)
            self.total_chunks = sum(d.chunk_count for d in self.documents)
            self.total_characters = sum(d.character_count for d in self.documents)
            self.total_words = sum(d.word_count for d in self.documents)

        self.has_errors = len(self.errors) > 0
        self.has_warnings = len(self.warnings) > 0

        return self


# Export all models
__all__ = [
    "DocumentEngineConfig",
    "DocumentInput",
    "DocumentOutput",
    "ProcessedDocument",
    "DocumentChunk",
    "LoaderPreference",
    "ProcessingStrategy",
    "ChunkingStrategy",
    "DocumentFormat",
    "DocumentSourceType",
]
