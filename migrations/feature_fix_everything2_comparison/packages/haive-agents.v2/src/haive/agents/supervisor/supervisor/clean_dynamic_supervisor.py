"""Clean_Dynamic_Supervisor core module.

This module provides clean dynamic supervisor functionality for the Haive framework.

Classes:
    DynamicSupervisorState: DynamicSupervisorState implementation.
    DynamicSupervisor: DynamicSupervisor implementation.

Functions:
    setup_agent: Setup Agent functionality.
    add_agent: Add Agent functionality.
"""

# src/haive/agents/supervisor/clean_dynamic_supervisor.py

"""Clean Dynamic Supervisor Implementation.

A dynamic supervisor that can add/remove agents at runtime and
adapt routing based on agent capabilities.
"""

import logging
from typing import Any

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.node.agent_node_v3 import AgentNodeV3Config
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from langchain_core.tools import tool
from langgraph.graph import END
from pydantic import BaseModel, Field

from haive.agents.base import Agent
from haive.agents.react.agent import ReactAgent

logger = logging.getLogger(__name__)


class DynamicSupervisorState(BaseModel):
    """Enhanced state for dynamic supervisor."""

    messages: list[Any] = Field(default_factory=list)
    registered_agents: dict[str, Agent] = Field(default_factory=dict)
    agent_capabilities: dict[str, str] = Field(default_factory=dict)
    routing_history: list[dict[str, Any]] = Field(default_factory=list)
    needs_rebuild: bool = Field(default=False)


