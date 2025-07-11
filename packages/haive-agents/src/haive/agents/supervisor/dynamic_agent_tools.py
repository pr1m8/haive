"""Dynamic Agent Management Tools for Supervisor.

This module provides tools that allow the supervisor to dynamically add, remove,
and manage agents at runtime through tool calls, integrating with DynamicChoiceModel
for routing and state management.
"""

import logging
from typing import Any, Dict, List, Optional

from haive.core.common.models.dynamic_choice_model import DynamicChoiceModel
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from rich.console import Console

from haive.agents.base.agent import Agent

logger = logging.getLogger(__name__)
console = Console()


class AgentDescriptor(BaseModel):
    """Descriptor for an agent that can be dynamically added."""

    name: str = Field(description="Unique agent name")
    agent_type: str = Field(description="Type of agent (SimpleAgent, ReactAgent, etc.)")
    capability_description: str = Field(description="What this agent is capable of")
    priority: int = Field(
        default=1, description="Agent priority (higher = more preferred)"
    )
    tools: list[str] = Field(
        default_factory=list, description="List of tool names this agent has"
    )
    config: dict[str, Any] = Field(
        default_factory=dict, description="Agent configuration"
    )


class AddAgentInput(BaseModel):
    """Input for adding a new agent to the supervisor."""

    agent_descriptor: AgentDescriptor = Field(description="Descriptor of agent to add")
    rebuild_graph: bool = Field(
        default=True, description="Whether to rebuild supervisor graph"
    )


class RemoveAgentInput(BaseModel):
    """Input for removing an agent from the supervisor."""

    agent_name: str = Field(description="Name of agent to remove")
    rebuild_graph: bool = Field(
        default=True, description="Whether to rebuild supervisor graph"
    )


class ChangeAgentInput(BaseModel):
    """Input for changing/updating an existing agent."""

    agent_name: str = Field(description="Name of agent to change")
    updates: dict[str, Any] = Field(
        description="Updates to apply to agent configuration"
    )


class ListAgentsInput(BaseModel):
    """Input for listing available agents."""

    include_performance: bool = Field(
        default=True, description="Include performance metrics"
    )


class AgentRegistryManager:
    """Manages dynamic agent registry with tool integration."""

    def __init__(self, supervisor_agent):
        """Initialize with supervisor agent reference."""
        self.supervisor = supervisor_agent
        self.choice_model = DynamicChoiceModel[str](
            options=[], model_name="AgentChoice", include_end=True
        )

        # Registry of available agent constructors (for testing)
        self.agent_constructors = {}

    def register_agent_constructor(self, agent_type: str, constructor):
        """Register an agent constructor function."""
        self.agent_constructors[agent_type] = constructor
        logger.info(f"Registered agent constructor: {agent_type}")

    def create_agent_from_descriptor(self, descriptor: AgentDescriptor) -> Agent | None:
        """Create an agent instance from descriptor."""
        constructor = self.agent_constructors.get(descriptor.agent_type)
        if not constructor:
            logger.error(
                f"No constructor registered for agent type: {descriptor.agent_type}"
            )
            return None

        try:
            # Create agent with descriptor config
            agent = constructor(name=descriptor.name, **descriptor.config)

            logger.info(f"Created agent: {descriptor.name} ({descriptor.agent_type})")
            return agent

        except Exception as e:
            logger.exception(f"Failed to create agent {descriptor.name}: {e}")
            return None

    def get_agent_choice_model(self) -> DynamicChoiceModel[str]:
        """Get current agent choice model."""
        # Update choice model with current agents
        current_agents = self.supervisor.agent_registry.get_available_agents()

        # Clear and rebuild options
        self.choice_model.options = current_agents.copy()
        self.choice_model._regenerate_model()

        return self.choice_model


class AddAgentTool(BaseTool):
    """Tool for dynamically adding agents to the supervisor."""

    name: str = "add_agent"
    description: str = """Add a new agent to the supervisor's registry.
    This allows the supervisor to route requests to the new agent."""
    args_schema = AddAgentInput

    def __init__(self, registry_manager: AgentRegistryManager):
        super().__init__()
        self.registry_manager = registry_manager

    async def _arun(
        self, agent_descriptor: AgentDescriptor, rebuild_graph: bool = True
    ) -> str:
        """Add agent asynchronously."""
        try:
            # Create agent from descriptor
            agent = self.registry_manager.create_agent_from_descriptor(agent_descriptor)
            if not agent:
                return f"Failed to create agent: {agent_descriptor.name}"

            # Register with supervisor
            execution_config = {
                "priority": agent_descriptor.priority,
                **agent_descriptor.config,
            }

            success = await self.registry_manager.supervisor.register_agent(
                agent,
                capability_description=agent_descriptor.capability_description,
                execution_config=execution_config,
                rebuild_graph=rebuild_graph,
            )

            if success:
                # Update choice model
                self.registry_manager.get_agent_choice_model()
                return f"Successfully added agent: {agent_descriptor.name}"
            return f"Failed to register agent: {agent_descriptor.name}"

        except Exception as e:
            logger.exception(f"Error adding agent: {e}")
            return f"Error adding agent: {e!s}"

    def _run(
        self, agent_descriptor: AgentDescriptor, rebuild_graph: bool = True
    ) -> str:
        """Synchronous version - not implemented for async supervisor."""
        return "This tool requires async execution"


