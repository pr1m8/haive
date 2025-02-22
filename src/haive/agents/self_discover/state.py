from typing_extensions import TypedDict,Optional
from pydantic import Field
from typing import List
from src.haive.agents.self_discover.models import Plan
from typing_extensions import TypedDict, Optional
from pydantic import Field
from typing import List
from src.haive.agents.self_discover.models import Plan

class SelfDiscoverState(TypedDict):
    """State for the Self Discover Agent"""
    task_description: str = Field(description="Task description")
    selected_modules: Optional[str] = Field(description="Selected modules")
    plan: Optional[Plan] = Field(default=None, description="Plan to solve the problem with reasoning steps")
    adapted_modules: Optional[str] = Field(default=None, description="Adapted reasoning modules")
    reasoning_structure: Optional[str] = Field(default=None, description="Structured reasoning plan")
    answer: Optional[str] = Field(default=None, description="Final Answer")

    def add_response_to_plan(self, step_id: int, response: str):
        """
        Adds a response to the corresponding step in the plan.
        """
        if self.plan:
            for step in self.plan.steps:
                if step.id == step_id:
                    step.add_re
