"""State schema for Reflection Agent."""

from haive.core.schema.prebuilt.multi_agent_state import MultiAgentState
from pydantic import Field

from haive.agents.reflection.models import Critique, Improvement


class ReflectionState(MultiAgentState):
    """State for Reflection Agent."""

    input: str = Field(..., description="The original content to reflect on")
    current_content: str = Field(..., description="Current version of the content")

    critique: Critique | None = Field(
        default=None, description="Current critique of the content"
    )

    improvements: list[Improvement] = Field(
        default_factory=list, description="List of improvements made"
    )

    iteration_count: int = Field(default=0, description="Current iteration number")

    max_iterations: int = Field(default=3, description="Maximum number of iterations")

    quality_threshold: float = Field(
        default=0.8, description="Quality threshold to stop iterating"
    )

    final_content: str | None = Field(
        default=None, description="Final improved content"
    )

    def should_continue(self) -> bool:
        """Check if reflection should continue."""
        if self.iteration_count >= self.max_iterations:
            return False

        if self.critique and self.critique.quality_score >= self.quality_threshold:
            return False

        return self.critique is None or self.critique.needs_improvement

    def add_improvement(self, improvement: Improvement) -> None:
        """Add improvement and update current content."""
        self.improvements.append(improvement)
        self.current_content = improvement.improved_content
        self.iteration_count += 1

    def finalize(self) -> str:
        """Finalize the reflection process."""
        self.final_content = self.current_content
        return self.final_content
