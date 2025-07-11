"""Base models for the unified planning system.

This module provides the foundation for a flexible planning system that can support
various planning patterns including Plan-and-Execute, ReWOO, LLM Compiler, FLARE RAG,
and recursive planning capabilities.

Key Design Principles:
1. Composable: Different planning patterns can mix and match components
2. Extensible: Easy to add new step types and planning patterns
3. Type-safe: Comprehensive validation and type checking
4. Resource-aware: Built-in support for resource tracking and constraints
"""

from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, TypeVar, Union

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    computed_field,
    field_validator,
    model_validator,
)

# ============================================================================
# ENUMS
# ============================================================================


class StepStatus(str, Enum):
    """Universal status for any plan step."""

    PENDING = "pending"  # Not yet started
    READY = "ready"  # Ready to execute (dependencies met)
    IN_PROGRESS = "in_progress"  # Currently executing
    COMPLETED = "completed"  # Successfully completed
    FAILED = "failed"  # Execution failed
    SKIPPED = "skipped"  # Skipped (conditional or user choice)
    BLOCKED = "blocked"  # Blocked by dependencies
    CANCELLED = "cancelled"  # Cancelled by user/system


class StepType(str, Enum):
    """Type of plan step - extensible for different planning patterns."""

    # Basic types
    ACTION = "action"  # Direct action/tool execution
    RESEARCH = "research"  # Information gathering
    ANALYSIS = "analysis"  # Data analysis/processing
    SYNTHESIS = "synthesis"  # Combining information
    VALIDATION = "validation"  # Checking/verifying results
    DECISION = "decision"  # Making choices

    # Advanced types
    RECURSIVE = "recursive"  # Recursive sub-planning
    PARALLEL = "parallel"  # Parallel execution container
    CONDITIONAL = "conditional"  # Conditional branching
    LOOP = "loop"  # Iterative execution
    JOIN = "join"  # Synchronization point

    # Specialized types
    RETRIEVAL = "retrieval"  # RAG retrieval step
    GENERATION = "generation"  # LLM generation step
    TOOL_CALL = "tool_call"  # External tool invocation
    EVIDENCE = "evidence"  # Evidence collection (ReWOO style)


class ExecutionMode(str, Enum):
    """How a step should be executed."""

    SEQUENTIAL = "sequential"  # One at a time
    PARALLEL = "parallel"  # Can run simultaneously
    STREAM = "stream"  # Streaming execution
    BATCH = "batch"  # Batch processing


class DependencyType(str, Enum):
    """Type of dependency between steps."""

    HARD = "hard"  # Must complete before dependent can start
    SOFT = "soft"  # Preferred but not required
    CONDITIONAL = "conditional"  # Depends on condition
    DATA = "data"  # Requires data output from dependency


# ============================================================================
# BASE STEP MODEL
# ============================================================================


class StepMetadata(BaseModel):
    """Metadata for tracking step execution and debugging."""

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    started_at: datetime | None = None
    completed_at: datetime | None = None

    # Execution tracking
    retry_count: int = Field(default=0, ge=0)
    error_count: int = Field(default=0, ge=0)
    last_error: str | None = None

    # Performance metrics
    tokens_used: int | None = Field(default=None, ge=0)
    api_calls_made: int | None = Field(default=None, ge=0)

    # Custom metadata
    tags: set[str] = Field(default_factory=set)
    custom_data: dict[str, Any] = Field(default_factory=dict)

    @computed_field
    @property
    def execution_time(self) -> float | None:
        """Calculate execution time in seconds."""
        if self.started_at and self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        return None


class Dependency(BaseModel):
    """Represents a dependency between steps."""

    step_id: str = Field(description="ID of the step this depends on")
    dependency_type: DependencyType = Field(
        default=DependencyType.HARD, description="Type of dependency"
    )
    condition: str | None = Field(
        default=None, description="Condition for conditional dependencies"
    )
    required_output: str | None = Field(
        default=None, description="Specific output field required from dependency"
    )

    def is_satisfied(self, step_results: dict[str, Any]) -> bool:
        """Check if this dependency is satisfied."""
        if self.step_id not in step_results:
            return False

        if self.dependency_type == DependencyType.SOFT:
            return True  # Soft dependencies are always "satisfied"

        result = step_results[self.step_id]

        # Check condition if specified
        if self.condition and self.dependency_type == DependencyType.CONDITIONAL:
            # Simple condition evaluation (can be extended)
            try:
                # This is simplified - in production use safe evaluation
                return eval(self.condition, {"result": result})
            except:
                return False

        # Check required output
        if self.required_output and isinstance(result, dict):
            return self.required_output in result

        return True


