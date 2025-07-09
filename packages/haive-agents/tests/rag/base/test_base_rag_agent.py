"""Test the integration between retriever engines and RAG agents."""

import logging

import pytest
from haive.core.engine.retriever import VectorStoreRetrieverConfig
from haive.core.engine.vectorstore import VectorStoreConfig, VectorStoreProvider
from haive.core.graph.node.config import NodeConfig
from haive.core.graph.node.factory import NodeFactory

# Import from our architecture
from haive.core.models.embeddings.base import HuggingFaceEmbeddingConfig
from langchain_core.documents import Document
from rich.console import Console
from rich.logging import RichHandler
from rich.panel import Panel
from rich.pretty import Pretty

from haive.agents.rag.base.agent import BaseRAGAgent
from haive.agents.rag.base.config import BaseRAGConfig

# Set up rich console for output
console = Console()
debug_console = Console(stderr=True)

# Configure rich logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True, console=debug_console)],
)

# Get loggers
logger = logging.getLogger("rag_test")
node_logger = logging.getLogger("haive.core.graph.node")
factory_logger = logging.getLogger("haive.core.graph.node.factory")

# Set log levels
node_logger.setLevel(logging.DEBUG)
factory_logger.setLevel(logging.DEBUG)


@pytest.fixture(scope="module")
def sample_documents():
    """Create sample documents for testing."""
    console.print(
        Panel.fit("Creating sample documents", title="Setup", border_style="blue")
    )

    documents = [
        Document(
            page_content="LangChain is a framework for developing applications powered by language models.",
            metadata={"source": "docs", "section": "intro"},
        ),
        Document(
            page_content="It provides tools and abstractions for working with LLMs and other components.",
            metadata={"source": "docs", "section": "intro"},
        ),
        Document(
            page_content="LangGraph is part of the LangChain ecosystem for building stateful agent workflows.",
            metadata={"source": "docs", "section": "langgraph"},
        ),
        Document(
            page_content="Agents are systems that use LLMs to determine which actions to take.",
            metadata={"source": "docs", "section": "agents"},
        ),
        Document(
            page_content="RAG (Retrieval Augmented Generation) combines retrieval with generation.",
            metadata={"source": "docs", "section": "rag"},
        ),
    ]

    console.print(f"Created {len(documents)} test documents")
    return documents


@pytest.fixture(scope="module")
def vectorstore_config(sample_documents):
    """Create a vector store config with sample documents."""
    console.print(
        Panel.fit("Creating vector store config", title="Setup", border_style="blue")
    )

    # Enable debug in NodeFactory
    NodeFactory.set_debug(True)

    vs_config = VectorStoreConfig(
        name="test_vector_store",
        documents=sample_documents,
        vector_store_provider=VectorStoreProvider.FAISS,
        embedding_model=HuggingFaceEmbeddingConfig(
            model="sentence-transformers/all-MiniLM-L6-v2"
        ),
    )

    console.print("Vector store config created")
    return vs_config


@pytest.fixture(scope="module")
def retriever_config(vectorstore_config):
    """Create a retriever config using the vector store."""
    console.print(
        Panel.fit("Creating retriever config", title="Setup", border_style="blue")
    )

    retriever_config = VectorStoreRetrieverConfig(
        name="test_retriever", vector_store_config=vectorstore_config, k=2
    )

    console.print("Retriever config created")
    return retriever_config


@pytest.fixture(scope="module")
def direct_vs_rag_agent(vectorstore_config):
    """Create a RAG agent that uses vectorstore directly."""
    console.print(
        Panel.fit(
            "Creating direct vectorstore RAG agent", title="Setup", border_style="blue"
        )
    )

    agent = BaseRAGAgent(
        BaseRAGConfig(
            name="direct_vectorstore_rag", retriever_config=vectorstore_config
        )
    )

    console.print("Direct vectorstore RAG agent created")
    return agent


@pytest.fixture(scope="module")
def explicit_retriever_rag_agent(retriever_config):
    """Create a RAG agent with an explicit retriever."""
    console.print(
        Panel.fit(
            "Creating explicit retriever RAG agent", title="Setup", border_style="blue"
        )
    )

    agent = BaseRAGAgent(
        BaseRAGConfig(name="explicit_retriever_rag", retriever_config=retriever_config)
    )

    console.print("Explicit retriever RAG agent created")
    return agent


def test_retriever_direct_invocation(retriever_config):
    """Test direct invocation of retriever engine."""
    console.print(
        Panel.fit(
            "Testing direct retriever invocation", title="Test", border_style="green"
        )
    )

    # Test invocation with string
    query = "What is LangChain?"
    console.print(f"Invoking retriever with query: '{query}'")

    result = retriever_config.invoke(query)

    console.print(f"Retrieved {len(result)} documents")
    console.print(f"Result type: {type(result).__name__}")

    if result:
        console.print("First document content:")
        console.print(f"[bold cyan]{result[0].page_content}[/bold cyan]")

    assert isinstance(result, list), "Result should be a list"
    assert len(result) > 0, "Should retrieve at least one document"
    assert hasattr(result[0], "page_content"), "Result should contain Document objects"


