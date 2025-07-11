"""Document models for Haive document processing.

This module provides a comprehensive set of models for document processing in Haive.
It includes base models, enums, and specialized models for different document types
and operations, designed to be used as prebuilt components in the Haive framework.
"""

from __future__ import annotations

import datetime
import uuid
from enum import Enum
from typing import Any, ClassVar

from langchain_core.documents import Document as LCDocument
from pydantic import BaseModel, Field, validator

# ===== Base Enums =====


class DocumentSourceType(str, Enum):
    """Enum of document source types."""

    FILE = "file"
    DIRECTORY = "directory"
    URL = "url"
    DATABASE = "database"
    API = "api"
    TEXT = "text"
    CLOUD = "cloud"
    UNKNOWN = "unknown"


class DocumentFormat(str, Enum):
    """Enum of document format types."""

    # Text formats
    TXT = "txt"
    MARKDOWN = "markdown"
    HTML = "html"

    # Document formats
    PDF = "pdf"
    DOCX = "docx"
    DOC = "doc"
    RTF = "rtf"
    ODT = "odt"

    # Data formats
    CSV = "csv"
    JSON = "json"
    XML = "xml"
    YAML = "yaml"

    # Media formats
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"

    # Code formats
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    JAVA = "java"
    CPP = "cpp"

    # Database formats
    SQL = "sql"

    # Other
    UNKNOWN = "unknown"

    @classmethod
    def from_extension(cls, extension: str) -> DocumentFormat:
        """Get document format from file extension.

        Args:
            extension: File extension (with or without leading dot).

        Returns:
            DocumentFormat: The corresponding document format.
        """
        if extension.startswith("."):
            extension = extension[1:]
        extension = extension.lower()

        extension_mapping = {
            "txt": cls.TXT,
            "md": cls.MARKDOWN,
            "html": cls.HTML,
            "htm": cls.HTML,
            "pdf": cls.PDF,
            "docx": cls.DOCX,
            "doc": cls.DOC,
            "rtf": cls.RTF,
            "odt": cls.ODT,
            "csv": cls.CSV,
            "json": cls.JSON,
            "xml": cls.XML,
            "yaml": cls.YAML,
            "yml": cls.YAML,
            "jpg": cls.IMAGE,
            "jpeg": cls.IMAGE,
            "png": cls.IMAGE,
            "gif": cls.IMAGE,
            "mp3": cls.AUDIO,
            "wav": cls.AUDIO,
            "ogg": cls.AUDIO,
            "mp4": cls.VIDEO,
            "avi": cls.VIDEO,
            "mov": cls.VIDEO,
            "py": cls.PYTHON,
            "js": cls.JAVASCRIPT,
            "java": cls.JAVA,
            "cpp": cls.CPP,
            "sql": cls.SQL,
        }

        return extension_mapping.get(extension, cls.UNKNOWN)


class ProcessingStage(str, Enum):
    """Enum of document processing stages."""

    INITIALIZED = "initialized"
    QUEUED = "queued"
    ANALYZING = "analyzing"
    LOADING = "loading"
    TRANSFORMING = "transforming"
    CHUNKING = "chunking"
    EMBEDDING = "embedding"
    VECTORIZING = "vectorizing"
    INDEXING = "indexing"
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
    STREAMING = "streaming"


class ChunkingStrategy(str, Enum):
    """Enum of document chunking strategies."""

    NONE = "none"
    FIXED_SIZE = "fixed_size"
    SEMANTIC = "semantic"
    RECURSIVE = "recursive"
    PARAGRAPH = "paragraph"
    SENTENCE = "sentence"
    HEADER = "header"
    CODE = "code"
    CUSTOM = "custom"


class EmbeddingModel(str, Enum):
    """Enum of embedding models."""

    OPENAI = "openai"
    COHERE = "cohere"
    HUGGINGFACE = "huggingface"
    SENTENCE_TRANSFORMERS = "sentence_transformers"
    CUSTOM = "custom"
    NONE = "none"


# ===== Base Models =====


class BaseDocumentModel(BaseModel):
    """Base model for document-related models.

    This base model provides common functionality and metadata fields for
    all document-related models in the system.

    Attributes:
        id (str): Unique identifier for this model instance.
        created_at (datetime.datetime): When this instance was created.
        updated_at (datetime.datetime): When this instance was last updated.
    """

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.now)

    def update_timestamp(self) -> None:
        """Update the updated_at timestamp."""
        self.updated_at = datetime.datetime.now()

    class Config:
        """Pydantic configuration."""

        arbitrary_types_allowed = True


