# src/haive/agents/plan_and_execute/models.py
"""Models for Plan and Execute Agent System.

This module defines the data models for planning, execution, and replanning
in the Plan and Execute agent architecture.
"""

from datetime import datetime
from enum import Enum
from typing import Literal, Union

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    computed_field,
    field_serializer,
    field_validator,
    model_validator,
)


class StepStatus(str, Enum):
    """Status of a plan step."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class StepType(str, Enum):
    """Type of plan step."""

    RESEARCH = "research"
    ANALYSIS = "analysis"
    SYNTHESIS = "synthesis"
    VALIDATION = "validation"
    ACTION = "action"
    DECISION = "decision"


class PlanStep(BaseModel):
    """Individual step in an execution plan."""

    model_config = ConfigDict()

    step_id: int = Field(description="Unique identifier for this step (1-based index)")

    description: str = Field(
        description="Clear, actionable description of what needs to be done"
    )

    step_type: StepType = Field(
        default=StepType.ACTION,
        description="Type of step to help executor choose appropriate approach",
    )

    dependencies: list[int] = Field(
        default_factory=list,
        description="List of step IDs that must be completed before this step",
    )

    expected_output: str = Field(
        description="Description of the expected output/outcome from this step"
    )

    status: StepStatus = Field(
        default=StepStatus.PENDING, description="Current status of the step"
    )

    result: str | None = Field(
        default=None, description="Actual result/output from executing this step"
    )

    error: str | None = Field(default=None, description="Error message if step failed")

    started_at: datetime | None = Field(
        default=None, description="Timestamp when step execution started"
    )

    completed_at: datetime | None = Field(
        default=None, description="Timestamp when step execution completed"
    )

    @field_serializer("started_at", "completed_at")
    def serialize_datetime(self, dt: datetime | None) -> str | None:
        """Serialize datetime fields to ISO format."""
        return dt.isoformat() if dt else None

    @computed_field
    @property
    def is_ready(self) -> bool:
        """Check if step is ready to execute (all dependencies completed)."""
        # This will be validated against actual plan in Plan model
        return self.status == StepStatus.PENDING

    @computed_field
    @property
    def execution_time(self) -> float | None:
        """Calculate execution time in seconds."""
        if self.started_at and self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        return None

    def to_prompt_format(self) -> str:
        """Format step for inclusion in prompts."""
        parts = [f"Step {self.step_id}: {self.description}"]
        if self.expected_output:
            parts.append(f"Expected Output: {self.expected_output}")
        if self.result:
            parts.append(f"Result: {self.result}")
        if self.error:
            parts.append(f"Error: {self.error}")
        return "\n".join(parts)


class Plan(BaseModel):
    """Complete execution plan with steps and metadata."""

    model_config = ConfigDict()

    objective: str = Field(
        description="The main objective/goal this plan aims to achieve"
    )

    steps: list[PlanStep] = Field(description="Ordered list of steps to execute")

    total_steps: int = Field(description="Total number of steps in the plan")

    created_at: datetime = Field(
        default_factory=datetime.now, description="When the plan was created"
    )

    updated_at: datetime = Field(
        default_factory=datetime.now, description="Last time the plan was updated"
    )

    @field_serializer("created_at", "updated_at")
    def serialize_datetime(self, dt: datetime) -> str:
        """Serialize datetime fields to ISO format."""
        return dt.isoformat()

    @field_validator("steps")
    @classmethod
    def validate_step_ids(cls, steps: list[PlanStep]) -> list[PlanStep]:
        """Ensure step IDs are sequential starting from 1."""
        for i, step in enumerate(steps, 1):
            if step.step_id != i:
                step.step_id = i
        return steps

    @field_validator("steps")
    @classmethod
    def validate_dependencies(cls, steps: list[PlanStep]) -> list[PlanStep]:
        """Ensure dependencies reference valid step IDs."""
        step_ids = {step.step_id for step in steps}
        for step in steps:
            invalid_deps = [
                d for d in step.dependencies if d not in step_ids or d >= step.step_id
            ]
            if invalid_deps:
                raise ValueError(
                    f"Step {step.step_id} has invalid dependencies: {invalid_deps}"
                )
        return steps

    @model_validator(mode="after")
    def update_total_steps(self) -> "Plan":
        """Ensure total_steps matches actual step count."""
        self.total_steps = len(self.steps)
        return self

    @computed_field
    @property
    def completed_steps(self) -> list[PlanStep]:
        """Get all completed steps."""
        return [s for s in self.steps if s.status == StepStatus.COMPLETED]

    @computed_field
    @property
    def failed_steps(self) -> list[PlanStep]:
        """Get all failed steps."""
        return [s for s in self.steps if s.status == StepStatus.FAILED]

    @computed_field
    @property
    def pending_steps(self) -> list[PlanStep]:
        """Get all pending steps."""
        return [s for s in self.steps if s.status == StepStatus.PENDING]

    @computed_field
    @property
    def next_step(self) -> PlanStep | None:
        """Get the next step ready for execution."""
        completed_ids = {s.step_id for s in self.completed_steps}

        for step in self.steps:
            if step.status == StepStatus.PENDING:
                # Check if all dependencies are completed
                if all(dep_id in completed_ids for dep_id in step.dependencies):
                    return step
        return None

    @computed_field
    @property
    def progress_percentage(self) -> float:
        """Calculate completion percentage."""
        if self.total_steps == 0:
            return 0.0
        return (len(self.completed_steps) / self.total_steps) * 100

    @computed_field
    @property
    def is_complete(self) -> bool:
        """Check if all steps are completed."""
        return all(s.status == StepStatus.COMPLETED for s in self.steps)

    @computed_field
    @property
    def has_failures(self) -> bool:
        """Check if any steps have failed."""
        return any(s.status == StepStatus.FAILED for s in self.steps)

    def get_step(self, step_id: int) -> PlanStep | None:
        """Get a specific step by ID."""
        for step in self.steps:
            if step.step_id == step_id:
                return step
        return None

    def update_step_status(
        self,
        step_id: int,
        status: StepStatus,
        result: str | None = None,
        error: str | None = None,
    ) -> bool:
        """Update the status of a specific step."""
        step = self.get_step(step_id)
        if not step:
            return False

        step.status = status
        if result is not None:
            step.result = result
        if error is not None:
            step.error = error

        if status == StepStatus.IN_PROGRESS and not step.started_at:
            step.started_at = datetime.now()
        elif status in [StepStatus.COMPLETED, StepStatus.FAILED]:
            step.completed_at = datetime.now()

        self.updated_at = datetime.now()
        return True

    def to_prompt_format(self) -> str:
        """Format plan for inclusion in prompts."""
        lines = [
            f"Objective: {self.objective}",
            f"Total Steps: {self.total_steps}",
            f"Progress: {len(self.completed_steps)}/{self.total_steps} ({self.progress_percentage:.1f}%)",
            "\nSteps:",
        ]

        for step in self.steps:
            status_marker = {
                StepStatus.COMPLETED: "✓",
                StepStatus.FAILED: "✗",
                StepStatus.IN_PROGRESS: "→",
                StepStatus.PENDING: "○",
                StepStatus.SKIPPED: "-",
            }.get(step.status, "?")

            lines.append(f"{status_marker} {step.to_prompt_format()}")

        return "\n".join(lines)


class ExecutionResult(BaseModel):
    """Result from executing a single step."""

    step_id: int = Field(description="ID of the executed step")
    success: bool = Field(description="Whether execution was successful")
    output: str = Field(description="Output/result from the execution")
    error: str | None = Field(default=None, description="Error message if failed")
    execution_time: float | None = Field(
        default=None, description="Time taken in seconds"
    )

    def to_prompt_format(self) -> str:
        """Format result for inclusion in prompts."""
        status = "Success" if self.success else "Failed"
        lines = [f"Step {self.step_id} - {status}"]
        if self.output:
            lines.append(f"Output: {self.output}")
        if self.error:
            lines.append(f"Error: {self.error}")
        if self.execution_time:
            lines.append(f"Time: {self.execution_time:.2f}s")
        return "\n".join(lines)


class ReplanDecision(BaseModel):
    """Decision on whether to replan or provide final answer."""

    decision: Literal["continue", "replan", "answer"] = Field(
        description="Decision on how to proceed"
    )

    reasoning: str = Field(description="Explanation for the decision")

    final_answer: str | None = Field(
        default=None, description="Final answer if decision is 'answer'"
    )

    replan_instructions: str | None = Field(
        default=None, description="Instructions for replanning if decision is 'replan'"
    )

    skip_steps: list[int] | None = Field(
        default=None, description="Step IDs to skip if continuing with modifications"
    )

    @model_validator(mode="after")
    def validate_decision_fields(self) -> "ReplanDecision":
        """Ensure required fields are present based on decision."""
        if self.decision == "answer" and not self.final_answer:
            raise ValueError("final_answer required when decision is 'answer'")
        if self.decision == "replan" and not self.replan_instructions:
            raise ValueError("replan_instructions required when decision is 'replan'")
        return self


# Union type for replan agent output
ReplanAction = Union[Plan, str]  # Either a new Plan or final answer string


class Response(BaseModel):
    """Response to user with final answer."""

    response: str = Field(
        description="The final response/answer to provide to the user"
    )


class Act(BaseModel):
    """Action to perform - either respond with answer or continue with plan."""

    action: Response | Plan = Field(
        description="Action to perform. If you want to respond to user, use Response. "
        "If you need to further use tools to get the answer, use Plan."
    )

    @computed_field
    @property
    def is_final_response(self) -> bool:
        """Check if this is a final response."""
        return isinstance(self.action, Response)

    @computed_field
    @property
    def is_plan(self) -> bool:
        """Check if this is a plan to execute."""
        return isinstance(self.action, Plan)
