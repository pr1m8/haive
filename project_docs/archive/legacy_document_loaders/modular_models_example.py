#!/usr/bin/env python
"""Example of using the modular document models.

This script demonstrates how to use the modular document models for document processing,
showing their integration with LangChain and flexibility for different document types.
"""

import logging
import os
import tempfile

from document_models import (  # Base models; Enums; Configuration models; Utility functions
    ChunkingOptions,
    ChunkingStrategy,
    Document,
    DocumentCollection,
    DocumentFormat,
    DocumentSourceType,
    DocumentState,
    LoadingOptions,
    LoadingStrategy,
    ProcessingStage,
    chunks_to_langchain,
    documents_to_langchain,
    lc_documents_to_document_collection,
)

# Try to import langchain for demonstration
try:
    from langchain_core.documents import Document as LCDocument

    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False

    # Simple mock for demonstration purposes
    class LCDocument:
        def __init__(self, page_content, metadata=None):
            self.page_content = page_content
            self.metadata = metadata or {}


# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


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

This is a sample text document for testing document models.

## Section 1

This document has multiple sections and paragraphs.
Each paragraph can be processed as a separate chunk.

## Section 2

Different document models provide different functionality.
"""
        )
    file_paths.append(text_file)

    # Create a markdown file
    md_file = os.path.join(temp_dir, "sample.md")
    with open(md_file, "w") as f:
        f.write(
            """# Sample Markdown Document

This is a sample markdown document for testing document models.

## Features

- Document models for different document types
- Integration with LangChain
- Flexible configuration options

## Benefits