class MetadataModel(BaseDocumentModel):
    """Base model for metadata.

    This model provides a base for all metadata models in the system, with common
    fields and functionality.

    Attributes:
        size_bytes (Optional[int]): Size in bytes.
        mime_type (Optional[str]): MIME type.
        encoding (Optional[str]): Text encoding.
        author (Optional[str]): Author.
        title (Optional[str]): Title.
        description (Optional[str]): Description.
        language (Optional[str]): Language code (e.g., "en", "fr").
        tags (List[str]): Tags.
        custom (Dict[str, Any]): Custom metadata fields.
    """

    size_bytes: int | None = None
    mime_type: str | None = None
    encoding: str | None = None
    author: str | None = None
    title: str | None = None
    description: str | None = None
    language: str | None = None
    tags: list[str] = Field(default_factory=list)
    custom: dict[str, Any] = Field(default_factory=dict)

    def update(self, **kwargs: Any) -> None:
        """Update metadata fields.

        Args:
            **kwargs: The fields to update.
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                self.custom[key] = value

        self.update_timestamp()

    def to_dict(self) -> dict[str, Any]:
        """Convert metadata to a flat dictionary.

        Returns:
            Dict[str, Any]: Dictionary of metadata.
        """
        result = {}

        # Add all fields except custom
        for field_name, field_value in self.dict(exclude={"custom"}).items():
            if field_value is not None and field_name not in [
                "id",
                "created_at",
                "updated_at",
            ]:
                result[field_name] = field_value

        # Add custom fields
        result.update(self.custom)

        return result


# ===== Configuration Models =====


class LoadingOptions(BaseDocumentModel):
    """Options for document loading.

    Attributes:
        strategy (LoadingStrategy): The loading strategy to use.
        max_size_bytes (Optional[int]): Maximum size in bytes to load.
        recursive_depth (int): How deep to recursively load.
        exclude_patterns (List[str]): Patterns to exclude from loading.
        include_patterns (List[str]): Patterns to include in loading.
        max_files (Optional[int]): Maximum number of files to load.
        force_reload (bool): Whether to force reload even if already loaded.
        timeout_seconds (int): Timeout in seconds for loading operations.
        extract_metadata (bool): Whether to extract metadata from documents.
    """

    strategy: LoadingStrategy = LoadingStrategy.AUTO
    max_size_bytes: int | None = None
    recursive_depth: int = 3
    exclude_patterns: list[str] = Field(default_factory=list)
    include_patterns: list[str] = Field(default_factory=list)
    max_files: int | None = None
    force_reload: bool = False
    timeout_seconds: int = 60
    extract_metadata: bool = True

    def to_dict(self) -> dict[str, Any]:
        """Convert options to dictionary.

        Returns:
            Dict[str, Any]: Dictionary representation of options.
        """
        return {
            "strategy": self.strategy.value,
            "max_size_bytes": self.max_size_bytes,
            "recursive_depth": self.recursive_depth,
            "exclude_patterns": self.exclude_patterns,
            "include_patterns": self.include_patterns,
            "max_files": self.max_files,
            "force_reload": self.force_reload,
            "timeout_seconds": self.timeout_seconds,
            "extract_metadata": self.extract_metadata,
        }


class ChunkingOptions(BaseDocumentModel):
    """Options for document chunking.

    Attributes:
        strategy (ChunkingStrategy): The chunking strategy to use.
        chunk_size (int): Size of chunks in characters or tokens.
        chunk_overlap (int): Overlap between chunks in characters or tokens.
        keep_separator (bool): Whether to keep separators in chunks.
        custom_separators (List[str]): Custom separators for chunking.
        metadata_scope (str): Scope of metadata to include ("document", "chunk", "all").
        add_chunk_info (bool): Whether to add chunk info to metadata.
        token_model (Optional[str]): Token model to use for token-based chunking.
    """

    strategy: ChunkingStrategy = ChunkingStrategy.FIXED_SIZE
    chunk_size: int = 1000
    chunk_overlap: int = 200
    keep_separator: bool = True
    custom_separators: list[str] = Field(default_factory=list)
    metadata_scope: str = "all"
    add_chunk_info: bool = True
    token_model: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert options to dictionary.

        Returns:
            Dict[str, Any]: Dictionary representation of options.
        """
        return {
            "strategy": self.strategy.value,
            "chunk_size": self.chunk_size,
            "chunk_overlap": self.chunk_overlap,
            "keep_separator": self.keep_separator,
            "custom_separators": self.custom_separators,
            "metadata_scope": self.metadata_scope,
            "add_chunk_info": self.add_chunk_info,
            "token_model": self.token_model,
        }


