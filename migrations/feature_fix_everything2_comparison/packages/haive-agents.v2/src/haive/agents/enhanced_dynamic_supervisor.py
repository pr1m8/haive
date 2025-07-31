"""Enhanced DynamicSupervisor implementation extending SupervisorAgent.

DynamicSupervisor = SupervisorAgent + dynamic worker management + adaptive strategies.
"""

import logging
from typing import Any

from pydantic import Field, field_validator

from haive.agents.multi.enhanced_supervisor_agent import SupervisorAgent

logger = logging.getLogger(__name__)


class DynamicSupervisor(SupervisorAgent):
    """Enhanced DynamicSupervisor with adaptive worker management.

    DynamicSupervisor extends SupervisorAgent with:
    1. Dynamic worker addition/removal during execution
    2. Worker performance tracking
    3. Adaptive delegation strategies
    4. Worker pooling and recycling

    Attributes:
        max_workers: Maximum number of concurrent workers
        min_workers: Minimum number of workers to maintain
        worker_performance: Track worker performance metrics
        auto_scale: Enable automatic scaling based on load
        recycling_enabled: Enable worker recycling

    Examples:
        Dynamic scaling based on load::

            supervisor = DynamicSupervisor(
                name="auto_scaling_manager",
                min_workers=2,
                max_workers=10,
                auto_scale=True
            )

            # Starts with min workers, scales up as needed
            supervisor.add_worker("base_analyst", AnalystAgent())
            supervisor.add_worker("base_researcher", ResearchAgent())

            # During high load, automatically adds workers
            result = supervisor.run("Process 100 documents")

        Worker performance tracking::

            supervisor = DynamicSupervisor(
                name="performance_manager",
                track_performance=True
            )

            # After execution, check performance
            metrics = supervisor.get_worker_metrics()
            # Shows success rate, average time, task count per worker
    """

    # Dynamic supervisor specific fields
    max_workers: int = Field(
        default=10, ge=1, le=50, description="Maximum number of workers"
    )

    min_workers: int = Field(
        default=1, ge=0, le=10, description="Minimum number of workers to maintain"
    )

    worker_performance: dict[str, dict[str, Any]] = Field(
        default_factory=dict, description="Performance metrics for each worker"
    )

    auto_scale: bool = Field(default=False, description="Enable automatic scaling")

    worker_timeout: float = Field(
        default=60.0, gt=0, description="Timeout for worker tasks in seconds"
    )

    recycling_enabled: bool = Field(
        default=True, description="Enable recycling of idle workers"
    )

    worker_templates: dict[str, type] = Field(
        default_factory=dict, description="Templates for creating new workers"
    )

    active_tasks: dict[str, str] = Field(
        default_factory=dict, description="Map of task_id to worker_name"
    )

    idle_workers: set[str] = Field(
        default_factory=set, description="Set of idle worker names"
    )

    @field_validator("min_workers")
    @classmethod
    def validate_min_workers(cls, v: int, info) -> int:
        """Ensure min_workers <= max_workers."""
        max_workers = info.data.get("max_workers", 10)
        if v > max_workers:
            raise ValueError(
                f"min_workers ({v}) cannot exceed max_workers ({max_workers})"
            )
        return v

    def can_add_worker(self) -> bool:
        """Check if more workers can be added."""
        return len(self.workers) < self.max_workers

    def should_scale_up(self) -> bool:
        """Determine if should scale up workers."""
        if not self.auto_scale or not self.can_add_worker():
            return False

        # Scale up if all workers are busy
        return len(self.idle_workers) == 0 and len(self.active_tasks) >= len(
            self.workers
        )

    def should_scale_down(self) -> bool:
        """Determine if should scale down workers."""
        if not self.auto_scale or len(self.workers) <= self.min_workers:
            return False

        # Scale down if too many idle workers
        idle_ratio = len(self.idle_workers) / len(self.workers) if self.workers else 0
        return idle_ratio > 0.5  # More than 50% idle

    def add_worker_from_template(self, template_name: str, worker_name: str) -> bool:
        """Create and add a worker from template.

        Args:
            template_name: Name of the template to use
            worker_name: Name for the new worker

        Returns:
            True if worker was added successfully
        """
        if not self.can_add_worker():
            logger.warning(f"Cannot add worker: at max capacity ({self.max_workers})")
            return False

        if template_name not in self.worker_templates:
            logger.error(f"Unknown template: {template_name}")
            return False

        try:
            # Create worker from template
            worker_class = self.worker_templates[template_name]
            worker = worker_class()
            self.add_worker(worker_name, worker)

            # Initialize performance tracking
            self.worker_performance[worker_name] = {
                "tasks_completed": 0,
                "tasks_failed": 0,
                "total_time": 0.0,
                "success_rate": 1.0,
            }

            # Mark as idle
            self.idle_workers.add(worker_name)

            logger.info(f"Added worker '{worker_name}' from template '{template_name}'")
            return True

        except Exception as e:
            logger.error(f"Failed to create worker from template: {e}")
            return False

    def remove_idle_worker(self) -> str | None:
        """Remove an idle worker.

        Returns:
            Name of removed worker or None
        """
        if not self.idle_workers or len(self.workers) <= self.min_workers:
            return None

        # Remove least recently used idle worker
        worker_name = self.idle_workers.pop()
        removed = self.remove_worker(worker_name)

        if removed:
            # Clean up performance metrics
            self.worker_performance.pop(worker_name, None)
            logger.info(f"Removed idle worker '{worker_name}'")
            return worker_name

        return None

    def assign_task(self, task_id: str, worker_name: str | None = None) -> str | None:
        """Assign a task to a worker.

        Args:
            task_id: Unique task identifier
            worker_name: Specific worker to assign to (optional)

        Returns:
            Name of assigned worker or None
        """
        # Auto-scale if needed
        if self.should_scale_up() and self.worker_templates:
            template_name = list(self.worker_templates.keys())[0]
            worker_name = f"dynamic_worker_{len(self.workers)}"
            self.add_worker_from_template(template_name, worker_name)

        # Find available worker
        if worker_name and worker_name in self.idle_workers:
            assigned = worker_name
        elif self.idle_workers:
            assigned = self.idle_workers.pop()
        else:
            logger.warning("No idle workers available")
            return None

        # Assign task
        self.active_tasks[task_id] = assigned
        self.idle_workers.discard(assigned)

        logger.debug(f"Assigned task '{task_id}' to worker '{assigned}'")
        return assigned

    def complete_task(
        self, task_id: str, success: bool = True, duration: float = 0.0
    ) -> None:
        """Mark a task as completed.

        Args:
            task_id: Task identifier
            success: Whether task succeeded
            duration: Task duration in seconds
        """
        if task_id not in self.active_tasks:
            logger.warning(f"Unknown task: {task_id}")
            return

        worker_name = self.active_tasks.pop(task_id)

        # Update performance metrics
        if worker_name in self.worker_performance:
            metrics = self.worker_performance[worker_name]
            metrics["tasks_completed"] += 1
            if not success:
                metrics["tasks_failed"] += 1
            metrics["total_time"] += duration

            # Update success rate
            total = metrics["tasks_completed"]
            failed = metrics["tasks_failed"]
            metrics["success_rate"] = (total - failed) / total if total > 0 else 0

        # Mark worker as idle
        self.idle_workers.add(worker_name)

        # Auto-scale down if needed
        if self.should_scale_down():
            self.remove_idle_worker()

    def get_worker_metrics(self) -> dict[str, dict[str, Any]]:
        """Get performance metrics for all workers."""
        return {
            name: {
                **metrics,
                "average_time": (
                    metrics["total_time"] / metrics["tasks_completed"]
                    if metrics["tasks_completed"] > 0
                    else 0
                ),
                "is_idle": name in self.idle_workers,
            }
            for name, metrics in self.worker_performance.items()
        }

    def get_best_worker(self) -> str | None:
        """Get the best performing idle worker."""
        if not self.idle_workers:
            return None

        # Find idle worker with best success rate
        best_worker = None
        best_rate = 0.0

        for worker_name in self.idle_workers:
            if worker_name in self.worker_performance:
                rate = self.worker_performance[worker_name]["success_rate"]
                if rate > best_rate:
                    best_rate = rate
                    best_worker = worker_name

        return best_worker or next(iter(self.idle_workers))

    def __repr__(self) -> str:
        """String representation with dynamic info."""
        engine_type = type(self.engine).__name__ if self.engine else "None"
        return (
            f"DynamicSupervisor[{engine_type}]("
            f"name='{self.name}', "
            f"workers={len(self.workers)}/{self.max_workers}, "
            f"idle={len(self.idle_workers)}, "
            f"active_tasks={len(self.active_tasks)})"
        )


