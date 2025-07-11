"""Token usage tracking mixin for MessagesState.

This module provides a mixin class that adds token usage tracking capabilities
to MessagesState or any other schema that manages messages.
"""

from typing import Any, Dict, List, Optional, Union

from langchain_core.messages import AnyMessage
from pydantic import BaseModel, Field

from haive.core.schema.prebuilt.messages.token_usage import (
    TokenUsage,
    aggregate_token_usage,
    calculate_token_cost,
    extract_token_usage_from_message,
)


class TokenUsageMixin(BaseModel):
    """Mixin that adds token usage tracking to message-based schemas.

    This mixin provides:
    - Automatic token usage extraction from messages
    - Aggregated token usage tracking
    - Token usage history
    - Cost calculation
    - Usage statistics and summaries

    To use this mixin, simply inherit from it in your schema:

    Example:
        ```python
        class MyMessagesState(MessagesState, TokenUsageMixin):
            pass
        ```
    """

    # Token usage tracking fields
    token_usage: Optional[TokenUsage] = Field(
        default=None, description="Aggregated token usage for all messages"
    )

    token_usage_history: List[TokenUsage] = Field(
        default_factory=list, description="History of token usage per message round"
    )

    def track_message_tokens(self, message: AnyMessage) -> Optional[TokenUsage]:
        """Extract and track token usage from a message.

        Args:
            message: The message to extract usage from

        Returns:
            TokenUsage if found, None otherwise
        """
        usage = extract_token_usage_from_message(message)
        if usage:
            # Update aggregated usage
            if self.token_usage:
                self.token_usage = self.token_usage + usage
            else:
                self.token_usage = usage

            # Add to history
            self.token_usage_history.append(usage)

        return usage

    def get_token_usage(self) -> Optional[TokenUsage]:
        """Get the current aggregated token usage."""
        return self.token_usage

    def recalculate_token_usage(self) -> TokenUsage:
        """Recalculate token usage from all messages.

        This method requires the implementing class to have a 'messages' attribute.

        Returns:
            Recalculated TokenUsage
        """
        if not hasattr(self, "messages"):
            raise AttributeError(
                "TokenUsageMixin requires a 'messages' attribute to recalculate usage"
            )

        self.token_usage = aggregate_token_usage(self.messages)
        return self.token_usage

    def get_last_token_usage(self) -> Optional[TokenUsage]:
        """Get token usage from the last AI message.

        This method requires the implementing class to have a 'get_last_ai_message' method.

        Returns:
            TokenUsage from last AI message if found
        """
        if hasattr(self, "get_last_ai_message"):
            last_ai = self.get_last_ai_message()
            if last_ai:
                return extract_token_usage_from_message(last_ai)
        elif hasattr(self, "messages") and self.messages:
            # Fallback: check last message if it's an AI message
            from langchain_core.messages import AIMessage

            last_msg = self.messages[-1]
            if isinstance(last_msg, AIMessage):
                return extract_token_usage_from_message(last_msg)

        return None

    def calculate_costs(
        self,
        input_cost_per_1k: float,
        output_cost_per_1k: float,
        cached_input_cost_per_1k: Optional[float] = None,
    ) -> Optional[TokenUsage]:
        """Calculate costs for current token usage.

        Args:
            input_cost_per_1k: Cost per 1000 input tokens
            output_cost_per_1k: Cost per 1000 output tokens
            cached_input_cost_per_1k: Optional cost per 1000 cached input tokens

        Returns:
            TokenUsage with calculated costs, or None if no usage tracked
        """
        if not self.token_usage:
            return None

        self.token_usage = calculate_token_cost(
            self.token_usage,
            input_cost_per_1k,
            output_cost_per_1k,
            cached_input_cost_per_1k,
        )
        return self.token_usage

    def get_token_usage_summary(self) -> Dict[str, Any]:
        """Get a summary of token usage statistics.

        Returns:
            Dictionary with usage statistics
        """
        if not self.token_usage:
            base_summary = {"total_tokens": 0, "total_cost": 0.0, "rounds": 0}

            # Add message count if available
            if hasattr(self, "messages"):
                base_summary["message_count"] = len(self.messages)

            return base_summary

        summary = {
            "total_tokens": self.token_usage.total_tokens,
            "input_tokens": self.token_usage.input_tokens,
            "output_tokens": self.token_usage.output_tokens,
            "total_cost": self.token_usage.total_cost,
            "capacity_percentage": self.token_usage.capacity_percentage,
            "rounds": len(self.token_usage_history),
            "has_cached_tokens": self.token_usage.input_tokens_cached is not None,
            "has_audio_tokens": self.token_usage.audio_tokens is not None,
            "has_reasoning_tokens": self.token_usage.reasoning_tokens is not None,
        }

        # Add message count if available
        if hasattr(self, "messages"):
            summary["message_count"] = len(self.messages)

        return summary

    def clear_token_usage(self) -> None:
        """Clear all token usage tracking."""
        self.token_usage = None
        self.token_usage_history = []

    def get_capacity_status(self) -> str:
        """Get a human-readable capacity status.

        Returns:
            Status string indicating capacity level
        """
        if not self.token_usage:
            return "Unknown"

        percentage = self.token_usage.capacity_percentage
        if percentage >= 90:
            return "Critical (≥90%)"
        elif percentage >= 75:
            return "High (≥75%)"
        elif percentage >= 50:
            return "Moderate (≥50%)"
        else:
            return "Low (<50%)"
