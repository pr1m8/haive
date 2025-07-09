# haive/agents/multi/base.py

"""Base multi-agent class for the Haive framework.

This module provides the abstract base class for multi-agent systems,
enabling composition of multiple agents with various coordination patterns.
"""

import logging
from abc import abstractmethod
from typing import Any, Literal

from haive.core.graph.node.engine_node import EngineNodeConfig
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.schema.agent_schema_composer import AgentSchemaComposer
from langgraph.graph import END
from langgraph.types import Command
from pydantic import Field, PrivateAttr, model_validator

from haive.agents.base.agent import Agent

logger = logging.getLogger(__name__)


class MultiAgent(Agent):
    """Abstract base class for multi-agent systems.

    This class provides the foundation for composing multiple agents into
    coordinated systems with various execution patterns.
    """

    # Multi-agent specific fields
    agents: dict[str, Agent] = Field(
        default_factory=dict,
        description="Dictionary of sub-agents in this multi-agent system",
    )

    coordination_mode: Literal[
        "sequential", "parallel", "supervisor", "swarm", "custom"
    ] = Field(default="sequential", description="Coordination mode for the agents")

    separation_strategy: Literal["namespaced", "smart", "flat"] = Field(
        default="smart", description="Schema field separation strategy"
    )

    enable_meta: bool = Field(
        default=False,
        description="Enable meta-agent capabilities (graph self-modification)",
    )

    # Agent execution configuration
    max_iterations: int = Field(
        default=10, description="Maximum iterations for iterative patterns"
    )

    allow_agent_communication: bool = Field(
        default=True, description="Allow agents to communicate directly"
    )

    share_message_history: bool = Field(
        default=True, description="Share message history between agents"
    )

    # Private tracking
    _agent_order: list[str] = PrivateAttr(default_factory=list)
    _coordinator_agent: str | None = PrivateAttr(default=None)

    def __reduce__(self):
        """Make MultiAgent picklable."""
        state_dict = self.model_dump(
            exclude={
                "_state_instance",
                "graph",
                "_compiled_graph",
                "checkpointer",
                "store",
                "config",
                "_agent_order",
                "_coordinator_agent",
            }
        )

        # Handle agent references
        if "agents" in state_dict:
            # Store agent names only for serialization
            state_dict["agent_names"] = list(state_dict["agents"].keys())
            state_dict.pop("agents")

        return (self.__class__, (), state_dict)

    @model_validator(mode="before")
    @classmethod
    def normalize_agents(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Normalize agents into engines dict."""
        # Handle list of agents - convert to dict
        if "agents" in values and isinstance(values["agents"], list):
            agent_dict = {}
            for i, agent in enumerate(values["agents"]):
                if hasattr(agent, "name"):
                    agent_dict[agent.name] = agent
                else:
                    agent_dict[f"agent_{i}"] = agent
            values["agents"] = agent_dict

        # Now handle the dict of agents
        if values.get("agents"):
            # Also add agents to engines dict for compatibility
            if "engines" not in values:
                values["engines"] = {}

            for name, agent in values["agents"].items():
                if isinstance(agent, Agent):
                    values["engines"][name] = agent

        return values

    def setup_agent(self) -> None:
        """Set up the multi-agent system."""
        # Validate we have agents
        if not self.agents:
            raise ValueError(f"{self.__class__.__name__} requires at least one agent")

        # Store agent order
        self._agent_order = list(self.agents.keys())

        # Set up coordinator if needed
        if self.coordination_mode == "supervisor":
            self._setup_supervisor()

        # Ensure schema generation
        self.set_schema = True

    def _setup_schemas(self) -> None:
        """Generate schemas using MultiAgentSchemaComposer."""
        # Don't regenerate if we already have schemas
        if self.state_schema:
            return

        # Get list of agents
        agent_list = list(self.agents.values())

        # Use AgentSchemaComposer
        self.state_schema = AgentSchemaComposer.from_agents(
            agents=agent_list,
            name=f"{self.__class__.__name__}State",
            separation=self.separation_strategy,
            include_meta=self.enable_meta,
        )

        # Let parent handle input/output schema derivation
        super()._setup_schemas()

    @abstractmethod
    def build_graph(self) -> BaseGraph:
        """Build the multi-agent graph - must be implemented by subclasses."""

    def _create_agent_node(self, agent_name: str, agent: Agent) -> EngineNodeConfig:
        """Create an engine node for an agent."""
        return EngineNodeConfig(
            name=f"{agent_name}_node",
            engine=agent,
            # Use smart field mapping based on separation strategy
            input_fields=self._get_agent_input_mapping(agent_name),
            output_fields=self._get_agent_output_mapping(agent_name),
        )

    def _get_agent_input_mapping(self, agent_name: str) -> dict[str, str]:
        """Get input field mapping for an agent based on separation strategy."""
        mapping = {}

        if self.separation_strategy == "flat":
            # Direct mapping
            return None  # Use default mapping

        if self.separation_strategy == "namespaced":
            # Map namespaced fields to agent's expected fields
            agent = self.agents.get(agent_name)
            if (
                agent
                and agent.state_schema
                and hasattr(agent.state_schema, "model_fields")
            ):
                for field_name in agent.state_schema.model_fields:
                    namespaced = f"{agent_name}_{field_name}"
                    mapping[namespaced] = field_name

        elif self.separation_strategy == "smart":
            # Map both shared and namespaced fields
            agent = self.agents.get(agent_name)
            if (
                agent
                and agent.state_schema
                and hasattr(agent.state_schema, "model_fields")
            ):
                for field_name in agent.state_schema.model_fields:
                    # Check if field is conflicted
                    if hasattr(self.state_schema, "__metadata__"):
                        conflicts = self.state_schema.__metadata__.get(
                            "field_conflicts", {}
                        )
                        if (
                            field_name in conflicts
                            and agent_name in conflicts[field_name]
                        ):
                            # Use namespaced version
                            namespaced = f"{agent_name}_{field_name}"
                            mapping[namespaced] = field_name
                        # Shared fields map directly

        return mapping if mapping else None

    def _get_agent_output_mapping(self, agent_name: str) -> dict[str, str]:
        """Get output field mapping for an agent based on separation strategy."""
        mapping = {}

        if self.separation_strategy == "flat":
            # Direct mapping
            return None

        if self.separation_strategy == "namespaced":
            # Map agent outputs to namespaced fields
            agent = self.agents.get(agent_name)
            if (
                agent
                and agent.state_schema
                and hasattr(agent.state_schema, "model_fields")
            ):
                for field_name in agent.state_schema.model_fields:
                    namespaced = f"{agent_name}_{field_name}"
                    mapping[field_name] = namespaced

        elif self.separation_strategy == "smart":
            # Map conflicted fields to namespaced versions
            agent = self.agents.get(agent_name)
            if (
                agent
                and agent.state_schema
                and hasattr(agent.state_schema, "model_fields")
            ):
                for field_name in agent.state_schema.model_fields:
                    # Check if field is conflicted
                    if hasattr(self.state_schema, "__metadata__"):
                        conflicts = self.state_schema.__metadata__.get(
                            "field_conflicts", {}
                        )
                        if (
                            field_name in conflicts
                            and agent_name in conflicts[field_name]
                        ):
                            # Use namespaced version
                            namespaced = f"{agent_name}_{field_name}"
                            mapping[field_name] = namespaced

        return mapping if mapping else None

    def _setup_supervisor(self) -> None:
        """Set up a supervisor agent if needed."""
        # This would be implemented to create a supervisor agent
        # For now, we'll use the first agent as coordinator
        if self._agent_order:
            self._coordinator_agent = self._agent_order[0]

    def route_to_agent(self, state: Any) -> str:
        """Route to the next agent based on state."""
        # This is a simple implementation - subclasses can override
        if hasattr(state, "next_agent") and state.next_agent:
            return f"{state.next_agent}_node"

        # Default routing based on completion
        if hasattr(state, "completed_agents"):
            for agent_name in self._agent_order:
                if agent_name not in state.completed_agents:
                    return f"{agent_name}_node"

        return END

    def should_continue(self, state: Any) -> bool:
        """Check if execution should continue."""
        if hasattr(state, "completed_agents") and hasattr(state, "agents"):
            return len(state.completed_agents) < len(state.agents)
        return False

    def update_agent_state(self, agent_name: str) -> Any:
        """Update state after agent execution."""

        def _update(state: Any) -> Command:
            updates = {
                "current_agent": agent_name,
                "completed_agents": (
                    state.completed_agents + [agent_name]
                    if agent_name not in state.completed_agents
                    else state.completed_agents
                ),
            }

            # Store result if available
            if hasattr(state, f"{agent_name}_output"):
                result = getattr(state, f"{agent_name}_output")
                updates["agent_results"] = {**state.agent_results, agent_name: result}

            return Command(update=updates)

        return _update

    @classmethod
    def from_agents(
        cls,
        agents: list[Agent] | dict[str, Agent],
        name: str | None = None,
        coordination_mode: str = "sequential",
        **kwargs,
    ) -> "MultiAgent":
        """Create a multi-agent system from a list or dict of agents."""
        # Convert list to dict if needed
        if isinstance(agents, list):
            agent_dict = {agent.name: agent for agent in agents}
        else:
            agent_dict = agents

        return cls(
            name=name or f"{cls.__name__}",
            agents=agent_dict,
            coordination_mode=coordination_mode,
            **kwargs,
        )
