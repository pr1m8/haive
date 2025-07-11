# haive/agents/multi/base.py
"""Base multi-agent implementation with branching and conditional routing support.

This module provides an abstract base class for multi-agent systems that can:
- Execute agents in sequence, parallel, or with conditional branching
- Maintain private agent state schemas while sharing a global state
- Support complex routing patterns including loops and conditional paths
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
    Tuple,
    Type,
    Union,
)

from haive.core.engine.base import EngineType
from haive.core.graph.node.engine_node import EngineNodeConfig
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.schema.agent_schema_composer import AgentSchemaComposer, BuildMode
from haive.core.schema.state_schema import StateSchema
from langchain_core.messages import BaseMessage
from langgraph.graph import END, START
from pydantic import BaseModel, Field, PrivateAttr, model_validator
from rich.console import Console
from rich.tree import Tree

from haive.agents.base.agent import Agent

logger = logging.getLogger(__name__)
console = Console()


class ExecutionMode(str, Enum):
    """Execution modes for multi-agent systems."""

    SEQUENCE = "sequence"  # Execute agents in order
    PARALLEL = "parallel"  # Execute agents in parallel
    CONDITIONAL = "conditional"  # Use conditional routing
    HIERARCHICAL = "hierarchical"  # Parent-child execution


class MultiAgent(Agent):
    """Abstract base class for multi-agent systems with branching support.

    This class provides:
    - Automatic schema composition from child agents
    - Support for sequential, parallel, and conditional execution
    - Private agent state management
    - Complex routing patterns via conditional edges
    - Meta state for agent coordination
    """

    # Configuration
    name: str = Field(
        default="Multi Agent", description="Name of the multi-agent system"
    )
    agents: Sequence[Agent] = Field(
        default_factory=list, description="List of agents in this multi-agent system"
    )
    execution_mode: ExecutionMode = Field(
        default=ExecutionMode.SEQUENCE, description="How agents should be executed"
    )

    # Schema configuration
    include_meta: bool = Field(
        default=True, description="Whether to include MetaAgentState for coordination"
    )
    schema_separation: Literal["smart", "shared", "namespaced"] = Field(
        default="smart", description="How to handle field separation in composed schema"
    )

    # Branching configuration
    branches: dict[str, dict[str, Any]] = Field(
        default_factory=dict,
        description="Branch configurations keyed by source node name",
    )

    # Private state management
    _agent_private_states: dict[str, type[BaseModel]] = PrivateAttr(
        default_factory=dict
    )
    _agent_node_mapping: dict[str, str] = PrivateAttr(default_factory=dict)

    @model_validator(mode="before")
    @classmethod
    def validate_agents(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Ensure agents list is not empty."""
        if isinstance(values, dict):
            agents = values.get("agents", [])
            if not agents:
                raise ValueError("MultiAgent requires at least one agent")
        return values

    @model_validator(mode="after")
    def setup_multi_agent(self) -> "MultiAgent":
        """Set up the multi-agent system after initialization."""
        # Generate schema based on execution mode
        build_mode = self._get_build_mode()

        # Compose state schema from agents
        self.state_schema = AgentSchemaComposer.from_agents(
            agents=list(self.agents),
            name=f"{self.__class__.__name__}State",
            include_meta=self.include_meta,
            separation=self.schema_separation,
            build_mode=build_mode,
        )

        # Store private schemas for each agent
        for agent in self.agents:
            agent_id = getattr(agent, "id", agent.name)
            if hasattr(agent, "state_schema") and agent.state_schema:
                self._agent_private_states[agent_id] = agent.state_schema

        # Set input/output schemas
        self._setup_io_schemas()

        return self

    def _get_build_mode(self) -> BuildMode:
        """Map execution mode to build mode."""
        mode_mapping = {
            ExecutionMode.SEQUENCE: BuildMode.SEQUENCE,
            ExecutionMode.PARALLEL: BuildMode.PARALLEL,
            ExecutionMode.CONDITIONAL: BuildMode.SEQUENCE,  # Use sequence for conditional
            ExecutionMode.HIERARCHICAL: BuildMode.HIERARCHICAL,
        }
        return mode_mapping.get(self.execution_mode, BuildMode.CUSTOM)

    def _setup_io_schemas(self) -> None:
        """Set up input and output schemas based on execution mode."""
        if self.execution_mode == ExecutionMode.SEQUENCE:
            # Input from first agent, output from last
            if self.agents:
                first_agent = self.agents[0]
                last_agent = self.agents[-1]

                # Use first agent's input schema or derive from state
                if hasattr(first_agent, "input_schema") and first_agent.input_schema:
                    self.input_schema = first_agent.input_schema
                else:
                    self.input_schema = self.state_schema.derive_input_schema()

                # Use last agent's output schema or derive from state
                if hasattr(last_agent, "output_schema") and last_agent.output_schema:
                    self.output_schema = last_agent.output_schema
                else:
                    self.output_schema = self.state_schema.derive_output_schema()
        else:
            # For other modes, derive from state schema
            self.input_schema = self.state_schema.derive_input_schema()
            self.output_schema = self.state_schema.derive_output_schema()

    def add_conditional_edge(
        self,
        source_agent: str | Agent,
        condition: Callable[[Any], str | bool],
        destinations: dict[str | bool, str | Agent],
        default: str | Agent | None = None,
    ) -> None:
        """Add a conditional edge between agents.

        Args:
            source_agent: Source agent or its name/id
            condition: Function that returns a routing key
            destinations: Mapping of condition results to target agents
            default: Default destination if no match
        """
        # Normalize source
        source_name = self._get_node_name(source_agent)

        # Normalize destinations
        normalized_dests = {}
        for key, dest in destinations.items():
            dest_name = self._get_node_name(dest) if dest != END else END
            normalized_dests[key] = dest_name

        # Store branch configuration
        self.branches[source_name] = {
            "condition": condition,
            "destinations": normalized_dests,
            "default": (
                self._get_node_name(default) if default and default != END else default
            ),
        }

    def _get_node_name(self, agent: str | Agent) -> str:
        """Get the node name for an agent."""
        if isinstance(agent, str):
            # Could be agent name or id
            for a in self.agents:
                if getattr(a, "name", None) == agent or getattr(a, "id", None) == agent:
                    return self._get_agent_node_name(a)
            return agent  # Assume it's a node name
        if isinstance(agent, Agent):
            return self._get_agent_node_name(agent)
        raise ValueError(f"Invalid agent reference: {agent}")

    def _get_agent_node_name(self, agent: Agent) -> str:
        """Get the unique node name for an agent."""
        base_name = getattr(agent, "name", agent.__class__.__name__)
        agent_id = getattr(agent, "id", base_name)

        # Ensure uniqueness
        if agent_id not in self._agent_node_mapping:
            node_name = base_name
            counter = 1
            while any(
                node_name == existing for existing in self._agent_node_mapping.values()
            ):
                node_name = f"{base_name}_{counter}"
                counter += 1
            self._agent_node_mapping[agent_id] = node_name

        return self._agent_node_mapping[agent_id]

    def build_graph(self) -> BaseGraph:
        """Build the graph based on execution mode."""
        graph = BaseGraph(name=self.name)

        # Build based on execution mode
        if self.execution_mode == ExecutionMode.SEQUENCE:
            self._build_sequence_graph(graph)
        elif self.execution_mode == ExecutionMode.PARALLEL:
            self._build_parallel_graph(graph)
        elif self.execution_mode == ExecutionMode.CONDITIONAL:
            self._build_conditional_graph(graph)
        elif self.execution_mode == ExecutionMode.HIERARCHICAL:
            self._build_hierarchical_graph(graph)
        else:
            # Custom mode - must be implemented by subclass
            graph = self.build_custom_graph(graph)

        return graph

    def _build_sequence_graph(self, graph: BaseGraph) -> None:
        """Build a sequential execution graph."""
        node_names = []

        # Add all agents as nodes
        for agent in self.agents:
            node_name = self._get_agent_node_name(agent)
            node_names.append(node_name)

            # Create agent node config
            from haive.core.graph.node.agent_node import AgentNodeConfig

            agent_node = AgentNodeConfig(
                name=node_name,
                agent=agent,
                private_state_schema=self._agent_private_states.get(
                    getattr(agent, "id", agent.name)
                ),
            )
            graph.add_node(node_name, agent_node)

        # Connect in sequence
        for i, node_name in enumerate(node_names):
            if i == 0:
                graph.add_edge(START, node_name)

            # Check for branches
            if node_name in self.branches:
                branch_config = self.branches[node_name]
                graph.add_conditional_edges(
                    node_name,
                    branch_config["condition"],
                    branch_config["destinations"],
                    default=branch_config.get(
                        "default",
                        END if i == len(node_names) - 1 else node_names[i + 1],
                    ),
                )
            elif i == len(node_names) - 1:
                graph.add_edge(node_name, END)
            else:
                graph.add_edge(node_name, node_names[i + 1])

    def _build_parallel_graph(self, graph: BaseGraph) -> None:
        """Build a parallel execution graph."""
        # Create a coordinator node
        coordinator_name = f"{self.name}_coordinator"

        # Add coordinator that fans out
        from haive.core.graph.node.agent_node import CoordinatorNodeConfig

        coordinator = CoordinatorNodeConfig(
            name=coordinator_name, agents=list(self.agents), mode="fanout"
        )
        graph.add_node(coordinator_name, coordinator)
        graph.add_edge(START, coordinator_name)

        # Add all agents
        agent_nodes = []
        for agent in self.agents:
            node_name = self._get_agent_node_name(agent)
            agent_nodes.append(node_name)

            from haive.core.graph.node.agent_node import AgentNodeConfig

            agent_node = AgentNodeConfig(
                name=node_name,
                agent=agent,
                private_state_schema=self._agent_private_states.get(
                    getattr(agent, "id", agent.name)
                ),
            )
            graph.add_node(node_name, agent_node)
            graph.add_edge(coordinator_name, node_name)

        # Create aggregator node
        aggregator_name = f"{self.name}_aggregator"
        aggregator = CoordinatorNodeConfig(
            name=aggregator_name, agents=list(self.agents), mode="aggregate"
        )
        graph.add_node(aggregator_name, aggregator)

        # Connect all agents to aggregator
        for node_name in agent_nodes:
            graph.add_edge(node_name, aggregator_name)

        graph.add_edge(aggregator_name, END)

    def _build_conditional_graph(self, graph: BaseGraph) -> None:
        """Build a conditional execution graph."""
        # Start with sequence and add conditional edges
        self._build_sequence_graph(graph)
        # Conditional edges are already added in sequence building

    def _build_hierarchical_graph(self, graph: BaseGraph) -> None:
        """Build a hierarchical execution graph."""
        # Default implementation - can be overridden
        logger.warning("Hierarchical mode not fully implemented, using sequence")
        self._build_sequence_graph(graph)

    @abstractmethod
    def build_custom_graph(self, graph: BaseGraph) -> BaseGraph:
        """Build a custom graph - must be implemented by subclasses if using CUSTOM mode.

        Args:
            graph: The graph to build on

        Returns:
            The modified graph
        """
        raise NotImplementedError(
            "Subclasses must implement build_custom_graph for CUSTOM mode"
        )

    def get_agent_by_name(self, name: str) -> Agent | None:
        """Get an agent by name or id."""
        for agent in self.agents:
            if (
                getattr(agent, "name", None) == name
                or getattr(agent, "id", None) == name
            ):
                return agent
        return None

    def visualize_structure(self) -> None:
        """Visualize the multi-agent structure."""
        tree = Tree(f"[bold blue]{self.name}[/bold blue] ({self.execution_mode.value})")

        # Add agents
        agents_branch = tree.add("[green]Agents[/green]")
        for agent in self.agents:
            agent_name = getattr(agent, "name", agent.__class__.__name__)
            agent_info = f"{agent_name}"
            if hasattr(agent, "engine") and agent.engine:
                engine_type = getattr(agent.engine, "engine_type", "unknown")
                agent_info += f" (engine: {engine_type})"
            agents_branch.add(agent_info)

        # Add branches
        if self.branches:
            branches_branch = tree.add("[yellow]Conditional Branches[/yellow]")
            for source, config in self.branches.items():
                branch_info = f"{source} → "
                dests = config.get("destinations", {})
                branch_info += ", ".join(f"{k}: {v}" for k, v in dests.items())
                if config.get("default"):
                    branch_info += f" (default: {config['default']})"
                branches_branch.add(branch_info)

        # Add schema info
        schema_branch = tree.add("[cyan]Schema Info[/cyan]")
        if self.state_schema:
            schema_branch.add(
                f"State: {getattr(self.state_schema, '__name__', 'Unknown')}"
            )
        if self.input_schema:
            schema_branch.add(
                f"Input: {getattr(self.input_schema, '__name__', 'Unknown')}"
            )
        if self.output_schema:
            schema_branch.add(
                f"Output: {getattr(self.output_schema, '__name__', 'Unknown')}"
            )

        console.print(tree)


class SequentialAgent(MultiAgent):
    """Pre-configured sequential multi-agent."""

    execution_mode: ExecutionMode = Field(
        default=ExecutionMode.SEQUENCE, description="Sequential execution mode"
    )

    def build_custom_graph(self, graph: BaseGraph) -> BaseGraph:
        """Not needed for sequential mode."""
        return graph


class ParallelAgent(MultiAgent):
    """Pre-configured parallel multi-agent."""

    execution_mode: ExecutionMode = Field(
        default=ExecutionMode.PARALLEL, description="Parallel execution mode"
    )

    def build_custom_graph(self, graph: BaseGraph) -> BaseGraph:
        """Not needed for parallel mode."""
        return graph


class ConditionalAgent(MultiAgent):
    """Pre-configured conditional multi-agent with branching."""

    execution_mode: ExecutionMode = Field(
        default=ExecutionMode.CONDITIONAL, description="Conditional execution mode"
    )

    def build_custom_graph(self, graph: BaseGraph) -> BaseGraph:
        """Not needed for conditional mode."""
        return graph
