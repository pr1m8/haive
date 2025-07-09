"""Simple test for graph pattern integration.

This test directly tests pattern functionality without relying on fixtures.
"""

import logging

from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel

from haive.core.graph.patterns.base import GraphPattern, PatternMetadata

# Set up logging
logger = logging.getLogger(__name__)


# Create a simple state schema
class _TestState(BaseModel):
    """Simple state schema for tests."""

    message: str = ""


def test_minimal_pattern():
    """Test a minimal pattern configuration directly with StateGraph."""
    # Create a state graph with a schema
    graph = StateGraph(state_schema=dict)

    # Define a simple identity function for the node
    def identity_fn(state):
        return state

    # Add a node to the graph
    node_name = "test_node"
    graph.add_node(node_name, identity_fn)

    # Add START edge
    graph.add_edge(START, node_name)

    # Add END edge
    graph.add_edge(node_name, END)

    # Compile the graph
    compiled = graph.compile()

    # Verify the graph was compiled
    assert compiled is not None, "Graph failed to compile"

    # Run the graph with a simple state
    result = compiled.invoke({"message": "hello"})

    # Verify the result
    assert result is not None, "Graph execution failed"
    assert "message" in result, "Result missing expected field"
    assert result["message"] == "hello", "Result value incorrect"


def test_simple_pattern():
    """Test a simple pattern with direct StateGraph."""
    # Create a state graph with a schema
    graph = StateGraph(state_schema=dict)

    # Create a minimal pattern
    class MinimalPattern(GraphPattern):
        """Minimal test pattern."""

        def __init__(self):
            metadata = PatternMetadata(
                name="minimal_pattern",
                description="Minimal test pattern",
                pattern_type="test",
                required_components=[],
                parameters={},
            )
            super().__init__(metadata=metadata)

        def apply(self, graph, **kwargs):
            """Apply the pattern directly to a StateGraph."""
            # Add a simple node
            node_name = "pattern_node"

            # Define a simple function
            def simple_fn(state):
                return state

            # Add the node and edges
            graph.add_node(node_name, simple_fn)
            graph.add_edge(START, node_name)
            graph.add_edge(node_name, END)

            return True

    # Create and apply the pattern
    pattern = MinimalPattern()
    result = pattern.apply(graph)

    # Verify pattern application success
    assert result is True, "Pattern application failed"

    # Try to compile the graph
    compiled = graph.compile()
    assert compiled is not None, "Graph failed to compile"

    # Run the graph with a simple input
    input_data = {"test": "data"}
    output = compiled.invoke(input_data)

    # Verify output
    assert output == input_data, "Graph execution produced unexpected result"
