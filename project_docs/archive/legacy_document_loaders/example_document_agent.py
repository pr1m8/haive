#!/usr/bin/env python
"""Example usage of DocumentAgent for document loading and processing.

This script demonstrates how to use the DocumentAgent to load and process
documents from various sources, including files, text, and URLs.
"""

import os
import tempfile

from .document_agent import (
    DocumentAgent,
    DocumentAgentOptions,
    create_directory_document_agent,
    create_file_document_agent,
    create_web_document_agent,
)
from .document_state import (
    ChunkingOptions,
    ChunkingStrategy,
    DocumentFormat,
    DocumentSourceType,
    LoadingOptions,
    LoadingStrategy,
)


def create_sample_files() -> list[str]:
    """Create sample files for the example.

    Returns:
        List[str]: List of file paths.
    """
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

    return file_paths


def example_basic_usage():
    """Example of basic DocumentAgent usage."""
    # Create sample files
    file_paths = create_sample_files()

    # Create a document agent
    agent = DocumentAgent()

    # Add sources
    agent.add_sources(file_paths)
    agent.add_source("https://example.com")
    agent.add_source("text://This is a sample text source for testing.")

    # Initialize the agent's graph
    graph = agent.build_graph()

    # Execute the workflow
    agent.state = graph.invoke(agent.state)

    # Check results
    for _doc in agent.get_documents():
        pass

    # Display statistics

    # Sample output:
    """
    === Example: Basic DocumentAgent Usage ===

    Adding sources...
    Building agent graph...
    Executing document processing workflow...
    Processed 4 documents:
    - /tmp/tmpdir123/sample.txt: 427 chars, 6 chunks
    - /tmp/tmpdir123/sample.md: 297 chars, 4 chunks
    - https://example.com: 1256 chars, 8 chunks
    - text://This is a sample text source for testing.: 45 chars, 1 chunks

    Processing statistics:
    - Total sources: 4
    - Total documents: 4
    - Total chunks: 19
    - Processing time: 1.23 seconds
    """


def example_custom_configuration():
    """Example of DocumentAgent with custom configuration."""
    # Create sample files
    file_paths = create_sample_files()

    # Create custom options
    options = DocumentAgentOptions(
        default_loading_options=LoadingOptions(
            strategy=LoadingStrategy.DIRECT,
            timeout_seconds=30,
        ),
        default_chunking_options=ChunkingOptions(
            strategy=ChunkingStrategy.PARAGRAPH,
            chunk_size=1000,  # Not used for paragraph chunking
            metadata_scope="document",
        ),
        parallel_processing=True,
        max_workers=2,
        skip_errors=True,
    )

    # Create a document agent with custom options
    agent = DocumentAgent(options=options)

    # Add sources
    for path in file_paths:
        # Add a source with source-specific options
        agent.add_source(
            path,
            loading_options=LoadingOptions(
                strategy=LoadingStrategy.DIRECT,
                timeout_seconds=60,  # Override default timeout
            ),
            chunking_options=ChunkingOptions(
                strategy=ChunkingStrategy.PARAGRAPH,
            ),
        )

    # Add a text source with different chunking strategy
    agent.add_source(
        "text://This is a sample text source.\nIt has multiple lines.\nEach line can be processed separately.",
        source_type=DocumentSourceType.TEXT,
        chunking_options=ChunkingOptions(
            strategy=ChunkingStrategy.SENTENCE,
        ),
    )

    # Initialize and execute
    graph = agent.build_graph()
    agent.state = graph.invoke(agent.state)

    # Check results by format
    for format_type in agent.state.document_formats:
        agent.get_documents_by_format(format_type)

    # Check chunking results
    for doc in agent.get_documents():
        # Print first chunk from each document
        if doc.chunks:
            pass

    # Sample output:
    """
    === Example: Custom Configuration ===

    Processing documents with custom configuration...

    Documents by format:
    - txt: 1 documents
    - markdown: 1 documents
    - text: 1 documents

    Chunking results:
    - /tmp/tmpdir123/sample.txt: 9 chunks
      First chunk: "# Sample Text Document"...
    - /tmp/tmpdir123/sample.md: 6 chunks
      First chunk: "# Sample Markdown Document"...
    - text://This is a sample text source.\nIt has multiple lines.\nEach line can be processed separately.: 3 chunks
      First chunk: "This is a sample text source."...
    """


