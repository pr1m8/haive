# haive/core/schema/meta_agent_state.py
"""Meta agent state for multi-agent coordination.

This module provides a state schema that enables agents to share metadata,
coordination information, and workflow state in multi-agent systems.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from haive.core.schema.state_schema import StateSchema


class AgentExecutionInfo(BaseModel):
    """Information about an agent's execution."""

    agent_id: str = Field(description="ID of the agent")
    agent_name: str = Field(description="Name of the agent")
    started_at: datetime | None = Field(
        default=None, description="When execution started"
    )
    completed_at: datetime | None = Field(
        default=None, description="When execution completed"
    )
    status: str = Field(
        default="pending",
        description="Execution status: pending, running, completed, failed",
    )
    error: str | None = Field(default=None, description="Error message if failed")
    output: Any | None = Field(default=None, description="Output produced by the agent")


class MetaAgentState(StateSchema):
    """Meta state for multi-agent coordination.

    This state provides shared fields for coordinating multiple agents including:
    - Tracking which agent is currently active
    - Storing outputs from each agent
    - Managing workflow metadata
    - Sharing coordination information
    """

    # Core coordination fields
    active_agent_id: str | None = Field(
        default=None, description="ID of the currently active agent"
    )

    active_agent_name: str | None = Field(
        default=None, description="Name of the currently active agent"
    )

    # Agent outputs and history
    agent_outputs: dict[str, Any] = Field(
        default_factory=dict, description="Outputs from each agent keyed by agent ID"
    )

    agent_execution_history: list[AgentExecutionInfo] = Field(
        default_factory=list, description="History of agent executions"
    )

    # Workflow management
    workflow_metadata: dict[str, Any] = Field(
        default_factory=dict, description="Metadata about the current workflow"
    )

    workflow_stage: str | None = Field(
        default=None, description="Current stage of the workflow"
    )

    # Shared context
    shared_context: dict[str, Any] = Field(
        default_factory=dict, description="Shared context accessible to all agents"
    )

    # Error handling
    last_error: str | None = Field(
        default=None, description="Last error that occurred in the workflow"
    )

    error_count: int = Field(default=0, description="Number of errors encountered")

    # Control flow
    should_continue: bool = Field(
        default=True, description="Whether the workflow should continue"
    )

    next_agent_hint: str | None = Field(
        default=None, description="Hint for which agent should execute next"
    )

    # Configuration for field sharing
    __shared_fields__ = {
        "active_agent_id",
        "active_agent_name",
        "agent_outputs",
        "agent_execution_history",
        "workflow_metadata",
        "workflow_stage",
        "shared_context",
        "last_error",
        "error_count",
        "should_continue",
        "next_agent_hint",
    }

    # All fields use default reducers (last write wins)
    __reducer_fields__ = {}

    def record_agent_start(self, agent_id: str, agent_name: str) -> None:
        """Record that an agent has started execution."""
        self.active_agent_id = agent_id
        self.active_agent_name = agent_name

        # Add to execution history
        exec_info = AgentExecutionInfo(
            agent_id=agent_id,
            agent_name=agent_name,
            started_at=datetime.now(),
            status="running",
        )
        self.agent_execution_history.append(exec_info)

    def record_agent_completion(self, agent_id: str, output: Any) -> None:
        """Record that an agent has completed execution."""
        # Store output
        self.agent_outputs[agent_id] = output

        # Update execution history
        for exec_info in reversed(self.agent_execution_history):
            if exec_info.agent_id == agent_id and exec_info.status == "running":
                exec_info.completed_at = datetime.now()
                exec_info.status = "completed"
                exec_info.output = output
                break

        # Clear active agent
        self.active_agent_id = None
        self.active_agent_name = None

    def record_agent_error(self, agent_id: str, error: str) -> None:
        """Record that an agent encountered an error."""
        self.last_error = error
        self.error_count += 1

        # Update execution history
        for exec_info in reversed(self.agent_execution_history):
            if exec_info.agent_id == agent_id and exec_info.status == "running":
                exec_info.completed_at = datetime.now()
                exec_info.status = "failed"
                exec_info.error = error
                break

    def get_agent_output(self, agent_id: str) -> Any | None:
        """Get the output from a specific agent."""
        return self.agent_outputs.get(agent_id)

    def set_shared_context(self, key: str, value: Any) -> None:
        """Set a value in the shared context."""
        self.shared_context[key] = value

    def get_shared_context(self, key: str, default: Any = None) -> Any:
        """Get a value from the shared context."""
        return self.shared_context.get(key, default)

    def update_workflow_stage(
        self, stage: str, metadata: dict[str, Any] | None = None
    ) -> None:
        """Update the current workflow stage."""
        self.workflow_stage = stage
        if metadata:
            self.workflow_metadata.update(metadata)

    def signal_stop(self, reason: str | None = None) -> None:
        """Signal that the workflow should stop."""
        self.should_continue = False
        if reason:
            self.workflow_metadata["stop_reason"] = reason
