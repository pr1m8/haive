from pydantic import BaseModel,Field
from typing import List,Union
# Recursive Task Model


class AdaptedModule(BaseModel):
    """Represents an adapted module"""
    adapted_module: str = Field(description="The adapted module")
class AdaptedModules(BaseModel):
    """Represents a list of adapted modules"""
    adapted_modules: List[AdaptedModule] = Field(default_factory=lambda: [])

from pydantic import BaseModel, Field
from typing import List

class ReasoningModule(BaseModel):
    """Represents a single reasoning module."""
    name: str = Field(description="The name of the reasoning module.")
    description: str = Field(description="A description of the reasoning module.")

class ReasoningModules(BaseModel):
    """Reasoning modules for the self-discovery agent."""
    modules: List[ReasoningModule] = Field(
        default_factory=lambda: [
            ReasoningModule(
                name="Experimentation",
                description="How could I devise an experiment to help solve that problem?"
            ),
            ReasoningModule(
                name="Idea Generation",
                description="Make a list of ideas for solving this problem, and apply them one by one to see if any progress can be made."
            ),
            ReasoningModule(
                name="Simplification",
                description="How can I simplify the problem so that it is easier to solve?"
            ),
            ReasoningModule(
                name="Key Assumptions",
                description="What are the key assumptions underlying this problem?"
            ),
            ReasoningModule(
                name="Risk Analysis",
                description="What are the potential risks and drawbacks of each solution?"
            ),
            ReasoningModule(
                name="Alternative Perspectives",
                description="What are the alternative perspectives or viewpoints on this problem?"
            ),
            ReasoningModule(
                name="Long-Term Implications",
                description="What are the long-term implications of this problem and its solutions?"
            ),
            ReasoningModule(
                name="Problem Decomposition",
                description="How can I break down this problem into smaller, more manageable parts?"
            ),
            ReasoningModule(
                name="Critical Thinking",
                description="Analyze the problem from different perspectives, questioning assumptions, and evaluating evidence or information."
            ),
            ReasoningModule(
                name="Creative Thinking",
                description="Generate innovative and out-of-the-box ideas to solve the problem. Explore unconventional solutions."
            ),
            ReasoningModule(
                name="Systems Thinking",
                description="Consider the problem as part of a larger system and understand interconnected elements."
            ),
            ReasoningModule(
                name="Core Issue Identification",
                description="What is the core issue or problem that needs to be addressed?"
            ),
            ReasoningModule(
                name="Underlying Causes",
                description="What are the underlying causes or factors contributing to the problem?"
            ),
            ReasoningModule(
                name="Past Solutions",
                description="Have potential solutions been tried before? What were the outcomes?"
            ),
            ReasoningModule(
                name="Obstacles and Challenges",
                description="What obstacles might arise in solving this problem?"
            ),
            ReasoningModule(
                name="Data Analysis",
                description="Are there relevant data or information available? How can it be analyzed?"
            ),
            ReasoningModule(
                name="Stakeholder Perspectives",
                description="Who are the stakeholders affected by the problem? What are their perspectives?"
            ),
            ReasoningModule(
                name="Resource Assessment",
                description="What resources are needed to tackle the problem effectively?"
            ),
            ReasoningModule(
                name="Progress Measurement",
                description="How can progress or success in solving the problem be measured?"
            ),
            ReasoningModule(
                name="Technical Expertise",
                description="Is the problem technical or practical? What expertise is required?"
            ),
            ReasoningModule(
                name="Conceptual Analysis",
                description="Is the problem conceptual or theoretical?"
            ),
            ReasoningModule(
                name="Design Challenge",
                description="Is the problem a design challenge requiring creative solutions?"
            ),
            ReasoningModule(
                name="Step-by-Step Plan",
                description="Let’s make a step-by-step plan and implement it with good notation and explanation."
            )
        ]
    )
from pydantic import BaseModel, Field
from typing import List, Literal, Optional, Union

# Status Model

from pydantic import BaseModel, Field
from typing import List, Literal, Optional, Union

class ReasoningModule(BaseModel):
    """
    Represents a reasoning module.
    """
    name: str = Field(description="The name of the reasoning module.")
    description: str = Field(description="A description of the reasoning module.")

class Step(BaseModel):
    """
    Represents a step in the plan, which can contain nested steps and reasoning modules.
    """
    id: int = Field(description="The unique identifier for the step.")
    description: str = Field(description="A description of the step.")
    status: Literal["not_started", "in_progress", "complete"] = "not_started"
    reasoning_modules: List[ReasoningModule] = Field(
        default_factory=lambda: [],
        description="A list of reasoning modules associated with this step."
    )
    response: Optional[str] = Field(default=None, description="Stores the response/output of the step.")  # ✅ New field
    subtasks: Optional[List["Step"]] = Field(
        default_factory=lambda: [],
        description="A list of subtasks nested under this step."
    )

    def is_complete(self) -> bool:
        """
        Check if the step and all its subtasks are complete.
        """
        return (
            self.status == "complete"
            and all(subtask.is_complete() for subtask in self.subtasks or [])
        )

    def add_response(self, response: str):
        """
        Adds a response to the step and marks it as complete.
        """
        self.response = response
        self.status = "complete"

    class Config:
        orm_mode = True

class Plan(BaseModel):
    """
    Represents a plan containing a recursive structure of steps.
    """
    description: str = Field(..., description="Description of the plan")  # ✅ `default` removed
    status: Literal["not_started", "in_progress", "complete"] = "not_started"
    steps: List[Step] = Field(default_factory=list)  # ✅ Use `default_factory` instead of `default=[]`

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


# Response Model
class Response(BaseModel):
    """
    Represents a response to a user.
    """
    response: str = Field(description="The response to the user.")


# Act Model
class Act(BaseModel):
    """
    Represents an action to perform.
    """
    action: Union[Response, Plan] = Field(
        description=(
            "Action to perform. If you want to respond to the user, use Response. "
            "If you need to further use tools to get the answer, use Plan."
        )
    )

# Rebuild forward references for recursive relationships
Step.model_rebuild()
Plan.model_rebuild()