class BaseStep(BaseModel):
    """Base class for all planning steps.

    This provides the core functionality that all step types share,
    while being flexible enough to support various planning patterns.
    """

    model_config = ConfigDict(
        validate_assignment=True,
        use_enum_values=True,
        extra="allow",  # Allow extensions
    )

    # ========================================================================
    # IDENTITY
    # ========================================================================

    id: str = Field(
        default_factory=lambda: f"step_{uuid.uuid4().hex[:8]}",
        description="Unique identifier",
    )

    name: str = Field(
        ..., description="Human-readable name", min_length=1, max_length=200
    )

    description: str = Field(
        default="", description="Detailed description", max_length=1000
    )

    step_type: StepType = Field(default=StepType.ACTION, description="Type of step")

    # ========================================================================
    # EXECUTION
    # ========================================================================

    status: StepStatus = Field(default=StepStatus.PENDING, description="Current status")

    execution_mode: ExecutionMode = Field(
        default=ExecutionMode.SEQUENTIAL, description="How to execute"
    )

    # ========================================================================
    # DATA
    # ========================================================================

    input_data: dict[str, Any] | None = Field(
        default=None, description="Input data/parameters"
    )

    output_data: dict[str, Any] | None = Field(
        default=None, description="Output/results"
    )

    # ========================================================================
    # DEPENDENCIES
    # ========================================================================

    dependencies: list[Dependency] = Field(
        default_factory=list, description="Steps this depends on"
    )

    # ========================================================================
    # METADATA
    # ========================================================================

    metadata: StepMetadata = Field(
        default_factory=StepMetadata, description="Execution metadata"
    )

    priority: int = Field(
        default=5, description="Execution priority (1-10)", ge=1, le=10
    )

    # ========================================================================
    # VALIDATION
    # ========================================================================

    @field_validator("dependencies")
    @classmethod
    def validate_unique_dependencies(cls, v: list[Dependency]) -> list[Dependency]:
        """Ensure no duplicate dependencies."""
        seen = set()
        for dep in v:
            if dep.step_id in seen:
                raise ValueError(f"Duplicate dependency: {dep.step_id}")
            seen.add(dep.step_id)
        return v

    # ========================================================================
    # METHODS
    # ========================================================================

    def add_dependency(
        self,
        step_id: str,
        dependency_type: DependencyType = DependencyType.HARD,
        condition: str | None = None,
        required_output: str | None = None,
    ) -> None:
        """Add a dependency to this step."""
        dep = Dependency(
            step_id=step_id,
            dependency_type=dependency_type,
            condition=condition,
            required_output=required_output,
        )
        self.dependencies.append(dep)

    def is_ready(self, completed_steps: dict[str, Any]) -> bool:
        """Check if all dependencies are satisfied."""
        if self.status != StepStatus.PENDING:
            return False

        for dep in self.dependencies:
            if dep.dependency_type == DependencyType.HARD:
                if not dep.is_satisfied(completed_steps):
                    return False

        return True

    def mark_ready(self) -> None:
        """Mark step as ready to execute."""
        if self.status == StepStatus.PENDING:
            self.status = StepStatus.READY
            self.metadata.updated_at = datetime.now()

    def mark_in_progress(self) -> None:
        """Mark step as in progress."""
        self.status = StepStatus.IN_PROGRESS
        self.metadata.started_at = datetime.now()
        self.metadata.updated_at = datetime.now()

    def mark_completed(self, output: dict[str, Any] | None = None) -> None:
        """Mark step as completed."""
        self.status = StepStatus.COMPLETED
        self.metadata.completed_at = datetime.now()
        self.metadata.updated_at = datetime.now()
        if output is not None:
            self.output_data = output

    def mark_failed(self, error: str) -> None:
        """Mark step as failed."""
        self.status = StepStatus.FAILED
        self.metadata.error_count += 1
        self.metadata.last_error = error
        self.metadata.updated_at = datetime.now()
        if self.metadata.started_at and not self.metadata.completed_at:
            self.metadata.completed_at = datetime.now()

    def to_prompt_format(self) -> str:
        """Format step for inclusion in prompts."""
        status_marker = {
            StepStatus.COMPLETED: "✓",
            StepStatus.FAILED: "✗",
            StepStatus.IN_PROGRESS: "→",
            StepStatus.PENDING: "○",
            StepStatus.READY: "●",
            StepStatus.SKIPPED: "-",
            StepStatus.BLOCKED: "□",
            StepStatus.CANCELLED: "⨯",
        }.get(self.status, "?")

        parts = [f"{status_marker} {self.name}"]
        if self.description:
            parts.append(f"  {self.description}")
        if self.output_data:
            parts.append(f"  Output: {self.output_data}")
        if self.metadata.last_error:
            parts.append(f"  Error: {self.metadata.last_error}")

        return "\n".join(parts)


# ============================================================================
# SPECIALIZED STEP TYPES
# ============================================================================


