"""Haive Supervisor Agent Package.

Provides sophisticated multi-agent orchestration using ReactAgent patterns
with dynamic routing and intelligent agent coordination. Includes traditional
supervisor, enhanced dynamic supervisor, and integrated multi-agent supervisor
implementations with tool-based agent management.
"""

from .agent import SupervisorAgent, SupervisorState
from .dynamic_agent_tools import (
    AddAgentTool,
    AgentDescriptor,
    AgentRegistryManager,
    ChangeAgentTool,
    ListAgentsTool,
    RemoveAgentTool,
    create_agent_management_tools,
)
from .dynamic_state import (
    AgentExecutionConfig,
    AgentExecutionResult,
    DynamicSupervisorState,
    SupervisorDecision,
)
from .dynamic_supervisor import DynamicSupervisorAgent
from .integrated_supervisor import IntegratedDynamicSupervisor
from .multi_agent_dynamic_state import (
    AgentRegistryState,
    MultiAgentCoordinationState,
    MultiAgentDynamicSupervisorState,
)
from .registry import AgentRegistry

__all__ = [
    "AddAgentTool",
    # Agent management tools
    "AgentDescriptor",
    "AgentExecutionConfig",
    "AgentExecutionResult",
    "AgentRegistry",
    "AgentRegistryManager",
    "AgentRegistryState",
    "ChangeAgentTool",
    # Dynamic supervisor
    "DynamicSupervisorAgent",
    "DynamicSupervisorState",
    # Integrated multi-agent supervisor
    "IntegratedDynamicSupervisor",
    "ListAgentsTool",
    "MultiAgentCoordinationState",
    "MultiAgentDynamicSupervisorState",
    "RemoveAgentTool",
    # Traditional supervisor
    "SupervisorAgent",
    "SupervisorDecision",
    "SupervisorState",
    "create_agent_management_tools",
]
