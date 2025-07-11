"""State schemas for dynamic supervisor agent.

This module defines the state management for the dynamic supervisor, including
agent registry, routing control, and tool generation. Two versions are provided:
- SupervisorState: Uses exclude=True for agent serialization (v1)
- SupervisorStateV2: Attempts full agent serialization (experimental)

Classes:
    SupervisorState: Base supervisor state with agent registry
    SupervisorStateWithTools: Extends base with dynamic tool generation
    SupervisorStateV2: Experimental version with full serialization

Example:
    Creating and managing supervisor state::

        state = SupervisorState()
        state.add_agent("search", search_agent, "Search specialist")
        state.activate_agent("search")

        # List active agents
        active = state.list_active_agents()
"""

from typing import Any, Dict, List, Optional

from haive.core.common.models.dynamic_choice_model import DynamicChoiceModel
from haive.core.schema.prebuilt.messages.messages_with_token_usage import (
    MessagesStateWithTokenUsage,
)
from langchain_core.messages import BaseMessage
from pydantic import Field, field_validator, model_validator

from haive.agents.dynamic_supervisor.models import AgentInfo, AgentInfoV2
from haive.agents.dynamic_supervisor.tools import create_agent_tools


class SupervisorState(MessagesStateWithTokenUsage):
    """Base state for dynamic supervisor with agent registry.

    Inherits from MessagesState for message handling and adds agent management
    capabilities. Agents are stored in a registry with metadata for routing.

    Attributes:
        agents: Registry of available agents by name
        active_agents: List of currently active agent names (unique)
        next_agent: Name of agent to execute next (routing control)
        agent_task: Task to pass to the selected agent
        agent_response: Response from the last executed agent

    Example:
        Basic agent management::

            state = SupervisorState()
            state.add_agent("math", math_agent, "Math specialist")
            state.set_routing("math", "Calculate 2+2")
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

    # Execution tracking
    last_executed_agent: str | None = Field(
        default=None, description="Name of the last executed agent"
    )
    agent_response: str | None = Field(
        default=None, description="Response from the last executed agent"
    )
    execution_success: bool = Field(
        default=True, description="Whether the last agent execution was successful"
    )

    @field_validator("active_agents")
    @classmethod
    def ensure_unique_agents(cls, v: list[str]) -> list[str]:
        """Ensure active agents list contains unique values.

        Args:
            v: List of agent names

        Returns:
            List with duplicates removed
        """
        return list(dict.fromkeys(v)) if v else []

    def add_agent(
        self, name: str, agent: Any, description: str, active: bool = True
    ) -> None:
        """Add an agent to the registry.

        Args:
            name: Unique identifier for the agent
            agent: The agent instance
            description: Human-readable description of agent capabilities
            active: Whether agent should be immediately active

        Example:
            state.add_agent("search", search_agent, "Web search expert", active=True)
        """
        agent_info = AgentInfo(
            agent=agent, name=name, description=description, active=active
        )

        self.agents[name] = agent_info

        if active and name not in self.active_agents:
            self.active_agents.append(name)

    def remove_agent(self, name: str) -> bool:
        """Remove an agent from the registry completely.

        Args:
            name: Agent name to remove

        Returns:
            True if agent was removed, False if not found
        """
        if name in self.agents:
            del self.agents[name]
            if name in self.active_agents:
                self.active_agents.remove(name)
            return True
        return False

    def activate_agent(self, name: str) -> bool:
        """Activate an inactive agent.

        Args:
            name: Agent name to activate

        Returns:
            True if agent was activated, False if not found
        """
        if name in self.agents:
            self.agents[name].activate()
            if name not in self.active_agents:
                self.active_agents.append(name)
            return True
        return False

    def deactivate_agent(self, name: str) -> bool:
        """Deactivate an active agent.

        Args:
            name: Agent name to deactivate

        Returns:
            True if agent was deactivated, False if not found
        """
        if name in self.agents:
            self.agents[name].deactivate()
            if name in self.active_agents:
                self.active_agents.remove(name)
            return True
        return False

    def get_agent(self, name: str) -> Any | None:
        """Get agent instance by name.

        Args:
            name: Agent name

        Returns:
            Agent instance or None if not found
        """
        if name in self.agents:
            return self.agents[name].get_agent()
        return None

    def list_active_agents(self) -> dict[str, str]:
        """List all active agents with descriptions.

        Returns:
            Dict mapping agent names to descriptions
        """
        return {
            name: info.description
            for name, info in self.agents.items()
            if info.is_active()
        }

    def list_all_agents(self) -> dict[str, str]:
        """List all agents (active and inactive) with descriptions.

        Returns:
            Dict mapping agent names to descriptions
        """
        return {name: info.description for name, info in self.agents.items()}

    def clear_execution_state(self) -> None:
        """Clear execution state after completion."""
        self.last_executed_agent = None
        self.agent_response = None
        self.execution_success = True


class SupervisorStateWithTools(SupervisorState):
    """Supervisor state with dynamic tool generation.

    Extends SupervisorState with automatic tool generation from registered agents.
    Creates handoff tools for each agent and manages a dynamic choice model.

    Attributes:
        agent_choice_model: Dynamic model for validated agent selection
        generated_tools: List of tool names generated from agents

    Example:
        Using dynamic tools::

            state = SupervisorStateWithTools()
            state.add_agent("search", agent, "Search expert")
            state.sync_agents()  # Generates handoff_to_search tool

            tools = state.get_all_tools()  # Get tool instances
    """

    # Choice model for validation
    agent_choice_model: DynamicChoiceModel = Field(
        default_factory=lambda: DynamicChoiceModel(
            model_name="AgentChoice", include_end=True
        ),
        description="Dynamic choice model for agent selection validation",
    )

    # Generated tools tracking
    generated_tools: list[str] = Field(
        default_factory=list, description="Names of tools generated from agents"
    )

    @model_validator(mode="after")
    def sync_on_init(self):
        """Sync tools and choice model after initialization."""
        self._sync_internal()
        return self

    def sync_agents(self) -> None:
        """Public method to sync agents with tools and choice model.

        Call this after adding/removing agents to regenerate tools.
        """
        self._sync_internal()

    def _sync_internal(self) -> None:
        """Internal sync method."""
        self._update_choice_model()
        self._generate_tools_from_agents()

    def _update_choice_model(self) -> None:
        """Update choice model with current agents."""
        # Get current options (excluding END)
        current_options = [
            opt for opt in self.agent_choice_model.option_names if opt != "END"
        ]

        # Remove options that are no longer in agents
        for option in current_options:
            if option not in self.agents:
                self.agent_choice_model.remove_option_by_name(option)

        # Add new agents
        for agent_name in self.agents:
            if agent_name not in self.agent_choice_model.option_names:
                self.agent_choice_model.add_option(agent_name)

    def _generate_tools_from_agents(self) -> None:
        """Generate tools from current agents."""
        self.generated_tools.clear()

        # Create handoff tools for each agent
        for agent_name, _agent_info in self.agents.items():
            tool_name = f"handoff_to_{agent_name}"
            self.generated_tools.append(tool_name)

        # Add choice validation tool
        self.generated_tools.append("choose_agent")

    def get_all_tools(self) -> list[Any]:
        """Get all generated tools as callable instances.

        Returns:
            List of tool instances ready for use
        """
        return create_agent_tools(self)

    def add_agent(
        self, name: str, agent: Any, description: str, active: bool = True
    ) -> None:
        """Override to trigger tool regeneration."""
        super().add_agent(name, agent, description, active)
        self._sync_internal()

    def remove_agent(self, name: str) -> bool:
        """Override to trigger tool regeneration."""
        result = super().remove_agent(name)
        if result:
            self._sync_internal()
        return result

    def activate_agent(self, name: str) -> bool:
        """Override to trigger tool regeneration."""
        result = super().activate_agent(name)
        if result:
            self._sync_internal()
        return result

    def deactivate_agent(self, name: str) -> bool:
        """Override to trigger tool regeneration."""
        result = super().deactivate_agent(name)
        if result:
            self._sync_internal()
        return result


# Version 2: Experimental full serialization
class SupervisorStateV2(MessagesStateWithTokenUsage):
    """Experimental supervisor state with full agent serialization.

    This version attempts to serialize agents fully rather than excluding them.
    May require custom serialization logic or agent reconstruction.

    Warning:
        This is experimental and may not work with all agent types or
        checkpointing systems. Use SupervisorState for production.
    """

    model_config = {"arbitrary_types_allowed": True}

    # Using V2 agent info that doesn't exclude agents
    agents: dict[str, AgentInfoV2] = Field(
        default_factory=dict,
        description="Registry of available agents (serializable version)",
    )

    # Rest of the implementation would be similar to SupervisorState
    # but with custom serialization handling...
