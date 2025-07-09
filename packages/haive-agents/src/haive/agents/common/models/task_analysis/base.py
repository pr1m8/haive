"""Base classes and enums for task complexity analysis.

This module defines the fundamental building blocks for task complexity analysis
including task representations, dependency types, and complexity classifications.
"""

from enum import Enum
from typing import Any, Union

from haive.core.common.structures.tree import AutoTree
from pydantic import BaseModel, ConfigDict, Field


class TaskType(str, Enum):
    """Types of tasks based on their fundamental nature.

    Attributes:
        FACTUAL: Tasks requiring factual information lookup
        COMPUTATIONAL: Tasks involving calculations or data processing
        RESEARCH: Tasks requiring investigation and analysis
        CREATIVE: Tasks involving creative or generative work
        DECISION: Tasks requiring decision-making or judgment
        COORDINATION: Tasks involving coordination between multiple entities
        COMMUNICATION: Tasks involving information exchange
        VERIFICATION: Tasks involving validation or checking
        SYNTHESIS: Tasks combining multiple inputs into new outputs
        ITERATIVE: Tasks that require multiple cycles or refinement
    """

    FACTUAL = "factual"
    COMPUTATIONAL = "computational"
    RESEARCH = "research"
    CREATIVE = "creative"
    DECISION = "decision"
    COORDINATION = "coordination"
    COMMUNICATION = "communication"
    VERIFICATION = "verification"
    SYNTHESIS = "synthesis"
    ITERATIVE = "iterative"


class DependencyType(str, Enum):
    """Types of dependency relationships between tasks.

    Attributes:
        SEQUENTIAL: Task B cannot start until Task A completes (A → B)
        PARALLEL: Tasks can execute simultaneously (A || B)
        CONDITIONAL: Task B only executes if Task A meets conditions (A ?→ B)
        ITERATIVE: Task B feeds back to Task A (A ↔ B)
        JOIN: Multiple tasks must complete before next task (A,B → C)
        SPLIT: One task creates multiple parallel branches (A → B,C)
        OPTIONAL: Task is optional based on conditions
        ALTERNATIVE: Either Task A or Task B, but not both (A ⊕ B)
    """

    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    CONDITIONAL = "conditional"
    ITERATIVE = "iterative"
    JOIN = "join"
    SPLIT = "split"
    OPTIONAL = "optional"
    ALTERNATIVE = "alternative"


class ComplexityLevel(str, Enum):
    """Overall complexity classification for tasks.

    Attributes:
        TRIVIAL: Simple, single-step tasks (1-2 minutes)
        SIMPLE: Straightforward tasks with few steps (5-15 minutes)
        MODERATE: Multi-step tasks with some dependencies (30 minutes - 2 hours)
        COMPLEX: Involved tasks with multiple branches (2-8 hours)
        COMPLICATED: Sophisticated tasks requiring expertise (1-3 days)
        EXPERT: High-expertise tasks with uncertainty (weeks)
        RESEARCH: Unknown solution path, investigation required (months)
        UNSOLVABLE: Currently impossible or undefined problems
    """

    TRIVIAL = "trivial"
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    COMPLICATED = "complicated"
    EXPERT = "expert"
    RESEARCH = "research"
    UNSOLVABLE = "unsolvable"


class ComputationalComplexity(str, Enum):
    """Computational complexity classifications.

    Attributes:
        CONSTANT: O(1) - Fixed time regardless of input size
        LOGARITHMIC: O(log n) - Scales logarithmically with input
        LINEAR: O(n) - Scales linearly with input size
        LINEARITHMIC: O(n log n) - Common in efficient algorithms
        QUADRATIC: O(n²) - Scales quadratically
        POLYNOMIAL: O(n^k) - Polynomial time complexity
        EXPONENTIAL: O(2^n) - Exponential time complexity
        UNKNOWN: Complexity cannot be determined
    """

    CONSTANT = "constant"
    LOGARITHMIC = "logarithmic"
    LINEAR = "linear"
    LINEARITHMIC = "linearithmic"
    QUADRATIC = "quadratic"
    POLYNOMIAL = "polynomial"
    EXPONENTIAL = "exponential"
    UNKNOWN = "unknown"


class KnowledgeComplexity(str, Enum):
    """Knowledge complexity requirements.

    Attributes:
        BASIC: General knowledge or simple lookup
        INTERMEDIATE: Domain-specific knowledge required
        ADVANCED: Deep expertise in specific domain
        EXPERT: Cutting-edge expertise, research-level knowledge
        INTERDISCIPLINARY: Knowledge across multiple domains
        UNKNOWN: Knowledge requirements unclear
    """

    BASIC = "basic"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"
    INTERDISCIPLINARY = "interdisciplinary"
    UNKNOWN = "unknown"


