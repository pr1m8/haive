# =============================================
# React Agent State
# =============================================
from collections.abc import Sequence
from typing import Any, Optional

from haive.core.utils.message_utils import has_tool_calls
from langchain_core.messages import BaseMessage
from pydantic import BaseModel, Field


class ReactAgentState(BaseModel):
    """State for React agents with tool usage.

    This state schema handles proper message normalization
    and tracking for ReAct agents.
    """

    # Base message tracking with add_messages reducer
    messages: Sequence[BaseMessage] = Field(
        default_factory=list, description="Conversation messages"
    )

    # LangGraph managed fields for iteration count
    current_step: int = Field(default=0, description="Current execution step")

    remaining_steps: int = Field(default=10, description="Number of steps remaining")

    max_iterations: int = Field(default=10, description="Maximum number of iterations")

    is_last_step: bool = Field(
        default=False, description="Whether this is the last step"
    )

    # Tool tracking
    tool_results: list[dict[str, Any]] = Field(
        default_factory=list, description="Results from tool executions"
    )

    # Error tracking
    error: str | None = Field(default=None, description="Error message if any")

    # Structured output storage
    structured_output: dict[str, Any] | None = Field(
        default=None, description="Structured output from the agent"
    )

    # Reasoning/analysis state
    thought: str | None = Field(default=None, description="Agent's reasoning steps")

    # Memory storage
    memory: dict[str, Any] = Field(
        default_factory=dict, description="Memory for persisting information"
    )

    # Tool usage statistics
    tool_usage_stats: dict[str, int] = Field(
        default_factory=dict, description="Statistics on tool usage"
    )

    # Make field access Dict-like for compatibility with Branches
    def get(self, key: str, default: Any = None) -> Any:
        """Get a field value, similar to dict.get()."""
        return getattr(self, key, default)

    # State check methods
    def has_tool_calls(self) -> bool:
        """Check if the last message has tool calls."""
        return has_tool_calls(self)

    def should_continue(self) -> bool:
        """Determine if agent iteration should continue."""
        # Check if max iterations reached
        if self.current_step >= self.max_iterations:
            return False

        # Check if there's an error
        if self.error:
            return False

        # Check if there are tool calls to execute
        if self.has_tool_calls():
            return True

        # No more actions to take
        return False

    def increment_step(self) -> None:
        """Increment the current step counter."""
        self.current_step += 1
        self.remaining_steps = max(0, self.max_iterations - self.current_step)
        self.is_last_step = self.remaining_steps <= 0

    def update_tool_usage_stats(self, tool_name: str) -> None:
        """Update tool usage statistics."""
        if tool_name in self.tool_usage_stats:
            self.tool_usage_stats[tool_name] += 1
        else:
            self.tool_usage_stats[tool_name] = 1

    # Factory method for creating specialized state with structured output
    @classmethod
    def with_structured_output(cls, output_model_type: type) -> type:
        """Create a specialized state with a typed structured_output field.

        Args:
            output_model_type: Type for structured output

        Returns:
            A new state class with the specified structured output type
        """
        from pydantic import create_model

        return create_model(
            f"ReactAgentState[{output_model_type.__name__}]",
            structured_output=(Optional[output_model_type], Field(default=None)),
            __base__=cls,
        )
