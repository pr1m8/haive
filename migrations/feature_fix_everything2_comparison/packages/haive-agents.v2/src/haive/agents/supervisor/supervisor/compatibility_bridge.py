"""Compatibility Bridge for Dynamic Supervisor with Existing Multi-Agent Architecture.

This module provides integration between the new dynamic supervisor system
and the existing multi-agent base classes, ensuring seamless interoperability.
"""

import logging
from collections.abc import Sequence
from typing import Any, Optional

from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.schema.agent_schema_composer import AgentSchemaComposer
from pydantic import Field, model_validator

from haive.agents.base.agent import Agent
from haive.agents.multi.base import ExecutionMode, MultiAgent
from haive.agents.supervisor.integrated_supervisor import IntegratedDynamicSupervisor

logger = logging.getLogger(__name__)


class DynamicMultiAgentSupervisor(MultiAgent):
    """Multi-agent system with dynamic supervisor capabilities.

    This class bridges the gap between the existing MultiAgent architecture
    and the new dynamic supervisor system, providing:

    - Compatibility with existing MultiAgent patterns
    - Dynamic agent addition/removal during runtime
    - Integration with AgentSchemaComposer
    - Support for all existing execution modes + dynamic supervision
    """

    # Additional configuration for dynamic capabilities
    enable_dynamic_management: bool = Field(
        default=True, description="Enable dynamic agent addition/removal"
    )

    supervisor_engine: Any | None = Field(
        default=None, description="Engine for supervisor decision making"
    )

    use_choice_model: bool = Field(
        default=True, description="Use DynamicChoiceModel for routing decisions"
    )

    # Private dynamic supervisor instance
    _dynamic_supervisor: IntegratedDynamicSupervisor | None = None

    @model_validator(mode="after")
    @classmethod
    def setup_dynamic_supervisor(cls) -> "DynamicMultiAgentSupervisor":
        """Set up the dynamic supervisor if needed."""
        if (
            self.execution_mode == ExecutionMode.HIERARCHICAL
            and self.enable_dynamic_management
        ):
            # Create dynamic supervisor instance
            self._dynamic_supervisor = IntegratedDynamicSupervisor(
                name=f"{self.name}_supervisor",
                engine=self.supervisor_engine,
                enable_agent_management_tools=True,
                coordination_mode="supervisor",
                auto_rebuild_graph=True,
            )

            # Register existing agents with supervisor
            for agent in self.agents:
                if hasattr(agent, "name"):
                    # Use asyncio.create_task or run in executor for async registration
                    logger.info(f"Will register {agent.name} with dynamic supervisor")

        return self

    def setup_agent(self) -> None:
        """Enhanced setup with dynamic supervisor integration."""
        # Call parent setup
        super().setup_agent()

        # Additional setup for dynamic supervisor
        if self._dynamic_supervisor:
            logger.info("Setting up dynamic supervisor integration")

    def _setup_schemas(self) -> None:
        """Enhanced schema setup that integrates dynamic supervisor state."""
        if (
            self.enable_dynamic_management
            and self.execution_mode == ExecutionMode.HIERARCHICAL
        ):
            # Use enhanced state schema that combines both approaches
            self._setup_hybrid_schema()
        else:
            # Use standard multi-agent schema composition
            super()._setup_schemas()

    def _setup_hybrid_schema(self) -> None:
        """Set up hybrid schema combining AgentSchemaComposer and dynamic state."""
        # Get list of agents for schema composition
        agent_list = list(self.agents)

        logger.info(f"Creating hybrid schema from {len(agent_list)} agents")

        # Create base composed schema using existing approach
        composed_schema = AgentSchemaComposer.from_agents(
            agents=agent_list,
            name=f"{self.__class__.__name__}BaseState",
            separation=self.schema_separation,
            include_meta=self.include_meta,
        )

        # Enhance with dynamic supervisor capabilities
        from haive.core.schema.schema_composer import SchemaComposer

        enhanced_composer = SchemaComposer(name=f"{self.__class__.__name__}State")

        # Add all fields from composed schema
        enhanced_composer.add_fields_from_model(composed_schema)

        # Add dynamic supervisor fields
        enhanced_composer.add_field(
            "dynamic_agent_registry",
            Optional[dict[str, Any]],
            default_factory=dict,
            description="Dynamic agent registry for runtime management",
        )

        enhanced_composer.add_field(
            "supervisor_decisions",
            list[dict[str, Any]],
            default_factory=list,
            description="History of supervisor routing decisions",
        )

        enhanced_composer.add_field(
            "dynamic_coordination_active",
            bool,
            default=False,
            description="Whether dynamic coordination is active",
        )

        # Build final schema
        self.state_schema = enhanced_composer.build()

        logger.info(f"Created hybrid schema: {self.state_schema.__name__}")

    def build_graph(self) -> BaseGraph:
        """Build graph with dynamic supervisor integration."""
        if (
            self.enable_dynamic_management
            and self.execution_mode == ExecutionMode.HIERARCHICAL
        ):
            return self._build_dynamic_supervisor_graph()
        # Use standard multi-agent graph building
        return super().build_graph()

    def _build_dynamic_supervisor_graph(self) -> BaseGraph:
        """Build graph with integrated dynamic supervisor."""
        # Create hybrid graph that combines multi-agent patterns with dynamic supervision
        graph = BaseGraph(name=f"{self.name}DynamicGraph")

        # Add supervisor node
        supervisor_node = self._create_dynamic_supervisor_node()
        graph.add_node("dynamic_supervisor", supervisor_node)

        # Add existing agents as managed nodes
        for agent in self.agents:
            agent_node = self._create_managed_agent_node(agent)
            graph.add_node(f"managed_{agent.name}", agent_node)

            # Connect supervisor to agents
            graph.add_edge("dynamic_supervisor", f"managed_{agent.name}")
            # Connect agents back to supervisor
            graph.add_edge(f"managed_{agent.name}", "dynamic_supervisor")

        # Add dynamic management node
        mgmt_node = self._create_dynamic_management_node()
        graph.add_node("dynamic_management", mgmt_node)
        graph.add_edge("dynamic_supervisor", "dynamic_management")
        graph.add_edge("dynamic_management", "dynamic_supervisor")

        return graph

    def _create_dynamic_supervisor_node(self) -> Any:
        """Create supervisor node that integrates with multi-agent state."""

        async def supervisor_node(state: Any, config=None) -> dict[str, Any]:
            """Supervisor node with multi-agent state integration."""
            # Extract multi-agent state
            if hasattr(state, "messages"):
                messages = state.messages
            else:
                messages = getattr(state, "messages", [])

            # Use dynamic supervisor for routing if available
            if self._dynamic_supervisor:
                # Create supervisor state
                supervisor_state = {
                    "messages": messages,
                    "registered_agents": getattr(state, "dynamic_agent_registry", {}),
                    "supervisor_decisions": getattr(state, "supervisor_decisions", []),
                }

                # Get supervisor decision
                decision_result = await self._dynamic_supervisor.route_request_internal(
                    supervisor_state
                )

                # Update multi-agent state
                updates = {
                    "supervisor_decisions": [
                        *getattr(state, "supervisor_decisions", []),
                        decision_result,
                    ],
                    "dynamic_coordination_active": True,
                }

                return updates

            # Fallback to first agent if no dynamic supervisor
            return {"dynamic_coordination_active": False}

        return supervisor_node

    def _create_managed_agent_node(self, agent: Agent) -> Any:
        """Create node for an agent managed by dynamic supervisor."""

        async def managed_agent_node(state: Any, config=None) -> dict[str, Any]:
            """Execute agent within multi-agent context."""
            # Extract input for agent using existing multi-agent patterns
            agent_input = self._extract_agent_input(agent.name, agent, state)

            # Execute agent
            logger.info(f"Executing managed agent: {agent.name}")
            result = await agent.ainvoke(agent_input, config)

            # Create update using existing patterns
            update = self._create_agent_output(agent.name, agent, result, state)

            return update

        return managed_agent_node

    def _create_dynamic_management_node(self) -> Any:
        """Create node for dynamic agent management operations."""

        async def management_node(state: Any, config=None) -> dict[str, Any]:
            """Handle dynamic agent management requests."""
            # Check for management requests in messages
            messages = getattr(state, "messages", [])

            if messages:
                last_message = messages[-1]
                content = getattr(last_message, "content", "").lower()

                # Simple management command detection
                if "add agent" in content:
                    # Simulate agent addition
                    registry = getattr(state, "dynamic_agent_registry", {})
                    registry["new_agent"] = {"added_at": "now", "capability": "dynamic"}
                    return {"dynamic_agent_registry": registry}

                if "remove agent" in content:
                    # Simulate agent removal
                    registry = getattr(state, "dynamic_agent_registry", {})
                    if "target_agent" in registry:
                        del registry["target_agent"]
                    return {"dynamic_agent_registry": registry}

            return {}

        return management_node

    async def register_agent_dynamically(
        self, agent: Agent, capability: str | None = None
    ) -> bool:
        """Register an agent dynamically at runtime."""
        if not self._dynamic_supervisor:
            logger.warning("Dynamic supervisor not available for agent registration")
            return False

        try:
            # Register with dynamic supervisor
            success = await self._dynamic_supervisor.register_agent(
                agent,
                capability_description=capability or f"Dynamically added {agent.name}",
                rebuild_graph=True,
            )

            if success:
                # Add to multi-agent agents list
                self.agents = [*list(self.agents), agent]
                logger.info(f"Successfully registered {agent.name} dynamically")

            return success

        except Exception as e:
            logger.exception(f"Failed to register agent {agent.name}: {e}")
            return False

    async def unregister_agent_dynamically(self, agent_name: str) -> bool:
        """Unregister an agent dynamically at runtime."""
        if not self._dynamic_supervisor:
            logger.warning("Dynamic supervisor not available for agent removal")
            return False

        try:
            # Remove from dynamic supervisor
            success = await self._dynamic_supervisor.unregister_agent(agent_name)

            if success:
                # Remove from multi-agent agents list
                self.agents = [
                    agent for agent in self.agents if agent.name != agent_name
                ]
                logger.info(f"Successfully unregistered {agent_name} dynamically")

            return success

        except Exception as e:
            logger.exception(f"Failed to unregister agent {agent_name}: {e}")
            return False

    def get_dynamic_status(self) -> dict[str, Any]:
        """Get status of dynamic supervisor capabilities."""
        status = {
            "dynamic_management_enabled": self.enable_dynamic_management,
            "execution_mode": self.execution_mode,
            "total_agents": len(self.agents),
            "supervisor_available": self._dynamic_supervisor is not None,
        }

        if self._dynamic_supervisor:
            status.update(
                {
                    "registered_agents": self._dynamic_supervisor.agent_registry.get_available_agents(),
                    "coordination_status": self._dynamic_supervisor.get_coordination_status(),
                }
            )

        return status


