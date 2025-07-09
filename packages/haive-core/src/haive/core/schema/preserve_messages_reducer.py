"""Custom message reducer for preserving BaseMessage fields.

This module provides a custom reducer function that preserves BaseMessage objects
intact during state updates in multi-agent systems. Unlike LangGraph's default
add_messages reducer, this implementation avoids converting messages to dicts
and back, which can cause loss of important fields like tool_call_id.

The preserve_messages_reducer is critical for multi-agent tool coordination,
ensuring that ToolMessage objects maintain their tool_call_id field when
passed between agents. This prevents KeyError exceptions and enables proper
tool result routing.

Example:
    >>> from haive.core.schema.preserve_messages_reducer import preserve_messages_reducer
    >>> from langchain_core.messages import ToolMessage
    >>>
    >>> # Create a ToolMessage with tool_call_id
    >>> tool_msg = ToolMessage(content="Result: 42", tool_call_id="call_123")
    >>>
    >>> # Using preserve_messages_reducer maintains the field
    >>> messages = preserve_messages_reducer([], [tool_msg])
    >>> assert messages[0].tool_call_id == "call_123"  # Preserved!

Note:
    This reducer is automatically used by AgentSchemaComposer for message fields
    to ensure proper multi-agent message handling.
"""

import logging
from typing import List, Union

from langchain_core.messages import BaseMessage, convert_to_messages

logger = logging.getLogger(__name__)


def preserve_messages_reducer(left: List, right: List) -> List:
    """
    Custom reducer that preserves BaseMessage objects to avoid losing fields.

    This is a replacement for LangGraph's add_messages reducer that avoids
    calling convert_to_messages when the messages are already BaseMessage objects.

    Args:
        left: Existing messages in state
        right: New messages to add

    Returns:
        Combined list of messages with BaseMessage objects preserved
    """
    # Start with existing messages
    result = list(left) if left else []

    if not right:
        return result

    # Handle the new messages
    for msg in right:
        if isinstance(msg, BaseMessage):
            # Already a BaseMessage object - preserve it exactly
            result.append(msg)
            logger.debug(f"Preserved BaseMessage: {type(msg).__name__}")
            if hasattr(msg, "tool_call_id"):
                logger.debug(f"  tool_call_id: {getattr(msg, 'tool_call_id', 'None')}")
        else:
            # Need to convert from dict - use convert_to_messages
            # but only for this individual message
            try:
                converted = convert_to_messages([msg])
                result.extend(converted)
                logger.debug(f"Converted message from dict: {type(msg)}")
            except Exception as e:
                logger.warning(f"Failed to convert message: {e}")
                # Fallback: add as-is
                result.append(msg)

    return result
