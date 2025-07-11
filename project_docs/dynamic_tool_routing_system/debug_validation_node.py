"""Debug the validation node to understand how it handles tool routing."""

import logging

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.tools import tool

from haive.agents.simple.agent import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig


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


def debug_validation_node():
    """Debug how validation node handles tool routing."""
    # Create agent with initial tool
    engine = AugLLMConfig(
        tools=[calculate], system_message="You are a helpful assistant."
    )
    agent = SimpleAgent(name="test_agent", engine=engine)

    # Build graph and get validation node
    graph = agent.build_graph()

    # Find validation node
    validation_node = None
    for node_name, node in graph.nodes.items():
        if node_name == "validation":
            validation_node = node
            break

    if validation_node:

        # Check if it has config
        if hasattr(validation_node, "config"):
            pass

        # Check if it has metadata
        if hasattr(validation_node, "metadata"):
            pass

    # Add a tool and rebuild
    engine.add_tool(search)
    new_graph = agent.build_graph()

    new_validation_node = None
    for node_name, node in new_graph.nodes.items():
        if node_name == "validation":
            new_validation_node = node
            break

    if new_validation_node:

        # Check if the validation node changed

        # Check tool routes in validation node
        if hasattr(new_validation_node, "config"):
            config = new_validation_node.config
            if hasattr(config, "tool_routes"):
                pass

        # Check if validation node has access to engine tool routes
        if hasattr(new_validation_node, "metadata"):
            metadata = new_validation_node.metadata
            if "tool_routes" in metadata:
                pass

    # Test with a mock tool call

    # Create a mock state with tool call
    mock_state = {
        "messages": [
            HumanMessage(content="Calculate 2+2"),
            AIMessage(
                content="I'll help you calculate that.",
                tool_calls=[
                    {
                        "name": "calculate",
                        "args": {"expression": "2+2"},
                        "id": "test_call_1",
                    }
                ],
            ),
        ]
    }

    # Try to call validation node
    try:
        if callable(new_validation_node):
            new_validation_node(mock_state)
        else:
            pass
    except Exception:
        pass

    # Test with search tool call

    search_state = {
        "messages": [
            HumanMessage(content="Search for information"),
            AIMessage(
                content="I'll search for that.",
                tool_calls=[
                    {
                        "name": "search",
                        "args": {"query": "test query"},
                        "id": "test_call_2",
                    }
                ],
            ),
        ]
    }

    try:
        if callable(new_validation_node):
            new_validation_node(search_state)
        else:
            pass
    except Exception:
        pass


if __name__ == "__main__":
    debug_validation_node()
