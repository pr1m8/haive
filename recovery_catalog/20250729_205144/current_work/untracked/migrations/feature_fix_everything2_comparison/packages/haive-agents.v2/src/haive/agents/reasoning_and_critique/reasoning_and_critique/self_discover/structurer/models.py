"""Models for the Self-Discover Structurer Agent."""

from pydantic import BaseModel, Field


class ReasoningStep(BaseModel):
    """A single step in the structured reasoning process."""

    step_number: int = Field(
        ..., description="The order of this step in the reasoning process"
    )
    step_name: str = Field(..., description="Descriptive name for this reasoning step")
    guiding_questions: list[str] = Field(
        ..., description="Key questions to address in this step", min_length=2
    )
    expected_output: str = Field(
        ..., description="What should be produced or decided in this step"
    )
    dependencies: list[str] = Field(
        default_factory=list, description="Names of previous steps this step depends on"
    )


class ReasoningStructure(BaseModel):
    """The complete structured reasoning plan."""

    task_context: str = Field(
        ..., description="Brief context about the task this structure addresses"
    )
    reasoning_steps: list[ReasoningStep] = Field(
        ..., description="Ordered list of reasoning steps to follow", min_length=3
    )
    integration_approach: str = Field(
        ..., description="How the steps work together to solve the problem"
    )
    success_criteria: list[str] = Field(
        ...,
        description="Criteria for determining if the reasoning was successful",
        min_length=2,
    )
    execution_notes: str = Field(
        ..., description="Important notes for executing this reasoning structure"
    )
