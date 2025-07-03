#!/usr/bin/env python
"""Simplified example of the Document Agent system.

This script demonstrates the core functionality of the DocumentState and DocumentAgent
classes without relying on the full Haive framework.
"""

import datetime
from enum import Enum
import os
import tempfile
from typing import Any
import uuid


# ====== Mock classes to replace dependencies =======


class StateGraph:
    """Mock StateGraph for demonstration purposes."""

    def __init__(self, state_cls):
        self.state_cls = state_cls
        self.nodes = {}
        self.edges = {}
        self.entry_point = None

    def add_node(self, name, func):
        self.nodes[name] = func

    def add_edge(self, source, target):
        if source not in self.edges:
            self.edges[source] = []
        self.edges[source].append(target)

    def set_entry_point(self, node):
        self.entry_point = node

    def compile(self):
        return self

    def invoke(self, state):
        """Simulate workflow execution."""
        current_node = self.entry_point
        while current_node != "END":
            state = self.nodes[current_node](state)
            current_node = self.edges[current_node][0]
        return state


# ====== Document State Schema =======


class DocumentSourceType(str, Enum):
    """Enum of document source types."""

    FILE = "file"
    DIRECTORY = "directory"
    URL = "url"
    DATABASE = "database"
    API = "api"
    TEXT = "text"
    UNKNOWN = "unknown"


class DocumentFormat(str, Enum):
    """Enum of document format types."""

    PDF = "pdf"
    DOCX = "docx"
    TXT = "txt"
    HTML = "html"
    MARKDOWN = "markdown"
    CSV = "csv"
    JSON = "json"
    XML = "xml"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    UNKNOWN = "unknown"


class ProcessingStage(str, Enum):
    """Enum of document processing stages."""

    INITIALIZED = "initialized"
    QUEUED = "queued"
    ANALYZING = "analyzing"
    LOADING = "loading"
    CHUNKING = "chunking"
    EMBEDDING = "embedding"
    COMPLETED = "completed"
    FAILED = "failed"


class LoadingStrategy(str, Enum):
    """Enum of document loading strategies."""

    AUTO = "auto"
    DIRECT = "direct"
    RECURSIVE = "recursive"
    PARALLEL = "parallel"
    SEQUENTIAL = "sequential"
    LAZY = "lazy"


class ChunkingStrategy(str, Enum):
    """Enum of document chunking strategies."""

    NONE = "none"
    FIXED_SIZE = "fixed_size"
    SEMANTIC = "semantic"
    RECURSIVE = "recursive"
    PARAGRAPH = "paragraph"
    SENTENCE = "sentence"
    CUSTOM = "custom"


class PathAnalysisResult:
    """Result of path analysis."""

    def __init__(
        self,
        source_type: DocumentSourceType = DocumentSourceType.UNKNOWN,
        document_format: DocumentFormat = DocumentFormat.UNKNOWN,
        metadata: dict[str, Any] | None = None,
    ):
        self.source_type = source_type
        self.document_format = document_format
        self.metadata = metadata or {}


class MockDocument:
    """Mock document for the example."""

    def __init__(self, page_content: str, metadata: dict[str, Any]):
        self.page_content = page_content
        self.metadata = metadata


class MockLoader:
    """Mock document loader for the example."""

    def __init__(self, content: str = "Example content"):
        self.content = content

    def load(self) -> list[MockDocument]:
        """Return a mock document."""
        return [
            MockDocument(page_content=self.content, metadata={"source": "mock_source"})
        ]


# ====== Helper functions to replace dependencies =======


def analyze_path(path: str) -> PathAnalysisResult:
    """Analyze path to determine source type and format."""
    result = PathAnalysisResult()

    # Determine source type
    if path.startswith(("http://", "https://")):
        result.source_type = DocumentSourceType.URL
        result.document_format = DocumentFormat.HTML
        result.metadata = {"title": "Example Web Page"}
    elif path.startswith("text://"):
        result.source_type = DocumentSourceType.TEXT
        result.document_format = DocumentFormat.TXT
        result.metadata = {"content_length": len(path) - 7}  # Remove "text://" prefix
    elif path.lower().endswith(".txt"):
        result.source_type = DocumentSourceType.FILE
        result.document_format = DocumentFormat.TXT
        result.metadata = {"size_bytes": 1024}  # Mock file size
    elif path.lower().endswith(".pdf"):
        result.source_type = DocumentSourceType.FILE
        result.document_format = DocumentFormat.PDF
        result.metadata = {"size_bytes": 2048}  # Mock file size
    elif path.lower().endswith(".md"):
        result.source_type = DocumentSourceType.FILE
        result.document_format = DocumentFormat.MARKDOWN
        result.metadata = {"size_bytes": 512}  # Mock file size
    elif os.path.isdir(path):
        result.source_type = DocumentSourceType.DIRECTORY
        result.metadata = {"file_count": 10}  # Mock file count

    return result