class EmbeddingOptions(BaseDocumentModel):
    """Options for document embedding.

    Attributes:
        model (EmbeddingModel): The embedding model to use.
        model_name (str): Name of the specific model.
        batch_size (int): Batch size for embedding operations.
        embed_chunks (bool): Whether to embed chunks.
        embed_documents (bool): Whether to embed whole documents.
        dimensions (Optional[int]): Dimensions of embeddings.
    """

    model: EmbeddingModel = EmbeddingModel.NONE
    model_name: str = "default"
    batch_size: int = 32
    embed_chunks: bool = True
    embed_documents: bool = False
    dimensions: int | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert options to dictionary.

        Returns:
            Dict[str, Any]: Dictionary representation of options.
        """
        return {
            "model": self.model.value,
            "model_name": self.model_name,
            "batch_size": self.batch_size,
            "embed_chunks": self.embed_chunks,
            "embed_documents": self.embed_documents,
            "dimensions": self.dimensions,
        }


# ===== Document Models =====


class DocumentSourceMetadata(MetadataModel):
    """Metadata for document sources.

    Attributes:
        source_size_bytes (Optional[int]): Size of the source in bytes.
        last_modified (Optional[datetime.datetime]): When the source was last modified.
        file_count (Optional[int]): Number of files in a directory source.
        url (Optional[str]): URL for web sources.
        parent_id (Optional[str]): ID of parent source (for nested sources).
    """

    source_size_bytes: int | None = None
    last_modified: datetime.datetime | None = None
    file_count: int | None = None
    url: str | None = None
    parent_id: str | None = None


class DocumentSource(BaseDocumentModel):
    """A document source with path and configuration.

    Attributes:
        path (str): The path or URL to the document source.
        source_type (DocumentSourceType): The type of source.
        format (DocumentFormat): The format of the document.
        credential_id (Optional[str]): ID of credential needed to access this source.
        metadata (DocumentSourceMetadata): Metadata about the source.
        stage (ProcessingStage): Current processing stage.
        loading_options (LoadingOptions): Options for loading.
        chunking_options (ChunkingOptions): Options for chunking.
        embedding_options (EmbeddingOptions): Options for embedding.
        error (Optional[str]): Error message if loading failed.
        last_processed (Optional[datetime.datetime]): When the source was last processed.
    """

    path: str
    source_type: DocumentSourceType = DocumentSourceType.UNKNOWN
    format: DocumentFormat = DocumentFormat.UNKNOWN
    credential_id: str | None = None
    metadata: DocumentSourceMetadata = Field(default_factory=DocumentSourceMetadata)
    stage: ProcessingStage = ProcessingStage.INITIALIZED
    loading_options: LoadingOptions = Field(default_factory=LoadingOptions)
    chunking_options: ChunkingOptions = Field(default_factory=ChunkingOptions)
    embedding_options: EmbeddingOptions = Field(default_factory=EmbeddingOptions)
    error: str | None = None
    last_processed: datetime.datetime | None = None

    @validator("source_type", pre=True)
    def set_source_type(self, v, values):
        """Validate and set source type based on path if not provided."""
        if v != DocumentSourceType.UNKNOWN:
            return v

        path = values.get("path", "")
        if path.startswith(("http://", "https://", "ftp://")):
            return DocumentSourceType.URL
        if path.startswith(("db://", "sql://", "mongodb://", "postgres://")):
            return DocumentSourceType.DATABASE
        if path.startswith(("api://", "rest://")):
            return DocumentSourceType.API
        if path.startswith(("s3://", "gs://", "azure://", "oss://")):
            return DocumentSourceType.CLOUD
        if not path or path.startswith(("text://", "content://")):
            return DocumentSourceType.TEXT
        if "/" in path or "\\" in path:
            import os

            if os.path.isdir(path):
                return DocumentSourceType.DIRECTORY
            return DocumentSourceType.FILE

        return DocumentSourceType.UNKNOWN

    @validator("format", pre=True)
    def set_format(self, v, values):
        """Validate and set format based on path if not provided."""
        if v != DocumentFormat.UNKNOWN:
            return v

        path = values.get("path", "")
        if not path:
            return DocumentFormat.UNKNOWN

        # Extract extension
        import os

        _, ext = os.path.splitext(path.lower())
        if ext:
            return DocumentFormat.from_extension(ext)

        # Format from URL patterns
        if path.startswith(("http://", "https://")):
            return DocumentFormat.HTML

        return DocumentFormat.UNKNOWN

    def update_stage(self, stage: ProcessingStage, error: str | None = None) -> None:
        """Update the processing stage of this source.

        Args:
            stage: The new processing stage.
            error: Optional error message if stage is FAILED.
        """
        self.stage = stage
        if stage == ProcessingStage.FAILED and error:
            self.error = error
        if stage == ProcessingStage.COMPLETED:
            self.last_processed = datetime.datetime.now()
        self.update_timestamp()

    def to_dict(self) -> dict[str, Any]:
        """Convert source to dictionary.

        Returns:
            Dict[str, Any]: Dictionary representation of source.
        """
        return {
            "id": self.id,
            "path": self.path,
            "source_type": self.source_type.value,
            "format": self.format.value,
            "credential_id": self.credential_id,
            "metadata": self.metadata.to_dict(),
            "stage": self.stage.value,
            "error": self.error,
            "last_processed": (
                self.last_processed.isoformat() if self.last_processed else None
            ),
        }

    def to_langchain_metadata(self) -> dict[str, Any]:
        """Convert source to LangChain metadata.

        Returns:
            Dict[str, Any]: Metadata dictionary for LangChain documents.
        """
        return {
            "source_id": self.id,
            "source_path": self.path,
            "source_type": self.source_type.value,
            "format": self.format.value,
            **self.metadata.to_dict(),
        }


class DocumentChunk(BaseDocumentModel):
    """A chunk of a document.

    Attributes:
        content (str): The content of the chunk.
        document_id (str): ID of the parent document.
        chunk_index (int): Index of this chunk in the document.
        metadata (Dict[str, Any]): Metadata for this chunk.
        embedding (Optional[List[float]]): Vector embedding of this chunk.
    """

    content: str
    document_id: str
    chunk_index: int
    metadata: dict[str, Any] = Field(default_factory=dict)
    embedding: list[float] | None = None

    @property
    def token_estimate(self) -> int:
        """Estimate the number of tokens in this chunk.

        Returns:
            int: Estimated number of tokens.
        """
        # Simple estimate: 4 characters per token
        return len(self.content) // 4

    def to_langchain(self) -> LCDocument:
        """Convert to LangChain Document.

        Returns:
            LCDocument: A LangChain Document.
        """
        return LCDocument(
            page_content=self.content,
            metadata={
                "chunk_id": self.id,
                "document_id": self.document_id,
                "chunk_index": self.chunk_index,
                **self.metadata,
            },
        )

    @classmethod
    def from_langchain(
        cls, lc_doc: LCDocument, document_id: str, chunk_index: int
    ) -> DocumentChunk:
        """Create a DocumentChunk from a LangChain Document.

        Args:
            lc_doc: LangChain Document.
            document_id: ID of the parent document.
            chunk_index: Index of this chunk.

        Returns:
            DocumentChunk: A new DocumentChunk.
        """
        # Extract metadata, excluding fields that will be set explicitly
        metadata = lc_doc.metadata.copy()
        for field in ["chunk_id", "document_id", "chunk_index"]:
            if field in metadata:
                del metadata[field]

        return cls(
            content=lc_doc.page_content,
            document_id=document_id,
            chunk_index=chunk_index,
            metadata=metadata,
        )


class Document(BaseDocumentModel):
    """A document loaded from a source.

    Attributes:
        content (str): The content of the document.
        source_path (str): Path or URL where the document was loaded from.
        source_type (DocumentSourceType): Type of the source.
        format (DocumentFormat): Format of the document.
        metadata (Dict[str, Any]): Metadata about the document.
        chunks (List[DocumentChunk]): Chunks of this document.
        embedding (Optional[List[float]]): Vector embedding of the document.
        source_id (Optional[str]): ID of the source this document was loaded from.
        chunking_options (Optional[ChunkingOptions]): Options for chunking this document.
    """

    content: str
    source_path: str
    source_type: DocumentSourceType = DocumentSourceType.UNKNOWN
    format: DocumentFormat = DocumentFormat.UNKNOWN
    metadata: dict[str, Any] = Field(default_factory=dict)
    chunks: list[DocumentChunk] = Field(default_factory=list)
    embedding: list[float] | None = None
    source_id: str | None = None
    chunking_options: ChunkingOptions | None = None

    @property
    def chunk_count(self) -> int:
        """Get the number of chunks in this document.

        Returns:
            int: Number of chunks.
        """
        return len(self.chunks)

    @property
    def token_estimate(self) -> int:
        """Estimate the number of tokens in this document.

        Returns:
            int: Estimated number of tokens.
        """
        # Simple estimate: 4 characters per token
        return len(self.content) // 4

    def add_chunk(
        self, content: str, metadata: dict[str, Any] | None = None
    ) -> DocumentChunk:
        """Add a chunk to this document.

        Args:
            content: The content of the chunk.
            metadata: Optional metadata for the chunk.

        Returns:
            DocumentChunk: The created chunk.
        """
        if metadata is None:
            metadata = {}

        chunk = DocumentChunk(
            content=content,
            document_id=self.id,
            chunk_index=len(self.chunks),
            metadata={
                **metadata,
                "document_id": self.id,
                "source_path": self.source_path,
            },
        )
        self.chunks.append(chunk)
        self.update_timestamp()
        return chunk

    def to_langchain(self) -> LCDocument:
        """Convert to LangChain Document.

        Returns:
            LCDocument: A LangChain Document.
        """
        return LCDocument(
            page_content=self.content,
            metadata={
                "document_id": self.id,
                "source": self.source_path,
                "source_type": self.source_type.value,
                "format": self.format.value,
                **self.metadata,
            },
        )

    @classmethod
    def from_langchain(cls, lc_doc: LCDocument, **kwargs: Any) -> Document:
        """Create a Document from a LangChain Document.

        Args:
            lc_doc: LangChain Document.
            **kwargs: Additional fields to set.

        Returns:
            Document: A new Document.
        """
        # Extract metadata
        metadata = lc_doc.metadata.copy()

        # Try to extract source path, source type, and format from metadata
        source_path = metadata.pop("source", kwargs.get("source_path", ""))
        source_type_str = metadata.pop("source_type", "unknown")
        format_str = metadata.pop("format", "unknown")

        # Convert to enum values
        try:
            source_type = DocumentSourceType(source_type_str)
        except (ValueError, TypeError):
            source_type = DocumentSourceType.UNKNOWN

        try:
            format = DocumentFormat(format_str)
        except (ValueError, TypeError):
            format = DocumentFormat.UNKNOWN

        # Create document
        return cls(
            content=lc_doc.page_content,
            source_path=source_path,
            source_type=source_type,
            format=format,
            metadata=metadata,
            **kwargs,
        )

    def get_chunks_as_langchain(self) -> list[LCDocument]:
        """Get all chunks as LangChain Documents.

        Returns:
            List[LCDocument]: List of LangChain Documents.
        """
        return [chunk.to_langchain() for chunk in self.chunks]


class ProcessingStatistics(BaseDocumentModel):
    """Statistics about document processing.

    Attributes:
        start_time (datetime.datetime): When processing started.
        end_time (Optional[datetime.datetime]): When processing completed.
        total_sources (int): Total number of sources.
        processed_sources (int): Number of processed sources.
        failed_sources (int): Number of failed sources.
        total_documents (int): Total number of documents.
        total_chunks (int): Total number of chunks.
        total_tokens (int): Total number of tokens.
        errors_count (int): Number of errors encountered.
    """

    start_time: datetime.datetime = Field(default_factory=datetime.datetime.now)
    end_time: datetime.datetime | None = None
    total_sources: int = 0
    processed_sources: int = 0
    failed_sources: int = 0
    total_documents: int = 0
    total_chunks: int = 0
    total_tokens: int = 0
    errors_count: int = 0

    @property
    def processing_time_seconds(self) -> float:
        """Calculate the total processing time in seconds.

        Returns:
            float: Processing time in seconds, or -1 if still processing.
        """
        if self.end_time is None:
            return (datetime.datetime.now() - self.start_time).total_seconds()
        return (self.end_time - self.start_time).total_seconds()

    @property
    def is_complete(self) -> bool:
        """Check if processing is complete.

        Returns:
            bool: True if processing is complete, False otherwise.
        """
        return self.end_time is not None

    def complete(self) -> None:
        """Mark processing as complete."""
        self.end_time = datetime.datetime.now()
        self.update_timestamp()

    def update(self, **kwargs: Any) -> None:
        """Update statistics.

        Args:
            **kwargs: Statistics to update.
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.update_timestamp()

    def increment(self, field: str, amount: int = 1) -> None:
        """Increment a statistic.

        Args:
            field: The field to increment.
            amount: The amount to increment by.
        """
        if hasattr(self, field):
            current_value = getattr(self, field)
            if isinstance(current_value, int):
                setattr(self, field, current_value + amount)
        self.update_timestamp()


