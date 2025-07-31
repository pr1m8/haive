"""Base data models for supervisor agents.

This module provides common data models and schemas used across all supervisor
implementations for agent management and coordination.

The models in this module support:
    - Agent metadata tracking with performance metrics
    - Task and result management with execution history
    - Routing decisions with confidence scoring
    - Configuration management for supervisor behavior

Example:
    Creating agent info for registration:

    >>> from haive.agents.supervisor_new.base.models import AgentInfo
    >>> agent_info = AgentInfo(
    ...     name="research_agent",
    ...     description="Specialized in web research and analysis",
    ...     agent_class="ResearchAgent",
    ...     capabilities=["web_search", "data_analysis", "summarization"]
    ... )
    >>> print(f"Agent: {agent_info.name}, Active: {agent_info.is_active}")
    Agent: research_agent, Active: True

    Tracking task execution:

    >>> from haive.agents.supervisor_new.base.models import SupervisorTask, SupervisorResult
    >>> task = SupervisorTask(
    ...     task_id="task_001",
    ...     content="Research climate change impacts",
    ...     target_agent="research_agent",
    ...     priority=8
    ... )
    >>> result = SupervisorResult(
    ...     task_id=task.task_id,
    ...     agent_used="research_agent",
    ...     result="Climate change impacts include...",
    ...     execution_time=2.5,
    ...     success=True
    ... )
    >>> print(f"Task completed in {result.execution_time}s: {result.success}")
    Task completed in 2.5s: True
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class AgentInfo(BaseModel):
    """Information about a registered agent in supervisor.

    This is the base model for tracking agent metadata across different
    supervisor implementations. It provides comprehensive tracking of
    agent capabilities, performance, and usage patterns.

    Attributes:
        name (str): Unique agent identifier within the supervisor.
        description (str): Human-readable description of agent capabilities.
        agent_class (str): Name of the agent's Python class.
        capabilities (List[str]): List of specific capabilities this agent provides.
        is_active (bool): Whether the agent is currently active and available.
        created_at (datetime): When this agent was registered with the supervisor.
        last_used (Optional[datetime]): When this agent was last executed.
        usage_count (int): Total number of times this agent has been used.

    Examples:
        Creating agent info for a research specialist:

        >>> agent_info = AgentInfo(
        ...     name="research_specialist",
        ...     description="Expert in academic research and data analysis",
        ...     agent_class="ResearchAgent",
        ...     capabilities=["literature_search", "data_analysis", "citation_formatting"]
        ... )
        >>> print(f"Created: {agent_info.name} ({agent_info.agent_class})")
        Created: research_specialist (ResearchAgent)

        Tracking usage over time:

        >>> agent_info.usage_count += 1
        >>> agent_info.last_used = datetime.now()
        >>> print(f"Usage: {agent_info.usage_count} times")
        Usage: 1 times

    Note:
        The `created_at` field is automatically set to the current time when
        the AgentInfo instance is created. Performance tracking should be
        handled through the `usage_count` and `last_used` fields.
    """

    name: str = Field(..., description="Unique agent identifier")
    description: str = Field(..., description="Agent description for routing")
    agent_class: str = Field(..., description="Agent class name")
    capabilities: list[str] = Field(
        default_factory=list, description="List of agent capabilities"
    )
    is_active: bool = Field(default=True, description="Whether agent is active")
    created_at: datetime = Field(default_factory=datetime.now)
    last_used: datetime | None = Field(None, description="Last execution time")
    usage_count: int = Field(default=0, description="Number of times used")

    class Config:
        """Pydantic config."""

        json_encoders = {datetime: lambda v: v.isoformat()}


class SupervisorTask(BaseModel):
    """Represents a task to be executed by supervisor.

    This model encapsulates all information about a task that needs to be
    routed and executed by the supervisor system. It includes task content,
    routing preferences, context, and metadata for tracking.

    Attributes:
        task_id (str): Unique identifier for this task.
        content (str): The actual task content or description.
        target_agent (Optional[str]): Preferred agent name for execution.
        context (Dict[str, Any]): Additional context data for the task.
        priority (int): Task priority level from 1 (lowest) to 10 (highest).
        created_at (datetime): When this task was created.

    Examples:
        Creating a high-priority research task:

        >>> task = SupervisorTask(
        ...     task_id="research_001",
        ...     content="Analyze recent developments in quantum computing",
        ...     target_agent="research_agent",
        ...     context={"domain": "technology", "depth": "detailed"},
        ...     priority=9
        ... )
        >>> print(f"Task {task.task_id}: Priority {task.priority}")
        Task research_001: Priority 9

        Creating a general task without agent preference:

        >>> task = SupervisorTask(
        ...     task_id="general_001",
        ...     content="Write a summary of the quarterly report"
        ... )
        >>> print(f"No target agent: {task.target_agent is None}")
        No target agent: True
    """

    task_id: str = Field(..., description="Unique task identifier")
    content: str = Field(..., description="Task content/description")
    target_agent: str | None = Field(None, description="Preferred agent")
    context: dict[str, Any] = Field(
        default_factory=dict, description="Additional task context"
    )
    priority: int = Field(default=1, description="Task priority (1-10)")
    created_at: datetime = Field(default_factory=datetime.now)


class SupervisorResult(BaseModel):
    """Result from supervisor task execution."""

    task_id: str = Field(..., description="Original task ID")
    agent_used: str = Field(..., description="Agent that executed task")
    result: Any = Field(..., description="Execution result")
    execution_time: float = Field(..., description="Execution time in seconds")
    success: bool = Field(..., description="Whether execution succeeded")
    error_message: str | None = Field(None, description="Error if failed")
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional result metadata"
    )
    completed_at: datetime = Field(default_factory=datetime.now)


class RoutingDecision(BaseModel):
    """Decision made by supervisor routing logic."""

    selected_agent: str = Field(..., description="Selected agent name")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Routing confidence")
    reasoning: str = Field(..., description="Why this agent was selected")
    alternatives: list[str] = Field(
        default_factory=list, description="Alternative agents considered"
    )
    routing_method: str = Field(..., description="Method used for routing")


class AgentPerformanceMetrics(BaseModel):
    """Performance metrics for an agent."""

    agent_name: str = Field(..., description="Agent name")
    total_executions: int = Field(default=0)
    successful_executions: int = Field(default=0)
    failed_executions: int = Field(default=0)
    average_execution_time: float = Field(default=0.0)
    last_execution: datetime | None = Field(None)

    @property
    def success_rate(self) -> float:
        """Calculate success rate."""
        if self.total_executions == 0:
            return 0.0
        return self.successful_executions / self.total_executions

    @property
    def failure_rate(self) -> float:
        """Calculate failure rate."""
        return 1.0 - self.success_rate


class SupervisorConfig(BaseModel):
    """Configuration for supervisor behavior."""

    name: str = Field(..., description="Supervisor name")
    max_iterations: int = Field(default=10, description="Max iterations for ReactAgent")
    routing_strategy: str = Field(default="llm", description="Routing strategy")
    enable_performance_tracking: bool = Field(default=True)
    auto_retry_on_failure: bool = Field(default=True)
    max_retries: int = Field(default=2)
    timeout_seconds: float | None = Field(None, description="Task timeout")

    # Tool configuration
    enable_dynamic_tools: bool = Field(default=True)
    tool_prefix_format: str = Field(default="{agent_name}_{tool_name}")

    # Logging configuration
    log_level: str = Field(default="INFO")
    log_executions: bool = Field(default=True)
    log_routing_decisions: bool = Field(default=False)
