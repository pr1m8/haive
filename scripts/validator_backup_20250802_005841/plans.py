"""Plan Models for ReWOO Planning.

ExecutionPlan that takes generic AbstractStep instances with computed fields.
"""

from datetime import datetime
from uuid import uuid4

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    computed_field,
    field_validator,
    model_validator,
)

from .steps import AbstractStep


class ExecutionPlan(BaseModel):
    """A plan that works with any AbstractStep implementation."""

    model_config = ConfigDict(
        str_strip_whitespace=True, validate_assignment=True, extra="forbid"
    )

    # Core identity
    id: str = Field(
        default_factory=lambda: f"plan_{uuid4().hex[:8]}",
        description="Unique plan identifier",
    )

    name: str = Field(
        ..., min_length=1, max_length=200, description="Human-readable plan name"
    )

    description: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="Detailed description of the plan",
    )

    # The steps - generic AbstractStep instances
    steps: list[AbstractStep] = Field(
        default_factory=list, description="List of steps in the plan"
    )

    # Timing
    created_at: datetime = Field(
        default_factory=datetime.now, description="When the plan was created"
    )

    # Computed fields - automatically calculated
    @computed_field
    @property
    def step_count(self) -> int:
        """Total number of steps."""
        return len(self.steps)

    @computed_field
    @property
    def step_ids(self) -> list[str]:
        """List of all step IDs."""
        return [step.id for step in self.steps]

    @computed_field
    @property
    def has_dependencies(self) -> bool:
        """Whether any step has dependencies."""
        return any(step.has_dependencies for step in self.steps)

    @computed_field
    @property
    def execution_levels(self) -> list[list[str]]:
        """Steps organized by execution level for parallelization."""
        if not self.steps:
            return []

        levels = []
        {step.id: step for step in self.steps}
        processed = set()

        while len(processed) < len(self.steps):
            level_steps = []

            for step in self.steps:
                if step.id in processed:
                    continue

                # Check if all dependencies are processed
                deps_ready = all(dep in processed for dep in step.depends_on)

                if deps_ready:
                    level_steps.append(step.id)

            if not level_steps:
                # Handle case where remaining steps have unmet dependencies
                # Take any unprocessed step (shouldn't happen with validation)
                for step in self.steps:
                    if step.id not in processed:
                        level_steps.append(step.id)
                        break

            levels.append(level_steps)
            processed.update(level_steps)

        return levels

    @computed_field
    @property
    def max_parallelism(self) -> int:
        """Maximum number of steps that can run in parallel."""
        return (
            max(len(level) for level in self.execution_levels)
            if self.execution_levels
            else 0
        )

    # Validators
    @field_validator("steps")
    @classmethod
    def validate_steps(cls, v: list[AbstractStep]) -> list[AbstractStep]:
        """Validate steps and check for duplicate IDs."""
        if not v:
            return v

        # Check for duplicate IDs
        step_ids = [step.id for step in v]
        if len(step_ids) != len(set(step_ids)):
            raise ValueError("Duplicate step IDs found")

        # Check for invalid dependencies
        for step in v:
            for dep in step.depends_on:
                if dep not in step_ids:
                    raise ValueError(
                        f"Step '{step.id}' depends on unknown step '{dep}'"
                    )

        return v

    @model_validator(mode="after")
    @classmethod
    def validate_no_circular_dependencies(cls) -> "ExecutionPlan":
        """Validate no circular dependencies exist."""
        if not self.steps:
            return self

        # Simple cycle detection using DFS
        visited = set()
        rec_stack = set()

        def has_cycle(step_id: str) -> bool:
            if step_id in rec_stack:
                return True
            if step_id in visited:
                return False

            visited.add(step_id)
            rec_stack.add(step_id)

            # Find step by ID
            step = next((s for s in self.steps if s.id == step_id), None)
            if step:
                for dep in step.depends_on:
                    if has_cycle(dep):
                        return True

            rec_stack.remove(step_id)
            return False

        for step in self.steps:
            if has_cycle(step.id):
                raise ValueError("Circular dependency detected in plan")

        return self

    # Utility methods
    def add_step(self, step: AbstractStep):
        """Add a step to the plan."""
        self.steps.append(step)
        # Computed fields will automatically recalculate

    def get_step_by_id(self, step_id: str) -> AbstractStep | None:
        """Get step by ID."""
        return next((step for step in self.steps if step.id == step_id), None)

    def get_ready_steps(self, completed_steps: set[str]) -> list[AbstractStep]:
        """Get steps that are ready to execute."""
        return [step for step in self.steps if step.can_execute(completed_steps)]
