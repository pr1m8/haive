"""Token usage tracking schema for LLM interactions.

This module provides schemas for tracking token usage, costs, and capacity
across different LLM providers and models. It supports comprehensive metrics
including cached tokens, audio tokens, and reasoning tokens.
"""

from langchain_core.messages import AIMessage, BaseMessage
from pydantic import BaseModel, Field, model_validator


class TokenUsage(BaseModel):
    """Comprehensive token usage tracking with cost calculation.

    This class tracks all aspects of token usage including:
    - Input/output/total tokens
    - Cached tokens (for providers that support caching)
    - Audio tokens (for multimodal models)
    - Reasoning tokens (for models with explicit reasoning steps)
    - Cost calculation based on provider pricing
    - Capacity percentage for context window management
    """

    input_tokens: int = Field(default=0, description="Number of input tokens")
    output_tokens: int = Field(default=0, description="Number of output tokens")
    total_tokens: int = Field(default=0, description="Total tokens (input + output)")

    # Advanced token types
    input_tokens_cached: int | None = Field(
        default=None, description="Number of cached input tokens (if supported)"
    )
    audio_tokens: int | None = Field(
        default=None, description="Number of audio tokens (for multimodal models)"
    )
    reasoning_tokens: int | None = Field(
        default=None, description="Number of reasoning tokens (for reasoning models)"
    )

    # Cost tracking
    input_token_cost: float = Field(default=0.0, description="Cost of input tokens")
    output_token_cost: float = Field(default=0.0, description="Cost of output tokens")
    total_cost: float = Field(default=0.0, description="Total cost")

    # Capacity tracking
    capacity_percentage: float = Field(
        default=0.0, description="Percentage of model's context window used"
    )

    @model_validator(mode="after")
    def validate_totals(self):
        """Ensure total_tokens and total_cost are calculated if not set."""
        if self.total_tokens == 0:
            self.total_tokens = self.input_tokens + self.output_tokens

        if self.total_cost == 0.0:
            self.total_cost = self.input_token_cost + self.output_token_cost

        return self

    def add(self, other: "TokenUsage") -> "TokenUsage":
        """Add two TokenUsage instances together."""
        return TokenUsage(
            input_tokens=self.input_tokens + other.input_tokens,
            output_tokens=self.output_tokens + other.output_tokens,
            total_tokens=self.total_tokens + other.total_tokens,
            input_tokens_cached=(
                (self.input_tokens_cached or 0) + (other.input_tokens_cached or 0)
                if self.input_tokens_cached is not None
                or other.input_tokens_cached is not None
                else None
            ),
            audio_tokens=(
                (self.audio_tokens or 0) + (other.audio_tokens or 0)
                if self.audio_tokens is not None or other.audio_tokens is not None
                else None
            ),
            reasoning_tokens=(
                (self.reasoning_tokens or 0) + (other.reasoning_tokens or 0)
                if self.reasoning_tokens is not None
                or other.reasoning_tokens is not None
                else None
            ),
            input_token_cost=self.input_token_cost + other.input_token_cost,
            output_token_cost=self.output_token_cost + other.output_token_cost,
            total_cost=self.total_cost + other.total_cost,
            capacity_percentage=max(
                self.capacity_percentage, other.capacity_percentage
            ),
        )

    def __add__(self, other: "TokenUsage") -> "TokenUsage":
        """Support + operator for TokenUsage instances."""
        return self.add(other)


