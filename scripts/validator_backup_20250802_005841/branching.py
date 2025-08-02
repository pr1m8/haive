"""Task branching and decomposition analysis.

This module analyzes how tasks can be broken down into subtasks, identifying
parallel execution opportunities, sequential dependencies, and optimal
decomposition strategies.
"""

from datetime import timedelta
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator


class BranchType(str, Enum):
    """Types of task branches and execution patterns.

    Attributes:
        SEQUENTIAL: Tasks that must be executed in order
        PARALLEL: Tasks that can be executed simultaneously
        CONDITIONAL: Tasks that depend on conditions or outcomes
        ITERATIVE: Tasks that repeat with feedback loops
        CONVERGENT: Multiple branches that merge into one
        DIVERGENT: One task that splits into multiple branches
        INDEPENDENT: Completely independent execution streams
        DEPENDENT: Branches with complex interdependencies
    """

    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    CONDITIONAL = "conditional"
    ITERATIVE = "iterative"
    CONVERGENT = "convergent"
    DIVERGENT = "divergent"
    INDEPENDENT = "independent"
    DEPENDENT = "dependent"


class TaskBranch(BaseModel):
    """Individual branch in task decomposition.

    Represents a single execution path or subtask within a larger task
    decomposition, including its dependencies, requirements, and characteristics.

    Attributes:
        branch_id: Unique identifier for this branch
        name: Human-readable name for the branch
        description: Detailed description of what this branch accomplishes
        branch_type: Type of execution pattern for this branch
        estimated_effort: Relative effort required (1-10 scale)
        estimated_duration: Expected time to complete
        prerequisites: Other branches that must complete first
        enables: Branches that this branch enables
        resources_needed: Specific resources required for this branch
        parallel_compatible: Whether this can run in parallel with others

    Example:
        .. code-block:: python

            # Finding Wimbledon winner's birthday - first branch
            winner_branch = TaskBranch(
            branch_id="find_winner",
            name="Find Recent Wimbledon Winner",
            description="Look up the most recent Wimbledon championship winner",
            branch_type=BranchType.SEQUENTIAL,
            estimated_effort=3,
            estimated_duration=timedelta(minutes=5),
            prerequisites=[],
            enables=["find_birthday"],
            resources_needed=["web_search", "sports_database"]
            )

            # Cancer research - complex branch
            research_branch = TaskBranch(
            branch_id="mechanism_research",
            name="Research Cancer Mechanisms",
            description="Deep investigation into cellular mechanisms of cancer development",
            branch_type=BranchType.ITERATIVE,
            estimated_effort=10,
            estimated_duration=timedelta(weeks=52),
            prerequisites=["literature_review", "lab_setup"],
            resources_needed=["research_lab", "expert_oncologists", "funding"]
            )

    """

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        use_enum_values=True,
        str_strip_whitespace=True,
    )

    branch_id: str = Field(
        ...,
        description="Unique identifier for this branch",
        min_length=1,
        max_length=100,
        examples=[
            "find_winner",
            "calculate_sum",
            "research_mechanism",
            "validate_results",
        ],
    )

    name: str = Field(
        ...,
        description="Human-readable name for the branch",
        min_length=1,
        max_length=200,
        examples=[
            "Find Recent Wimbledon Winner",
            "Calculate Mathematical Sum",
            "Research Cancer Mechanisms",
            "Validate Experimental Results",
        ],
    )

    description: str = Field(
        ...,
        description="Detailed description of what this branch accomplishes",
        min_length=10,
        max_length=1000,
        examples=[
            "Look up the most recent Wimbledon championship winner using sports databases",
            "Perform mathematical calculations on retrieved factual data",
            "Conduct comprehensive research into cellular mechanisms of cancer development",
        ],
    )

    branch_type: BranchType = Field(
        ...,
        description="Type of execution pattern for this branch",
        examples=["sequential", "parallel", "conditional", "iterative"],
    )

    estimated_effort: int = Field(
        ...,
        description="Relative effort required on 1-10 scale (1=trivial, 10=maximum)",
        ge=1,
        le=10,
        examples=[1, 3, 7, 10],
    )

    estimated_duration: timedelta = Field(
        ...,
        description="Expected time to complete this branch",
        examples=[
            timedelta(minutes=5),
            timedelta(hours=2),
            timedelta(days=30),
            timedelta(weeks=52),
        ],
    )

    prerequisites: list[str] = Field(
        default_factory=list,
        description="IDs of other branches that must complete first",
        examples=[
            [],
            ["find_winner"],
            ["literature_review", "lab_setup"],
            ["data_collection", "analysis_plan"],
        ],
    )

    enables: list[str] = Field(
        default_factory=list,
        description="IDs of branches that this branch enables",
        examples=[
            ["find_birthday"],
            ["calculate_result"],
            ["clinical_trials", "drug_development"],
            ["publication", "patent_filing"],
        ],
    )

    resources_needed: list[str] = Field(
        default_factory=list,
        description="Specific resources required for this branch",
        examples=[
            ["web_search", "sports_database"],
            ["calculator", "mathematical_knowledge"],
            ["research_lab", "expert_oncologists", "funding"],
            ["supercomputer", "quantum_hardware", "specialist_team"],
        ],
    )

    parallel_compatible: bool = Field(
        default=True,
        description="Whether this branch can run in parallel with others",
        examples=[True, False],
    )

    risk_level: int = Field(
        default=1,
        description="Risk level for this branch (1=low, 5=extreme)",
        ge=1,
        le=5,
        examples=[1, 2, 3, 4, 5],
    )

    success_probability: float = Field(
        default=0.9,
        description="Estimated probability of successful completion",
        ge=0.0,
        le=1.0,
        examples=[0.95, 0.8, 0.3, 0.1],
    )

    def get_effort_category(self) -> str:
        """Get effort category classification.

        Returns:
            String describing effort category
        """
        if self.estimated_effort <= 2:
            return "trivial"
        if self.estimated_effort <= 4:
            return "low"
        if self.estimated_effort <= 6:
            return "moderate"
        if self.estimated_effort <= 8:
            return "high"
        return "extreme"

    def get_duration_category(self) -> str:
        """Get duration category classification.

        Returns:
            String describing duration category
        """
        total_seconds = self.estimated_duration.total_seconds()

        if total_seconds <= 3600:  # 1 hour
            return "immediate"
        if total_seconds <= 86400:  # 1 day
            return "same_day"
        if total_seconds <= 604800:  # 1 week
            return "short_term"
        if total_seconds <= 2592000:  # 30 days
            return "medium_term"
        if total_seconds <= 31536000:  # 1 year
            return "long_term"
        return "extended"

    def has_dependencies(self) -> bool:
        """Check if this branch has prerequisite dependencies.

        Returns:
            True if branch has prerequisites
        """
        return len(self.prerequisites) > 0

    def is_enabling(self) -> bool:
        """Check if this branch enables other branches.

        Returns:
            True if branch enables others
        """
        return len(self.enables) > 0

    def is_high_risk(self) -> bool:
        """Check if this is a high-risk branch.

        Returns:
            True if risk level is 4 or 5
        """
        return self.risk_level >= 4

    def is_likely_to_succeed(self, threshold: float = 0.7) -> bool:
        """Check if branch is likely to succeed.

        Args:
            threshold: Minimum probability for "likely"

        Returns:
            True if success probability exceeds threshold
        """
        return self.success_probability >= threshold


