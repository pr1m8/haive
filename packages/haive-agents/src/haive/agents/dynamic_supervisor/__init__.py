"""Dynamic Supervisor Agent - Runtime agent management for Haive.

This module provides a dynamic supervisor agent that can add, remove, and manage
other agents at runtime. Handoff tools execute agents directly within the tool
function, following our experimental pattern.

Classes:
    DynamicSupervisorAgent: Main supervisor agent that extends SimpleAgent
    SupervisorState: State management for dynamic agent registry
    AgentInfo: Metadata container for agent information

Example:
    Basic usage with dynamic agent management::

        from haive.agents.dynamic_supervisor import DynamicSupervisorAgent
        from haive.agents.simple import SimpleAgent

        # Create supervisor
        supervisor = DynamicSupervisorAgent(
            name="task_router",
            engine=supervisor_engine
        )

        # Add agents dynamically
        state = supervisor.create_initial_state()
        state.add_agent("search", search_agent, "Web search specialist")
        state.add_agent("math", math_agent, "Mathematics expert")

        # Run task - supervisor routes to appropriate agent
        result = await supervisor.arun("Find the population of Tokyo")

Version: 1.0.0
Author: Haive Team
"""

from haive.agents.dynamic_supervisor.agent import DynamicSupervisorAgent
from haive.agents.dynamic_supervisor.models import AgentInfo
from haive.agents.dynamic_supervisor.state import (
    SupervisorState,
    SupervisorStateV2,
    SupervisorStateWithTools,
)

__version__ = "1.0.0"
__all__ = [
    "AgentInfo",
    "DynamicSupervisorAgent",
    "SupervisorState",
    "SupervisorStateV2",
    "SupervisorStateWithTools",
]
