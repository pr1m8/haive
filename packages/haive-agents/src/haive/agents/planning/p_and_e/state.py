# src/haive/agents/plan_and_execute/state.py
"""State schemas for Plan and Execute Agent System.

This module defines the state schemas used by the planning, execution,
and replanning agents.
"""

from datetime import datetime
from typing import Annotated, Any, Dict, List, Optional

from haive.core.schema.prebuilt.messages.messages_state import MessagesState
from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages
from pydantic import Field, computed_field

from haive.agents.planning.p_and_e.models import (
    ExecutionResult,
    Plan,
    PlanStep,
    ReplanDecision,
    StepStatus,
)


class PlanExecuteState(MessagesState):
    """Main state schema for the Plan and Execute agent system.

    This state is shared across planning, execution, and replanning agents
    to maintain the full context of the operation.
    """

    # Messages field is inherited from MessagesState

    @computed_field
    @property
    def objective(self) -> str:
        """Get the objective from the plan or messages."""
        if self.plan and self.plan.objective:
            return self.plan.objective

        # Fallback to extracting from messages
        messages = getattr(self, "messages", None)
        if messages:
            for msg in messages:
                # Handle both dict and Message object formats
                if hasattr(msg, "type"):
                    msg_type = msg.type
                    msg_content = msg.content
                elif isinstance(msg, dict):
                    msg_type = msg.get("type")
                    msg_content = msg.get("content")
                else:
                    continue

                if msg_type == "human" and msg_content:
                    return msg_content.strip()
        return "No objective specified"

    # Additional context
    context: str | None = Field(
        default=None, description="Additional context or requirements for the objective"
    )

    # Current plan
    plan: Plan | None = Field(default=None, description="The current execution plan")

    # Execution tracking
    current_step_id: int | None = Field(
        default=None, description="ID of the step currently being executed"
    )

    execution_results: list[ExecutionResult] = Field(
        default_factory=list, description="Results from executed steps"
    )

    # Replanning tracking
    replan_count: int = Field(
        default=0, description="Number of times the plan has been revised"
    )

    replan_history: list[dict[str, Any]] = Field(
        default_factory=list, description="History of replanning decisions and reasons"
    )

    # Final answer
    final_answer: str | None = Field(
        default=None, description="Final answer once execution is complete"
    )

    # Error tracking
    errors: list[dict[str, Any]] = Field(
        default_factory=list, description="Errors encountered during execution"
    )

    # Timestamp tracking
    started_at: datetime = Field(
        default_factory=datetime.now, description="When the execution started"
    )

    completed_at: datetime | None = Field(
        default=None, description="When the execution completed"
    )

    @computed_field
    @property
    def execution_time(self) -> float | None:
        """Total execution time in seconds."""
        # Use getattr with defaults to avoid AttributeError during initialization
        started_at = getattr(self, "started_at", None)
        completed_at = getattr(self, "completed_at", None)
        if started_at and completed_at:
            return (completed_at - started_at).total_seconds()
        return None

    @computed_field
    @property
    def current_step(self) -> str | None:
        """Get the current step formatted for the executor."""
        if not self.plan or not self.current_step_id:
            return None

        step = self.plan.get_step(self.current_step_id)
        if not step:
            return None

        return step.to_prompt_format()

    @computed_field
    @property
    def plan_status(self) -> str:
        """Get the plan status formatted for the executor."""
        if not self.plan:
            return "No plan available"

        lines = [
            f"Objective: {self.plan.objective}",
            f"Total Steps: {self.plan.total_steps}",
            f"Progress: {self.plan.progress_percentage:.1f}%",
            f"Completed: {len(self.plan.completed_steps)}",
            f"Failed: {len(self.plan.failed_steps)}",
            f"Pending: {len(self.plan.pending_steps)}",
        ]

        if self.plan.next_step:
            lines.append(f"Next Step: {self.plan.next_step.step_id}")

        return "\n".join(lines)

    @computed_field
    @property
    def previous_results(self) -> str:
        """Get previous execution results formatted for the executor."""
        if not self.execution_results:
            return "No previous results"

        lines = []
        for result in self.execution_results[-5:]:  # Last 5 results
            lines.append(result.to_prompt_format())

        return "\n\n".join(lines)

    @computed_field
    @property
    def should_replan(self) -> bool:
        """Determine if replanning is needed."""
        if not self.plan:
            return True

        # Replan if there are failures and no next step
        if self.plan.has_failures and not self.plan.next_step:
            return True

        # Replan after every 3 completed steps for review
        completed_count = len(self.plan.completed_steps)
        return bool(completed_count > 0 and completed_count % 3 == 0)

    # Configuration for LangGraph - messages is already shared from MessagesState
    __shared_fields__ = [
        "messages",
        "objective",
        "plan",
        "execution_results",
        "final_answer",
    ]
