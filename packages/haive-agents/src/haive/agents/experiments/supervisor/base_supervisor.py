"""Base supervisor agent using ReactAgent with state-synchronized tools.

This module provides the base supervisor implementation that inherits from
ReactAgent and uses the state models and tools for agent management.
"""

import logging
from typing import Any, Callable, Dict, List, Optional, Type

from haive.core.graph.node.tool_node_config import ToolNodeConfig
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.tools import BaseTool

from haive.agents.base.agent import Agent
from haive.agents.experiments.supervisor.state_models import (
    AgentMetadata,
    DynamicSupervisorState,
    SerializedAgent,
    SupervisorState,
)
from haive.agents.experiments.supervisor.tools import (
    build_supervisor_tools,
    create_supervisor_handoff_tool,
    sync_tools_with_state,
)
from haive.agents.react.agent import ReactAgent

logger = logging.getLogger(__name__)


class BaseSupervisor(ReactAgent):
    """Base supervisor that manages agents through state.

    This supervisor:
    - Inherits ReactAgent's looping behavior
    - Stores agents as serialized objects in state
    - Dynamically creates/syncs handoff tools via model validators
    - Executes agents by deserializing from state in the tool node
    """

    def __init__(
        self,
        state_schema: Type[SupervisorState] = SupervisorState,
        agent_factory: Optional[Callable] = None,
        **kwargs,
    ):
        """Initialize supervisor with custom state schema.

        Args:
            state_schema: State schema class to use (SupervisorState or subclass)
            agent_factory: Optional factory for creating agents dynamically
            **kwargs: Additional arguments for ReactAgent
        """
        # Set state schema
        kwargs["state_schema"] = state_schema

        # Store agent factory
        self._agent_factory = agent_factory

        # Initialize parent
        super().__init__(**kwargs)

    def setup_agent(self) -> None:
        """Setup the supervisor with initial tools."""
        # Call parent setup
        super().setup_agent()

        # Sync tools with empty state
        self._sync_engine_tools()

    def _sync_engine_tools(self) -> None:
        """Synchronize engine tools with current state."""
        if not self.main_engine:
            return

        # Get current state
        try:
            state = self.get_state()
        except:
            # If state not available yet, use default
            state = self.state_schema()

        # Build tools based on state
        tools = build_supervisor_tools(
            get_state_fn=lambda: self.get_state(),
            update_state_fn=lambda s: self.update_state(s),
            include_dynamic_creation=isinstance(state, DynamicSupervisorState),
            agent_factory=self._agent_factory,
        )

        # Update engine tools
        if hasattr(self.main_engine, "tools"):
            self.main_engine.tools = tools
        elif hasattr(self.main_engine, "config") and hasattr(
            self.main_engine.config, "tools"
        ):
            self.main_engine.config.tools = tools

        logger.info(f"Synced {len(tools)} tools with engine")

    def register_agent(
        self,
        name: str,
        description: str,
        agent: Agent,
        capabilities: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
    ) -> None:
        """Register an agent with the supervisor.

        This updates the state, triggering validators to sync tools.
        """
        # Create metadata
        metadata = AgentMetadata(
            name=name,
            description=description,
            capabilities=capabilities or [],
            tags=tags or [],
        )

        # Get current state
        state = self.get_state()

        # Register agent
        state.register_agent(agent, metadata)

        # Update state - triggers validators
        self.update_state(state)

        # Sync tools with new agent
        self._sync_engine_tools()

        logger.info(f"Registered agent '{name}' with supervisor")

    def unregister_agent(self, name: str) -> bool:
        """Remove an agent from the supervisor.

        Returns:
            True if agent was removed, False if not found
        """
        state = self.get_state()

        if name not in state.agents:
            return False

        # Remove from state
        del state.agents[name]

        # Update state - triggers validators
        self.update_state(state)

        # Sync tools
        self._sync_engine_tools()

        logger.info(f"Unregistered agent '{name}'")
        return True

    def build_graph(self) -> BaseGraph:
        """Build graph using ReactAgent pattern with custom tool node."""
        # Get base ReactAgent graph
        graph = super().build_graph()

        # Override the tool node configuration
        if "tool_node" in graph.nodes:
            # Get the existing node function
            original_node_fn = graph.nodes["tool_node"]

            # Wrap it with our state-aware execution
            def state_aware_tool_node(state):
                """Enhanced tool node that handles agent handoffs from state."""
                # First, sync tools to ensure they match state
                self._sync_engine_tools()

                # Check if this is an agent handoff
                messages = state.get("messages", [])
                if messages and isinstance(messages[-1], AIMessage):
                    last_msg = messages[-1]
                    if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
                        # Check for handoff tools
                        tool_call = last_msg.tool_calls[0]
                        tool_name = tool_call.get("name", "")

                        # If it's a handoff, it will be handled by our custom tool
                        # which deserializes from state

                # Call original tool node
                return original_node_fn(state)

            # Replace the node
            graph.nodes["tool_node"] = state_aware_tool_node

        return graph

    def get_agent_status(self, agent_name: Optional[str] = None) -> Dict[str, Any]:
        """Get status information about agents.

        Args:
            agent_name: Specific agent name or None for all agents

        Returns:
            Status dictionary with agent information
        """
        state = self.get_state()

        if agent_name:
            if agent_name not in state.agents:
                return {"error": f"Agent '{agent_name}' not found"}

            agent_info = state.agents[agent_name]
            return {
                "name": agent_name,
                "metadata": agent_info.metadata.dict(),
                "class": agent_info.agent_class,
                "module": agent_info.agent_module,
            }
        else:
            # Return all agents
            return {
                "total_agents": len(state.agents),
                "agents": {
                    name: {
                        "description": info.metadata.description,
                        "usage_count": info.metadata.usage_count,
                        "last_used": (
                            info.metadata.last_used.isoformat()
                            if info.metadata.last_used
                            else None
                        ),
                    }
                    for name, info in state.agents.items()
                },
            }

    def get_execution_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent execution history.

        Args:
            limit: Maximum number of entries to return

        Returns:
            List of execution records
        """
        state = self.get_state()
        return state.execution_history[-limit:]

    def clear_history(self) -> None:
        """Clear execution history."""
        state = self.get_state()
        state.execution_history.clear()
        self.update_state(state)


class DynamicSupervisor(BaseSupervisor):
    """Dynamic supervisor that can create agents on the fly.

    This extends BaseSupervisor with dynamic agent creation capabilities.
    """

    def __init__(self, agent_factory: Optional[Callable] = None, **kwargs):
        """Initialize with DynamicSupervisorState."""
        super().__init__(
            state_schema=DynamicSupervisorState, agent_factory=agent_factory, **kwargs
        )

    def add_agent_template(self, name: str, template: Dict[str, Any]) -> None:
        """Add a template for agent creation.

        Templates can be used by the create_agent tool.
        """
        state = self.get_state()
        state.add_agent_template(name, template)
        self.update_state(state)

    def set_agent_limit(self, max_agents: int) -> None:
        """Set the maximum number of agents allowed."""
        state = self.get_state()
        state.max_agents = max_agents
        self.update_state(state)

    def enable_agent_creation(self, enabled: bool = True) -> None:
        """Enable or disable dynamic agent creation."""
        state = self.get_state()
        state.can_create_agents = enabled
        self.update_state(state)

        # Re-sync tools to add/remove creation tool
        self._sync_engine_tools()
