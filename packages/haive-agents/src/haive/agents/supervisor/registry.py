"""Agent Registry for Haive Supervisor System.

Manages agent lifecycle and routing model synchronization using DynamicChoiceModel.
Provides runtime agent registration/deregistration with automatic routing updates.
"""

import logging
import time
from typing import Any, Dict, List, Optional, Set

from haive.core.common.models.dynamic_choice_model import DynamicChoiceModel
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.tree import Tree

from haive.agents.base.agent import Agent

logger = logging.getLogger(__name__)
console = Console()


class AgentRegistry:
    """Manages agent lifecycle and routing model synchronization.

    This class provides a centralized registry for managing agents in a supervisor
    system, with automatic synchronization to a DynamicChoiceModel for routing.

    Features:
        - Runtime agent registration/deregistration
        - Automatic routing model updates
        - Agent capability tracking
        - Conflict detection and resolution
        - Rich visualization of registry state
    """

    def __init__(self, routing_model: DynamicChoiceModel[str]):
        """Initialize agent registry.

        Args:
            routing_model: DynamicChoiceModel to synchronize with agent changes
        """
        self.routing_model = routing_model
        self.agents: Dict[str, Agent] = {}
        self.agent_capabilities: Dict[str, str] = {}
        self.registration_timestamps: Dict[str, float] = {}
        self._rebuild_needed = False

        logger.info("AgentRegistry initialized")

    def register(
        self, agent: Agent, capability_description: Optional[str] = None
    ) -> bool:
        """Register an agent and update routing model.

        Args:
            agent: Agent instance to register
            capability_description: Optional description of agent capabilities

        Returns:
            bool: True if registration successful, False if agent name conflict

        Raises:
            ValueError: If agent has no name or invalid configuration
        """
        if not agent.name:
            raise ValueError("Agent must have a name to be registered")

        agent_name = agent.name

        # Check for name conflicts
        if agent_name in self.agents:
            logger.warning(f"Agent '{agent_name}' already registered")
            console.print(f"[yellow]⚠️  Agent '{agent_name}' already exists[/yellow]")
            return False

        # Register agent
        self.agents[agent_name] = agent
        self.registration_timestamps[agent_name] = time.time()

        # Store capability description
        if capability_description:
            self.agent_capabilities[agent_name] = capability_description
        elif hasattr(agent, "description") and agent.description:
            self.agent_capabilities[agent_name] = agent.description
        else:
            self.agent_capabilities[agent_name] = f"Agent for {agent_name} tasks"

        # Update routing model
        self.routing_model.add_option(agent_name)
        self._rebuild_needed = True

        # Log registration
        logger.info(f"Registered agent: {agent_name}")
        console.print(f"[green]✅ Registered agent:[/green] {agent_name}")

        self._print_registration_details(agent_name, "REGISTER")

        return True

    def unregister(self, agent_name: str) -> bool:
        """Remove an agent and update routing model.

        Args:
            agent_name: Name of agent to remove

        Returns:
            bool: True if removal successful, False if agent not found
        """
        if agent_name not in self.agents:
            logger.warning(f"Agent '{agent_name}' not found for removal")
            console.print(f"[yellow]⚠️  Agent '{agent_name}' not found[/yellow]")
            return False

        # Remove agent and metadata
        del self.agents[agent_name]
        del self.registration_timestamps[agent_name]
        if agent_name in self.agent_capabilities:
            del self.agent_capabilities[agent_name]

        # Update routing model
        self.routing_model.remove_option_by_name(agent_name)
        self._rebuild_needed = True

        # Log removal
        logger.info(f"Unregistered agent: {agent_name}")
        console.print(f"[red]❌ Unregistered agent:[/red] {agent_name}")

        self._print_registration_details(agent_name, "UNREGISTER")

        return True

    def get_agent(self, name: str) -> Optional[Agent]:
        """Get agent by name.

        Args:
            name: Agent name

        Returns:
            Agent instance or None if not found
        """
        return self.agents.get(name)

    def get_available_agents(self) -> List[str]:
        """Get list of currently available agent names.

        Returns:
            List of agent names available for routing
        """
        return list(self.agents.keys())

    def get_routing_options(self) -> List[str]:
        """Get all routing options including END.

        Returns:
            List of all valid routing choices
        """
        return self.routing_model.option_names

    def get_agent_capabilities(self) -> Dict[str, str]:
        """Get mapping of agent names to their capabilities.

        Returns:
            Dict mapping agent names to capability descriptions
        """
        return self.agent_capabilities.copy()

    def get_agent_capability(self, agent_name: str) -> Optional[str]:
        """Get capability description for specific agent.

        Args:
            agent_name: Name of agent

        Returns:
            Capability description or None if agent not found
        """
        return self.agent_capabilities.get(agent_name)

    def is_agent_registered(self, agent_name: str) -> bool:
        """Check if agent is registered.

        Args:
            agent_name: Agent name to check

        Returns:
            True if agent is registered, False otherwise
        """
        return agent_name in self.agents

    def get_agent_count(self) -> int:
        """Get number of registered agents.

        Returns:
            Number of currently registered agents
        """
        return len(self.agents)

    def needs_rebuild(self) -> bool:
        """Check if supervisor graph needs rebuilding.

        Returns:
            True if agents have been added/removed since last check
        """
        return self._rebuild_needed

    def mark_rebuilt(self) -> None:
        """Mark that supervisor graph has been rebuilt."""
        self._rebuild_needed = False

    def validate_routing_choice(self, choice: str) -> bool:
        """Validate if a routing choice is valid.

        Args:
            choice: Routing choice to validate

        Returns:
            True if choice is valid, False otherwise
        """
        return self.routing_model.validate_choice(choice)

    def clear_all(self) -> None:
        """Remove all registered agents.

        Warning: This will clear the entire registry!
        """
        agent_names = list(self.agents.keys())

        for agent_name in agent_names:
            self.unregister(agent_name)

        logger.info("Cleared all agents from registry")
        console.print("[red]🗑️  Cleared all agents from registry[/red]")

    def _print_registration_details(self, agent_name: str, action: str) -> None:
        """Print detailed registration information.

        Args:
            agent_name: Name of affected agent
            action: Action performed (REGISTER/UNREGISTER)
        """
        action_color = "green" if action == "REGISTER" else "red"
        action_emoji = "➕" if action == "REGISTER" else "➖"

        tree = Tree(
            f"{action_emoji} [bold {action_color}]{action} Operation[/bold {action_color}]"
        )

        # Operation details
        op_branch = tree.add("📋 Operation Details")
        op_branch.add(f"Action: {action}")
        op_branch.add(f"Agent: {agent_name}")

        if action == "REGISTER" and agent_name in self.agent_capabilities:
            op_branch.add(f"Capability: {self.agent_capabilities[agent_name]}")

        # Current state
        state_branch = tree.add("🔄 Current State")
        state_branch.add(f"Total Agents: {len(self.agents)}")
        state_branch.add(f"Routing Options: {len(self.routing_model.option_names)}")

        if self.agents:
            agents_branch = state_branch.add("Active Agents")
            for name in sorted(self.agents.keys()):
                timestamp = self.registration_timestamps.get(name, 0)
                agents_branch.add(f"🤖 {name} (registered: {time.ctime(timestamp)})")

        console.print(Panel(tree, title="Registry Update", expand=False))

    def print_registry_state(self) -> None:
        """Print comprehensive registry state information."""
        table = Table(title="🔍 Agent Registry State")
        table.add_column("Property", style="cyan", no_wrap=True)
        table.add_column("Value", style="green")

        table.add_row("Total Agents", str(len(self.agents)))
        table.add_row("Routing Options", str(len(self.routing_model.option_names)))
        table.add_row("Rebuild Needed", str(self._rebuild_needed))

        if self.agents:
            agent_list = ", ".join(sorted(self.agents.keys()))
            table.add_row("Registered Agents", agent_list)

        # Routing model info
        table.add_row("Current Model", self.routing_model.current_model.__name__)
        table.add_row("Include END", str(self.routing_model.include_end))

        console.print(table)

        # Show capabilities if available
        if self.agent_capabilities:
            cap_table = Table(title="🎯 Agent Capabilities")
            cap_table.add_column("Agent", style="cyan")
            cap_table.add_column("Capability", style="green")

            for agent_name, capability in self.agent_capabilities.items():
                cap_table.add_row(agent_name, capability)

            console.print(cap_table)

    def get_registry_stats(self) -> Dict[str, Any]:
        """Get registry statistics.

        Returns:
            Dictionary with registry statistics
        """
        return {
            "total_agents": len(self.agents),
            "routing_options": len(self.routing_model.option_names),
            "rebuild_needed": self._rebuild_needed,
            "registered_agents": list(self.agents.keys()),
            "oldest_registration": (
                min(self.registration_timestamps.values())
                if self.registration_timestamps
                else None
            ),
            "newest_registration": (
                max(self.registration_timestamps.values())
                if self.registration_timestamps
                else None
            ),
        }
