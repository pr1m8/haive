#!/usr/bin/env python
"""Example of document agent with core engine integration.

This script demonstrates how the DocumentAgent integrates with the Haive core engine's
document transformers and splitters for enhanced document processing capabilities.
"""

import logging
import os
import tempfile

from document_agent import (
    DocumentAgent,
    DocumentAgentOptions,
)
from document_processors import SPLITTERS_AVAILABLE, TRANSFORMERS_AVAILABLE
from document_state import (
    ChunkingOptions,
    ChunkingStrategy,
)


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


def example_engine_integration():
    """Example of DocumentAgent integration with core engine transformers and splitters."""
    logger.info("=== Example: Core Engine Integration ===")

    # Create sample files
    file_paths = create_sample_files()

    # Check if core components are available
    logger.info(f"Core splitters available: {SPLITTERS_AVAILABLE}")
    logger.info(f"Core transformers available: {TRANSFORMERS_AVAILABLE}")

    # Create a document agent with different chunking strategies
    options = DocumentAgentOptions(
        default_chunking_options=ChunkingOptions(
            strategy=ChunkingStrategy.RECURSIVE,
            chunk_size=300,
            chunk_overlap=50,
        )
    )

    agent = DocumentAgent(options=options)

    # Add sources with different formats to demonstrate format-specific processing
    for file_path in file_paths:
        logger.info(f"Adding source: {file_path}")
        agent.add_source(file_path)

    # Process documents
    logger.info("Processing documents...")
    agent.process_documents()

    # Display results
    logger.info("\nResults:")
    logger.info(f"- Processed {len(agent.get_documents())} documents")

    for doc in agent.get_documents():
        logger.info(f"  - {os.path.basename(doc.source_path)} ({doc.format.value}):")
        logger.info(f"    - Content length: {len(doc.content)} chars")
        logger.info(f"    - Chunks: {doc.chunk_count}")

        # Show the first chunk of each document
        if doc.chunks:
            logger.info(f"    - First chunk: '{doc.chunks[0].content[:50]}...'")

    # Display statistics
    stats = agent.state.processing_stats
    logger.info("\nProcessing statistics:")
    logger.info(f"- Total sources: {stats.total_sources}")
    logger.info(f"- Total documents: {stats.total_documents}")
    logger.info(f"- Total chunks: {stats.total_chunks}")
    logger.info(f"- Processing time: {stats.processing_time_seconds:.2f} seconds")


def example_html_transformation():
    """Example of HTML document transformation."""
    logger.info("\n=== Example: HTML Transformation ===")

    # Create sample files
    file_paths = create_sample_files()

    # Get only the HTML file
    html_file = [f for f in file_paths if f.endswith(".html")][0]

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
    else:
        logger.warning("No documents processed")


def example_specialized_chunking():
    """Example of specialized chunking strategies based on document format."""
    logger.info("\n=== Example: Specialized Chunking ===")

    # Create sample files
    file_paths = create_sample_files()

    # Create a document agent with format-specific chunking
    agent = DocumentAgent()

    # Add sources with specific chunking options based on format
    for file_path in file_paths:
        if file_path.endswith(".md"):
            # Use markdown-specific chunking for markdown files
            chunking_options = ChunkingOptions(
                strategy=ChunkingStrategy.RECURSIVE,
                chunk_size=200,
                chunk_overlap=30,
            )
            agent.add_source(file_path, chunking_options=chunking_options)
        elif file_path.endswith(".html"):
            # Use HTML header-based chunking for HTML files
            chunking_options = ChunkingOptions(
                strategy=ChunkingStrategy.PARAGRAPH,
                chunk_size=300,
                chunk_overlap=0,
            )
            agent.add_source(file_path, chunking_options=chunking_options)
        else:
            # Use sentence-based chunking for other files
            chunking_options = ChunkingOptions(
                strategy=ChunkingStrategy.SENTENCE,
            )
            agent.add_source(file_path, chunking_options=chunking_options)

    # Process documents
    logger.info("Processing documents with format-specific chunking...")
    agent.process_documents()

    # Display results
    logger.info("\nResults:")
    for doc in agent.get_documents():
        logger.info(f"  - {os.path.basename(doc.source_path)} ({doc.format.value}):")
        logger.info(f"    - Chunks: {doc.chunk_count}")
        logger.info(
            f"    - Avg chunk size: {sum(len(c.content) for c in doc.chunks) / max(1, doc.chunk_count):.1f} chars"
        )


def main():
    """Run the example script."""
    logger.info("==== Document Agent Engine Integration Example ====")

    example_engine_integration()
    example_html_transformation()
    example_specialized_chunking()

    logger.info("\n==== Example Complete ====")


if __name__ == "__main__":
    main()
