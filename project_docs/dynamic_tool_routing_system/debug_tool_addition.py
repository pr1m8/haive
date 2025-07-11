"""Debug script to understand tool addition and graph rebuilding."""

import logging

from haive.agents.simple.agent import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.tools import tool

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@tool
def calculate(expression: str) -> float:
    """Calculate a mathematical expression."""
    return eval(expression, {"__builtins__": {}}, {})


@tool
def search(query: str) -> str:
    """Search for information."""
    return f"Search results for: {query}"


@tool
def analyze(data: str) -> str:
    """Analyze data."""
    return f"Analysis of: {data}"


def debug_tool_addition():
    """Debug tool addition to SimpleAgent."""
    # Create initial engine with one tool
    engine = AugLLMConfig(
        tools=[calculate], system_message="You are a helpful assistant."
    )

    # Create agent
    agent = SimpleAgent(name="test_agent", engine=engine)

    # Build initial graph
    initial_graph = agent.build_graph()

    # Add a tool dynamically
    if hasattr(engine, "add_tool"):
        engine.add_tool(search)
    else:
        pass

    # Rebuild graph
    new_graph = agent.build_graph()

    # Check if nodes changed
    (set(initial_graph.nodes.keys()) if hasattr(initial_graph, "nodes") else set())
    set(new_graph.nodes.keys()) if hasattr(new_graph, "nodes") else set()

    # Add another tool
    if hasattr(engine, "add_tool"):
        engine.add_tool(analyze)

    # Final rebuild
    agent.build_graph()

    # Check engine structure

    # Check if tools are in the right place
    if hasattr(engine, "tools"):
        pass

    if hasattr(engine, "tool_routes"):
        pass


if __name__ == "__main__":
    debug_tool_addition()
