"""Haive State Graph System.

This package provides a comprehensive graph implementation for the Haive framework,
with flexible node and branch management, visualization, and LangGraph integration.

The state graph system is the foundational computational graph infrastructure in Haive,
enabling the creation, manipulation, and execution of complex workflows with robust
state management and schema validation.

Key Features:
    - Schema Validation: Enforce type safety through Pydantic models
    - Dynamic Routing: Create complex workflows with conditional branching
    - Serialization: Full serialization and deserialization support
    - LangGraph Integration: Seamless integration with LangChain's LangGraph
    - Visualization: Built-in visualization capabilities
    - Pattern Support: Reusable graph patterns and templates

Modules:
    base_graph2: Core graph implementation (transitional version)
    schema_graph: Schema-aware graph with validation
    state_graph: State graph serialization model
    components: Node and branch implementations
    models: Data models for graph components
    conversion: Format conversion utilities
    pattern: Graph pattern implementations
    utils: Utility functions

Example:
    Basic graph creation:
    ```python
    from haive.core.graph.state_graph import BaseGraph
    from langgraph.graph import START, END

    # Create a new graph
    graph = BaseGraph(name="my_graph")

    # Add nodes
    graph.add_node("node1", lambda state: state)
    graph.add_node("node2", lambda state: state)

    # Add edges
    graph.add_edge(START, "node1")
    graph.add_edge("node1", "node2")
    graph.add_edge("node2", END)

    # Compile and run the graph
    compiled_graph = graph.compile()
    result = compiled_graph.invoke({"input": "some input"})
    ```
"""

# Base graph implementation
from haive.core.graph.state_graph.base_graph2 import BaseGraph

# Core components
from haive.core.graph.state_graph.components import Branch, Node

# Conversion utilities
from haive.core.graph.state_graph.conversion import convert_to_langgraph

# Visualization
from haive.core.graph.state_graph.graph_visualizer import GraphVisualizer
from haive.core.graph.state_graph.schema_graph import SchemaGraph

__all__ = [
    # Core classes
    "BaseGraph",
    "SchemaGraph",
    "Node",
    "Branch",
    # Conversion
    "convert_to_langgraph",
    # Visualization
    "GraphVisualizer",
]
