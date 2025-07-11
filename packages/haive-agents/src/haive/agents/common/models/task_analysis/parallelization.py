"""Parallelization analysis for task execution planning.

This module analyzes task dependencies to identify parallelization opportunities,
execution phases, join points, and optimal execution strategies.
"""

from enum import Enum
from typing import Any

from haive.core.common.structures.tree import AutoTree
from pydantic import BaseModel, ConfigDict, Field

from haive.agents.common.models.task_analysis.base import (
    DependencyNode,
    Task,
    TaskStep,
)


class ExecutionStrategy(str, Enum):
    """Strategies for executing parallel tasks.

    Attributes:
        SEQUENTIAL: Execute all tasks one after another
        MAX_PARALLEL: Execute as many tasks in parallel as possible
        RESOURCE_CONSTRAINED: Parallel execution limited by resource availability
        PRIORITY_BASED: Execute high-priority tasks first, parallelize when possible
        BALANCED: Balance between parallelization and resource usage
    """

    SEQUENTIAL = "sequential"
    MAX_PARALLEL = "max_parallel"
    RESOURCE_CONSTRAINED = "resource_constrained"
    PRIORITY_BASED = "priority_based"
    BALANCED = "balanced"


class JoinPoint(BaseModel):
    """Represents a point where multiple parallel tasks must synchronize.

    Join points are critical for understanding where parallel execution
    must wait for all dependencies to complete before proceeding.

    Attributes:
        id: Unique identifier for this join point
        name: Descriptive name for the join point
        input_task_ids: IDs of tasks that must complete before this join
        output_task_ids: IDs of tasks that can start after this join
        join_type: Type of join operation
        estimated_wait_time: Expected time to wait for all inputs
        is_critical_path: Whether this join point is on the critical path

    Example:
        ```python
        join_point = JoinPoint(
            id="analysis_join",
            name="Combine Analysis Results",
            input_task_ids=["data_collection", "background_research"],
            output_task_ids=["final_report"],
            join_type="synchronous"
        )
        ```
    """

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
    )

    id: str = Field(
        ...,
        description="Unique identifier for this join point",
        examples=["join_1", "analysis_join", "data_merge_point"],
    )

    name: str = Field(
        ...,
        description="Descriptive name for the join point",
        examples=[
            "Combine Analysis Results",
            "Merge Data Sources",
            "Synchronize Processing",
        ],
    )

    input_task_ids: list[str] = Field(
        ...,
        description="IDs of tasks that must complete before this join",
        min_length=2,
        examples=[["task_1", "task_2"], ["data_collection", "background_research"]],
    )

    output_task_ids: list[str] = Field(
        default_factory=list,
        description="IDs of tasks that can start after this join",
        examples=[["task_3"], ["final_report", "presentation"]],
    )

    join_type: str = Field(
        default="synchronous",
        description="Type of join operation",
        examples=["synchronous", "asynchronous", "conditional", "partial"],
    )

    estimated_wait_time_minutes: float = Field(
        default=0.0,
        description="Expected time to wait for all inputs to complete",
        ge=0.0,
    )

    is_critical_path: bool = Field(
        default=False, description="Whether this join point is on the critical path"
    )

    bottleneck_probability: float = Field(
        default=0.0,
        description="Probability this join point will be a bottleneck (0.0 to 1.0)",
        ge=0.0,
        le=1.0,
    )

    def get_input_count(self) -> int:
        """Get the number of input tasks for this join point.

        Returns:
            Number of input tasks
        """
        return len(self.input_task_ids)

    def get_output_count(self) -> int:
        """Get the number of output tasks from this join point.

        Returns:
            Number of output tasks
        """
        return len(self.output_task_ids)

    def is_merge_point(self) -> bool:
        """Check if this is a merge point (multiple inputs, single output).

        Returns:
            True if multiple inputs merge to single output
        """
        return len(self.input_task_ids) > 1 and len(self.output_task_ids) == 1

    def is_split_point(self) -> bool:
        """Check if this is a split point (single input, multiple outputs).

        Returns:
            True if single input splits to multiple outputs
        """
        return len(self.input_task_ids) == 1 and len(self.output_task_ids) > 1