1. Consistent interface for document processing
2. Rich metadata handling
3. Enhanced document collections
"""
        )
    file_paths.append(md_file)

    return file_paths


def example_basic_document_models():
    """Example of basic document model usage."""
    logger.info("=== Example: Basic Document Models ===")

    # Create a document with metadata
    doc = Document(
        content="This is a sample document content.",
        source_path="/path/to/sample.txt",
        source_type=DocumentSourceType.FILE,
        format=DocumentFormat.TXT,
        metadata={
            "author": "Example Author",
            "title": "Sample Document",
            "keywords": ["sample", "document", "test"],
        },
    )

    # Add chunks to the document
    doc.add_chunk("This is the first chunk of content.", {"chunk_type": "introduction"})
    doc.add_chunk("This is the second chunk with more details.", {"chunk_type": "body"})
    doc.add_chunk("This is the conclusion chunk.", {"chunk_type": "conclusion"})

    logger.info(f"Created document with ID: {doc.id}")
    logger.info(f"Document has {doc.chunk_count} chunks")
    logger.info(f"Document token estimate: {doc.token_estimate}")

    # Convert to LangChain format
    if LANGCHAIN_AVAILABLE:
        lc_doc = doc.to_langchain()
        logger.info(
            f"Converted to LangChain document with content: '{lc_doc.page_content[:50]}...'"
        )
        logger.info(f"LangChain metadata: {lc_doc.metadata}")

        # Get chunks as LangChain documents
        lc_chunks = doc.get_chunks_as_langchain()
        logger.info(f"Converted {len(lc_chunks)} chunks to LangChain format")


def example_document_collections():
    """Example of document collections."""
    logger.info("\n=== Example: Document Collections ===")

    # Create a collection
    collection = DocumentCollection(
        name="Sample Collection",
        description="A collection of sample documents",
        tags=["sample", "test"],
    )

    # Create and add documents
    file_paths = create_sample_files()

    for _i, path in enumerate(file_paths):
        with open(path) as f:
            content = f.read()

        # Determine format from extension
        format = DocumentFormat.TXT
        if path.endswith(".md"):
            format = DocumentFormat.MARKDOWN

        # Create document
        doc = Document(
            content=content,
            source_path=path,
            source_type=DocumentSourceType.FILE,
            format=format,
            metadata={
                "filename": os.path.basename(path),
                "file_size": os.path.getsize(path),
            },
        )

        # Add some chunks
        paragraphs = content.split("\n\n")
        for j, para in enumerate(paragraphs):
            if para.strip():
                doc.add_chunk(para.strip(), {"paragraph_index": j})

        # Add to collection
        collection.add_document(doc)

    logger.info(
        f"Created collection '{collection.name}' with {collection.document_count} documents"
    )
    logger.info(
        f"Collection contains {collection.chunk_count} chunks across all documents"
    )
    logger.info(f"Estimated total tokens: {collection.token_estimate}")

    # Get all chunks as LangChain documents
    if LANGCHAIN_AVAILABLE:
        lc_docs = collection.get_all_chunks_as_langchain()
        logger.info(f"Converted all {len(lc_docs)} chunks to LangChain documents")

        # Show the first chunk
        if lc_docs:
            logger.info(f"First chunk: '{lc_docs[0].page_content[:50]}...'")
            logger.info(f"First chunk metadata: {lc_docs[0].metadata}")


def example_document_state():
    """Example of document state for tracking processing."""
    logger.info("\n=== Example: Document State ===")

    # Create a document state
    state = DocumentState()

    # Configure options
    state.loading_options = LoadingOptions(
        strategy=LoadingStrategy.DIRECT, extract_metadata=True
    )

    state.chunking_options = ChunkingOptions(
        strategy=ChunkingStrategy.PARAGRAPH, chunk_size=500, chunk_overlap=50
    )

    # Add sources
    file_paths = create_sample_files()
    for path in file_paths:
        state.add_source(path)

    logger.info(f"Added {len(state.sources)} sources to the state")

    # Simulate source analysis
    for source in state.sources:
        source.update_stage(ProcessingStage.ANALYZING)

        # Set source type and format based on file extension
        if source.path.endswith(".txt"):
            source.format = DocumentFormat.TXT
        elif source.path.endswith(".md"):
            source.format = DocumentFormat.MARKDOWN

        source.source_type = DocumentSourceType.FILE
        source.update_stage(ProcessingStage.QUEUED)

    logger.info("Analyzed all sources")

    # Simulate document loading
    for source in state.get_sources_by_stage(ProcessingStage.QUEUED):
        source.update_stage(ProcessingStage.LOADING)

        with open(source.path) as f:
            content = f.read()

        # Create a document
        doc = state.add_document(
            content=content,
            source_path=source.path,
            source_type=source.source_type,
            format=source.format,
            metadata={
                "filename": os.path.basename(source.path),
                "file_size": os.path.getsize(source.path),
            },
        )

        # Update source to chunking stage
        source.update_stage(ProcessingStage.CHUNKING)

    logger.info(f"Loaded {len(state.documents)} documents")

    # Simulate document chunking
    for source in state.get_sources_by_stage(ProcessingStage.CHUNKING):
        # Get documents for this source
        docs = state.get_documents_by_source(source.path)

        for doc in docs:
            # Skip already chunked documents
            if doc.chunks:
                continue

            # Split by paragraphs
            paragraphs = doc.content.split("\n\n")
            for i, paragraph in enumerate(paragraphs):
                if paragraph.strip():
                    doc.add_chunk(
                        paragraph.strip(),
                        {"paragraph_index": i, "source_path": doc.source_path},
                    )

            logger.info(f"Created {doc.chunk_count} chunks for document {doc.id}")

        # Mark source as completed
        source.update_stage(ProcessingStage.COMPLETED)

    # Update statistics
    state.processing_stats.total_chunks = state.total_chunks
    state.processing_stats.total_tokens = sum(
        doc.token_estimate for doc in state.documents
    )
    state.mark_processing_complete()

    # Get summary
    logger.info("Processing complete")
    logger.info(f"State summary: {state.summary}")

    # Create a collection from all documents
    collection = DocumentCollection(
        name="All Documents", description="Collection of all processed documents"
    )

    for doc in state.documents:
        collection.add_document(doc)

    logger.info(
        f"Created collection with {collection.document_count} documents and {collection.chunk_count} chunks"
    )

    # Convert to LangChain format
    if LANGCHAIN_AVAILABLE:
        lc_docs = state.get_all_langchain_documents()
        logger.info(f"Converted {len(lc_docs)} documents to LangChain format")

        lc_chunks = state.get_all_chunks_as_langchain()
        logger.info(f"Converted {len(lc_chunks)} chunks to LangChain format")


def example_langchain_integration():
    """Example of LangChain integration."""
    logger.info("\n=== Example: LangChain Integration ===")

    # Skip if LangChain is not available
    if not LANGCHAIN_AVAILABLE:
        logger.info("LangChain is not available. Skipping example.")
        return

    # Create some LangChain documents
    lc_docs = [
        LCDocument(
            page_content="This is the first LangChain document.",
            metadata={"source": "/path/to/doc1.txt", "author": "Author 1", "page": 1},
        ),
        LCDocument(
            page_content="This is the second LangChain document.",
            metadata={"source": "/path/to/doc2.txt", "author": "Author 2", "page": 1},
        ),
        LCDocument(
            page_content="This is the third LangChain document.",
            metadata={"source": "/path/to/doc3.txt", "author": "Author 3", "page": 1},
        ),
    ]

    # Create a document state
    state = DocumentState()

    # Add the LangChain documents
    for lc_doc in lc_docs:
        doc = state.add_langchain_document(lc_doc)
        logger.info(f"Added LangChain document as {doc.id}")

    # Create a collection from LangChain documents
    collection = lc_documents_to_document_collection(
        lc_docs,
        collection_name="LangChain Documents",
        description="Documents imported from LangChain",
    )

    logger.info(f"Created collection with {collection.document_count} documents")

    # Add the collection to the state
    state.collections[collection.id] = collection

    # Convert documents back to LangChain format
    converted_lc_docs = documents_to_langchain(state.documents)
    logger.info(
        f"Converted {len(converted_lc_docs)} documents back to LangChain format"
    )

    # Now chunk the documents and convert chunks to LangChain
    for doc in state.documents:
        # Create chunks (one sentence per chunk)
        sentences = doc.content.split(".")
        for i, sentence in enumerate(sentences):
            if sentence.strip():
                doc.add_chunk(
                    sentence.strip() + ".",
                    {"sentence_index": i, "source": doc.source_path},
                )

    # Get all chunks as LangChain documents
    chunk_lc_docs = chunks_to_langchain(state.get_all_chunks())
    logger.info(f"Converted {len(chunk_lc_docs)} chunks to LangChain format")


def main():
    """Run all examples."""
    logger.info("==== Document Models Examples ====")

    example_basic_document_models()
    example_document_collections()
    example_document_state()
    example_langchain_integration()

    logger.info("\n==== Examples Complete ====")


if __name__ == "__main__":
    main()
