"""Document Loader Agent Usage Examples.

This module demonstrates how to use the document loader agents in various scenarios.
"""

import asyncio

from haive.agents.document_loader import (
    DirectoryLoaderAgent,
    DocumentLoaderAgent,
    FileLoaderAgent,
    WebLoaderAgent,
)


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


async def example_async_loading():
    """Example of asynchronous document loading."""

    # Create an agent with async loading enabled
    agent = DocumentLoaderAgent(name="Async Document Loader", use_async=True)

    # Compile the agent
    compiled_agent = agent.compile()

    # Define multiple sources to load
    sources = ["./examples/doc1.txt", "./examples/doc2.pdf", "https://example.com"]

    # Load all sources concurrently
    tasks = [compiled_agent.ainvoke(source) for source in sources]
    results = await asyncio.gather(*tasks)

    # Print summary
    total_docs = sum(result["total_documents"] for result in results)
    total_time = sum(result["operation_time"] for result in results)


    # Print details for each source
    for i, result in enumerate(results):

    return results


def example_rag_integration():
    """Example of integrating document loader with RAG."""

    # This would be a real implementation in a production system
    # Here we just demonstrate the pattern

    # Step 1: Load documents
    DirectoryLoaderAgent(
        name="Knowledge Base Loader", directory_path="./knowledge_base", recursive=True
    )

    # Step 2: Load documents (in a real implementation)

    # Step 3: Create a RAG agent that would use the loaded documents

    # For this example, we just print the process

    return "Integration example"


if __name__ == "__main__":

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

    try:
        asyncio.run(example_async_loading())
    except Exception as e:
        pass

    try:
        example_rag_integration()
    except Exception as e:
        pass