class ActionStep(BaseStep):
    """Step that performs a specific action or tool call."""

    step_type: StepType = Field(default=StepType.ACTION, frozen=True)

    tool_name: str | None = Field(default=None, description="Name of tool to execute")

    tool_args: dict[str, Any] | None = Field(
        default=None, description="Arguments for tool"
    )

    expected_output_schema: dict[str, Any] | None = Field(
        default=None, description="Expected structure of output"
    )


class ResearchStep(BaseStep):
    """Step for information gathering and research."""

    step_type: StepType = Field(default=StepType.RESEARCH, frozen=True)

    query: str = Field(..., description="Research query or question")

    sources: list[str] = Field(default_factory=list, description="Sources to search")

    max_results: int = Field(default=5, description="Maximum results to retrieve", ge=1)


class RecursiveStep(BaseStep):
    """Step that can spawn sub-plans recursively."""

    step_type: StepType = Field(default=StepType.RECURSIVE, frozen=True)

    sub_objective: str = Field(..., description="Objective for sub-plan")

    max_depth: int = Field(
        default=3, description="Maximum recursion depth", ge=1, le=10
    )

    sub_plan_id: str | None = Field(
        default=None, description="ID of generated sub-plan"
    )


class ConditionalStep(BaseStep):
    """Step with conditional execution paths."""

    step_type: StepType = Field(default=StepType.CONDITIONAL, frozen=True)

    condition: str = Field(..., description="Condition to evaluate")

    then_steps: list[str] = Field(
        default_factory=list, description="Steps to execute if true"
    )

    else_steps: list[str] = Field(
        default_factory=list, description="Steps to execute if false"
    )


class ParallelStep(BaseStep):
    """Container for steps that can execute in parallel."""

    step_type: StepType = Field(default=StepType.PARALLEL, frozen=True)

    parallel_steps: list[str] = Field(
        default_factory=list, description="IDs of steps to run in parallel"
    )

    join_strategy: str = Field(
        default="all", description="How to join results: 'all', 'any', 'majority'"
    )


# Type alias for any step type
AnyStep = Union[
    BaseStep, ActionStep, ResearchStep, RecursiveStep, ConditionalStep, ParallelStep
]


# ============================================================================
# BASE PLAN MODEL
# ============================================================================