def get_loader_for_source(
    path: str, source_type: DocumentSourceType
) -> MockLoader | None:
    """Get a loader for the given source."""
    if source_type == DocumentSourceType.TEXT:
        # For text sources, extract the content
        if path.startswith("text://"):
            content = path[7:]  # Remove "text://" prefix
        else:
            content = "Example text content"
        return MockLoader(content=content)
    if source_type == DocumentSourceType.FILE:
        return MockLoader(content="Example file content")
    if source_type == DocumentSourceType.URL:
        return MockLoader(content="Example web content")
    return None


# ====== Simplified Document State =======


class LoadingOptions:
    """Options for document loading."""

    def __init__(
        self,
        strategy: LoadingStrategy = LoadingStrategy.AUTO,
        max_size_bytes: int | None = None,
        recursive_depth: int = 3,
        exclude_patterns: list[str] = None,
        include_patterns: list[str] = None,
        max_files: int | None = None,
        force_reload: bool = False,
        timeout_seconds: int = 60,
    ):
        self.strategy = strategy
        self.max_size_bytes = max_size_bytes
        self.recursive_depth = recursive_depth
        self.exclude_patterns = exclude_patterns or []
        self.include_patterns = include_patterns or []
        self.max_files = max_files
        self.force_reload = force_reload
        self.timeout_seconds = timeout_seconds


class ChunkingOptions:
    """Options for document chunking."""

    def __init__(
        self,
        strategy: ChunkingStrategy = ChunkingStrategy.FIXED_SIZE,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        keep_separator: bool = True,
        custom_separators: list[str] = None,
        metadata_scope: str = "all",
    ):
        self.strategy = strategy
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.keep_separator = keep_separator
        self.custom_separators = custom_separators or []
        self.metadata_scope = metadata_scope


