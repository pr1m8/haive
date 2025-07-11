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
from pydantic import BaseModel, Field

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
    """Defines the input state for document loading and processing.

    This schema supports various source types and configurations, providing a flexible
    interface for document ingestion workflows.

    Attributes:
        source (Optional[Union[str, Path, Dict[str, Any]]]): The primary source
            to process, which can be a file path, URL, or a configuration dictionary.
        sources (Optional[List[Union[str, Path, Dict[str, Any]]]]): A list of
            sources for bulk processing.
        source_type (Optional[DocumentSourceType]): The explicit type of the source
            (e.g., FILE, URL). If not provided, it will be auto-detected.
        loader_name (Optional[str]): The specific loader to use for processing.
            If not provided, a loader will be auto-selected.
        loader_preference (LoaderPreference): The preference for auto-selecting a
            loader, balancing speed and quality. Defaults to BALANCED.
        processing_strategy (ProcessingStrategy): The strategy for document
            processing. Defaults to ENHANCED.
        chunking_strategy (ChunkingStrategy): The strategy for chunking documents.
            Defaults to RECURSIVE.
        chunk_size (int): The size of chunks in characters. Defaults to 1000.
        chunk_overlap (int): The overlap between chunks in characters. Defaults to 200.
        recursive (bool): Whether to recursively process directories. Defaults to True.
        max_documents (Optional[int]): The maximum number of documents to load.
        use_async (bool): Whether to use asynchronous loading when available.
            Defaults to False.
        parallel_processing (bool): Whether to enable parallel processing for
            supported operations. Defaults to True.
        max_workers (int): The maximum number of worker threads for parallel
            processing. Defaults to 4.
        include_patterns (List[str]): Glob patterns for files to include.
        exclude_patterns (List[str]): Glob patterns for files to exclude.
        loader_options (Dict[str, Any]): Additional options specific to the loader.
        processing_options (Dict[str, Any]): Additional options for processing.
        enable_caching (bool): Whether to enable document caching. Defaults to False.
        cache_ttl (int): The time-to-live for the cache in seconds. Defaults to 3600.

    Examples:
        Loading a single PDF file with default settings:

        .. code-block:: python

            from haive.core.engine.document.config import DocumentSourceType
            from haive.core.schema.prebuilt.document_state import DocumentEngineInputSchema

            state = DocumentEngineInputSchema(
                source="/path/to/document.pdf",
                source_type=DocumentSourceType.FILE
            )

        Scraping a website with custom loader and processing options:

        .. code-block:: python

            state = DocumentEngineInputSchema(
                source="https://example.com",
                source_type=DocumentSourceType.URL,
                loader_options={"verify_ssl": True},
                processing_options={"extract_links": True}
            )

        Configuring a bulk loading operation with a preference for quality:

        .. code-block:: python

            from haive.core.engine.document.config import LoaderPreference, ChunkingStrategy

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
    """Defines the output state from document loading and processing.

    This schema contains the loaded documents, metadata, and processing statistics,
    providing a comprehensive overview of the operation's results.

    Attributes:
        documents (List[ProcessedDocument]): A list of processed documents.
        raw_documents (List[Document]): A list of raw LangChain Document objects.
        total_documents (int): The total number of documents processed.
        successful_documents (int): The number of documents successfully processed.
        failed_documents (int): The number of documents that failed to process.
        operation_time (float): The total time for the operation in seconds.
        average_processing_time (float): The average processing time per document.
        original_source (Optional[str]): The original source path or URL.
        source_type (Optional[DocumentSourceType]): The detected or specified source type.
        loader_names (List[str]): The names of the loaders used.
        processing_strategy (Optional[ProcessingStrategy]): The processing strategy used.
        chunking_strategy (Optional[ChunkingStrategy]): The chunking strategy used.
        total_chunks (int): The total number of chunks created.
        total_characters (int): The total character count across all documents.
        total_words (int): The estimated total word count.
        errors (List[Dict[str, Any]]): A list of errors encountered during processing.
        warnings (List[Dict[str, Any]]): A list of warnings generated.
        metadata (Dict[str, Any]): Additional metadata about the operation.

    Examples:
        Inspecting the output of a successful loading operation:

        .. code-block:: python

            # Assuming 'output' is an instance of DocumentEngineOutputSchema
            if output.successful_documents > 0:
                print(f"Successfully loaded {output.successful_documents} documents.")
                print(f"Total chunks created: {output.total_chunks}")
                print(f"First document content: {output.documents[0].content[:100]}")

        Handling partial success with errors:

        .. code-block:: python

            if output.failed_documents > 0:
                print(f"Failed to load {output.failed_documents} documents.")
                for error in output.errors:
                    print(f"Source: {error['source']}, Error: {error['error']}")
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
        """Adds a processed document to the output state.

        This method appends a processed document to the output state and updates
        various statistics, such as total documents, successful documents, and
        chunk/character/word counts.

        Args:
            document (ProcessedDocument): The processed document to add.
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
        """Adds an error record to the output state.

        This method is used to log errors encountered during document processing,
        providing a structured way to track failures.

        Args:
            source (str): The source that caused the error (e.g., file path or URL).
            error (str): A description of the error.
            details (Optional[Dict[str, Any]]): Additional details about the error.
        """
        error_entry = {
            "source": source,
            "error": error,
            "timestamp": None,  # This would be set by the processing engine
        }
        if details:
            error_entry.update(details)

        self.errors.append(error_entry)
        self.failed_documents += 1
        self.total_documents += 1

    def calculate_statistics(self) -> None:
        """Calculates aggregate statistics from the loaded documents.

        This method updates the output state with summary statistics, such as
        average processing time and total counts for chunks, characters, and words.
        """
        if self.successful_documents > 0:
            self.average_processing_time = (
                self.operation_time / self.successful_documents
            )

        # Update totals from documents
        self.total_chunks = sum(doc.chunk_count for doc in self.documents)
        self.total_characters = sum(doc.character_count for doc in self.documents)
        self.total_words = sum(doc.word_count for doc in self.documents)


class DocumentWorkflowSchema(BaseModel):
    """Manages the state of a document processing workflow.

    This schema tracks the progress and metadata of a multi-step document
    processing workflow.

    Attributes:
        processing_stage (str): The current stage of the processing workflow
            (e.g., "initialized", "loading", "chunking", "completed").
        last_processed_index (int): The index of the last document processed,
            useful for resuming workflows.
        workflow_metadata (Dict[str, Any]): A dictionary for storing any
            additional metadata related to the workflow.
    """

    processing_stage: str = Field(
        default="initialized", description="Current processing stage"
    )

    last_processed_index: int = Field(
        default=0, description="Index of last processed document"
    )

    workflow_metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Workflow-specific metadata"
    )


class DocumentState(DocumentEngineInputSchema, DocumentEngineOutputSchema):
    """Represents the complete state of a document processing workflow.

    This schema combines the input, output, and workflow states to provide a
    full picture of a document processing operation. It inherits all attributes
    from `DocumentEngineInputSchema` and `DocumentEngineOutputSchema`.

    Attributes:
        workflow (DocumentWorkflowSchema): The state of the processing workflow.

    Examples:
        Initializing a complete workflow state and executing a step:

        .. code-block:: python

            from haive.core.engine.document.config import DocumentSourceType
            from haive.core.schema.prebuilt.document_state import DocumentState, DocumentWorkflowSchema

            # Initial state for processing a directory
            state = DocumentState(
                source="/path/to/documents/",
                source_type=DocumentSourceType.DIRECTORY,
                recursive=True,
                workflow=DocumentWorkflowSchema(processing_stage="loading")
            )

            # After processing, the state might look like this:
            # state.total_documents = 50
            # state.successful_documents = 48
            # state.workflow.processing_stage = "completed"
    """

    workflow: DocumentWorkflowSchema = Field(default_factory=DocumentWorkflowSchema)

    class Config:
        """Pydantic configuration for the DocumentState schema.

        Attributes:
            arbitrary_types_allowed (bool): Allows Pydantic to handle arbitrary types,
                which is useful for complex data structures like `langchain_core.documents.Document`.
        """

        arbitrary_types_allowed = True
