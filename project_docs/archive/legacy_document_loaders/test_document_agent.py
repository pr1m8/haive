"""Tests for the DocumentAgent class.

This module contains tests for the DocumentAgent class and related functionality.
"""

import os
import shutil
import tempfile
from collections.abc import Generator
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from pydantic import BaseModel

from .document_agent import (
    DocumentAgent,
    DocumentAgentOptions,
    create_directory_document_agent,
    create_document_agent,
    create_file_document_agent,
    create_web_document_agent,
)
from .document_state import (
    ChunkingOptions,
    ChunkingStrategy,
    Document,
    DocumentFormat,
    DocumentSource,
    DocumentSourceType,
    DocumentState,
    LoadingStrategy,
    ProcessingStage,
)


class MockDocument(BaseModel):
    """Mock document for testing."""

    page_content: str
    metadata: dict[str, Any]


class MockLoader:
    """Mock document loader for testing."""

    def __init__(self, documents: list[MockDocument]):
        self.documents = documents

    def load(self) -> list[MockDocument]:
        """Return mock documents."""
        return self.documents


@pytest.fixture
def test_dir() -> Generator[str, None, None]:
    """Create a temporary directory for test files."""
    temp_dir = tempfile.mkdtemp()
    try:
        yield temp_dir
    finally:
        shutil.rmtree(temp_dir)


@pytest.fixture
def test_files(test_dir: str) -> list[str]:
    """Create test files for document loading."""
    file_paths = []

    # Create a text file
    text_file = os.path.join(test_dir, "sample.txt")
    with open(text_file, "w") as f:
        f.write(
            "This is a test document.\n\nIt has multiple paragraphs.\n\nEach paragraph tests chunking."
        )
    file_paths.append(text_file)

    # Create a markdown file
    md_file = os.path.join(test_dir, "sample.md")
    with open(md_file, "w") as f:
        f.write(
            "# Sample Document\n\nThis is a markdown document.\n\n## Section\n\nIt has multiple sections."
        )
    file_paths.append(md_file)

    return file_paths


@pytest.fixture
def mock_loader_patch() -> Generator[MagicMock, None, None]:
    """Patch the get_loader_for_source function."""
    with patch(
        "haive.project_notes.document_loaders.document_agent.get_loader_for_source"
    ) as mock:
        yield mock