class ParallelGroup(BaseModel):
    """Represents a group of tasks that can execute in parallel.

    Parallel groups identify sets of tasks that have no blocking
    dependencies between them and can therefore run simultaneously.

    Attributes:
        group_id: Unique identifier for this parallel group
        task_ids: IDs of tasks in this parallel group
        estimated_duration_minutes: Time for the longest task in the group
        resource_requirements: Combined resource requirements
        can_be_interleaved: Whether tasks can be interleaved or must run fully parallel
        priority: Priority level for this group
        phase: Execution phase this group belongs to

    Example:
        ```python
        parallel_group = ParallelGroup(
            group_id="research_phase",
            task_ids=["web_research", "library_research", "expert_interviews"],
            estimated_duration_minutes=120,
            resource_requirements={"researchers": 3, "internet": True}
        )
        ```
    """

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
    )

    group_id: str = Field(
        ...,
        description="Unique identifier for this parallel group",
        examples=["group_1", "research_phase", "data_collection"],
    )

    task_ids: list[str] = Field(
        ...,
        description="IDs of tasks in this parallel group",
        min_length=1,
        examples=[["task_1", "task_2"], ["web_research", "library_research"]],
    )

    estimated_duration_minutes: float = Field(
        ..., description="Time for the longest task in the group", gt=0.0
    )

    resource_requirements: dict[str, Any] = Field(
        default_factory=dict,
        description="Combined resource requirements for the group",
        examples=[
            {"cpu_cores": 4, "memory_gb": 8},
            {"researchers": 2, "internet": True, "database_access": True},
        ],
    )

    can_be_interleaved: bool = Field(
        default=True,
        description="Whether tasks can be interleaved or must run fully parallel",
    )

    priority: int = Field(
        default=3,
        description="Priority level for this group (1=low, 5=critical)",
        ge=1,
        le=5,
    )

    phase: int = Field(
        default=1, description="Execution phase this group belongs to", ge=1
    )

    parallelization_efficiency: float = Field(
        default=1.0,
        description="Efficiency of parallel execution (1.0 = perfect, 0.0 = no benefit)",
        ge=0.0,
        le=1.0,
    )

    def get_task_count(self) -> int:
        """Get the number of tasks in this parallel group.

        Returns:
            Number of tasks in the group
        """
        return len(self.task_ids)

    def get_theoretical_speedup(self) -> float:
        """Calculate theoretical speedup from parallelization.

        Returns:
            Theoretical speedup factor
        """
        if self.get_task_count() <= 1:
            return 1.0

        return min(
            self.get_task_count(),
            self.parallelization_efficiency * self.get_task_count(),
        )

    def calculate_actual_duration(self, sequential_duration: float) -> float:
        """Calculate actual duration considering parallelization.

        Args:
            sequential_duration: Duration if tasks ran sequentially

        Returns:
            Actual duration with parallelization
        """
        speedup = self.get_theoretical_speedup()
        return max(self.estimated_duration_minutes, sequential_duration / speedup)


