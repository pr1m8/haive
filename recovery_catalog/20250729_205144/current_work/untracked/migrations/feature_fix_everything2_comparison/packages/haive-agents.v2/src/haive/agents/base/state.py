"""Base state schemas for supervisor agents.

This module provides the foundational state schemas that all supervisor
implementations extend from. It defines the core state structure for
tracking tasks, agents, routing decisions, and performance metrics.

The state management system supports:
    - Message-based conversation tracking (ReactAgent compatibility)
    - Task lifecycle management with history
    - Agent performance monitoring and metrics
    - Routing decision logging and analysis
    - Error tracking and recovery support

Example:
    Creating and managing supervisor state:

    >>> from haive.agents.supervisor_new.base.state import BaseSupervisorState
    >>> from haive.agents.supervisor_new.base.models import SupervisorTask
    >>> state = BaseSupervisorState(supervisor_name="main_supervisor")
    >>>
    >>> # Register an agent
    >>> state.register_agent_name("research_agent")
    >>> print(f"Active agents: {state.active_agent_names}")
    Active agents: ['research_agent']
    >>>
    >>> # Track a task
    >>> task = SupervisorTask(task_id="t1", content="Research AI trends")
    >>> state.add_task(task)
    >>> print(f"Current task: {state.current_task.task_id}")
    Current task: t1

    Performance tracking:

    >>> metrics = state.get_agent_performance("research_agent")
    >>> if metrics:
    ...     print(f"Success rate: {metrics.success_rate:.2%}")
    ... else:
    ...     print("No performance data yet")
    No performance data yet
"""

from typing import Any

from haive.core.schema.state_schema import StateSchema
from langchain_core.messages import BaseMessage
from pydantic import Field

from haive.agents.supervisor_new.base.models import (
    AgentPerformanceMetrics,
    RoutingDecision,
    SupervisorResult,
    SupervisorTask,
)


