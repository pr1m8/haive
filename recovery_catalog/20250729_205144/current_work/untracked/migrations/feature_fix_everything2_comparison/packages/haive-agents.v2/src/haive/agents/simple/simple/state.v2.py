"""State core module.

This module provides state functionality for the Haive framework.

Classes:
    SimpleAgentState: SimpleAgentState implementation.

Functions:
    add_human_message: Add Human Message functionality.
    add_ai_message: Add Ai Message functionality.
    extract_last_message_content: Extract Last Message Content functionality.
"""

from collections.abc import Sequence
from typing import Annotated

from haive.core.schema.state_schema import StateSchema
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langgraph.graph import add_messages
from pydantic import Field


class SimpleAgentState(StateSchema):
    """Base state for simple agents.

    This provides a standard chat-based state with a messages field that
    supports proper message history management through the add_messages reducer.
    """

    messages: Annotated[Sequence[BaseMessage], add_messages] = Field(
        default_factory=list, description="Chat message history"
    )

    def add_human_message(self, content: str) -> "SimpleAgentState":
        """Add a human message to the state.

        Args:
            content: Message content

        Returns:
            Self for chaining
        """
        if not hasattr(self, "messages"):
            self.messages = []

        message = HumanMessage(content=content)
        self.messages = add_messages(self.messages, [message])
        return self

    def add_ai_message(self, content: str) -> "SimpleAgentState":
        """Add an AI message to the state.

        Args:
            content: Message content

        Returns:
            Self for chaining
        """
        if not hasattr(self, "messages"):
            self.messages = []

        message = AIMessage(content=content)
        self.messages = add_messages(self.messages, [message])
        return self

    def extract_last_message_content(self) -> str | None:
        """Extract the content of the last message in the state.

        Returns:
            Content of the last message or None if no messages
        """
        if not hasattr(self, "messages") or not self.messages:
            return None

        last_message = self.messages[-1]
        return last_message.content if hasattr(last_message, "content") else None

    @classmethod
    def with_messages(cls, messages: list[BaseMessage]) -> "SimpleAgentState":
        """Create a new instance with the given messages.

        Args:
            messages: Initial messages

        Returns:
            New SimpleAgentState instance
        """
        return cls(messages=messages)
