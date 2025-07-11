from enum import Enum
from typing import Any

from langchain_core.documents import Document
from pydantic import BaseModel, Field


class DocumentLoadingStatus(str, Enum):
    """Status of document loading operation."""

    PENDING = "pending"
    LOADING = "loading"
    LOADED = "loaded"
    FAILED = "failed"
    PROCESSING = "processing"
    COMPLETED = "completed"


class LoadingStrategy(str, Enum):
    """Loading strategies for documents."""

    LOAD = "load"  # Standard load() method
    LOAD_AND_SPLIT = "load_and_split"  # Load and split into chunks
    LAZY_LOAD = "lazy_load"  # Lazy loading with iterator
    FETCH_ALL = "fetch_all"  # Fetch all tables/collections
    SCRAPE_ALL = "scrape_all"  # Comprehensive database scraping


class TextSplitterType(str, Enum):
    """Text splitter types for load_and_split."""

    RECURSIVE_CHARACTER = "recursive_character"
    CHARACTER = "character"
    TOKEN = "token"
    MARKDOWN = "markdown"
    PYTHON_CODE = "python_code"
    HTML = "html"
    CUSTOM = "custom"


class DocumentSourceInfo(BaseModel):
    """Information about the document source."""

    source_type: str = Field(description="Type of document source")
    source_path: str = Field(description="Path or URL to the source")
    source_id: str = Field(description="Unique identifier for the source")
    loader_used: str | None = Field(
        None, description="Loader used to process this source"
    )

    # Loading strategy information
    loading_strategy: LoadingStrategy = Field(
        LoadingStrategy.LOAD, description="Loading strategy used"
    )
    lazy_loaded: bool = Field(False, description="Whether lazy loading was used")

    # Text splitting information (for load_and_split)
    was_split: bool = Field(
        False, description="Whether documents were split into chunks"
    )
    text_splitter_type: TextSplitterType | None = Field(
        None, description="Text splitter type used"
    )
    chunk_size: int | None = Field(None, description="Chunk size used for splitting")
    chunk_overlap: int | None = Field(
        None, description="Chunk overlap used for splitting"
    )
    chunks_created: int = Field(
        0, description="Number of chunks created from this source"
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional source metadata"
    )


class DocumentEngineInputSchema(BaseModel):
    """Enhanced input schema for the document engine with source tracking."""

    # Primary input - can be documents OR source paths
    documents: list[Document] | None = Field(
        None, description="Pre-loaded documents to process"
    )
    source_paths: list[str] | None = Field(
        None, description="Paths/URLs to load documents from"
    )

    # Loading configuration
    loader_preference: str = Field(
        "balanced", description="Loader preference: speed, quality, balanced"
    )
    bulk_loading: bool = Field(
        False, description="Enable bulk loading for multiple sources"
    )
    max_concurrent: int = Field(4, description="Maximum concurrent loading operations")

    # Loading strategy and methods
    loading_strategy: LoadingStrategy = Field(
        LoadingStrategy.LOAD, description="Document loading strategy"
    )
    enable_lazy_loading: bool = Field(
        False, description="Enable lazy loading for large datasets"
    )

    # Text splitting configuration (unified for all sources)
    text_splitter_type: TextSplitterType = Field(
        TextSplitterType.RECURSIVE_CHARACTER, description="Text splitter type"
    )
    chunk_size: int = Field(1000, description="Chunk size for text splitting")
    chunk_overlap: int = Field(200, description="Overlap between chunks")
    custom_separators: list[str] | None = Field(
        None, description="Custom separators for text splitting"
    )

    # Legacy chunking support (deprecated, use loading_strategy instead)
    chunking_enabled: bool = Field(
        True, description="Enable document chunking (deprecated)"
    )

    # Filtering and selection
    file_extensions: list[str] | None = Field(
        None, description="Filter by file extensions"
    )
    max_files: int | None = Field(
        None, description="Maximum number of files to process"
    )

    # Metadata and tracking
    session_id: str | None = Field(None, description="Session identifier for tracking")
    user_id: str | None = Field(None, description="User identifier")
    tags: list[str] = Field(default_factory=list, description="Tags for organization")


