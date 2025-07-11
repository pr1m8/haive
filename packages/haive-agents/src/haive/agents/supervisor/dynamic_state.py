"""Enhanced state schema for dynamic supervisor operations.

This module provides an enhanced state management system for dynamic supervisor
agents that can add/remove agents at runtime and adapt their responses based
on agent configuration and execution context.
"""

import time
from typing import Any, Dict, List, Optional, Set, Union
from uuid import uuid4

from haive.core.schema.state_schema import StateSchema
from langchain_core.messages import BaseMessage
from pydantic import BaseModel, Field, computed_field


class AgentExecutionConfig(BaseModel):
    """Configuration for agent execution within supervisor context."""

    agent_name: str = Field(description="Name of the agent")
    capability_description: str = Field(description="Agent's capability description")
    execution_timeout: float | None = Field(
        default=300.0, description="Timeout in seconds"
    )
    retry_count: int = Field(default=0, description="Number of retries attempted")
    max_retries: int = Field(default=3, description="Maximum retries allowed")
    output_mode: str = Field(
        default="full_history", description="Output mode: full_history, last_message"
    )
    handoff_back: bool = Field(
        default=True, description="Whether to include handoff back messages"
    )
    priority: int = Field(
        default=1, description="Agent priority (higher = more priority)"
    )

    # Agent metadata
    agent_type: str | None = Field(
        default=None, description="Type of agent (react, simple, etc.)"
    )
    created_at: float = Field(
        default_factory=time.time, description="When agent was registered"
    )
    last_used_at: float | None = Field(
        default=None, description="Last execution timestamp"
    )
    success_count: int = Field(default=0, description="Number of successful executions")
    error_count: int = Field(default=0, description="Number of failed executions")

    # Dynamic configuration
    custom_params: dict[str, Any] = Field(
        default_factory=dict, description="Custom agent parameters"
    )
    state_adapters: dict[str, Any] = Field(
        default_factory=dict, description="State adaptation rules"
    )


class AgentExecutionResult(BaseModel):
    """Result of agent execution with metadata."""

    execution_id: str = Field(
        default_factory=lambda: str(uuid4()), description="Unique execution ID"
    )
    agent_name: str = Field(description="Name of executed agent")
    success: bool = Field(description="Whether execution was successful")
    start_time: float = Field(
        default_factory=time.time, description="Execution start time"
    )
    end_time: float | None = Field(default=None, description="Execution end time")
    duration: float | None = Field(
        default=None, description="Execution duration in seconds"
    )

    # Results
    messages: list[BaseMessage] = Field(
        default_factory=list, description="Messages from agent execution"
    )
    output: Any | None = Field(default=None, description="Agent output data")
    error: str | None = Field(default=None, description="Error message if failed")

    # Metadata
    token_usage: dict[str, int] | None = Field(
        default=None, description="Token usage statistics"
    )
    tool_calls: list[dict[str, Any]] = Field(
        default_factory=list, description="Tools called during execution"
    )
    state_changes: dict[str, Any] = Field(
        default_factory=dict, description="State changes made"
    )


class SupervisorDecision(BaseModel):
    """Represents a supervisor routing decision with reasoning."""

    decision_id: str = Field(
        default_factory=lambda: str(uuid4()), description="Unique decision ID"
    )
    target_agent: str | None = Field(description="Selected agent name or END")
    reasoning: str = Field(description="Explanation for the decision")
    confidence: float = Field(
        default=0.5, ge=0.0, le=1.0, description="Confidence in decision"
    )
    timestamp: float = Field(
        default_factory=time.time, description="When decision was made"
    )

    # Decision context
    available_agents: list[str] = Field(
        default_factory=list, description="Agents available at decision time"
    )
    input_analysis: dict[str, Any] = Field(
        default_factory=dict, description="Analysis of user input"
    )
    previous_context: str | None = Field(
        default=None, description="Previous conversation context"
    )

    # Alternative options considered
    alternatives: list[dict[str, float]] = Field(
        default_factory=list, description="Other options with scores"
    )


