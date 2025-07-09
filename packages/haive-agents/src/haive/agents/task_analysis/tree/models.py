# src/haive/agents/task_analysis/tree/models.py

from collections.abc import Callable
from typing import Any

from haive.core.common.structures.tree import AutoTree

from haive.agents.task_analysis.base.models import (
    ActionStep,
    TaskNode,
)


class TaskTree(AutoTree[TaskNode]):
    """Enhanced AutoTree specifically for task analysis.
    Adds task-specific functionality while leveraging AutoTree's auto-building.
    """

    def __init__(self, content: TaskNode, **kwargs):
        super().__init__(content, **kwargs)
        # Task-specific initialization
        self._join_points: list[dict[str, Any]] = []
        self._parallel_groups: list[list[str]] = []
        self._critical_path: list[str] = []
        self._analyze_structure()

    def _analyze_structure(self):
        """Analyze task structure after tree is built."""
        self._identify_join_points()
        self._identify_parallel_groups()
        self._calculate_critical_path()

    def _identify_join_points(self):
        """Find all join points in the task tree."""
        # Look for tasks marked as join points
        for node in self.traverse_depth_first(lambda n: n):  # type: ignore
            if hasattr(node.content, "is_join_point") and node.content.is_join_point:
                # Find incoming dependencies
                incoming = self._find_incoming_tasks(node.content.task_id)
                if len(incoming) > 1:
                    self._join_points.append(
                        {
                            "join_id": f"join_{node.content.task_id}",
                            "task_id": node.content.task_id,
                            "incoming_tasks": incoming,
                            "join_strategy": node.content.join_strategy or "merge",
                        }
                    )

    def _identify_parallel_groups(self):
        """Identify groups of tasks that can run in parallel."""
        # Group tasks by their dependencies
        dependency_map = self._build_dependency_map()

        # Find tasks with no interdependencies
        all_task_ids = self._get_all_task_ids()

        for i, task_id1 in enumerate(all_task_ids):
            group = [task_id1]
            for task_id2 in all_task_ids[i + 1 :]:
                if not self._has_path_between(task_id1, task_id2, dependency_map):
                    group.append(task_id2)

            if len(group) > 1:
                self._parallel_groups.append(group)

    def _calculate_critical_path(self):
        """Calculate the critical path through the task tree."""
        # Simplified - would use proper CPM algorithm
        path = []

        # Start from root
        current = self.content
        path.append(current.task_id)

        # Follow path with highest duration
        while current.subtasks:
            max_duration_subtask = None
            max_duration = 0

            for subtask in current.subtasks:
                duration = self._get_subtask_duration(subtask)
                if duration > max_duration:
                    max_duration = duration
                    max_duration_subtask = subtask

            if max_duration_subtask:
                if isinstance(max_duration_subtask, TaskNode):
                    path.append(max_duration_subtask.task_id)
                    current = max_duration_subtask
                else:
                    path.append(max_duration_subtask.step_id)
                    break
            else:
                break

        self._critical_path = path

    def _build_dependency_map(self) -> dict[str, list[str]]:
        """Build a map of dependencies."""
        dep_map = {}

        for node in self.traverse_depth_first(lambda n: n):  # type: ignore
            if hasattr(node.content, "dependencies"):
                for dep in node.content.dependencies:
                    if dep.target_id not in dep_map:
                        dep_map[dep.target_id] = []
                    dep_map[dep.target_id].append(dep.source_id)

        return dep_map

    def _get_all_task_ids(self) -> list[str]:
        """Get all task and step IDs."""
        ids = []
        for node in self.traverse_depth_first(lambda n: n):  # type: ignore
            if hasattr(node.content, "task_id"):
                ids.append(node.content.task_id)
            elif hasattr(node.content, "step_id"):
                ids.append(node.content.step_id)
        return ids

    def _has_path_between(
        self, id1: str, id2: str, dep_map: dict[str, list[str]]
    ) -> bool:
        """Check if there's a dependency path between two tasks."""
        # BFS to find path
        visited = set()
        queue = [id1]

        while queue:
            current = queue.pop(0)
            if current == id2:
                return True

            visited.add(current)

            # Check dependencies
            if current in dep_map:
                for dep in dep_map[current]:
                    if dep not in visited:
                        queue.append(dep)

        return False

    def _find_incoming_tasks(self, task_id: str) -> list[str]:
        """Find all tasks that have dependencies pointing to this task."""
        incoming = []

        for node in self.traverse_depth_first(lambda n: n):  # type: ignore
            if hasattr(node.content, "dependencies"):
                for dep in node.content.dependencies:
                    if dep.target_id == task_id:
                        incoming.append(dep.source_id)

        return incoming

    def _get_subtask_duration(self, subtask: TaskNode | ActionStep) -> float:
        """Get duration of a subtask."""
        if isinstance(subtask, ActionStep):
            return subtask.estimated_duration_minutes
        if isinstance(subtask, TaskNode):
            return subtask.calculate_total_duration()
        return 0.0

    # ========================================================================
    # PUBLIC METHODS
    # ========================================================================

    def get_join_points(self) -> list[dict[str, Any]]:
        """Get all join points in the tree."""
        return self._join_points

    def get_parallel_groups(self) -> list[list[str]]:
        """Get groups of tasks that can run in parallel."""
        return self._parallel_groups

    def get_critical_path(self) -> list[str]:
        """Get the critical path."""
        return self._critical_path

    def get_execution_phases(self) -> list[dict[str, Any]]:
        """Organize tasks into execution phases.
        Tasks in the same phase can run in parallel.
        """
        phases = []
        processed = set()

        # Build dependency map
        dep_map = self._build_dependency_map()
        all_ids = self._get_all_task_ids()

        phase_num = 1
        while len(processed) < len(all_ids):
            # Find tasks that can run (all dependencies satisfied)
            phase_tasks = []

            for task_id in all_ids:
                if task_id in processed:
                    continue

                # Check if all dependencies are processed
                deps = dep_map.get(task_id, [])
                if all(dep in processed for dep in deps):
                    phase_tasks.append(task_id)

            if phase_tasks:
                phases.append(
                    {
                        "phase_number": phase_num,
                        "tasks": phase_tasks,
                        "can_parallelize": len(phase_tasks) > 1,
                    }
                )
                processed.update(phase_tasks)
                phase_num += 1
            else:
                # Avoid infinite loop
                break

        return phases

    def expand_node(
        self,
        node_id: str,
        expansion_fn: Callable[[TaskNode], list[TaskNode | ActionStep]],
    ) -> bool:
        """Expand a specific node using the provided expansion function.
        Returns True if expansion was successful.
        """
        # Find the node
        target_node = None
        for node in self.traverse_depth_first(lambda n: n):  # type: ignore
            if hasattr(node.content, "task_id") and node.content.task_id == node_id:
                target_node = node
                break

        if not target_node or not isinstance(target_node.content, TaskNode):
            return False

        if not target_node.content.can_expand:
            return False

        # Expand using provided function
        new_subtasks = expansion_fn(target_node.content)

        # Add new subtasks
        for subtask in new_subtasks:
            target_node.content.add_subtask(subtask)

        # Rebuild the tree structure
        target_node._build_children()

        # Re-analyze structure
        self._analyze_structure()

        return True

    def get_analysis_summary(self) -> dict[str, Any]:
        """Get a summary of the task tree analysis."""
        all_steps = self.content.get_all_steps()

        return {
            "total_tasks": len(self._get_all_task_ids()),
            "total_steps": len(all_steps),
            "max_depth": self._calculate_max_depth(0),
            "total_duration_minutes": self.content.calculate_total_duration(),
            "critical_path_length": len(self._critical_path),
            "join_points": len(self._join_points),
            "parallel_groups": len(self._parallel_groups),
            "can_parallelize": len(self._parallel_groups) > 0,
        }

    def _calculate_max_depth(self, current_depth: int) -> int:
        """Calculate maximum depth from this node."""
        if not self.children:
            return current_depth

        max_child_depth = max(
            child._calculate_max_depth(current_depth + 1)
            for child in self.children
            if isinstance(child, TaskTree)
        )

        return max_child_depth