class RemoveAgentTool(BaseTool):
    """Tool for dynamically removing agents from the supervisor."""

    name: str = "remove_agent"
    description: str = """Remove an agent from the supervisor's registry.
    The agent will no longer be available for routing."""
    args_schema = RemoveAgentInput

    def __init__(self, registry_manager: AgentRegistryManager):
        super().__init__()
        self.registry_manager = registry_manager

    async def _arun(self, agent_name: str, rebuild_graph: bool = True) -> str:
        """Remove agent asynchronously."""
        try:
            success = await self.registry_manager.supervisor.unregister_agent(
                agent_name, rebuild_graph=rebuild_graph
            )

            if success:
                # Update choice model
                self.registry_manager.get_agent_choice_model()
                return f"Successfully removed agent: {agent_name}"
            return f"Agent not found or failed to remove: {agent_name}"

        except Exception as e:
            logger.exception(f"Error removing agent: {e}")
            return f"Error removing agent: {e!s}"

    def _run(self, agent_name: str, rebuild_graph: bool = True) -> str:
        """Synchronous version - not implemented for async supervisor."""
        return "This tool requires async execution"


class ChangeAgentTool(BaseTool):
    """Tool for updating agent configuration."""

    name: str = "change_agent"
    description: str = """Update configuration of an existing agent.
    Can modify priority, timeout, and other execution parameters."""
    args_schema = ChangeAgentInput

    def __init__(self, registry_manager: AgentRegistryManager):
        super().__init__()
        self.registry_manager = registry_manager

    async def _arun(self, agent_name: str, updates: dict[str, Any]) -> str:
        """Change agent configuration asynchronously."""
        try:
            success = await self.registry_manager.supervisor.update_agent_config(
                agent_name, updates
            )

            if success:
                return f"Successfully updated agent: {agent_name}"
            return f"Agent not found or failed to update: {agent_name}"

        except Exception as e:
            logger.exception(f"Error updating agent: {e}")
            return f"Error updating agent: {e!s}"

    def _run(self, agent_name: str, updates: dict[str, Any]) -> str:
        """Synchronous version - not implemented for async supervisor."""
        return "This tool requires async execution"


class ListAgentsTool(BaseTool):
    """Tool for listing available agents and their capabilities."""

    name: str = "list_agents"
    description: str = """List all available agents in the supervisor registry
    with their capabilities and performance metrics."""
    args_schema = ListAgentsInput

    def __init__(self, registry_manager: AgentRegistryManager):
        super().__init__()
        self.registry_manager = registry_manager

    async def _arun(self, include_performance: bool = True) -> str:
        """List agents asynchronously."""
        try:
            supervisor = self.registry_manager.supervisor
            available_agents = supervisor.agent_registry.get_available_agents()

            if not available_agents:
                return "No agents currently registered"

            agent_info = []
            for agent_name in available_agents:
                capability = supervisor.agent_registry.get_agent_capability(agent_name)
                info = f"- {agent_name}: {capability}"

                if (
                    include_performance
                    and hasattr(supervisor, "_state")
                    and supervisor._state
                ):
                    performance = supervisor._state.get_agent_performance(agent_name)
                    if performance.get("executions", 0) > 0:
                        success_rate = performance.get("success_rate", 0.0) * 100
                        info += f" (Success: {success_rate:.1f}%, Executions: {performance.get('executions', 0)})"

                agent_info.append(info)

            return f"Available agents ({len(available_agents)}):\n" + "\n".join(
                agent_info
            )

        except Exception as e:
            logger.exception(f"Error listing agents: {e}")
            return f"Error listing agents: {e!s}"

    def _run(self, include_performance: bool = True) -> str:
        """Synchronous version - not implemented for async supervisor."""
        return "This tool requires async execution"


class AgentSelectorTool(BaseTool):
    """Tool for selecting which agent to use for the next task."""

    name: str = "select_agent"
    description: str = """Select a specific agent to handle the next user request.
    Use this when you want to explicitly route to a particular agent."""

    def __init__(self, registry_manager: AgentRegistryManager):
        super().__init__()
        self.registry_manager = registry_manager

        # Create dynamic args schema based on available agents
        self._update_args_schema()

    def _update_args_schema(self):
        """Update args schema with current agent choices."""
        choice_model = self.registry_manager.get_agent_choice_model()
        self.args_schema = choice_model.current_model

    async def _arun(self, choice: str) -> str:
        """Select agent asynchronously."""
        try:
            if (
                not self.registry_manager.supervisor.agent_registry.is_agent_registered(
                    choice
                )
                and choice != "END"
            ):
                return f"Agent not found: {choice}"

            # This tool doesn't actually change state, just validates the choice
            # The routing will be handled by the supervisor's decision logic
            return f"Agent selected: {choice}"

        except Exception as e:
            logger.exception(f"Error selecting agent: {e}")
            return f"Error selecting agent: {e!s}"

    def _run(self, choice: str) -> str:
        """Synchronous version - not implemented for async supervisor."""
        return "This tool requires async execution"


def create_agent_management_tools(supervisor_agent) -> list[BaseTool]:
    """Create all agent management tools for a supervisor."""
    registry_manager = AgentRegistryManager(supervisor_agent)

    # Register some basic agent constructors for testing
    try:
        from haive.agents.react.agent import ReactAgent
        from haive.agents.simple.agent import SimpleAgent

        registry_manager.register_agent_constructor("SimpleAgent", SimpleAgent)
        registry_manager.register_agent_constructor("ReactAgent", ReactAgent)

    except ImportError as e:
        logger.warning(f"Could not import agent classes: {e}")

    tools = [
        AddAgentTool(registry_manager),
        RemoveAgentTool(registry_manager),
        ChangeAgentTool(registry_manager),
        ListAgentsTool(registry_manager),
        AgentSelectorTool(registry_manager),
    ]

    return tools


def register_agent_constructor(supervisor_agent, agent_type: str, constructor):
    """Register an agent constructor with the supervisor's registry manager."""
    # This would need to be called on the registry manager
    # For now, this is a placeholder for the integration pattern
