"""Document Loader Engine for pure document loading without splitting.

This module provides the DocumentLoaderEngine that handles only document loading
from various sources and returns raw documents in DocumentState format.
"""

import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from langchain.schema import Document
from pydantic import BaseModel, Field

from haive.core.common.config.runnable import RunnableConfig
from haive.core.engine.base.base import InvokableEngine
from haive.core.engine.base.types import EngineType
from haive.core.engine.document.config import (
    DocumentSourceType,
    LoaderPreference,
    ProcessedDocument,
)
from haive.core.schema.prebuilt.document_state import DocumentState

from .auto_loader import AutoLoader, AutoLoaderConfig


class DocumentLoaderConfig(BaseModel):
    """Configuration for document loader engine."""

    name: str = Field(default="document_loader", description="Engine name")
    loader_preference: LoaderPreference = Field(
        default=LoaderPreference.BALANCED,
        description="Preference for loader selection (speed vs quality)",
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

    # Caching
    enable_caching: bool = Field(default=False, description="Enable document caching")
    cache_ttl: int = Field(
        default=3600, ge=60, description="Cache time-to-live in seconds"
    )

    # Document identity options
    generate_document_ids: bool = Field(
        default=True, description="Whether to generate unique document IDs"
    )
    preserve_source_metadata: bool = Field(
        default=True, description="Whether to preserve original source metadata"
    )

    class Config:
        use_enum_values = True


class DocumentLoaderEngine(
    InvokableEngine[Union[str, Path, Dict[str, Any]], DocumentState]
):
    """Document loader engine for loading documents from various sources.

    This engine handles pure document loading without any splitting or transformation.
    It returns raw documents in DocumentState format with proper metadata and IDs.

    Examples:
        Basic usage::

            engine = DocumentLoaderEngine(config=DocumentLoaderConfig())
            result = engine.invoke("/path/to/document.pdf")

        With custom configuration::

            config = DocumentLoaderConfig(
                loader_preference=LoaderPreference.QUALITY,
                recursive=True,
                max_workers=8
            )
            engine = DocumentLoaderEngine(config=config)
            runnable = engine.create_runnable({"enable_caching": True})
            result = runnable.invoke("https://example.com/docs")
    """

    def __init__(self, config: Optional[DocumentLoaderConfig] = None):
        """Initialize the document loader engine.

        Args:
            config: Configuration for the loader engine
        """
        super().__init__()
        self.config = config or DocumentLoaderConfig()
        self.engine_type = EngineType.DOCUMENT_LOADER

        # Create auto loader with configuration
        auto_loader_config = AutoLoaderConfig(
            preference=self.config.loader_preference,
            max_concurrency=self.config.max_workers,
            enable_caching=self.config.enable_caching,
            cache_ttl=self.config.cache_ttl,
        )
        self.auto_loader = AutoLoader(config=auto_loader_config)

    def create_runnable(
        self, runnable_config: Optional[Dict[str, Any]] = None
    ) -> "DocumentLoaderEngine":
        """Create a runnable instance with optional configuration overrides.

        Args:
            runnable_config: Configuration overrides for this runnable

        Returns:
            New DocumentLoaderEngine instance with updated configuration
        """
        if runnable_config:
            # Merge configurations
            config_dict = self.config.model_dump()
            config_dict.update(runnable_config)

            # Create new config and engine
            new_config = DocumentLoaderConfig.model_validate(config_dict)
            return DocumentLoaderEngine(config=new_config)

        return self

    def invoke(
        self,
        input_data: Union[str, Path, Dict[str, Any], DocumentState],
        config: Optional[RunnableConfig] = None,
    ) -> DocumentState:
        """Load documents from the specified source.

        Args:
            input_data: Source path, URL, or configuration
            config: Optional runnable configuration

        Returns:
            DocumentState with loaded documents and metadata
        """
        start_time = time.time()

        try:
            # Extract source from input
            if isinstance(input_data, (str, Path)):
                source = str(input_data)
                loader_options = {}
            elif isinstance(input_data, dict):
                source = input_data.get("source")
                if not source:
                    raise ValueError("Dictionary input must contain 'source' key")
                loader_options = input_data.get("loader_options", {})
            elif isinstance(input_data, DocumentState):
                source = input_data.source
                if not source:
                    raise ValueError("DocumentState must contain source")
                loader_options = {}
            else:
                raise ValueError(f"Invalid input type: {type(input_data)}")

            # Load documents using AutoLoader
            result = self.auto_loader.load(
                source, **{**self.config.loader_options, **loader_options}
            )

            # Convert to our format and add metadata
            raw_documents = []
            processed_documents = []

            for doc_index, doc in enumerate(result.documents):
                # Generate unique document ID
                doc_id = f"doc_{doc_index}_{int(start_time)}"

                # Add loader metadata
                enhanced_metadata = {
                    **doc.metadata,
                    # Document identity
                    "document_id": doc_id,
                    "is_loaded": True,
                    "is_original": True,
                    "document_hierarchy_level": 0,
                    # Loader information
                    "loader_engine": "DocumentLoaderEngine",
                    "loader_name": result.loader_name or "auto_detected",
                    "loader_preference": self.config.loader_preference.value,
                    "loading_timestamp": start_time,
                    # Source information
                    "source": source,
                    "source_type": result.source_type or "auto_detected",
                    "original_source": source,
                    # Document characteristics
                    "document_length": len(doc.page_content),
                    "document_type": self._detect_document_type(doc),
                    # Processing flags
                    "is_split": False,
                    "is_transformed": False,
                    "is_child_document": False,
                }

                # Create enhanced raw document
                enhanced_doc = Document(
                    page_content=doc.page_content, metadata=enhanced_metadata
                )
                raw_documents.append(enhanced_doc)

                # Create processed document
                processed_doc = ProcessedDocument(
                    content=doc.page_content,
                    metadata=enhanced_metadata,
                    source_type=result.source_type,
                    loader_name=result.loader_name or "auto_detected",
                    character_count=len(doc.page_content),
                    word_count=len(doc.page_content.split()),
                    chunk_count=1,  # Original document is one chunk
                    chunks=[enhanced_doc],
                    format=self._detect_format(doc),
                    processing_time=0.0,  # Individual loading time
                )
                processed_documents.append(processed_doc)

            operation_time = time.time() - start_time

            # Create document state
            document_state = DocumentState(
                # Input configuration
                source=source,
                source_type=self._map_source_type(result.source_type),
                loader_preference=self.config.loader_preference,
                # Output data
                raw_documents=raw_documents,
                documents=processed_documents,
                total_documents=len(raw_documents),
                successful_documents=len(raw_documents),
                processing_stage="load_completed",
                # Workflow metadata
                workflow_metadata={
                    "loader_config": {
                        "loader_preference": self.config.loader_preference.value,
                        "recursive": self.config.recursive,
                        "max_workers": self.config.max_workers,
                        "enable_caching": self.config.enable_caching,
                    },
                    "loading_operation_time": operation_time,
                    "total_loaded_documents": len(raw_documents),
                    "auto_loader_result": {
                        "loader_name": result.loader_name,
                        "source_type": result.source_type,
                        "operation_time": result.operation_time,
                    },
                },
            )

            return document_state

        except Exception as e:
            operation_time = time.time() - start_time

            # Create error document state
            document_state = DocumentState(
                source=str(input_data) if hasattr(input_data, "__str__") else "unknown",
                processing_stage="load_failed",
                errors=[
                    {
                        "error": str(e),
                        "error_type": type(e).__name__,
                        "stage": "loading",
                        "timestamp": start_time,
                    }
                ],
                workflow_metadata={
                    "loader_error": {
                        "error": str(e),
                        "error_type": type(e).__name__,
                        "operation_time": operation_time,
                    }
                },
            )

            return document_state

    async def ainvoke(
        self,
        input_data: Union[str, Path, Dict[str, Any], DocumentState],
        config: Optional[RunnableConfig] = None,
    ) -> DocumentState:
        """Asynchronously load documents.

        Args:
            input_data: Source path, URL, or configuration
            config: Optional runnable configuration

        Returns:
            DocumentState with loaded documents and metadata
        """
        # For now, run synchronously in thread pool
        # TODO: Implement true async processing if needed
        import asyncio

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.invoke, input_data, config)

    def _detect_document_type(self, document: Document) -> str:
        """Detect document type from metadata or content."""
        # Check metadata first
        if "document_type" in document.metadata:
            return document.metadata["document_type"]

        # Check file extension
        source = document.metadata.get("source", "")
        if isinstance(source, str):
            if source.endswith((".pdf", ".PDF")):
                return "pdf"
            elif source.endswith((".docx", ".DOCX", ".doc", ".DOC")):
                return "word"
            elif source.endswith((".html", ".HTML", ".htm", ".HTM")):
                return "html"
            elif source.endswith((".md", ".MD", ".markdown")):
                return "markdown"
            elif source.endswith((".txt", ".TXT")):
                return "text"

        # Default
        return "unknown"

    def _detect_format(self, document: Document) -> Optional[str]:
        """Detect document format."""
        doc_type = self._detect_document_type(document)
        return doc_type if doc_type != "unknown" else None

    def _map_source_type(
        self, auto_loader_source_type: Optional[str]
    ) -> Optional[DocumentSourceType]:
        """Map auto loader source type to DocumentSourceType enum."""
        if not auto_loader_source_type:
            return None

        # Map common types
        mapping = {
            "file": DocumentSourceType.FILE,
            "url": DocumentSourceType.URL,
            "directory": DocumentSourceType.DIRECTORY,
            "api": DocumentSourceType.API,
        }

        return mapping.get(auto_loader_source_type.lower(), DocumentSourceType.UNKNOWN)