def test_node_function_creation(retriever_config):
    """Test creation of node function from retriever config."""
    console.print(
        Panel.fit("Testing node function creation", title="Test", border_style="green")
    )

    # Create node config
    node_config = NodeConfig(
        name="test_retriever_node",
        engine=retriever_config,
        input_mapping={"query": "query"},
        output_mapping={"documents": "retrieved_documents"},
    )

    console.print("Creating node function")
    node_func = NodeFactory.create_node_function(node_config, debug=True)

    console.print(f"Node function created: {node_func.__name__}")

    # Test with simple state
    state = {"query": "What is LangChain?"}
    console.print(f"Invoking node function with state: {state}")

    result = node_func(state)

    console.print(f"Result type: {type(result).__name__}")

    # Display result details
    if hasattr(result, "update"):
        console.print("Result has update field:")
        console.print(Pretty(list(result.update.keys())))

        if "retrieved_documents" in result.update:
            docs = result.update["retrieved_documents"]
            console.print(f"Retrieved {len(docs)} documents")

            if docs:
                console.print("First document:")
                console.print(f"[bold cyan]{docs[0].page_content}[/bold cyan]")

    assert hasattr(result, "update"), "Result should have update field"
    assert (
        "retrieved_documents" in result.update
    ), "Update should contain retrieved_documents"
    assert len(result.update["retrieved_documents"]) > 0, "Should retrieve documents"


def test_direct_vs_rag_agent(direct_vs_rag_agent):
    """Test the RAG agent that uses vectorstore directly."""
    console.print(
        Panel.fit(
            "Testing direct vectorstore RAG agent", title="Test", border_style="green"
        )
    )

    query = {"query": "What is LangChain?"}
    console.print(f"Running agent with query: {query}")

    result = direct_vs_rag_agent.run(query)

    console.print(f"Result keys: {list(result.keys())}")

    assert "retrieved_documents" in result, "Result should contain retrieved_documents"
    assert len(result["retrieved_documents"]) > 0, "Should retrieve documents"

    console.print(f"Retrieved {len(result['retrieved_documents'])} documents")
    if result["retrieved_documents"]:
        console.print("First document:")
        console.print(
            f"[bold cyan]{result['retrieved_documents'][0].page_content}[/bold cyan]"
        )


def test_explicit_retriever_rag_agent(explicit_retriever_rag_agent):
    """Test the RAG agent with explicit retriever."""
    console.print(
        Panel.fit(
            "Testing explicit retriever RAG agent", title="Test", border_style="green"
        )
    )

    query = {"query": "What is LangGraph?"}
    console.print(f"Running agent with query: {query}")

    result = explicit_retriever_rag_agent.run(query)

    console.print(f"Result keys: {list(result.keys())}")

    assert "retrieved_documents" in result, "Result should contain retrieved_documents"
    assert len(result["retrieved_documents"]) > 0, "Should retrieve documents"

    console.print(f"Retrieved {len(result['retrieved_documents'])} documents")
    if result["retrieved_documents"]:
        console.print("First document:")
        console.print(
            f"[bold cyan]{result['retrieved_documents'][0].page_content}[/bold cyan]"
        )


def test_different_input_formats(explicit_retriever_rag_agent):
    """Test the RAG agent with different input formats."""
    console.print(
        Panel.fit("Testing different input formats", title="Test", border_style="green")
    )

    # Test with dict containing query
    input1 = {"query": "What is retrieval?"}
    console.print(f"Testing with dict input: {input1}")
    result1 = explicit_retriever_rag_agent.run(input1)
    assert "retrieved_documents" in result1, "Result should contain retrieved_documents"

    # Test with string query (should be handled by BaseRAGAgent)
    input2 = "What are agents?"
    console.print(f"Testing with string input: '{input2}'")
    result2 = explicit_retriever_rag_agent.run(input2)
    assert "retrieved_documents" in result2, "Result should contain retrieved_documents"

    # Compare results
    console.print(
        f"Dict input retrieved {len(result1['retrieved_documents'])} documents"
    )
    console.print(
        f"String input retrieved {len(result2['retrieved_documents'])} documents"
    )


def test_alternative_mapping(retriever_config):
    """Test retriever with alternative input/output mapping."""
    console.print(
        Panel.fit("Testing alternative mapping", title="Test", border_style="green")
    )

    # Create node config with different mapping
    node_config = NodeConfig(
        name="alt_mapping_node",
        engine=retriever_config,
        input_mapping={"question": "query"},  # Map state.question to query
        output_mapping={
            "documents": "search_results"
        },  # Map documents to search_results
    )

    console.print("Creating node function with alternative mapping")
    node_func = NodeFactory.create_node_function(node_config, debug=True)

    # Test with matching state
    state = {"question": "What is RAG?"}
    console.print(f"Invoking with state: {state}")

    result = node_func(state)

    assert hasattr(result, "update"), "Result should have update field"
    assert "search_results" in result.update, "Update should contain search_results"

    console.print(f"Retrieved {len(result.update['search_results'])} documents")
    console.print(
        "Mapping correctly applied state.question → query → documents → state.search_results"
    )


def test_error_handling(retriever_config):
    """Test error handling in retriever nodes."""
    console.print(
        Panel.fit("Testing error handling", title="Test", border_style="green")
    )

    # Create test with empty state
    node_config = NodeConfig(
        name="error_test_node",
        engine=retriever_config,
        input_mapping={"missing_field": "query"},  # This field doesn't exist
    )

    console.print("Creating node function")
    node_func = NodeFactory.create_node_function(node_config, debug=True)

    # Test with empty state
    state = {}
    console.print(f"Invoking with empty state: {state}")

    # This should handle the error gracefully
    result = node_func(state)
    console.print(f"Result type: {type(result).__name__}")

    # Check if error is handled properly
    if hasattr(result, "update") and "error" in result.update:
        console.print(f"Error properly handled: {result.update['error']}")

    # The test passes if no exception is raised
    assert True, "Function should handle errors without crashing"