class TimeComplexity(str, Enum):
    """Time complexity categories for task completion.

    Attributes:
        INSTANT: Less than 1 minute
        QUICK: 1-10 minutes
        SHORT: 10-60 minutes
        MEDIUM: 1-8 hours
        LONG: 1-7 days
        EXTENDED: 1-4 weeks
        PROJECT: 1-6 months
        RESEARCH: 6+ months or unknown timeline
    """

    INSTANT = "instant"
    QUICK = "quick"
    SHORT = "short"
    MEDIUM = "medium"
    LONG = "long"
    EXTENDED = "extended"
    PROJECT = "project"
    RESEARCH = "research"


class ResourceType(str, Enum):
    """Types of resources required for task execution.

    Attributes:
        HUMAN: Human expertise or labor
        COMPUTATIONAL: Computing resources
        DATA: Access to specific datasets or information
        TOOLS: Specialized tools or software
        FINANCIAL: Monetary resources
        TIME: Significant time investment
        NETWORK: Network access or connectivity
        STORAGE: Data storage capabilities
        EXPERTISE: Specialized domain expertise
        APPROVAL: Authorization or approval from authorities
    """

    HUMAN = "human"
    COMPUTATIONAL = "computational"
    DATA = "data"
    TOOLS = "tools"
    FINANCIAL = "financial"
    TIME = "time"
    NETWORK = "network"
    STORAGE = "storage"
    EXPERTISE = "expertise"
    APPROVAL = "approval"


class TaskStep(BaseModel):
    """Individual executable step within a task.

    Represents an atomic unit of work that cannot be further decomposed
    in the current analysis context.

    Attributes:
        name: Descriptive name for the step
        description: Detailed description of what the step involves
        task_type: The type of task this step represents
        estimated_duration_minutes: Estimated time to complete
        required_resources: Resources needed for this step
        difficulty_level: Subjective difficulty assessment
        can_be_automated: Whether this step can be automated
        requires_human_judgment: Whether human judgment is essential
        dependencies: IDs of other steps this depends on
        outputs: What this step produces

    Example:
        ```python
        step = TaskStep(
            name="Look up Wimbledon winner",
            description="Search for the most recent Wimbledon men's singles champion",
            task_type=TaskType.FACTUAL,
            estimated_duration_minutes=5,
            required_resources=[ResourceType.NETWORK, ResourceType.DATA],
            can_be_automated=True
        )
        ```
    """

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        use_enum_values=True,
    )

    name: str = Field(
        ...,
        description="Descriptive name for the step",
        min_length=1,
        max_length=200,
        examples=[
            "Look up Wimbledon winner",
            "Calculate age in days",
            "Find square root",
        ],
    )

    description: str = Field(
        ...,
        description="Detailed description of what the step involves",
        min_length=1,
        max_length=2000,
        examples=[
            "Search for the most recent Wimbledon men's singles champion",
            "Calculate the number of days between birth date and today",
            "Compute the square root of the calculated number of days",
        ],
    )

    task_type: TaskType = Field(
        ..., description="The type of task this step represents"
    )

    estimated_duration_minutes: float = Field(
        default=5.0,
        description="Estimated time to complete this step in minutes",
        gt=0,
        examples=[1.0, 5.0, 30.0, 120.0],
    )

    required_resources: list[ResourceType] = Field(
        default_factory=list,
        description="Resources needed to complete this step",
        max_length=10,
    )

    difficulty_level: int = Field(
        default=1,
        description="Subjective difficulty level (1=easy, 5=very hard)",
        ge=1,
        le=5,
    )

    can_be_automated: bool = Field(
        default=True, description="Whether this step can be fully automated"
    )

    requires_human_judgment: bool = Field(
        default=False, description="Whether human judgment is essential for this step"
    )

    dependencies: set[str] = Field(
        default_factory=set, description="IDs of other steps this step depends on"
    )

    outputs: list[str] = Field(
        default_factory=list,
        description="What this step produces or provides",
        examples=[
            ["winner_name", "tournament_year"],
            ["age_in_days"],
            ["square_root_result"],
        ],
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata about this step"
    )

    def get_duration_hours(self) -> float:
        """Get estimated duration in hours.

        Returns:
            Duration in hours
        """
        return self.estimated_duration_minutes / 60.0

    def is_blocking(self) -> bool:
        """Check if this step blocks other steps.

        Returns:
            True if other steps depend on this one
        """
        return bool(self.dependencies)

    def get_complexity_score(self) -> float:
        """Calculate a complexity score for this step.

        Combines duration, difficulty, and resource requirements.

        Returns:
            Complexity score (0.0 to 10.0)
        """
        base_score = self.difficulty_level

        # Add time factor
        if self.estimated_duration_minutes > 60:
            base_score += 1
        if self.estimated_duration_minutes > 240:
            base_score += 1

        # Add resource complexity
        resource_bonus = len(self.required_resources) * 0.2

        # Add human judgment factor
        if self.requires_human_judgment:
            base_score += 1

        # Add automation penalty (non-automated is more complex)
        if not self.can_be_automated:
            base_score += 0.5

        return min(10.0, base_score + resource_bonus)


