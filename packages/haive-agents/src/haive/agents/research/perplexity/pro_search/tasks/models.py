# recursive_planning_models.py
"""
Pydantic models for recursive conditional planning with tree-based task decomposition.
Supports dynamic planning, parallel execution, and adaptive replanning.
"""

import json
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Callable, Dict, List, Literal, Optional, Set, Union
from uuid import uuid4

from pydantic import BaseModel, Field, computed_field, field_validator, model_validator

# ============================================================================
# Task Status and Priority Enums
# ============================================================================


class TaskStatus(str, Enum):
    """Status of a task in the planning tree."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"
    DEFERRED = "deferred"


class TaskPriority(str, Enum):
    """Priority levels for tasks."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    OPTIONAL = "optional"


# ============================================================================
# Core Planning Models
# ============================================================================


class TaskDependency(BaseModel):
    """Dependency relationship between tasks."""

    task_id: str = Field(description="ID of the dependent task")
    dependency_type: Literal["requires", "blocks", "relates_to"] = Field(
        default="requires", description="Type of dependency relationship"
    )
    is_strict: bool = Field(
        default=True, description="Whether this dependency must be satisfied"
    )
    condition: Optional[str] = Field(
        default=None, description="Optional condition for the dependency"
    )


class TaskResource(BaseModel):
    """Resource requirements for a task."""

    resource_type: Literal["tool", "data", "model", "api", "human"] = Field(
        description="Type of resource needed"
    )
    resource_id: str = Field(description="Identifier for the specific resource")
    quantity: float = Field(default=1.0, ge=0, description="Amount of resource needed")
    is_exclusive: bool = Field(
        default=False, description="Whether this task needs exclusive access"
    )

    @computed_field
    @property
    def resource_key(self) -> str:
        """Unique key for this resource requirement."""
        return f"{self.resource_type}:{self.resource_id}"


class TaskMetadata(BaseModel):
    """Metadata for task tracking and optimization."""

    estimated_duration_seconds: int = Field(
        default=60, ge=0, description="Estimated time to complete"
    )
    actual_duration_seconds: Optional[int] = Field(
        default=None, description="Actual time taken (after completion)"
    )
    retry_count: int = Field(default=0, ge=0, description="Number of retry attempts")
    max_retries: int = Field(default=3, ge=0, description="Maximum retry attempts")
    last_error: Optional[str] = Field(default=None, description="Last error message")
    tags: Set[str] = Field(default_factory=set, description="Tags for categorization")

    @computed_field
    @property
    def can_retry(self) -> bool:
        """Check if task can be retried."""
        return self.retry_count < self.max_retries

    @computed_field
    @property
    def efficiency_ratio(self) -> Optional[float]:
        """Calculate efficiency ratio (estimated vs actual)."""
        if self.actual_duration_seconds and self.estimated_duration_seconds > 0:
            return self.estimated_duration_seconds / self.actual_duration_seconds
        return None


