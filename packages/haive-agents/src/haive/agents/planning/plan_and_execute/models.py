import operator
from typing import Literal, Optional

from pydantic import BaseModel, Field


class Step(BaseModel):
    """Represents a step that can recursively contain nested steps."""

    id: int
    description: str
    status: Literal["not_started", "in_progress", "complete"] = Field(
        default="not_started"
    )
    steps: list["Step"] | None = Field(default_factory=list)  # ✅ Use `default_factory`
    result: str | None = None  # ✅ No `default` Field

    def add_result(self, result: str):
        """Marks the step as complete and stores the result."""
        self.result = result
        self.status = "complete"

    def is_complete(self) -> bool:
        """Check if the step and all its nested steps are complete."""
        return self.status == "complete" and all(
            step.is_complete() for step in self.steps or []
        )

    def remove_completed_substeps(self):
        """Removes substeps that have been marked as complete."""
        self.steps = list(
            filter(operator.not_, map(operator.attrgetter("is_complete"), self.steps))
        )

    @classmethod
    def get_last_incomplete_step(cls, steps: list["Step"]) -> Optional["Step"]:
        """Retrieves the last step that is either 'in_progress' or 'not_started'.
        Prioritizes 'in_progress' steps to ensure they get completed first.
        """
        sorted_steps = sorted(
            steps, key=operator.attrgetter("status"), reverse=True
        )  # Prioritize "in_progress"
        for step in sorted_steps:
            if step.status in {"not_started", "in_progress"}:
                return step
        return None


class Plan(BaseModel):
    """Represents a plan containing a recursive structure of steps."""

    description: str = Field(
        ..., description="Description of the plan"
    )  # ✅ `default` removed
    status: Literal["not_started", "in_progress", "complete"] = "not_started"
    steps: list[Step] = Field(
        default_factory=list
    )  # ✅ Use `default_factory` instead of `default=[]`

    def update_status(self):
        """Updates the overall status of the plan based on step completion."""
        if all(step.is_complete() for step in self.steps):
            self.status = "complete"
        elif any(step.status == "in_progress" for step in self.steps):
            self.status = "in_progress"
        else:
            self.status = "not_started"

    def add_step(self, step: Step):
        """Adds a new step to the plan."""
        self.steps = operator.add(self.steps, [step])  # ✅ Using `operator.add`

    def remove_completed_steps(self):
        """Removes steps that have been completed."""
        self.steps = list(
            filter(operator.not_, map(operator.attrgetter("is_complete"), self.steps))
        )

    def get_last_incomplete_step(self) -> Step | None:
        """Retrieves the last incomplete step (either 'in_progress' or 'not_started')."""
        return Step.get_last_incomplete_step(self.steps)


class Response(BaseModel):
    """Response to user."""

    response: str


class Act(BaseModel):
    """Action to perform."""

    action: Response | Plan = Field(
        description="Action to perform. If you want to respond to user, use Response. "
        "If you need to further use tools to get the answer, use Plan."
    )


# Rebuild forward references for recursive relationships
Step.model_rebuild()
Plan.model_rebuild()
