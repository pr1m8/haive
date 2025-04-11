"""
Examples demonstrating how to use the SourceFinderAgent in different scenarios.
"""

import os
from typing import List, Dict, Any
import logging

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma, FAISS
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from src.haive.core.engine.aug_llm import AugLLMConfig
from src.haive.core.models.llm.base import AzureLLMConfig
from src.haive.agents.flstaesr.fetch.agent import (
    create_source_finder_agent,
    create_web_search_tool,
    create_github_search_tool,
    create_docs_search_tool,
    SourceToRAGProcessor
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Example 1: Basic usage with default configuration
def basic_usage_example():
    """Basic usage of the SourceFinderAgent with default settings."""
    # Create the agent
    agent = create_source_finder_agent(
        system_prompt="You are a research assistant that finds the best sources for user queries.",
        max_sources_to_load=3
    )
    
    # Run the agent with a query
    query = "What are the best practices for implementing RAG with LangChain?"
    result = agent.run(query)
    
    # Print the result
    print("Basic Usage Example Result:")
    print(f"Loaded {len(result.get('loaded_documents', []))} documents")
    print(f"Created {len(result.get('chunked_documents', []))} chunks")
    
    # Print the messages
    for msg in result.get('messages', []):
        if hasattr(msg, 'content'):
            print(f"{msg.type.upper()}: {msg.content[:100]}...")
    
    return result

# Example 2: Advanced configuration with embeddings and vector store
def advanced_usage_example():
    """Advanced usage with embeddings and vector store integration."""
    # Initialize embeddings model
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2"
    )
    
    # Create the agent with advanced configuration
    agent = create_source_finder_agent(
        system_prompt="You are a research assistant specialized in technical documentation.",
        max_sources_to_load=5,
        chunk_size=500,  # Smaller chunks for more granular retrieval
        chunk_overlap=100,
        embeddings=embeddings,
        vectorstore_class=FAISS,  # Use FAISS for in-memory vector storage
        create_vectorstore=True,
        skip_analysis=False,  # Don't skip the analysis step
        skip_chunking=False,
    )
    
    # Run the agent with a technical query
    query = "How do I implement a custom agent using LangGraph?"
    result = agent.run(query)
    
    # Print the result
    print("\nAdvanced Usage Example Result:")
    print(f"Loaded {len(result.get('loaded_documents', []))} documents")
    print(f"Created {len(result.get('chunked_documents', []))} chunks")
    print(f"Created vector store: {result.get('embedded_documents', False)}")
    
    # If retriever was created, test it
    retriever = result.get('retriever')
    if retriever:
        retrieved_docs = retriever.get_relevant_documents(query)
        print(f"Retrieved {len(retrieved_docs)} relevant documents")
        
        # Print snippets from the top documents
        for i, doc in enumerate(retrieved_docs[:2]):
            print(f"\nDocument {i+1} snippet: {doc.page_content[:200]}...")
    
    return result

# Example 3: Integration with a RAG pipeline
def rag_integration_example():
    """Example of integrating SourceFinderAgent with a RAG pipeline."""
    # Initialize embeddings model
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2"
    )
    
    # Create source finder agent
    agent = create_source_finder_agent(
        system_prompt="You are a research assistant that finds sources for RAG processing.",
        max_sources_to_load=3,
        embeddings=embeddings,
        vectorstore_class=FAISS,
        create_vectorstore=True
    )
    
    # Create RAG processor
    rag_processor = SourceToRAGProcessor(
        source_finder=agent,
        embedding_model=embeddings,
        vector_store_cls=FAISS
    )
    
    # Create RAG chain
    def create_rag_chain(llm_config):
        # Create the RAG prompt
        rag_prompt = ChatPromptTemplate.from_template(
            """You are a helpful AI assistant who provides accurate information based on the retrieved documents.
            
            Context information from retrieved documents:
            {context}
            
            User question: {question}
            
            Please provide a comprehensive answer using only the information in the retrieved documents. 
            If the documents don't contain relevant information, acknowledge this limitation.
            """
        )
        
        # Create the LLM
        llm = llm_config.instantiate_llm()
        
        # Create the RAG chain
        return (
            {"context": lambda x: x["context"], "question": lambda x: x["question"]}
            | rag_prompt
            | llm
            | StrOutputParser()
        )
    
    # Create Azure OpenAI LLM config
    llm_config = AugLLMConfig(
        name="rag_llm",
        llm_config=AzureLLMConfig(
            model="gpt-4o",
            parameters={"temperature": 0.3}
        )
    )
    
    # Create the RAG chain
    rag_chain = create_rag_chain(llm_config)
    
    # Process a query
    query = "What are the key components of the LangChain framework?"
    
    # Get relevant documents
    relevant_docs = rag_processor.retrieve_relevant_documents(query, k=5)
    
    # Format documents for RAG
    docs_content = "\n\n".join([doc.page_content for doc in relevant_docs])
    
    # Run the RAG chain
    if docs_content:
        rag_result = rag_chain.invoke({
            "context": docs_content,
            "question": query
        })
        
        print("\nRAG Integration Example Result:")
        print(f"Query: {query}")
        print(f"Retrieved {len(relevant_docs)} documents")
        print(f"RAG Response: {rag_result[:200]}...")
    else:
        print("\nRAG Integration Example Result:")
        print("No documents retrieved for RAG processing")
    
    return {
        "query": query,
        "documents": relevant_docs,
        "rag_result": rag_result if docs_content else None
    }

