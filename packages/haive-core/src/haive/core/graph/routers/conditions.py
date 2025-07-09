# src/haive/core/router/Router.py

import logging
from collections.abc import Callable
from typing import (
    Any,
)

from langchain_core.messages import (
    AIMessage,
)
from pydantic import BaseModel, Field

# Set up logging
logger = logging.getLogger(__name__)


class RouteCondition(BaseModel):
    """Base model for routing conditions."""

    priority: int = Field(
        default=0,
        description="Priority of the condition (higher priorities are evaluated first)",
    )
    description: str | None = Field(
        default=None, description="Description of the condition"
    )
    tags: list[str] = Field(
        default_factory=list, description="Tags for categorizing this condition"
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata"
    )

    def evaluate(self, state: dict[str, Any]) -> bool:
        """Evaluate the condition against the current state.

        Args:
            state: Current state to evaluate against

        Returns:
            True if condition is met, False otherwise
        """
        raise NotImplementedError("Subclasses must implement evaluate method")


class ToolCallCondition(RouteCondition):
    """Routes based on the presence of specific tool calls in the latest AI message."""

    tool_names: list[str] = Field(..., description="Names of tools to check for")
    require_all: bool = Field(
        default=False, description="Whether all tools must be present"
    )

    def evaluate(self, state: dict[str, Any]) -> bool:
        """Check if the latest AI message contains specified tool calls."""
        # Extract messages from state
        messages = state.get("messages", [])
        if not messages:
            return False

        # Find the last AI message
        ai_message = None
        for msg in reversed(messages):
            if isinstance(msg, AIMessage) or (
                hasattr(msg, "type") and msg.type == "ai"
            ):
                ai_message = msg
                break

        if not ai_message:
            return False

        # Check for tool calls
        tool_calls = getattr(ai_message, "tool_calls", [])
        if not tool_calls:
            return False

        # Extract tool names from calls
        called_tools = [
            call.get("name")
            for call in tool_calls
            if isinstance(call, dict) and "name" in call
        ]

        # Check if required tools are present
        if self.require_all:
            return all(tool in called_tools for tool in self.tool_names)
        return any(tool in called_tools for tool in self.tool_names)


class ContentCondition(RouteCondition):
    """Routes based on content in the latest message."""

    keywords: list[str] = Field(..., description="Keywords to check for in the message")
    require_all: bool = Field(
        default=False, description="Whether all keywords must be present"
    )
    case_sensitive: bool = Field(
        default=False, description="Whether keyword matching is case sensitive"
    )
    message_type: str | None = Field(
        default=None, description="Type of message to check (human, ai, system, etc.)"
    )

    def evaluate(self, state: dict[str, Any]) -> bool:
        """Check if the latest message contains specified keywords."""
        # Extract messages from state
        messages = state.get("messages", [])
        if not messages:
            return False

        # Get the last message, or a specific type if specified
        last_message = None
        for msg in reversed(messages):
            msg_type = getattr(msg, "type", None)
            if self.message_type is None or msg_type == self.message_type:
                last_message = msg
                break

        if not last_message:
            return False

        # Get message content
        content = ""
        if hasattr(last_message, "content"):
            content = last_message.content
        elif isinstance(last_message, dict) and "content" in last_message:
            content = last_message["content"]
        else:
            # Try to convert to string
            content = str(last_message)

        # Make case insensitive if needed
        if not self.case_sensitive:
            content = content.lower()
            keywords = [k.lower() for k in self.keywords]
        else:
            keywords = self.keywords

        # Check keywords
        if self.require_all:
            return all(keyword in content for keyword in keywords)
        return any(keyword in content for keyword in keywords)


class StateValueCondition(RouteCondition):
    """Routes based on state values."""

    key: str = Field(..., description="State key to check")
    value: Any = Field(..., description="Value to compare against")
    comparison: str = Field(
        default="==", description="Comparison type: ==, !=, >, <, in, etc."
    )

    def evaluate(self, state: dict[str, Any]) -> bool:
        """Check if a state value matches the condition."""
        # Check if key exists
        if self.key not in state:
            return False

        # Get the value
        state_value = state[self.key]

        # Perform comparison
        if self.comparison == "==":
            return state_value == self.value
        if self.comparison == "!=":
            return state_value != self.value
        if self.comparison == ">":
            return state_value > self.value
        if self.comparison == "<":
            return state_value < self.value
        if self.comparison == ">=":
            return state_value >= self.value
        if self.comparison == "<=":
            return state_value <= self.value
        if self.comparison == "in":
            return state_value in self.value
        if self.comparison == "contains":
            return self.value in state_value
        if self.comparison == "is":
            return state_value is self.value
        if self.comparison == "is not":
            return state_value is not self.value
        if self.comparison == "type":
            return isinstance(state_value, self.value)
        logger.warning(f"Unknown comparison type: {self.comparison}")
        return False


class FunctionCondition(RouteCondition):
    """Routes based on a custom function evaluation."""

    function: Callable[[dict[str, Any]], bool] = Field(
        ..., description="Function to evaluate condition"
    )

    def evaluate(self, state: dict[str, Any]) -> bool:
        """Evaluate using the provided function."""
        try:
            return self.function(state)
        except Exception as e:
            logger.error(f"Error evaluating function condition: {e}")
            return False


class CompositeCondition(RouteCondition):
    """Combines multiple conditions using logical operators."""

    conditions: list[RouteCondition] = Field(
        ..., description="List of conditions to combine"
    )
    operator: str = Field(default="and", description="Logical operator: and, or, not")

    def evaluate(self, state: dict[str, Any]) -> bool:
        """Evaluate combined conditions."""
        if not self.conditions:
            return False

        if self.operator == "and":
            return all(condition.evaluate(state) for condition in self.conditions)
        if self.operator == "or":
            return any(condition.evaluate(state) for condition in self.conditions)
        if self.operator == "not":
            # Not operator should have only one condition
            if len(self.conditions) != 1:
                logger.warning("Not operator expects exactly one condition")
                return False
            return not self.conditions[0].evaluate(state)
        logger.warning(f"Unknown operator: {self.operator}")
        return False