class DependencyNode(BaseModel):
    """Represents a dependency relationship between tasks or steps.

    Attributes:
        source_id: ID of the source task/step
        target_id: ID of the target task/step
        dependency_type: Type of dependency relationship
        condition: Optional condition for conditional dependencies
        weight: Strength/importance of the dependency (0.0 to 1.0)
        description: Human-readable description of the dependency

    Example:
        ```python
        dependency = DependencyNode(
            source_id="lookup_winner",
            target_id="lookup_birthday",
            dependency_type=DependencyType.SEQUENTIAL,
            weight=1.0,
            description="Must know winner before looking up their birthday"
        )
        ```
    """

    source_id: str = Field(
        ...,
        description="ID of the source task/step",
        examples=["lookup_winner", "calculate_age", "step_1"],
    )

    target_id: str = Field(
        ...,
        description="ID of the target task/step",
        examples=["lookup_birthday", "find_square_root", "step_2"],
    )

    dependency_type: DependencyType = Field(
        ..., description="Type of dependency relationship"
    )

    condition: str | None = Field(
        default=None,
        description="Optional condition for conditional dependencies",
        examples=[
            "if winner_found",
            "if calculation_successful",
            "if approval_granted",
        ],
    )

    weight: float = Field(
        default=1.0,
        description="Strength/importance of the dependency (0.0 to 1.0)",
        ge=0.0,
        le=1.0,
    )

    description: str = Field(
        default="",
        description="Human-readable description of the dependency",
        max_length=500,
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata about this dependency"
    )

    def is_blocking(self) -> bool:
        """Check if this dependency creates a blocking relationship.

        Returns:
            True if the target cannot proceed without the source
        """
        return self.dependency_type in {
            DependencyType.SEQUENTIAL,
            DependencyType.JOIN,
            DependencyType.CONDITIONAL,
        }

    def allows_parallelization(self) -> bool:
        """Check if this dependency allows parallel execution.

        Returns:
            True if source and target can run in parallel
        """
        return self.dependency_type == DependencyType.PARALLEL

    def creates_join_point(self) -> bool:
        """Check if this dependency creates a join point.

        Returns:
            True if this is a join dependency
        """
        return self.dependency_type == DependencyType.JOIN


