"""Models for the LLM Compiler agent.

This module defines the pydantic models specific to the LLM Compiler agent,
integrating with the base Step and Plan models from the plan_and_execute agent.
"""

from typing import Any

from agents.plan_and_execute.models import Plan, Step
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field


class TaskDependency(BaseModel):
    """Represents a dependency reference to another task's output.

    This allows for tracking references between steps in the plan.
    """

    step_id: int = Field(description="ID of the step that outputs needed data")
    output_key: str | None = Field(
        default=None, description="Specific key in the output (if needed)"
    )

    def resolve(self, results: dict[int, Any]) -> Any:
        """Resolve the dependency to the actual value."""
        if self.step_id not in results:
            return f"${{{self.step_id}}}"  # Unresolved dependency

        result = results[self.step_id]
        if self.output_key and isinstance(result, dict):
            return result.get(self.output_key, f"${{{self.step_id}.{self.output_key}}}")

        return result


class CompilerTask(BaseModel):
    """Represents a task in the LLM Compiler framework's DAG.

    Tasks define what tools to run and their dependencies on other tasks.
    """

    tool_name: str = Field(description="Name of the tool to execute (or 'join')")
    arguments: dict[str, Any] = Field(
        default_factory=dict, description="Arguments for the tool"
    )
    dependencies: list[TaskDependency] = Field(
        default_factory=list, description="Dependencies on other tasks"
    )

    @property
    def is_join(self) -> bool:
        """Check if this is a join (final) task."""
        return self.tool_name.lower() == "join"

    def resolve_arguments(self, results: dict[int, Any]) -> dict[str, Any]:
        """Resolve dependencies in arguments to actual values.

        Args:
            results: Dictionary mapping step IDs to their results

        Returns:
            Dictionary with resolved argument values
        """
        resolved_args = {}

        for key, value in self.arguments.items():
            if isinstance(value, str) and value.startswith("$"):
                # This is a reference to another step's output
                # Extract the step ID from the format ${1} or $1
                import re

                match = re.match(r"\$\{?(\d+)\}?", value)
                if match:
                    step_id = int(match.group(1))
                    if step_id in results:
                        resolved_args[key] = results[step_id]
                    else:
                        resolved_args[key] = value  # Keep unresolved
                else:
                    resolved_args[key] = value
            else:
                # Regular value, no resolution needed
                resolved_args[key] = value

        return resolved_args


class CompilerStep(Step):
    """Extends the base Step model with LLM Compiler-specific fields.

    Each step contains a task to execute and tracks dependencies.
    """

    task: CompilerTask = Field(description="The task to execute for this step")

    @property
    def dependencies(self) -> list[int]:
        """Get IDs of steps this step depends on."""
        dep_ids = []
        # Extract step IDs from TaskDependency objects
        for dep in self.task.dependencies:
            dep_ids.append(dep.step_id)

        # Also check for string references in arguments
        for arg_value in self.task.arguments.values():
            if isinstance(arg_value, str) and arg_value.startswith("$"):
                import re

                match = re.match(r"\$\{?(\d+)\}?", arg_value)
                if match:
                    dep_ids.append(int(match.group(1)))

        return dep_ids

    def can_execute(self, results: dict[int, Any]) -> bool:
        """Check if all dependencies are satisfied.

        Args:
            results: Dictionary mapping step IDs to their results

        Returns:
            True if all dependencies are satisfied, False otherwise
        """
        return all(dep_id in results for dep_id in self.dependencies)

    def execute(self, tool_map: dict[str, BaseTool], results: dict[int, Any]) -> Any:
        """Execute this step's task with the given tools.

        Args:
            tool_map: Dictionary mapping tool names to tool objects
            results: Dictionary mapping step IDs to their results

        Returns:
            Result of executing the task
        """
        if self.task.is_join:
            return "join"

        # Get the tool
        tool = tool_map.get(self.task.tool_name)
        if not tool:
            return f"ERROR: Tool '{self.task.tool_name}' not found"

        # Resolve arguments
        resolved_args = self.task.resolve_arguments(results)

        # Execute the tool
        try:
            return tool.invoke(resolved_args)
        except Exception as e:
            import traceback

            return f"ERROR: {e!s}\n{traceback.format_exc()}"


class CompilerPlan(Plan):
    """Extends the base Plan model for the LLM Compiler agent.

    Handles DAG execution and dependency tracking.
    """

    steps: list[CompilerStep] = Field(
        default_factory=list, description="Steps in the plan"
    )

    def get_executable_steps(self, results: dict[int, Any]) -> list[CompilerStep]:
        """Get steps that can be executed (all dependencies satisfied).

        Args:
            results: Dictionary mapping step IDs to their results

        Returns:
            List of executable steps
        """
        return [
            step
            for step in self.steps
            if not step.is_complete() and step.can_execute(results)
        ]

    def get_join_step(self) -> CompilerStep | None:
        """Get the join step (final step) if present."""
        for step in self.steps:
            if step.task.is_join:
                return step
        return None

    def get_step_by_id(self, step_id: int) -> CompilerStep | None:
        """Find a step by its ID."""
        for step in self.steps:
            if step.id == step_id:
                return step
        return None

    def add_compiler_step(
        self,
        step_id: int,
        description: str,
        tool_name: str,
        arguments: dict[str, Any],
        dependencies: list[int | TaskDependency] | None = None,
    ) -> CompilerStep:
        """Add a new compiler step to the plan.

        Args:
            step_id: Unique ID for the step
            description: Description of the step
            tool_name: Name of the tool to execute
            arguments: Arguments for the tool
            dependencies: List of step IDs or TaskDependency objects

        Returns:
            The newly created step
        """
        # Convert simple int dependencies to TaskDependency objects
        task_dependencies = []
        if dependencies:
            for dep in dependencies:
                if isinstance(dep, int):
                    task_dependencies.append(TaskDependency(step_id=dep))
                else:
                    task_dependencies.append(dep)

        # Create the task
        task = CompilerTask(
            tool_name=tool_name, arguments=arguments, dependencies=task_dependencies
        )

        # Create the step
        step = CompilerStep(
            id=step_id, description=description, task=task, status="not_started"
        )

        # Add to plan
        self.steps.append(step)
        return step


# FinalResponse and Replan models for joiner decisions


class FinalResponse(BaseModel):
    """The final response/answer to return to the user."""

    response: str


class Replan(BaseModel):
    """Feedback for replanning when the current plan wasn't sufficient."""

    feedback: str = Field(
        description="Analysis of the previous attempts and recommendations on what needs to be fixed."
    )


class JoinerOutput(BaseModel):
    """The joiner's decision: either provide a final response or request replanning."""

    thought: str = Field(
        description="The chain of thought reasoning for the selected action"
    )
    action: FinalResponse | Replan = Field(
        description="The action to take: either provide a final response or replan"
    )