# Example 4: Custom search tools and specialized configurations
def custom_search_example():
    """Example with custom search tools and specialized configurations."""
    # Configure custom search tools
    web_search = create_web_search_tool()
    github_search = create_github_search_tool()
    docs_search = create_docs_search_tool()
    
    # Create specialized LLM configurations for different steps
    analyze_query_llm = AugLLMConfig(
        name="analyze_query_llm",
        llm_config=AzureLLMConfig(
            model="gpt-4o",
            parameters={"temperature": 0.2}  # Low temperature for precise analysis
        )
    )
    
    source_selection_llm = AugLLMConfig(
        name="source_selection_llm",
        llm_config=AzureLLMConfig(
            model="gpt-4o",
            parameters={"temperature": 0.3}  # Balanced for good selection
        )
    )
    
    document_analysis_llm = AugLLMConfig(
        name="document_analysis_llm",
        llm_config=AzureLLMConfig(
            model="gpt-4o",
            parameters={"temperature": 0.4}  # More creative for analysis
        )
    )
    
    # Create the agent with custom configuration
    agent = create_source_finder_agent(
        name="technical_documentation_agent",
        system_prompt="You are a specialized research assistant focused on technical documentation and code.",
        search_tools=[web_search, github_search, docs_search],
        max_sources_to_load=5,
        analyze_query_llm=analyze_query_llm,
        source_selection_llm=source_selection_llm,
        document_analysis_llm=document_analysis_llm,
        include_web_search=True,
        include_github_search=True,
        include_docs_search=True
    )
    
    # Process different query types
    technical_query = "How do I implement parallel processing with asyncio in Python?"
    academic_query = "What are the latest developments in transformer-based language models?"
    
    # Run for technical query
    print("\nTechnical Query Example:")
    tech_result = agent.run(technical_query)
    print(f"Query: {technical_query}")
    print(f"Search strategy: {tech_result.get('query_state', {}).get('search_strategy', 'unknown')}")
    print(f"Routes taken: {tech_result.get('routes_taken', [])}")
    print(f"Loaded {len(tech_result.get('loaded_documents', []))} documents")
    
    # Run for academic query
    print("\nAcademic Query Example:")
    academic_result = agent.run(academic_query)
    print(f"Query: {academic_query}")
    print(f"Search strategy: {academic_result.get('query_state', {}).get('search_strategy', 'unknown')}")
    print(f"Routes taken: {academic_result.get('routes_taken', [])}")
    print(f"Loaded {len(academic_result.get('loaded_documents', []))} documents")
    
    return {
        "technical_result": tech_result,
        "academic_result": academic_result
    }

# Run the examples if executed directly
if __name__ == "__main__":
    print("Running Source Finder Agent Examples")
    print("=" * 50)
    
    # Run basic example
    basic_result = basic_usage_example()
    
    # Run advanced example
    advanced_result = advanced_usage_example()
    
    # Run RAG integration example
    rag_result = rag_integration_example()
    
    # Run custom search example
    custom_result = custom_search_example()
    
    print("\nAll examples completed successfully!")