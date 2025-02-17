from pydantic import BaseModel, Field
from typing import List, Literal, Optional



class Step(BaseModel):
    """
    Represents a step that can recursively contain nested steps.
    """
    id: int
    description: str
    status: Literal["not_started", "in_progress", "complete"] = Field(default="not_started")
    steps: Optional[List['Step']] = []
    result: Optional[str] = Field(default=None)

    def add_result(self, result: str):
        """
        Marks the step as complete and stores the result.
        """
        self.result = result
        self.status = "complete"

    def is_complete(self) -> bool:
        """
        Check if the step and all its nested steps are complete.
        """
        return self.status == "complete" and all(step.is_complete() for step in self.steps or [])

    def remove_completed_substeps(self):
        """
        Removes substeps that have been marked as complete.
        """
        self.steps = [step for step in self.steps if not step.is_complete()]


class Plan(BaseModel):
    """
    Represents a plan containing a recursive structure of steps.
    """
    
    description: str = Field(default="", description="Description of the plan")
    status: Literal["not_started", "in_progress", "complete"] = "not_started"
    steps: List[Step] = []

    def update_status(self):
        """
        Updates the overall status of the plan based on step completion.
        """
        if all(step.is_complete() for step in self.steps):
            self.status = "complete"
        elif any(step.status == "in_progress" for step in self.steps):
            self.status = "in_progress"
        else:
            self.status = "not_started"

    def add_step(self, step: Step):
        """
        Adds a new step to the plan.
        """
        self.steps.append(step)

    def remove_completed_steps(self):
        """
        Removes steps that have been completed.
        """
        self.steps = [step for step in self.steps if not step.is_complete()]
from typing import Union
class Response(BaseModel):
    """Response to user."""

    response: str


class Act(BaseModel):
    """Action to perform."""

    action: Union[Response, Plan] = Field(
        description="Action to perform. If you want to respond to user, use Response. "
        "If you need to further use tools to get the answer, use Plan."
    )


# Rebuild forward references for recursive relationships
Step.model_rebuild()
#Plan.model_rebuild()
