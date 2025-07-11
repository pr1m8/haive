"""Multi-agent V2 with proper state management and rebuilding support.

This module provides a rebuilt MultiAgent that uses MultiAgentState without
schema flattening, maintaining type safety and hierarchical access.
"""

import logging
from abc import abstractmethod
from enum import Enum
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Literal,
    Optional,
    Sequence,
    Type,
    Union,
)

from haive.core.graph.node.agent_node_v3 import create_agent_node_v3
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.schema.prebuilt.multi_agent_state import MultiAgentState
from haive.core.schema.state_schema import StateSchema
from langgraph.graph import END, START
from pydantic import BaseModel, Field, create_model, model_validator

from haive.agents.base.agent import Agent

logger = logging.getLogger(__name__)


class ExecutionMode(str, Enum):
    """Execution modes for multi-agent systems."""

    SEQUENCE = "sequence"
    PARALLEL = "parallel"
    CONDITIONAL = "conditional"
    HIERARCHICAL = "hierarchical"


class MultiAgentV2(Agent[MultiAgentState]):
    """Rebuilt multi-agent system using proper state management.

    Key improvements:
    - Uses MultiAgentState without schema flattening
    - Each agent maintains its own schema
    - Supports rebuilding with class methods
    - Proper hierarchical state access
    """

    # Agent configuration
    agents: list[Agent] | dict[str, Agent] = Field(
        ..., description="Agents to coordinate (list or dict)"
    )

    execution_mode: ExecutionMode = Field(
        default=ExecutionMode.SEQUENCE, description="How agents are executed"
    )

    # State configuration
    state_schema: type[StateSchema] = Field(
        default=MultiAgentState,
        description="State schema (defaults to MultiAgentState)",
    )

    use_prebuilt_base: bool = Field(
        default=True, description="Use MultiAgentState as base for composition"
    )

    # Routing configuration (for conditional mode)
    routing_function: Callable | None = Field(
        default=None, description="Function for conditional routing"
    )

    route_map: dict[str, str] | None = Field(
        default=None, description="Map of routing outputs to agent names"
    )

    @model_validator(mode="before")
    @classmethod
    def validate_agents(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Ensure agents are provided."""
        agents = values.get("agents", [])
        if not agents:
            raise ValueError("MultiAgent requires at least one agent")

        # Convert list to dict if needed
        if isinstance(agents, list):
            values["agents"] = {agent.name: agent for agent in agents}

        return values

    @model_validator(mode="after")
    def setup_multi_agent(self) -> "MultiAgentV2":
        """Set up the multi-agent system."""
        # Create custom state schema if needed
        if self.state_schema == MultiAgentState:
            # Use default MultiAgentState
            pass
        elif not issubclass(self.state_schema, MultiAgentState):
            raise ValueError("state_schema must extend MultiAgentState")

        # Validate routing for conditional mode
        if self.execution_mode == ExecutionMode.CONDITIONAL:
            if not self.routing_function or not self.route_map:
                raise ValueError(
                    "Conditional mode requires routing_function and route_map"
                )

        return self

    @classmethod
    def from_agents(
        cls,
        agents: list[Agent] | dict[str, Agent],
        name: str | None = None,
        execution_mode: ExecutionMode = ExecutionMode.SEQUENCE,
        **kwargs,
    ) -> "MultiAgentV2":
        """Create MultiAgent from a list or dict of agents.

        Args:
            agents: List or dict of agents to coordinate
            name: Optional name for the multi-agent
            execution_mode: How to execute agents
            **kwargs: Additional configuration

        Returns:
            MultiAgentV2 instance
        """
        return cls(
            name=name or "multi_agent",
            agents=agents,
            execution_mode=execution_mode,
            **kwargs,
        )

    @classmethod
    def from_config(
        cls,
        config: dict[str, Any],
        agents: list[Agent] | dict[str, Agent] | None = None,
    ) -> "MultiAgentV2":
        """Create MultiAgent from configuration dict.

        Args:
            config: Configuration dictionary
            agents: Optional agents (overrides config)

        Returns:
            MultiAgentV2 instance
        """
        if agents:
            config["agents"] = agents

        return cls(**config)

    @classmethod
    def rebuild_with_agents(
        cls,
        original: "MultiAgentV2",
        new_agents: list[Agent] | dict[str, Agent],
        **kwargs,
    ) -> "MultiAgentV2":
        """Rebuild MultiAgent with new agents.

        Args:
            original: Original MultiAgent to rebuild from
            new_agents: New agents to use
            **kwargs: Additional config overrides

        Returns:
            New MultiAgentV2 instance
        """
        # Get original config
        config = {
            "name": original.name,
            "execution_mode": original.execution_mode,
            "state_schema": original.state_schema,
            "routing_function": original.routing_function,
            "route_map": original.route_map,
        }

        # Apply overrides
        config.update(kwargs)
        config["agents"] = new_agents

        return cls(**config)

    def add_agent(self, agent: Agent, rebuild: bool = True) -> "MultiAgentV2":
        """Add an agent and optionally rebuild.

        Args:
            agent: Agent to add
            rebuild: Whether to rebuild the graph

        Returns:
            Self or new instance if rebuilt
        """
        if isinstance(self.agents, dict):
            new_agents = {**self.agents, agent.name: agent}
        else:
            new_agents = [*list(self.agents), agent]

        if rebuild:
            return self.rebuild_with_agents(self, new_agents)
        self.agents = new_agents
        return self

    def remove_agent(self, agent_name: str, rebuild: bool = True) -> "MultiAgentV2":
        """Remove an agent and optionally rebuild.

        Args:
            agent_name: Name of agent to remove
            rebuild: Whether to rebuild the graph

        Returns:
            Self or new instance if rebuilt
        """
        if isinstance(self.agents, dict):
            new_agents = {k: v for k, v in self.agents.items() if k != agent_name}
        else:
            new_agents = [a for a in self.agents if a.name != agent_name]

        if rebuild:
            return self.rebuild_with_agents(self, new_agents)
        self.agents = new_agents
        return self

    def get_agent(self, agent_name: str) -> Agent | None:
        """Get an agent by name."""
        if isinstance(self.agents, dict):
            return self.agents.get(agent_name)
        for agent in self.agents:
            if agent.name == agent_name:
                return agent
        return None

    def build_graph(self) -> BaseGraph:
        """Build the multi-agent graph based on execution mode."""
        graph = BaseGraph(state_schema=self.state_schema)

        if self.execution_mode == ExecutionMode.SEQUENCE:
            self._build_sequence_graph(graph)
        elif self.execution_mode == ExecutionMode.PARALLEL:
            self._build_parallel_graph(graph)
        elif self.execution_mode == ExecutionMode.CONDITIONAL:
            self._build_conditional_graph(graph)
        elif self.execution_mode == ExecutionMode.HIERARCHICAL:
            self._build_hierarchical_graph(graph)
        else:
            raise ValueError(f"Unknown execution mode: {self.execution_mode}")

        return graph.compile()

    def _build_sequence_graph(self, graph: BaseGraph) -> None:
        """Build sequential execution graph."""
        agent_names = (
            list(self.agents.keys())
            if isinstance(self.agents, dict)
            else [a.name for a in self.agents]
        )

        # Add nodes
        for i, agent_name in enumerate(agent_names):
            node = create_agent_node_v3(
                agent_name=agent_name, name=f"agent_{agent_name}"
            )
            graph.add_node(f"agent_{agent_name}", node)

        # Add edges
        graph.add_edge(START, f"agent_{agent_names[0]}")

        for i in range(len(agent_names) - 1):
            graph.add_edge(f"agent_{agent_names[i]}", f"agent_{agent_names[i+1]}")

        graph.add_edge(f"agent_{agent_names[-1]}", END)

    def _build_parallel_graph(self, graph: BaseGraph) -> None:
        """Build parallel execution graph."""
        agent_names = (
            list(self.agents.keys())
            if isinstance(self.agents, dict)
            else [a.name for a in self.agents]
        )

        # Add coordinator node
        graph.add_node("coordinator", self._coordinate_parallel)

        # Add agent nodes
        for agent_name in agent_names:
            node = create_agent_node_v3(
                agent_name=agent_name, name=f"agent_{agent_name}"
            )
            graph.add_node(f"agent_{agent_name}", node)

            # Fan out from coordinator
            graph.add_edge("coordinator", f"agent_{agent_name}")
            # Fan in to aggregator
            graph.add_edge(f"agent_{agent_name}", "aggregator")

        # Add aggregator
        graph.add_node("aggregator", self._aggregate_results)

        # Connect flow
        graph.add_edge(START, "coordinator")
        graph.add_edge("aggregator", END)

    def _build_conditional_graph(self, graph: BaseGraph) -> None:
        """Build conditional execution graph."""
        if not self.routing_function or not self.route_map:
            raise ValueError("Conditional mode requires routing_function and route_map")

        # Add router node
        graph.add_node("router", self._route_conditionally)
        graph.add_edge(START, "router")

        # Add agent nodes and conditional edges
        for route_key, agent_name in self.route_map.items():
            node = create_agent_node_v3(
                agent_name=agent_name, name=f"agent_{agent_name}"
            )
            graph.add_node(f"agent_{agent_name}", node)

            # Conditional edge from router
            graph.add_conditional_edges(
                "router", self.routing_function, {route_key: f"agent_{agent_name}"}
            )

            # All agents go to END
            graph.add_edge(f"agent_{agent_name}", END)

    def _build_hierarchical_graph(self, graph: BaseGraph) -> None:
        """Build hierarchical execution graph."""
        # This is a simplified version - can be extended
        self._build_sequence_graph(graph)

    def _coordinate_parallel(self, state: MultiAgentState) -> dict[str, Any]:
        """Coordinate parallel execution."""
        # Mark all agents for execution
        return {"execution_stage": "parallel_start"}

    def _aggregate_results(self, state: MultiAgentState) -> dict[str, Any]:
        """Aggregate results from parallel execution."""
        # Results are already in agent_outputs
        return {"execution_stage": "parallel_complete"}

    def _route_conditionally(self, state: MultiAgentState) -> str:
        """Route based on condition."""
        if self.routing_function:
            return self.routing_function(state)
        return "END"

    @abstractmethod
    def setup_agent(self) -> None:
        """Setup hook for subclasses."""