# Factory functions for common loading scenarios
def create_file_loader(
    loader_preference: LoaderPreference = LoaderPreference.BALANCED,
    enable_caching: bool = False,
) -> DocumentLoaderEngine:
    """Create a document loader engine optimized for file loading.

    Args:
        loader_preference: Preference for loader selection
        enable_caching: Whether to enable document caching

    Returns:
        DocumentLoaderEngine configured for file loading
    """
    config = DocumentLoaderConfig(
        loader_preference=loader_preference,
        recursive=False,
        parallel_processing=True,
        max_workers=4,
        enable_caching=enable_caching,
    )
    return DocumentLoaderEngine(config=config)


def create_directory_loader(
    loader_preference: LoaderPreference = LoaderPreference.BALANCED,
    max_workers: int = 8,
    include_patterns: Optional[List[str]] = None,
    exclude_patterns: Optional[List[str]] = None,
) -> DocumentLoaderEngine:
    """Create a document loader engine optimized for directory processing.

    Args:
        loader_preference: Preference for loader selection
        max_workers: Maximum number of worker threads
        include_patterns: Glob patterns for files to include
        exclude_patterns: Glob patterns for files to exclude

    Returns:
        DocumentLoaderEngine configured for directory processing
    """
    config = DocumentLoaderConfig(
        loader_preference=loader_preference,
        recursive=True,
        parallel_processing=True,
        max_workers=max_workers,
        include_patterns=include_patterns or [],
        exclude_patterns=exclude_patterns or [],
    )
    return DocumentLoaderEngine(config=config)


def create_web_loader(
    loader_preference: LoaderPreference = LoaderPreference.QUALITY,
    enable_caching: bool = True,
    cache_ttl: int = 3600,
) -> DocumentLoaderEngine:
    """Create a document loader engine optimized for web content.

    Args:
        loader_preference: Preference for loader selection
        enable_caching: Whether to enable document caching
        cache_ttl: Cache time-to-live in seconds

    Returns:
        DocumentLoaderEngine configured for web loading
    """
    config = DocumentLoaderConfig(
        loader_preference=loader_preference,
        recursive=False,
        parallel_processing=True,
        max_workers=2,  # Be gentle with web servers
        enable_caching=enable_caching,
        cache_ttl=cache_ttl,
    )
    return DocumentLoaderEngine(config=config)
