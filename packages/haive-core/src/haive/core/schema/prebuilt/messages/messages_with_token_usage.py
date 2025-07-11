"""MessagesState with integrated token usage tracking.

This module provides THE standard messages state schema with automatic token tracking.
This should be used as the base for all conversational agents that need token awareness.
"""

from typing import Dict, List, Union

from langchain_core.messages import AIMessage, AnyMessage, messages_from_dict
from pydantic import model_validator

from haive.core.schema.prebuilt.messages.token_usage_mixin import TokenUsageMixin
from haive.core.schema.prebuilt.messages_state import MessagesState


class MessagesStateWithTokenUsage(MessagesState, TokenUsageMixin):
    """MessagesState with integrated token usage tracking.

    This prebuilt schema combines all the features of MessagesState with
    automatic token usage tracking, cost calculation, and usage analytics.

    Features:
    - All MessagesState capabilities (message handling, filtering, etc.)
    - Automatic token usage extraction from AI messages
    - Aggregated token usage tracking across the conversation
    - Token usage history per message round
    - Cost calculation based on provider pricing
    - Capacity percentage tracking
    - Usage statistics and summaries

    Example:
        ```python
        from haive.core.schema.prebuilt import MessagesStateWithTokenUsage

        # Create state with token tracking
        state = MessagesStateWithTokenUsage()

        # Messages automatically track tokens
        state.add_message(ai_message_with_usage)

        # Get usage summary
        summary = state.get_token_usage_summary()
        print(f"Total tokens: {summary['total_tokens']}")
        print(f"Total cost: ${summary['total_cost']:.4f}")

        # Calculate costs with provider pricing
        state.calculate_costs(
            input_cost_per_1k=0.003,  # $0.003 per 1k input tokens
            output_cost_per_1k=0.015  # $0.015 per 1k output tokens
        )
        ```
    """

    @model_validator(mode="after")
    def auto_track_all_tokens(self) -> "MessagesStateWithTokenUsage":
        """
        Automatically track token usage for ALL messages in the state.
        This ensures token tracking happens no matter how messages are added.
        """
        # Track tokens for ALL messages
        for message in self.messages:
            # Track tokens for any message type that might have usage data
            self.track_message_tokens(message)

        return self

    def add_message(self, message: Union[AnyMessage, Dict]) -> None:
        """Add a message to the conversation and track token usage.

        This overrides the base add_message to automatically extract
        and track token usage from AI messages.

        Args:
            message: Message to add (dict or Message object)
        """
        # Convert dict to message if needed
        if isinstance(message, dict):
            message = messages_from_dict([message])[0]

        # Add to messages list
        self.messages.append(message)

        # Track token usage immediately for any message
        self.track_message_tokens(message)

    @classmethod
    def with_system_message_and_tracking(
        cls, system_content: str
    ) -> "MessagesStateWithTokenUsage":
        """Create a new state with a system message and token tracking enabled.

        Args:
            system_content: Content for the system message

        Returns:
            New MessagesStateWithTokenUsage instance
        """
        state = cls()
        state.add_system_message(system_content)
        return state

    def get_conversation_cost_analysis(self) -> Dict[str, Union[float, int, str]]:
        """Get detailed cost analysis for the conversation.

        Returns:
            Dictionary with cost breakdown and analysis
        """
        summary = self.get_token_usage_summary()

        # Calculate average tokens per round
        avg_tokens_per_round = (
            summary["total_tokens"] / summary["rounds"] if summary["rounds"] > 0 else 0
        )

        # Get capacity status
        capacity_status = self.get_capacity_status()

        return {
            "total_cost": summary["total_cost"],
            "total_tokens": summary["total_tokens"],
            "input_tokens": summary.get("input_tokens", 0),
            "output_tokens": summary.get("output_tokens", 0),
            "rounds": summary["rounds"],
            "messages": summary.get("message_count", 0),
            "avg_tokens_per_round": avg_tokens_per_round,
            "capacity_status": capacity_status,
            "capacity_percentage": summary.get("capacity_percentage", 0.0),
            "has_cached_tokens": summary.get("has_cached_tokens", False),
            "has_special_tokens": (
                summary.get("has_audio_tokens", False)
                or summary.get("has_reasoning_tokens", False)
            ),
        }
