from enum import Enum
from typing import Any

from langchain_core.messages import AnyMessage
from pydantic import BaseModel, Field


class ReactionData(BaseModel):
    """Data for agent reasoning and action."""

    thought: str | None = Field(default=None, description="Agent's reasoning")
    action: str | None = Field(
        default=None, description="Tool to use or 'final_answer'"
    )
    action_input: str | dict[str, Any] | None = Field(
        default=None, description="Input for the tool or final answer text"
    )


class ActionType(str, Enum):
    """Types of actions that the agent can take."""

    SEARCH = "search"
    CALCULATOR = "calculator"
    WEATHER = "weather"
    DATABASE = "database"
    FINAL_ANSWER = "final_answer"
    # Add more action types as needed


class Action(BaseModel):
    """An action that the agent decides to take."""

    action_type: ActionType
    action_input: str

    def __str__(self):
        return f"{self.action_type}: {self.action_input}"


class Thought(BaseModel):
    """The agent's reasoning process."""

    thought: str
    action: Action

    def __str__(self):
        return f"Thought: {self.thought}\nAction: ActionType.{self.action.action_type}, ActionInput: {self.action.action_input}"


class ReactState(BaseModel):
    """State schema for React agent."""

    messages: list[AnyMessage] = Field(
        default_factory=list
    )  # Removed the operator.add annotation
    thoughts: list[Thought] = Field(default_factory=list)
    observations: list[str] = Field(default_factory=list)
    intermediate_steps: list[dict[str, Any] | tuple[Action, str]] = Field(
        default_factory=list
    )
    final_answer: str | None = None
    current_thought: Thought | None = None
    iteration_count: int = 0
    max_iterations: int = 10
    tools: dict[str, Any] = Field(default_factory=dict)
    tool_names: list[str] = Field(default_factory=list)
    status: str = "thinking"  # thinking, acting, observing, done
    current_action: Action | None = None
    retry_attempts: dict[str, int] = Field(default_factory=dict)
    max_retry_attempts: int = 3
