#!/usr/bin/env python
"""Tests for document processor adapters for transformers and splitters.

This module tests the functionality of the document processors in the document_processors.py
module, including transformer and splitter factories, document conversion, and processing
functions.
"""

import unittest

from document_processors import (
    SPLITTERS_AVAILABLE,
    TRANSFORMERS_AVAILABLE,
    SplitterFactory,
    TransformerFactory,
    document_to_langchain,
    documents_to_langchain_list,
    langchain_to_document,
    langchain_to_document_chunk,
    process_document,
    split_document,
    transform_document,
)
from document_state import (
    ChunkingOptions,
    ChunkingStrategy,
    Document,
    DocumentFormat,
    DocumentSourceType,
)

# Import LangChain Document for testing
from langchain_core.documents import Document as LCDocument


class TestDocumentAdapters(unittest.TestCase):
    """Tests for document adapter functions."""

    def setUp(self):
        """Set up test fixtures."""
        self.document = Document(
            document_id="test-doc-1",
            content="This is a test document with some content.",
            source_path="/path/to/test.txt",
            source_type=DocumentSourceType.FILE,
            format=DocumentFormat.TXT,
            metadata={"author": "Test Author", "keywords": ["test", "document"]},
        )

    def test_document_to_langchain(self):
        """Test converting a Document to a LangChain Document."""
        lc_doc = document_to_langchain(self.document)

        assert lc_doc.page_content == self.document.content
        assert lc_doc.metadata["source"] == self.document.source_path
        assert lc_doc.metadata["document_id"] == self.document.document_id
        assert lc_doc.metadata["author"] == "Test Author"
        assert lc_doc.metadata["keywords"] == ["test", "document"]

    def test_langchain_to_document(self):
        """Test updating a Document with content from a LangChain Document."""
        # Create a LangChain document with different content and metadata
        lc_doc = LCDocument(
            page_content="Updated content for the document.",
            metadata={
                "source": "/path/to/test.txt",
                "document_id": "test-doc-1",
                "author": "New Author",
                "new_field": "New Value",
            },
        )

        # Update the document
        updated_doc = langchain_to_document(lc_doc, self.document)

        # Check that the content was updated
        assert updated_doc.content == "Updated content for the document."

        # Check that metadata was updated correctly
        assert updated_doc.metadata["author"] == "New Author"
        assert updated_doc.metadata["new_field"] == "New Value"

        # Check that source and document_id were not overwritten
        assert updated_doc.source_path == "/path/to/test.txt"
        assert updated_doc.document_id == "test-doc-1"

    def test_langchain_to_document_chunk(self):
        """Test converting a LangChain Document to a DocumentChunk."""
        lc_doc = LCDocument(
            page_content="This is chunk content.",
            metadata={
                "source": "/path/to/test.txt",
                "document_id": "test-doc-1",
                "chunk_specific": "Chunk metadata",
            },
        )

        chunk = langchain_to_document_chunk(lc_doc, self.document, 3)

        assert chunk.content == "This is chunk content."
        assert chunk.document_id == "test-doc-1"
        assert chunk.chunk_index == 3
        assert chunk.metadata["chunk_specific"] == "Chunk metadata"
        assert chunk.metadata["chunk_index"] == 3

        # Check that source and document_id were not duplicated in metadata
        assert "source" not in chunk.metadata
        assert "document_id" not in chunk.metadata

    def test_documents_to_langchain_list(self):
        """Test converting a list of Documents to a list of LangChain Documents."""
        doc2 = Document(
            document_id="test-doc-2",
            content="Another test document.",
            source_path="/path/to/test2.txt",
            source_type=DocumentSourceType.FILE,
            format=DocumentFormat.TXT,
        )

        documents = [self.document, doc2]
        lc_docs = documents_to_langchain_list(documents)

        assert len(lc_docs) == 2
        assert lc_docs[0].page_content == "This is a test document with some content."
        assert lc_docs[1].page_content == "Another test document."
        assert lc_docs[0].metadata["document_id"] == "test-doc-1"
        assert lc_docs[1].metadata["document_id"] == "test-doc-2"