def extract_token_usage_from_message(
    message: BaseMessage, provider: str | None = None
) -> TokenUsage | None:
    """Extract token usage information from a message.

    Args:
        message: The message to extract usage from
        provider: Optional provider name for provider-specific handling

    Returns:
        TokenUsage instance if usage info found, None otherwise
    """
    if not isinstance(message, AIMessage):
        return None

    # Check for usage_metadata (newer LangChain versions)
    if hasattr(message, "usage_metadata") and message.usage_metadata:
        metadata = message.usage_metadata
        return TokenUsage(
            input_tokens=metadata.get("input_tokens", 0),
            output_tokens=metadata.get("output_tokens", 0),
            total_tokens=metadata.get("total_tokens", 0),
            input_tokens_cached=metadata.get("input_tokens_cached"),
            audio_tokens=metadata.get("audio_tokens"),
            reasoning_tokens=metadata.get("reasoning_tokens"),
            input_token_cost=metadata.get("input_token_cost", 0.0),
            output_token_cost=metadata.get("output_token_cost", 0.0),
            total_cost=metadata.get("total_cost", 0.0),
        )

    # Check response_metadata (common pattern)
    if hasattr(message, "response_metadata") and message.response_metadata:
        metadata = message.response_metadata

        # OpenAI pattern
        if "usage" in metadata:
            usage = metadata["usage"]
            return TokenUsage(
                input_tokens=usage.get("prompt_tokens", 0),
                output_tokens=usage.get("completion_tokens", 0),
                total_tokens=usage.get("total_tokens", 0),
                input_tokens_cached=usage.get("prompt_tokens_cached"),
            )

        # Anthropic pattern
        if "usage" in metadata:
            usage = metadata["usage"]
            return TokenUsage(
                input_tokens=usage.get("input_tokens", 0),
                output_tokens=usage.get("output_tokens", 0),
                total_tokens=(
                    usage.get("input_tokens", 0) + usage.get("output_tokens", 0)
                ),
            )

        # Direct token counts in metadata
        if "input_tokens" in metadata or "prompt_tokens" in metadata:
            return TokenUsage(
                input_tokens=metadata.get(
                    "input_tokens", metadata.get("prompt_tokens", 0)
                ),
                output_tokens=metadata.get(
                    "output_tokens", metadata.get("completion_tokens", 0)
                ),
                total_tokens=metadata.get("total_tokens", 0),
            )

    # Check additional_kwargs (older patterns)
    if hasattr(message, "additional_kwargs") and message.additional_kwargs:
        kwargs = message.additional_kwargs
        if "usage" in kwargs:
            usage = kwargs["usage"]
            if isinstance(usage, dict):
                return TokenUsage(
                    input_tokens=usage.get(
                        "input_tokens", usage.get("prompt_tokens", 0)
                    ),
                    output_tokens=usage.get(
                        "output_tokens", usage.get("completion_tokens", 0)
                    ),
                    total_tokens=usage.get("total_tokens", 0),
                )

    return None


def aggregate_token_usage(messages: list[BaseMessage]) -> TokenUsage:
    """Aggregate token usage across multiple messages.

    Args:
        messages: List of messages to aggregate usage from

    Returns:
        Combined TokenUsage instance
    """
    total_usage = TokenUsage()

    for message in messages:
        usage = extract_token_usage_from_message(message)
        if usage:
            total_usage = total_usage + usage

    return total_usage


def calculate_token_cost(
    usage: TokenUsage,
    input_cost_per_1k: float,
    output_cost_per_1k: float,
    cached_input_cost_per_1k: float | None = None,
) -> TokenUsage:
    """Calculate costs based on token usage and pricing.

    Args:
        usage: TokenUsage instance to calculate costs for
        input_cost_per_1k: Cost per 1000 input tokens
        output_cost_per_1k: Cost per 1000 output tokens
        cached_input_cost_per_1k: Optional cost per 1000 cached input tokens

    Returns:
        New TokenUsage instance with calculated costs
    """
    # Calculate base costs
    input_cost = (usage.input_tokens / 1000) * input_cost_per_1k
    output_cost = (usage.output_tokens / 1000) * output_cost_per_1k

    # Adjust for cached tokens if applicable
    if usage.input_tokens_cached and cached_input_cost_per_1k is not None:
        cached_cost = (usage.input_tokens_cached / 1000) * cached_input_cost_per_1k
        uncached_tokens = usage.input_tokens - usage.input_tokens_cached
        uncached_cost = (uncached_tokens / 1000) * input_cost_per_1k
        input_cost = cached_cost + uncached_cost

    return usage.model_copy(
        update={
            "input_token_cost": input_cost,
            "output_token_cost": output_cost,
            "total_cost": input_cost + output_cost,
        }
    )
