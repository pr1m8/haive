# src/haive/agents/task_analysis/base/models.py

import uuid
from enum import Enum
from typing import Any, Union

from pydantic import BaseModel, Field

# ============================================================================
# ENUMS
# ============================================================================


class TaskType(str, Enum):
    """Type of task - affects how it's processed."""

    ACTION = "action"  # Direct executable action
    ANALYSIS = "analysis"  # Analytical task
    DECISION = "decision"  # Decision point
    RESEARCH = "research"  # Research/investigation
    CREATIVE = "creative"  # Creative/generative
    INTEGRATION = "integration"  # System integration
    COMPOSITE = "composite"  # Contains multiple subtasks


class ActionType(str, Enum):
    """Types of atomic actions."""

    COMPUTE = "compute"
    RETRIEVE = "retrieve"
    GENERATE = "generate"
    VALIDATE = "validate"
    TRANSFORM = "transform"
    AGGREGATE = "aggregate"
    STORE = "store"


class DependencyType(str, Enum):
    """Types of dependencies between tasks."""

    SEQUENTIAL = "sequential"  # Must complete before
    PARALLEL = "parallel"  # Can run simultaneously
    CONDITIONAL = "conditional"  # Depends on condition
    JOIN = "join"  # Multiple inputs join here


# ============================================================================
# CORE MODELS FOR AUTOTREE
# ============================================================================


class TaskDependency(BaseModel):
    """Dependency between tasks."""

    source_id: str = Field(..., description="Source task ID")
    target_id: str = Field(..., description="Target task ID")
    dependency_type: DependencyType = Field(default=DependencyType.SEQUENTIAL)
    condition: str | None = Field(
        default=None, description="Condition for conditional deps"
    )
    data_flow: dict[str, str] | None = Field(
        default=None, description="Data that flows between tasks"
    )


class ActionStep(BaseModel):
    """Atomic action that cannot be decomposed further.
    This is a leaf node in the task tree.
    """

    # Identity
    step_id: str = Field(default_factory=lambda: f"step_{uuid.uuid4().hex[:8]}")
    name: str = Field(..., description="Action name")
    description: str = Field(..., description="What this action does")

    # Type and execution
    action_type: ActionType = Field(..., description="Type of action")
    estimated_duration_minutes: float = Field(default=5.0, gt=0)

    # Requirements
    required_tools: list[str] = Field(default_factory=list)
    required_context: list[str] = Field(default_factory=list)

    # Input/Output specification
    inputs: dict[str, str] = Field(
        default_factory=dict, description="Expected inputs with types"
    )
    outputs: dict[str, str] = Field(
        default_factory=dict, description="Expected outputs with types"
    )

    # Validation
    success_criteria: list[str] = Field(default_factory=list)

    # State
    can_parallelize: bool = Field(default=True)
    is_critical: bool = Field(default=False)


class TaskNode(BaseModel):
    """A task that may contain subtasks or action steps.
    Designed to work perfectly with AutoTree.
    """

    # Identity
    task_id: str = Field(default_factory=lambda: f"task_{uuid.uuid4().hex[:8]}")
    name: str = Field(..., description="Task name")
    description: str = Field(..., description="Detailed description")

    # Type
    task_type: TaskType = Field(..., description="Type of task")

    # CRITICAL: Union type for AutoTree to detect and handle
    subtasks: list[Union["TaskNode", ActionStep]] = Field(
        default_factory=list,
        description="Child tasks or action steps - AutoTree will handle this!",
    )

    # Dependencies (between children)
    dependencies: list[TaskDependency] = Field(default_factory=list)

    # Estimates
    estimated_duration_minutes: float | None = Field(default=None)
    complexity_score: float = Field(default=1.0, ge=0, le=10)

    # Requirements
    required_resources: list[str] = Field(default_factory=list)
    required_capabilities: list[str] = Field(default_factory=list)

    # Execution hints
    can_parallelize: bool = Field(default=True)
    can_expand: bool = Field(default=True, description="Can be further decomposed")
    expansion_hints: str | None = Field(
        default=None, description="Hints for decomposition"
    )

    # Join information
    is_join_point: bool = Field(default=False)
    join_strategy: str | None = Field(default=None)

    def calculate_total_duration(self) -> float:
        """Calculate total duration including subtasks."""
        if self.estimated_duration_minutes is not None:
            return self.estimated_duration_minutes

        if not self.subtasks:
            return 5.0  # Default for leaf nodes

        # Sum durations (simplified - real impl would consider parallelism)
        total = 0.0
        for subtask in self.subtasks:
            if isinstance(subtask, ActionStep):
                total += subtask.estimated_duration_minutes
            elif isinstance(subtask, TaskNode):
                total += subtask.calculate_total_duration()

        return total

    def get_all_steps(self) -> list[ActionStep]:
        """Get all ActionSteps in this task tree."""
        steps = []
        for subtask in self.subtasks:
            if isinstance(subtask, ActionStep):
                steps.append(subtask)
            elif isinstance(subtask, TaskNode):
                steps.extend(subtask.get_all_steps())
        return steps

    def add_subtask(self, subtask: Union["TaskNode", ActionStep]) -> None:
        """Add a subtask and assign dependencies if needed."""
        self.subtasks.append(subtask)

    def add_dependency(
        self,
        source_id: str,
        target_id: str,
        dep_type: DependencyType = DependencyType.SEQUENTIAL,
    ) -> None:
        """Add a dependency between child tasks."""
        dep = TaskDependency(
            source_id=source_id, target_id=target_id, dependency_type=dep_type
        )
        self.dependencies.append(dep)


# ============================================================================
# ROOT TASK PLAN MODEL
# ============================================================================


class TaskPlan(BaseModel):
    """Root object representing a complete task plan.
    This is what we'll create from a task description.
    """

    # Identity
    plan_id: str = Field(default_factory=lambda: f"plan_{uuid.uuid4().hex[:8]}")
    name: str = Field(..., description="Plan name")
    original_request: str = Field(..., description="Original task description")

    # The root task - can be a tree of any depth
    root_task: TaskNode = Field(..., description="Root task node")

    # Metadata
    created_at: str = Field(default_factory=lambda: str(uuid.uuid4()))
    total_estimated_duration_minutes: float | None = None
    total_tasks: int | None = None
    max_depth: int | None = None

    # Analysis results (populated after analysis)
    complexity_analysis: dict[str, Any] | None = None
    parallelization_analysis: dict[str, Any] | None = None
    execution_plan: dict[str, Any] | None = None

    def calculate_stats(self) -> None:
        """Calculate plan statistics."""
        from haive.core.common.structures.tree import AutoTree

        tree = AutoTree(self.root_task)
        all_nodes = tree.traverse_depth_first(lambda n: n)

        self.total_tasks = len(all_nodes)
        self.total_estimated_duration_minutes = (
            self.root_task.calculate_total_duration()
        )
        self.max_depth = self._calculate_max_depth(tree)

    def _calculate_max_depth(self, tree) -> int:
        """Calculate maximum depth of the tree."""
        if not tree.children:
            return 0
        return 1 + max(self._calculate_max_depth(child) for child in tree.children)


# IMPORTANT: Rebuild model for forward references
TaskNode.model_rebuild()