class DocumentSourceMetadata:
    """Metadata for document sources."""

    def __init__(
        self,
        created_at: datetime.datetime = None,
        updated_at: datetime.datetime = None,
        size_bytes: int | None = None,
        mime_type: str | None = None,
        encoding: str | None = None,
        author: str | None = None,
        title: str | None = None,
        description: str | None = None,
        tags: list[str] = None,
        custom: dict[str, Any] = None,
    ):
        self.created_at = created_at or datetime.datetime.now()
        self.updated_at = updated_at or datetime.datetime.now()
        self.size_bytes = size_bytes
        self.mime_type = mime_type
        self.encoding = encoding
        self.author = author
        self.title = title
        self.description = description
        self.tags = tags or []
        self.custom = custom or {}

    def update(self, **kwargs: Any) -> None:
        """Update metadata fields."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.datetime.now()


class ProcessingStatistics:
    """Statistics about document processing."""

    def __init__(
        self,
        start_time: datetime.datetime = None,
        end_time: datetime.datetime | None = None,
        total_sources: int = 0,
        processed_sources: int = 0,
        failed_sources: int = 0,
        total_documents: int = 0,
        total_chunks: int = 0,
        total_tokens: int = 0,
    ):
        self.start_time = start_time or datetime.datetime.now()
        self.end_time = end_time
        self.total_sources = total_sources
        self.processed_sources = processed_sources
        self.failed_sources = failed_sources
        self.total_documents = total_documents
        self.total_chunks = total_chunks
        self.total_tokens = total_tokens

    @property
    def processing_time_seconds(self) -> float:
        """Calculate the total processing time in seconds."""
        if self.end_time is None:
            return (datetime.datetime.now() - self.start_time).total_seconds()
        return (self.end_time - self.start_time).total_seconds()

    @property
    def is_complete(self) -> bool:
        """Check if processing is complete."""
        return self.end_time is not None

    def complete(self) -> None:
        """Mark processing as complete."""
        self.end_time = datetime.datetime.now()


class DocumentSource:
    """A document source with path and configuration."""

    def __init__(
        self,
        path: str,
        source_type: DocumentSourceType = DocumentSourceType.UNKNOWN,
        format: DocumentFormat = DocumentFormat.UNKNOWN,
        credential_id: str | None = None,
        metadata: DocumentSourceMetadata | None = None,
        stage: ProcessingStage = ProcessingStage.INITIALIZED,
        loading_options: LoadingOptions | None = None,
        chunking_options: ChunkingOptions | None = None,
        error: str | None = None,
        last_processed: datetime.datetime | None = None,
    ):
        self.path = path
        self.source_type = source_type
        self.format = format
        self.credential_id = credential_id
        self.metadata = metadata or DocumentSourceMetadata()
        self.stage = stage
        self.loading_options = loading_options or LoadingOptions()
        self.chunking_options = chunking_options or ChunkingOptions()
        self.error = error
        self.last_processed = last_processed

    def update_stage(self, stage: ProcessingStage, error: str | None = None) -> None:
        """Update the processing stage of this source."""
        self.stage = stage
        if stage == ProcessingStage.FAILED and error:
            self.error = error
        if stage == ProcessingStage.COMPLETED:
            self.last_processed = datetime.datetime.now()


class DocumentChunk:
    """A chunk of a document."""

    def __init__(
        self,
        content: str,
        document_id: str,
        chunk_index: int,
        metadata: dict[str, Any] = None,
        embedding: list[float] | None = None,
    ):
        self.content = content
        self.document_id = document_id
        self.chunk_index = chunk_index
        self.metadata = metadata or {}
        self.embedding = embedding


class Document:
    """A document loaded from a source."""

    def __init__(
        self,
        document_id: str,
        content: str,
        source_path: str,
        source_type: DocumentSourceType = DocumentSourceType.UNKNOWN,
        format: DocumentFormat = DocumentFormat.UNKNOWN,
        metadata: dict[str, Any] = None,
        chunks: list[DocumentChunk] = None,
        embedding: list[float] | None = None,
        created_at: datetime.datetime = None,
        updated_at: datetime.datetime = None,
    ):
        self.document_id = document_id
        self.content = content
        self.source_path = source_path
        self.source_type = source_type
        self.format = format
        self.metadata = metadata or {}
        self.chunks = chunks or []
        self.embedding = embedding
        self.created_at = created_at or datetime.datetime.now()
        self.updated_at = updated_at or datetime.datetime.now()

    def add_chunk(
        self, content: str, metadata: dict[str, Any] | None = None
    ) -> DocumentChunk:
        """Add a chunk to this document."""
        if metadata is None:
            metadata = {}

        chunk = DocumentChunk(
            content=content,
            document_id=self.document_id,
            chunk_index=len(self.chunks),
            metadata=metadata,
        )
        self.chunks.append(chunk)
        self.updated_at = datetime.datetime.now()
        return chunk

    @property
    def chunk_count(self) -> int:
        """Get the number of chunks in this document."""
        return len(self.chunks)


class DocumentState:
    """State schema for document operations."""

    def __init__(
        self,
        sources: list[DocumentSource] = None,
        documents: list[Document] = None,
        credentials: dict[str, Any] = None,
        loading_options: LoadingOptions | None = None,
        chunking_options: ChunkingOptions | None = None,
        processing_stats: ProcessingStatistics | None = None,
        current_query: str | None = None,
        messages: list[dict[str, Any]] = None,
        parallel_processing: bool = True,
        max_workers: int = 4,
        error_messages: list[str] = None,
    ):
        self.sources = sources or []
        self.documents = documents or []
        self.credentials = credentials or {}
        self.loading_options = loading_options or LoadingOptions()
        self.chunking_options = chunking_options or ChunkingOptions()
        self.processing_stats = processing_stats or ProcessingStatistics()
        self.current_query = current_query
        self.messages = messages or []
        self.parallel_processing = parallel_processing
        self.max_workers = max_workers
        self.error_messages = error_messages or []

    def add_source(self, path: str, **kwargs: Any) -> DocumentSource:
        """Add a document source to be processed."""
        source = DocumentSource(path=path, **kwargs)
        self.sources.append(source)
        self.processing_stats.total_sources += 1
        return source

    def add_sources(self, paths: list[str]) -> list[DocumentSource]:
        """Add multiple document sources to be processed."""
        sources = []
        for path in paths:
            source = self.add_source(path)
            sources.append(source)
        return sources

    def add_document(
        self, document_id: str, content: str, source_path: str, **kwargs: Any
    ) -> Document:
        """Add a document to the state."""
        document = Document(
            document_id=document_id, content=content, source_path=source_path, **kwargs
        )
        self.documents.append(document)
        self.processing_stats.total_documents += 1
        return document

    def update_source_stage(
        self, path: str, stage: ProcessingStage, error: str | None = None
    ) -> None:
        """Update the processing stage of a source."""
        for source in self.sources:
            if source.path == path:
                source.update_stage(stage, error)
                if stage == ProcessingStage.COMPLETED:
                    self.processing_stats.processed_sources += 1
                elif stage == ProcessingStage.FAILED:
                    self.processing_stats.failed_sources += 1
                    if error:
                        self.error_messages.append(f"Error processing {path}: {error}")
                return

    def get_document(self, document_id: str) -> Document | None:
        """Get a document by ID."""
        for doc in self.documents:
            if doc.document_id == document_id:
                return doc
        return None

    def get_documents_by_source(self, source_path: str) -> list[Document]:
        """Get all documents from a specific source."""
        return [doc for doc in self.documents if doc.source_path == source_path]

    def get_documents_by_format(
        self, format: DocumentFormat | str
    ) -> list[Document]:
        """Get all documents of a specific format."""
        if isinstance(format, str):
            format = DocumentFormat(format)
        return [doc for doc in self.documents if doc.format == format]

    def get_sources_by_stage(self, stage: ProcessingStage) -> list[DocumentSource]:
        """Get all sources in a specific processing stage."""
        return [source for source in self.sources if source.stage == stage]

    def get_unprocessed_sources(self) -> list[DocumentSource]:
        """Get all unprocessed sources."""
        return [
            source
            for source in self.sources
            if source.stage
            in [
                ProcessingStage.INITIALIZED,
                ProcessingStage.QUEUED,
                ProcessingStage.ANALYZING,
            ]
        ]

    def get_all_chunks(self) -> list[DocumentChunk]:
        """Get all document chunks across all documents."""
        chunks = []
        for doc in self.documents:
            chunks.extend(doc.chunks)
        return chunks

    def mark_processing_complete(self) -> None:
        """Mark document processing as complete."""
        self.processing_stats.complete()

    @property
    def all_sources_processed(self) -> bool:
        """Check if all sources have been processed."""
        for source in self.sources:
            if source.stage not in [ProcessingStage.COMPLETED, ProcessingStage.FAILED]:
                return False
        return True

    @property
    def has_errors(self) -> bool:
        """Check if there are any errors."""
        return len(self.error_messages) > 0 or any(
            source.stage == ProcessingStage.FAILED for source in self.sources
        )

    @property
    def has_documents(self) -> bool:
        """Check if there are any documents."""
        return len(self.documents) > 0

    @property
    def total_chunks(self) -> int:
        """Get the total number of chunks."""
        return sum(doc.chunk_count for doc in self.documents)

    @property
    def source_types(self) -> set[DocumentSourceType]:
        """Get the set of all source types in this state."""
        return {source.source_type for source in self.sources}

    @property
    def document_formats(self) -> set[DocumentFormat]:
        """Get the set of all document formats in this state."""
        return {doc.format for doc in self.documents}


# ====== Document Agent Options =======


class DocumentAgentOptions:
    """Options for document agent configuration."""

    def __init__(
        self,
        default_loading_options: LoadingOptions | None = None,
        default_chunking_options: ChunkingOptions | None = None,
        parallel_processing: bool = True,
        max_workers: int = 4,
        source_timeout_seconds: int = 30,
        loading_timeout_seconds: int = 120,
        chunking_timeout_seconds: int = 60,
        max_documents: int | None = None,
        max_document_size_bytes: int | None = None,
        skip_errors: bool = True,
    ):
        self.default_loading_options = default_loading_options or LoadingOptions()
        self.default_chunking_options = default_chunking_options or ChunkingOptions()
        self.parallel_processing = parallel_processing
        self.max_workers = max_workers
        self.source_timeout_seconds = source_timeout_seconds
        self.loading_timeout_seconds = loading_timeout_seconds
        self.chunking_timeout_seconds = chunking_timeout_seconds
        self.max_documents = max_documents
        self.max_document_size_bytes = max_document_size_bytes
        self.skip_errors = skip_errors


# ====== Document Agent Implementation =======


class DocumentAgent:
    """Agent for loading and processing documents from various sources."""

    def __init__(
        self,
        state: DocumentState | None = None,
        options: DocumentAgentOptions | None = None,
        **kwargs: Any,
    ):
        """Initialize a DocumentAgent."""
        self.state = state or DocumentState()
        self.options = options or DocumentAgentOptions()

        # Initialize state with default options
        self.state.loading_options = self.options.default_loading_options
        self.state.chunking_options = self.options.default_chunking_options
        self.state.parallel_processing = self.options.parallel_processing
        self.state.max_workers = self.options.max_workers

    def add_source(self, path: str, **kwargs: Any) -> DocumentSource:
        """Add a document source to be processed."""
        return self.state.add_source(path, **kwargs)

    def add_sources(self, paths: list[str]) -> list[DocumentSource]:
        """Add multiple document sources to be processed."""
        return self.state.add_sources(paths)

    def get_documents(self) -> list[Document]:
        """Get all loaded documents."""
        return self.state.documents

    def get_document(self, document_id: str) -> Document | None:
        """Get a document by ID."""
        return self.state.get_document(document_id)

    def get_documents_by_source(self, source_path: str) -> list[Document]:
        """Get all documents from a specific source."""
        return self.state.get_documents_by_source(source_path)

    def get_documents_by_format(
        self, format: DocumentFormat | str
    ) -> list[Document]:
        """Get all documents of a specific format."""
        return self.state.get_documents_by_format(format)

    def get_all_chunks(self) -> list[DocumentChunk]:
        """Get all document chunks across all documents."""
        return self.state.get_all_chunks()

    def clear(self) -> None:
        """Clear the agent state."""
        self.state = DocumentState()
        self.state.loading_options = self.options.default_loading_options
        self.state.chunking_options = self.options.default_chunking_options
        self.state.parallel_processing = self.options.parallel_processing
        self.state.max_workers = self.options.max_workers

    def analyze_source(self, state: DocumentState) -> DocumentState:
        """Analyze document sources and prepare them for loading."""
        print("Analyzing sources...")

        for source in state.sources:
            if source.stage == ProcessingStage.INITIALIZED:
                try:
                    source.update_stage(ProcessingStage.ANALYZING)

                    # Use path analysis to determine source type and format
                    path_info = analyze_path(source.path)

                    # Update source with analysis results
                    if path_info.source_type != DocumentSourceType.UNKNOWN:
                        source.source_type = path_info.source_type

                    if path_info.document_format != DocumentFormat.UNKNOWN:
                        source.format = path_info.document_format

                    # Update metadata with analysis results
                    if path_info.metadata:
                        for key, value in path_info.metadata.items():
                            if hasattr(source.metadata, key):
                                setattr(source.metadata, key, value)
                            else:
                                source.metadata.custom[key] = value

                    # Update stage to QUEUED for loading
                    source.update_stage(ProcessingStage.QUEUED)
                    print(
                        f"  Source {source.path} analyzed as {source.source_type}, {source.format}"
                    )

                except Exception as e:
                    error_msg = f"Error analyzing source: {e!s}"
                    source.update_stage(ProcessingStage.FAILED, error_msg)
                    state.error_messages.append(error_msg)
                    print(f"  Error analyzing source {source.path}: {e!s}")
                    if not self.options.skip_errors:
                        raise

        return state

    def load_documents(self, state: DocumentState) -> DocumentState:
        """Load documents from sources."""
        print("Loading documents...")

        queued_sources = state.get_sources_by_stage(ProcessingStage.QUEUED)

        if not queued_sources:
            return state

        for source in queued_sources:
            try:
                source.update_stage(ProcessingStage.LOADING)
                print(f"  Loading {source.path}...")

                # Get loader for this source
                loader = get_loader_for_source(source.path, source.source_type)

                if loader is None:
                    error = f"No loader found for source: {source.path}"
                    source.update_stage(ProcessingStage.FAILED, error)
                    state.error_messages.append(error)
                    print(f"  Error: {error}")
                    continue

                # Load documents
                raw_docs = loader.load()

                # Convert to Document objects
                for i, raw_doc in enumerate(raw_docs):
                    doc_id = f"{uuid.uuid4()}"
                    content = raw_doc.page_content

                    # Create document
                    doc = Document(
                        document_id=doc_id,
                        content=content,
                        source_path=source.path,
                        source_type=source.source_type,
                        format=source.format,
                        metadata={**raw_doc.metadata, **source.metadata.custom},
                    )
                    state.documents.append(doc)
                    state.processing_stats.total_documents += 1
                    print(
                        f"    Created document {doc_id} with {len(content)} characters"
                    )

                # Update source stage
                if state.chunking_options.strategy == ChunkingStrategy.NONE:
                    source.update_stage(ProcessingStage.COMPLETED)
                else:
                    source.update_stage(ProcessingStage.CHUNKING)

            except Exception as e:
                error = f"Error loading source: {e!s}"
                source.update_stage(ProcessingStage.FAILED, error)
                state.error_messages.append(error)
                print(f"  Error loading {source.path}: {e!s}")
                if not self.options.skip_errors:
                    raise

        return state

    def chunk_documents(self, state: DocumentState) -> DocumentState:
        """Chunk documents into smaller pieces."""
        print("Chunking documents...")

        # Use the local _simple_split_document function instead of the external processor
        # to avoid import errors with haive.core dependencies

        chunking_sources = state.get_sources_by_stage(ProcessingStage.CHUNKING)

        if (
            not chunking_sources
            or state.chunking_options.strategy == ChunkingStrategy.NONE
        ):
            return state

        for source in chunking_sources:
            try:
                # Get documents for this source
                docs = state.get_documents_by_source(source.path)
                print(f"  Chunking {len(docs)} documents from {source.path}")

                for doc in docs:
                    # Skip already chunked documents
                    if doc.chunks:
                        continue

                    # Get chunking strategy
                    chunking_options = source.chunking_options or state.chunking_options

                    # Use the basic chunking methods directly, since we can't import
                    # the external processors due to haive.core dependencies
                    if chunking_options.strategy == ChunkingStrategy.FIXED_SIZE:
                        self._chunk_fixed_size(doc, chunking_options)
                    elif chunking_options.strategy == ChunkingStrategy.PARAGRAPH:
                        self._chunk_paragraphs(doc, chunking_options)
                    elif chunking_options.strategy == ChunkingStrategy.SENTENCE:
                        self._chunk_sentences(doc, chunking_options)
                    else:
                        # Default to fixed size if strategy not implemented
                        self._chunk_fixed_size(doc, chunking_options)

                    print(
                        f"    Created {doc.chunk_count} chunks for document {doc.document_id}"
                    )

                # Update source stage
                source.update_stage(ProcessingStage.COMPLETED)

            except Exception as e:
                error_msg = f"Error chunking documents: {e!s}"
                source.update_stage(ProcessingStage.FAILED, error_msg)
                state.error_messages.append(error_msg)
                print(f"  Error chunking documents from {source.path}: {e!s}")
                if not self.options.skip_errors:
                    raise

        return state

    def _chunk_fixed_size(self, doc: Document, options: ChunkingOptions) -> None:
        """Chunk a document into fixed-size chunks."""
        content = doc.content
        chunk_size = options.chunk_size
        chunk_overlap = options.chunk_overlap

        # Simple chunking implementation
        start = 0
        chunk_index = 0

        while start < len(content):
            # Calculate end position with overlap
            end = min(start + chunk_size, len(content))

            # Extract chunk content
            chunk_content = content[start:end]

            # Create chunk metadata
            chunk_metadata = {
                "chunk_index": chunk_index,
                "start": start,
                "end": end,
                "document_id": doc.document_id,
                "source_path": doc.source_path,
            }

            # Add metadata from document if scope includes document
            if options.metadata_scope in ["all", "document"]:
                for key, value in doc.metadata.items():
                    if key not in chunk_metadata:
                        chunk_metadata[key] = value

            # Add chunk to document
            doc.add_chunk(chunk_content, chunk_metadata)

            # Move to next chunk position, accounting for overlap
            start = end - chunk_overlap if end < len(content) else len(content)
            chunk_index += 1

    def _chunk_paragraphs(self, doc: Document, options: ChunkingOptions) -> None:
        """Chunk a document by paragraphs."""
        content = doc.content

        # Split by double newlines (paragraph breaks)
        paragraphs = content.split("\n\n")

        for i, paragraph in enumerate(paragraphs):
            paragraph = paragraph.strip()
            if not paragraph:
                continue

            # Create chunk metadata
            chunk_metadata = {
                "chunk_index": i,
                "paragraph_index": i,
                "document_id": doc.document_id,
                "source_path": doc.source_path,
            }

            # Add metadata from document if scope includes document
            if options.metadata_scope in ["all", "document"]:
                for key, value in doc.metadata.items():
                    if key not in chunk_metadata:
                        chunk_metadata[key] = value

            # Add chunk to document
            doc.add_chunk(paragraph, chunk_metadata)

    def _chunk_sentences(self, doc: Document, options: ChunkingOptions) -> None:
        """Chunk a document by sentences."""
        content = doc.content

        # Simple sentence splitting by ., !, ?
        # This is a simplified approach; a more robust approach would use NLP
        sentence_endings = [". ", "! ", "? ", ".\n", "!\n", "?\n"]
        current_sentence = ""
        sentences = []

        for char in content:
            current_sentence += char
            for ending in sentence_endings:
                if current_sentence.endswith(ending):
                    sentences.append(current_sentence.strip())
                    current_sentence = ""
                    break

        if current_sentence.strip():
            sentences.append(current_sentence.strip())

        for i, sentence in enumerate(sentences):
            if not sentence:
                continue

            # Create chunk metadata
            chunk_metadata = {
                "chunk_index": i,
                "sentence_index": i,
                "document_id": doc.document_id,
                "source_path": doc.source_path,
            }

            # Add metadata from document if scope includes document
            if options.metadata_scope in ["all", "document"]:
                for key, value in doc.metadata.items():
                    if key not in chunk_metadata:
                        chunk_metadata[key] = value

            # Add chunk to document
            doc.add_chunk(sentence, chunk_metadata)

    def finalize_processing(self, state: DocumentState) -> DocumentState:
        """Finalize document processing."""
        print("Finalizing document processing...")

        # Update statistics
        state.processing_stats.total_chunks = state.total_chunks

        # Estimate total tokens (very rough approximation)
        total_tokens = 0
        for doc in state.documents:
            # Estimate 4 characters per token on average
            doc_tokens = len(doc.content) // 4
            total_tokens += doc_tokens

        state.processing_stats.total_tokens = total_tokens

        # Mark processing as complete
        state.mark_processing_complete()

        print(
            f"Processing complete: {state.processing_stats.total_documents} documents, "
            f"{state.processing_stats.total_chunks} chunks, "
            f"{state.processing_stats.total_tokens} tokens (estimated)"
        )

        return state

    def build_graph(self) -> StateGraph:
        """Build the document agent graph."""
        print("Building document processing graph...")

        builder = StateGraph(DocumentState)

        # Add nodes
        builder.add_node("analyze_source", self.analyze_source)
        builder.add_node("load_documents", self.load_documents)
        builder.add_node("chunk_documents", self.chunk_documents)
        builder.add_node("finalize_processing", self.finalize_processing)

        # Define edges
        builder.add_edge("analyze_source", "load_documents")
        builder.add_edge("load_documents", "chunk_documents")
        builder.add_edge("chunk_documents", "finalize_processing")
        builder.add_edge("finalize_processing", "END")

        # Set entry point
        builder.set_entry_point("analyze_source")

        return builder.compile()

    def process_documents(self) -> None:
        """Process all documents in the agent's state."""
        graph = self.build_graph()
        self.state = graph.invoke(self.state)


