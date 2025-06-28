"""Document Loader Agent Examples.

This module demonstrates various ways to use the Document Loader Agent
in real-world scenarios.
"""

import asyncio
import os
from typing import Any, Dict, List

# Import document loader agents
from agent import (
    DirectoryLoaderAgent,
    DocumentLoaderAgent,
    FileLoaderAgent,
    WebLoaderAgent,
)
from haive.core.graph.state_graph.state_graph import StateGraph

# ============================================================================
# BASIC USAGE EXAMPLES
# ============================================================================


def example_basic_document_loader():
    """Basic example using the DocumentLoaderAgent."""

    # Create a document loader agent
    agent = DocumentLoaderAgent(
        name="Basic Document Loader", include_metadata=True, max_documents=10
    )

    # Compile the agent
    compiled_agent = agent.compile()

    # Load a text file
    result = compiled_agent.invoke("./examples/sample.txt")

    # Print the result

    # Print the first document's content
    if result["total_documents"] > 0:

    return result


def example_file_loader():
    """Example using the FileLoaderAgent."""

    # Create a file loader agent
    agent = FileLoaderAgent(
        name="PDF File Loader",
        file_path="./examples/document.pdf",
        loader_name="pdf_loader",
        include_metadata=True,
    )

    # Compile the agent
    compiled_agent = agent.compile()

    # Load the file
    result = compiled_agent.invoke()

    # Print the result

    # Print metadata from the first document
    if result["total_documents"] > 0 and "metadata" in result["documents"][0]:
        for key, value in result["documents"][0]["metadata"].items():
            pass

    return result


def example_web_loader():
    """Example using the WebLoaderAgent."""

    # Create a web loader agent
    agent = WebLoaderAgent(
        name="Dynamic Web Loader",
        url="https://en.wikipedia.org/wiki/Artificial_intelligence",
        dynamic_loading=True,
        max_documents=5,
    )

    # Compile the agent
    compiled_agent = agent.compile()

    # Load the web page
    result = compiled_agent.invoke()

    # Print the result

    # Print the titles extracted from the web page
    if result["total_documents"] > 0:
        for doc in result["documents"][:2]:  # Show first 2 documents
            content = doc["page_content"]
            # Extract first 100 characters

    return result


def example_directory_loader():
    """Example using the DirectoryLoaderAgent."""

    # Create a directory loader agent
    agent = DirectoryLoaderAgent(
        name="Markdown Directory Loader",
        directory_path="./docs",
        recursive=True,
        include_extensions=[".md", ".txt"],
        exclude_extensions=[".tmp"],
    )

    # Compile the agent
    compiled_agent = agent.compile()

    # Load the directory
    result = compiled_agent.invoke()

    # Print the result

    # Print a summary of loaded files
    if result["total_documents"] > 0:
        for doc in result["documents"]:
            source = doc["metadata"].get("source", "unknown")
            size = len(doc["page_content"])

    return result


# ============================================================================
# ADVANCED USAGE EXAMPLES
# ============================================================================


async def example_async_loading():
    """Example of asynchronous document loading."""

    # Create an agent with async loading enabled
    agent = DocumentLoaderAgent(name="Async Document Loader", use_async=True)

    # Compile the agent
    compiled_agent = agent.compile()

    # Define multiple sources to load
    sources = [
        "./examples/doc1.txt",
        "./examples/doc2.pdf",
        "https://example.com",
        "./examples/data_directory",
    ]

    # Load all sources concurrently
    tasks = [compiled_agent.ainvoke(source) for source in sources]
    results = await asyncio.gather(*tasks)

    # Print summary
    total_docs = sum(result["total_documents"] for result in results)
    total_time = sum(result["operation_time"] for result in results)


    # Print details for each source
    for i, result in enumerate(results):

    return results


def example_combined_with_rag():
    """Example of combining document loading with retrieval."""

    # This example demonstrates how the document loader agent can be used
    # as part of a larger RAG workflow. In a real implementation, you would
    # integrate this with a vector store and retriever.

    # First, load documents
    loader_agent = DirectoryLoaderAgent(
        name="Document Loader", directory_path="./knowledge_base", recursive=True
    )

    # Compile the agent
    compiled_loader = loader_agent.compile()

    # Load documents
    loading_result = compiled_loader.invoke()


    # In a real implementation, you would now:
    # 1. Process and chunk the documents
    # 2. Create embeddings
    # 3. Store in a vector database
    # 4. Set up a retriever
    # 5. Use the retriever in a RAG workflow


    return loading_result


def example_complex_workflow():
    """Example of a more complex document loading workflow with branching logic."""

    # Define a complex workflow that:
    # 1. Determines the type of input (file, URL, directory)
    # 2. Routes to the appropriate loader
    # 3. Processes the loaded documents

    # In a real implementation, this would be a proper LangGraph workflow
    # Here we'll just simulate the routing logic

    def process_input(input_path: str) -> dict[str, Any]:
        """Process input and route to appropriate loader."""
        # Determine input type
        if input_path.startswith(("http://", "https://")):
            agent = WebLoaderAgent(url=input_path)
        elif os.path.isdir(input_path):
            agent = DirectoryLoaderAgent(directory_path=input_path)
        elif os.path.isfile(input_path):
            agent = FileLoaderAgent(file_path=input_path)
        else:
            # Try generic loader as fallback
            agent = DocumentLoaderAgent()

        # Compile and invoke
        compiled_agent = agent.compile()
        return compiled_agent.invoke()

    # Try different input types
    inputs = [
        "./examples/document.txt",  # File
        "https://example.com",  # URL
        "./examples/data_dir",  # Directory
        "invalid_path",  # Invalid input
    ]

    results = []
    for input_path in inputs:
        try:
            result = process_input(input_path)
            results.append(result)
        except Exception as e:
            pass

    return results


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":

    # Basic examples
    try:
        example_basic_document_loader()
    except Exception as e:
        pass

    try:
        example_file_loader()
    except Exception as e:
        pass

    try:
        example_web_loader()
    except Exception as e:
        pass

    try:
        example_directory_loader()
    except Exception as e:
        pass

    # Advanced examples
    try:
        asyncio.run(example_async_loading())
    except Exception as e:
        pass

    try:
        example_combined_with_rag()
    except Exception as e:
        pass

    try:
        example_complex_workflow()
    except Exception as e:
        pass

