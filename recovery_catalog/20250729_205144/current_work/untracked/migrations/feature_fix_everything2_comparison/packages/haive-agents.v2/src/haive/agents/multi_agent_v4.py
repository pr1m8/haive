"""MultiAgent V4 - Clean implementation using enhanced base agent.

This implementation follows the V4 pattern with:
- Enhanced base agent integration
- MultiAgentState usage
- AgentNodeV3 execution
- Simple list initialization
- Incremental build-up approach

Start small, test incrementally, build up features.
"""

from __future__ import annotations

import logging
from typing import Any, Literal

from haive.core.graph.node.agent_node_v3 import create_agent_node_v3
from haive.core.schema.prebuilt.multi_agent_state import MultiAgentState
from langgraph.graph import END, START, StateGraph
from langgraph.graph.graph import CompiledGraph
from pydantic import Field, model_validator

from haive.agents.base.agent import Agent

logger = logging.getLogger(__name__)


class MultiAgentV4(Agent):
    """V4 Multi-agent coordinator using enhanced base agent.

    Simple, clean implementation that starts small and builds incrementally.
    Uses MultiAgentState and AgentNodeV3 for proper integration.

    Example:
        >>> from haive.agents.simple.agent import SimpleAgent
        >>> from haive.agents.react.agent import ReactAgent
        >>>
        >>> # Create agents
        >>> planner = ReactAgent(name="planner", engine=config, tools=[...])
        >>> writer = SimpleAgent(name="writer", engine=config)
        >>>
        >>> # Create multi-agent (simple list initialization)
        >>> workflow = MultiAgentV4(
        ...     name="content_workflow",
        ...     agents=[planner, writer],
        ...     execution_mode="sequential"
        ... )
        >>>
        >>> # Execute
        >>> result = await workflow.arun({"task": "Write an article"})
    """

    # ========================================================================
    # CORE FIELDS - Start simple
    # ========================================================================

    agents: list[Agent] = Field(
        default_factory=list,
        description="List of agents to coordinate (converted to dict internally)",
    )

    execution_mode: Literal["sequential", "parallel"] = Field(
        default="sequential", description="How to execute the agents"
    )

    build_mode: Literal["auto", "manual", "lazy"] = Field(
        default="auto", description="When to build the execution graph"
    )

    # Internal state - use PrivateAttr for internal fields
    agent_dict: dict[str, Agent] = Field(
        default_factory=dict,
        description="Internal agent dictionary (converted from list)",
    )

    execution_graph: CompiledGraph | None = Field(
        default=None, description="Compiled LangGraph for execution"
    )

    state_schema: type[MultiAgentState] = Field(
        default=MultiAgentState, description="State schema to use"
    )

    # ========================================================================
    # VALIDATION - Convert list to dict, validate agents
    # ========================================================================

    @model_validator(mode="after")
    def setup_multi_agent(self):
        """Set up multi-agent system after initialization."""
        # Convert agent list to dict
        if self.agents:
            self.agent_dict = self._convert_agents_to_dict(self.agents)
            logger.info(
                f"Converted {len(self.agents)} agents to dict: {list(self.agent_dict.keys())}"
            )

        # Handle build mode
        if self.build_mode == "auto":
            # Build graph automatically
            self._build_execution_graph()

        return self

    def _convert_agents_to_dict(self, agents: list[Agent]) -> dict[str, Agent]:
        """Convert agent list to dictionary keyed by name."""
        agent_dict = {}

        for i, agent in enumerate(agents):
            # Ensure agent has name
            if not hasattr(agent, "name") or not agent.name:
                raise ValueError(f"Agent at index {i} must have a name: {agent}")

            # Check for duplicates
            if agent.name in agent_dict:
                raise ValueError(f"Duplicate agent name: {agent.name}")

            agent_dict[agent.name] = agent

        return agent_dict

    # ========================================================================
    # GRAPH BUILDING - Start with simple sequential
    # ========================================================================

    def _build_execution_graph(self) -> CompiledGraph:
        """Build LangGraph for agent execution."""
        if not self.agent_dict:
            raise ValueError("No agents to build graph with")

        logger.info(
            f"Building {self.execution_mode} execution graph for {len(self.agent_dict)} agents"
        )

        # Create state graph with MultiAgentState
        graph = StateGraph(self.state_schema)

        # Add agent nodes using AgentNodeV3
        for agent_name, _agent in self.agent_dict.items():
            node_func = create_agent_node_v3(agent_name)
            graph.add_node(agent_name, node_func)
            logger.debug(f"Added node for agent: {agent_name}")

        # Add edges based on execution mode
        if self.execution_mode == "sequential":
            self._add_sequential_edges(graph)
        elif self.execution_mode == "parallel":
            self._add_parallel_edges(graph)

        # Compile graph
        self.execution_graph = graph.compile()
        logger.info("Successfully compiled execution graph")

        return self.execution_graph

    def _add_sequential_edges(self, graph: StateGraph):
        """Add sequential edges: START -> agent1 -> agent2 -> ... -> END."""
        agent_names = list(self.agent_dict.keys())

        if not agent_names:
            return

        # START -> first agent
        graph.add_edge(START, agent_names[0])

        # Chain agents sequentially
        for i in range(len(agent_names) - 1):
            current = agent_names[i]
            next_agent = agent_names[i + 1]
            graph.add_edge(current, next_agent)
            logger.debug(f"Added edge: {current} -> {next_agent}")

        # Last agent -> END
        graph.add_edge(agent_names[-1], END)

        logger.info(f"Added sequential edges for {len(agent_names)} agents")

    def _add_parallel_edges(self, graph: StateGraph):
        """Add parallel edges: START -> all agents -> END."""
        agent_names = list(self.agent_dict.keys())

        # START -> all agents in parallel
        for agent_name in agent_names:
            graph.add_edge(START, agent_name)
            graph.add_edge(agent_name, END)

        logger.info(f"Added parallel edges for {len(agent_names)} agents")

    # ========================================================================
    # EXECUTION - Simple execution with MultiAgentState
    # ========================================================================

    async def arun(self, input_data: Any, **kwargs) -> Any:
        """Execute the multi-agent workflow."""
        # Ensure graph is built
        if not self.execution_graph:
            if self.build_mode == "manual":
                raise RuntimeError(
                    "Graph not built. Call build() first or use auto build mode."
                )
            self._build_execution_graph()

        # Create initial state
        initial_state = self._create_initial_state(input_data)

        logger.info(
            f"Executing {self.execution_mode} workflow with {len(self.agent_dict)} agents"
        )
        logger.debug(f"Initial state keys: {list(initial_state.__dict__.keys())}")

        # Execute graph
        try:
            final_state = await self.execution_graph.ainvoke(initial_state)
            logger.info("Workflow execution completed successfully")

            return self._extract_result(final_state)

        except Exception as e:
            logger.error(f"Workflow execution failed: {e}")
            raise

    def _create_initial_state(self, input_data: Any) -> MultiAgentState:
        """Create initial MultiAgentState from input."""
        # Convert agents dict to the format expected by MultiAgentState
        agents_for_state = self.agent_dict

        # Create state
        if isinstance(input_data, dict):
            state_data = input_data.copy()
        else:
            state_data = {"input": input_data}

        state_data["agents"] = agents_for_state

        initial_state = self.state_schema(**state_data)

        logger.debug(f"Created initial state with {initial_state.agent_count} agents")
        return initial_state

    def _extract_result(self, final_state: MultiAgentState) -> Any:
        """Extract final result from state."""
        # Simple result extraction - can be enhanced later
        if (
            hasattr(final_state, "final_result")
            and final_state.final_result is not None
        ):
            return final_state.final_result

        # Return agent outputs if no final result
        if final_state.agent_outputs:
            return final_state.agent_outputs

        # Return the full state as fallback
        return final_state

    # ========================================================================
    # UTILITY METHODS - Simple interface
    # ========================================================================

    def build(self) -> CompiledGraph:
        """Manually build the execution graph."""
        return self._build_execution_graph()

    def add_agent(self, agent: Agent) -> None:
        """Add an agent to the workflow."""
        if not agent.name:
            raise ValueError("Agent must have a name")

        if agent.name in self.agent_dict:
            raise ValueError(f"Agent with name '{agent.name}' already exists")

        self.agent_dict[agent.name] = agent
        self.agents.append(agent)  # Keep list in sync

        # Rebuild graph if auto mode
        if self.build_mode == "auto" and self.execution_graph:
            self._build_execution_graph()

        logger.info(f"Added agent: {agent.name}")

    def get_agent_names(self) -> list[str]:
        """Get list of agent names."""
        return list(self.agent_dict.keys())

    def get_agent(self, name: str) -> Agent | None:
        """Get agent by name."""
        return self.agent_dict.get(name)

    # ========================================================================
    # DEBUG METHODS - Simple debugging
    # ========================================================================

    def display_workflow_info(self) -> None:
        """Display workflow information."""
        print(f"\n=== MultiAgent V4: {self.name} ===")
        print(f"Execution Mode: {self.execution_mode}")
        print(f"Build Mode: {self.build_mode}")
        print(f"Agents ({len(self.agent_dict)}):")

        for i, (name, agent) in enumerate(self.agent_dict.items(), 1):
            agent_type = type(agent).__name__
            print(f"  {i}. {name} ({agent_type})")

        print(f"Graph Built: {'Yes' if self.execution_graph else 'No'}")
        print()

    # ========================================================================
    # INHERITED METHODS - From enhanced base agent
    # ========================================================================

    # The enhanced base agent provides:
    # - Standard run/arun interface
    # - Persistence capabilities
    # - State management
    # - Tool integration
    # - All the mixin functionality

    # We just need to implement the core execution logic above
