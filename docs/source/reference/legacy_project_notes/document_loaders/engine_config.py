"""Document Loader Engine Configuration.

This module defines the configuration model for the DocumentLoaderEngine.
It provides type definitions and validation for engine configuration.
"""

from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator, model_validator


class EngineType(str, Enum):
    """Engine type classification."""

    DOCUMENT_LOADER = "document_loader"
    VECTOR_STORE = "vector_store"
    RETRIEVER = "retriever"
    LLM = "llm"
    CHAT_MODEL = "chat_model"
    EMBEDDING = "embedding"
    TEXT_SPLITTER = "text_splitter"
    TOOL = "tool"
    AGENT = "agent"


class DocumentLoaderConfig(BaseModel):
    """Configuration for the DocumentLoaderEngine.

    This model defines the configuration parameters for the document loader engine,
    including source type specification, loader selection, and various options.
    """

    # Engine type
    engine_type: EngineType = Field(
        default=EngineType.DOCUMENT_LOADER, description="Type of the engine"
    )

    # Source settings
    source_type: str | None = Field(
        default=None,
        description="Explicit source type to use (auto-detected if not provided)",
    )

    # Loader settings
    loader_name: str | None = Field(
        default=None,
        description="Name of the document loader to use (auto-detected if not provided)",
    )

    # Loading options
    recursive: bool = Field(
        default=True, description="Whether to recursively load from directory sources"
    )

    max_documents: int | None = Field(
        default=None,
        description="Maximum number of documents to load (None for unlimited)",
    )

    use_async: bool = Field(
        default=False, description="Whether to use async loading if available"
    )

    # Loading preferences
    loader_preference: Literal["speed", "quality", "balanced"] | None = Field(
        default="balanced",
        description="Preference for loader selection when multiple are available",
    )

    # Additional configuration
    loader_options: dict[str, Any] = Field(
        default_factory=dict, description="Configuration parameters for the loader"
    )

    # Credential management
    credential_sources: list[str] = Field(
        default_factory=list,
        description="Sources to use for credential lookup (environment, keyring, etc.)",
    )

    # Error handling
    raise_on_error: bool = Field(
        default=True, description="Whether to raise exceptions on loading errors"
    )

    @model_validator(mode="after")
    def validate_loader_preference(self) -> "DocumentLoaderConfig":
        """Validate loader preference if specified."""
        if self.loader_preference not in (None, "speed", "quality", "balanced"):
            raise ValueError(
                f"Invalid loader_preference: {self.loader_preference}. "
                "Must be one of: 'speed', 'quality', 'balanced', or None"
            )
        return self

    @field_validator("max_documents")
    @classmethod
    def validate_max_documents(cls, v: int | None) -> int | None:
        """Validate max_documents if specified."""
        if v is not None and v <= 0:
            raise ValueError("max_documents must be a positive integer or None")
        return v


class DocumentLoaderInput(BaseModel):
    """Input model for the DocumentLoaderEngine.

    This model defines the input parameters for document loading operations.
    It supports various input types including strings, paths, and dictionaries.
    """

    # Primary input - can be a string path, dictionary of parameters, etc.
    source: str | dict[str, Any] = Field(
        ...,
        description="Source to load documents from (path, URL, or source configuration)",
    )

    # Optional overrides
    source_type: str | None = Field(
        default=None, description="Override source type for this invocation"
    )

    loader_name: str | None = Field(
        default=None, description="Override loader name for this invocation"
    )

    loader_options: dict[str, Any] = Field(
        default_factory=dict, description="Additional options for the loader"
    )

    # Include filters
    include_metadata: bool = Field(
        default=True, description="Whether to include metadata in the loaded documents"
    )

    include_patterns: list[str] = Field(
        default_factory=list,
        description="Glob patterns for files to include (for directory sources)",
    )

    exclude_patterns: list[str] = Field(
        default_factory=list,
        description="Glob patterns for files to exclude (for directory sources)",
    )


class DocumentMetadata(BaseModel):
    """Metadata for a document.

    This model defines the standard metadata for documents loaded by the engine.
    It captures source information, content details, and processing metadata.
    """

    # Source information
    source: str = Field(..., description="Original source of the document")
    source_type: str = Field(..., description="Type of the source")

    # File information (if applicable)
    file_path: str | None = Field(None, description="Path to the file")
    file_type: str | None = Field(None, description="Type of the file")
    file_size: int | None = Field(None, description="Size of the file in bytes")

    # URL information (if applicable)
    url: str | None = Field(None, description="URL of the document")
    domain: str | None = Field(None, description="Domain of the URL")

    # Content information
    content_type: str | None = Field(None, description="MIME type of the content")
    language: str | None = Field(None, description="Detected language of the content")

    # Document structure
    page_number: int | None = Field(
        None, description="Page number in multi-page document"
    )
    total_pages: int | None = Field(None, description="Total number of pages")

    # Processing information
    loader_name: str = Field(..., description="Name of the loader used")
    load_time: float | None = Field(
        None, description="Time taken to load the document in seconds"
    )

    # Custom metadata
    custom: dict[str, Any] = Field(
        default_factory=dict, description="Custom metadata fields"
    )


class DocumentLoaderOutput(BaseModel):
    """Output model for the DocumentLoaderEngine.

    This model defines the output of document loading operations, including
    the loaded documents and operation metadata.
    """

    # The loaded documents (simplified for this example)
    documents: list[dict[str, Any]] = Field(
        default_factory=list, description="Loaded documents with content and metadata"
    )

    # Operation metadata
    total_documents: int = Field(0, description="Total number of documents loaded")

    operation_time: float = Field(
        0.0, description="Time taken for the operation in seconds"
    )

    source_type: str = Field(..., description="Source type that was used")

    loader_name: str = Field(..., description="Loader that was used")

    # Error information
    errors: list[dict[str, Any]] = Field(
        default_factory=list, description="Errors encountered during loading"
    )

    has_errors: bool = Field(False, description="Whether any errors were encountered")

    # Source information
    original_source: str = Field(..., description="Original source that was loaded")


# Export all models
__all__ = [
    "DocumentLoaderConfig",
    "DocumentLoaderInput",
    "DocumentLoaderOutput",
    "DocumentMetadata",
    "EngineType",
]
