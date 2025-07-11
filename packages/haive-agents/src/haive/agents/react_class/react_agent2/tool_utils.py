# src/haive/agents/react/tool_utils.py

import json
import logging
import uuid
from collections.abc import Callable
from typing import Any

from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.tools import BaseTool

# Set up logging
logger = logging.getLogger(__name__)


def create_custom_tool_node(tools: list[BaseTool]) -> Callable:
    """Create a custom tool node function that properly handles AIMessage tool calls.

    This function specifically addresses edge cases in tool_call ID handling between
    different message formats.

    Args:
        tools: List of tools to use

    Returns:
        A function that can be used as a node in the graph
    """
    # Create a mapping of tool names to tool objects
    tool_map = {tool.name: tool for tool in tools}

    def extract_tool_calls(message: dict[str, Any] | AIMessage) -> list[dict[str, Any]]:
        """Extract tool calls from either an AIMessage or dict representation."""
        if isinstance(message, AIMessage):
            # Check direct tool_calls attribute
            if hasattr(message, "tool_calls") and message.tool_calls:
                return message.tool_calls

            # Check additional_kwargs
            if (
                hasattr(message, "additional_kwargs")
                and "tool_calls" in message.additional_kwargs
            ):
                return message.additional_kwargs["tool_calls"]

        elif isinstance(message, dict) and message.get("type") == "ai":
            # Check additional_kwargs in dict
            if "tool_calls" in message.get("additional_kwargs", {}):
                return message["additional_kwargs"]["tool_calls"]

        return []

    def parse_tool_arguments(tool_call: dict[str, Any]) -> dict[str, Any]:
        """Parse tool arguments from various formats."""
        # Direct args key
        if "args" in tool_call and isinstance(tool_call["args"], dict):
            return tool_call["args"]

        # Function.arguments pattern (OpenAI style)
        if "function" in tool_call and "arguments" in tool_call["function"]:
            args_str = tool_call["function"]["arguments"]
            try:
                if isinstance(args_str, str):
                    return json.loads(args_str)
                return args_str
            except json.JSONDecodeError:
                logger.warning(f"Failed to parse arguments: {args_str}")
                return {"raw_arguments": args_str}

        return {}

    def get_tool_name(tool_call: dict[str, Any]) -> str | None:
        """Extract tool name from various formats."""
        # Direct name field
        if "name" in tool_call:
            return tool_call["name"]

        # Function.name pattern (OpenAI style)
        if "function" in tool_call and "name" in tool_call["function"]:
            return tool_call["function"]["name"]

        return None

    def tool_node(state: dict[str, Any]) -> dict[str, Any]:
        """Execute tools based on the messages in the state."""
        logger.debug("Custom tool node called")

        # Convert state to dict if needed
        state_dict = state.model_dump() if hasattr(state, "model_dump") else dict(state)

        # Create a fresh copy to avoid mutation issues
        updated_state = state_dict.copy()

        # Get messages
        messages = updated_state.get("messages", [])
        if not messages:
            logger.warning("No messages found in state")
            return updated_state

        # Find the last AI message
        last_ai_message = None
        for message in reversed(messages):
            # Check if it's an AI message with tool calls
            if isinstance(message, AIMessage) or (
                isinstance(message, dict) and message.get("type") == "ai"
            ):
                last_ai_message = message
                break

        if not last_ai_message:
            logger.warning("No AI message found with tool calls")
            return updated_state

        # Extract tool calls
        tool_calls = extract_tool_calls(last_ai_message)
        if not tool_calls:
            logger.warning("No tool calls found in last AI message")
            return updated_state

        # Process each tool call
        new_messages = []
        tool_results = []

        for tool_call in tool_calls:
            # Get tool information
            tool_name = get_tool_name(tool_call)
            if not tool_name:
                logger.warning(f"Could not determine tool name: {tool_call}")
                continue

            # Get tool ID or generate one
            tool_id = tool_call.get("id")
            if not tool_id:
                tool_id = f"call_{uuid.uuid4().hex[:16]}"
                logger.debug(f"Generated tool ID: {tool_id}")

            # Get arguments
            tool_args = parse_tool_arguments(tool_call)

            # Find the tool
            tool = tool_map.get(tool_name)
            if not tool:
                error_msg = f"Tool '{tool_name}' not found"
                logger.warning(error_msg)

                # Create an error message
                error_tool_msg = ToolMessage(
                    content=f"Error: {error_msg}", name=tool_name, tool_call_id=tool_id
                )
                new_messages.append(error_tool_msg)
                continue

            # Execute the tool
            try:
                logger.debug(f"Executing tool {tool_name} with args: {tool_args}")
                result = tool(**tool_args)

                # Create tool message
                tool_msg = ToolMessage(
                    content=str(result), name=tool_name, tool_call_id=tool_id
                )
                new_messages.append(tool_msg)

                # Record result
                tool_results.append(
                    {"name": tool_name, "id": tool_id, "result": result}
                )

            except Exception as e:
                error_msg = f"Error executing tool '{tool_name}': {e!s}"
                logger.exception(error_msg)

                # Create an error message
                error_tool_msg = ToolMessage(
                    content=f"Error: {error_msg}", name=tool_name, tool_call_id=tool_id
                )
                new_messages.append(error_tool_msg)

        # Add the new messages to the state
        if "messages" in updated_state:
            updated_state["messages"] = messages + new_messages
        else:
            updated_state["messages"] = new_messages

        # Add tool results
        if "tool_results" in updated_state:
            updated_state["tool_results"] = (
                updated_state.get("tool_results", []) + tool_results
            )
        else:
            updated_state["tool_results"] = tool_results

        return updated_state

    return tool_node


