from typing import Any

from agents.llm_compiler.models import CompilerPlan, CompilerStep
from langchain_core.messages import BaseMessage
from pydantic import BaseModel, Field


# State model for LLMCompiler agent
class CompilerState(BaseModel):
    """State model for the LLM Compiler agent.

    Tracks:
    - The user's query
    - The current plan
    - Results from executed steps
    - Conversation history
    """

    query: str = Field(default="", description="User's original query")
    plan: CompilerPlan | None = None
    results: dict[int, Any] = Field(
        default_factory=dict, description="Results from executed steps"
    )
    messages: list[BaseMessage] = Field(
        default_factory=list, description="Conversation history"
    )
    replan_count: int = Field(
        default=0, description="Number of times replanning has been attempted"
    )

    def get_highest_step_id(self) -> int:
        """Get the highest step ID in the current plan."""
        if not self.plan or not self.plan.steps:
            return 0
        return max(step.id for step in self.plan.steps)

    def get_executable_steps(self) -> list[CompilerStep]:
        """Get steps that can be executed right now."""
        if not self.plan:
            return []
        return self.plan.get_executable_steps(self.results)

    def all_steps_complete(self) -> bool:
        """Check if all steps in the plan are complete."""
        if not self.plan or not self.plan.steps:
            return False
        return all(step.is_complete() for step in self.plan.steps)

    def has_join_result(self) -> bool:
        """Check if the join step has been executed."""
        if not self.plan:
            return False

        join_step = self.plan.get_join_step()
        if not join_step:
            return False

        return join_step.id in self.results