class ReactMultiAgentSupervisor(DynamicMultiAgentSupervisor):
    """Multi-agent supervisor with ReactAgent-style capabilities.

    Combines ReactAgent looping behavior with multi-agent coordination
    and dynamic supervisor capabilities.
    """

    # Force hierarchical execution for supervisor pattern
    execution_mode: ExecutionMode = Field(default=ExecutionMode.HIERARCHICAL)

    def build_graph(self) -> BaseGraph:
        """Build graph with React-style looping and multi-agent coordination."""
        # Get base dynamic supervisor graph
        graph = super().build_graph()

        # Add React-style looping between supervisor and agents
        if self._dynamic_supervisor and hasattr(graph, "nodes"):
            # Remove END edges and add loops back to supervisor
            for node_name in list(graph.nodes.keys()):
                if (
                    node_name.startswith("managed_")
                    and "dynamic_supervisor" in graph.nodes
                ):
                    # Change edge to loop back instead of ending
                    # This creates ReactAgent-style continuous execution
                    pass

        return graph


def create_compatible_supervisor(
    agents: Sequence[Agent],
    name: str = "Compatible Supervisor",
    enable_dynamic: bool = True,
    supervisor_engine: Any = None,
) -> DynamicMultiAgentSupervisor | MultiAgent:
    """Factory function to create compatible supervisor based on requirements.

    Args:
        agents: List of agents to manage
        name: Name of the supervisor system
        enable_dynamic: Whether to enable dynamic capabilities
        supervisor_engine: Engine for supervisor decisions

    Returns:
        Either DynamicMultiAgentSupervisor or standard MultiAgent
    """
    if enable_dynamic and supervisor_engine:
        return DynamicMultiAgentSupervisor(
            name=name,
            agents=agents,
            execution_mode=ExecutionMode.HIERARCHICAL,
            enable_dynamic_management=True,
            supervisor_engine=supervisor_engine,
            use_choice_model=True,
        )
    return MultiAgent(name=name, agents=agents, execution_mode=ExecutionMode.SEQUENCE)


def migrate_from_multi_agent(multi_agent: MultiAgent) -> DynamicMultiAgentSupervisor:
    """Migrate existing MultiAgent to dynamic supervisor version.

    Args:
        multi_agent: Existing MultiAgent instance

    Returns:
        DynamicMultiAgentSupervisor with same configuration
    """
    return DynamicMultiAgentSupervisor(
        name=multi_agent.name,
        agents=multi_agent.agents,
        execution_mode=ExecutionMode.HIERARCHICAL,  # Upgrade to hierarchical
        enable_dynamic_management=True,
        schema_separation=getattr(multi_agent, "schema_separation", "smart"),
        include_meta=getattr(multi_agent, "include_meta", True),
    )
