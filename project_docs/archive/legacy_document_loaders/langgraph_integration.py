"""LangGraph integration for Document Loaders.

This module demonstrates how to integrate the document loader system with LangGraph
for production use, including proper error handling, authentication, and multi-source loading.
"""

import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any

from langgraph.graph import StateGraph
from pydantic import BaseModel, Field, validator

# Import our document loader components
from .auto_loader_factory import analyze_path_and_suggest_loader, create_document_loader
from .source_implementation import (
    CredentialManager,
)

# Configure logging
logger = logging.getLogger(__name__)


# Source definition with authentication
class DocumentSource(BaseModel):
    """A document source with path and configuration information.

    This represents any source that can be loaded, including files, URLs,
    databases, APIs, and cloud storage.
    """

    # Required fields
    path: str

    # Optional configuration
    source_type: str | None = None
    loading_strategy: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)

    # Authentication
    credentials: dict[str, Any] | None = None
    require_auth: bool = False

    # Processing options
    chunk: bool = False
    chunk_size: int = 1000
    chunk_overlap: int = 200

    @validator("path")
    def path_must_not_be_empty(self, v):
        if not v.strip():
            raise ValueError("Path cannot be empty")
        return v


# Document model
class LoadedDocument(BaseModel):
    """A document loaded from a source.

    Contains the content, metadata about the source, and optional page info.
    """

    # Content
    content: str

    # Source information
    source_path: str
    source_type: str | None = None

    # Metadata
    metadata: dict[str, Any] = Field(default_factory=dict)

    # Page or segment info (for multi-page documents)
    page_number: int | None = None
    total_pages: int | None = None

    # Chunk info (if document was chunked)
    chunk_id: int | None = None
    total_chunks: int | None = None


# Error information
class LoaderError(BaseModel):
    """Error information for document loading."""

    source_path: str
    error_type: str
    error_message: str
    recoverable: bool = False
    retries: int = 0
    max_retries: int = 3

    @property
    def can_retry(self) -> bool:
        return self.recoverable and self.retries < self.max_retries


# State for the document loader graph
class DocumentLoaderState(BaseModel):
    """State for document loader graph.

    Tracks sources, loaded documents, errors, and processing status.
    """

    # Input
    sources: list[DocumentSource] = Field(default_factory=list)

    # Processing state
    pending_sources: list[DocumentSource] = Field(default_factory=list)
    in_progress_sources: list[DocumentSource] = Field(default_factory=list)
    completed_sources: list[DocumentSource] = Field(default_factory=list)

    # Output
    documents: list[LoadedDocument] = Field(default_factory=list)
    errors: list[LoaderError] = Field(default_factory=list)
    analysis_results: list[dict[str, Any]] = Field(default_factory=list)

    # Authentication
    credential_manager: Any | None = None

    # Processing options
    parallel_loading: bool = True
    max_workers: int = 4

    @property
    def all_sources_processed(self) -> bool:
        """Check if all sources have been processed."""
        return len(self.pending_sources) == 0 and len(self.in_progress_sources) == 0

    @property
    def has_errors(self) -> bool:
        """Check if there are any errors."""
        return len(self.errors) > 0

    @property
    def has_retryable_errors(self) -> bool:
        """Check if there are any retryable errors."""
        return any(error.can_retry for error in self.errors)


# Graph nodes


def initialize_state(state: DocumentLoaderState) -> DocumentLoaderState:
    """Initialize the state for document loading.

    Sets up credential manager if needed and moves sources to pending.
    """
    # Initialize credential manager if we have credentials
    if state.credential_manager is None and any(
        source.credentials for source in state.sources
    ):
        # Create a credential manager that can handle all types of credentials
        state.credential_manager = CredentialManager([])

        # Add credentials from sources
        for source in state.sources:
            if source.credentials:
                for cred_name, cred_value in source.credentials.items():
                    state.credential_manager.store_credential(cred_name, cred_value)

    # Move all sources to pending
    pending_sources = state.sources.copy()

    return DocumentLoaderState(
        sources=state.sources,
        pending_sources=pending_sources,
        in_progress_sources=[],
        completed_sources=[],
        documents=state.documents,
        errors=state.errors,
        analysis_results=state.analysis_results,
        credential_manager=state.credential_manager,
        parallel_loading=state.parallel_loading,
        max_workers=state.max_workers,
    )