class DynamicSupervisor(ReactAgent):
    """Dynamic supervisor with runtime agent management.

    Key features:
    - Add/remove agents at runtime
    - Automatic graph rebuilding
    - Tool aggregation from agents
    - Intelligent routing with history
    """

    # ========================================================================
    # CONFIGURATION
    # ========================================================================

    registered_agents: dict[str, Agent] = Field(
        default_factory=dict, description="Currently registered agents"
    )

    agent_capabilities: dict[str, str] = Field(
        default_factory=dict, description="Agent capability descriptions"
    )

    auto_rebuild: bool = Field(
        default=True, description="Automatically rebuild graph on agent changes"
    )

    enable_tool_aggregation: bool = Field(
        default=True, description="Aggregate tools from all agents"
    )

    state_schema: type[BaseModel] = Field(
        default=DynamicSupervisorState, description="Use dynamic supervisor state"
    )

    # ========================================================================
    # SETUP
    # ========================================================================

    def setup_agent(self) -> None:
        """Setup dynamic supervisor with management tools."""
        # Ensure low temperature for routing
        if not self.engine:
            self.engine = AugLLMConfig(temperature=0.1)
        elif hasattr(self.engine, "temperature"):
            self.engine.temperature = 0.1

        # Add agent management tools
        self._add_management_tools()

        # Call parent setup
        super().setup_agent()

    def _add_management_tools(self) -> None:
        """Add tools for agent management."""

        @tool
        def add_agent(name: str, capability: str) -> str:
            """Add a new agent to supervision.

            Args:
                name: Agent name to add
                capability: Description of agent capabilities
            """
            # This is a placeholder - in real use, would create agent
            return f"Agent '{name}' added with capability: {capability}"

        @tool
        def remove_agent(name: str) -> str:
            """Remove an agent from supervision.

            Args:
                name: Agent name to remove
            """
            if name in self.registered_agents:
                del self.registered_agents[name]
                del self.agent_capabilities[name]
                if self.auto_rebuild:
                    self._mark_for_rebuild()
                return f"Agent '{name}' removed"
            return f"Agent '{name}' not found"

        @tool
        def list_agents() -> str:
            """List all registered agents and their capabilities."""
            if not self.registered_agents:
                return "No agents registered"

            lines = ["Registered agents:"]
            for name, capability in self.agent_capabilities.items():
                lines.append(f"- {name}: {capability}")
            return "\n".join(lines)

        # Add tools to engine
        if self.engine and hasattr(self.engine, "tools"):
            if not self.engine.tools:
                self.engine.tools = []
            self.engine.tools.extend([add_agent, remove_agent, list_agents])

    # ========================================================================
    # AGENT MANAGEMENT
    # ========================================================================

    def register_agent(self, name: str, agent: Agent, capability: str) -> None:
        """Register an agent dynamically.

        Args:
            name: Unique agent name
            agent: Agent instance
            capability: Capability description
        """
        self.registered_agents[name] = agent
        self.agent_capabilities[name] = capability

        # Add to engines for state composition
        self.engines[f"agent_{name}"] = agent

        # Aggregate tools if enabled
        if self.enable_tool_aggregation:
            self._aggregate_agent_tools()

        # Mark for rebuild
        if self.auto_rebuild:
            self._mark_for_rebuild()

        logger.info(f"Dynamically registered agent '{name}'")

    def unregister_agent(self, name: str) -> bool:
        """Remove an agent dynamically.

        Args:
            name: Agent name to remove

        Returns:
            True if removed, False if not found
        """
        if name not in self.registered_agents:
            return False

        del self.registered_agents[name]
        del self.agent_capabilities[name]

        # Remove from engines
        engine_key = f"agent_{name}"
        if engine_key in self.engines:
            del self.engines[engine_key]

        # Mark for rebuild
        if self.auto_rebuild:
            self._mark_for_rebuild()

        logger.info(f"Dynamically unregistered agent '{name}'")
        return True

    def _mark_for_rebuild(self) -> None:
        """Mark that graph needs rebuilding."""
        # In a real implementation, this would trigger graph rebuild
        logger.info("Graph marked for rebuild due to agent changes")

    def _aggregate_agent_tools(self) -> None:
        """Aggregate tools from all registered agents."""
        aggregated_tools = []

        for name, agent in self.registered_agents.items():
            # Get tools from agent
            agent_tools = []

            # Check agent.tools
            if hasattr(agent, "tools") and agent.tools:
                agent_tools.extend(agent.tools)

            # Check agent.engine.tools
            if hasattr(agent, "engine") and agent.engine:
                if hasattr(agent.engine, "tools") and agent.engine.tools:
                    agent_tools.extend(agent.engine.tools)

            # Add prefixed tools to avoid conflicts
            for tool in agent_tools:
                # Clone tool with prefixed name
                if hasattr(tool, "name"):
                    tool.name = f"{name}_{tool.name}"
                aggregated_tools.append(tool)

        # Add aggregated tools to supervisor
        if self.engine and hasattr(self.engine, "tools"):
            # Keep management tools, add agent tools
            mgmt_tools = [
                t
                for t in (self.engine.tools or [])
                if t.name in ("add_agent", "remove_agent", "list_agents")
            ]
            self.engine.tools = mgmt_tools + aggregated_tools

            logger.info(f"Aggregated {len(aggregated_tools)} tools from agents")

    # ========================================================================
    # GRAPH BUILDING
    # ========================================================================

    def build_graph(self) -> BaseGraph:
        """Build dynamic supervisor graph."""
        # Start with ReactAgent graph
        graph = super().build_graph()

        # Add dynamic routing for registered agents
        if not self.registered_agents:
            return graph

        # Add routing decision node
        def route_to_agent(state: dict[str, Any]) -> str:
            """Route based on supervisor decision or tool calls."""
            messages = state.get("messages", [])
            if not messages:
                return END

            last_msg = messages[-1]

            # Check for tool calls first
            if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
                # Tool calls are handled by ReactAgent loop
                return "tool_node"

            # Check for agent routing
            if hasattr(last_msg, "content"):
                content = last_msg.content.strip().lower()

                if content == "end":
                    return END

                # Match agent names
                for agent_name in self.registered_agents:
                    if agent_name.lower() in content:
                        return f"{agent_name}_node"

            return END

        # Add agent nodes
        for name, agent in self.registered_agents.items():
            node = AgentNodeV3Config(name=f"{name}_node", agent=agent)
            graph.add_node(f"{name}_node", node)
            # Route back to supervisor after agent execution
            graph.add_edge(f"{name}_node", "agent_node")

        # Update routing from agent_node
        if "agent_node" in graph.nodes:
            # Remove existing edges from agent_node
            edges_to_remove = []
            for source, target in graph.edges:
                if source == "agent_node" and target != "route_decision":
                    edges_to_remove.append((source, target))

            for edge in edges_to_remove:
                graph.remove_edge(*edge)

            # Add routing
            graph.add_node("route_decision", route_to_agent)
            graph.add_edge("agent_node", "route_decision")

            # Add conditional routing
            route_map = {
                END: END,
                "tool_node": "tool_node" if "tool_node" in graph.nodes else END,
                **{f"{name}_node": f"{name}_node" for name in self.registered_agents},
            }

            graph.add_conditional_edges("route_decision", route_to_agent, route_map)

        return graph

    # ========================================================================
    # CONVENIENCE METHODS
    # ========================================================================

    @classmethod
    def create_with_agents(
        cls,
        agents: list[tuple[str, Agent, str]],
        name: str = "dynamic_supervisor",
        **kwargs,
    ) -> "DynamicSupervisor":
        """Create dynamic supervisor with initial agents.

        Args:
            agents: List of (name, agent, capability) tuples
            name: Supervisor name
            **kwargs: Additional arguments

        Returns:
            Configured DynamicSupervisor
        """
        supervisor = cls(name=name, **kwargs)

        for agent_name, agent, capability in agents:
            supervisor.register_agent(agent_name, agent, capability)

        return supervisor