class TaskDecomposition(BaseModel):
    """Complete task breakdown into subtasks and execution branches.

    Analyzes how a complex task can be decomposed into manageable subtasks,
    identifying execution patterns, dependencies, and optimization opportunities.

    Attributes:
        task_description: Original task being decomposed
        branches: List of individual execution branches
        execution_pattern: Overall execution pattern
        critical_path: Sequence of branches on the critical path
        parallelization_opportunities: Groups of branches that can run in parallel
        bottlenecks: Branches that are likely to be bottlenecks
        total_estimated_effort: Sum of all branch efforts
        estimated_duration_sequential: Duration if executed sequentially
        estimated_duration_optimal: Duration with optimal parallelization

    Example:
        .. code-block:: python

            # Simple factual lookup task
            decomposition = TaskDecomposition.decompose_task(
            task_description="Find the birthday of the most recent Wimbledon winner",
            complexity_hint="simple_research"
            )

            # Complex research task
            decomposition = TaskDecomposition.decompose_task(
            task_description="Develop a cure for cancer",
            complexity_hint="breakthrough_research"
            )

            print(f"Branches: {len(decomposition.branches)}")
            print(f"Critical path: {decomposition.critical_path}")
            print(f"Parallelizable: {decomposition.parallelization_opportunities}")

    """

    task_description: str = Field(
        ...,
        description="Original task being decomposed",
        min_length=10,
        max_length=1000,
        examples=[
            "Find the birthday of the most recent Wimbledon winner",
            "Calculate Tom Clancy's birthday + sun's age + feet in mile, then square result",
            "Develop a cure for cancer through novel therapeutic approaches",
        ],
    )

    branches: list[TaskBranch] = Field(
        ...,
        description="List of individual execution branches",
        min_length=1,
        max_length=50,
    )

    execution_pattern: str = Field(
        ...,
        description="Overall execution pattern",
        examples=[
            "linear_sequential",
            "parallel_convergent",
            "complex_dependent",
            "iterative_research",
            "branching_exploration",
            "pipeline_flow",
        ],
    )

    critical_path: list[str] = Field(
        ...,
        description="Sequence of branch IDs on the critical path",
        examples=[
            ["find_winner", "find_birthday"],
            ["research_mechanism", "develop_therapy", "clinical_trials"],
            ["gather_facts", "calculate", "square_result"],
        ],
    )

    parallelization_opportunities: list[list[str]] = Field(
        default_factory=list,
        description="Groups of branch IDs that can run in parallel",
        examples=[
            [["find_clancy_birthday", "find_sun_age", "find_mile_feet"]],
            [
                ["mechanism_research", "drug_screening"],
                ["toxicity_testing", "efficacy_testing"],
            ],
            [["data_source_1", "data_source_2", "data_source_3"]],
        ],
    )

    bottlenecks: list[str] = Field(
        default_factory=list,
        description="Branch IDs that are likely to be bottlenecks",
        examples=[
            ["expert_review"],
            ["regulatory_approval", "funding_acquisition"],
            ["specialized_equipment_access"],
        ],
    )

    total_estimated_effort: int = Field(
        ...,
        description="Sum of all branch effort estimates",
        ge=1,
        examples=[5, 25, 150, 500],
    )

    estimated_duration_sequential: timedelta = Field(
        ...,
        description="Total duration if executed sequentially",
        examples=[
            timedelta(minutes=15),
            timedelta(hours=8),
            timedelta(weeks=104),
            timedelta(weeks=520),
        ],
    )

    estimated_duration_optimal: timedelta = Field(
        ...,
        description="Duration with optimal parallelization",
        examples=[
            timedelta(minutes=10),
            timedelta(hours=4),
            timedelta(weeks=52),
            timedelta(weeks=260),
        ],
    )

    @model_validator(mode="after")
    @classmethod
    def validate_decomposition_consistency(cls) -> "TaskDecomposition":
        """Validate that decomposition is internally consistent.

        Returns:
            Self if validation passes

        Raises:
            ValueError: If decomposition has inconsistencies
        """
        # Check that all critical path branches exist
        branch_ids = {branch.branch_id for branch in self.branches}
        for branch_id in self.critical_path:
            if branch_id not in branch_ids:
                raise ValueError(
                    f"Critical path branch '{branch_id}' not found in branches"
                )

        # Check that all parallelization branches exist
        for parallel_group in self.parallelization_opportunities:
            for branch_id in parallel_group:
                if branch_id not in branch_ids:
                    raise ValueError(
                        f"Parallelizable branch '{branch_id}' not found in branches"
                    )

        # Check that bottleneck branches exist
        for branch_id in self.bottlenecks:
            if branch_id not in branch_ids:
                raise ValueError(
                    f"Bottleneck branch '{branch_id}' not found in branches"
                )

        # Validate effort calculation
        calculated_effort = sum(branch.estimated_effort for branch in self.branches)
        if abs(calculated_effort - self.total_estimated_effort) > 1:
            raise ValueError(
                f"Total effort {
                    self.total_estimated_effort} doesn't match sum of branches {calculated_effort}"
            )

        # Validate that optimal duration is not longer than sequential
        if self.estimated_duration_optimal > self.estimated_duration_sequential:
            raise ValueError(
                "Optimal duration cannot be longer than sequential duration"
            )

        return self

    def get_dependency_graph(self) -> dict[str, list[str]]:
        """Get dependency graph as adjacency list.

        Returns:
            Dictionary mapping branch IDs to their dependencies
        """
        return {branch.branch_id: branch.prerequisites for branch in self.branches}

    def get_enables_graph(self) -> dict[str, list[str]]:
        """Get enables graph as adjacency list.

        Returns:
            Dictionary mapping branch IDs to branches they enable
        """
        return {branch.branch_id: branch.enables for branch in self.branches}

    def find_independent_branches(self) -> list[str]:
        """Find branches with no dependencies.

        Returns:
            List of branch IDs that can start immediately
        """
        return [
            branch.branch_id
            for branch in self.branches
            if not branch.has_dependencies()
        ]

    def find_terminal_branches(self) -> list[str]:
        """Find branches that don't enable anything else.

        Returns:
            List of branch IDs that are endpoints
        """
        return [
            branch.branch_id for branch in self.branches if not branch.is_enabling()
        ]

    def calculate_parallelization_speedup(self) -> float:
        """Calculate potential speedup from parallelization.

        Returns:
            Speedup ratio (sequential_time / optimal_time)
        """
        sequential_seconds = self.estimated_duration_sequential.total_seconds()
        optimal_seconds = self.estimated_duration_optimal.total_seconds()

        if optimal_seconds == 0:
            return float("inf")

        return sequential_seconds / optimal_seconds

    def get_complexity_metrics(self) -> dict[str, Any]:
        """Get various complexity metrics for the decomposition.

        Returns:
            Dictionary of complexity metrics
        """
        return {
            "total_branches": len(self.branches),
            "total_effort": self.total_estimated_effort,
            "average_effort_per_branch": self.total_estimated_effort
            / len(self.branches),
            "critical_path_length": len(self.critical_path),
            "parallelizable_groups": len(self.parallelization_opportunities),
            "bottleneck_count": len(self.bottlenecks),
            "max_branch_effort": max(
                branch.estimated_effort for branch in self.branches
            ),
            "dependency_density": sum(
                len(branch.prerequisites) for branch in self.branches
            )
            / len(self.branches),
            "parallelization_speedup": self.calculate_parallelization_speedup(),
            "high_risk_branches": sum(
                1 for branch in self.branches if branch.is_high_risk()
            ),
            "low_success_probability": sum(
                1 for branch in self.branches if not branch.is_likely_to_succeed()
            ),
        }

    def get_execution_recommendations(self) -> list[str]:
        """Get recommendations for optimal execution.

        Returns:
            List of execution recommendations
        """
        recommendations = []
        metrics = self.get_complexity_metrics()

        # Parallelization recommendations
        if metrics["parallelization_speedup"] > 2.0:
            recommendations.append(
                "High parallelization potential - strongly recommend parallel execution"
            )
        elif metrics["parallelization_speedup"] > 1.5:
            recommendations.append("Moderate parallelization benefits available")

        # Bottleneck recommendations
        if metrics["bottleneck_count"] > 0:
            recommendations.append(
                f"Address {
                    metrics['bottleneck_count']} identified bottlenecks early"
            )

        # Risk recommendations
        if metrics["high_risk_branches"] > 0:
            recommendations.append(
                f"Plan mitigation for {
                    metrics['high_risk_branches']} high-risk branches"
            )

        # Success probability recommendations
        if metrics["low_success_probability"] > 0:
            recommendations.append(
                f"Consider alternatives for {
                    metrics['low_success_probability']} low-probability branches"
            )

        # Complexity recommendations
        if metrics["total_branches"] > 20:
            recommendations.append(
                "Consider hierarchical decomposition for large branch count"
            )

        if metrics["dependency_density"] > 3.0:
            recommendations.append(
                "Complex dependencies detected - careful sequencing required"
            )

        return recommendations

    @classmethod
    def create_simple_sequential(
        cls,
        task_description: str,
        branch_descriptions: list[str],
        effort_estimates: list[int] | None = None,
        duration_estimates: list[timedelta] | None = None,
    ) -> "TaskDecomposition":
        """Create a simple sequential task decomposition.

        Args:
            task_description: Description of the overall task
            branch_descriptions: List of branch descriptions
            effort_estimates: Optional effort estimates (defaults to 3 for all)
            duration_estimates: Optional duration estimates (defaults to 1 hour each)

        Returns:
            TaskDecomposition with sequential branches
        """
        num_branches = len(branch_descriptions)

        if effort_estimates is None:
            effort_estimates = [3] * num_branches

        if duration_estimates is None:
            duration_estimates = [timedelta(hours=1)] * num_branches

        branches = []
        for i, description in enumerate(branch_descriptions):
            branch_id = f"step_{i + 1}"
            prerequisites = [f"step_{i}"] if i > 0 else []
            enables = [f"step_{i + 2}"] if i < num_branches - 1 else []

            branch = TaskBranch(
                branch_id=branch_id,
                name=f"Step {i + 1}",
                description=description,
                branch_type=BranchType.SEQUENTIAL,
                estimated_effort=effort_estimates[i],
                estimated_duration=duration_estimates[i],
                prerequisites=prerequisites,
                enables=enables,
                parallel_compatible=False,
            )
            branches.append(branch)

        critical_path = [f"step_{i + 1}" for i in range(num_branches)]
        total_effort = sum(effort_estimates)
        sequential_duration = sum(duration_estimates, timedelta())

        return cls(
            task_description=task_description,
            branches=branches,
            execution_pattern="linear_sequential",
            critical_path=critical_path,
            parallelization_opportunities=[],
            bottlenecks=[],
            total_estimated_effort=total_effort,
            estimated_duration_sequential=sequential_duration,
            estimated_duration_optimal=sequential_duration,
        )