# ====== Factory Functions =======


def create_document_agent(
    options: DocumentAgentOptions | None = None,
    sources: list[str] | None = None,
    **kwargs: Any,
) -> DocumentAgent:
    """Create a general-purpose document agent."""
    agent = DocumentAgent(options=options, **kwargs)

    if sources:
        agent.add_sources(sources)

    return agent


def create_file_document_agent(
    file_paths: list[str],
    chunking_strategy: ChunkingStrategy = ChunkingStrategy.FIXED_SIZE,
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
    **kwargs: Any,
) -> DocumentAgent:
    """Create a document agent optimized for file loading."""
    options = DocumentAgentOptions(
        default_loading_options=LoadingOptions(
            strategy=LoadingStrategy.DIRECT,
            max_files=len(file_paths),
        ),
        default_chunking_options=ChunkingOptions(
            strategy=chunking_strategy,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        ),
    )

    agent = DocumentAgent(options=options, **kwargs)
    agent.add_sources(file_paths)

    return agent


def create_web_document_agent(
    urls: list[str],
    chunking_strategy: ChunkingStrategy = ChunkingStrategy.PARAGRAPH,
    **kwargs: Any,
) -> DocumentAgent:
    """Create a document agent optimized for web loading."""
    options = DocumentAgentOptions(
        default_loading_options=LoadingOptions(
            strategy=LoadingStrategy.DIRECT,
            timeout_seconds=120,
        ),
        default_chunking_options=ChunkingOptions(
            strategy=chunking_strategy,
        ),
    )

    agent = DocumentAgent(options=options, **kwargs)
    agent.add_sources(urls)

    return agent