class Task(BaseModel):
    """Represents a complex task that can contain subtasks and steps.

    This is the main building block for task complexity analysis.
    Tasks can contain either other Tasks or TaskSteps, creating a
    hierarchical structure that AutoTree can automatically handle.

    Attributes:
        name: Descriptive name for the task
        description: Detailed description of the task
        task_type: Primary type of this task
        subtasks: List of subtasks and steps (Union type for AutoTree)
        dependencies: Dependency relationships
        estimated_duration_minutes: Total estimated duration
        complexity_level: Overall complexity assessment
        required_resources: Resources needed for the entire task
        success_criteria: How to measure successful completion

    Example:
        ```python
        # Create a complex task with mixed subtasks and steps
        main_task = Task(
            name="Analyze Wimbledon Champion Age",
            description="Find recent champion, calculate age, and analyze",
            task_type=TaskType.RESEARCH,
            subtasks=[
                TaskStep(
                    name="Find winner",
                    description="Look up most recent Wimbledon champion",
                    task_type=TaskType.FACTUAL
                ),
                Task(
                    name="Age Analysis",
                    description="Calculate and analyze age",
                    task_type=TaskType.COMPUTATIONAL,
                    subtasks=[
                        TaskStep(name="Get birthday", ...),
                        TaskStep(name="Calculate age", ...),
                        TaskStep(name="Find square root", ...)
                    ]
                )
            ]
        )
        ```
    """

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        use_enum_values=True,
    )

    name: str = Field(
        ...,
        description="Descriptive name for the task",
        min_length=1,
        max_length=200,
        examples=[
            "Analyze Wimbledon Champion Age",
            "Database Migration Project",
            "Research Market Trends",
        ],
    )

    description: str = Field(
        ...,
        description="Detailed description of the task",
        min_length=1,
        max_length=5000,
    )

    task_type: TaskType = Field(..., description="Primary type of this task")

    # This is the key field that AutoTree will handle - Union of Task and TaskStep
    subtasks: list[Union["Task", TaskStep]] = Field(
        default_factory=list,
        description="List of subtasks and steps that make up this task",
        max_length=50,
    )

    dependencies: list[DependencyNode] = Field(
        default_factory=list,
        description="Dependency relationships between subtasks",
        max_length=100,
    )

    estimated_duration_minutes: float | None = Field(
        default=None,
        description="Total estimated duration in minutes (calculated if None)",
        gt=0,
    )

    complexity_level: ComplexityLevel | None = Field(
        default=None, description="Overall complexity assessment (calculated if None)"
    )

    required_resources: list[ResourceType] = Field(
        default_factory=list, description="Resources needed for the entire task"
    )

    success_criteria: list[str] = Field(
        default_factory=list,
        description="Criteria for measuring successful task completion",
        examples=[
            [
                "Champion identified correctly",
                "Age calculated accurately",
                "Analysis completed",
            ],
            [
                "Database migrated successfully",
                "No data loss",
                "Performance maintained",
            ],
        ],
    )

    priority: int = Field(
        default=3, description="Task priority (1=low, 5=critical)", ge=1, le=5
    )

    can_be_parallelized: bool = Field(
        default=True, description="Whether subtasks can potentially run in parallel"
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata about this task"
    )

    def get_all_steps(self) -> list[TaskStep]:
        """Get all TaskStep objects from the entire task hierarchy.

        Returns:
            Flattened list of all TaskStep objects
        """
        steps = []

        for subtask in self.subtasks:
            if isinstance(subtask, TaskStep):
                steps.append(subtask)
            elif isinstance(subtask, Task):
                steps.extend(subtask.get_all_steps())

        return steps

    def get_all_tasks(self) -> list["Task"]:
        """Get all Task objects from the hierarchy including self.

        Returns:
            List of all Task objects in the hierarchy
        """
        tasks = [self]

        for subtask in self.subtasks:
            if isinstance(subtask, Task):
                tasks.extend(subtask.get_all_tasks())

        return tasks

    def calculate_total_duration(self) -> float:
        """Calculate total estimated duration for all subtasks.

        Returns:
            Total duration in minutes
        """
        if self.estimated_duration_minutes is not None:
            return self.estimated_duration_minutes

        total = 0.0
        for subtask in self.subtasks:
            if isinstance(subtask, TaskStep):
                total += subtask.estimated_duration_minutes
            elif isinstance(subtask, Task):
                total += subtask.calculate_total_duration()

        return total

    def get_max_depth(self) -> int:
        """Calculate the maximum depth of the task hierarchy.

        Returns:
            Maximum depth (0 for leaf tasks)
        """
        if not self.subtasks:
            return 0

        max_depth = 0
        for subtask in self.subtasks:
            if isinstance(subtask, Task):
                depth = subtask.get_max_depth() + 1
                max_depth = max(max_depth, depth)

        return max_depth

    def get_breadth(self) -> int:
        """Get the breadth (number of direct subtasks) of this task.

        Returns:
            Number of direct subtasks
        """
        return len(self.subtasks)

    def has_parallel_opportunities(self) -> bool:
        """Check if this task has opportunities for parallelization.

        Returns:
            True if some subtasks can potentially run in parallel
        """
        if not self.can_be_parallelized:
            return False

        # Check if we have multiple subtasks with no blocking dependencies
        if len(self.subtasks) < 2:
            return False

        # Simple heuristic: if we have multiple subtasks and not all are sequential
        sequential_deps = [
            d
            for d in self.dependencies
            if d.dependency_type == DependencyType.SEQUENTIAL
        ]
        return len(sequential_deps) < len(self.subtasks) - 1

    def create_auto_tree(self) -> AutoTree:
        """Create an AutoTree representation of this task.

        Returns:
            AutoTree instance wrapping this task
        """
        return AutoTree(self)


# Model rebuilding for forward references
Task.model_rebuild()
