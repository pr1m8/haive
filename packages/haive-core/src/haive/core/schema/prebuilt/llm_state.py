"""LLM-specific state with single engine and token tracking.

This module provides a state schema optimized for LLM-based agents that need
to track token usage against thresholds and metadata.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Optional, Union

# Import BaseOutputParser for type resolution in LangGraph
# This ensures it's available when LangGraph evaluates type hints
from langchain_core.output_parsers.base import BaseOutputParser
from pydantic import Field, computed_field, field_validator, model_validator

# Direct import - simpler approach
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.schema.prebuilt.tool_state import ToolState

# Model-specific context lengths (approximate)
MODEL_CONTEXT_LENGTHS = {
    # GPT-4 variants
    "gpt-4": 8192,
    "gpt-4-32k": 32768,
    "gpt-4-turbo": 128000,
    "gpt-4-turbo-preview": 128000,
    "gpt-4o": 128000,
    "gpt-4o-mini": 128000,
    # GPT-3.5 variants
    "gpt-3.5-turbo": 4096,
    "gpt-3.5-turbo-16k": 16384,
    # Claude variants
    "claude-3-opus": 200000,
    "claude-3-sonnet": 200000,
    "claude-3-haiku": 200000,
    "claude-2.1": 200000,
    "claude-2": 100000,
    "claude-instant": 100000,
    # Other models
    "llama-2-70b": 4096,
    "mixtral-8x7b": 32768,
    "gemini-pro": 32768,
    "gemini-pro-1.5": 1000000,
}


class LLMState(ToolState):
    """State schema for LLM-based agents with single engine, tool management and token tracking.

    This schema is designed for agents that:
    - Use a single primary LLM engine (with optional additional engines)
    - Need automatic tool management and routing (inherited from ToolState)
    - Need automatic token usage tracking for all messages (inherited from ToolState → MessagesStateWithTokenUsage)
    - Want to compare token usage against engine metadata/thresholds
    - Require cost tracking and capacity monitoring

    The schema combines:
    - ToolState for tool management, routing, and token tracking
    - Single primary engine field for cleaner LLM agent design
    - Computed properties for threshold comparison
    - Automatic context length detection from model names

    Input Schema: Just messages (from MessagesStateWithTokenUsage)
    Output Schema: Full state including engine, messages, token usage, etc.

    Example:
        ```python
        from haive.core.schema.prebuilt import LLMState
        from haive.core.engine.aug_llm import AugLLMConfig

        # Create state with engine
        state = LLMState(
            engine=AugLLMConfig(
                name="gpt4_engine",
                model="gpt-4-turbo",  # Automatically detects 128k context
                temperature=0.7
            )
        )

        # Messages automatically track tokens
        state.add_message(ai_message)

        # Check against model-specific thresholds
        if state.is_approaching_token_limit:
            print(f"Warning: {state.token_usage_percentage:.1f}% of {state.context_length} tokens used")

        # Set custom thresholds
        state.warning_threshold = 0.75  # Warn at 75% usage
        state.critical_threshold = 0.90  # Critical at 90% usage

        # Get cost analysis
        analysis = state.get_conversation_cost_analysis()
        print(f"Total cost: ${analysis['total_cost']:.4f}")
        ```
    """

    # Override to make engine required for LLM agents
    # Use forward reference to avoid runtime type evaluation issues
    engine: AugLLMConfig = Field(
        ..., description="The LLM engine for this agent"  # Required field
    )

    # engines field inherited from ToolState (via StateSchema)
    # No need to override - ToolState manages engines properly

    # Threshold configuration
    warning_threshold: float = Field(
        default=0.75,
        ge=0.0,
        le=1.0,
        description="Threshold for warning about token usage (0.0-1.0)",
    )
    critical_threshold: float = Field(
        default=0.90,
        ge=0.0,
        le=1.0,
        description="Threshold for critical token usage (0.0-1.0)",
    )

    # Context length override (if not auto-detected)
    context_length_override: int | None = Field(
        default=None, description="Override auto-detected context length"
    )

    @model_validator(mode="after")
    def setup_primary_engine_references(self) -> LLMState:
        """Ensure the primary LLM engine is available in engines dict with standard keys.

        This works with ToolState's engine management to provide consistent access.
        """
        # Call parent validators in correct order
        # ToolState calls MessagesStateWithTokenUsage validators automatically
        super().sync_tools_and_update_routes()

        if self.engine:
            # Add primary engine to engines dict under standard keys
            self.engines["main"] = self.engine
            self.engines["llm"] = self.engine
            self.engines["primary"] = self.engine

            # Also add by engine name if it has one
            if hasattr(self.engine, "name") and self.engine.name:
                self.engines[self.engine.name] = self.engine

        return self

    @computed_field
    @property
    def context_length(self) -> int:
        """Get the context length for the current model."""
        if self.context_length_override:
            return self.context_length_override

        if not self.engine:
            return 4096  # Default

        # Try to get model name from various places
        model_name = None

        # Check engine attributes
        if hasattr(self.engine, "model"):
            model_name = self.engine.model
        elif hasattr(self.engine, "model_name"):
            model_name = self.engine.model_name
        elif hasattr(self.engine, "llm_config"):
            llm_config = self.engine.llm_config
            if hasattr(llm_config, "model"):
                model_name = llm_config.model
            elif hasattr(llm_config, "model_name"):
                model_name = llm_config.model_name

        if model_name:
            # Check exact match first
            if model_name in MODEL_CONTEXT_LENGTHS:
                return MODEL_CONTEXT_LENGTHS[model_name]

            # Check partial matches
            model_lower = model_name.lower()
            for key, length in MODEL_CONTEXT_LENGTHS.items():
                if key in model_lower or model_lower in key:
                    return length

        # Try to get from engine max_tokens
        if hasattr(self.engine, "max_tokens") and self.engine.max_tokens:
            return self.engine.max_tokens

        # Default based on engine type
        return 4096

    @computed_field
    @property
    def token_usage_percentage(self) -> float:
        """Get token usage as percentage of context length."""
        if not self.token_usage:
            return 0.0

        return (self.token_usage.total_tokens / self.context_length) * 100

    @computed_field
    @property
    def is_approaching_token_limit(self) -> bool:
        """Check if token usage is approaching the warning threshold."""
        return (self.token_usage_percentage / 100) >= self.warning_threshold

    @computed_field
    @property
    def is_at_critical_limit(self) -> bool:
        """Check if token usage has reached the critical threshold."""
        return (self.token_usage_percentage / 100) >= self.critical_threshold

    @computed_field
    @property
    def is_at_token_limit(self) -> bool:
        """Check if token usage has reached or exceeded the limit."""
        return self.token_usage_percentage >= 100

    @computed_field
    @property
    def remaining_tokens(self) -> int:
        """Calculate remaining tokens before hitting the limit."""
        if not self.engine:
            return 0

        # Get max tokens
        max_tokens = 4000  # default
        if hasattr(self.engine, "max_tokens") and self.engine.max_tokens:
            max_tokens = self.engine.max_tokens
        elif (
            hasattr(self.engine, "llm_config")
            and hasattr(self.engine.llm_config, "max_tokens")
            and self.engine.llm_config.max_tokens
        ):
            max_tokens = self.engine.llm_config.max_tokens

        if not self.token_usage:
            return max_tokens

        return max(0, max_tokens - self.token_usage.total_tokens)

    def get_engine_metadata(self) -> dict[str, Any]:
        """Get metadata from the engine for threshold comparisons."""
        if not self.engine:
            return {}

        metadata = {}

        # Extract common metadata
        if hasattr(self.engine, "metadata"):
            metadata.update(self.engine.metadata)

        # Extract specific fields
        for field in ["temperature", "max_tokens", "model", "model_name"]:
            if hasattr(self.engine, field):
                value = getattr(self.engine, field)
                if value is not None:
                    metadata[field] = value

        # Check in llm_config if available
        if hasattr(self.engine, "llm_config") and self.engine.llm_config:
            llm_config = self.engine.llm_config
            for field in ["temperature", "max_tokens", "model"]:
                if hasattr(llm_config, field):
                    value = getattr(llm_config, field)
                    if value is not None:
                        metadata[f"llm_{field}"] = value

        return metadata

    def should_summarize_context(self, threshold: float = 0.75) -> bool:
        """Determine if context should be summarized based on token usage.

        Args:
            threshold: Percentage threshold (0.0-1.0) for triggering summarization

        Returns:
            True if token usage exceeds threshold percentage of max tokens
        """
        return (self.token_usage_percentage / 100) > threshold

    @classmethod
    def from_engine(cls, engine: AugLLMConfig, **kwargs) -> LLMState:
        """Create LLMState from an AugLLMConfig engine.

        Args:
            engine: The AugLLMConfig engine
            **kwargs: Additional fields for the state

        Returns:
            New LLMState instance
        """
        return cls(engine=engine, **kwargs)
