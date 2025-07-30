"""Enhanced MultiAgent V4 - Using enhanced base agent pattern.

This implementation follows the enhanced base agent pattern by extending Agent
and implementing build_graph() while being influenced by clean.py's functionality.

Key Features:
- Proper enhanced base agent inheritance
- Implements build_graph() abstract method
- Direct list initialization: agents=[agent1, agent2]
- Build modes: auto, manual, lazy
- Sequential, parallel, conditional execution
- Uses AgentNodeV3 for execution
- Uses MultiAgentState for state management
- Uses BaseGraph2.add_conditional_edges()
"""

from __future__ import annotations

import logging
from collections.abc import Callable
from typing import TYPE_CHECKING, Any, Literal

if TYPE_CHECKING:
    from haive.agents.base.agent import Agent
else:
    try:
        from haive.agents.base.agent import Agent
    except ImportError:
        Agent = None
from haive.core.graph.node.agent_node_v3 import create_agent_node_v3
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.schema.prebuilt.multi_agent_state import MultiAgentState
from langgraph.graph import END, START
from pydantic import Field, model_validator

logger = logging.getLogger(__name__)


class EnhancedMultiAgentV4(Agent):
    """Enhanced MultiAgent V4 using enhanced base agent pattern.

    This class properly extends the enhanced base Agent class and implements
    the build_graph() abstract method. It provides clean initialization with
    direct list support and flexible execution modes.

    Example:
        >>> # Simple sequential
        >>> workflow = EnhancedMultiAgentV4(
        ...     name="my_workflow",
        ...     agents=[planner, executor, reviewer],
        ...     execution_mode="sequential"
        ... )
        >>>
        >>> # With conditional branching
        >>> workflow = EnhancedMultiAgentV4(
        ...     name="smart_workflow",
        ...     agents=[classifier, simple_processor, complex_processor],
        ...     execution_mode="conditional",
        ...     build_mode="manual"
        ... )
        >>>
        >>> # Add conditional edges
        >>> workflow.add_conditional_edge(
        ...     from_agent="classifier",
        ...     condition=lambda state: state.get("complexity") > 0.7,
        ...     true_agent="complex_processor",
        ...     false_agent="simple_processof"
        ... )
        >>>
        >>> # Build and execute
        >>> workflow.build()
        >>> result = await workflow.arun({"task": "Process this data"})
    """

    # ========================================================================
    # CORE FIELDS - Enhanced base agent integration
    # ========================================================================

    agents: list[Agent] = Field(
        default_factory=list, description="List of agents to coordinate"
    )

    execution_mode: Literal["sequential", "parallel", "conditional", "manual"] = Field(
        default="sequential", description="How to execute the agents"
    )

    build_mode: Literal["auto", "manual", "lazy"] = Field(
        default="auto",
        description="When to build the graph: auto (on init), manual (explicit), lazy (on first run)",
    )

    entry_point: str | None = Field(
        default=None, description="Starting agent (defaults to first agent)"
    )

    # Internal state - converted from list
    agent_dict: dict[str, Agent] = Field(
        default_factory=dict, description="Agents converted to dict by name"
    )

    # Conditional edges configuration
    conditional_edges: list[dict[str, Any]] = Field(
        default_factory=list, description="Conditional edge configurations"
    )

    # ========================================================================
    # ENHANCED BASE AGENT SETUP
    # ========================================================================

    @model_validator(mode="after")
    def setup_multi_agent(self):
        """Set up multi-agent after initialization - enhanced base agent pattern."""
        # Convert agents list to dict
        if self.agents:
            self.agent_dict = self._convert_agents_to_dict(self.agents)
            logger.info(f"Converted {len(self.agents)} agents to dict")

        # Set default state schema to MultiAgentState
        if self.state_schema is None:
            self.state_schema = MultiAgentState
            logger.debug("Using default MultiAgentState schema")

        return self

    def _convert_agents_to_dict(self, agents: list[Agent]) -> dict[str, Agent]:
        """Convert agent list to dictionary keyed by name."""
        agent_dict = {}

        for i, agent in enumerate(agents):
            if not hasattr(agent, "name") or not agent.name:
                raise ValueError(f"Agent at index {i} must have a name")

            if agent.name in agent_dict:
                # Handle duplicates by adding index
                agent_dict[f"{agent.name}_{i}"] = agent
                logger.warning(
                    f"Duplicate agent name '{agent.name}', using '{agent.name}_{i}'"
                )
            else:
                agent_dict[agent.name] = agent

        return agent_dict

    # ========================================================================
    # ABSTRACT METHOD IMPLEMENTATION - build_graph()
    # ========================================================================

    def build_graph(self) -> BaseGraph:
        """Build the BaseGraph for this multi-agent - implements abstract method.

        This is the core method required by enhanced base agent pattern.
        Creates the graph based on execution_mode and conditional_edges.
        """
        if not self.agent_dict:
            raise ValueError("No agents to build graph with")

        logger.info(
            f"Building {self.execution_mode} graph with {len(self.agent_dict)} agents"
        )

        # Create BaseGraph with MultiAgentState
        graph = BaseGraph(
            name=f"{self.name}_graph", state_schema=self.state_schema or MultiAgentState
        )

        # Add all agents as nodes using AgentNodeV3
        self._add_agent_nodes(graph)

        # Add edges based on execution mode
        if self.execution_mode == "sequential":
            self._add_sequential_edges(graph)
        elif self.execution_mode == "parallel":
            self._add_parallel_edges(graph)
        elif self.execution_mode == "conditional":
            self._add_conditional_edges(graph)
        elif self.execution_mode == "manual":
            # Manual mode - user adds edges manually
            self._add_manual_edges(graph)

        logger.info("Successfully built multi-agent graph")
        return graph

    def _add_agent_nodes(self, graph: BaseGraph):
        """Add all agents as nodes using AgentNodeV3."""
        for agent_name, agent in self.agent_dict.items():
            # Create AgentNodeV3 for proper state projection
            node_config = create_agent_node_v3(agent_name=agent_name, agent=agent)
            graph.add_node(agent_name, node_config)
            logger.debug(f"Added AgentNodeV3 for: {agent_name}")

    def _add_sequential_edges(self, graph: BaseGraph):
        """Add sequential edges: START -> agent1 -> agent2 -> ... -> END."""
        agent_names = list(self.agent_dict.keys())

        if not agent_names:
            return

        # Determine entry point
        start_agent = (
            self.entry_point if self.entry_point in agent_names else agent_names[0]
        )

        # START -> first agent
        graph.add_edge(START, start_agent)

        # Chain agents sequentially
        for i in range(len(agent_names) - 1):
            current = agent_names[i]
            next_agent = agent_names[i + 1]
            graph.add_edge(current, next_agent)

        # Last agent -> END
        graph.add_edge(agent_names[-1], END)

        logger.info(f"Added sequential edges for {len(agent_names)} agents")

    def _add_parallel_edges(self, graph: BaseGraph):
        """Add parallel edges: START -> all agents -> END."""
        agent_names = list(self.agent_dict.keys())

        # START -> all agents in parallel
        for agent_name in agent_names:
            graph.add_edge(START, agent_name)
            graph.add_edge(agent_name, END)

        logger.info(f"Added parallel edges for {len(agent_names)} agents")

    def _add_conditional_edges(self, graph: BaseGraph):
        """Add conditional edges using BaseGraph2.add_conditional_edges()."""
        # Start with entry point or first agent
        agent_names = list(self.agent_dict.keys())
        start_agent = (
            self.entry_point if self.entry_point in agent_names else agent_names[0]
        )
        graph.add_edge(START, start_agent)

        # Add configured conditional edges
        for edge_config in self.conditional_edges:
            from_agent = edge_config["from_agent"]
            condition = edge_config["condition"]
            destinations = edge_config["destinations"]
            default = edge_config.get("default", END)

            # Use BaseGraph2's add_conditional_edges
            graph.add_conditional_edges(
                source_node=from_agent,
                condition=condition,
                destinations=destinations,
                default=default,
            )

            logger.debug(f"Added conditional edge from {from_agent}")

        # Ensure unconnected agents go to END
        for agent_name in agent_names:
            # Check if agent has outgoing edges configured
            has_outgoing = any(
                edge["from_agent"] == agent_name for edge in self.conditional_edges
            )
            if not has_outgoing and agent_name != start_agent:
                graph.add_edge(agent_name, END)

        logger.info(f"Added conditional edges for {self.execution_mode} mode")

    def _add_manual_edges(self, graph: BaseGraph):
        """Manual mode - minimal setup, user adds edges."""
        # Just ensure START connects to entry point
        agent_names = list(self.agent_dict.keys())
        start_agent = (
            self.entry_point if self.entry_point in agent_names else agent_names[0]
        )
        graph.add_edge(START, start_agent)

        logger.info(
            "Manual mode - user must add edges with add_edge() or add_conditional_edge()"
        )

    # ========================================================================
    # USER-FRIENDLY EDGE METHODS
    # ========================================================================

    def add_edge(self, from_agent: str, to_agent: str):
        """Add direct edge between agents."""
        if from_agent not in self.agent_dict:
            raise ValueError(f"Agent '{from_agent}' not found")
        if to_agent not in self.agent_dict and to_agent != END:
            raise ValueError(f"Agent '{to_agent}' not found")

        # If graph is built, add edge directly
        if hasattr(self, "graph") and self.graph:
            self.graph.add_edge(from_agent, to_agent)
            logger.info(f"Added direct edge: {from_agent} -> {to_agent}")
        else:
            logger.warning("Graph not built yet, edge will be added on build")

    def add_conditional_edge(
        self,
        from_agent: str,
        condition: Callable[[Any], bool],
        true_agent: str,
        false_agent: str = END,
    ):
        """Add conditional edge with boolean condition."""
        if from_agent not in self.agent_dict:
            raise ValueError(f"Agent '{from_agent}' not found")

        # Store configuration
        edge_config = {
            "from_agent": from_agent,
            "condition": condition,
            "destinations": {True: true_agent, False: false_agent},
            "default": false_agent,
        }
        self.conditional_edges.append(edge_config)

        # If graph is built, add edge directly
        if hasattr(self, "graph") and self.graph:
            self.graph.add_conditional_edges(
                source_node=from_agent,
                condition=condition,
                destinations={True: true_agent, False: false_agent},
                default=false_agent,
            )
            logger.info(f"Added conditional edge from {from_agent}")

        logger.info(
            f"Configured conditional edge: {from_agent} -> {true_agent}/{false_agent}"
        )

    def add_multi_conditional_edge(
        self,
        from_agent: str,
        condition: Callable[[Any], str],
        routes: dict[str, str],
        default: str = END,
    ):
        """Add multi-way conditional edge."""
        if from_agent not in self.agent_dict:
            raise ValueError(f"Agent '{from_agent}' not found")

        # Store configuration
        edge_config = {
            "from_agent": from_agent,
            "condition": condition,
            "destinations": routes,
            "default": default,
        }
        self.conditional_edges.append(edge_config)

        # If graph is built, add edge directly
        if hasattr(self, "graph") and self.graph:
            self.graph.add_conditional_edges(
                source_node=from_agent,
                condition=condition,
                destinations=routes,
                default=default,
            )

        logger.info(
            f"Configured multi-conditional edge from {from_agent} with {len(routes)} routes"
        )

    # ========================================================================
    # UTILITY METHODS
    # ========================================================================

    def get_agent_names(self) -> list[str]:
        """Get list of agent names."""
        return list(self.agent_dict.keys())

    def get_agent(self, name: str) -> Agent | None:
        """Get agent by name."""
        return self.agent_dict.get(name)

    def add_agent(self, agent: Agent):
        """Add agent dynamically."""
        if not agent.name:
            raise ValueError("Agent must have a name")

        if agent.name in self.agent_dict:
            raise ValueError(f"Agent '{agent.name}' already exists")

        self.agent_dict[agent.name] = agent
        self.agents.append(agent)

        # Rebuild graph if auto mode and already built
        if self.build_mode == "auto" and hasattr(self, "graph") and self.graph:
            self.rebuild_graph()

        logger.info(f"Added agent: {agent.name}")

    def display_info(self):
        """Display workflow information."""
        print(f"\n=== Enhanced MultiAgent V4: {self.name} ===")
        print(f"Execution Mode: {self.execution_mode}")
        print(f"Build Mode: {self.build_mode}")
        print(f"Entry Point: {self.entry_point or 'auto'}")
        print(f"Agents ({len(self.agent_dict)}):")

        for i, (name, agent) in enumerate(self.agent_dict.items(), 1):
            agent_type = type(agent).__name__
            print(f"  {i}. {name} ({agent_type})")

        print(f"Conditional Edges: {len(self.conditional_edges)}")
        print(
            f"Graph Built: {'Yes' if hasattr(self, 'graph') and self.graph else 'No'}"
        )
        print()

    # ========================================================================
    # ENHANCED BASE AGENT INTEGRATION
    # ========================================================================

    # The enhanced base agent provides:
    # - Automatic graph building based on build_mode
    # - Schema generation and management
    # - Persistence capabilities
    # - Standard run/arun interface
    # - All mixin functionality (execution, state, persistence, etc.)

    # We just implement build_graph() and the enhanced base agent handles the rest!
