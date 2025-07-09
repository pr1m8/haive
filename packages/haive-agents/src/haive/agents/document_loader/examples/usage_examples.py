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
    print("\n=== Basic Document Loader Agent Example ===")

    # Create a document loader agent
    agent = DocumentLoaderAgent(
        name="Basic Document Loader", include_metadata=True, max_documents=10
    )

    # Compile the agent
    compiled_agent = agent.compile()

    # Load a text file
    result = compiled_agent.invoke("./examples/sample.txt")

    # Print the result
    print(
        f"Loaded {result['total_documents']} documents from {result['original_source']}"
    )
    print(f"Loader used: {result['loader_name']}")
    print(f"Operation time: {result['operation_time']:.2f} seconds")

    # Print the first document's content
    if result["total_documents"] > 0:
        print("\nFirst document content:")
        print(result["documents"][0]["page_content"][:200] + "...")

    return result


def example_file_loader():
    """Example using the FileLoaderAgent."""
    print("\n=== File Loader Agent Example ===")

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
    print(
        f"Loaded {result['total_documents']} documents from {result['original_source']}"
    )
    print(f"Loader used: {result['loader_name']}")
    print(f"Operation time: {result['operation_time']:.2f} seconds")

    # Print metadata from the first document
    if result["total_documents"] > 0 and "metadata" in result["documents"][0]:
        print("\nDocument metadata:")
        for key, value in result["documents"][0]["metadata"].items():
            print(f"  {key}: {value}")

    return result


def example_web_loader():
    """Example using the WebLoaderAgent."""
    print("\n=== Web Loader Agent Example ===")

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
    print(
        f"Loaded {result['total_documents']} documents from {result['original_source']}"
    )
    print(f"Loader used: {result['loader_name']}")
    print(f"Operation time: {result['operation_time']:.2f} seconds")

    # Print the titles extracted from the web page
    if result["total_documents"] > 0:
        print("\nExtracted content:")
        for doc in result["documents"][:2]:  # Show first 2 documents
            content = doc["page_content"]
            # Extract first 100 characters
            print(f"  {content[:100]}...")

    return result


def example_directory_loader():
    """Example using the DirectoryLoaderAgent."""
    print("\n=== Directory Loader Agent Example ===")

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
    print(
        f"Loaded {result['total_documents']} documents from {result['original_source']}"
    )
    print(f"Source type: {result['source_type']}")
    print(f"Operation time: {result['operation_time']:.2f} seconds")

    # Print a summary of loaded files
    if result["total_documents"] > 0:
        print("\nLoaded files:")
        for doc in result["documents"]:
            source = doc["metadata"].get("source", "unknown")
            size = len(doc["page_content"])
            print(f"  {source}: {size} characters")

    return result


async def example_async_loading():
    """Example of asynchronous document loading."""
    print("\n=== Async Document Loading Example ===")

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

    print(f"Loaded {total_docs} documents from {len(sources)} sources")
    print(f"Total operation time: {total_time:.2f} seconds")

    # Print details for each source
    for i, result in enumerate(results):
        print(f"\nSource {i+1}: {result['original_source']}")
        print(f"  Documents: {result['total_documents']}")
        print(f"  Loader: {result['loader_name']}")
        print(f"  Time: {result['operation_time']:.2f} seconds")

    return results


def example_rag_integration():
    """Example of integrating document loader with RAG."""
    print("\n=== Document Loader + RAG Integration Example ===")

    # This would be a real implementation in a production system
    # Here we just demonstrate the pattern

    # Step 1: Load documents
    DirectoryLoaderAgent(
        name="Knowledge Base Loader", directory_path="./knowledge_base", recursive=True
    )

    # Step 2: Load documents (in a real implementation)
    # documents = loader.invoke()

    # Step 3: Create a RAG agent that would use the loaded documents
    # rag_agent = SimpleRAGAgent(
    #     name="RAG with Loaded Documents",
    #     documents=documents
    # )

    # For this example, we just print the process
    print("1. Document Loader Agent loads documents from knowledge base")
    print("2. Documents are processed and stored in vector database")
    print("3. RAG Agent uses the loaded documents for retrieval and generation")

    return "Integration example"


if __name__ == "__main__":
    print("Document Loader Agent Examples")
    print("==============================")

    try:
        example_basic_document_loader()
    except Exception as e:
        print(f"Error in basic example: {e}")

    try:
        example_file_loader()
    except Exception as e:
        print(f"Error in file loader example: {e}")

    try:
        example_web_loader()
    except Exception as e:
        print(f"Error in web loader example: {e}")

    try:
        example_directory_loader()
    except Exception as e:
        print(f"Error in directory loader example: {e}")

    try:
        asyncio.run(example_async_loading())
    except Exception as e:
        print(f"Error in async loading example: {e}")

    try:
        example_rag_integration()
    except Exception as e:
        print(f"Error in RAG integration example: {e}")

    print("\nExamples completed.")
