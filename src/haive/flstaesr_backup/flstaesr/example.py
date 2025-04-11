# Examples of using the FLSTAESR agent for RAG

from src.haive.agents.flstaesr.agent import (
    create_flstaesr_agent, 
    DocumentSource, 
    run_query_with_documents,
    run_query_with_urls
)
from langchain_core.documents import Document

# Example 1: Basic usage with a simple query
def example_basic_usage():
    """Example of basic agent usage with a query."""
    # Create the agent
    agent = create_flstaesr_agent(
        name="documentation_assistant",
        llm_model="gpt-4o",
        embedding_model="text-embedding-3-small"
    )
    
    # Run a query
    query = "What are the key components of LangChain's LCEL?"
    result = agent.run(query)
    
    # Print the response
    messages = result.get("messages", [])
    for message in messages:
        if hasattr(message, "content") and message.type == "ai":
            print(f"AI: {message.content}")

# Example 2: Using pre-loaded documents
def example_with_documents():
    """Example using pre-loaded documents."""
    # Create some documents
    documents = [
        Document(
            page_content="LangChain Expression Language (LCEL) is a declarative way to compose chains together. "
                         "It uses the '|' operator to connect components.",
            metadata={"source": "documentation", "title": "LCEL Introduction"}
        ),
        Document(
            page_content="Key components of LCEL include prompts, LLMs, output parsers, and retrievers.",
            metadata={"source": "documentation", "title": "LCEL Components"}
        ),
        Document(
            page_content="LCEL enables easy serialization and streaming of chains.",
            metadata={"source": "documentation", "title": "LCEL Benefits"}
        )
    ]
    
    # Run a query with the documents
    query = "Explain the benefits of LCEL"
    result = run_query_with_documents(query, documents)
    
    # Print the response
    messages = result.get("messages", [])
    for message in messages:
        if hasattr(message, "content") and message.type == "ai":
            print(f"AI: {message.content}")

# Example 3: Using URLs as sources
def example_with_urls():
    """Example using URLs as sources."""
    # List of URLs to use as sources
    urls = [
        "https://python.langchain.com/docs/expression_language/",
        "https://python.langchain.com/docs/expression_language/interface/",
        "https://python.langchain.com/docs/expression_language/why/"
    ]
    
    # Run a query with the URLs
    query = "What are the advantages of using LCEL over traditional chain construction?"
    result = run_query_with_urls(query, urls)
    
    # Print the response
    messages = result.get("messages", [])
    for message in messages:
        if hasattr(message, "content") and message.type == "ai":
            print(f"AI: {message.content}")

# Example 4: Using a sitemap source
def example_with_sitemap():
    """Example using a sitemap source."""
    # Create the agent
    agent = create_flstaesr_agent()
    
    # Create document source from sitemap
    sitemap_source = DocumentSource.from_sitemap("https://python.langchain.com")
    
    # Create initial state with query and document source
    initial_state = {
        "query": "How does LangChain handle RAG?",
        "document_sources": [sitemap_source]
    }
    
    # Run agent starting from the load step
    result = agent.run(initial_state, override_entry_point="load")
    
    # Print the response
    messages = result.get("messages", [])
    for message in messages:
        if hasattr(message, "content") and message.type == "ai":
            print(f"AI: {message.content}")

# Example 5: Using HuggingFace model search
def example_with_huggingface():
    """Example using HuggingFace model search."""
    # Create the agent
    agent = create_flstaesr_agent()
    
    # Create document source from HuggingFace model search
    hf_source = DocumentSource.from_huggingface_model("text-to-sql", limit=3)
    
    # Create initial state with query and document source
    initial_state = {
        "query": "What are the best text-to-SQL models and how do they work?",
        "document_sources": [hf_source]
    }
    
    # Run agent starting from the load step
    result = agent.run(initial_state, override_entry_point="load")
    
    # Print the response
    messages = result.get("messages", [])
    for message in messages:
        if hasattr(message, "content") and message.type == "ai":
            print(f"AI: {message.content}")

# Example 6: Recursive URL loading
def example_with_recursive_url():
    """Example using recursive URL loading."""
    # Create document source with recursive loading
    documentation_source = DocumentSource.from_recursive_url(
        "https://python.langchain.com/docs/get_started/introduction", 
        max_depth=2
    )
    
    # Create initial state with query and document source
    initial_state = {
        "query": "What is LangChain and what are its core components?",
        "document_sources": [documentation_source]
    }
    
    # Create the agent and run
    agent = create_flstaesr_agent()
    result = agent.run(initial_state, override_entry_point="load")
    
    # Print the response
    messages = result.get("messages", [])
    for message in messages:
        if hasattr(message, "content") and message.type == "ai":
            print(f"AI: {message.content}")

if __name__ == "__main__":
    print("\n=== Example 1: Basic Usage ===\n")
    example_basic_usage()
    
    print("\n=== Example 2: With Documents ===\n")
    example_with_documents()
    
    print("\n=== Example 3: With URLs ===\n")
    example_with_urls()
    
    # These examples require internet connection
    print("\n=== Example 4: With Sitemap ===\n")
    example_with_sitemap()
    
    print("\n=== Example 5: With HuggingFace ===\n")
    example_with_huggingface()
    
    print("\n=== Example 6: With Recursive URL ===\n")
    example_with_recursive_url()