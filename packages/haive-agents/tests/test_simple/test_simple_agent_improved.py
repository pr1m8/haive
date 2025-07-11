"""Test SimpleAgent with improved validation node that can add ToolMessages."""

import uuid
from typing import Any, Dict, List, Optional, Sequence, Union

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.node.engine_node import EngineNodeConfig
from haive.core.graph.node.parser_node_config import ParserNodeConfig
from haive.core.graph.node.tool_node_config import ToolNodeConfig
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from langchain_core.messages import AIMessage, BaseMessage, ToolMessage
from langchain_core.tools import tool
from langgraph.graph import END, START
from langgraph.types import Command, Send
from pydantic import BaseModel, Field

from haive.agents.simple import SimpleAgent


# Test schemas
class Plan(BaseModel):
    """A plan with steps."""

    steps: list[str] = Field(description="A list of steps to complete the task")


# Test tools
@tool
def add_numbers(a: float, b: float) -> float:
    """Add two numbers together."""
    return a + b


def improved_validation_node(state: dict[str, Any]) -> Command:
    """Improved validation node that can add ToolMessages to state.

    This node replaces the conditional edge validation with a proper node
    that can update state by adding ToolMessages when needed.
    """

    # Get messages from state
    messages = state.get("messages", [])
    if not messages:
        return Command(goto=END)

    last_message = messages[-1]

    # Check if last message is AIMessage with tool calls
    if not isinstance(last_message, AIMessage) or not hasattr(
        last_message, "tool_calls"
    ):
        return Command(goto=END)

    tool_calls = getattr(last_message, "tool_calls", [])
    if not tool_calls:
        return Command(goto=END)

    # Get engine and tool routes
    engine_name = state.get("engine_name")
    tool_routes = state.get("tool_routes", {})

    if not engine_name:
        # Default engine name for SimpleAgent
        engine_name = "test_pydantic_engine"  # This should match engine config

    # Process each tool call
    new_messages = []
    destinations = []

    for tool_call in tool_calls:
        tool_name = tool_call.get("name")
        tool_id = tool_call.get("id")

        # Get route for this tool
        route = tool_routes.get(tool_name, "unknown")

        if route == "pydantic_model":
            # This is a Pydantic model - we need to parse it
            try:
                # Try to parse the args as the model
                args = tool_call.get("args", {})

                # For Plan model, validate the structure
                if tool_name == "Plan":
                    plan_data = Plan(**args)
                    # Create success ToolMessage
                    tool_msg = ToolMessage(
                        content=f"Successfully created plan with {len(plan_data.steps)} steps: {plan_data.steps}",
                        tool_call_id=tool_id,
                        name=tool_name,
                    )
                    new_messages.append(tool_msg)
                    destinations.append("parse_output")
                else:
                    # Unknown Pydantic model
                    tool_msg = ToolMessage(
                        content=f"Unknown Pydantic model: {tool_name}",
                        tool_call_id=tool_id,
                        name=tool_name,
                    )
                    new_messages.append(tool_msg)
                    destinations.append(END)

            except Exception as e:
                # Create error ToolMessage
                tool_msg = ToolMessage(
                    content=f"Error validating {tool_name}: {e!s}",
                    tool_call_id=tool_id,
                    name=tool_name,
                )
                new_messages.append(tool_msg)
                destinations.append(END)

        elif route in ["langchain_tool", "function", "tool_node"]:
            # This is a regular tool - route to tool_node
            destinations.append("tool_node")

        else:
            # Unknown tool - create error message
            tool_msg = ToolMessage(
                content=f"Unknown tool: {tool_name}",
                tool_call_id=tool_id,
                name=tool_name,
            )
            new_messages.append(tool_msg)
            destinations.append(END)

    # Update state with new messages
    update_dict = {}
    if new_messages:
        update_dict["messages"] = new_messages

    # Determine where to go next
    if not destinations:
        goto = END
    elif len(set(destinations)) == 1:
        # All tools go to same destination
        goto = destinations[0]
    elif "tool_node" in destinations:
        goto = "tool_node"
    elif "parse_output" in destinations:
        goto = "parse_output"
    else:
        goto = END

    return Command(update=update_dict, goto=goto)