class TestSplitterFactory(unittest.TestCase):
    """Tests for the SplitterFactory."""

    def test_get_splitter_type(self):
        """Test getting the appropriate splitter type for different strategies."""
        # Skip test if splitters are not available
        if not SPLITTERS_AVAILABLE:
            self.skipTest("Core splitters not available")

        # Test strategy-based splitter types
        assert (
            SplitterFactory.get_splitter_type(ChunkingStrategy.FIXED_SIZE) is not None
        )
        assert SplitterFactory.get_splitter_type(ChunkingStrategy.RECURSIVE) is not None
        assert SplitterFactory.get_splitter_type(ChunkingStrategy.PARAGRAPH) is not None
        assert SplitterFactory.get_splitter_type(ChunkingStrategy.SENTENCE) is not None

        # Test format-specific splitter types
        assert (
            SplitterFactory.get_splitter_type(
                ChunkingStrategy.FIXED_SIZE, DocumentFormat.MARKDOWN
            )
            is not None
        )
        assert (
            SplitterFactory.get_splitter_type(
                ChunkingStrategy.FIXED_SIZE, DocumentFormat.HTML
            )
            is not None
        )

    def test_create_splitter(self):
        """Test creating splitters for different strategies."""
        # Skip test if splitters are not available
        if not SPLITTERS_AVAILABLE:
            self.skipTest("Core splitters not available")

        options = ChunkingOptions(
            chunk_size=500,
            chunk_overlap=50,
        )

        # Test creating different types of splitters
        fixed_splitter = SplitterFactory.create_splitter(
            ChunkingStrategy.FIXED_SIZE, options
        )
        recursive_splitter = SplitterFactory.create_splitter(
            ChunkingStrategy.RECURSIVE, options
        )
        paragraph_splitter = SplitterFactory.create_splitter(
            ChunkingStrategy.PARAGRAPH, options
        )

        assert fixed_splitter is not None
        assert recursive_splitter is not None
        assert paragraph_splitter is not None


class TestTransformerFactory(unittest.TestCase):
    """Tests for the TransformerFactory."""

    def test_get_transformer_type(self):
        """Test getting the appropriate transformer type for different formats."""
        # Skip test if transformers are not available
        if not TRANSFORMERS_AVAILABLE:
            self.skipTest("Core transformers not available")

        # HTML should have a transformer
        html_transformer_type = TransformerFactory.get_transformer_type(
            DocumentFormat.HTML
        )
        assert html_transformer_type is not None

        # Markdown doesn't need transformation
        md_transformer_type = TransformerFactory.get_transformer_type(
            DocumentFormat.MARKDOWN
        )
        assert md_transformer_type is None

    def test_create_transformer(self):
        """Test creating transformers for different formats."""
        # Skip test if transformers are not available
        if not TRANSFORMERS_AVAILABLE:
            self.skipTest("Core transformers not available")

        # HTML should have a transformer
        html_transformer = TransformerFactory.create_transformer(DocumentFormat.HTML)
        assert html_transformer is not None

        # Markdown doesn't need transformation
        md_transformer = TransformerFactory.create_transformer(DocumentFormat.MARKDOWN)
        assert md_transformer is None


class TestProcessingFunctions(unittest.TestCase):
    """Tests for document processing functions."""

    def setUp(self):
        """Set up test fixtures."""
        # Create a test HTML document
        self.html_doc = Document(
            document_id="test-html",
            content="<html><body><h1>Test</h1><p>This is a test HTML document.</p></body></html>",
            source_path="/path/to/test.html",
            source_type=DocumentSourceType.FILE,
            format=DocumentFormat.HTML,
        )

        # Create a test text document
        self.text_doc = Document(
            document_id="test-text",
            content="This is a test document.\n\nIt has multiple paragraphs.\n\nEach paragraph can be a separate chunk.",
            source_path="/path/to/test.txt",
            source_type=DocumentSourceType.FILE,
            format=DocumentFormat.TXT,
        )

        # Create chunking options
        self.chunking_options = ChunkingOptions(
            strategy=ChunkingStrategy.PARAGRAPH,
            chunk_size=100,
            chunk_overlap=0,
        )

    def test_transform_document(self):
        """Test transforming a document based on its format."""
        # Transform the HTML document
        transformed_doc = transform_document(self.html_doc)

        # If transformers are available, the content should be different
        if TRANSFORMERS_AVAILABLE:
            # The transformation might not actually happen if the transformer isn't available
            # but the function should still return the document
            assert transformed_doc is not None
        else:
            # If transformers aren't available, the document should be returned as is
            assert transformed_doc.content == self.html_doc.content

    def test_split_document(self):
        """Test splitting a document into chunks."""
        # Split the text document into paragraphs
        chunks = split_document(
            self.text_doc, ChunkingStrategy.PARAGRAPH, self.chunking_options
        )

        # Check that we have the expected number of chunks
        assert len(chunks) == 3

        # Check that the chunks have the expected content
        assert chunks[0].content == "This is a test document."
        assert chunks[1].content == "It has multiple paragraphs."
        assert chunks[2].content == "Each paragraph can be a separate chunk."

        # Check that the chunks have the correct document_id
        for chunk in chunks:
            assert chunk.document_id == "test-text"

    def test_process_document(self):
        """Test processing a document (transform and split)."""
        # Create a document with chunking options
        doc = Document(
            document_id="test-process",
            content="This is a document to process.\n\nIt has multiple paragraphs.\n\nLet's see how it's processed.",
            source_path="/path/to/test.txt",
            source_type=DocumentSourceType.FILE,
            format=DocumentFormat.TXT,
        )

        # Set chunking options
        doc.chunking_options = self.chunking_options

        # Process the document
        processed_doc = process_document(doc)

        # Check that we have the expected number of chunks
        assert len(processed_doc.chunks) == 3

        # Check that the chunks have the expected content
        assert processed_doc.chunks[0].content == "This is a document to process."
        assert processed_doc.chunks[1].content == "It has multiple paragraphs."
        assert processed_doc.chunks[2].content == "Let's see how it's processed."