def example_specialized_agents():
    """Example of specialized document agents."""
    # Create sample files
    file_paths = create_sample_files()

    # 1. File Document Agent
    file_agent = create_file_document_agent(
        file_paths=file_paths,
        chunking_strategy=ChunkingStrategy.FIXED_SIZE,
        chunk_size=100,
        chunk_overlap=20,
    )

    # Execute the file agent
    graph = file_agent.build_graph()
    file_agent.state = graph.invoke(file_agent.state)

    # 2. Web Document Agent
    create_web_document_agent(
        urls=["https://example.com", "https://haive.ai"],
        chunking_strategy=ChunkingStrategy.PARAGRAPH,
    )

    # For this example, we'll just show the configuration
    # (without actually making network requests)

    # 3. Directory Document Agent
    # Get the directory of the first sample file
    sample_dir = os.path.dirname(file_paths[0])
    create_directory_document_agent(
        directory_paths=[sample_dir],
        include_patterns=["*.txt", "*.md"],
        exclude_patterns=["*.tmp", "*.log"],
        recursive=True,
        recursive_depth=2,
    )

    # For this example, we'll just show the configuration

    # Sample output:
    """
    === Example: Specialized Document Agents ===

    1. File Document Agent
    Loaded 2 documents with 16 chunks

    2. Web Document Agent
    Created agent for 2 URLs
    Chunking strategy: paragraph
    Loading timeout: 120 seconds

    3. Directory Document Agent
    Created agent for directory: /tmp/tmpdir123
    Include patterns: ['*.txt', '*.md']
    Exclude patterns: ['*.tmp', '*.log', '.git/*', '__pycache__/*']
    Recursive depth: 2
    """


def example_error_handling():
    """Example of error handling in DocumentAgent."""
    # Create a document agent with error skipping enabled
    agent = DocumentAgent(
        options=DocumentAgentOptions(
            skip_errors=True,  # Continue processing even if some sources fail
        )
    )

    # Add valid and invalid sources
    agent.add_source("/path/to/nonexistent/file.txt")  # Should fail
    agent.add_source("invalid://schema")  # Should fail

    # Add a valid text source
    agent.add_source("text://This is a valid text source.")

    # Process the sources
    graph = agent.build_graph()
    agent.state = graph.invoke(agent.state)

    # Check results

    # Display errors
    for _i, _error in enumerate(agent.state.error_messages):
        pass

    # Check documents
    for _doc in agent.get_documents():
        pass

    # Sample output:
    """
    === Example: Error Handling ===

    Processing sources with error handling...

    Processing results:
    Total sources: 3
    Successful sources: 1
    Failed sources: 2

    Errors encountered:
    1. Error processing /path/to/nonexistent/file.txt: Error analyzing source: File not found
    2. Error processing invalid://schema: No loader found for source: invalid://schema

    Loaded 1 documents successfully
    - text://This is a valid text source.: 29 chars
    """


def example_document_access():
    """Example of accessing and analyzing documents."""
    # Create sample files
    file_paths = create_sample_files()

    # Create an agent and process files
    agent = create_file_document_agent(
        file_paths=file_paths,
        chunking_strategy=ChunkingStrategy.PARAGRAPH,
    )

    # Process the documents
    graph = agent.build_graph()
    agent.state = graph.invoke(agent.state)

    # 1. Access documents by ID
    documents = agent.get_documents()
    if documents:
        doc_id = documents[0].document_id
        agent.get_document(doc_id)

    # 2. Access documents by source
    if file_paths:
        source_path = file_paths[0]
        docs = agent.get_documents_by_source(source_path)
        if docs:
            pass

    # 3. Access documents by format
    agent.get_documents_by_format(DocumentFormat.TXT)
    agent.get_documents_by_format(DocumentFormat.MARKDOWN)

    # 4. Access all chunks
    all_chunks = agent.get_all_chunks()

    # 5. Search for content in chunks
    search_term = "DocumentAgent"
    matching_chunks = [
        chunk for chunk in all_chunks if search_term.lower() in chunk.content.lower()
    ]
    if matching_chunks:
        pass

    # Sample output:
    """
    === Example: Document Access and Analysis ===

    1. Access documents by ID
    Document ID: 12345-abcde-67890
    Source: /tmp/tmpdir123/sample.txt
    Format: txt
    Size: 427 characters
    Chunks: 9

    2. Access documents by source
    Documents from /tmp/tmpdir123/sample.txt: 1
    First document has 9 chunks

    3. Access documents by format
    Text documents: 1
    Markdown documents: 1

    4. Access all chunks
    Total chunks: 15

    5. Search for content in chunks
    Chunks containing 'DocumentAgent': 3
    First match: "This is a sample text document for testing the DocumentAgent."...
    """


def main():
    """Run all examples."""
    # Run basic usage example
    example_basic_usage()

    # Run custom configuration example
    example_custom_configuration()

    # Run specialized agents example
    example_specialized_agents()

    # Run error handling example
    example_error_handling()

    # Run document access example
    example_document_access()


if __name__ == "__main__":
    main()