class DynamicSupervisorState(StateSchema):
    """Enhanced state schema for dynamic supervisor operations.

    This state schema provides comprehensive tracking of agent execution,
    dynamic configuration, and adaptive response handling for supervisor agents.
    """

    # Core messaging (inherited from StateSchema)
    messages: list[BaseMessage] = Field(
        default_factory=list, description="Conversation messages"
    )

    # Agent management
    registered_agents: dict[str, AgentExecutionConfig] = Field(
        default_factory=dict, description="Currently registered agents with config"
    )
    agent_execution_history: list[AgentExecutionResult] = Field(
        default_factory=list, description="History of agent executions"
    )

    # Current execution context
    current_execution: AgentExecutionResult | None = Field(
        default=None, description="Currently executing agent result"
    )
    execution_queue: list[str] = Field(
        default_factory=list, description="Queue of agents to execute"
    )

    # Supervisor decision tracking
    routing_decisions: list[SupervisorDecision] = Field(
        default_factory=list, description="History of routing decisions"
    )
    current_decision: SupervisorDecision | None = Field(
        default=None, description="Current routing decision"
    )

    # Dynamic configuration
    supervisor_config: dict[str, Any] = Field(
        default_factory=dict, description="Dynamic supervisor configuration"
    )
    adaptation_rules: dict[str, Any] = Field(
        default_factory=dict, description="Rules for adapting agent responses"
    )

    # Performance tracking
    session_stats: dict[str, Any] = Field(
        default_factory=lambda: {
            "total_executions": 0,
            "successful_executions": 0,
            "failed_executions": 0,
            "average_response_time": 0.0,
            "session_start": time.time(),
        },
        description="Session-level performance statistics",
    )

    # Task and conversation management
    task_context: dict[str, Any] = Field(
        default_factory=dict, description="Current task context and requirements"
    )
    conversation_metadata: dict[str, Any] = Field(
        default_factory=dict, description="Conversation-level metadata"
    )

    # Flags and control
    requires_human_intervention: bool = Field(
        default=False, description="Whether human intervention is needed"
    )
    conversation_complete: bool = Field(
        default=False, description="Whether conversation is finished"
    )
    auto_adapt_responses: bool = Field(
        default=True, description="Whether to automatically adapt agent responses"
    )
    parallel_execution_enabled: bool = Field(
        default=False, description="Whether parallel agent execution is allowed"
    )

    @computed_field
    @property
    def active_agent_count(self) -> int:
        """Number of currently registered agents."""
        return len(self.registered_agents)

    @computed_field
    @property
    def last_execution_time(self) -> float | None:
        """Timestamp of last agent execution."""
        if not self.agent_execution_history:
            return None
        return max(result.start_time for result in self.agent_execution_history)

    @computed_field
    @property
    def success_rate(self) -> float:
        """Success rate of agent executions."""
        if not self.agent_execution_history:
            return 0.0
        successful = sum(1 for result in self.agent_execution_history if result.success)
        return successful / len(self.agent_execution_history)

    @computed_field
    @property
    def most_used_agent(self) -> str | None:
        """Name of most frequently used agent."""
        if not self.agent_execution_history:
            return None

        usage_counts = {}
        for result in self.agent_execution_history:
            usage_counts[result.agent_name] = usage_counts.get(result.agent_name, 0) + 1

        return (
            max(usage_counts.items(), key=lambda x: x[1])[0] if usage_counts else None
        )

    def add_agent_config(self, agent_name: str, config: AgentExecutionConfig) -> None:
        """Add or update agent configuration."""
        self.registered_agents[agent_name] = config

    def remove_agent_config(self, agent_name: str) -> bool:
        """Remove agent configuration."""
        if agent_name in self.registered_agents:
            del self.registered_agents[agent_name]
            return True
        return False

    def get_agent_config(self, agent_name: str) -> AgentExecutionConfig | None:
        """Get agent configuration by name."""
        return self.registered_agents.get(agent_name)

    def update_agent_stats(
        self, agent_name: str, success: bool, duration: float
    ) -> None:
        """Update agent execution statistics."""
        if agent_name in self.registered_agents:
            config = self.registered_agents[agent_name]
            config.last_used_at = time.time()
            if success:
                config.success_count += 1
            else:
                config.error_count += 1

    def add_execution_result(self, result: AgentExecutionResult) -> None:
        """Add execution result to history."""
        # Set end time and duration if not set
        if result.end_time is None:
            result.end_time = time.time()
        if result.duration is None and result.end_time:
            result.duration = result.end_time - result.start_time

        self.agent_execution_history.append(result)

        # Update session stats
        self.session_stats["total_executions"] += 1
        if result.success:
            self.session_stats["successful_executions"] += 1
        else:
            self.session_stats["failed_executions"] += 1

        # Update average response time
        total_duration = sum(
            r.duration or 0 for r in self.agent_execution_history if r.duration
        )
        self.session_stats["average_response_time"] = total_duration / len(
            self.agent_execution_history
        )

        # Update agent stats
        self.update_agent_stats(result.agent_name, result.success, result.duration or 0)

    def add_routing_decision(self, decision: SupervisorDecision) -> None:
        """Add routing decision to history."""
        self.routing_decisions.append(decision)
        self.current_decision = decision

    def get_recent_decisions(self, limit: int = 5) -> list[SupervisorDecision]:
        """Get recent routing decisions."""
        return self.routing_decisions[-limit:] if self.routing_decisions else []

    def get_agent_performance(self, agent_name: str) -> dict[str, Any]:
        """Get performance metrics for specific agent."""
        agent_results = [
            r for r in self.agent_execution_history if r.agent_name == agent_name
        ]

        if not agent_results:
            return {"executions": 0, "success_rate": 0.0, "average_duration": 0.0}

        successful = sum(1 for r in agent_results if r.success)
        durations = [r.duration for r in agent_results if r.duration is not None]

        return {
            "executions": len(agent_results),
            "success_rate": successful / len(agent_results),
            "average_duration": sum(durations) / len(durations) if durations else 0.0,
            "last_execution": max(r.start_time for r in agent_results),
            "error_count": len(agent_results) - successful,
        }

    def should_retry_agent(self, agent_name: str) -> bool:
        """Determine if agent should be retried based on configuration."""
        config = self.get_agent_config(agent_name)
        if not config:
            return False
        return config.retry_count < config.max_retries

    def increment_retry_count(self, agent_name: str) -> None:
        """Increment retry count for agent."""
        config = self.get_agent_config(agent_name)
        if config:
            config.retry_count += 1

    def reset_retry_count(self, agent_name: str) -> None:
        """Reset retry count for agent."""
        config = self.get_agent_config(agent_name)
        if config:
            config.retry_count = 0

    def get_available_agents(self) -> list[str]:
        """Get list of available agent names."""
        return list(self.registered_agents.keys())

    def get_high_priority_agents(self) -> list[str]:
        """Get agents sorted by priority (highest first)."""
        agents_with_priority = [
            (name, config.priority) for name, config in self.registered_agents.items()
        ]
        return [
            name
            for name, _ in sorted(
                agents_with_priority, key=lambda x: x[1], reverse=True
            )
        ]

    def adapt_response_for_agent(self, agent_name: str, response: Any) -> Any:
        """Apply adaptation rules to agent response."""
        if not self.auto_adapt_responses:
            return response

        config = self.get_agent_config(agent_name)
        if not config or not config.state_adapters:
            return response

        # Apply any configured state adapters
        adapted_response = response
        for _adapter_name, _adapter_config in config.state_adapters.items():
            # This would be implemented based on specific adaptation needs
            # For now, return original response
            pass

        return adapted_response

    def cleanup_old_history(self, max_history: int = 100) -> None:
        """Clean up old execution history to prevent memory bloat."""
        if len(self.agent_execution_history) > max_history:
            self.agent_execution_history = self.agent_execution_history[-max_history:]

        if len(self.routing_decisions) > max_history:
            self.routing_decisions = self.routing_decisions[-max_history:]