def fix_tool_messages(messages: list[Any]) -> list[Any]:
    """Fix tool messages by ensuring they have proper tool_call_ids.

    This function ensures all ToolMessages have a valid tool_call_id
    by matching them with their corresponding AIMessage tool calls.

    Args:
        messages: List of messages to fix

    Returns:
        Fixed list of messages
    """
    # Collect tool call IDs for each tool name
    tool_call_ids = {}
    fixed_messages = []

    # First pass: collect IDs from AI messages
    for msg in messages:
        if isinstance(msg, AIMessage) or (
            isinstance(msg, dict) and msg.get("type") == "ai"
        ):
            tool_calls = []
            # Handle AIMessage
            if isinstance(msg, AIMessage):
                if hasattr(msg, "tool_calls") and msg.tool_calls:
                    tool_calls = msg.tool_calls
                elif (
                    hasattr(msg, "additional_kwargs")
                    and "tool_calls" in msg.additional_kwargs
                ):
                    tool_calls = msg.additional_kwargs["tool_calls"]

            # Handle dict format
            elif isinstance(msg, dict):
                tool_calls = msg.get("additional_kwargs", {}).get("tool_calls", [])

            # Extract IDs
            for call in tool_calls:
                tool_name = call.get("name")
                if not tool_name and "function" in call:
                    tool_name = call["function"].get("name")

                tool_id = call.get("id")
                if tool_name and tool_id:
                    tool_call_ids[tool_name] = tool_id

    # Second pass: fix tool messages
    for msg in messages:
        if isinstance(msg, ToolMessage) or (
            isinstance(msg, dict) and msg.get("type") == "tool"
        ):
            # Get tool name
            if isinstance(msg, ToolMessage):
                tool_name = msg.name
                tool_call_id = getattr(msg, "tool_call_id", None)
            else:
                tool_name = msg.get("name")
                tool_call_id = msg.get("tool_call_id")

            # Fix missing tool_call_id if we have a match
            if not tool_call_id and tool_name in tool_call_ids:
                if isinstance(msg, ToolMessage):
                    # Create a new message with the ID
                    fixed_msg = ToolMessage(
                        content=msg.content,
                        name=tool_name,
                        tool_call_id=tool_call_ids[tool_name],
                    )
                    fixed_messages.append(fixed_msg)
                else:
                    # Fix dict message
                    fixed_msg = msg.copy()
                    fixed_msg["tool_call_id"] = tool_call_ids[tool_name]
                    fixed_messages.append(fixed_msg)
            else:
                # No fix needed or can't fix
                fixed_messages.append(msg)
        else:
            # Not a tool message, no fix needed
            fixed_messages.append(msg)

    return fixed_messages