class DocumentEngineOutputSchema(BaseModel):
    """Enhanced output schema for the document engine with comprehensive tracking."""

    # Processed documents
    documents: list[Document] = Field(description="The processed documents")

    # Loading results
    loading_status: DocumentLoadingStatus = Field(description="Overall loading status")
    sources_processed: list[DocumentSourceInfo] = Field(
        description="Information about processed sources"
    )

    # Statistics
    total_sources: int = Field(description="Total number of sources processed")
    successful_loads: int = Field(description="Number of successfully loaded sources")
    failed_loads: int = Field(description="Number of failed source loads")
    total_documents: int = Field(description="Total number of documents produced")
    total_chunks: int = Field(description="Total number of chunks if chunking enabled")

    # Performance metrics
    processing_time_seconds: float = Field(description="Total processing time")
    average_load_time: float = Field(description="Average time per source load")

    # Error information
    errors: list[dict[str, Any]] = Field(
        default_factory=list, description="Loading errors encountered"
    )
    warnings: list[str] = Field(
        default_factory=list, description="Warnings during processing"
    )

    # Metadata
    loader_usage: dict[str, int] = Field(
        default_factory=dict, description="Count of each loader type used"
    )
    source_types: dict[str, int] = Field(
        default_factory=dict, description="Count of each source type processed"
    )
    loading_strategies: dict[str, int] = Field(
        default_factory=dict, description="Count of each loading strategy used"
    )
    text_splitter_usage: dict[str, int] = Field(
        default_factory=dict, description="Count of each text splitter type used"
    )

    # Splitting statistics
    sources_split: int = Field(
        0, description="Number of sources that were split into chunks"
    )
    lazy_loaded_sources: int = Field(0, description="Number of sources loaded lazily")


class DocumentBatchLoadingSchema(BaseModel):
    """Schema for batch document loading operations."""

    batch_id: str = Field(description="Unique batch identifier")
    sources: list[str] = Field(description="List of source paths to process")
    batch_size: int = Field(10, description="Number of sources to process per batch")

    # Processing configuration
    loader_preference: str = Field("balanced", description="Loader preference")
    parallel_processing: bool = Field(True, description="Enable parallel processing")
    max_workers: int = Field(4, description="Maximum worker threads")

    # Progress tracking
    progress_callback: str | None = Field(
        None, description="Callback for progress updates"
    )
    save_intermediate: bool = Field(False, description="Save intermediate results")

    # Error handling
    continue_on_error: bool = Field(
        True, description="Continue processing if individual sources fail"
    )
    max_retries: int = Field(3, description="Maximum retry attempts per source")


class DocumentEngineStateSchema(BaseModel):
    """State schema for document engine with persistence support."""

    # Input configuration
    input_config: DocumentEngineInputSchema = Field(description="Input configuration")

    # Processing state
    current_status: DocumentLoadingStatus = Field(
        DocumentLoadingStatus.PENDING, description="Current processing status"
    )
    sources_queue: list[str] = Field(
        default_factory=list, description="Queue of sources to process"
    )
    sources_completed: list[str] = Field(
        default_factory=list, description="Completed sources"
    )
    sources_failed: list[str] = Field(
        default_factory=list, description="Failed sources"
    )

    # Results
    loaded_documents: list[Document] = Field(
        default_factory=list, description="All loaded documents"
    )
    source_mappings: dict[str, DocumentSourceInfo] = Field(
        default_factory=dict, description="Source to info mapping"
    )

    # Metrics
    start_time: float | None = Field(None, description="Processing start timestamp")
    end_time: float | None = Field(None, description="Processing end timestamp")
    error_log: list[dict[str, Any]] = Field(
        default_factory=list, description="Error log"
    )

    # Persistence info
    thread_id: str | None = Field(
        None, description="Conversation thread ID for persistence"
    )
    checkpoint_id: str | None = Field(
        None, description="Checkpoint ID for state recovery"
    )
