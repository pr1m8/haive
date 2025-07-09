"""
Validation Router V2 - Conditional edge function for routing after V2 validation.

This router function works with ValidationNodeV2 to make routing decisions
based on the ToolMessages that were added to state by the validation node.

Flow:
1. ValidationNodeV2 processes tool calls and adds ToolMessages to state
2. This router reads the updated state and makes routing decisions
3. Routes to appropriate nodes (tool_node, parse_output, agent_node, END)
"""

import logging
from typing import Any, Dict, List, Union

from langchain_core.messages import AIMessage, ToolMessage
from langgraph.graph import END
from langgraph.types import Send

logger = logging.getLogger(__name__)


def has_tool_error_v2(message: ToolMessage) -> bool:
    """Check if a ToolMessage contains an error - V2 version."""
    if not isinstance(message, ToolMessage):
        return False

    # Check additional_kwargs first (most reliable)
    if hasattr(message, "additional_kwargs") and message.additional_kwargs:
        if message.additional_kwargs.get("is_error"):
            return True
        if not message.additional_kwargs.get("validation_passed", True):
            return False

    # Check content for error indicators
    content = message.content
    if isinstance(content, str):
        try:
            import json

            content_dict = json.loads(content)
            if isinstance(content_dict, dict):
                if not content_dict.get("success", True):
                    return True
                if "error" in content_dict:
                    return True
        except:
            pass

        # String-based error detection
        error_terms = ["error", "invalid", "failed", "exception", "validation error"]
        return any(term in content.lower() for term in error_terms)

    # Check dict content
    if isinstance(content, dict):
        if not content.get("success", True):
            return True
        error_keys = ["error", "errors", "exception", "validation_error"]
        return any(key in content for key in error_keys)

    return False


def validation_router_v2(state: Dict[str, Any]) -> Union[str, List[str], Send]:
    """
    V2 Validation Router - Routes based on ToolMessages added by ValidationNodeV2.

    This function analyzes the ToolMessages that were just added to state
    and determines where to route next.

    Returns:
        - "tool_node": For regular tools that need execution
        - "parse_output": For successfully validated Pydantic models
        - "agent_node": For errors that need agent handling
        - END: When no more processing needed
    """
    logger.info("=== ValidationRouterV2 Execution ===")

    # Get messages from state
    messages = state.get("messages", [])
    if not messages:
        logger.warning("No messages in state")
        return END

    # Get the last AIMessage with tool calls
    last_ai_message = None
    for msg in reversed(messages):
        if isinstance(msg, AIMessage) and hasattr(msg, "tool_calls") and msg.tool_calls:
            last_ai_message = msg
            break

    if not last_ai_message:
        logger.warning("No AIMessage with tool calls found")
        return END

    tool_calls = last_ai_message.tool_calls
    logger.info(f"Routing for {len(tool_calls)} tool calls")

    # Get tool routes from state
    tool_routes = state.get("tool_routes", {})

    # Analyze each tool call and determine destinations
    destinations = set()
    has_errors = False

    for tool_call in tool_calls:
        tool_name = tool_call.get("name")
        tool_id = tool_call.get("id")

        if not tool_name or not tool_id:
            continue

        logger.debug(f"Analyzing tool call: {tool_name}")

        # Get route for this tool
        route = tool_routes.get(tool_name, "unknown")
        logger.debug(f"Tool route: {tool_name} -> {route}")

        # Find corresponding ToolMessage (if any)
        tool_message = None
        for msg in messages:
            if (
                isinstance(msg, ToolMessage)
                and getattr(msg, "tool_call_id", None) == tool_id
            ):
                tool_message = msg
                break

        if route == "pydantic_model":
            if tool_message:
                # We have a ToolMessage from V2 validation
                if has_tool_error_v2(tool_message):
                    logger.warning(f"Pydantic validation failed for {tool_name}")
                    destinations.add("agent_node")  # Route errors back to agent
                    has_errors = True
                else:
                    logger.info(f"Pydantic validation passed for {tool_name}")
                    destinations.add("parse_output")  # Route to parser for processing
            else:
                # No ToolMessage found - this shouldn't happen with V2
                logger.warning(f"No ToolMessage found for Pydantic model {tool_name}")
                destinations.add("agent_node")
                has_errors = True

        elif route in ["langchain_tool", "function", "tool_node"]:
            if tool_message:
                # Tool already executed and has ToolMessage
                if has_tool_error_v2(tool_message):
                    logger.warning(f"Tool execution failed for {tool_name}")
                    destinations.add("agent_node")
                    has_errors = True
                else:
                    logger.info(f"Tool execution completed for {tool_name}")
                    # Tool is done, no further routing needed
                    pass
            else:
                # Tool needs to be executed
                logger.info(f"Routing {tool_name} to tool_node for execution")
                destinations.add("tool_node")

        else:
            # Unknown tool
            if tool_message and has_tool_error_v2(tool_message):
                logger.warning(f"Unknown tool error for {tool_name}")
                destinations.add("agent_node")
                has_errors = True
            else:
                logger.warning(f"Unknown tool {tool_name}, routing to agent")
                destinations.add("agent_node")
                has_errors = True

    # Determine final routing decision
    destinations_list = list(destinations)

    logger.info(f"Routing analysis complete:")
    logger.info(f"  Destinations: {destinations_list}")
    logger.info(f"  Has errors: {has_errors}")

    if not destinations_list:
        logger.info("No destinations found, ending")
        return END
    elif len(destinations_list) == 1:
        destination = destinations_list[0]
        logger.info(f"Single destination: {destination}")
        return destination
    else:
        # Multiple destinations - prioritize
        if "agent_node" in destinations_list:
            # If there are errors, go to agent first
            logger.info("Multiple destinations with errors, routing to agent_node")
            return "agent_node"
        elif "tool_node" in destinations_list:
            # If tools need execution, do that first
            logger.info("Multiple destinations, prioritizing tool_node")
            return "tool_node"
        elif "parse_output" in destinations_list:
            # Parse output next
            logger.info("Multiple destinations, prioritizing parse_output")
            return "parse_output"
        else:
            # Fallback to first destination
            destination = destinations_list[0]
            logger.info(f"Multiple destinations, using first: {destination}")
            return destination