class ExecutionPhase(BaseModel):
    """Represents a phase in the overall task execution plan.

    Execution phases organize the task execution into sequential stages,
    where each phase must complete before the next phase can begin.

    Attributes:
        phase_number: Sequential phase number
        name: Descriptive name for this phase
        parallel_groups: Groups of tasks that can run in parallel within this phase
        dependencies: What this phase depends on
        estimated_duration_minutes: Total time for this phase
        critical_path_tasks: Tasks on the critical path within this phase

    Example:
        ```python
        phase = ExecutionPhase(
            phase_number=1,
            name="Data Collection Phase",
            parallel_groups=[research_group, survey_group],
            estimated_duration_minutes=180
        )
        ```
    """

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
    )

    phase_number: int = Field(..., description="Sequential phase number", ge=1)

    name: str = Field(
        ...,
        description="Descriptive name for this phase",
        examples=["Data Collection Phase", "Analysis Phase", "Reporting Phase"],
    )

    parallel_groups: list[ParallelGroup] = Field(
        default_factory=list,
        description="Groups of tasks that can run in parallel within this phase",
    )

    dependencies: list[str] = Field(
        default_factory=list,
        description="Phase dependencies (other phases that must complete first)",
    )

    estimated_duration_minutes: float = Field(
        ..., description="Total time for this phase", gt=0.0
    )

    critical_path_tasks: list[str] = Field(
        default_factory=list, description="Tasks on the critical path within this phase"
    )

    resource_utilization: dict[str, float] = Field(
        default_factory=dict,
        description="Expected resource utilization during this phase",
        examples=[{"cpu": 0.8, "memory": 0.6, "network": 0.4}],
    )

    can_start_early: bool = Field(
        default=False,
        description="Whether this phase can start before all dependencies complete",
    )

    def get_total_task_count(self) -> int:
        """Get total number of tasks across all parallel groups.

        Returns:
            Total task count
        """
        return sum(group.get_task_count() for group in self.parallel_groups)

    def get_max_parallelism(self) -> int:
        """Get maximum number of tasks that can run simultaneously.

        Returns:
            Maximum parallelism level
        """
        if not self.parallel_groups:
            return 0

        return max(group.get_task_count() for group in self.parallel_groups)

    def calculate_sequential_duration(self) -> float:
        """Calculate duration if all tasks ran sequentially.

        Returns:
            Sequential execution duration in minutes
        """
        total = 0.0
        for group in self.parallel_groups:
            total += group.estimated_duration_minutes * group.get_task_count()
        return total

    def get_parallelization_benefit(self) -> float:
        """Calculate benefit from parallelization as a ratio.

        Returns:
            Parallelization benefit (sequential_time / parallel_time)
        """
        sequential = self.calculate_sequential_duration()
        if sequential == 0 or self.estimated_duration_minutes == 0:
            return 1.0

        return sequential / self.estimated_duration_minutes


class ParallelizationAnalysis(BaseModel):
    """Complete analysis of parallelization opportunities for a task.

    This is the main result of parallelization analysis, containing
    all the information needed to optimize task execution.

    Attributes:
        execution_phases: Sequential phases of execution
        parallel_groups: All identified parallel groups
        join_points: Critical synchronization points
        critical_path: Tasks on the critical path
        execution_strategy: Recommended execution strategy
        estimated_speedup: Expected speedup from parallelization
        resource_requirements: Peak resource requirements
        bottlenecks: Identified bottlenecks and constraints

    Example:
        ```python
        analysis = ParallelizationAnalysis(
            execution_phases=[phase1, phase2, phase3],
            parallel_groups=[group1, group2],
            join_points=[join1, join2],
            critical_path=["task_1", "task_3", "task_5"],
            estimated_speedup=2.5
        )
        ```
    """

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
    )

    execution_phases: list[ExecutionPhase] = Field(
        default_factory=list, description="Sequential phases of execution"
    )

    parallel_groups: list[ParallelGroup] = Field(
        default_factory=list, description="All identified parallel groups"
    )

    join_points: list[JoinPoint] = Field(
        default_factory=list, description="Critical synchronization points"
    )

    critical_path: list[str] = Field(
        default_factory=list, description="Task IDs on the critical path"
    )

    execution_strategy: ExecutionStrategy = Field(
        default=ExecutionStrategy.BALANCED, description="Recommended execution strategy"
    )

    estimated_speedup: float = Field(
        default=1.0, description="Expected speedup from parallelization", ge=1.0
    )

    sequential_duration_minutes: float = Field(
        default=0.0, description="Total duration if executed sequentially", ge=0.0
    )

    parallel_duration_minutes: float = Field(
        default=0.0, description="Total duration with optimal parallelization", ge=0.0
    )

    resource_requirements: dict[str, Any] = Field(
        default_factory=dict,
        description="Peak resource requirements for parallel execution",
    )

    bottlenecks: list[str] = Field(
        default_factory=list,
        description="Identified bottlenecks and constraints",
        examples=[
            ["Limited CPU cores", "Memory constraints", "Network bandwidth"],
            ["Single-threaded database", "File system locks", "API rate limits"],
        ],
    )

    parallelization_efficiency: float = Field(
        default=1.0,
        description="Overall efficiency of parallelization (0.0 to 1.0)",
        ge=0.0,
        le=1.0,
    )

    coordination_overhead_minutes: float = Field(
        default=0.0,
        description="Estimated overhead for coordinating parallel execution",
        ge=0.0,
    )

    def get_total_phases(self) -> int:
        """Get total number of execution phases.

        Returns:
            Number of phases
        """
        return len(self.execution_phases)

    def get_max_parallelism(self) -> int:
        """Get maximum parallelism across all phases.

        Returns:
            Maximum number of tasks that can run simultaneously
        """
        if not self.execution_phases:
            return 0

        return max(phase.get_max_parallelism() for phase in self.execution_phases)

    def get_critical_path_duration(self) -> float:
        """Get duration of the critical path.

        Returns:
            Critical path duration in minutes
        """
        return self.parallel_duration_minutes

    def calculate_time_savings(self) -> float:
        """Calculate time savings from parallelization.

        Returns:
            Time savings in minutes
        """
        return max(
            0.0, self.sequential_duration_minutes - self.parallel_duration_minutes
        )

    def get_efficiency_percentage(self) -> float:
        """Get parallelization efficiency as a percentage.

        Returns:
            Efficiency percentage (0-100)
        """
        return self.parallelization_efficiency * 100

    def is_worth_parallelizing(self, min_speedup: float = 1.2) -> bool:
        """Determine if parallelization is worthwhile.

        Args:
            min_speedup: Minimum speedup required to justify parallelization

        Returns:
            True if parallelization provides sufficient benefit
        """
        return self.estimated_speedup >= min_speedup