# Example usage
if __name__ == "__main__":
    # Mock worker class for demo
    class MockWorkerTemplate:
        """Template for creating workers."""

        def __init__(self):
            self.engine = None  # Would be actual engine

    # Create dynamic supervisor
    supervisor = DynamicSupervisor(
        name="dynamic_managef",
        min_workers=2,
        max_workers=5,
        auto_scale=True,
        worker_templates={
            "analyst": MockWorkerTemplate,
            "processor": MockWorkerTemplate,
        },
    )

    print(f"Created: {supervisor}")
    print(f"Auto-scaling: {supervisor.auto_scale}")
    print(f"Worker limits: {supervisor.min_workers}-{supervisor.max_workers}")

    # Simulate task assignment
    print("\nSimulating task flow:")

    # Add initial workers
    supervisor.add_worker_from_template("analyst", "analyst_1")
    supervisor.add_worker_from_template("processor", "processor_1")
    print(f"Initial state: {supervisor}")

    # Assign tasks
    task1 = supervisor.assign_task("task_001")
    print(f"Assigned task_001 to: {task1}")

    task2 = supervisor.assign_task("task_002")
    print(f"Assigned task_002 to: {task2}")

    # All workers busy, should trigger scale up
    task3 = supervisor.assign_task("task_003")
    print(f"Assigned task_003 to: {task3}")
    print(f"After scaling: {supervisor}")

    # Complete some tasks
    supervisor.complete_task("task_001", success=True, duration=5.0)
    supervisor.complete_task("task_002", success=False, duration=3.0)

    # Check metrics
    print("\nWorker metrics:")
    for name, metrics in supervisor.get_worker_metrics().items():
        print(
            f"  {name}: success_rate={metrics['success_rate']:.2f}, avg_time={metrics['average_time']:.2f}s"
        )