def analyze_sources(state: DocumentLoaderState) -> DocumentLoaderState:
    """Analyze all pending sources to determine appropriate loaders.

    This helps validate sources before attempting to load them.
    """
    analysis_results = state.analysis_results.copy()
    pending_sources = state.pending_sources.copy()
    errors = state.errors.copy()

    for source in state.pending_sources:
        try:
            # Analyze the path
            analysis = analyze_path_and_suggest_loader(source.path)

            # Update source with detected type if not specified
            if not source.source_type and analysis["matches"]:
                source.source_type = analysis["matches"][0]["source_type"]

            analysis_results.append(
                {
                    "path": source.path,
                    "source_type": source.source_type,
                    "analysis": analysis,
                }
            )
        except Exception as e:
            logger.exception(f"Error analyzing source {source.path}: {e!s}")

            # Record the error
            errors.append(
                LoaderError(
                    source_path=source.path,
                    error_type="AnalysisError",
                    error_message=str(e),
                    recoverable=False,
                )
            )

            # Remove from pending sources
            pending_sources.remove(source)

    return DocumentLoaderState(
        sources=state.sources,
        pending_sources=pending_sources,
        in_progress_sources=state.in_progress_sources,
        completed_sources=state.completed_sources,
        documents=state.documents,
        errors=errors,
        analysis_results=analysis_results,
        credential_manager=state.credential_manager,
        parallel_loading=state.parallel_loading,
        max_workers=state.max_workers,
    )


def load_single_source(
    source: DocumentSource, credential_manager: CredentialManager | None = None
) -> list[LoadedDocument] | LoaderError:
    """Load documents from a single source.

    This is a helper function for load_documents.
    """
    try:
        # Create document loader
        loader = create_document_loader(
            path=source.path,
            strategy=source.loading_strategy,
            credential_manager=credential_manager,
            metadata=source.metadata,
        )

        # Load documents
        loaded_docs = loader.load()

        # Convert to our document model
        documents = []
        for _i, doc in enumerate(loaded_docs):
            # Extract content and metadata
            content = doc.page_content if hasattr(doc, "page_content") else str(doc)
            metadata = doc.metadata if hasattr(doc, "metadata") else {}

            # Add source information to metadata
            if "source" not in metadata:
                metadata["source"] = source.path

            # Create document
            document = LoadedDocument(
                content=content,
                source_path=source.path,
                source_type=source.source_type,
                metadata=metadata,
            )

            documents.append(document)

        return documents

    except Exception as e:
        logger.exception(f"Error loading source {source.path}: {e!s}")

        # Determine if error is recoverable
        recoverable = False
        if (
            "auth" in str(e).lower()
            or "credentials" in str(e).lower()
            or "timeout" in str(e).lower()
            or "connection" in str(e).lower()
        ):
            recoverable = True

        return LoaderError(
            source_path=source.path,
            error_type=type(e).__name__,
            error_message=str(e),
            recoverable=recoverable,
        )


def load_documents_parallel(state: DocumentLoaderState) -> DocumentLoaderState:
    """Load documents from all pending sources in parallel."""
    documents = state.documents.copy()
    errors = state.errors.copy()
    completed_sources = state.completed_sources.copy()
    in_progress_sources = []

    # Move all pending sources to in-progress
    in_progress_sources = state.pending_sources.copy()

    # Use thread pool for parallel loading
    with ThreadPoolExecutor(max_workers=state.max_workers) as executor:
        # Submit all loading tasks
        future_to_source = {
            executor.submit(
                load_single_source, source, state.credential_manager
            ): source
            for source in in_progress_sources
        }

        # Process results as they complete
        for future in as_completed(future_to_source):
            source = future_to_source[future]
            try:
                result = future.result()

                # Handle result
                if isinstance(result, LoaderError):
                    errors.append(result)
                else:
                    documents.extend(result)
                    completed_sources.append(source)

                # Remove from in-progress
                in_progress_sources.remove(source)

            except Exception as e:
                logger.exception(f"Unexpected error processing {source.path}: {e!s}")
                errors.append(
                    LoaderError(
                        source_path=source.path,
                        error_type="ProcessingError",
                        error_message=str(e),
                        recoverable=False,
                    )
                )
                in_progress_sources.remove(source)

    return DocumentLoaderState(
        sources=state.sources,
        pending_sources=[],  # All moved to in-progress
        in_progress_sources=[],  # All processed
        completed_sources=completed_sources,
        documents=documents,
        errors=errors,
        analysis_results=state.analysis_results,
        credential_manager=state.credential_manager,
        parallel_loading=state.parallel_loading,
        max_workers=state.max_workers,
    )


def load_documents_sequential(state: DocumentLoaderState) -> DocumentLoaderState:
    """Load documents from all pending sources sequentially."""
    documents = state.documents.copy()
    errors = state.errors.copy()
    completed_sources = state.completed_sources.copy()
    pending_sources = state.pending_sources.copy()

    # Process each source sequentially
    for source in list(pending_sources):
        # Move to in-progress
        pending_sources.remove(source)

        # Load documents
        result = load_single_source(source, state.credential_manager)

        # Handle result
        if isinstance(result, LoaderError):
            errors.append(result)
        else:
            documents.extend(result)
            completed_sources.append(source)

    return DocumentLoaderState(
        sources=state.sources,
        pending_sources=pending_sources,
        in_progress_sources=[],
        completed_sources=completed_sources,
        documents=documents,
        errors=errors,
        analysis_results=state.analysis_results,
        credential_manager=state.credential_manager,
        parallel_loading=state.parallel_loading,
        max_workers=state.max_workers,
    )


