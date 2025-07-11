# src/haive/agents/react/tool_utils.py

import inspect
import logging
import uuid
from collections.abc import Callable
from typing import Any, Literal

from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.tools import BaseTool, StructuredTool
from langgraph.graph import END
from langgraph.types import Send

logger = logging.getLogger(__name__)


def prepare_tools(tools: list[BaseTool | dict[str, Any] | Callable]) -> list[BaseTool]:
    """Prepare tools for the React Agent.

    Args:
        tools: List of tools that can be BaseTool instances, dictionaries, or callables.

    Returns:
        List of BaseTool instances.
    """
    prepared_tools = []

    for tool in tools:
        if isinstance(tool, BaseTool):
            # Already a BaseTool instance
            prepared_tools.append(tool)
        elif isinstance(tool, dict):
            # Dictionary describing a tool
            try:
                if "func" in tool:
                    # Create a StructuredTool from the provided function
                    prepared_tools.append(
                        StructuredTool.from_function(
                            func=tool["func"],
                            name=tool.get("name", tool["func"].__name__),
                            description=tool.get(
                                "description", tool["func"].__doc__ or ""
                            ),
                            return_direct=tool.get("return_direct", False),
                            args_schema=tool.get("args_schema", None),
                            coroutine=inspect.iscoroutinefunction(tool["func"]),
                        )
                    )
            except Exception as e:
                logger.exception(f"Error creating tool from dictionary: {e}")
        elif callable(tool):
            # Callable function that can be converted to a tool
            try:
                prepared_tools.append(
                    StructuredTool.from_function(
                        func=tool,
                        name=getattr(tool, "__name__", f"tool_{uuid.uuid4().hex[:8]}"),
                        description=tool.__doc__ or "A tool with no description.",
                    )
                )
            except Exception as e:
                logger.exception(f"Error creating tool from callable: {e}")

    return prepared_tools


def tools_router(state: dict[str, Any]) -> str | list[Send]:
    """Router function for deciding next step after agent node.

    Args:
        state: Current state with messages field

    Returns:
        Next node to route to, or END if no tools needed
    """
    # Get the latest message
    messages = state.get("messages", [])
    if not messages:
        return END

    last_message = messages[-1]

    # Check if the message has tool calls
    if isinstance(last_message, AIMessage) and getattr(
        last_message, "tool_calls", None
    ):
        # Route to tool execution
        return "execute_tools"

    # No tool calls, so we're done
    return END


def tools_router_v2(state: dict[str, Any]) -> str | list[Send]:
    """Router function for v2 - sending each tool call to a separate tool node instance.

    Args:
        state: Current state with messages field

    Returns:
        Next node to route to, list of Send objects, or END
    """
    # Get the latest message
    messages = state.get("messages", [])
    if not messages:
        return END

    last_message = messages[-1]

    # Check if the message has tool calls
    if isinstance(last_message, AIMessage) and getattr(
        last_message, "tool_calls", None
    ):
        # Version 2: Each tool call gets its own node instance
        return [
            Send("execute_tools", tool_call) for tool_call in last_message.tool_calls
        ]

    # No tool calls, so we're done
    return END


