# src/haive/agents/react/debug.py

import json
import logging
import uuid
from pprint import pformat
from typing import Any

from langchain_core.messages import AIMessage, ToolMessage

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def debug_print_state(state: dict[str, Any], label: str = "State") -> None:
    """Print state in a readable format for debugging."""
    logger.debug(f"--- {label} ---")

    # Handle messages separately for better clarity
    if "messages" in state:
        messages = state["messages"]
        logger.debug(f"Messages ({len(messages)}):")
        for i, msg in enumerate(messages):
            logger.debug(f"  Message {i+1}:")

            # Convert message to dict if it's not already
            if hasattr(msg, "model_dump"):
                msg_dict = msg.model_dump()
            elif hasattr(msg, "dict"):
                msg_dict = msg.dict()
            else:
                msg_dict = msg if isinstance(msg, dict) else {"content": str(msg)}

            # Print message details
            for key, value in msg_dict.items():
                if key == "additional_kwargs" and value:
                    logger.debug(f"    {key}:")
                    # Format tool_calls for better readability
                    if "tool_calls" in value:
                        logger.debug("      tool_calls:")
                        for j, tc in enumerate(value["tool_calls"]):
                            logger.debug(f"        Tool Call {j+1}:")
                            for tc_key, tc_value in tc.items():
                                logger.debug(f"          {tc_key}: {tc_value}")
                    else:
                        logger.debug(f"      {pformat(value)}")
                else:
                    logger.debug(f"    {key}: {value}")

    # Print other state elements
    for key, value in state.items():
        if key != "messages":
            logger.debug(f"{key}: {value}")


def fix_tool_messages(messages: list[Any]) -> list[Any]:
    """Fix tool messages by ensuring each tool message has a valid tool_call_id.

    Args:
        messages: List of messages to fix

    Returns:
        Fixed list of messages
    """
    logger.debug("Fixing tool messages...")

    # Keep track of tool calls from AI messages
    tool_calls_map = {}  # Map tool names to their corresponding IDs
    fixed_messages = []

    # First pass: collect tool call IDs from AI messages
    for msg in messages:
        is_ai_message = isinstance(msg, AIMessage) or (
            isinstance(msg, dict) and msg.get("type") == "ai"
        )

        if is_ai_message:
            # Get tool calls depending on format
            tool_calls = []

            if isinstance(msg, AIMessage):
                if hasattr(msg, "tool_calls") and msg.tool_calls:
                    tool_calls = msg.tool_calls
                elif (
                    hasattr(msg, "additional_kwargs")
                    and "tool_calls" in msg.additional_kwargs
                ):
                    tool_calls = msg.additional_kwargs.get("tool_calls", [])
            elif isinstance(msg, dict):
                tool_calls = msg.get("additional_kwargs", {}).get("tool_calls", [])

            # Extract tool name and ID
            for call in tool_calls:
                if isinstance(call, dict):
                    tool_name = call.get("name")
                    if not tool_name and "function" in call:
                        tool_name = call["function"].get("name")

                    tool_id = call.get("id", f"call_{uuid.uuid4().hex[:12]}")

                    if tool_name:
                        tool_calls_map[tool_name] = tool_id
                        logger.debug(f"Recorded tool call: {tool_name} -> {tool_id}")

    # Second pass: fix tool messages using collected IDs
    for msg in messages:
        is_tool_message = isinstance(msg, ToolMessage) or (
            isinstance(msg, dict) and msg.get("type") == "tool"
        )

        if is_tool_message:
            print("--------------------------------")
            print(msg)
            print("--------------------------------")
            # Get tool name
            tool_name = None
            if isinstance(msg, ToolMessage):
                tool_name = msg.name
            elif isinstance(msg, dict):
                tool_name = msg.get("name")
            logger.debug(
                "----------------     tool info--------------------------------"
            )
            logger.debug(f"tool_msg: {msg}")
            logger.debug(f"tool_name: {tool_name}")
            # Get existing tool_call_id
            tool_call_id = None
            if isinstance(msg, ToolMessage):
                tool_call_id = getattr(msg, "tool_call_id", None)
            elif isinstance(msg, dict):
                tool_call_id = msg.get("tool_call_id")

            # If missing tool_call_id but we have a mapping for this tool
            if not tool_call_id and tool_name in tool_calls_map:
                logger.debug(
                    f"Fixing message for tool '{tool_name}' with ID {tool_calls_map[tool_name]}"
                )

                # Create a new message with the fixed ID
                if isinstance(msg, ToolMessage):
                    content = msg.content
                    fixed_msg = ToolMessage(
                        content=content,
                        name=tool_name,
                        tool_call_id=tool_calls_map[tool_name],
                    )
                    fixed_messages.append(fixed_msg)
                elif isinstance(msg, dict):
                    fixed_msg = msg.copy()
                    fixed_msg["tool_call_id"] = tool_calls_map[tool_name]
                    fixed_messages.append(fixed_msg)
            else:
                # No fix needed or can't be fixed
                if not tool_call_id:
                    logger.warning(
                        f"Can't fix tool message for '{tool_name}' - no matching tool call found"
                    )
                fixed_messages.append(msg)
        else:
            # Not a tool message, no fix needed
            fixed_messages.append(msg)

    return fixed_messages


