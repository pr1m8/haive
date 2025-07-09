# src/haive/agents/react/state.py

from collections.abc import Sequence
from typing import Annotated, Any

from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages
from pydantic import BaseModel, Field


class ReactAgentState(BaseModel):
    """State schema for React agent."""

    # Messages with the add_messages reducer
    messages: Annotated[Sequence[BaseMessage], add_messages] = Field(
        default_factory=list, description="Messages in the conversation"
    )

    # Tool results
    tool_results: list[dict[str, Any]] = Field(
        default_factory=list, description="Results from tool executions"
    )

    # Track iterations
    iteration: int = Field(default=0, description="Current iteration count")

    # Optional structured output
    structured_output: dict[str, Any] | None = Field(
        default=None, description="Structured output from the agent"
    )

    # Other useful state tracking
    intermediate_steps: list[dict[str, Any]] = Field(
        default_factory=list, description="Intermediate reasoning steps"
    )

    # Flag for human assistance
    requires_human_input: bool = Field(
        default=False, description="Flag to indicate if human input is required"
    )

    # Human request content
    human_request: str | None = Field(
        default=None, description="Request for human assistance"
    )