# ====== Helper Functions =======


def create_sample_files() -> list[str]:
    """Create sample files for the example."""
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    file_paths = []

    # Create a text file
    text_file = os.path.join(temp_dir, "sample.txt")
    with open(text_file, "w") as f:
        f.write(
            """# Sample Text Document

This is a sample text document for testing the DocumentAgent.

## Section 1

This document has multiple sections and paragraphs.
Each paragraph can be processed as a separate chunk.

## Section 2

The DocumentAgent can load and process documents from various sources:
- Files
- URLs
- Text input
- Directories

## Section 3

Different chunking strategies can be used:
- Fixed size chunking
- Paragraph chunking
- Sentence chunking
"""
        )
    file_paths.append(text_file)

    # Create a markdown file
    md_file = os.path.join(temp_dir, "sample.md")
    with open(md_file, "w") as f:
        f.write(
            """# Sample Markdown Document

This is a sample markdown document for testing the DocumentAgent.

## Features

- Document loading from various sources
- Flexible chunking strategies
- Error handling and recovery
- Parallel processing of documents

## Benefits

1. Simplified document processing
2. Consistent interface for different source types
3. Integrated with Haive agent framework
"""
        )
    file_paths.append(md_file)

    return file_paths


# ====== Example Implementations =======


def example_basic_usage():
    """Example of basic DocumentAgent usage."""
    print("\n=== Example: Basic DocumentAgent Usage ===\n")

    # Create sample files
    file_paths = create_sample_files()

    # Create a document agent
    agent = DocumentAgent()

    # Add sources
    print("Adding sources...")
    agent.add_sources(file_paths)
    agent.add_source("text://This is a sample text source for testing.")

    # Process documents
    agent.process_documents()

    # Display results
    print("\nResults:")
    print(f"- Processed {len(agent.get_documents())} documents")
    for doc in agent.get_documents():
        print(
            f"  - {doc.source_path}: {len(doc.content)} chars, {doc.chunk_count} chunks"
        )

    # Display statistics
    stats = agent.state.processing_stats
    print("\nProcessing statistics:")
    print(f"- Total sources: {stats.total_sources}")
    print(f"- Total documents: {stats.total_documents}")
    print(f"- Total chunks: {stats.total_chunks}")
    print(f"- Processing time: {stats.processing_time_seconds:.2f} seconds")


