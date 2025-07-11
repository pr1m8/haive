"""ReWOO Planner State and Models."""

from typing import Any, Dict, List, Optional

from haive.core.schema.prebuilt.llm_state import LLMState
from pydantic import BaseModel, Field

from haive.agents.planning.rewoo.models import ReWOOPlan


class PlannerState(LLMState):
    """State schema for ReWOO planner agent.

    This state extends LLMState to provide planning-specific functionality
    while maintaining tool routing and token tracking capabilities.
    """

    # Available tools for planning context
    available_tools: list[Any] = Field(
        default_factory=list,
        description="Available tools for planning (provided to prompt context)",
    )

    # Generated plan
    generated_plan: ReWOOPlan | None = Field(
        default=None, description="The generated ReWOO plan from structured output"
    )

    # Planning metadata
    planning_metadata: dict[str, Any] = Field(
        default_factory=dict, description="Metadata about the planning process"
    )

    @property
    def tool_options(self) -> list[str]:
        """Get tool names for prompt context."""
        return [
            tool.name if hasattr(tool, "name") else str(tool)
            for tool in self.available_tools
        ]

    def update_plan(self, plan: ReWOOPlan) -> None:
        """Update the generated plan and metadata."""
        self.generated_plan = plan
        self.planning_metadata.update(
            {
                "plan_name": plan.name,
                "objective": plan.objective,
                "step_count": len(plan.steps),
                "evidence_count": len(plan.evidence_map) if plan.evidence_map else 0,
            }
        )

    def has_valid_plan(self) -> bool:
        """Check if we have a valid generated plan."""
        return self.generated_plan is not None and len(self.generated_plan.steps) > 0


class PlannerOutput(BaseModel):
    """Output from the ReWOO planner agent."""

    plan: ReWOOPlan = Field(..., description="The generated ReWOO plan")

    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Planning metadata including tool usage, timing, etc.",
    )

    success: bool = Field(default=True, description="Whether planning was successful")

    errors: list[str] = Field(
        default_factory=list, description="Any errors encountered during planning"
    )