class DocumentCredential(BaseDocumentModel):
    """Credential for accessing documents.

    Attributes:
        credential_type (str): The type of credential (api_key, token, username_password, etc.).
        credential_data (Dict[str, Any]): The credential data as a dictionary.
        service_name (Optional[str]): The name of the service this credential is for.
        expires_at (Optional[datetime.datetime]): When this credential expires.
    """

    credential_type: str
    credential_data: dict[str, Any]
    service_name: str | None = None
    expires_at: datetime.datetime | None = None

    @property
    def is_expired(self) -> bool:
        """Check if the credential is expired.

        Returns:
            bool: True if the credential is expired, False otherwise.
        """
        if self.expires_at is None:
            return False
        return self.expires_at < datetime.datetime.now()


# ===== Document Collection Models =====


class DocumentCollection(BaseDocumentModel):
    """A collection of related documents.

    Attributes:
        name (str): Name of the collection.
        description (Optional[str]): Description of the collection.
        documents (List[Document]): Documents in the collection.
        metadata (Dict[str, Any]): Metadata about the collection.
        tags (List[str]): Tags associated with the collection.
    """

    name: str
    description: str | None = None
    documents: list[Document] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
    tags: list[str] = Field(default_factory=list)

    @property
    def document_count(self) -> int:
        """Get the number of documents in this collection.

        Returns:
            int: Number of documents.
        """
        return len(self.documents)

    @property
    def chunk_count(self) -> int:
        """Get the total number of chunks in this collection.

        Returns:
            int: Number of chunks.
        """
        return sum(doc.chunk_count for doc in self.documents)

    @property
    def token_estimate(self) -> int:
        """Estimate the total number of tokens in this collection.

        Returns:
            int: Estimated number of tokens.
        """
        return sum(doc.token_estimate for doc in self.documents)

    def add_document(self, document: Document) -> None:
        """Add a document to the collection.

        Args:
            document: The document to add.
        """
        self.documents.append(document)
        self.update_timestamp()

    def get_all_chunks(self) -> list[DocumentChunk]:
        """Get all chunks from all documents in this collection.

        Returns:
            List[DocumentChunk]: All chunks.
        """
        chunks = []
        for doc in self.documents:
            chunks.extend(doc.chunks)
        return chunks

    def to_langchain_documents(self) -> list[LCDocument]:
        """Convert all documents to LangChain Documents.

        Returns:
            List[LCDocument]: List of LangChain Documents.
        """
        return [doc.to_langchain() for doc in self.documents]

    def get_all_chunks_as_langchain(self) -> list[LCDocument]:
        """Get all chunks as LangChain Documents.

        Returns:
            List[LCDocument]: List of LangChain Documents.
        """
        lc_docs = []
        for doc in self.documents:
            lc_docs.extend(doc.get_chunks_as_langchain())
        return lc_docs