def example_chunking_strategies():
    """Example of different chunking strategies."""
    print("\n=== Example: Different Chunking Strategies ===\n")

    # Create text content
    text_content = """This is a sample text for testing different chunking strategies.
It has multiple sentences. Each sentence can be a separate chunk.

This is a second paragraph.
It also has multiple sentences for testing.

And this is a third paragraph with more content.
The DocumentAgent supports different chunking strategies:
- Fixed size chunking
- Paragraph chunking
- Sentence chunking
"""

    # 1. Fixed size chunking
    print("1. Fixed Size Chunking")
    fixed_agent = DocumentAgent(
        options=DocumentAgentOptions(
            default_chunking_options=ChunkingOptions(
                strategy=ChunkingStrategy.FIXED_SIZE,
                chunk_size=50,
                chunk_overlap=10,
            )
        )
    )
    fixed_agent.add_source(f"text://{text_content}")
    fixed_agent.process_documents()

    # Display results
    doc = fixed_agent.get_documents()[0]
    print(f"Created {doc.chunk_count} fixed-size chunks:")
    for i, chunk in enumerate(doc.chunks[:3]):  # Show first 3 chunks
        print(f"  Chunk {i}: '{chunk.content[:30]}...'")
    if doc.chunk_count > 3:
        print(f"  (and {doc.chunk_count - 3} more chunks)")

    # 2. Paragraph chunking
    print("\n2. Paragraph Chunking")
    para_agent = DocumentAgent(
        options=DocumentAgentOptions(
            default_chunking_options=ChunkingOptions(
                strategy=ChunkingStrategy.PARAGRAPH,
            )
        )
    )
    para_agent.add_source(f"text://{text_content}")
    para_agent.process_documents()

    # Display results
    doc = para_agent.get_documents()[0]
    print(f"Created {doc.chunk_count} paragraph chunks:")
    for i, chunk in enumerate(doc.chunks):
        print(f"  Paragraph {i}: '{chunk.content[:30]}...'")

    # 3. Sentence chunking
    print("\n3. Sentence Chunking")
    sent_agent = DocumentAgent(
        options=DocumentAgentOptions(
            default_chunking_options=ChunkingOptions(
                strategy=ChunkingStrategy.SENTENCE,
            )
        )
    )
    sent_agent.add_source(f"text://{text_content}")
    sent_agent.process_documents()

    # Display results
    doc = sent_agent.get_documents()[0]
    print(f"Created {doc.chunk_count} sentence chunks:")
    for i, chunk in enumerate(doc.chunks[:5]):  # Show first 5 sentences
        print(f"  Sentence {i}: '{chunk.content}'")
    if doc.chunk_count > 5:
        print(f"  (and {doc.chunk_count - 5} more sentences)")


