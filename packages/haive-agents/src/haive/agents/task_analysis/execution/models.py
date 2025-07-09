# src/haive/agents/task_analysis/execution/models.py

from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class ResourceType(str, Enum):
    """Types of resources needed for execution."""

    HUMAN = "human"
    COMPUTE = "compute"
    API = "api"
    STORAGE = "storage"
    NETWORK = "network"
    TOOL = "tool"
    DATA = "data"


class ExecutionPhase(BaseModel):
    """A phase in the execution plan."""

    phase_id: str = Field(..., description="Unique phase identifier")
    phase_number: int = Field(..., ge=1, description="Sequential phase number")
    name: str = Field(..., description="Phase name")
    description: str = Field(default="", description="Phase description")

    # Tasks in this phase
    task_ids: list[str] = Field(default_factory=list)
    parallel_groups: list[list[str]] = Field(
        default_factory=list, description="Groups of tasks that can run in parallel"
    )

    # Timing
    estimated_duration_minutes: float = Field(..., gt=0)
    can_start_early: bool = Field(default=False)
    earliest_start_minutes: float | None = None

    # Dependencies
    depends_on_phases: list[str] = Field(default_factory=list)

    # Resources
    required_resources: dict[ResourceType, float] = Field(
        default_factory=dict, description="Resource requirements (type -> amount)"
    )

    # Completion criteria
    completion_criteria: list[str] = Field(default_factory=list)

    def add_task(self, task_id: str, group_index: int | None = None):
        """Add a task to this phase."""
        if task_id not in self.task_ids:
            self.task_ids.append(task_id)

        if group_index is not None:
            # Add to specific parallel group
            while len(self.parallel_groups) <= group_index:
                self.parallel_groups.append([])
            if task_id not in self.parallel_groups[group_index]:
                self.parallel_groups[group_index].append(task_id)


class JoinPoint(BaseModel):
    """Represents where parallel execution paths converge."""

    join_id: str = Field(..., description="Unique join identifier")
    join_type: Literal["aggregate", "merge", "select", "custom"] = Field(...)

    # Tasks involved
    input_task_ids: list[str] = Field(..., min_length=2)
    output_task_id: str = Field(...)

    # Join logic
    join_function: str = Field(
        default="merge", description="How to combine results (merge, sum, concat, etc.)"
    )
    custom_logic: str | None = Field(
        default=None, description="Custom join logic description"
    )

    # Execution
    wait_for_all: bool = Field(
        default=True, description="Wait for all inputs vs proceed with partial"
    )
    timeout_minutes: float | None = Field(
        default=None, description="Max wait time before proceeding"
    )

    # Error handling
    on_partial_failure: Literal["fail", "continue", "retry"] = Field(default="continue")
    fallback_strategy: str | None = None


class ResourceAllocation(BaseModel):
    """Resource allocation over time."""

    phase_id: str
    resource_type: ResourceType
    amount: float
    start_time_minutes: float
    duration_minutes: float

    # Optional fields
    cost_per_unit: float | None = None
    availability: float | None = Field(default=1.0, ge=0, le=1)


class ExecutionPlan(BaseModel):
    """Complete execution plan for a task."""

    plan_id: str = Field(..., description="Unique plan identifier")
    name: str = Field(..., description="Plan name")

    # Phases
    phases: list[ExecutionPhase] = Field(default_factory=list)
    phase_dependencies: dict[str, list[str]] = Field(
        default_factory=dict, description="Phase ID -> List of dependent phase IDs"
    )

    # Join points
    join_points: list[JoinPoint] = Field(default_factory=list)

    # Critical path
    critical_path_task_ids: list[str] = Field(default_factory=list)
    critical_path_duration_minutes: float = Field(default=0.0)

    # Overall timing
    total_duration_minutes: float = Field(..., gt=0)
    parallel_efficiency: float = Field(default=1.0, ge=0, le=1)

    # Resources
    resource_timeline: list[ResourceAllocation] = Field(default_factory=list)
    peak_resource_usage: dict[ResourceType, float] = Field(default_factory=dict)

    # Risk and optimization
    bottlenecks: list[str] = Field(default_factory=list)
    optimization_opportunities: list[str] = Field(default_factory=list)

    # Execution metadata
    can_checkpoint: bool = Field(default=True)
    checkpoint_phases: list[str] = Field(default_factory=list)

    def add_phase(self, phase: ExecutionPhase):
        """Add a phase to the plan."""
        self.phases.append(phase)
        # Update phase number
        phase.phase_number = len(self.phases)

    def calculate_critical_path(self) -> list[str]:
        """Calculate and return the critical path."""
        # This would implement CPM algorithm
        # For now, return stored critical path
        return self.critical_path_task_ids

    def get_phase_by_task(self, task_id: str) -> ExecutionPhase | None:
        """Find which phase contains a task."""
        for phase in self.phases:
            if task_id in phase.task_ids:
                return phase
        return None
