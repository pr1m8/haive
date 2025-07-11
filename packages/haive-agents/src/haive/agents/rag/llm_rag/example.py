"""Example usage of the LLM RAG Agent.

This script demonstrates how to:
1. Create and configure an LLM RAG agent
2. Run queries and access the results
3. Customize the agent's behavior
"""

import logging
import uuid
from pathlib import Path

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.engine.retriever import VectorStoreRetrieverConfig
from haive.core.engine.vectorstore import VectorStoreConfig, VectorStoreProvider
from langchain.schema import Document
from langchain_core.prompts import ChatPromptTemplate

from haive.agents.rag.llm_rag.agent import LLMRAGAgent
from haive.agents.rag.llm_rag.config import LLMRAGConfig

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Sample documents to populate our vector store
SAMPLE_DOCUMENTS = [
    Document(
        page_content="Python is a high-level programming language known for its readability and versatility. "
        "It supports multiple programming paradigms, including procedural, object-oriented, and functional programming.",
        metadata={"source": "programming_docs", "topic": "python"},
    ),
    Document(
        page_content="JavaScript is a scripting language that enables dynamic content on web pages. "
        "It is an essential part of web applications and runs in the browser.",
        metadata={"source": "programming_docs", "topic": "javascript"},
    ),
    Document(
        page_content="Machine learning is a subset of artificial intelligence that provides systems the ability to "
        "learn and improve from experience without being explicitly programmed.",
        metadata={"source": "ai_docs", "topic": "machine_learning"},
    ),
    Document(
        page_content="Deep learning is part of a broader family of machine learning methods based on artificial neural networks. "
        "It uses multiple layers to progressively extract higher-level features from raw input.",
        metadata={"source": "ai_docs", "topic": "deep_learning"},
    ),
    Document(
        page_content="The Large Language Model (LLM) is a type of AI model designed to understand and generate human language. "
        "Examples include GPT-4, Claude, and LLaMA.",
        metadata={"source": "ai_docs", "topic": "llm"},
    ),
]


def create_llm_rag_agent(use_relevance_checker=True, return_documents=3):
    """Creates and configures an LLM RAG agent.

    Args:
        use_relevance_checker (bool): Whether to include a relevance checking component
        return_documents (int): Number of documents to retrieve

    Returns:
        LLMRAGAgent: Configured agent instance
    """
    # Create a unique ID for this example
    session_id = uuid.uuid4().hex[:8]
    vs_path = f"example_vectorstore_{session_id}"

    # Step 1: Create a vector store with our sample documents
    vector_store = VectorStoreConfig(
        name=f"example_vectorstore_{session_id}",
        documents=SAMPLE_DOCUMENTS,
        vector_store_provider=VectorStoreProvider.FAISS,
        vector_store_path=vs_path,
    )

    # Step 2: Create a retriever configuration
    retriever = VectorStoreRetrieverConfig(
        name=f"example_retriever_{session_id}",
        vector_store_config=vector_store,
        k=return_documents,  # Number of documents to retrieve
    )

    # Step 3: Define LLM configurations

    # Main LLM for answering
    answer_prompt = """You are a helpful AI assistant that answers questions based on the provided context.

Question: {query}
Context: {context}

First, analyze whether the context contains relevant information to answer the question.
If the context is relevant, provide a concise and accurate answer using only the information in the context.
If the context is not relevant or doesn't contain enough information, simply state that you don't have enough information.

Answer:"""

    llm_config = AugLLMConfig(
        name=f"answer_llm_{session_id}",
        prompt_template=ChatPromptTemplate.from_template(answer_prompt),
    )

    # Relevance checker LLM (optional)
    relevance_prompt = """Determine if the following documents are relevant to the question.

Question: {query}
Documents: {documents}

Are these documents relevant to the question? Answer with just 'Yes' or 'No'.
Only answer 'Yes' if the documents contain information that directly helps answer the question."""

    relevance_checker = None
    if use_relevance_checker:
        relevance_checker = AugLLMConfig(
            name=f"relevance_checker_{session_id}",
            prompt_template=ChatPromptTemplate.from_template(relevance_prompt),
        )

    # Step 4: Create the agent configuration
    agent_config = LLMRAGConfig(
        name=f"llm_rag_agent_{session_id}",
        description="Example LLM RAG agent",
        retriever_config=retriever,
        llm_config=llm_config,
        relevance_checker_config=relevance_checker,
    )

    # Step 5: Create and return the agent
    agent = LLMRAGAgent(agent_config)

    logger.info(f"Created LLM RAG agent with ID: {session_id}")
    logger.info(f"Vector store path: {vs_path}")
    logger.info(f"Using relevance checker: {use_relevance_checker}")
    logger.info(f"Documents to retrieve: {return_documents}")

    return agent