def create_debug_tool_node(tools: list[Any]):
    """Create a thoroughly debugged tool node that prevents tool_call_id issues."""
    logger.debug("Creating debug tool node...")

    # Create a mapping of tool names to tool objects
    tool_map = {tool.name: tool for tool in tools}

    def debug_tool_node(state: dict[str, Any]) -> dict[str, Any]:
        """Execute tools with extensive debugging."""
        logger.debug("Debug tool node called")

        # Deep copy to avoid mutations
        state_copy = state.copy() if isinstance(state, dict) else state.model_dump()
        debug_print_state(state_copy, "Tool Node Input State")

        # Extract messages
        messages = state_copy.get("messages", [])
        if not messages:
            logger.warning("No messages in state")
            return state_copy

        # Find the last AI message with tool calls
        tool_calls = []
        last_ai_message = None

        for message in reversed(messages):
            if isinstance(message, AIMessage) or (
                isinstance(message, dict) and message.get("type") == "ai"
            ):
                last_ai_message = message
                break

        logger.debug(f"Last AI message: {last_ai_message}")

        # Extract tool calls from the AI message
        if isinstance(last_ai_message, AIMessage):
            if hasattr(last_ai_message, "tool_calls") and last_ai_message.tool_calls:
                tool_calls = last_ai_message.tool_calls
                logger.debug(f"Found tool_calls attribute: {tool_calls}")
            elif (
                hasattr(last_ai_message, "additional_kwargs")
                and "tool_calls" in last_ai_message.additional_kwargs
            ):
                tool_calls = last_ai_message.additional_kwargs.get("tool_calls", [])
                logger.debug(f"Found tool_calls in additional_kwargs: {tool_calls}")
        elif isinstance(last_ai_message, dict) and last_ai_message.get("type") == "ai":
            tool_calls = last_ai_message.get("additional_kwargs", {}).get(
                "tool_calls", []
            )
            logger.debug(f"Found tool_calls in dict: {tool_calls}")

        if not tool_calls:
            logger.warning("No tool calls found")
            return state_copy

        # Process each tool call and accumulate results
        new_messages = []
        tool_results = []

        for tool_call in tool_calls:
            # Extract tool information with detailed logging
            if isinstance(tool_call, dict):
                if "name" in tool_call:
                    tool_name = tool_call["name"]
                    logger.debug(f"Found direct name: {tool_name}")
                elif "function" in tool_call and "name" in tool_call["function"]:
                    tool_name = tool_call["function"]["name"]
                    logger.debug(f"Found function.name: {tool_name}")
                else:
                    logger.error("Could not determine tool name")
                    continue

                tool_id = tool_call.get("id")
                if not tool_id:
                    tool_id = f"call_{uuid.uuid4().hex[:16]}"
                    logger.debug(f"Generated new ID: {tool_id}")
                else:
                    logger.debug(f"Found existing ID: {tool_id}")

                if "args" in tool_call:
                    tool_args = tool_call["args"]
                    logger.debug(f"Found direct args: {tool_args}")
                elif "function" in tool_call and "arguments" in tool_call["function"]:
                    try:
                        args_str = tool_call["function"]["arguments"]
                        logger.debug(f"Found function.arguments string: {args_str}")
                        if isinstance(args_str, str):
                            tool_args = json.loads(args_str)
                            logger.debug(f"Parsed JSON arguments: {tool_args}")
                        else:
                            tool_args = args_str
                            logger.debug(f"Using non-string arguments: {tool_args}")
                    except json.JSONDecodeError as e:
                        logger.error(f"Failed to parse arguments JSON: {e}")
                        tool_args = {"raw_arguments": args_str}
                else:
                    logger.warning("No arguments found, using empty dict")
                    tool_args = {}
            else:
                # Handle non-dict tool calls
                logger.debug(f"Non-dict tool call: {type(tool_call)}")
                tool_name = getattr(tool_call, "name", None)
                tool_id = getattr(tool_call, "id", f"call_{uuid.uuid4().hex[:16]}")
                tool_args = getattr(tool_call, "args", {})

            # Find the tool to execute
            logger.debug(f"Looking for tool '{tool_name}'")
            tool = tool_map.get(tool_name)
            if not tool:
                error_msg = f"Tool '{tool_name}' not found"
                logger.warning(error_msg)

                # Create error message
                tool_message = ToolMessage(
                    content=f"Error: {error_msg}", name=tool_name, tool_call_id=tool_id
                )
                new_messages.append(tool_message)
                logger.debug(f"Added error message for missing tool: {tool_message}")
                continue

            # Execute the tool
            try:
                logger.debug(f"Executing {tool_name} with args: {tool_args}")
                if isinstance(tool_args, dict):
                    result = tool(**tool_args)
                else:
                    result = tool(tool_args)

                logger.debug(f"Tool result: {result}")

                # Create tool message with proper tool_call_id
                tool_message = ToolMessage(
                    content=str(result), name=tool_name, tool_call_id=tool_id
                )
                new_messages.append(tool_message)
                logger.debug(
                    f"Created tool message: {tool_message.model_dump() if hasattr(tool_message, 'model_dump') else tool_message}"
                )

                # Record tool result
                tool_results.append(
                    {"name": tool_name, "id": tool_id, "result": result}
                )

            except Exception as e:
                error_msg = f"Error executing tool '{tool_name}': {e!s}"
                logger.error(error_msg)

                # Create error message
                tool_message = ToolMessage(
                    content=f"Error: {error_msg}", name=tool_name, tool_call_id=tool_id
                )
                new_messages.append(tool_message)
                logger.debug(f"Added error message for failed tool: {tool_message}")

        # Update state with new messages and tool results
        logger.debug(f"Adding {len(new_messages)} new messages")

        # Ensure we're not losing original messages when updating
        if "messages" in state_copy:
            state_copy["messages"] = messages + new_messages
            logger.debug(
                f"Updated messages, now have {len(state_copy['messages'])} total"
            )
        else:
            state_copy["messages"] = new_messages
            logger.debug(f"Set messages to {len(new_messages)} new messages")

        # Add tool results
        if "tool_results" in state_copy:
            state_copy["tool_results"] = state_copy["tool_results"] + tool_results
        else:
            state_copy["tool_results"] = tool_results

        debug_print_state(state_copy, "Tool Node Output State")
        return state_copy

    return debug_tool_node