class BaseSupervisorState(StateSchema):
    """Base state schema for all supervisor agents.

    This provides the common fields and functionality needed by all
    supervisor implementations. It extends StateSchema to provide
    supervisor-specific state management including task tracking,
    agent performance monitoring, and routing decision history.

    Attributes:
        messages (List[BaseMessage]): Conversation messages (ReactAgent compatibility).
        supervisor_name (str): Name identifier for this supervisor instance.
        current_task (Optional[SupervisorTask]): Currently executing task.
        task_history (List[SupervisorTask]): Complete history of all tasks.
        results_history (List[SupervisorResult]): History of task execution results.
        last_routing_decision (Optional[RoutingDecision]): Most recent routing decision.
        routing_history (List[RoutingDecision]): Complete routing decision history.
        registered_agent_names (List[str]): Names of all registered agents.
        active_agent_names (List[str]): Names of currently active agents.
        agent_performance (Dict[str, AgentPerformanceMetrics]): Performance metrics per agent.
        execution_count (int): Total number of task executions.
        last_agent_used (Optional[str]): Name of last agent that executed a task.
        last_error (Optional[str]): Most recent error message if any.
        error_count (int): Total number of errors encountered.
        supervisor_metadata (Dict[str, Any]): Additional supervisor-specific metadata.

    Examples:
        Basic state management:

        >>> state = BaseSupervisorState(supervisor_name="coordinator")
        >>> state.register_agent_name("writer")
        >>> state.register_agent_name("researcher")
        >>> print(f"Registered: {len(state.registered_agent_names)} agents")
        Registered: 2 agents

        Task lifecycle management:

        >>> from haive.agents.supervisor_new.base.models import SupervisorTask, SupervisorResult
        >>> task = SupervisorTask(task_id="t1", content="Write article")
        >>> state.add_task(task)
        >>> result = SupervisorResult(
        ...     task_id="t1", agent_used="writer", result="Article written",
        ...     execution_time=1.5, success=True
        ... )
        >>> state.complete_task(result)
        >>> print(f"Executions: {state.execution_count}")
        Executions: 1

        Performance analysis:

        >>> best_agent = state.get_most_successful_agent()
        >>> success_rate = state.get_total_success_rate()
        >>> print(f"Best agent: {best_agent}, Overall rate: {success_rate:.2%}")
        Best agent: writer, Overall rate: 100.00%

    Note:
        This state schema is designed to be extended by specific supervisor
        implementations. The base functionality provides comprehensive tracking
        and can be supplemented with implementation-specific fields.
    """

    # Core messaging (inherited from ReactAgent pattern)
    messages: list[BaseMessage] = Field(
        default_factory=list, description="Conversation messages"
    )

    # Supervisor-specific state
    supervisor_name: str = Field(..., description="Name of this supervisor")

    # Task management
    current_task: SupervisorTask | None = Field(
        None, description="Currently executing task"
    )
    task_history: list[SupervisorTask] = Field(
        default_factory=list, description="History of executed tasks"
    )
    results_history: list[SupervisorResult] = Field(
        default_factory=list, description="History of task results"
    )

    # Routing and decision tracking
    last_routing_decision: RoutingDecision | None = Field(
        None, description="Last routing decision made"
    )
    routing_history: list[RoutingDecision] = Field(
        default_factory=list, description="History of routing decisions"
    )

    # Agent management (basic tracking)
    registered_agent_names: list[str] = Field(
        default_factory=list, description="Names of registered agents"
    )
    active_agent_names: list[str] = Field(
        default_factory=list, description="Names of currently active agents"
    )

    # Performance tracking
    agent_performance: dict[str, AgentPerformanceMetrics] = Field(
        default_factory=dict, description="Performance metrics per agent"
    )

    # Execution context
    execution_count: int = Field(default=0, description="Total number of executions")
    last_agent_used: str | None = Field(
        None, description="Last agent that was executed"
    )

    # Error handling
    last_error: str | None = Field(None, description="Last error message if any")
    error_count: int = Field(default=0, description="Total number of errors")

    # Metadata
    supervisor_metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional supervisor metadata"
    )

    def add_task(self, task: SupervisorTask) -> None:
        """Add a task to history and set as current."""
        self.current_task = task
        self.task_history.append(task)

    def complete_task(self, result: SupervisorResult) -> None:
        """Complete current task with result."""
        self.results_history.append(result)
        self.current_task = None
        self.execution_count += 1

        # Update agent performance
        agent_name = result.agent_used
        if agent_name not in self.agent_performance:
            self.agent_performance[agent_name] = AgentPerformanceMetrics(
                agent_name=agent_name
            )

        metrics = self.agent_performance[agent_name]
        metrics.total_executions += 1
        if result.success:
            metrics.successful_executions += 1
        else:
            metrics.failed_executions += 1

        # Update average execution time
        if metrics.total_executions == 1:
            metrics.average_execution_time = result.execution_time
        else:
            # Running average
            metrics.average_execution_time = (
                metrics.average_execution_time * (metrics.total_executions - 1)
                + result.execution_time
            ) / metrics.total_executions

        metrics.last_execution = result.completed_at

    def add_routing_decision(self, decision: RoutingDecision) -> None:
        """Add routing decision to history."""
        self.last_routing_decision = decision
        self.routing_history.append(decision)

    def register_agent_name(self, agent_name: str) -> None:
        """Register an agent name."""
        if agent_name not in self.registered_agent_names:
            self.registered_agent_names.append(agent_name)
        if agent_name not in self.active_agent_names:
            self.active_agent_names.append(agent_name)

    def deactivate_agent(self, agent_name: str) -> None:
        """Deactivate an agent."""
        if agent_name in self.active_agent_names:
            self.active_agent_names.remove(agent_name)

    def activate_agent(self, agent_name: str) -> None:
        """Activate an agent."""
        if (
            agent_name in self.registered_agent_names
            and agent_name not in self.active_agent_names
        ):
            self.active_agent_names.append(agent_name)

    def set_error(self, error_message: str) -> None:
        """Set error state."""
        self.last_error = error_message
        self.error_count += 1

    def clear_error(self) -> None:
        """Clear error state."""
        self.last_error = None

    def get_agent_performance(self, agent_name: str) -> AgentPerformanceMetrics | None:
        """Get performance metrics for an agent."""
        return self.agent_performance.get(agent_name)

    def get_most_successful_agent(self) -> str | None:
        """Get the agent with highest success rate."""
        if not self.agent_performance:
            return None

        best_agent = None
        best_rate = -1.0

        for agent_name, metrics in self.agent_performance.items():
            if metrics.success_rate > best_rate:
                best_rate = metrics.success_rate
                best_agent = agent_name

        return best_agent

    def get_total_success_rate(self) -> float:
        """Get overall success rate across all agents."""
        if not self.results_history:
            return 0.0

        successful = sum(1 for r in self.results_history if r.success)
        return successful / len(self.results_history)