class TaskNode(BaseModel):
    """Individual task node in the planning tree."""

    # Core identifiers
    task_id: str = Field(default_factory=lambda: f"task_{uuid4().hex[:8]}")
    parent_id: Optional[str] = Field(default=None, description="Parent task ID")

    # Task definition
    name: str = Field(min_length=1, description="Task name")
    description: str = Field(description="Detailed task description")
    task_type: Literal["action", "decision", "parallel", "sequential", "loop"] = Field(
        default="action", description="Type of task node"
    )

    # Execution details
    action: Optional[str] = Field(
        default=None, description="Action to execute (for action nodes)"
    )
    decision_criteria: Optional[str] = Field(
        default=None, description="Decision criteria (for decision nodes)"
    )
    loop_condition: Optional[str] = Field(
        default=None, description="Loop continuation condition (for loop nodes)"
    )

    # Status and priority
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM)

    # Relationships
    children: List[str] = Field(default_factory=list, description="Child task IDs")
    dependencies: List[TaskDependency] = Field(
        default_factory=list, description="Task dependencies"
    )

    # Resources and metadata
    required_resources: List[TaskResource] = Field(
        default_factory=list, description="Required resources"
    )
    metadata: TaskMetadata = Field(
        default_factory=TaskMetadata, description="Task metadata"
    )

    # Results
    result: Optional[Dict[str, Any]] = Field(
        default=None, description="Task execution result"
    )

    @field_validator("children")
    @classmethod
    def validate_children_for_type(cls, v, info):
        """Validate children based on task type."""
        task_type = info.data.get("task_type", "action")

        if task_type == "action" and len(v) > 0:
            raise ValueError("Action nodes cannot have children")
        elif task_type in ["parallel", "sequential"] and len(v) == 0:
            # These types typically should have children, but allow empty for initialization
            pass

        return v

    @computed_field
    @property
    def is_leaf(self) -> bool:
        """Check if this is a leaf node."""
        return len(self.children) == 0

    @computed_field
    @property
    def is_executable(self) -> bool:
        """Check if task can be executed."""
        return (
            self.status == TaskStatus.PENDING
            and self.task_type == "action"
            and self.action is not None
        )

    @computed_field
    @property
    def is_complete(self) -> bool:
        """Check if task is complete."""
        return self.status in [TaskStatus.COMPLETED, TaskStatus.CANCELLED]

    def can_start(self, completed_tasks: Set[str]) -> bool:
        """Check if all dependencies are satisfied."""
        for dep in self.dependencies:
            if dep.is_strict and dep.task_id not in completed_tasks:
                return False
        return True


# ============================================================================
# Planning Strategy Models
# ============================================================================


class PlanningStrategy(BaseModel):
    """Strategy configuration for the planning process."""

    max_depth: int = Field(
        default=5, ge=1, le=10, description="Maximum depth of task tree"
    )
    max_width: int = Field(
        default=10, ge=1, le=20, description="Maximum children per node"
    )
    parallelization_threshold: int = Field(
        default=3, ge=2, description="Min tasks to create parallel node"
    )

    decomposition_strategy: Literal[
        "breadth_first", "depth_first", "balanced", "adaptive"
    ] = Field(default="balanced")

    optimization_goals: List[
        Literal[
            "minimize_time",
            "minimize_resources",
            "maximize_parallelism",
            "maximize_reliability",
            "balanced",
        ]
    ] = Field(default_factory=lambda: ["balanced"])

    allow_dynamic_replanning: bool = Field(
        default=True, description="Allow replanning during execution"
    )

    resource_constraints: Dict[str, int] = Field(
        default_factory=dict, description="Resource limits (e.g., {'api_calls': 100})"
    )

    @model_validator(mode="after")
    def validate_strategy_coherence(self) -> "PlanningStrategy":
        """Ensure strategy settings are coherent."""
        if "maximize_parallelism" in self.optimization_goals:
            if self.parallelization_threshold > 5:
                self.parallelization_threshold = 3

        return self


# ============================================================================
# Task Decomposition Models
# ============================================================================


class TaskDecomposition(BaseModel):
    """Result of decomposing a high-level task."""

    original_task: str = Field(description="Original task description")

    decomposition_reasoning: str = Field(
        min_length=20, description="Reasoning for how task was decomposed"
    )

    subtasks: List[TaskNode] = Field(min_length=1, description="Decomposed subtasks")

    execution_order: Literal["sequential", "parallel", "mixed"] = Field(
        default="sequential", description="How subtasks should be executed"
    )

    estimated_total_duration: int = Field(
        ge=0, description="Total estimated duration in seconds"
    )

    critical_path: List[str] = Field(
        default_factory=list, description="Task IDs forming the critical path"
    )

    @model_validator(mode="after")
    def calculate_critical_path(self) -> "TaskDecomposition":
        """Calculate critical path if not provided."""
        if not self.critical_path and self.subtasks:
            # Simple critical path: longest chain of dependencies
            # In practice, this would use proper graph algorithms
            task_map = {t.task_id: t for t in self.subtasks}

            # Find root tasks (no dependencies)
            roots = [t for t in self.subtasks if not t.dependencies]

            if roots:
                # Follow longest path from first root
                path = [roots[0].task_id]
                current = roots[0]

                while current.children:
                    # Pick child with highest priority
                    child_id = current.children[0]
                    if child_id in task_map:
                        path.append(child_id)
                        current = task_map[child_id]
                    else:
                        break

                self.critical_path = path

        return self

    @computed_field
    @property
    def parallelizable_groups(self) -> List[List[str]]:
        """Identify groups of tasks that can run in parallel."""
        groups = []

        # Group tasks by their dependencies
        dependency_levels: Dict[int, List[str]] = {}
        task_map = {t.task_id: t for t in self.subtasks}

        # Simple level assignment (in practice, use topological sort)
        for task in self.subtasks:
            if not task.dependencies:
                level = 0
            else:
                # Max level of dependencies + 1
                level = 1  # Simplified

            if level not in dependency_levels:
                dependency_levels[level] = []
            dependency_levels[level].append(task.task_id)

        # Each level can run in parallel
        groups = list(dependency_levels.values())

        return groups


