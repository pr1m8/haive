"""
Utility classes and functions for message processing in Haive.

This module provides common utilities used by various implementations
of MessagesState, enabling advanced message analysis, transformation,
and tracking features.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, ToolMessage
from pydantic import BaseModel, Field


class ToolCallInfo(BaseModel):
    """Information about a completed tool call."""

    tool_call_id: str = Field(description="ID of the tool call")
    tool_call: Dict[str, Any] = Field(description="Original tool call object")
    tool_message: ToolMessage = Field(description="Corresponding tool message")
    ai_message: AIMessage = Field(description="AI message that made the tool call")
    is_successful: bool = Field(description="Whether the tool call was successful")
    timestamp: datetime = Field(default_factory=datetime.now)


class MessageRound(BaseModel):
    """Information about a conversation round."""

    round_number: int = Field(description="Round number (1-indexed)")
    human_message: HumanMessage = Field(
        description="The human message that started this round"
    )
    ai_responses: List[AIMessage] = Field(
        default_factory=list, description="AI responses in this round"
    )
    tool_calls: List[Dict[str, Any]] = Field(
        default_factory=list, description="Tool calls made in this round"
    )
    tool_responses: List[ToolMessage] = Field(
        default_factory=list, description="Tool responses in this round"
    )
    is_complete: bool = Field(
        default=False, description="Whether the round is complete"
    )
    has_errors: bool = Field(
        default=False, description="Whether the round has any tool errors"
    )


def is_real_human_message(msg: HumanMessage) -> bool:
    """
    Check if a human message is real (not transformed).

    Args:
        msg: The message to check

    Returns:
        True if the message is from a real human, False if transformed
    """
    has_name = hasattr(msg, "name") and msg.name is not None
    has_engine_metadata = has_engine_metadata_attribute(msg)
    has_agent_metadata = has_agent_metadata_attribute(msg)
    return not (has_name or has_engine_metadata or has_agent_metadata)


def has_engine_metadata_attribute(msg: BaseMessage) -> bool:
    """
    Check if message has engine-related metadata.

    Args:
        msg: The message to check

    Returns:
        True if the message has engine metadata, False otherwise
    """
    if not hasattr(msg, "additional_kwargs") or not msg.additional_kwargs:
        return False
    return (
        "engine_id" in msg.additional_kwargs or "engine_name" in msg.additional_kwargs
    )


def has_agent_metadata_attribute(msg: BaseMessage) -> bool:
    """
    Check if message has agent-related metadata.

    Args:
        msg: The message to check

    Returns:
        True if the message has agent metadata, False otherwise
    """
    if not hasattr(msg, "additional_kwargs") or not msg.additional_kwargs:
        return False
    return "source_agent" in msg.additional_kwargs


def is_tool_error(msg: ToolMessage) -> bool:
    """
    Check if a tool message represents an error.

    Args:
        msg: The tool message to check

    Returns:
        True if the message indicates an error, False otherwise
    """
    if hasattr(msg, "additional_kwargs") and msg.additional_kwargs:
        return msg.additional_kwargs.get("is_error", False)
    return False


def extract_tool_calls(message: AIMessage) -> List[Dict[str, Any]]:
    """
    Extract tool calls from an AI message.

    Args:
        message: The AI message to extract tool calls from

    Returns:
        List of tool call dictionaries
    """
    if not message:
        return []

    # Check direct tool_calls attribute
    if hasattr(message, "tool_calls") and message.tool_calls:
        return message.tool_calls

    # Check in additional_kwargs
    if hasattr(message, "additional_kwargs") and message.additional_kwargs.get(
        "tool_calls"
    ):
        return message.additional_kwargs["tool_calls"]

    return []


def inject_state_into_tool_calls(
    tool_calls: List[Dict], state_data: Optional[Dict[str, Any]] = None
) -> List[Dict]:
    """
    Inject state data into tool call arguments.

    Args:
        tool_calls: List of tool call dictionaries
        state_data: Optional state data to inject

    Returns:
        Modified tool calls with injected state
    """
    if not tool_calls:
        return []

    # Inject state into each tool call
    injected_calls = []
    for call in tool_calls:
        call_copy = call.copy()

        if "args" not in call_copy or not isinstance(call_copy["args"], dict):
            call_copy["args"] = {}

        if "_state" not in call_copy["args"] and state_data is not None:
            call_copy["args"]["_state"] = state_data

        injected_calls.append(call_copy)

    return injected_calls
