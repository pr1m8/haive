"""Base components for supervisor agents.

This module provides the foundational components that all supervisor
implementations build upon.

The base module includes:
    - BaseSupervisor: Core supervisor agent class extending ReactAgent
    - BaseSupervisorState: State schema with task and performance tracking
    - Data models: AgentInfo, SupervisorTask, SupervisorResult, etc.
    - Prompt templates: System prompts and routing templates
    - Tool factory: Dynamic tool creation and management utilities

Example:
    Basic supervisor setup:

    >>> from haive.agents.supervisor_new.base import BaseSupervisor, SupervisorConfig
    >>> from haive.core.engine.aug_llm import AugLLMConfig
    >>>
    >>> config = SupervisorConfig(name="coordinator", max_iterations=5)
    >>> engine = AugLLMConfig(temperature=0.7)
    >>> supervisor = BaseSupervisor(name="coordinator", engine=engine, config=config)

    Agent registration and management:

    >>> from haive.agents.simple import SimpleAgent
    >>> agent = SimpleAgent(name="helper", engine=engine)
    >>> supervisor.register_agent("helper", agent, "General purpose assistant")
    >>> agents = supervisor.list_agents()
    >>> print(f"Registered agents: {list(agents.keys())}")
    Registered agents: ['helper']
"""

from haive.agents.supervisor_new.base.agent import BaseSupervisor
from haive.agents.supervisor_new.base.models import (
    AgentInfo,
    AgentPerformanceMetrics,
    RoutingDecision,
    SupervisorConfig,
    SupervisorResult,
    SupervisorTask,
)
from haive.agents.supervisor_new.base.prompts import (
    BaseSupervisorPrompts,
    CoordinationPrompts,
    RoutingPrompts,
    create_system_prompt,
    format_agent_capabilities,
    format_agent_list,
)
from haive.agents.supervisor_new.base.state import BaseSupervisorState
from haive.agents.supervisor_new.base.tools import (
    SupervisorToolFactory,
    create_end_supervision_tool,
    create_forward_message_tool,
    create_get_agent_info_tool,
    create_get_performance_stats_tool,
    create_handoff_tool,
    create_list_agents_tool,
)

__all__ = [
    # Core classes
    "BaseSupervisor",
    "BaseSupervisorState",
    # Models
    "AgentInfo",
    "SupervisorTask",
    "SupervisorResult",
    "RoutingDecision",
    "AgentPerformanceMetrics",
    "SupervisorConfig",
    # Prompts
    "BaseSupervisorPrompts",
    "RoutingPrompts",
    "CoordinationPrompts",
    "format_agent_list",
    "format_agent_capabilities",
    "create_system_prompt",
    # Tools
    "SupervisorToolFactory",
    "create_list_agents_tool",
    "create_forward_message_tool",
    "create_end_supervision_tool",
    "create_get_agent_info_tool",
    "create_get_performance_stats_tool",
    "create_handoff_tool",
]