# ===== Error Models =====


class DocumentError(BaseDocumentModel):
    """An error that occurred during document processing.

    Attributes:
        error_type (str): Type of error.
        message (str): Error message.
        source_path (Optional[str]): Path of the source that caused the error.
        source_id (Optional[str]): ID of the source that caused the error.
        document_id (Optional[str]): ID of the document that caused the error.
        stage (ProcessingStage): Stage where the error occurred.
        traceback (Optional[str]): Traceback of the error.
        recoverable (bool): Whether the error is recoverable.
    """

    error_type: str
    message: str
    source_path: str | None = None
    source_id: str | None = None
    document_id: str | None = None
    stage: ProcessingStage = ProcessingStage.INITIALIZED
    traceback: str | None = None
    recoverable: bool = True

    @classmethod
    def from_exception(
        cls,
        exception: Exception,
        stage: ProcessingStage,
        source_path: str | None = None,
        source_id: str | None = None,
        document_id: str | None = None,
        recoverable: bool = True,
    ) -> DocumentError:
        """Create a DocumentError from an exception.

        Args:
            exception: The exception that occurred.
            stage: The stage where the error occurred.
            source_path: Optional path of the source that caused the error.
            source_id: Optional ID of the source that caused the error.
            document_id: Optional ID of the document that caused the error.
            recoverable: Whether the error is recoverable.

        Returns:
            DocumentError: A new DocumentError.
        """
        import traceback

        return cls(
            error_type=type(exception).__name__,
            message=str(exception),
            source_path=source_path,
            source_id=source_id,
            document_id=document_id,
            stage=stage,
            traceback=traceback.format_exc(),
            recoverable=recoverable,
        )


