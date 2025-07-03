#!/usr/bin/env python
"""Runnable example of document processing with transformers and splitters.

This script demonstrates the document processing functionality in a self-contained
way that doesn't require the full Haive framework.
"""

import datetime
import logging
import os
import tempfile
import uuid
from enum import Enum
from typing import Any

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# ====== Document State Classes =======


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


class LoadingOptions:
    """Options for document loading."""

    def __init__(
        self,
        strategy: LoadingStrategy = LoadingStrategy.AUTO,
        max_size_bytes: int | None = None,
        recursive_depth: int = 3,
        exclude_patterns: list[str] | None = None,
        include_patterns: list[str] | None = None,
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
        custom_separators: list[str] | None = None,
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
        created_at: datetime.datetime | None = None,
        updated_at: datetime.datetime | None = None,
        size_bytes: int | None = None,
        mime_type: str | None = None,
        encoding: str | None = None,
        author: str | None = None,
        title: str | None = None,
        description: str | None = None,
        tags: list[str] | None = None,
        custom: dict[str, Any] | None = None,
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
        start_time: datetime.datetime | None = None,
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
        metadata: dict[str, Any] | None = None,
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
        metadata: dict[str, Any] | None = None,
        chunks: list[DocumentChunk] | None = None,
        embedding: list[float] | None = None,
        created_at: datetime.datetime | None = None,
        updated_at: datetime.datetime | None = None,
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
    """State for document operations."""

    def __init__(
        self,
        sources: list[DocumentSource] | None = None,
        documents: list[Document] | None = None,
        credentials: dict[str, Any] | None = None,
        loading_options: LoadingOptions | None = None,
        chunking_options: ChunkingOptions | None = None,
        processing_stats: ProcessingStatistics | None = None,
        current_query: str | None = None,
        messages: list[dict[str, Any]] | None = None,
        parallel_processing: bool = True,
        max_workers: int = 4,
        error_messages: list[str] | None = None,
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

    def get_documents_by_format(self, format: DocumentFormat | str) -> list[Document]:
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


# ====== Document Processor Functions =======


def transform_document(doc: Document) -> Document:
    """Apply a transformation to a document based on its format.

    In this simplified example, we just implement a basic HTML to text transformation.

    Args:
        doc: The document to transform.

    Returns:
        The transformed document.
    """
    if doc.format == DocumentFormat.HTML:
        logger.info(f"Transforming HTML document {doc.document_id}")
        # Very simple HTML to text transformation - in a real implementation,
        # we would use a proper HTML parser
        content = doc.content
        content = content.replace("<html>", "").replace("</html>", "")
        content = content.replace("<head>", "").replace("</head>", "")
        content = content.replace("<body>", "").replace("</body>", "")
        content = content.replace("<title>", "").replace("</title>", "")

        # Replace header tags
        for i in range(1, 7):
            content = content.replace(f"<h{i}>", "\n## ").replace(f"</h{i}>", "\n")

        # Replace paragraph tags
        content = content.replace("<p>", "").replace("</p>", "\n\n")

        # Replace list items
        content = content.replace("<li>", "- ").replace("</li>", "\n")

        # Remove other tags
        content = content.replace("<ul>", "").replace("</ul>", "")
        content = content.replace("<ol>", "").replace("</ol>", "")

        # Update document content
        doc.content = content
        doc.metadata["transformed"] = True

    return doc


def split_document(
    doc: Document, strategy: ChunkingStrategy, options: ChunkingOptions
) -> list[DocumentChunk]:
    """Split a document into chunks based on the chunking strategy.

    Args:
        doc: The document to split.
        strategy: The chunking strategy to use.
        options: The chunking options.

    Returns:
        A list of document chunks.
    """
    logger.info(f"Splitting document {doc.document_id} using strategy {strategy}")
    content = doc.content
    chunks = []

    if strategy == ChunkingStrategy.FIXED_SIZE:
        # Fixed size chunking
        chunk_size = options.chunk_size
        chunk_overlap = options.chunk_overlap

        start = 0
        chunk_index = 0

        while start < len(content):
            end = min(start + chunk_size, len(content))
            chunk_content = content[start:end]

            chunk_metadata = {
                "chunk_index": chunk_index,
                "start": start,
                "end": end,
                "source_path": doc.source_path,
            }

            # Add document metadata
            if options.metadata_scope in ["all", "document"]:
                for key, value in doc.metadata.items():
                    if key not in chunk_metadata:
                        chunk_metadata[key] = value

            # Create chunk
            chunks.append(
                DocumentChunk(
                    content=chunk_content,
                    document_id=doc.document_id,
                    chunk_index=chunk_index,
                    metadata=chunk_metadata,
                )
            )

            # Move to next position, accounting for overlap
            start = end - chunk_overlap if end < len(content) else len(content)
            chunk_index += 1

    elif strategy == ChunkingStrategy.PARAGRAPH:
        # Paragraph chunking
        paragraphs = content.split("\n\n")

        for i, paragraph in enumerate(paragraphs):
            paragraph = paragraph.strip()
            if not paragraph:
                continue

            chunk_metadata = {
                "chunk_index": i,
                "paragraph_index": i,
                "source_path": doc.source_path,
            }

            # Add document metadata
            if options.metadata_scope in ["all", "document"]:
                for key, value in doc.metadata.items():
                    if key not in chunk_metadata:
                        chunk_metadata[key] = value

            # Create chunk
            chunks.append(
                DocumentChunk(
                    content=paragraph,
                    document_id=doc.document_id,
                    chunk_index=i,
                    metadata=chunk_metadata,
                )
            )

    elif strategy == ChunkingStrategy.SENTENCE:
        # Sentence chunking
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

            chunk_metadata = {
                "chunk_index": i,
                "sentence_index": i,
                "source_path": doc.source_path,
            }

            # Add document metadata
            if options.metadata_scope in ["all", "document"]:
                for key, value in doc.metadata.items():
                    if key not in chunk_metadata:
                        chunk_metadata[key] = value

            # Create chunk
            chunks.append(
                DocumentChunk(
                    content=sentence,
                    document_id=doc.document_id,
                    chunk_index=i,
                    metadata=chunk_metadata,
                )
            )

    elif strategy == ChunkingStrategy.RECURSIVE:
        # Simplified recursive chunking - use a list of separators
        separators = options.custom_separators or ["\n\n", "\n", ". ", " "]

        # Use the first separator to split
        if separators:
            parts = content.split(separators[0])

            for i, part in enumerate(parts):
                part = part.strip()
                if not part:
                    continue

                chunk_metadata = {
                    "chunk_index": i,
                    "separator": separators[0],
                    "source_path": doc.source_path,
                }

                # Add document metadata
                if options.metadata_scope in ["all", "document"]:
                    for key, value in doc.metadata.items():
                        if key not in chunk_metadata:
                            chunk_metadata[key] = value

                # Create chunk
                chunks.append(
                    DocumentChunk(
                        content=part,
                        document_id=doc.document_id,
                        chunk_index=i,
                        metadata=chunk_metadata,
                    )
                )

    logger.info(f"Created {len(chunks)} chunks for document {doc.document_id}")
    return chunks


# ====== Path Analysis Implementation =======


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


def analyze_path(path: str) -> PathAnalysisResult:
    """Analyze a path to determine its type and format."""
    result = PathAnalysisResult()

    # Determine source type
    if path.startswith(("http://", "https://", "ftp://")):
        result.source_type = DocumentSourceType.URL
        result.document_format = DocumentFormat.HTML
        result.metadata = {"title": "Web Document"}
    elif path.startswith("text://"):
        result.source_type = DocumentSourceType.TEXT
        result.document_format = DocumentFormat.TXT
        result.metadata = {"content_length": len(path) - 7}  # Remove "text://" prefix
    elif path.lower().endswith(".txt"):
        result.source_type = DocumentSourceType.FILE
        result.document_format = DocumentFormat.TXT
        if os.path.exists(path):
            result.metadata = {"size_bytes": os.path.getsize(path)}
    elif path.lower().endswith(".pdf"):
        result.source_type = DocumentSourceType.FILE
        result.document_format = DocumentFormat.PDF
        if os.path.exists(path):
            result.metadata = {"size_bytes": os.path.getsize(path)}
    elif path.lower().endswith(".md"):
        result.source_type = DocumentSourceType.FILE
        result.document_format = DocumentFormat.MARKDOWN
        if os.path.exists(path):
            result.metadata = {"size_bytes": os.path.getsize(path)}
    elif path.lower().endswith(".html") or path.lower().endswith(".htm"):
        result.source_type = DocumentSourceType.FILE
        result.document_format = DocumentFormat.HTML
        if os.path.exists(path):
            result.metadata = {"size_bytes": os.path.getsize(path)}
    elif os.path.isdir(path):
        result.source_type = DocumentSourceType.DIRECTORY
        if os.path.exists(path):
            result.metadata = {"file_count": len(os.listdir(path))}

    return result


# ====== Document Loader Implementation =======


class MockDocument:
    """Mock document for the example."""

    def __init__(self, page_content: str, metadata: dict[str, Any]):
        self.page_content = page_content
        self.metadata = metadata


class MockLoader:
    """Mock document loader for the example."""

    def __init__(self, path: str, source_type: DocumentSourceType):
        self.path = path
        self.source_type = source_type

    def load(self) -> list[MockDocument]:
        """Load document(s) from the source."""
        # For text sources, extract content from the path
        if self.source_type == DocumentSourceType.TEXT:
            if self.path.startswith("text://"):
                content = self.path[7:]  # Remove "text://" prefix
            else:
                content = "Example text content"
            return [MockDocument(page_content=content, metadata={"source": self.path})]

        # For file sources, read content from file
        if self.source_type == DocumentSourceType.FILE:
            if os.path.exists(self.path):
                try:
                    with open(self.path, encoding="utf-8") as f:
                        content = f.read()
                    return [
                        MockDocument(
                            page_content=content,
                            metadata={
                                "source": self.path,
                                "size_bytes": os.path.getsize(self.path),
                                "last_modified": os.path.getmtime(self.path),
                            },
                        )
                    ]
                except Exception as e:
                    logger.exception(f"Error reading file {self.path}: {e!s}")
                    return [
                        MockDocument(
                            page_content=f"Error reading file: {e!s}",
                            metadata={"source": self.path, "error": str(e)},
                        )
                    ]
            else:
                return [
                    MockDocument(
                        page_content="File not found",
                        metadata={"source": self.path, "error": "File not found"},
                    )
                ]

        # For URL sources, return mock web content
        elif self.source_type == DocumentSourceType.URL:
            return [
                MockDocument(
                    page_content="Example web content from " + self.path,
                    metadata={"source": self.path, "url": self.path},
                )
            ]

        # For unknown sources, return generic content
        return [
            MockDocument(
                page_content="Example content for " + self.path,
                metadata={"source": self.path},
            )
        ]


def get_loader_for_source(path: str, source_type: DocumentSourceType) -> MockLoader:
    """Get a loader for the source."""
    return MockLoader(path, source_type)


# ====== Document Agent Implementation =======


class DocumentAgent:
    """Agent for loading and processing documents."""

    def __init__(
        self,
        state: DocumentState | None = None,
        options: DocumentAgentOptions | None = None,
    ):
        """Initialize the document agent."""
        self.state = state or DocumentState()
        self.options = options or DocumentAgentOptions()

        # Initialize state
        self._initialize_state()

    def _initialize_state(self) -> None:
        """Initialize the agent state."""
        self.state.loading_options = self.options.default_loading_options
        self.state.chunking_options = self.options.default_chunking_options
        self.state.parallel_processing = self.options.parallel_processing
        self.state.max_workers = self.options.max_workers

        # Initialize processing statistics
        self.state.processing_stats.start_time = datetime.datetime.now()

        logger.debug("Initialized DocumentAgent")

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

    def process_documents(self) -> None:
        """Process all documents in the agent's state."""
        logger.info("Starting document processing workflow")

        # Step 1: Analyze sources
        self._analyze_sources()

        # Step 2: Load documents
        self._load_documents()

        # Step 3: Chunk documents (if needed)
        if self._should_chunk_documents():
            self._chunk_documents()

        # Step 4: Finalize processing
        self._finalize_processing()

        # Log results
        stats = self.state.processing_stats
        logger.info("Document processing complete:")
        logger.info(
            f"- Sources: {stats.processed_sources} processed, {stats.failed_sources} failed"
        )
        logger.info(f"- Documents: {stats.total_documents} documents loaded")
        logger.info(f"- Chunks: {stats.total_chunks} chunks created")
        logger.info(f"- Processing time: {stats.processing_time_seconds:.2f} seconds")

    def _should_chunk_documents(self) -> bool:
        """Determine if we should proceed with document chunking."""
        # Skip chunking if chunking strategy is NONE
        if self.state.chunking_options.strategy == ChunkingStrategy.NONE:
            return False

        # Skip chunking if no documents need chunking
        chunking_sources = self.state.get_sources_by_stage(ProcessingStage.CHUNKING)
        return chunking_sources

    def _analyze_sources(self) -> None:
        """Analyze document sources and prepare them for loading."""
        logger.info("Analyzing sources...")

        for source in self.state.sources:
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
                    logger.info(
                        f"Source {source.path} analyzed as {source.source_type}, {source.format}"
                    )

                except Exception as e:
                    error_msg = f"Error analyzing source: {e!s}"
                    source.update_stage(ProcessingStage.FAILED, error_msg)
                    self.state.error_messages.append(error_msg)
                    logger.exception(f"Error analyzing source {source.path}: {e!s}")
                    if not self.options.skip_errors:
                        raise

    def _load_documents(self) -> None:
        """Load documents from sources."""
        logger.info("Loading documents...")

        queued_sources = self.state.get_sources_by_stage(ProcessingStage.QUEUED)

        if not queued_sources:
            logger.info("No sources queued for loading")
            return

        for source in queued_sources:
            try:
                source.update_stage(ProcessingStage.LOADING)
                logger.info(f"Loading {source.path}...")

                # Get loader for this source
                loader = get_loader_for_source(source.path, source.source_type)

                if loader is None:
                    error = f"No loader found for source: {source.path}"
                    source.update_stage(ProcessingStage.FAILED, error)
                    self.state.error_messages.append(error)
                    logger.error(f"Error: {error}")
                    continue

                # Load documents
                raw_docs = loader.load()

                # Convert to Document objects
                for _i, raw_doc in enumerate(raw_docs):
                    doc_id = f"{uuid.uuid4()}"
                    content = raw_doc.page_content

                    # Create document
                    doc = Document(
                        document_id=doc_id,
                        content=content,
                        source_path=source.path,
                        source_type=source.source_type,
                        format=source.format,
                        metadata=raw_doc.metadata,
                    )
                    self.state.documents.append(doc)
                    self.state.processing_stats.total_documents += 1
                    logger.info(
                        f"Created document {doc_id} with {len(content)} characters"
                    )

                # Update source stage
                if self.state.chunking_options.strategy == ChunkingStrategy.NONE:
                    source.update_stage(ProcessingStage.COMPLETED)
                else:
                    source.update_stage(ProcessingStage.CHUNKING)

            except Exception as e:
                error = f"Error loading source: {e!s}"
                source.update_stage(ProcessingStage.FAILED, error)
                self.state.error_messages.append(error)
                logger.exception(f"Error loading {source.path}: {e!s}")
                if not self.options.skip_errors:
                    raise

    def _chunk_documents(self) -> None:
        """Chunk documents into smaller pieces."""
        logger.info("Chunking documents...")

        chunking_sources = self.state.get_sources_by_stage(ProcessingStage.CHUNKING)

        if not chunking_sources:
            logger.info("No sources ready for chunking")
            return

        for source in chunking_sources:
            try:
                # Get documents for this source
                docs = self.state.get_documents_by_source(source.path)
                logger.info(f"Chunking {len(docs)} documents from {source.path}")

                for doc in docs:
                    # Skip already chunked documents
                    if doc.chunks:
                        continue

                    # Get chunking strategy
                    chunking_options = (
                        source.chunking_options or self.state.chunking_options
                    )

                    # Transform document if needed (like HTML to text)
                    transformed_doc = transform_document(doc)

                    # Split the document
                    chunks = split_document(
                        transformed_doc, chunking_options.strategy, chunking_options
                    )

                    # Add chunks to document
                    transformed_doc.chunks = chunks

                    # Update the document in the state
                    for i, state_doc in enumerate(self.state.documents):
                        if state_doc.document_id == doc.document_id:
                            self.state.documents[i] = transformed_doc
                            break

                    logger.info(
                        f"Created {len(chunks)} chunks for document {doc.document_id}"
                    )

                # Update source stage
                source.update_stage(ProcessingStage.COMPLETED)

            except Exception as e:
                error_msg = f"Error chunking documents: {e!s}"
                source.update_stage(ProcessingStage.FAILED, error_msg)
                self.state.error_messages.append(error_msg)
                logger.exception(f"Error chunking documents from {source.path}: {e!s}")
                if not self.options.skip_errors:
                    raise

    def _finalize_processing(self) -> None:
        """Finalize document processing."""
        logger.info("Finalizing document processing...")

        # Update statistics
        self.state.processing_stats.total_chunks = self.state.total_chunks

        # Estimate total tokens (very rough approximation)
        total_tokens = 0
        for doc in self.state.documents:
            # Estimate 4 characters per token on average
            doc_tokens = len(doc.content) // 4
            total_tokens += doc_tokens

        self.state.processing_stats.total_tokens = total_tokens

        # Mark processing as complete
        self.state.mark_processing_complete()


# ====== Factory Functions =======


def create_file_document_agent(
    file_paths: list[str],
    chunking_strategy: ChunkingStrategy = ChunkingStrategy.FIXED_SIZE,
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
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

    agent = DocumentAgent(options=options)
    agent.add_sources(file_paths)

    return agent


def create_web_document_agent(
    urls: list[str],
    chunking_strategy: ChunkingStrategy = ChunkingStrategy.PARAGRAPH,
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

    agent = DocumentAgent(options=options)
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

    # Create an HTML file
    html_file = os.path.join(temp_dir, "sample.html")
    with open(html_file, "w") as f:
        f.write(
            """<!DOCTYPE html>
<html>
<head>
    <title>Sample HTML Document</title>
</head>
<body>
    <h1>Sample HTML Document</h1>
    <p>This is a sample HTML document for testing the DocumentAgent.</p>

    <h2>Features</h2>
    <ul>
        <li>HTML to text transformation</li>
        <li>HTML header-based chunking</li>
        <li>Metadata extraction</li>
    </ul>

    <h2>Benefits</h2>
    <ol>
        <li>Automatic HTML parsing</li>
        <li>Semantic chunking based on HTML structure</li>
        <li>Clean text extraction from complex HTML</li>
    </ol>
</body>
</html>"""
        )
    file_paths.append(html_file)

    return file_paths


# ====== Example Implementations =======


def example_basic_usage():
    """Example of basic DocumentAgent usage."""
    logger.info("\n=== Example: Basic DocumentAgent Usage ===\n")

    # Create sample files
    file_paths = create_sample_files()

    # Create a document agent
    agent = DocumentAgent()

    # Add sources
    logger.info("Adding sources...")
    agent.add_sources(file_paths)
    agent.add_source("text://This is a sample text source for testing.")

    # Process documents
    agent.process_documents()

    # Display results
    logger.info("\nResults:")
    logger.info(f"- Processed {len(agent.get_documents())} documents")
    for doc in agent.get_documents():
        logger.info(
            f"  - {os.path.basename(doc.source_path)}: {len(doc.content)} chars, {doc.chunk_count} chunks"
        )

    # Display statistics
    stats = agent.state.processing_stats
    logger.info("\nProcessing statistics:")
    logger.info(f"- Total sources: {stats.total_sources}")
    logger.info(f"- Total documents: {stats.total_documents}")
    logger.info(f"- Total chunks: {stats.total_chunks}")
    logger.info(f"- Processing time: {stats.processing_time_seconds:.2f} seconds")


def example_chunking_strategies():
    """Example of different chunking strategies."""
    logger.info("\n=== Example: Different Chunking Strategies ===\n")

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
    logger.info("1. Fixed Size Chunking")
    fixed_agent = DocumentAgent(
        options=DocumentAgentOptions(
            default_chunking_options=ChunkingOptions(
                strategy=ChunkingStrategy.FIXED_SIZE,
                chunk_size=100,
                chunk_overlap=20,
            )
        )
    )
    fixed_agent.add_source(f"text://{text_content}")
    fixed_agent.process_documents()

    # Display results
    doc = fixed_agent.get_documents()[0]
    logger.info(f"Created {doc.chunk_count} fixed-size chunks:")
    for i, chunk in enumerate(doc.chunks[:3]):  # Show first 3 chunks
        logger.info(f"  Chunk {i}: '{chunk.content[:50]}...'")
    if doc.chunk_count > 3:
        logger.info(f"  (and {doc.chunk_count - 3} more chunks)")

    # 2. Paragraph chunking
    logger.info("\n2. Paragraph Chunking")
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
    logger.info(f"Created {doc.chunk_count} paragraph chunks:")
    for i, chunk in enumerate(doc.chunks):
        logger.info(f"  Paragraph {i}: '{chunk.content[:50]}...'")

    # 3. Sentence chunking
    logger.info("\n3. Sentence Chunking")
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
    logger.info(f"Created {doc.chunk_count} sentence chunks:")
    for i, chunk in enumerate(doc.chunks[:5]):  # Show first 5 sentences
        logger.info(f"  Sentence {i}: '{chunk.content}'")
    if doc.chunk_count > 5:
        logger.info(f"  (and {doc.chunk_count - 5} more sentences)")


def example_html_transformation():
    """Example of HTML document transformation."""
    logger.info("\n=== Example: HTML Transformation ===\n")

    # Create sample files
    file_paths = create_sample_files()

    # Get only the HTML file
    html_file = next(f for f in file_paths if f.endswith(".html"))

    # Create a document agent specifically for HTML processing
    options = DocumentAgentOptions(
        default_chunking_options=ChunkingOptions(
            strategy=ChunkingStrategy.PARAGRAPH,
        )
    )

    agent = DocumentAgent(options=options)
    agent.add_source(html_file)

    # Process documents
    logger.info("Processing HTML document...")
    agent.process_documents()

    # Display results
    if agent.get_documents():
        doc = agent.get_documents()[0]
        logger.info(f"Original HTML content length: {os.path.getsize(html_file)} bytes")
        logger.info(f"Transformed text content length: {len(doc.content)} chars")
        logger.info("Transformed content preview:")
        logger.info(f"\n{doc.content[:300]}...\n")
        logger.info(f"Created {doc.chunk_count} chunks from the HTML content")

        # Show the first few chunks
        for i, chunk in enumerate(doc.chunks[:3]):
            logger.info(f"  Chunk {i}: '{chunk.content[:50]}...'")
    else:
        logger.warning("No documents processed")


def main():
    """Run the example script."""
    logger.info("==== Document Processing System Example ====")

    example_basic_usage()
    example_chunking_strategies()
    example_html_transformation()

    logger.info("\n==== Example Complete ====")


if __name__ == "__main__":
    main()