def create_tool_executor(tools: list[BaseTool]) -> Callable:
    """Create a function that executes tools based on tool calls.

    Args:
        tools: List of tools available for execution

    Returns:
        Function that takes state and executes tools
    """
    # Create a mapping of tool names to tools
    tool_map = {tool.name: tool for tool in tools}

    def execute_tools(state: dict[str, Any]) -> dict[str, Any]:
        """Execute tools based on tool calls in the latest message.

        Args:
            state: Current state with messages

        Returns:
            Updated state with tool responses
        """
        messages = state.get("messages", [])
        if not messages:
            return state

        last_message = messages[-1]

        # Check if the message has tool calls
        if not isinstance(last_message, AIMessage) or not getattr(
            last_message, "tool_calls", None
        ):
            return state

        # Execute each tool call
        tool_results = []
        new_messages = []

        for tool_call in last_message.tool_calls:
            tool_name = tool_call.get("name")
            tool_args = tool_call.get("args", {})
            tool_id = tool_call.get("id", str(uuid.uuid4()))

            if tool_name in tool_map:
                tool = tool_map[tool_name]
                try:
                    # Execute the tool
                    result = tool.invoke(tool_args)

                    # Create a ToolMessage
                    tool_message = ToolMessage(
                        content=str(result), tool_call_id=tool_id, name=tool_name
                    )
                    new_messages.append(tool_message)

                    # Save the result
                    tool_results.append(
                        {
                            "tool_name": tool_name,
                            "tool_args": tool_args,
                            "result": result,
                            "success": True,
                        }
                    )
                except Exception as e:
                    error_msg = f"Error executing tool {tool_name}: {e!s}"

                    # Create a ToolMessage with the error
                    tool_message = ToolMessage(
                        content=error_msg, tool_call_id=tool_id, name=tool_name
                    )
                    new_messages.append(tool_message)

                    # Save the error
                    tool_results.append(
                        {
                            "tool_name": tool_name,
                            "tool_args": tool_args,
                            "error": str(e),
                            "success": False,
                        }
                    )
            else:
                error_msg = f"Tool {tool_name} not found"

                # Create a ToolMessage with the error
                tool_message = ToolMessage(
                    content=error_msg, tool_call_id=tool_id, name=tool_name
                )
                new_messages.append(tool_message)

                # Save the error
                tool_results.append(
                    {
                        "tool_name": tool_name,
                        "tool_args": tool_args,
                        "error": error_msg,
                        "success": False,
                    }
                )

        # Update tool results and add new messages
        return {
            "messages": new_messages,
            "tool_results": state.get("tool_results", []) + tool_results,
            "current_iteration": state.get("current_iteration", 0) + 1,
        }

    return execute_tools


def create_tool_executor_v2(tools: list[BaseTool]) -> Callable:
    """Create a function that executes a single tool for v2 architecture.

    Args:
        tools: List of tools available for execution

    Returns:
        Function that takes state and a tool call and executes it
    """
    # Create a mapping of tool names to tools
    tool_map = {tool.name: tool for tool in tools}

    def execute_single_tool(
        state: dict[str, Any], tool_call: dict[str, Any]
    ) -> dict[str, Any]:
        """Execute a single tool based on the provided tool call.

        Args:
            state: Current state
            tool_call: Tool call to execute

        Returns:
            Updated state with tool response
        """
        tool_name = tool_call.get("name")
        tool_args = tool_call.get("args", {})
        tool_id = tool_call.get("id", str(uuid.uuid4()))

        if tool_name in tool_map:
            tool = tool_map[tool_name]
            try:
                # Execute the tool
                result = tool.invoke(tool_args)

                # Create a ToolMessage
                tool_message = ToolMessage(
                    content=str(result), tool_call_id=tool_id, name=tool_name
                )

                # Save the result
                tool_result = {
                    "tool_name": tool_name,
                    "tool_args": tool_args,
                    "result": result,
                    "success": True,
                }
            except Exception as e:
                error_msg = f"Error executing tool {tool_name}: {e!s}"

                # Create a ToolMessage with the error
                tool_message = ToolMessage(
                    content=error_msg, tool_call_id=tool_id, name=tool_name
                )

                # Save the error
                tool_result = {
                    "tool_name": tool_name,
                    "tool_args": tool_args,
                    "error": str(e),
                    "success": False,
                }
        else:
            error_msg = f"Tool {tool_name} not found"

            # Create a ToolMessage with the error
            tool_message = ToolMessage(
                content=error_msg, tool_call_id=tool_id, name=tool_name
            )

            # Save the error
            tool_result = {
                "tool_name": tool_name,
                "tool_args": tool_args,
                "error": error_msg,
                "success": False,
            }

        # Update the state
        return {
            "messages": [tool_message],
            "tool_results": [*state.get("tool_results", []), tool_result],
            "current_iteration": state.get("current_iteration", 0) + 1,
        }

    return execute_single_tool


def check_iteration_limit(state: dict[str, Any]) -> str | Literal["END"]:
    """Check if the agent has reached its iteration limit.

    Args:
        state: Current state

    Returns:
        Router decision: either continue to agent or END
    """
    current_iteration = state.get("current_iteration", 0)
    max_iterations = state.get("max_iterations", 10)

    if current_iteration >= max_iterations:
        logger.warning(f"Reached maximum iterations limit: {max_iterations}")
        return END

    # Continue to agent
    return "agent"
