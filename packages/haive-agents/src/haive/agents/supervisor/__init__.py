"""Haive Supervisor Agent Package

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
    # Traditional supervisor
    "SupervisorAgent",
    "SupervisorState",
    "AgentRegistry",
    # Dynamic supervisor
    "DynamicSupervisorAgent",
    "DynamicSupervisorState",
    "AgentExecutionConfig",
    "AgentExecutionResult",
    "SupervisorDecision",
    # Integrated multi-agent supervisor
    "IntegratedDynamicSupervisor",
    "MultiAgentDynamicSupervisorState",
    "AgentRegistryState",
    "MultiAgentCoordinationState",
    # Agent management tools
    "AgentDescriptor",
    "AgentRegistryManager",
    "AddAgentTool",
    "RemoveAgentTool",
    "ChangeAgentTool",
    "ListAgentsTool",
    "create_agent_management_tools",
]