# ============================================================================
# Planning State Models
# ============================================================================


class PlanningState(BaseModel):
    """State for recursive planning workflow."""

    # Goal definition
    goal: str = Field(description="High-level goal to achieve")
    context: Dict[str, Any] = Field(
        default_factory=dict, description="Context information for planning"
    )
    constraints: List[str] = Field(
        default_factory=list, description="Constraints to consider"
    )

    # Planning configuration
    strategy: PlanningStrategy = Field(
        default_factory=PlanningStrategy, description="Planning strategy configuration"
    )

    # Task tree
    root_task: Optional[TaskNode] = Field(
        default=None, description="Root of the task tree"
    )
    all_tasks: Dict[str, TaskNode] = Field(
        default_factory=dict, description="All tasks indexed by ID"
    )

    # Execution state
    completed_tasks: Set[str] = Field(
        default_factory=set, description="IDs of completed tasks"
    )
    failed_tasks: Set[str] = Field(
        default_factory=set, description="IDs of failed tasks"
    )
    active_tasks: Set[str] = Field(
        default_factory=set, description="IDs of currently active tasks"
    )

    # Resource tracking
    resource_usage: Dict[str, float] = Field(
        default_factory=dict, description="Current resource usage"
    )

    # Planning iterations
    planning_iterations: int = Field(
        default=0, description="Number of planning iterations"
    )
    replanning_triggers: List[str] = Field(
        default_factory=list, description="Events that triggered replanning"
    )

    @computed_field
    @property
    def executable_tasks(self) -> List[TaskNode]:
        """Get tasks ready for execution."""
        ready = []
        for task_id, task in self.all_tasks.items():
            if (
                task.is_executable
                and task_id not in self.active_tasks
                and task_id not in self.completed_tasks
                and task.can_start(self.completed_tasks)
            ):
                ready.append(task)

        # Sort by priority
        priority_order = {
            TaskPriority.CRITICAL: 0,
            TaskPriority.HIGH: 1,
            TaskPriority.MEDIUM: 2,
            TaskPriority.LOW: 3,
            TaskPriority.OPTIONAL: 4,
        }

        return sorted(ready, key=lambda t: priority_order[t.priority])

    @computed_field
    @property
    def completion_percentage(self) -> float:
        """Calculate completion percentage."""
        if not self.all_tasks:
            return 0.0

        return len(self.completed_tasks) / len(self.all_tasks) * 100

    @computed_field
    @property
    def is_complete(self) -> bool:
        """Check if planning goal is achieved."""
        if not self.root_task:
            return False

        return self.root_task.task_id in self.completed_tasks

    @computed_field
    @property
    def needs_replanning(self) -> bool:
        """Check if replanning is needed."""
        if not self.strategy.allow_dynamic_replanning:
            return False

        # Triggers for replanning
        failure_rate = len(self.failed_tasks) / max(len(self.all_tasks), 1)

        return (
            failure_rate > 0.3  # High failure rate
            or len(self.failed_tasks) > 5  # Many failures
            or any(
                task_id in self.failed_tasks for task_id in self.critical_path
            )  # Critical path failure
        )

    @computed_field
    @property
    def critical_path(self) -> List[str]:
        """Get current critical path."""
        # Simplified - in practice, recalculate based on current state
        if self.root_task:
            return [self.root_task.task_id]
        return []

    def add_task(self, task: TaskNode, parent_id: Optional[str] = None) -> None:
        """Add a task to the tree."""
        task.parent_id = parent_id
        self.all_tasks[task.task_id] = task

        if parent_id and parent_id in self.all_tasks:
            parent = self.all_tasks[parent_id]
            if task.task_id not in parent.children:
                parent.children.append(task.task_id)

        if not self.root_task and not parent_id:
            self.root_task = task

    def update_task_status(
        self, task_id: str, status: TaskStatus, result: Optional[Dict[str, Any]] = None
    ) -> None:
        """Update task status and handle state transitions."""
        if task_id not in self.all_tasks:
            return

        task = self.all_tasks[task_id]
        old_status = task.status
        task.status = status

        if result:
            task.result = result

        # Update tracking sets
        if status == TaskStatus.COMPLETED:
            self.completed_tasks.add(task_id)
            self.active_tasks.discard(task_id)
            self.failed_tasks.discard(task_id)
        elif status == TaskStatus.FAILED:
            self.failed_tasks.add(task_id)
            self.active_tasks.discard(task_id)
        elif status == TaskStatus.IN_PROGRESS:
            self.active_tasks.add(task_id)
        elif status == TaskStatus.CANCELLED:
            self.active_tasks.discard(task_id)