class ImprovedSimpleAgent(SimpleAgent):
    """SimpleAgent with improved validation node that can add ToolMessages."""

    def build_graph(self) -> BaseGraph:
        """Build the agent graph with improved validation node."""
        graph = BaseGraph(name=self.name)

        # Track available nodes
        available_nodes = []

        # Add agent node
        engine_node = EngineNodeConfig(name="agent_node", engine=self.engine)
        graph.add_node("agent_node", engine_node)
        graph.add_edge(START, "agent_node")
        available_nodes.append("agent_node")

        # Check what nodes we need
        needs_tool_node = self._needs_tool_node()
        needs_parser_node = self._needs_parser_node()
        has_force_tool_use = self._has_force_tool_use()

        # Simple case - no tools
        if not needs_tool_node and not needs_parser_node:
            graph.add_edge("agent_node", END)
            graph.metadata["available_nodes"] = available_nodes
            return graph

        # Add improved validation node (as a proper node, not conditional edge)
        graph.add_node("validation", improved_validation_node)
        available_nodes.append("validation")

        # Add tool node if needed
        if needs_tool_node:
            tool_config = ToolNodeConfig(
                name="tool_node",
                engine_name=self.engine.name,
                allowed_routes=["langchain_tool", "function", "tool_node"],
            )
            graph.add_node("tool_node", tool_config)
            graph.add_edge("tool_node", END)
            available_nodes.append("tool_node")

        # Add parser node if needed
        if needs_parser_node:
            parser_config = ParserNodeConfig(
                name="parse_output",
                engine_name=self.engine.name,
            )
            graph.add_node("parse_output", parser_config)
            graph.add_edge("parse_output", END)
            available_nodes.append("parse_output")

        # Agent routing
        if has_force_tool_use:
            # Force tools - always go to validation
            graph.add_edge("agent_node", "validation")
        else:
            # Use conditional branching for tool calls
            def has_tool_calls(state) -> bool:
                """Check if the last AI message has tool calls."""
                messages = state.get("messages", [])
                if not messages:
                    return False

                last_msg = messages[-1]
                if not isinstance(last_msg, AIMessage):
                    return False

                tool_calls = getattr(last_msg, "tool_calls", None)
                return bool(tool_calls)

            graph.add_conditional_edges(
                "agent_node", has_tool_calls, {True: "validation", False: END}
            )

        # Store metadata
        graph.metadata["available_nodes"] = available_nodes
        graph.metadata["tool_routes"] = self.get_tool_routes()

        return graph

    def create_runnable(self, runnable_config=None):
        """Override to ensure state includes engine_name."""
        compiled = super().create_runnable(runnable_config)

        # Wrap the compiled graph to inject engine_name into state
        original_ainvoke = compiled.ainvoke

        async def wrapped_ainvoke(input_data, config=None):
            # Ensure engine_name is in the state
            if isinstance(input_data, dict) and "engine_name" not in input_data:
                input_data["engine_name"] = self.engine.name

            return await original_ainvoke(input_data, config)

        compiled.ainvoke = wrapped_ainvoke
        return compiled


# Test functions
async def test_improved_pydantic_validation():
    """Test the improved validation with Pydantic models."""

    # Create engine with Pydantic model
    engine = AugLLMConfig(
        id=f"engine_{uuid.uuid4().hex[:8]}",
        name="test_pydantic_engine",
        system_message="You are a helpful assistant that creates plans.",
        structured_output_model=Plan,
    )

    # Create improved agent
    agent = ImprovedSimpleAgent(
        name="test_agent",
        engine=engine,
        enable_persistence=False,
    )

    # Create initial state with Pydantic tool call
    initial_state = {
        "messages": [
            {"role": "user", "content": "Create a plan for making coffee"},
            {
                "role": "assistant",
                "content": "I'll create a plan for making coffee.",
                "tool_calls": [
                    {
                        "id": "call_123",
                        "name": "Plan",
                        "args": {
                            "steps": [
                                "Boil water",
                                "Grind coffee beans",
                                "Add coffee to filter",
                                "Pour hot water over coffee",
                                "Wait 4 minutes",
                                "Enjoy",
                            ]
                        },
                    }
                ],
            },
        ],
        "engine_name": engine.name,
        "tool_routes": {"Plan": "pydantic_model"},
    }

    # Run the agent
    graph = agent.create_runnable()
    result = await graph.ainvoke(initial_state)

    for i, msg in enumerate(result["messages"]):
        if hasattr(msg, "tool_call_id"):
            pass

    # Check if ToolMessage was created
    tool_messages = [msg for msg in result["messages"] if isinstance(msg, ToolMessage)]

    if len(tool_messages) > 0:
        tool_msg = tool_messages[0]
        return True
    print("❌ No ToolMessage found - validation failed")
    return False


async def test_improved_regular_tool_validation():
    """Test the improved validation with regular tools."""

    # Create engine with regular tools
    engine = AugLLMConfig(
        id=f"engine_{uuid.uuid4().hex[:8]}",
        name="test_tools_engine",
        system_message="You are a helpful math assistant.",
        tools=[add_numbers],
    )

    # Create improved agent
    agent = ImprovedSimpleAgent(
        name="test_agent",
        engine=engine,
        enable_persistence=False,
    )

    # Create initial state with regular tool call
    initial_state = {
        "messages": [
            {"role": "user", "content": "Add 5 and 3"},
            {
                "role": "assistant",
                "content": "I'll add those numbers for you.",
                "tool_calls": [
                    {"id": "call_456", "name": "add_numbers", "args": {"a": 5, "b": 3}}
                ],
            },
        ],
        "engine_name": engine.name,
        "tool_routes": {"add_numbers": "tool_node"},
    }

    # Run the agent
    graph = agent.create_runnable()
    result = await graph.ainvoke(initial_state)

    for i, msg in enumerate(result["messages"]):
        if hasattr(msg, "tool_call_id"):
            pass

    # Check if ToolMessage was created by tool_node
    tool_messages = [msg for msg in result["messages"] if isinstance(msg, ToolMessage)]

    if len(tool_messages) > 0:
        tool_msg = tool_messages[0]
        return True
    print("❌ No ToolMessage found - validation failed")
    return False


if __name__ == "__main__":
    import asyncio

    async def main():

        results = []

        try:
            result1 = await test_improved_pydantic_validation()
            results.append(("Improved Pydantic", result1))
        except Exception as e:
            results.append(("Improved Pydantic", False))

        try:
            result2 = await test_improved_regular_tool_validation()
            results.append(("Improved Regular Tool", result2))
        except Exception as e:
            results.append(("Improved Regular Tool", False))

        for test_name, passed in results:
            status = "✅ PASS" if passed else "❌ FAIL"

        if all(result for _, result in results):
            pass!")
        else:
            passs")

    asyncio.run(main())