def run_example_queries(agent):
    """Run a set of example queries against the agent.

    Args:
        agent: The LLM RAG agent to query
    """
    # Example queries with different expected behaviors
    example_queries = [
        "What is Python programming language?",  # Should find relevant docs
        "What are the key features of JavaScript?",  # Should find relevant docs
        "How does machine learning work?",  # Should find relevant docs
        "What is the capital of France?",  # Should NOT find relevant docs
        "Tell me about large language models.",  # Should find relevant docs
    ]

    results = []

    # Run each query and collect results
    for i, query in enumerate(example_queries):
        logger.info(f"\n\n--- Query {i+1}: '{query}' ---")

        # Create input state with just the query
        input_state = {"query": query}

        # Invoke the agent
        result = agent.invoke(input_state)

        # Log the result
        logger.info(f"Retrieved {len(result.get('retrieved_documents', []))} documents")
        logger.info(f"Documents relevant: {result.get('is_relevant', False)}")
        logger.info(f"Answer: {result.get('answer', 'No answer generated')}")

        # Store results for comparison
        results.append(
            {
                "query": query,
                "doc_count": len(result.get("retrieved_documents", [])),
                "is_relevant": result.get("is_relevant", False),
                "answer": result.get("answer", "No answer generated"),
            }
        )

    return results


def compare_agent_configurations():
    """Compare different agent configurations side by side."""
    logger.info("\n\n=== Comparing Agent Configurations ===\n")

    # Configuration 1: With relevance checker, 2 documents
    logger.info("Creating agent with relevance checker, retrieving 2 documents")
    agent1 = create_llm_rag_agent(use_relevance_checker=True, return_documents=2)

    # Configuration 2: Without relevance checker, 3 documents
    logger.info("\nCreating agent without relevance checker, retrieving 3 documents")
    agent2 = create_llm_rag_agent(use_relevance_checker=False, return_documents=3)

    # Run a test query on both
    test_query = "What are the main types of machine learning?"

    logger.info("\n--- Running test query on both configurations ---")
    logger.info(f"Query: '{test_query}'")

    # Run on first configuration
    logger.info("\nResults from agent with relevance checker:")
    result1 = agent1.invoke({"query": test_query})
    logger.info(f"Retrieved {len(result1.get('retrieved_documents', []))} documents")
    logger.info(f"Documents relevant: {result1.get('is_relevant', False)}")
    logger.info(f"Answer: {result1.get('answer', 'No answer generated')}")

    # Run on second configuration
    logger.info("\nResults from agent without relevance checker:")
    result2 = agent2.invoke({"query": test_query})
    logger.info(f"Retrieved {len(result2.get('retrieved_documents', []))} documents")
    logger.info(f"Documents relevant: {result2.get('is_relevant', False)}")
    logger.info(f"Answer: {result2.get('answer', 'No answer generated')}")

    logger.info("\n=== Comparison Complete ===")


def main():
    """Main function to run the example."""
    logger.info("=== LLM RAG Agent Example ===\n")

    # Create an agent with default configuration
    agent = create_llm_rag_agent()

    # Run example queries
    run_example_queries(agent)

    # Compare different configurations
    compare_agent_configurations()

    logger.info("\n=== Example Complete ===")

    # Clean up temporary files
    # Note: In a real application, you might want to keep these files
    try:
        import shutil

        for path in Path(".").glob("example_vectorstore_*"):
            if path.is_dir():
                shutil.rmtree(path)
        logger.info("Cleaned up temporary files")
    except Exception as e:
        logger.warning(f"Failed to clean up temporary files: {e}")


if __name__ == "__main__":
    main()
