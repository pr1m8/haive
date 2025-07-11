"""Debug the validation node V2 setup and tool routing."""

import logging

from haive.agents.simple.agent import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.node.validation_node_config_v2 import \
    ValidationNodeConfigV2
from langchain_core.messages import AIMessage, HumanMessage
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


def debug_validation_node_v2():
    """Debug how V2 validation nodes handle tool routing."""
    # Create agent with initial tool
    engine = AugLLMConfig(
        tools=[calculate], system_message="You are a helpful assistant."
    )
    agent = SimpleAgent(name="test_agent", engine=engine)

    # Build graph and examine nodes
    graph = agent.build_graph()

    # Look at each node
    for _node_name, node in graph.nodes.items():

        # Check if it has a config
        if hasattr(node, "config"):
            config = node.config
            if hasattr(config, "tool_routes"):
                pass

        # Check metadata
        if hasattr(node, "metadata"):
            metadata = node.metadata
            if "callable" in metadata:
                callable_func = metadata["callable"]

    # Check if we can create a ValidationNodeConfigV2 directly
    try:
        validation_config = ValidationNodeConfigV2(
            name="test_validation", tool_routes=agent.engine.tool_routes
        )

        # Try to call the validation node
        validation_node = validation_config.create_runnable()

    except Exception:
        pass

    # Add a tool and rebuild
    engine.add_tool(search)

    new_graph = agent.build_graph()

    # Check validation node again
    if "validation" in new_graph.nodes:
        validation_node = new_graph.nodes["validation"]

        if hasattr(validation_node, "config"):
            config = validation_node.config
            if hasattr(config, "tool_routes"):
                pass

    # Test tool call processing

    # Create mock state with tool call
    mock_state = {
        "messages": [
            HumanMessage(content="Calculate 2+2"),
            AIMessage(
                content="I'll calculate that.",
                tool_calls=[
                    {
                        "name": "calculate",
                        "args": {"expression": "2+2"},
                        "id": "test_call_1",
                    }
                ],
            ),
        ],
        "tool_routes": engine.tool_routes,  # Add tool routes to state
    }

    # Try to process with validation node
    if "validation" in new_graph.nodes:
        validation_node = new_graph.nodes["validation"]

        # Get the actual callable
        if (
            hasattr(validation_node, "metadata")
            and "callable" in validation_node.metadata
        ):
            callable_func = validation_node.metadata["callable"]

            try:
                result = callable_func(mock_state)
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
        ],
        "tool_routes": engine.tool_routes,
    }

    if "validation" in new_graph.nodes:
        validation_node = new_graph.nodes["validation"]

        if (
            hasattr(validation_node, "metadata")
            and "callable" in validation_node.metadata
        ):
            callable_func = validation_node.metadata["callable"]

            try:
                callable_func(search_state)
            except Exception:
                pass


if __name__ == "__main__":
    debug_validation_node_v2()