# ===== Document State Models =====


class DocumentState(BaseDocumentModel):
    """State schema for document operations.

    This state schema tracks document sources, loaded documents, and processing
    state for document operations in Haive agents.

    Attributes:
        sources (List[DocumentSource]): Document sources to process.
        documents (List[Document]): Loaded documents.
        collections (Dict[str, DocumentCollection]): Document collections.
        credentials (Dict[str, DocumentCredential]): Credentials for accessing sources.
        loading_options (LoadingOptions): Default loading options.
        chunking_options (ChunkingOptions): Default chunking options.
        embedding_options (EmbeddingOptions): Default embedding options.
        processing_stats (ProcessingStatistics): Statistics about document processing.
        current_query (Optional[str]): Current query being processed.
        messages (List[Dict[str, Any]]): Messages for agent interaction.
        parallel_processing (bool): Whether to process sources in parallel.
        max_workers (int): Maximum number of parallel workers.
        errors (List[DocumentError]): Errors from processing.
    """

    sources: list[DocumentSource] = Field(default_factory=list)
    documents: list[Document] = Field(default_factory=list)
    collections: dict[str, DocumentCollection] = Field(default_factory=dict)
    credentials: dict[str, DocumentCredential] = Field(default_factory=dict)
    loading_options: LoadingOptions = Field(default_factory=LoadingOptions)
    chunking_options: ChunkingOptions = Field(default_factory=ChunkingOptions)
    embedding_options: EmbeddingOptions = Field(default_factory=EmbeddingOptions)
    processing_stats: ProcessingStatistics = Field(default_factory=ProcessingStatistics)
    current_query: str | None = None
    messages: list[dict[str, Any]] = Field(default_factory=list)
    parallel_processing: bool = True
    max_workers: int = 4
    errors: list[DocumentError] = Field(default_factory=list)

    # Class attribute for integrations
    _langchain_enabled: ClassVar[bool] = True

    def add_source(self, path: str, **kwargs: Any) -> DocumentSource:
        """Add a document source to be processed.

        Args:
            path: Path or URL to the document source.
            **kwargs: Additional fields to set on the DocumentSource.

        Returns:
            DocumentSource: The created source.
        """
        source = DocumentSource(path=path, **kwargs)
        self.sources.append(source)
        self.processing_stats.total_sources += 1
        return source

    def add_sources(self, paths: list[str]) -> list[DocumentSource]:
        """Add multiple document sources to be processed.

        Args:
            paths: List of paths or URLs to document sources.

        Returns:
            List[DocumentSource]: The created sources.
        """
        sources = []
        for path in paths:
            source = self.add_source(path)
            sources.append(source)
        return sources

    def add_document(self, content: str, source_path: str, **kwargs: Any) -> Document:
        """Add a document to the state.

        Args:
            content: The content of the document.
            source_path: Path or URL where the document was loaded from.
            **kwargs: Additional fields to set on the Document.

        Returns:
            Document: The created document.
        """
        document = Document(content=content, source_path=source_path, **kwargs)
        self.documents.append(document)
        self.processing_stats.total_documents += 1
        return document

    def add_langchain_document(self, lc_doc: LCDocument, **kwargs: Any) -> Document:
        """Add a LangChain document to the state.

        Args:
            lc_doc: The LangChain document.
            **kwargs: Additional fields to set on the Document.

        Returns:
            Document: The created document.
        """
        document = Document.from_langchain(lc_doc, **kwargs)
        self.documents.append(document)
        self.processing_stats.total_documents += 1
        return document

    def add_collection(
        self, name: str, description: str | None = None
    ) -> DocumentCollection:
        """Add a document collection.

        Args:
            name: Name of the collection.
            description: Optional description of the collection.

        Returns:
            DocumentCollection: The created collection.
        """
        collection = DocumentCollection(name=name, description=description)
        self.collections[collection.id] = collection
        return collection

    def add_credential(
        self,
        credential_id: str,
        credential_type: str,
        credential_data: dict[str, Any],
        **kwargs: Any,
    ) -> DocumentCredential:
        """Add a credential for accessing document sources.

        Args:
            credential_id: Unique identifier for the credential.
            credential_type: Type of credential.
            credential_data: Credential data.
            **kwargs: Additional fields to set on the DocumentCredential.

        Returns:
            DocumentCredential: The created credential.
        """
        credential = DocumentCredential(
            credential_type=credential_type, credential_data=credential_data, **kwargs
        )
        self.credentials[credential_id] = credential
        return credential

    def add_error(
        self, error: DocumentError | Exception, **kwargs: Any
    ) -> DocumentError:
        """Add an error to the state.

        Args:
            error: The error to add. Can be a DocumentError or an Exception.
            **kwargs: Additional fields for creating a DocumentError from an Exception.

        Returns:
            DocumentError: The added error.
        """
        if isinstance(error, Exception):
            doc_error = DocumentError.from_exception(error, **kwargs)
        else:
            doc_error = error

        self.errors.append(doc_error)
        self.processing_stats.errors_count += 1
        return doc_error

    def update_source_stage(
        self, path: str, stage: ProcessingStage, error: str | None = None
    ) -> None:
        """Update the processing stage of a source.

        Args:
            path: Path of the source to update.
            stage: New processing stage.
            error: Optional error message.
        """
        for source in self.sources:
            if source.path == path:
                source.update_stage(stage, error)
                if stage == ProcessingStage.COMPLETED:
                    self.processing_stats.processed_sources += 1
                elif stage == ProcessingStage.FAILED:
                    self.processing_stats.failed_sources += 1
                    if error:
                        self.add_error(
                            DocumentError(
                                error_type="SourceProcessingError",
                                message=error,
                                source_path=path,
                                source_id=source.id,
                                stage=stage,
                            )
                        )
                return

    def get_credential(self, credential_id: str) -> DocumentCredential | None:
        """Get a credential by ID.

        Args:
            credential_id: The ID of the credential.

        Returns:
            Optional[DocumentCredential]: The credential, or None if not found.
        """
        return self.credentials.get(credential_id)

    def get_document(self, document_id: str) -> Document | None:
        """Get a document by ID.

        Args:
            document_id: The ID of the document.

        Returns:
            Optional[Document]: The document, or None if not found.
        """
        for doc in self.documents:
            if doc.id == document_id:
                return doc
        return None

    def get_collection(self, collection_id: str) -> DocumentCollection | None:
        """Get a collection by ID.

        Args:
            collection_id: The ID of the collection.

        Returns:
            Optional[DocumentCollection]: The collection, or None if not found.
        """
        return self.collections.get(collection_id)

    def get_documents_by_source(self, source_path: str) -> list[Document]:
        """Get all documents from a specific source.

        Args:
            source_path: Path of the source.

        Returns:
            List[Document]: Documents from the source.
        """
        return [doc for doc in self.documents if doc.source_path == source_path]

    def get_documents_by_format(self, format: DocumentFormat | str) -> list[Document]:
        """Get all documents of a specific format.

        Args:
            format: The format to filter by.

        Returns:
            List[Document]: Documents with the specified format.
        """
        if isinstance(format, str):
            try:
                format = DocumentFormat(format)
            except ValueError:
                format = DocumentFormat.UNKNOWN
        return [doc for doc in self.documents if doc.format == format]

    def get_sources_by_stage(self, stage: ProcessingStage) -> list[DocumentSource]:
        """Get all sources in a specific processing stage.

        Args:
            stage: The processing stage to filter by.

        Returns:
            List[DocumentSource]: Sources in the specified stage.
        """
        return [source for source in self.sources if source.stage == stage]

    def get_unprocessed_sources(self) -> list[DocumentSource]:
        """Get all unprocessed sources.

        Returns:
            List[DocumentSource]: Unprocessed sources.
        """
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
        """Get all document chunks across all documents.

        Returns:
            List[DocumentChunk]: All document chunks.
        """
        chunks = []
        for doc in self.documents:
            chunks.extend(doc.chunks)
        return chunks

    def get_all_langchain_documents(self) -> list[LCDocument]:
        """Get all documents as LangChain Documents.

        Returns:
            List[LCDocument]: All documents as LangChain Documents.
        """
        return [doc.to_langchain() for doc in self.documents]

    def get_all_chunks_as_langchain(self) -> list[LCDocument]:
        """Get all chunks as LangChain Documents.

        Returns:
            List[LCDocument]: All chunks as LangChain Documents.
        """
        lc_docs = []
        for doc in self.documents:
            lc_docs.extend(doc.get_chunks_as_langchain())
        return lc_docs

    def add_message(self, role: str, content: str) -> None:
        """Add a message to the agent conversation.

        Args:
            role: The role of the message sender.
            content: The content of the message.
        """
        self.messages.append(
            {
                "role": role,
                "content": content,
                "timestamp": datetime.datetime.now().isoformat(),
            }
        )

    def mark_processing_complete(self) -> None:
        """Mark document processing as complete."""
        self.processing_stats.complete()

    @property
    def all_sources_processed(self) -> bool:
        """Check if all sources have been processed.

        Returns:
            bool: True if all sources have been processed.
        """
        for source in self.sources:
            if source.stage not in [ProcessingStage.COMPLETED, ProcessingStage.FAILED]:
                return False
        return True

    @property
    def has_errors(self) -> bool:
        """Check if there are any errors.

        Returns:
            bool: True if there are any errors.
        """
        return len(self.errors) > 0 or any(
            source.stage == ProcessingStage.FAILED for source in self.sources
        )

    @property
    def has_documents(self) -> bool:
        """Check if there are any documents.

        Returns:
            bool: True if there are any documents.
        """
        return len(self.documents) > 0

    @property
    def total_chunks(self) -> int:
        """Get the total number of chunks.

        Returns:
            int: Total number of chunks.
        """
        return sum(doc.chunk_count for doc in self.documents)

    @property
    def source_types(self) -> set[DocumentSourceType]:
        """Get the set of all source types in this state.

        Returns:
            Set[DocumentSourceType]: All source types.
        """
        return {source.source_type for source in self.sources}

    @property
    def document_formats(self) -> set[DocumentFormat]:
        """Get the set of all document formats in this state.

        Returns:
            Set[DocumentFormat]: All document formats.
        """
        return {doc.format for doc in self.documents}

    @property
    def summary(self) -> dict[str, Any]:
        """Get a summary of the state.

        Returns:
            Dict[str, Any]: Summary of the state.
        """
        return {
            "sources": self.processing_stats.total_sources,
            "processed_sources": self.processing_stats.processed_sources,
            "failed_sources": self.processing_stats.failed_sources,
            "documents": self.processing_stats.total_documents,
            "chunks": self.processing_stats.total_chunks,
            "tokens": self.processing_stats.total_tokens,
            "collections": len(self.collections),
            "errors": self.processing_stats.errors_count,
            "processing_time": self.processing_stats.processing_time_seconds,
            "is_complete": self.processing_stats.is_complete,
        }


# ===== Converter Functions =====


def lc_documents_to_document_collection(
    lc_docs: list[LCDocument], collection_name: str, description: str | None = None
) -> DocumentCollection:
    """Convert a list of LangChain Documents to a DocumentCollection.

    Args:
        lc_docs: List of LangChain Documents.
        collection_name: Name for the collection.
        description: Optional description of the collection.

    Returns:
        DocumentCollection: A new DocumentCollection with converted documents.
    """
    collection = DocumentCollection(name=collection_name, description=description)

    for lc_doc in lc_docs:
        doc = Document.from_langchain(lc_doc)
        collection.add_document(doc)

    return collection


def documents_to_langchain(docs: list[Document]) -> list[LCDocument]:
    """Convert a list of Documents to LangChain Documents.

    Args:
        docs: List of Documents.

    Returns:
        List[LCDocument]: List of LangChain Documents.
    """
    return [doc.to_langchain() for doc in docs]


def chunks_to_langchain(chunks: list[DocumentChunk]) -> list[LCDocument]:
    """Convert a list of DocumentChunks to LangChain Documents.

    Args:
        chunks: List of DocumentChunks.

    Returns:
        List[LCDocument]: List of LangChain Documents.
    """
    return [chunk.to_langchain() for chunk in chunks]
