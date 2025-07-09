# src/haive/agents/react/tool_handling.py

import logging
from typing import Any

from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.tools import BaseTool
from langgraph.prebuilt.tool_node import ToolNode as LangGraphToolNode
from langgraph.types import Command

logger = logging.getLogger(__name__)


class GeneralizedToolNode:
    """A generalized tool node that supports both standard tools and human interaction.

    This node processes tool calls from the LLM and either:
    1. Executes standard tools using LangGraph's ToolNode
    2. Flags the state for human input when the "request_human_assistance" tool is called
    """

    def __init__(self, tools: list[BaseTool], parallel: bool = True):
        """Initialize the generalized tool node.

        Args:
            tools: List of tools that can be executed
            parallel: Whether to run tools in parallel
        """
        # Create the LangGraph ToolNode for regular tools
        self.tool_node = LangGraphToolNode(tools)

        # Create a mapping of tool names for quick lookup
        self.tools_by_name = {tool.name: tool for tool in tools}

        # Special tool names that trigger human interaction
        self.human_tool_names = {"request_human_assistance", "ask_human", "human_input"}

        self.parallel = parallel

    def __call__(self, state: dict[str, Any]) -> dict[str, Any]:
        """Process tool calls and update state with results or flag for human input.

        Args:
            state: Current agent state

        Returns:
            Updated state with tool results or human input flag
        """
        messages = state.get("messages", [])

        # Find the last AI message with tool calls
        tool_calls = []
        last_ai_message = None
        for message in reversed(messages):
            if (
                isinstance(message, AIMessage)
                and hasattr(message, "tool_calls")
                and message.tool_calls
            ):
                tool_calls = message.tool_calls
                last_ai_message = message
                break

        if not tool_calls:
            logger.warning("No tool calls found in messages")
            return state

        # Check if any tool call is a request for human assistance
        human_assistance_calls = []
        standard_tool_calls = []

        for tool_call in tool_calls:
            tool_name = tool_call.get("name", "")
            if tool_name in self.human_tool_names:
                human_assistance_calls.append(tool_call)
            else:
                standard_tool_calls.append(tool_call)

        # Process human assistance requests if any
        if human_assistance_calls:
            request_call = human_assistance_calls[
                0
            ]  # Use the first request if multiple
            human_request = request_call.get("args", {}).get("query", "")
            if not human_request:
                human_request = "The assistant needs your input on this matter."

            return {
                "requires_human_input": True,
                "human_request": human_request,
                "iteration": state.get("iteration", 0) + 1,
            }

        # If no human assistance requested, process standard tools using LangGraph's ToolNode
        # Create a state copy with only the last AI message's tool calls
        if self.parallel:
            # For parallel tools, use the LangGraph ToolNode
            return self.tool_node(state)
        # For sequential tools, process one at a time
        # This is a simplified implementation - might need more complexity for actual sequential processing
        tool_results = []
        tool_messages = []

        for tool_call in tool_calls:
            tool_name = tool_call.get("name", "")
            tool_args = tool_call.get("args", {})
            tool_id = tool_call.get("id", "")

            if tool_name not in self.tools_by_name:
                logger.warning(f"Tool '{tool_name}' not found")
                tool_result = f"Error: Tool '{tool_name}' not found"
            else:
                try:
                    tool = self.tools_by_name[tool_name]
                    tool_result = tool.invoke(tool_args)
                except Exception as e:
                    logger.error(f"Error executing tool '{tool_name}': {e}")
                    tool_result = f"Error executing tool: {e!s}"

            # Create ToolMessage for the result
            tool_message = ToolMessage(
                content=str(tool_result), tool_call_id=tool_id, name=tool_name
            )

            tool_messages.append(tool_message)
            tool_results.append(
                {
                    "name": tool_name,
                    "args": tool_args,
                    "result": tool_result,
                    "id": tool_id,
                }
            )

        # Update state
        return {
            "messages": tool_messages,
            "tool_results": state.get("tool_results", []) + tool_results,
            "iteration": state.get("iteration", 0) + 1,
        }


# Create a human input node for the graph
def human_input_node(state: dict[str, Any]) -> Command:
    """Node that handles human input requests.

    This node generates a command to interrupt the graph execution
    and wait for human input. It's triggered when a tool requests human assistance.

    Args:
        state: Current agent state

    Returns:
        Command to interrupt the graph and wait for human input
    """
    from langgraph.types import Command

    # Get the human request message
    human_request = state.get("human_request", "The assistant needs your input.")

    # Return a command to interrupt and wait for human input
    # This will be picked up by the langgraph interrupt mechanism
    return Command(
        update={"requires_human_input": True, "human_request": human_request},
        # This doesn't route anywhere specific - the graph will be interrupted
        goto="",
    )


# Function to create a request_human_assistance tool
def create_human_assistance_tool(name: str = "request_human_assistance") -> BaseTool:
    """Create a tool for requesting human assistance.

    Args:
        name: Name for the tool

    Returns:
        A BaseTool that can be added to the agent's toolkit
    """
    from langchain_core.tools import Tool

    def _request_human_assistance(query: str) -> str:
        """Request assistance from a human.

        Args:
            query: The question or request for the human

        Returns:
            Acknowledgement that the request has been sent
        """
        return f"Human assistance requested: {query}"

    return Tool(
        name=name,
        description="Request assistance from a human when you need help or additional information.",
        func=_request_human_assistance,
        args_schema=None,  # Can add a schema if needed
    )