def retry_failed_sources(state: DocumentLoaderState) -> DocumentLoaderState:
    """Retry loading sources that had recoverable errors."""
    pending_sources = state.pending_sources.copy()
    errors = []

    # Find retryable errors
    for error in state.errors:
        if error.can_retry:
            # Find the source for this error
            source = next(
                (s for s in state.sources if s.path == error.source_path), None
            )
            if source:
                # Increment retry count
                error.retries += 1
                # Add back to pending
                pending_sources.append(source)
            else:
                # Keep the error if source not found
                errors.append(error)
        else:
            # Keep non-retryable errors
            errors.append(error)

    return DocumentLoaderState(
        sources=state.sources,
        pending_sources=pending_sources,
        in_progress_sources=state.in_progress_sources,
        completed_sources=state.completed_sources,
        documents=state.documents,
        errors=errors,
        analysis_results=state.analysis_results,
        credential_manager=state.credential_manager,
        parallel_loading=state.parallel_loading,
        max_workers=state.max_workers,
    )


def process_documents(state: DocumentLoaderState) -> dict[str, Any]:
    """Final processing and summarization of loaded documents.

    Returns the final state with processing statistics.
    """
    # Calculate statistics
    stats = {
        "total_sources": len(state.sources),
        "successful_sources": len(state.completed_sources),
        "failed_sources": len(state.errors),
        "total_documents": len(state.documents),
        "total_tokens": sum(len(doc.content.split()) for doc in state.documents),
        "source_types": {},
    }

    # Count by source type
    for doc in state.documents:
        source_type = doc.source_type or "unknown"
        if source_type not in stats["source_types"]:
            stats["source_types"][source_type] = 0
        stats["source_types"][source_type] += 1

    # Return final state with stats
    return {"documents": state.documents, "errors": state.errors, "stats": stats}


# Router functions for conditional execution
def route_by_loading_method(state: DocumentLoaderState) -> str:
    """Route to parallel or sequential loading based on configuration."""
    return "load_parallel" if state.parallel_loading else "load_sequential"


def check_for_retries(state: DocumentLoaderState) -> str:
    """Check if there are retryable errors to process."""
    if state.has_retryable_errors:
        return "retry_sources"
    return "process_documents"


# Create the document loader graph
def create_document_loader_graph() -> Any:
    """Create a LangGraph for document loading with error handling and retries."""
    workflow = StateGraph(DocumentLoaderState)

    # Add nodes
    workflow.add_node("initialize", initialize_state)
    workflow.add_node("analyze_sources", analyze_sources)
    workflow.add_node("load_parallel", load_documents_parallel)
    workflow.add_node("load_sequential", load_documents_sequential)
    workflow.add_node("retry_sources", retry_failed_sources)
    workflow.add_node("process_documents", process_documents)

    # Add conditional edges
    workflow.add_conditional_edges(
        "initialize",
        route_by_loading_method,
        {"load_parallel": "load_parallel", "load_sequential": "load_sequential"},
    )

    # Add regular edges
    workflow.add_edge("analyze_sources", "initialize")
    workflow.add_edge("load_parallel", check_for_retries)
    workflow.add_edge("load_sequential", check_for_retries)
    workflow.add_edge("retry_sources", route_by_loading_method)

    # Set entrypoint
    workflow.set_entry_point("analyze_sources")

    # Set conditional edge for retries or completion
    workflow.add_conditional_edges(
        "retry_sources",
        check_for_retries,
        {"retry_sources": "retry_sources", "process_documents": "process_documents"},
    )

    # Compile
    return workflow.compile()


# Example function to demonstrate usage
def load_documents_from_various_sources(
    sources: list[dict[str, Any]], parallel: bool = True, max_workers: int = 4
) -> dict[str, Any]:
    """Load documents from various sources using the document loader graph.

    Args:
        sources: List of source configurations
        parallel: Whether to load in parallel
        max_workers: Maximum number of parallel workers

    Returns:
        Dictionary with loaded documents, errors, and statistics
    """
    # Convert sources to DocumentSource objects
    source_objects = [DocumentSource(**source) for source in sources]

    # Create initial state
    initial_state = DocumentLoaderState(
        sources=source_objects, parallel_loading=parallel, max_workers=max_workers
    )

    # Create and run the graph
    document_loader_graph = create_document_loader_graph()
    result = document_loader_graph.invoke(initial_state)

    return result


# Example usage
if __name__ == "__main__":
    # Example sources
    example_sources = [
        {"path": "document.pdf", "loading_strategy": "fast"},
        {"path": "https://example.com", "source_type": "WebPageSource"},
        {
            "path": "s3://my-bucket/data.json",
            "credentials": {
                "aws_access_key_id": "YOUR_KEY",
                "aws_secret_access_key": "YOUR_SECRET",
            },
        },
        {"path": "https://github.com/user/repo", "require_auth": True},
    ]

    # Load documents
    result = load_documents_from_various_sources(example_sources)

    # Print summary
