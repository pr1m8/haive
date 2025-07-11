from typing import Any

from pydantic import ConfigDict, Field

from haive.agents.simple.state import SimpleAgentState


class ReactAgentState(SimpleAgentState):
    """State for React Agent, extending SimpleAgentState.

    Adds fields for tool results, intermediate reasoning,
    and structured output.
    """

    # Inherit messages field from SimpleAgentState

    # Tool-related fields
    tool_results: list[dict[str, Any]] = Field(default_factory=list)
    active_tools: list[str] = Field(default_factory=list)
    selected_tools: list[dict[str, Any]] = Field(default_factory=list)

    # Reasoning-related fields
    intermediate_steps: list[dict[str, Any]] = Field(default_factory=list)
    reasoning: str | None = None

    # Output-related fields
    structured_output: dict[str, Any] | None = None
    final_answer: str | None = None

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )
