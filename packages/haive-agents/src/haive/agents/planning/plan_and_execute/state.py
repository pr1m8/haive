from agents.plan_and_execute.models import Plan, Step
from pydantic import BaseModel, Field


class PlanAndExecuteState(BaseModel):
    """Represents the state for the PlanAndExecuteAgent."""

    input: str = Field(..., description="The original user query or objective.")
    plan: Plan | None = Field(
        default=None, description="The current plan, including tasks and subtasks."
    )
    past_steps: list[Step] = Field(
        default_factory=list, description="A list of completed steps or actions."
    )
    response: str | None = Field(
        default=None, description="The current response or output from the agent."
    )

    def update_past_steps(self, step: Step):
        """Adds a completed step to `past_steps` and updates the plan accordingly."""
        if step.is_complete():
            self.past_steps.append(step)
            self.plan.remove_completed_steps()  # ✅ Keep plan up-to-date
            self.plan.update_status()  # ✅ Ensure plan reflects latest step statuses

    def get_next_step(self) -> Step | None:
        """Finds the next step that is either 'in_progress' or 'not_started'."""
        if not self.plan:
            return None
        return self.plan.get_last_incomplete_step()

    def is_plan_complete(self) -> bool:
        """Checks if the entire plan is complete."""
        return self.plan is not None and self.plan.status == "complete"
