"""
Compatibility layer for MessagesState implementations.

This module provides adapter classes and utilities that enable backward
compatibility while adding new features from the enhanced MessagesState
implementation. It serves as a bridge between the old and new architectures.
"""

from typing import Any, Dict, List, Optional, Union

from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)
from langgraph.graph import END
from langgraph.types import Send

from haive.core.schema.prebuilt.messages.utils import (
    MessageRound,
    ToolCallInfo,
    extract_tool_calls,
    inject_state_into_tool_calls,
    is_real_human_message,
    is_tool_error,
)


class MessagesStateAdapter:
    """
    Adapter that enables old MessagesState instances to use new features
    with minimal changes to their API.

    This adapter wraps an existing MessagesState instance and provides
    methods that implement the enhanced functionality from the new
    MessagesState architecture.
    """

    def __init__(self, messages_state):
        """
        Initialize the adapter with an existing MessagesState instance.

        Args:
            messages_state: The MessagesState instance to adapt
        """
        self.state = messages_state

    def get_conversation_rounds(self) -> List[MessageRound]:
        """
        Get detailed information about each conversation round.

        A conversation round typically consists of a human message,
        followed by one or more AI responses and possibly tool calls/responses.

        Returns:
            List of MessageRound objects with round details
        """
        rounds = []
        current_round = None
        round_number = 0

        for msg in self.state.messages:
            if isinstance(msg, HumanMessage) and is_real_human_message(msg):
                # Start a new round
                if current_round:
                    current_round.is_complete = self._is_round_complete(current_round)
                    rounds.append(current_round)

                round_number += 1
                current_round = MessageRound(
                    round_number=round_number, human_message=msg
                )

            elif current_round:
                if isinstance(msg, AIMessage):
                    current_round.ai_responses.append(msg)

                    # Track tool calls
                    tool_calls = extract_tool_calls(msg)
                    if tool_calls:
                        current_round.tool_calls.extend(tool_calls)

                elif isinstance(msg, ToolMessage):
                    current_round.tool_responses.append(msg)

                    # Check for errors
                    if is_tool_error(msg):
                        current_round.has_errors = True

        # Add the last round if it exists
        if current_round:
            current_round.is_complete = self._is_round_complete(current_round)
            rounds.append(current_round)

        return rounds

    def _is_round_complete(self, round_info: MessageRound) -> bool:
        """
        Check if a conversation round is complete.

        A round is considered complete if:
        1. There's at least one AI response
        2. All tool calls have corresponding responses (if any)

        Args:
            round_info: The round to check

        Returns:
            True if the round is complete, False otherwise
        """
        if not round_info.ai_responses:
            return False

        tool_call_ids = set()
        for tool_call in round_info.tool_calls:
            if isinstance(tool_call, dict) and "id" in tool_call:
                tool_call_ids.add(tool_call["id"])
            elif hasattr(tool_call, "id") and tool_call.id:
                tool_call_ids.add(tool_call.id)

        tool_response_ids = set()
        for tool_response in round_info.tool_responses:
            if hasattr(tool_response, "tool_call_id") and tool_response.tool_call_id:
                tool_response_ids.add(tool_response.tool_call_id)

        # Round is complete if all tool calls have responses
        return tool_call_ids.issubset(tool_response_ids)

    def deduplicate_tool_calls(self) -> int:
        """
        Remove duplicate tool calls based on tool call ID.

        This is useful when the same API call might be made multiple times
        due to agent or LLM quirks.

        Returns:
            Number of duplicates removed
        """
        seen_tool_call_ids = set()
        duplicates_removed = 0

        for msg in self.state.messages:
            if not isinstance(msg, AIMessage):
                continue

            tool_calls = extract_tool_calls(msg)
            if not tool_calls:
                continue

            unique_tool_calls = []
            for tool_call in tool_calls:
                # Handle different tool call formats
                if isinstance(tool_call, dict):
                    tool_call_id = tool_call.get("id")
                else:
                    tool_call_id = getattr(tool_call, "id", None)

                if tool_call_id and tool_call_id not in seen_tool_call_ids:
                    unique_tool_calls.append(tool_call)
                    seen_tool_call_ids.add(tool_call_id)
                elif tool_call_id and tool_call_id in seen_tool_call_ids:
                    duplicates_removed += 1
                elif not tool_call_id:
                    # If no ID, keep it (can't deduplicate)
                    unique_tool_calls.append(tool_call)

            # Update tool_calls on the message
            if hasattr(msg, "tool_calls"):
                msg.tool_calls = unique_tool_calls
            elif (
                hasattr(msg, "additional_kwargs")
                and "tool_calls" in msg.additional_kwargs
            ):
                msg.additional_kwargs["tool_calls"] = unique_tool_calls

        return duplicates_removed

    def get_completed_tool_calls(self) -> List[ToolCallInfo]:
        """
        Get all completed tool calls with their responses.

        This method matches tool calls in AI messages with their
        corresponding tool responses.

        Returns:
            List of ToolCallInfo objects with tool call details
        """
        completed = []

        # Build a mapping of tool call IDs to their messages
        tool_messages = {}
        for msg in self.state.messages:
            if isinstance(msg, ToolMessage):
                tool_call_id = getattr(msg, "tool_call_id", None)
                if tool_call_id:
                    is_error = is_tool_error(msg)
                    tool_messages[tool_call_id] = {"message": msg, "is_error": is_error}

        # Find AI messages with tool calls and match them to tool messages
        for msg in self.state.messages:
            if not isinstance(msg, AIMessage):
                continue

            tool_calls = extract_tool_calls(msg)
            if not tool_calls:
                continue

            for tool_call in tool_calls:
                # Handle different tool call formats
                if isinstance(tool_call, dict):
                    tool_call_id = tool_call.get("id")
                else:
                    tool_call_id = getattr(tool_call, "id", None)

                if tool_call_id and tool_call_id in tool_messages:
                    tool_msg_info = tool_messages[tool_call_id]
                    completed.append(
                        ToolCallInfo(
                            tool_call_id=tool_call_id,
                            tool_call=tool_call,
                            tool_message=tool_msg_info["message"],
                            ai_message=msg,
                            is_successful=not tool_msg_info["is_error"],
                        )
                    )

        return completed

    def send_tool_calls(self, node_name: str = "tools") -> Union[str, List[Send]]:
        """
        Convert tool calls from the last AI message into Send objects for LangGraph routing.

        Args:
            node_name: The name of the node to send tool calls to

        Returns:
            Either a string (if no tool calls) or a list of Send objects
        """
        last_ai = None
        for msg in reversed(self.state.messages):
            if isinstance(msg, AIMessage):
                last_ai = msg
                break

        if not last_ai:
            return END

        tool_calls = extract_tool_calls(last_ai)
        if not tool_calls:
            return END

        # Create state data to inject
        state_data = {"messages": self.state.messages}
        if hasattr(self.state, "model_dump"):
            state_data = self.state.model_dump()

        # Inject state into tool calls
        injected_calls = inject_state_into_tool_calls(tool_calls, state_data)

        # Create a Send object for each tool call
        return [Send(node_name, tool_call) for tool_call in injected_calls]

    def transform_ai_to_human(
        self,
        preserve_metadata: bool = True,
        engine_id: Optional[str] = None,
        engine_name: Optional[str] = None,
    ) -> None:
        """
        Transform AI messages to Human messages in place.

        This is useful for agent-to-agent communication or for
        creating synthetic conversations.

        Args:
            preserve_metadata: Whether to preserve message metadata
            engine_id: Optional engine ID to add to transformed messages
            engine_name: Optional engine name to add to transformed messages
        """
        transformed_messages = []

        for msg in self.state.messages:
            if isinstance(msg, AIMessage):
                kwargs = {"content": msg.content}

                if preserve_metadata:
                    if hasattr(msg, "additional_kwargs") and msg.additional_kwargs:
                        kwargs["additional_kwargs"] = msg.additional_kwargs.copy()

                    if engine_id or engine_name:
                        if "additional_kwargs" not in kwargs:
                            kwargs["additional_kwargs"] = {}
                        if engine_id:
                            kwargs["additional_kwargs"]["engine_id"] = engine_id
                        if engine_name:
                            kwargs["additional_kwargs"]["engine_name"] = engine_name

                    if hasattr(msg, "name") and msg.name:
                        kwargs["name"] = msg.name

                transformed_messages.append(HumanMessage(**kwargs))
            else:
                transformed_messages.append(msg)

        self.state.messages = transformed_messages
