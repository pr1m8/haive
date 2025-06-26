"""Test harness for document loading graph with multiple source types.

This module demonstrates how to use the document loader system in a LangGraph workflow
with various source types using placeholder paths.
"""

from typing import Any

from langgraph.graph import StateGraph
from pydantic import BaseModel, Field

# Import our document loader components
from .auto_loader_factory import (
    analyze_path_and_suggest_loader,
)
from .source_implementation import (
    CredentialManager,
)


# State models
class Source(BaseModel):
    """A document source with path and metadata."""

    path: str
    source_type: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    credentials: dict[str, Any] | None = None
    loading_strategy: str | None = None


class Document(BaseModel):
    """Placeholder for loaded document."""

    content: str
    metadata: dict[str, Any] = Field(default_factory=dict)
    source_path: str


class LoaderState(BaseModel):
    """State for document loader graph."""

    sources: list[Source] = Field(default_factory=list)
    documents: list[Document] = Field(default_factory=list)
    errors: list[dict[str, Any]] = Field(default_factory=list)
    analysis_results: list[dict[str, Any]] = Field(default_factory=list)


# Graph nodes
def analyze_sources(state: LoaderState) -> LoaderState:
    """Analyze source paths and determine appropriate loaders."""
    analysis_results = []

    for source in state.sources:
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
            analysis_results.append({"path": source.path, "error": str(e)})

    return LoaderState(
        sources=state.sources,
        documents=state.documents,
        errors=state.errors,
        analysis_results=analysis_results,
    )


def load_source_documents(state: LoaderState) -> LoaderState:
    """Load documents from all sources."""
    documents = state.documents.copy()
    errors = state.errors.copy()

    # Set up credential manager if needed
    has_credentials = any(source.credentials for source in state.sources)
    if has_credentials:
        CredentialManager([])

    # Process each source
    for source in state.sources:
        try:
            # In a real implementation, we would use the actual loader
            # Here we're creating placeholder documents for testing

            # Create a placeholder based on the source type
            if source.path.endswith(".pdf"):
                content = f"[PDF CONTENT FROM {source.path}]"
            elif source.path.endswith((".doc", ".docx")):
                content = f"[WORD DOCUMENT CONTENT FROM {source.path}]"
            elif source.path.endswith((".xls", ".xlsx")):
                content = f"[EXCEL CONTENT FROM {source.path}]"
            elif source.path.startswith("http"):
                content = f"[WEB CONTENT FROM {source.path}]"
            elif source.path.startswith("s3://"):
                content = f"[S3 CONTENT FROM {source.path}]"
            elif source.path.startswith("gs://"):
                content = f"[GCS CONTENT FROM {source.path}]"
            elif "github.com" in source.path:
                content = f"[GITHUB CONTENT FROM {source.path}]"
            elif source.path.endswith((".jpg", ".png")):
                content = f"[IMAGE CONTENT FROM {source.path}]"
            else:
                content = f"[GENERIC CONTENT FROM {source.path}]"

            # Create document with metadata
            doc = Document(
                content=content,
                metadata={
                    "source": source.path,
                    "source_type": source.source_type,
                    "strategy": source.loading_strategy,
                },
                source_path=source.path,
            )

            # Add source metadata if available
            if source.metadata:
                doc.metadata.update(source.metadata)

            documents.append(doc)

        except Exception as e:
            errors.append({"path": source.path, "error": str(e)})

    return LoaderState(
        sources=state.sources,
        documents=documents,
        errors=errors,
        analysis_results=state.analysis_results,
    )


# Create the graph
def create_document_loader_graph():
    """Create a document loader graph."""
    workflow = StateGraph(LoaderState)

    # Add nodes
    workflow.add_node("analyze_sources", analyze_sources)
    workflow.add_node("load_documents", load_source_documents)

    # Add edges
    workflow.add_edge("analyze_sources", "load_documents")

    # Set entrypoint
    workflow.set_entry_point("analyze_sources")

    # Compile
    return workflow.compile()


# Test function with various source types
def test_document_loader_graph():
    """Test the document loader graph with various source types."""
    # Create test sources
    sources = [
        Source(path="document.pdf", loading_strategy="fast"),
        Source(path="data.csv", metadata={"description": "CSV data file"}),
        Source(path="https://example.com", source_type="WebPageSource"),
        Source(path="s3://my-bucket/data.json"),
        Source(path="gs://my-bucket/image.jpg"),
        Source(path="postgresql://user:pass@localhost:5432/db"),
        Source(path="https://github.com/user/repo"),
        Source(path="https://huggingface.co/models/bert-base-uncased"),
        Source(path="image.jpg", loading_strategy="ocr"),
        Source(path="presentation.pptx"),
        Source(path="https://en.wikipedia.org/wiki/Python_(programming_language)"),
        Source(path="https://arxiv.org/abs/1706.03762"),
    ]

    # Create initial state
    initial_state = LoaderState(sources=sources)

    # Create and run the graph
    document_loader_graph = create_document_loader_graph()
    result = document_loader_graph.invoke(initial_state)

    # Display results

    for _i, analysis in enumerate(result.analysis_results):
        analysis.get("path", "unknown")
        analysis.get("source_type", "unknown")

    for _i, _doc in enumerate(result.documents):
        pass

    if result.errors:
        for _i, _error in enumerate(result.errors):
            pass

    return result


# Extended workflow with document processing
class ProcessingState(LoaderState):
    """Extended state with document processing."""

    processed_documents: list[Document] = Field(default_factory=list)
    chunks: list[dict[str, Any]] = Field(default_factory=list)


def process_documents(state: ProcessingState) -> ProcessingState:
    """Process documents (placeholder for actual processing)."""
    processed = []
    chunks = []

    for doc in state.documents:
        # Create a processed version (just a placeholder)
        processed_doc = Document(
            content=f"PROCESSED: {doc.content}",
            metadata=doc.metadata,
            source_path=doc.source_path,
        )
        processed.append(processed_doc)

        # Create chunks (just placeholders)
        for i in range(2):  # Create 2 chunks per document
            chunks.append(
                {
                    "text": f"Chunk {i+1} from {doc.source_path}",
                    "metadata": doc.metadata,
                }
            )

    return ProcessingState(
        sources=state.sources,
        documents=state.documents,
        errors=state.errors,
        analysis_results=state.analysis_results,
        processed_documents=processed,
        chunks=chunks,
    )


def create_full_processing_graph():
    """Create a full document processing graph."""
    workflow = StateGraph(ProcessingState)

    # Add nodes
    workflow.add_node("analyze_sources", analyze_sources)
    workflow.add_node("load_documents", load_source_documents)
    workflow.add_node("process_documents", process_documents)

    # Add edges
    workflow.add_edge("analyze_sources", "load_documents")
    workflow.add_edge("load_documents", "process_documents")

    # Set entrypoint
    workflow.set_entry_point("analyze_sources")

    # Compile
    return workflow.compile()


def test_full_processing_graph():
    """Test the full document processing graph."""
    # Create test sources
    sources = [
        Source(path="document.pdf", loading_strategy="fast"),
        Source(path="https://example.com", source_type="WebPageSource"),
        Source(path="s3://my-bucket/data.json"),
    ]

    # Create initial state
    initial_state = ProcessingState(sources=sources)

    # Create and run the graph
    processing_graph = create_full_processing_graph()
    result = processing_graph.invoke(initial_state)

    # Display results

    return result


if __name__ == "__main__":
    # Run the tests
    test_document_loader_graph()

    test_full_processing_graph()