class ParallelizationAnalyzer(BaseModel):
    """Analyzer for identifying parallelization opportunities in tasks.

    This class performs sophisticated analysis of task dependencies to identify
    optimal parallelization strategies, execution phases, and resource requirements.

    Attributes:
        max_parallel_tasks: Maximum number of tasks to run in parallel
        resource_constraints: Resource limitations that affect parallelization
        prefer_balanced_groups: Whether to prefer balanced parallel groups
        include_coordination_overhead: Whether to include coordination overhead

    Example:
        ```python
        analyzer = ParallelizationAnalyzer(
            max_parallel_tasks=8,
            resource_constraints={"cpu_cores": 4, "memory_gb": 16}
        )

        analysis = analyzer.analyze_task(complex_task)
        print(f"Recommended speedup: {analysis.estimated_speedup:.1f}x")
        ```
    """

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
    )

    max_parallel_tasks: int = Field(
        default=10, description="Maximum number of tasks to run in parallel", gt=0
    )

    resource_constraints: dict[str, Any] = Field(
        default_factory=dict,
        description="Resource limitations that affect parallelization",
        examples=[
            {"cpu_cores": 4, "memory_gb": 16, "network_bandwidth_mbps": 100},
            {"workers": 5, "database_connections": 10, "api_calls_per_minute": 1000},
        ],
    )

    prefer_balanced_groups: bool = Field(
        default=True, description="Whether to prefer balanced parallel groups"
    )

    include_coordination_overhead: bool = Field(
        default=True,
        description="Whether to include coordination overhead in estimates",
    )

    coordination_overhead_per_task_minutes: float = Field(
        default=0.5, description="Coordination overhead per task in minutes", ge=0.0
    )

    def analyze_task(self, task: Task) -> ParallelizationAnalysis:
        """Analyze a task for parallelization opportunities.

        Args:
            task: Task to analyze

        Returns:
            Complete parallelization analysis
        """
        # Create AutoTree for dependency analysis
        tree = task.create_auto_tree()

        # Extract all tasks and steps
        all_tasks = self._extract_all_items(tree)
        dependencies = self._extract_dependencies(task)

        # Build dependency graph
        dependency_graph = self._build_dependency_graph(all_tasks, dependencies)

        # Find parallel groups
        parallel_groups = self._identify_parallel_groups(dependency_graph)

        # Find join points
        join_points = self._identify_join_points(dependency_graph)

        # Calculate critical path
        critical_path = self._calculate_critical_path(dependency_graph)

        # Create execution phases
        execution_phases = self._create_execution_phases(parallel_groups, dependencies)

        # Calculate durations and speedup
        sequential_duration = self._calculate_sequential_duration(all_tasks)
        parallel_duration = self._calculate_parallel_duration(execution_phases)
        estimated_speedup = sequential_duration / max(parallel_duration, 1.0)

        # Determine execution strategy
        execution_strategy = self._determine_execution_strategy(
            parallel_groups, resource_constraints=self.resource_constraints
        )

        # Calculate coordination overhead
        coordination_overhead = 0.0
        if self.include_coordination_overhead:
            coordination_overhead = (
                len(parallel_groups) * self.coordination_overhead_per_task_minutes
            )
            parallel_duration += coordination_overhead
            estimated_speedup = sequential_duration / max(parallel_duration, 1.0)

        # Identify bottlenecks
        bottlenecks = self._identify_bottlenecks(
            parallel_groups, self.resource_constraints
        )

        return ParallelizationAnalysis(
            execution_phases=execution_phases,
            parallel_groups=parallel_groups,
            join_points=join_points,
            critical_path=critical_path,
            execution_strategy=execution_strategy,
            estimated_speedup=estimated_speedup,
            sequential_duration_minutes=sequential_duration,
            parallel_duration_minutes=parallel_duration,
            resource_requirements=self._calculate_peak_resources(parallel_groups),
            bottlenecks=bottlenecks,
            parallelization_efficiency=(
                min(1.0, estimated_speedup / len(parallel_groups))
                if parallel_groups
                else 1.0
            ),
            coordination_overhead_minutes=coordination_overhead,
        )

    def _extract_all_items(self, tree: AutoTree) -> list[Task | TaskStep]:
        """Extract all tasks and steps from the tree."""
        items = [tree.content]

        for child in tree.children:
            items.extend(self._extract_all_items(child))

        return items

    def _extract_dependencies(self, task: Task) -> list[DependencyNode]:
        """Extract all dependencies from task hierarchy."""
        dependencies = list(task.dependencies)

        for subtask in task.subtasks:
            if isinstance(subtask, Task):
                dependencies.extend(self._extract_dependencies(subtask))

        return dependencies

    def _build_dependency_graph(
        self, items: list[Task | TaskStep], dependencies: list[DependencyNode]
    ) -> dict[str, dict[str, Any]]:
        """Build a dependency graph from items and dependencies."""
        graph = {}

        # Initialize nodes
        for item in items:
            item_id = getattr(item, "name", f"item_{id(item)}")
            graph[item_id] = {
                "item": item,
                "predecessors": [],
                "successors": [],
                "duration": getattr(item, "estimated_duration_minutes", 0.0)
                or getattr(item, "calculate_total_duration", lambda: 0.0)(),
            }

        # Add edges
        for dep in dependencies:
            if dep.source_id in graph and dep.target_id in graph:
                graph[dep.source_id]["successors"].append((dep.target_id, dep))
                graph[dep.target_id]["predecessors"].append((dep.source_id, dep))

        return graph

    def _identify_parallel_groups(
        self, dependency_graph: dict[str, dict[str, Any]]
    ) -> list[ParallelGroup]:
        """Identify groups of tasks that can run in parallel."""
        parallel_groups = []
        visited = set()
        group_id = 1

        # Find tasks with no predecessors or same predecessors
        for task_id, task_info in dependency_graph.items():
            if task_id in visited:
                continue

            # Find all tasks that can run in parallel with this one
            parallel_tasks = [task_id]

            # Simple heuristic: tasks with the same predecessors can often run in parallel
            predecessors = set(pred_id for pred_id, _ in task_info["predecessors"]}

            for other_id, other_info in dependency_graph.items():
                if other_id != task_id and other_id not in visited:
                    other_predecessors = set(
                        pred_id for pred_id, _ in other_info["predecessors"]
                    }

                    # Can run in parallel if they have the same predecessors
                    # and no blocking dependencies between them
                    if predecessors == other_predecessors:
                        if not self._has_blocking_dependency(
                            task_id, other_id, dependency_graph
                        ):
                            parallel_tasks.append(other_id)

            if (
                len(parallel_tasks) > 1 or len(parallel_tasks) == 1
            ):  # Include single tasks too
                # Calculate group duration (max of all tasks in group)
                group_duration = max(
                    dependency_graph[tid]["duration"] for tid in parallel_tasks
                )

                parallel_groups.append(
                    ParallelGroup(
                        group_id=f"group_{group_id}",
                        task_ids=parallel_tasks,
                        estimated_duration_minutes=group_duration,
                        phase=1,  # Will be updated later
                    )
                )

                visited.update(parallel_tasks)
                group_id += 1

        return parallel_groups

    def _has_blocking_dependency(
        self, task_a: str, task_b: str, dependency_graph: dict[str, dict[str, Any]]
    ) -> bool:
        """Check if there's a blocking dependency between two tasks."""
        # Check direct dependencies
        for succ_id, dep in dependency_graph[task_a]["successors"]:
            if succ_id == task_b and dep.is_blocking():
                return True

        for succ_id, dep in dependency_graph[task_b]["successors"]:
            if succ_id == task_a and dep.is_blocking():
                return True

        return False

    def _identify_join_points(
        self, dependency_graph: dict[str, dict[str, Any]]
    ) -> list[JoinPoint]:
        """Identify join points where multiple tasks synchronize."""
        join_points = []
        join_id = 1

        for task_id, task_info in dependency_graph.items():
            predecessors = task_info["predecessors"]

            # If a task has multiple predecessors, it's a potential join point
            if len(predecessors) > 1:
                input_tasks = [pred_id for pred_id, _ in predecessors]
                output_tasks = [succ_id for succ_id, _ in task_info["successors"]]

                join_points.append(
                    JoinPoint(
                        id=f"join_{join_id}",
                        name=f"Join before {task_id}",
                        input_task_ids=input_tasks,
                        output_task_ids=[task_id, *output_tasks],
                        bottleneck_probability=0.3 if len(input_tasks) > 2 else 0.1,
                    )
                )
                join_id += 1

        return join_points

    def _calculate_critical_path(
        self, dependency_graph: dict[str, dict[str, Any]]
    ) -> list[str]:
        """Calculate the critical path through the dependency graph."""
        # Simplified critical path calculation
        # In a real implementation, this would use proper CPM algorithm

        # Find starting nodes (no predecessors)
        start_nodes = [
            tid for tid, info in dependency_graph.items() if not info["predecessors"]
        ]

        if not start_nodes:
            return []

        # For now, return the longest path heuristically
        longest_path = []
        max_duration = 0

        for start_node in start_nodes:
            path, duration = self._find_longest_path(start_node, dependency_graph, [])
            if duration > max_duration:
                max_duration = duration
                longest_path = path

        return longest_path

    def _find_longest_path(
        self, node: str, graph: dict[str, dict[str, Any]], visited: list[str]
    ) -> tuple[list[str], float]:
        """Find the longest path from a given node."""
        if node in visited:  # Avoid cycles
            return [], 0.0

        current_path = [*visited, node]
        current_duration = graph[node]["duration"]

        successors = graph[node]["successors"]
        if not successors:
            return current_path, current_duration

        max_path = current_path
        max_duration = current_duration

        for succ_id, _ in successors:
            path, duration = self._find_longest_path(succ_id, graph, current_path)
            total_duration = current_duration + duration

            if total_duration > max_duration:
                max_duration = total_duration
                max_path = current_path + path[1:]  # Avoid duplicating current node

        return max_path, max_duration

    def _create_execution_phases(
        self, parallel_groups: list[ParallelGroup], dependencies: list[DependencyNode]
    ) -> list[ExecutionPhase]:
        """Create execution phases from parallel groups."""
        # Simplified phase creation
        # In reality, this would need sophisticated topological analysis

        phases = []
        phase_number = 1

        # Group parallel groups into phases based on dependencies
        remaining_groups = list(parallel_groups)

        while remaining_groups:
            current_phase_groups = []

            # Find groups that can start in this phase
            for group in remaining_groups[:]:
                can_start = True

                # Check if all dependencies are satisfied by previous phases
                for dep in dependencies:
                    if dep.target_id in group.task_ids:
                        # Check if source is in a later group
                        for other_group in remaining_groups:
                            if (
                                other_group != group
                                and dep.source_id in other_group.task_ids
                            ):
                                can_start = False
                                break
                        if not can_start:
                            break

                if can_start:
                    current_phase_groups.append(group)
                    # Update group phase
                    group.phase = phase_number

            if not current_phase_groups:
                # Avoid infinite loop - take the first remaining group
                current_phase_groups = [remaining_groups[0]]
                current_phase_groups[0].phase = phase_number

            # Remove groups from remaining
            for group in current_phase_groups:
                if group in remaining_groups:
                    remaining_groups.remove(group)

            # Calculate phase duration (max of all groups)
            phase_duration = (
                max(group.estimated_duration_minutes for group in current_phase_groups)
                if current_phase_groups
                else 0.0
            )

            phases.append(
                ExecutionPhase(
                    phase_number=phase_number,
                    name=f"Phase {phase_number}",
                    parallel_groups=current_phase_groups,
                    estimated_duration_minutes=phase_duration,
                )
            )

            phase_number += 1

        return phases

    def _calculate_sequential_duration(self, items: list[Task | TaskStep]) -> float:
        """Calculate total duration if all tasks run sequentially."""
        total = 0.0
        for item in items:
            if isinstance(item, TaskStep):
                total += item.estimated_duration_minutes
            elif isinstance(item, Task):
                total += item.calculate_total_duration()
        return total

    def _calculate_parallel_duration(self, phases: list[ExecutionPhase]) -> float:
        """Calculate total duration with parallel execution."""
        return sum(phase.estimated_duration_minutes for phase in phases)

    def _determine_execution_strategy(
        self, parallel_groups: list[ParallelGroup], resource_constraints: dict[str, Any]
    ) -> ExecutionStrategy:
        """Determine the best execution strategy."""
        if not parallel_groups:
            return ExecutionStrategy.SEQUENTIAL

        max_parallelism = max(group.get_task_count() for group in parallel_groups)

        # Consider resource constraints
        if resource_constraints:
            available_workers = resource_constraints.get(
                "workers", resource_constraints.get("cpu_cores", float("inf"))
            )
            if (
                isinstance(available_workers, int | float)
                and max_parallelism > available_workers
            ):
                return ExecutionStrategy.RESOURCE_CONSTRAINED

        # Default to balanced approach
        return ExecutionStrategy.BALANCED

    def _calculate_peak_resources(
        self, parallel_groups: list[ParallelGroup]
    ) -> dict[str, Any]:
        """Calculate peak resource requirements."""
        peak_resources = {}

        for group in parallel_groups:
            for resource, amount in group.resource_requirements.items():
                if resource not in peak_resources:
                    peak_resources[resource] = amount
                elif isinstance(amount, int | float):
                    peak_resources[resource] = max(peak_resources[resource], amount)

        return peak_resources

    def _identify_bottlenecks(
        self, parallel_groups: list[ParallelGroup], resource_constraints: dict[str, Any]
    ) -> list[str]:
        """Identify potential bottlenecks."""
        bottlenecks = []

        # Check resource constraints
        peak_resources = self._calculate_peak_resources(parallel_groups)

        for resource, required in peak_resources.items():
            available = resource_constraints.get(resource)
            if (
                available is not None
                and isinstance(required, (int, float))
                and isinstance(available, (int, float))
            ) and required > available:
                bottlenecks.append(
                    f"Insufficient {resource}: need {required}, have {available}"
                )

        # Check for large parallel groups
        max_parallelism = (
            max(group.get_task_count() for group in parallel_groups)
            if parallel_groups
            else 0
        )
        if max_parallelism > self.max_parallel_tasks:
            bottlenecks.append(
                f"Parallelism limit: {max_parallelism} tasks exceed limit of {self.max_parallel_tasks}"
            )

        return bottlenecks