def example_specialized_agents():
    """Example of specialized document agents."""
    print("\n=== Example: Specialized Document Agents ===\n")

    # Create sample files
    file_paths = create_sample_files()

    # 1. File Document Agent
    print("1. File Document Agent")
    file_agent = create_file_document_agent(
        file_paths=file_paths,
        chunking_strategy=ChunkingStrategy.FIXED_SIZE,
        chunk_size=100,
        chunk_overlap=20,
    )
    file_agent.process_documents()

    print(
        f"Loaded {len(file_agent.get_documents())} documents with {file_agent.state.total_chunks} chunks"
    )

    # 2. Web Document Agent
    print("\n2. Web Document Agent")
    web_agent = create_web_document_agent(
        urls=["https://example.com", "https://haive.ai"],
        chunking_strategy=ChunkingStrategy.PARAGRAPH,
    )

    # Instead of actually processing, just show the configuration
    print(f"Created agent for {len(web_agent.state.sources)} URLs")
    print(f"Chunking strategy: {web_agent.state.chunking_options.strategy}")
    print(f"Loading timeout: {web_agent.state.loading_options.timeout_seconds} seconds")

    # 3. Text Document Agent
    print("\n3. Text Document Agent")
    text_agent = create_document_agent(
        options=DocumentAgentOptions(
            default_chunking_options=ChunkingOptions(
                strategy=ChunkingStrategy.SENTENCE,
            ),
        ),
        sources=[
            "text://This is a sample text source.",
            "text://This is another text source with multiple sentences. Each sentence will be a separate chunk.",
        ],
    )
    text_agent.process_documents()

    print(
        f"Loaded {len(text_agent.get_documents())} text documents with {text_agent.state.total_chunks} chunks"
    )


def main():
    """Run the example script."""
    print("==== Document Agent System Example ====")

    example_basic_usage()
    example_chunking_strategies()
    example_specialized_agents()

    print("\n==== Example Complete ====")


if __name__ == "__main__":
    main()
