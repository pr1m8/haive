"""Supervisor state with agent registry and proper inheritance."""

from typing import Dict, List, Optional

from haive.core.schema.prebuilt.messages_state import MessagesState
from pydantic import Field, field_validator

from haive.agents.experiments.supervisor.agent_info import AgentInfo


class SupervisorState(MessagesState):
    """State for dynamic supervisor with agent registry.

    Inherits from MessagesState for proper message handling and adds
    agent registry and routing capabilities.
    """

    model_config = {"arbitrary_types_allowed": True}

    # Agent registry
    agents: dict[str, AgentInfo] = Field(
        default_factory=dict, description="Registry of available agents by name"
    )
    active_agents: list[str] = Field(
        default_factory=list,
        description="List of currently active agent names (unique)",
    )

    @field_validator("active_agents")
    @classmethod
    def ensure_unique_agents(cls, v: list[str]) -> list[str]:
        """Ensure active agents list contains unique values."""
        return list(set(v)) if v else []

    # Routing control
    next_agent: str | None = Field(
        default=None, description="Name of agent to execute next"
    )
    agent_task: str = Field(
        default="", description="Task to pass to the selected agent"
    )
    agent_response: str | None = Field(
        default=None, description="Response from the executed agent"
    )

    def add_agent(self, name: str, agent: any, description: str, active: bool = True):
        """Add an agent to the registry."""
        agent_info = AgentInfo(
            agent=agent, name=name, description=description, active=active
        )

        self.agents[name] = agent_info

        if active and name not in self.active_agents:
            self.active_agents.append(name)

    def remove_agent(self, name: str) -> bool:
        """Remove an agent from the registry."""
        if name in self.agents:
            del self.agents[name]
            if name in self.active_agents:
                self.active_agents.remove(name)
            return True
        return False

    def activate_agent(self, name: str) -> bool:
        """Activate an agent."""
        if name in self.agents:
            self.agents[name].activate()
            if name not in self.active_agents:
                self.active_agents.append(name)
            return True
        return False

    def deactivate_agent(self, name: str) -> bool:
        """Deactivate an agent."""
        if name in self.agents:
            self.agents[name].deactivate()
            if name in self.active_agents:
                self.active_agents.remove(name)
            return True
        return False

    def get_agent(self, name: str) -> any | None:
        """Get agent instance by name."""
        if name in self.agents:
            return self.agents[name].get_agent()
        return None

    def list_active_agents(self) -> dict[str, str]:
        """List active agents with descriptions."""
        return {
            name: info.description
            for name, info in self.agents.items()
            if info.is_active()
        }

    def list_all_agents(self) -> dict[str, str]:
        """List all agents with descriptions."""
        return {name: info.description for name, info in self.agents.items()}

    def set_routing(self, agent_name: str, task: str):
        """Set the next agent and task for execution."""
        self.next_agent = agent_name
        self.agent_task = task

    def clear_routing(self):
        """Clear routing information."""
        self.next_agent = None
        self.agent_task = ""
        self.agent_response = None
