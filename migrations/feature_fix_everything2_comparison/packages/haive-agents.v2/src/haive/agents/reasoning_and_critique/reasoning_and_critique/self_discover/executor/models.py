"""Models for the Self-Discover Executor Agent."""

from pydantic import BaseModel, Field


class StepResult(BaseModel):
    """Result of executing a single reasoning step."""

    step_number: int = Field(..., description="The step number that was executed")
    step_name: str = Field(..., description="Name of the step that was executed")
    findings: str = Field(
        ..., description="What was discovered or concluded in this step"
    )
    evidence: list[str] = Field(
        default_factory=list,
        description="Supporting evidence or reasoning for the findings",
    )
    confidence: float = Field(
        ...,
        description="Confidence level in this step's results (0.0-1.0)",
        ge=0.0,
        le=1.0,
    )
    next_step_recommendations: str | None = Field(
        default=None,
        description="Recommendations for subsequent steps based on these findings",
    )


class ExecutionResult(BaseModel):
    """The complete execution result of the structured reasoning process."""

    task_summary: str = Field(
        ..., description="Brief summary of the task that was solved"
    )
    step_results: list[StepResult] = Field(
        ..., description="Results from each executed reasoning step", min_length=1
    )
    final_solution: str = Field(
        ..., description="The final solution or conclusion reached"
    )
    solution_confidence: float = Field(
        ...,
        description="Overall confidence in the final solution (0.0-1.0)",
        ge=0.0,
        le=1.0,
    )
    supporting_analysis: str = Field(
        ..., description="Analysis explaining how the steps led to the solution"
    )
    alternative_perspectives: list[str] = Field(
        default_factory=list,
        description="Alternative viewpoints or solutions considered",
    )
    implementation_recommendations: str = Field(
        ..., description="Practical recommendations for implementing the solution"
    )
    success_criteria_met: list[str] = Field(
        ..., description="Which success criteria from the structure were satisfied"
    )