class BasePlan(BaseModel):
    """Base class for all planning patterns.

    This provides core planning functionality while allowing different
    planning strategies to extend and customize behavior.
    """

    model_config = ConfigDict(validate_assignment=True, use_enum_values=True)

    # ========================================================================
    # IDENTITY
    # ========================================================================

    id: str = Field(
        default_factory=lambda: f"plan_{uuid.uuid4().hex[:8]}",
        description="Unique plan identifier",
    )

    name: str = Field(..., description="Plan name")

    objective: str = Field(..., description="Main objective/goal")

    # ========================================================================
    # STEPS
    # ========================================================================

    steps: list[AnyStep] = Field(default_factory=list, description="Steps in the plan")

    # ========================================================================
    # METADATA
    # ========================================================================

    created_at: datetime = Field(default_factory=datetime.now)

    updated_at: datetime = Field(default_factory=datetime.now)

    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional plan metadata"
    )

    # ========================================================================
    # COMPUTED PROPERTIES
    # ========================================================================

    @computed_field
    @property
    def total_steps(self) -> int:
        """Total number of steps."""
        return len(self.steps)

    @computed_field
    @property
    def completed_steps(self) -> list[AnyStep]:
        """Get completed steps."""
        return [s for s in self.steps if s.status == StepStatus.COMPLETED]

    @computed_field
    @property
    def failed_steps(self) -> list[AnyStep]:
        """Get failed steps."""
        return [s for s in self.steps if s.status == StepStatus.FAILED]

    @computed_field
    @property
    def pending_steps(self) -> list[AnyStep]:
        """Get pending steps."""
        return [s for s in self.steps if s.status == StepStatus.PENDING]

    @computed_field
    @property
    def ready_steps(self) -> list[AnyStep]:
        """Get steps ready to execute."""
        return [s for s in self.steps if s.status == StepStatus.READY]

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
        """Check if plan is complete."""
        return all(
            s.status in [StepStatus.COMPLETED, StepStatus.SKIPPED] for s in self.steps
        )

    @computed_field
    @property
    def has_failures(self) -> bool:
        """Check if any steps failed."""
        return any(s.status == StepStatus.FAILED for s in self.steps)

    # ========================================================================
    # METHODS
    # ========================================================================

    def add_step(self, step: AnyStep) -> None:
        """Add a step to the plan."""
        self.steps.append(step)
        self.updated_at = datetime.now()

    def get_step(self, step_id: str) -> AnyStep | None:
        """Get step by ID."""
        for step in self.steps:
            if step.id == step_id:
                return step
        return None

    def update_ready_steps(self) -> list[AnyStep]:
        """Update and return steps that are ready to execute."""
        completed = {s.id: s.output_data for s in self.completed_steps}

        ready = []
        for step in self.pending_steps:
            if step.is_ready(completed):
                step.mark_ready()
                ready.append(step)

        return ready

    def get_execution_order(self) -> list[list[AnyStep]]:
        """Get steps organized by execution order (batches for parallel execution)."""
        # This is a simplified topological sort
        # Returns list of batches where each batch can run in parallel

        completed = set()
        remaining = list(self.steps)
        batches = []

        while remaining:
            batch = []

            for step in remaining[:]:
                deps_satisfied = all(
                    dep.step_id in completed
                    for dep in step.dependencies
                    if dep.dependency_type == DependencyType.HARD
                )

                if deps_satisfied:
                    batch.append(step)
                    remaining.remove(step)

            if not batch:
                # Circular dependency or invalid plan
                break

            batches.append(batch)
            completed.update(s.id for s in batch)

        return batches

    def to_prompt_format(self) -> str:
        """Format plan for inclusion in prompts."""
        lines = [
            f"Plan: {self.name}",
            f"Objective: {self.objective}",
            f"Progress: {len(self.completed_steps)}/{self.total_steps} ({self.progress_percentage:.1f}%)",
            "",
            "Steps:",
        ]

        for step in self.steps:
            lines.append(step.to_prompt_format())

        return "\n".join(lines)

    def to_mermaid(self) -> str:
        """Generate Mermaid diagram of plan."""
        lines = ["graph TD"]

        # Add nodes
        for step in self.steps:
            shape = {
                StepType.ACTION: f"{step.id}[{step.name}]",
                StepType.DECISION: f"{step.id}{{{step.name}}}",
                StepType.PARALLEL: f"{step.id}[/{step.name}/]",
                StepType.CONDITIONAL: f"{step.id}{{{{{step.name}}}}}",
            }.get(step.step_type, f"{step.id}[{step.name}]")

            lines.append(f"    {shape}")

        # Add edges
        for step in self.steps:
            for dep in step.dependencies:
                style = {
                    DependencyType.HARD: "-->",
                    DependencyType.SOFT: "-.->",
                    DependencyType.CONDITIONAL: "==>",
                    DependencyType.DATA: "-->",
                }.get(dep.dependency_type, "-->")

                lines.append(f"    {dep.step_id} {style} {step.id}")

        return "\n".join(lines)


# ============================================================================
# PLAN VARIANTS FOR DIFFERENT PATTERNS
# ============================================================================


class SequentialPlan(BasePlan):
    """Traditional sequential execution plan."""

    def add_sequential_step(
        self, step: AnyStep, depends_on_previous: bool = True
    ) -> None:
        """Add step with automatic dependency on previous step."""
        if depends_on_previous and self.steps:
            previous_step = self.steps[-1]
            step.add_dependency(previous_step.id)

        self.add_step(step)


class DAGPlan(BasePlan):
    """Plan with explicit DAG structure (LLM Compiler style)."""

    def validate_dag(self) -> bool:
        """Validate that plan forms a valid DAG (no cycles)."""
        # Simplified cycle detection
        visited = set()
        rec_stack = set()

        def has_cycle(step_id: str) -> bool:
            visited.add(step_id)
            rec_stack.add(step_id)

            step = self.get_step(step_id)
            if step:
                for dep in step.dependencies:
                    if dep.step_id not in visited:
                        if has_cycle(dep.step_id):
                            return True
                    elif dep.step_id in rec_stack:
                        return True

            rec_stack.remove(step_id)
            return False

        return all(
            not (step.id not in visited and has_cycle(step.id)) for step in self.steps
        )


class AdaptivePlan(BasePlan):
    """Plan that can adapt during execution (FLARE style)."""

    adaptation_triggers: list[str] = Field(
        default_factory=list, description="Conditions that trigger adaptation"
    )

    max_adaptations: int = Field(default=3, description="Maximum adaptation cycles")

    adaptation_count: int = Field(default=0, description="Current adaptation count")

    def should_adapt(self, context: dict[str, Any]) -> bool:
        """Check if plan should adapt based on context."""
        if self.adaptation_count >= self.max_adaptations:
            return False

        # Check triggers (simplified)
        for _trigger in self.adaptation_triggers:
            # This would evaluate trigger conditions
            pass

        return False

    def adapt(self, context: dict[str, Any]) -> None:
        """Adapt plan based on execution context."""
        self.adaptation_count += 1
        # Adaptation logic here


# Type variable for generic plan operations
TPlan = TypeVar("TPlan", bound=BasePlan)