# ============================================================================
# Execution Plan Model
# ============================================================================


class ExecutionPlan(BaseModel):
    """Execution plan for a set of tasks."""

    plan_id: str = Field(default_factory=lambda: f"plan_{uuid4().hex[:8]}")

    tasks_to_execute: List[TaskNode] = Field(
        min_length=1, description="Tasks to execute in this batch"
    )

    execution_strategy: Literal["parallel", "sequential", "mixed"] = Field(
        default="mixed", description="How to execute these tasks"
    )

    parallel_groups: List[List[str]] = Field(
        default_factory=list, description="Groups of task IDs that can run in parallel"
    )

    estimated_duration: int = Field(
        ge=0, description="Estimated total duration in seconds"
    )

    resource_requirements: Dict[str, float] = Field(
        default_factory=dict, description="Total resource requirements"
    )

    @model_validator(mode="after")
    def calculate_resource_requirements(self) -> "ExecutionPlan":
        """Calculate total resource requirements."""
        if not self.resource_requirements:
            requirements: Dict[str, float] = {}

            for task in self.tasks_to_execute:
                for resource in task.required_resources:
                    key = resource.resource_key
                    requirements[key] = requirements.get(key, 0) + resource.quantity

            self.resource_requirements = requirements

        return self

    @computed_field
    @property
    def can_parallelize(self) -> bool:
        """Check if any parallelization is possible."""
        return len(self.parallel_groups) > 1 or any(
            len(g) > 1 for g in self.parallel_groups
        )


# ============================================================================
# Replanning Model
# ============================================================================


class ReplanningAnalysis(BaseModel):
    """Analysis for replanning decision."""

    trigger_reason: str = Field(description="Reason for considering replanning")

    failure_analysis: Dict[str, str] = Field(
        default_factory=dict, description="Analysis of failed tasks"
    )

    should_replan: bool = Field(description="Whether replanning is recommended")

    replanning_strategy: Literal[
        "full_replan", "partial_replan", "retry_failed", "adjust_strategy"
    ] = Field(default="partial_replan")

    tasks_to_modify: List[str] = Field(
        default_factory=list, description="Task IDs that need modification"
    )

    new_constraints: List[str] = Field(
        default_factory=list, description="New constraints learned from failures"
    )

    adjusted_estimates: Dict[str, int] = Field(
        default_factory=dict, description="Adjusted duration estimates for tasks"
    )