class TestSimplifiedSplitting(unittest.TestCase):
    """Tests for simplified document splitting."""

    def setUp(self):
        """Set up test fixtures."""
        self.doc = Document(
            document_id="test-doc",
            content="This is a test document with multiple sentences. It has several sentences. And even more sentences here.\n\nIt also has multiple paragraphs.\n\nAnd even more paragraphs.",
            source_path="/path/to/test.txt",
            source_type=DocumentSourceType.FILE,
            format=DocumentFormat.TXT,
        )

    def test_simple_split_fixed_size(self):
        """Test simple fixed-size splitting."""
        options = ChunkingOptions(
            strategy=ChunkingStrategy.FIXED_SIZE,
            chunk_size=50,
            chunk_overlap=10,
        )

        # Force simplified splitting by setting SPLITTERS_AVAILABLE to False temporarily
        original_value = SPLITTERS_AVAILABLE
        try:
            # Make document_processors use the simplified splitting
            document_processors = __import__("document_processors")
            document_processors.SPLITTERS_AVAILABLE = False

            # Split the document
            chunks = split_document(self.doc, ChunkingStrategy.FIXED_SIZE, options)

            # Check that we have chunks
            assert len(chunks) > 0

            # Check that chunks are the right size
            for chunk in chunks:
                assert len(chunk.content) <= options.chunk_size

            # Check that chunks overlap
            if len(chunks) > 1:
                for i in range(len(chunks) - 1):
                    end_of_first = chunks[i].content[-options.chunk_overlap :]
                    start_of_second = chunks[i + 1].content[: options.chunk_overlap]
                    assert (
                        end_of_first == start_of_second
                        or end_of_first in start_of_second
                        or start_of_second in end_of_first
                    )
        finally:
            # Restore original value
            document_processors.SPLITTERS_AVAILABLE = original_value

    def test_simple_split_paragraph(self):
        """Test simple paragraph splitting."""
        options = ChunkingOptions(
            strategy=ChunkingStrategy.PARAGRAPH,
        )

        # Force simplified splitting
        original_value = SPLITTERS_AVAILABLE
        try:
            # Make document_processors use the simplified splitting
            document_processors = __import__("document_processors")
            document_processors.SPLITTERS_AVAILABLE = False

            # Split the document
            chunks = split_document(self.doc, ChunkingStrategy.PARAGRAPH, options)

            # Check that we have the expected number of chunks
            assert len(chunks) == 3

            # Check that chunks have the expected content
            assert (
                chunks[0].content
                == "This is a test document with multiple sentences. It has several sentences. And even more sentences here."
            )
            assert chunks[1].content == "It also has multiple paragraphs."
            assert chunks[2].content == "And even more paragraphs."
        finally:
            # Restore original value
            document_processors.SPLITTERS_AVAILABLE = original_value

    def test_simple_split_sentence(self):
        """Test simple sentence splitting."""
        options = ChunkingOptions(
            strategy=ChunkingStrategy.SENTENCE,
        )

        # Force simplified splitting
        original_value = SPLITTERS_AVAILABLE
        try:
            # Make document_processors use the simplified splitting
            document_processors = __import__("document_processors")
            document_processors.SPLITTERS_AVAILABLE = False

            # Split the document
            chunks = split_document(self.doc, ChunkingStrategy.SENTENCE, options)

            # Check that we have multiple chunks
            assert len(chunks) >= 3

            # Check that each chunk is a sentence
            for chunk in chunks:
                # Check that each chunk ends with a period or is a complete sentence
                assert (
                    chunk.content.endswith(".")
                    or chunk.content.endswith("!")
                    or chunk.content.endswith("?")
                )
        finally:
            # Restore original value
            document_processors.SPLITTERS_AVAILABLE = original_value


if __name__ == "__main__":
    unittest.main()
