"""
Test module for the graph_visualization_utils.py module.

This demonstrates how to use the enhanced visualization functionality
with DynamicGraph instances.
"""

import logging
import uuid

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
from langchain_core.documents import Document
from langgraph.graph import END, START

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.engine.retriever import BaseRetrieverConfig, RetrieverType
from haive.core.engine.vectorstore import VectorStoreConfig

# Adjust these imports to match your project structure
from haive.core.graph.dynamic_graph_builder import DynamicGraph
from haive.core.models.retriever.base import RetrieverType


# Import the visualization utils
# from haive.core.graph.utils.mermaid_visualizer import visualize_graph, replace_visualization_method
def create_sample_graph():
    """Create a sample graph for testing visualization."""

    # Create sample engines
    llm_engine = AugLLMConfig(
        name="gpt4_engine", id="llm-" + uuid.uuid4().hex[:8], model="gpt-4o"
    )

    retriever_engine = BaseRetrieverConfig(
        name="retriever_engine", id="retriever-" + uuid.uuid4().hex[:8]
    )

    vectorstore_engine = VectorStoreConfig(
        name="vectorstore_engine",
        id="vectorstore-" + uuid.uuid4().hex[:8],
        documents=[
            Document(page_content="The capital of France is Paris."),
            Document(page_content="The capital of Germany is Berlin."),
            Document(page_content="The capital of Italy is Rome."),
            Document(page_content="The capital of Spain is Madrid."),
            Document(page_content="The capital of Portugal is Lisbon."),
            Document(page_content="The capital of Greece is Athens."),
        ],
    )

    retrieve_engine = BaseRetrieverConfig(
        name="retrieve_engine",
        id="retrieve-" + uuid.uuid4().hex[:8],
        retriever_type=RetrieverType.VECTOR_STORE,
        vector_store_config=vectorstore_engine,
    )

    # Create a graph
    graph = DynamicGraph(
        name="TestRAGWorkflow",
        components=[llm_engine, retriever_engine, vectorstore_engine, retrieve_engine],
        description="A test RAG workflow for visualization",
        visualize=True,
        debug_level="verbose",
    )

    # Create a basic RAG workflow
    graph.add_node("query_understanding", llm_engine)
    graph.add_node("retrieve", retriever_engine)
    graph.add_node("generate", llm_engine, command_goto=END)

    # Add a tool node with custom function
    def process_results(state):
        """Process retrieval results."""
        # In a real implementation, this would process the documents
        return {"processed_results": True}

    graph.add_node("process_results", process_results)

    # Create a simple, linear flow
    graph.add_edge(START, "query_understanding")

    # Add a conditional branch
    def route_by_query_complexity(state):
        """Route based on query complexity."""
        # In a real implementation, this would analyze the query
        query_length = len(state.get("query", ""))
        if query_length > 100:
            return "complex"
        elif query_length > 50:
            return "medium"
        else:
            return "simple"

    # Add branching nodes with clear names and configurations
    graph.add_node("complex_retrieval", retriever_engine, config_overrides={"k": 10})
    graph.add_node("simple_retrieval", retriever_engine, config_overrides={"k": 3})
    graph.add_node("medium_retrieval", retrieve_engine)

    # Add conditional routing - this will create the conditional edges
    graph.add_conditional_edges(
        "query_understanding",
        route_by_query_complexity,
        {
            "complex": "complex_retrieval",
            "simple": "simple_retrieval",
            "medium": "medium_retrieval",
        },
    )

    # Connect all branches back to process_results
    graph.add_edge("complex_retrieval", "process_results")
    graph.add_edge("simple_retrieval", "process_results")
    graph.add_edge("medium_retrieval", "process_results")

    # Connect process_results to generate (final step)
    graph.add_edge("process_results", "generate")

    # Compile the graph to check for errors
    try:
        graph.compile()
        print("Graph compiled successfully.")
    except Exception as e:
        print(f"Compilation error: {e}")

    return graph


def test_direct_visualization():
    """Test direct visualization without replacing methods."""
    print("\n=== Testing Direct Visualization ===")

    # Create sample graph
    graph = create_sample_graph()
    graph.visualize_graph()


def main():
    """Main test function."""
    print("=== Graph Visualization Test ===")

    # Run tests
    test_direct_visualization()
    test_method_replacement()

    print("\n=== All Tests Completed ===")


if __name__ == "__main__":
    main()
