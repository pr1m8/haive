"""Example usage of the MermaidGenerator for visualizing state graphs.

This module provides examples of how to use the MermaidGenerator
for visualizing different types of state graphs.
"""

import os

from haive.core.graph.state_graph import MermaidGenerator, StateGraph
from haive.core.utils.mermaid_utils import display_mermaid, mermaid_to_png


def simple_graph_example():
    """Example of visualizing a simple state graph."""
    # Create a simple graph
    graph = StateGraph(name="SimpleExample")

    # Add some nodes
    graph.add_node("process_input", lambda state, config: state)
    graph.add_node("extract_entities", lambda state, config: state)
    graph.add_node("analyze_sentiment", lambda state, config: state)
    graph.add_node("generate_response", lambda state, config: state)

    # Add edges to connect nodes
    graph.add_edge("START", "process_input")
    graph.add_edge("process_input", "extract_entities")
    graph.add_edge("extract_entities", "analyze_sentiment")
    graph.add_edge("analyze_sentiment", "generate_response")
    graph.add_edge("generate_response", "END")

    # Generate a Mermaid diagram
    mermaid_code = MermaidGenerator.generate(
        graph=graph, highlight_nodes=["extract_entities"], theme="default"
    )

    # Display the diagram
    display_mermaid(mermaid_code)

    # Save as PNG
    output_dir = os.path.join(os.getcwd(), "graph_examples")
    os.makedirs(output_dir, exist_ok=True)
    mermaid_to_png(mermaid_code, os.path.join(output_dir, "simple_graph.png"))

    return graph, mermaid_code


def branching_graph_example():
    """Example of visualizing a graph with branches."""
    # Create a graph with branches
    graph = StateGraph(name="BranchingExample")

    # Add some nodes
    graph.add_node("check_input", lambda state, config: state)
    graph.add_node("process_text", lambda state, config: state)
    graph.add_node("process_image", lambda state, config: state)
    graph.add_node("process_audio", lambda state, config: state)
    graph.add_node("generate_response", lambda state, config: state)

    # Add a branch based on input type
    graph.add_branch(
        "input_type_branch",
        source_node="check_input",
        destinations={
            "text": "process_text",
            "image": "process_image",
            "audio": "process_audio",
        },
        default="process_text",
    )

    # Connect the rest of the graph
    graph.add_edge("START", "check_input")
    graph.add_edge("process_text", "generate_response")
    graph.add_edge("process_image", "generate_response")
    graph.add_edge("process_audio", "generate_response")
    graph.add_edge("generate_response", "END")

    # Generate a Mermaid diagram
    mermaid_code = MermaidGenerator.generate(graph=graph, theme="forest")

    # Display the diagram
    display_mermaid(mermaid_code)

    return graph, mermaid_code


def nested_subgraph_example():
    """Example of visualizing a graph with nested subgraphs."""
    # Create main graph
    main_graph = StateGraph(name="MainGraph")

    # Create first level subgraph
    preprocessing = StateGraph(name="Preprocessing")
    preprocessing.add_node("tokenize", lambda state, config: state)
    preprocessing.add_node("normalize", lambda state, config: state)
    preprocessing.add_edge("START", "tokenize")
    preprocessing.add_edge("tokenize", "normalize")
    preprocessing.add_edge("normalize", "END")

    # Create second level nested subgraph
    analysis = StateGraph(name="Analysis")

    # Create third level nested subgraph
    entity_analysis = StateGraph(name="EntityAnalysis")
    entity_analysis.add_node("extract_entities", lambda state, config: state)
    entity_analysis.add_node("classify_entities", lambda state, config: state)
    entity_analysis.add_edge("START", "extract_entities")
    entity_analysis.add_edge("extract_entities", "classify_entities")
    entity_analysis.add_edge("classify_entities", "END")

    # Add entity_analysis as a subgraph to analysis
    analysis.add_subgraph("entity_analysis", entity_analysis)
    analysis.add_node("sentiment_analysis", lambda state, config: state)
    analysis.add_edge("START", "entity_analysis")
    analysis.add_edge("entity_analysis", "sentiment_analysis")
    analysis.add_edge("sentiment_analysis", "END")

    # Add preprocessing and analysis as subgraphs to main graph
    main_graph.add_subgraph("preprocessing", preprocessing)
    main_graph.add_subgraph("analysis", analysis)
    main_graph.add_node("generate_response", lambda state, config: state)

    # Connect everything in the main graph
    main_graph.add_edge("START", "preprocessing")
    main_graph.add_edge("preprocessing", "analysis")
    main_graph.add_edge("analysis", "generate_response")
    main_graph.add_edge("generate_response", "END")

    # Generate a Mermaid diagram with different max_depth values
    for depth in range(1, 4):
        mermaid_code = MermaidGenerator.generate(
            graph=main_graph, max_depth=depth, theme="default"
        )

        # Display the diagram
        display_mermaid(mermaid_code, width="100%")

        # Save as PNG
        output_dir = os.path.join(os.getcwd(), "graph_examples")
        os.makedirs(output_dir, exist_ok=True)
        mermaid_to_png(
            mermaid_code, os.path.join(output_dir, f"nested_graph_depth_{depth}.png")
        )

    return main_graph


if __name__ == "__main__":
    # Run all examples
    simple_graph_example()
    branching_graph_example()
    nested_subgraph_example()