class TestDocumentAgent:
    """Tests for the DocumentAgent class."""

    def test_init(self):
        """Test initialization of DocumentAgent."""
        # Test with default parameters
        agent = DocumentAgent()
        assert isinstance(agent.state, DocumentState)
        assert isinstance(agent.options, DocumentAgentOptions)

        # Test with custom options
        options = DocumentAgentOptions(
            parallel_processing=False, max_workers=2, skip_errors=False
        )
        agent = DocumentAgent(options=options)
        assert agent.options.parallel_processing is False
        assert agent.options.max_workers == 2
        assert agent.options.skip_errors is False

        # Test with custom state schema
        state = DocumentState()
        agent = DocumentAgent(state_schema=state)
        assert agent.state is state

    def test_add_source(self):
        """Test adding a document source."""
        agent = DocumentAgent()

        # Add a source
        source = agent.add_source("test.txt")
        assert isinstance(source, DocumentSource)
        assert source.path == "test.txt"
        assert source.stage == ProcessingStage.INITIALIZED

        # Check that the source was added to the state
        state = agent.state
        assert isinstance(state, DocumentState)
        assert len(state.sources) == 1
        assert state.sources[0] is source
        assert state.processing_stats.total_sources == 1

        # Add another source with custom parameters
        source2 = agent.add_source(
            "test2.pdf", source_type=DocumentSourceType.FILE, format=DocumentFormat.PDF
        )
        assert source2.path == "test2.pdf"
        assert source2.source_type == DocumentSourceType.FILE
        assert source2.format == DocumentFormat.PDF
        assert len(state.sources) == 2
        assert state.processing_stats.total_sources == 2

    def test_add_sources(self):
        """Test adding multiple document sources."""
        agent = DocumentAgent()

        # Add multiple sources
        paths = ["test1.txt", "test2.pdf", "test3.html"]
        sources = agent.add_sources(paths)

        # Check that sources were added
        assert len(sources) == 3
        assert [s.path for s in sources] == paths

        # Check that sources were added to the state
        state = agent.state
        assert isinstance(state, DocumentState)
        assert len(state.sources) == 3
        assert state.processing_stats.total_sources == 3

    def test_analyze_source(self):
        """Test analyzing document sources."""
        agent = DocumentAgent()

        # Add sources with different types
        agent.add_source("test.txt")
        agent.add_source("https://example.com")
        agent.add_source("data:text/plain,content")

        # Mock the analyze_path function
        with patch(
            "haive.project_notes.document_loaders.document_agent.analyze_path"
        ) as mock_analyze:
            # Configure mock to return different values for each source
            mock_analyze.side_effect = [
                MagicMock(
                    source_type=DocumentSourceType.FILE,
                    document_format=DocumentFormat.TXT,
                    metadata={"size_bytes": 100},
                ),
                MagicMock(
                    source_type=DocumentSourceType.URL,
                    document_format=DocumentFormat.HTML,
                    metadata={"title": "Example"},
                ),
                MagicMock(
                    source_type=DocumentSourceType.TEXT,
                    document_format=DocumentFormat.TXT,
                    metadata={},
                ),
            ]

            # Run the analyze_source node
            state = agent.analyze_source(agent.state)

            # Check that sources were analyzed
            assert len(state.sources) == 3

            # Check first source
            assert state.sources[0].source_type == DocumentSourceType.FILE
            assert state.sources[0].format == DocumentFormat.TXT
            assert state.sources[0].metadata.size_bytes == 100
            assert state.sources[0].stage == ProcessingStage.QUEUED

            # Check second source
            assert state.sources[1].source_type == DocumentSourceType.URL
            assert state.sources[1].format == DocumentFormat.HTML
            assert state.sources[1].metadata.title == "Example"
            assert state.sources[1].stage == ProcessingStage.QUEUED

            # Check third source
            assert state.sources[2].source_type == DocumentSourceType.TEXT
            assert state.sources[2].format == DocumentFormat.TXT
            assert state.sources[2].stage == ProcessingStage.QUEUED

    def test_analyze_source_error(self):
        """Test error handling during source analysis."""
        agent = DocumentAgent(options=DocumentAgentOptions(skip_errors=True))

        # Add a source
        agent.add_source("test.txt")

        # Mock the analyze_path function to raise an exception
        with patch(
            "haive.project_notes.document_loaders.document_agent.analyze_path"
        ) as mock_analyze:
            mock_analyze.side_effect = Exception("Test error")

            # Run the analyze_source node
            state = agent.analyze_source(agent.state)

            # Check that the source failed
            assert state.sources[0].stage == ProcessingStage.FAILED
            assert state.sources[0].error is not None
            assert "Test error" in state.sources[0].error
            assert len(state.error_messages) == 1

    def test_load_documents(self, mock_loader_patch: MagicMock):
        """Test loading documents from sources."""
        agent = DocumentAgent()

        # Add sources
        file_source = agent.add_source("test.txt")
        file_source.stage = ProcessingStage.QUEUED
        file_source.source_type = DocumentSourceType.FILE
        file_source.format = DocumentFormat.TXT

        # Configure mock loader
        mock_loader = MockLoader(
            [
                MockDocument(
                    page_content="Document 1 content",
                    metadata={"source": "test.txt", "page": 1},
                ),
                MockDocument(
                    page_content="Document 2 content",
                    metadata={"source": "test.txt", "page": 2},
                ),
            ]
        )
        mock_loader_patch.return_value = mock_loader

        # Run the load_documents node
        state = agent.load_documents(agent.state)

        # Check that documents were loaded
        assert len(state.documents) == 2
        assert state.documents[0].content == "Document 1 content"
        assert state.documents[0].source_path == "test.txt"
        assert state.documents[0].source_type == DocumentSourceType.FILE
        assert state.documents[0].format == DocumentFormat.TXT
        assert state.documents[0].metadata["source"] == "test.txt"
        assert state.documents[0].metadata["page"] == 1

        assert state.documents[1].content == "Document 2 content"
        assert state.documents[1].metadata["page"] == 2

        # Check that source stage was updated
        assert file_source.stage == ProcessingStage.CHUNKING
        assert state.processing_stats.total_documents == 2

    def test_load_documents_no_chunking(self, mock_loader_patch: MagicMock):
        """Test loading documents without chunking."""
        agent = DocumentAgent()
        state = agent.state
        state.chunking_options.strategy = ChunkingStrategy.NONE

        # Add sources
        file_source = agent.add_source("test.txt")
        file_source.stage = ProcessingStage.QUEUED

        # Configure mock loader
        mock_loader = MockLoader(
            [
                MockDocument(
                    page_content="Document content", metadata={"source": "test.txt"}
                )
            ]
        )
        mock_loader_patch.return_value = mock_loader

        # Run the load_documents node
        state = agent.load_documents(state)

        # Check that source stage was updated to COMPLETED instead of CHUNKING
        assert file_source.stage == ProcessingStage.COMPLETED

    def test_load_documents_error(self, mock_loader_patch: MagicMock):
        """Test error handling during document loading."""
        agent = DocumentAgent(options=DocumentAgentOptions(skip_errors=True))

        # Add a source
        file_source = agent.add_source("test.txt")
        file_source.stage = ProcessingStage.QUEUED

        # Configure mock loader to raise an exception
        mock_loader_patch.side_effect = Exception("Loading error")

        # Run the load_documents node
        state = agent.load_documents(agent.state)

        # Check that the source failed
        assert file_source.stage == ProcessingStage.FAILED
        assert file_source.error is not None
        assert "Loading error" in file_source.error
        assert len(state.error_messages) == 1

    def test_load_documents_no_loader(self, mock_loader_patch: MagicMock):
        """Test handling when no loader is available."""
        agent = DocumentAgent(options=DocumentAgentOptions(skip_errors=True))

        # Add a source
        file_source = agent.add_source("test.txt")
        file_source.stage = ProcessingStage.QUEUED

        # Configure mock loader to return None
        mock_loader_patch.return_value = None

        # Run the load_documents node
        state = agent.load_documents(agent.state)

        # Check that the source failed
        assert file_source.stage == ProcessingStage.FAILED
        assert file_source.error is not None
        assert "No loader found" in file_source.error
        assert len(state.error_messages) == 1

    def test_chunk_documents_fixed_size(self):
        """Test chunking documents with fixed size strategy."""
        agent = DocumentAgent()
        state = agent.state

        # Create a document
        doc = Document(
            document_id="1",
            content="This is a test document with enough content to create multiple chunks. "
            "We need to ensure that it splits correctly and maintains proper context.",
            source_path="test.txt",
            source_type=DocumentSourceType.FILE,
            format=DocumentFormat.TXT,
        )
        state.documents.append(doc)

        # Add a source in CHUNKING stage
        source = DocumentSource(path="test.txt")
        source.stage = ProcessingStage.CHUNKING
        state.sources.append(source)

        # Configure chunking options
        state.chunking_options = ChunkingOptions(
            strategy=ChunkingStrategy.FIXED_SIZE, chunk_size=50, chunk_overlap=10
        )

        # Run the chunk_documents node
        state = agent.chunk_documents(state)

        # Check that document was chunked
        assert len(doc.chunks) > 0
        assert (
            doc.chunks[0].content
            == "This is a test document with enough content to create"
        )
        assert doc.chunks[0].document_id == "1"
        assert doc.chunks[0].metadata["chunk_index"] == 0
        assert doc.chunks[0].metadata["start"] == 0

        # Check for overlap in second chunk
        assert doc.chunks[1].content.startswith("create multiple")

        # Check that source stage was updated
        assert source.stage == ProcessingStage.COMPLETED

    def test_chunk_documents_paragraph(self):
        """Test chunking documents with paragraph strategy."""
        agent = DocumentAgent()
        state = agent.state

        # Create a document with paragraphs
        doc = Document(
            document_id="1",
            content="This is paragraph one.\n\nThis is paragraph two.\n\nThis is paragraph three.",
            source_path="test.txt",
            source_type=DocumentSourceType.FILE,
            format=DocumentFormat.TXT,
        )
        state.documents.append(doc)

        # Add a source in CHUNKING stage
        source = DocumentSource(path="test.txt")
        source.stage = ProcessingStage.CHUNKING
        state.sources.append(source)

        # Configure chunking options
        state.chunking_options = ChunkingOptions(strategy=ChunkingStrategy.PARAGRAPH)

        # Run the chunk_documents node
        state = agent.chunk_documents(state)

        # Check that document was chunked
        assert len(doc.chunks) == 3
        assert doc.chunks[0].content == "This is paragraph one."
        assert doc.chunks[1].content == "This is paragraph two."
        assert doc.chunks[2].content == "This is paragraph three."

        # Check that source stage was updated
        assert source.stage == ProcessingStage.COMPLETED

    def test_chunk_documents_sentence(self):
        """Test chunking documents with sentence strategy."""
        agent = DocumentAgent()
        state = agent.state

        # Create a document with sentences
        doc = Document(
            document_id="1",
            content="This is sentence one. This is sentence two! This is sentence three?",
            source_path="test.txt",
            source_type=DocumentSourceType.FILE,
            format=DocumentFormat.TXT,
        )
        state.documents.append(doc)

        # Add a source in CHUNKING stage
        source = DocumentSource(path="test.txt")
        source.stage = ProcessingStage.CHUNKING
        state.sources.append(source)

        # Configure chunking options
        state.chunking_options = ChunkingOptions(strategy=ChunkingStrategy.SENTENCE)

        # Run the chunk_documents node
        state = agent.chunk_documents(state)

        # Check that document was chunked
        assert len(doc.chunks) == 3
        assert doc.chunks[0].content == "This is sentence one."
        assert doc.chunks[1].content == "This is sentence two!"
        assert doc.chunks[2].content == "This is sentence three?"

        # Check that source stage was updated
        assert source.stage == ProcessingStage.COMPLETED

    def test_chunk_documents_error(self):
        """Test error handling during document chunking."""
        agent = DocumentAgent(options=DocumentAgentOptions(skip_errors=True))
        state = agent.state

        # Create a document
        doc = Document(document_id="1", content="Test content", source_path="test.txt")
        state.documents.append(doc)

        # Add a source in CHUNKING stage
        source = DocumentSource(path="test.txt")
        source.stage = ProcessingStage.CHUNKING
        state.sources.append(source)

        # Configure chunking options with an invalid strategy
        state.chunking_options = ChunkingOptions(
            strategy=ChunkingStrategy.CUSTOM  # Not implemented
        )

        # Mock the _chunk_fixed_size method to raise an exception
        with patch.object(
            agent, "_chunk_fixed_size", side_effect=Exception("Chunking error")
        ):
            # Run the chunk_documents node
            state = agent.chunk_documents(state)

            # Check that the source failed
            assert source.stage == ProcessingStage.FAILED
            assert source.error is not None
            assert "Chunking error" in source.error
            assert len(state.error_messages) == 1

    def test_finalize_processing(self):
        """Test finalizing document processing."""
        agent = DocumentAgent()
        state = agent.state

        # Add some documents with chunks
        doc1 = Document(
            document_id="1",
            content="Document 1 content with 100 characters " + "x" * 60,
            source_path="test1.txt",
        )
        doc1.add_chunk("Chunk 1.1", {"index": 0})
        doc1.add_chunk("Chunk 1.2", {"index": 1})

        doc2 = Document(
            document_id="2", content="Document 2 content", source_path="test2.txt"
        )
        doc2.add_chunk("Chunk 2.1", {"index": 0})

        state.documents.extend([doc1, doc2])

        # Run the finalize_processing node
        state = agent.finalize_processing(state)

        # Check that statistics were updated
        assert state.processing_stats.total_chunks == 3
        assert state.processing_stats.total_tokens > 0
        assert state.processing_stats.is_complete

    def test_document_agent_graph(self):
        """Test building the document agent graph."""
        agent = DocumentAgent()
        graph = agent.build_graph()

        # Check that graph was built correctly
        assert graph is not None

        # Unfortunately, we can't easily test the LangGraph structure
        # But we can verify the agent's state schema is correct
        assert agent.state_schema_cls == DocumentState

    def test_get_documents(self):
        """Test getting documents from the agent."""
        agent = DocumentAgent()
        state = agent.state

        # Add some documents
        doc1 = Document(document_id="1", content="Document 1", source_path="test1.txt")
        doc2 = Document(document_id="2", content="Document 2", source_path="test2.txt")
        state.documents.extend([doc1, doc2])

        # Get all documents
        docs = agent.get_documents()
        assert len(docs) == 2
        assert docs[0].document_id == "1"
        assert docs[1].document_id == "2"

        # Get document by ID
        doc = agent.get_document("1")
        assert doc is doc1

        # Get document by source
        docs = agent.get_documents_by_source("test1.txt")
        assert len(docs) == 1
        assert docs[0] is doc1

        # Get document by format
        doc1.format = DocumentFormat.TXT
        doc2.format = DocumentFormat.PDF
        docs = agent.get_documents_by_format(DocumentFormat.TXT)
        assert len(docs) == 1
        assert docs[0] is doc1

    def test_clear(self):
        """Test clearing the agent state."""
        agent = DocumentAgent()

        # Add some data to the state
        agent.add_source("test.txt")
        state = agent.state
        state.documents.append(
            Document(document_id="1", content="Document 1", source_path="test.txt")
        )

        # Clear the state
        agent.clear()

        # Check that state was cleared
        assert len(agent.state.sources) == 0
        assert len(agent.state.documents) == 0
        assert agent.state.processing_stats.total_sources == 0

    def test_create_document_agent(self):
        """Test creating a document agent with the factory function."""
        # Create with default options
        agent = create_document_agent()
        assert isinstance(agent, DocumentAgent)
        assert isinstance(agent.options, DocumentAgentOptions)

        # Create with custom options
        options = DocumentAgentOptions(parallel_processing=False, max_workers=2)
        agent = create_document_agent(options=options)
        assert agent.options is options

        # Create with sources
        agent = create_document_agent(sources=["test1.txt", "test2.txt"])
        assert len(agent.state.sources) == 2
        assert agent.state.sources[0].path == "test1.txt"
        assert agent.state.sources[1].path == "test2.txt"

    def test_create_file_document_agent(self):
        """Test creating a file document agent with the factory function."""
        agent = create_file_document_agent(
            file_paths=["test1.txt", "test2.txt"], chunk_size=2000, chunk_overlap=500
        )

        # Check that agent was configured correctly
        assert isinstance(agent, DocumentAgent)
        assert len(agent.state.sources) == 2
        assert agent.state.sources[0].path == "test1.txt"
        assert agent.state.sources[1].path == "test2.txt"

        # Check that chunking options were set
        assert (
            agent.options.default_chunking_options.strategy
            == ChunkingStrategy.FIXED_SIZE
        )
        assert agent.options.default_chunking_options.chunk_size == 2000
        assert agent.options.default_chunking_options.chunk_overlap == 500

        # Check that loading options were set
        assert agent.options.default_loading_options.strategy == LoadingStrategy.DIRECT

    def test_create_web_document_agent(self):
        """Test creating a web document agent with the factory function."""
        agent = create_web_document_agent(
            urls=["https://example.com", "https://test.com"]
        )

        # Check that agent was configured correctly
        assert isinstance(agent, DocumentAgent)
        assert len(agent.state.sources) == 2
        assert agent.state.sources[0].path == "https://example.com"
        assert agent.state.sources[1].path == "https://test.com"

        # Check that chunking options were set
        assert (
            agent.options.default_chunking_options.strategy
            == ChunkingStrategy.PARAGRAPH
        )

        # Check that loading options were set
        assert agent.options.default_loading_options.strategy == LoadingStrategy.DIRECT
        assert agent.options.default_loading_options.timeout_seconds == 120

    def test_create_directory_document_agent(self):
        """Test creating a directory document agent with the factory function."""
        agent = create_directory_document_agent(
            directory_paths=["/tmp/test1", "/tmp/test2"],
            include_patterns=["*.pdf"],
            exclude_patterns=["*.tmp"],
            recursive=True,
            recursive_depth=5,
        )

        # Check that agent was configured correctly
        assert isinstance(agent, DocumentAgent)
        assert len(agent.state.sources) == 2
        assert agent.state.sources[0].path == "/tmp/test1"
        assert agent.state.sources[1].path == "/tmp/test2"

        # Check that loading options were set
        assert (
            agent.options.default_loading_options.strategy == LoadingStrategy.RECURSIVE
        )
        assert agent.options.default_loading_options.recursive_depth == 5
        assert agent.options.default_loading_options.include_patterns == ["*.pdf"]
        assert agent.options.default_loading_options.exclude_patterns == ["*.tmp"]

        # Check that parallel processing is enabled
        assert agent.options.parallel_processing is True
        assert agent.options.max_workers == 8

    @pytest.mark.integration
    def test_integration_with_file(
        self, test_files: list[str], mock_loader_patch: MagicMock
    ):
        """Integration test with a real file."""
        file_path = test_files[0]  # Use the first test file

        # Configure mock loader
        mock_loader = MockLoader(
            [
                MockDocument(
                    page_content="Test content from file",
                    metadata={"source": file_path},
                )
            ]
        )
        mock_loader_patch.return_value = mock_loader

        # Create agent and add source
        agent = create_file_document_agent(
            file_paths=[file_path],
            chunking_strategy=ChunkingStrategy.FIXED_SIZE,
            chunk_size=20,
            chunk_overlap=5,
        )

        # Run the full workflow manually
        state = agent.analyze_source(agent.state)
        state = agent.load_documents(state)
        state = agent.chunk_documents(state)
        state = agent.finalize_processing(state)

        # Check that document was processed
        assert len(state.documents) == 1
        assert state.documents[0].content == "Test content from file"
        assert len(state.documents[0].chunks) > 0
        assert state.processing_stats.is_complete

        # Check that source was fully processed
        assert state.sources[0].stage == ProcessingStage.COMPLETED
        assert state.all_sources_processed
