"""Supervisor module for managing multi-agent systems.

This module provides a complete supervisor implementation that can manage
multiple agents, handle tool synchronization, and support dynamic agent creation.

Key Components:
    - BaseSupervisor: Core supervisor using ReactAgent
    - DynamicSupervisor: Extended supervisor with agent creation
    - SupervisorState: State model with agent registry
    - DynamicSupervisorState: Extended state for dynamic capabilities

Example Usage:
    Basic supervisor::

        from haive.agents.experiments.supervisor import BaseSupervisor
        from haive.agents.simple.agent import SimpleAgent

        # Create supervisor
        supervisor = BaseSupervisor(name="my_supervisor", engine=my_engine)

        # Register agents
        research_agent = SimpleAgent(name="researcher", engine=research_engine)
        supervisor.register_agent("research", "Research specialist", research_agent)

        # Use supervisor
        result = supervisor.invoke("Research quantum computing trends")

    Dynamic supervisor::

        from haive.agents.experiments.supervisor import DynamicSupervisor

        supervisor = DynamicSupervisor(name="dynamic_super", engine=my_engine)
        supervisor.enable_agent_creation()

        # Can create agents on the fly via tool calls
        result = supervisor.invoke("Create a coding agent and write Python code")
"""

from .base_supervisor import BaseSupervisor, DynamicSupervisor
from .state_models import (
    AgentMetadata,
    DynamicSupervisorState,
    ExecutionContext,
    SerializedAgent,
    SupervisorState,
    ToolMapping,
)
from .tools import (
    build_supervisor_tools,
    create_agent_creation_tool,
    create_execution_status_tool,
    create_list_agents_tool,
    create_supervisor_handoff_tool,
    sync_tools_with_state,
)

__all__ = [
    "AgentMetadata",
    # Supervisor classes
    "BaseSupervisor",
    "DynamicSupervisor",
    "DynamicSupervisorState",
    "ExecutionContext",
    "SerializedAgent",
    # State models
    "SupervisorState",
    "ToolMapping",
    "build_supervisor_tools",
    "create_agent_creation_tool",
    "create_execution_status_tool",
    "create_list_agents_tool",
    # Tool creation functions
    "create_supervisor_handoff_tool",
    "sync_tools_with_state",
]
