"""Clean Multi-Agent Implementation using AgentNodeV3.

from typing import Any, Dict
This module provides a clean multi-agent system that:
- Uses AgentNodeV3 for proper state projection
- Emulates the engines dict pattern from base Agent
- Supports private state passing between agents
- Maintains type safety without schema flattening
"""

import logging
from typing import Any, Literal

from haive.agents.base.agent import Agent
from haive.core.graph.node.agent_node_v3 import AgentNodeV3Config
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.schema.state_schema import StateSchema
from langgraph.graph import END, START
from pydantic import Field, PrivateAttr, model_validator
from typing_extensions import TypedDict

logger = logging.getLogger(__name__)


# Minimal shared state for multi-agent coordination
class MinimalMultiAgentState(TypedDict):
    """Minimal state for multi-agent coordination."""

    current_agent: str | None
    completed_agents: list[str]
    final_result: Any | None
    error: str | None


# Container pattern for more complex multi-agent scenarios
class ContainerMultiAgentState(StateSchema):
    """Container pattern with isolated agent states."""

    agents: dict[str, Agent] = Field(default_factory=dict)
    agent_states: dict[str, dict[str, Any]] = Field(default_factory=dict)
    shared_context: dict[str, Any] = Field(default_factory=dict)

    # Coordination fields
    current_agent: str | None = Field(default=None)
    completed_agents: list[str] = Field(default_factory=list)
    final_result: Any | None = Field(default=None)
    error: str | None = Field(default=None)


class MultiAgent(Agent):
    """Multi-agent coordinator using AgentNodeV3 for proper state management.

    This class provides a clean implementation that:
    - Emulates the engines dict pattern from base Agent
    - Uses AgentNodeV3 for each agent with state projection
    - Supports both list and dict agent specifications
    - Maintains type safety without schema flattening

    Example:
        Sequential execution::

            multi = MultiAgent(
                agents=[react_agent, simple_agent],
                mode="sequential"
            )

        With dict specification::

            multi = MultiAgent(
                agents={
                    "reasoner": react_agent,
                    "formatter": simple_agent
                }
            )
    """

    # Agents storage - emulating engines dict pattern
    agents: list[Agent] | dict[str, Agent] = Field(
        ..., description="Agents to coordinate - can be list or dict like engines"
    )

    # Execution mode
    mode: Literal["sequential", "conditional", "parallel"] = Field(
        default="sequential", description="Execution mode for agents"
    )

    # State management strategy
    state_strategy: Literal["minimal", "container", "custom"] = Field(
        default="minimal", description="State management strategy"
    )

    # Shared fields between agents
    shared_fields: list[str] = Field(
        default_factory=list,
        description="Fields shared between agents (empty for private state passing)",
    )

    # State transfer rules
    state_transfer_map: dict[str, dict[str, str]] = Field(
        default_factory=dict, description="Maps agent outputs to next agent inputs"
    )

    # For conditional routing
    routing_function: Any | None = Field(
        default=None, description="Function for conditional routing"
    )

    # Internal registries (like engines registry)
    _agent_registry: dict[str, Agent] = PrivateAttr(default_factory=dict)
    _agent_order: list[str] = PrivateAttr(default_factory=list)

    @model_validator(mode="after")
    def normalize_agents(cls) -> "MultiAgent":
        """Normalize agents into registry dict, similar to engines normalization."""
        # Clear registries
        self._agent_registry.clear()
        self._agent_order.clear()

        if isinstance(self.agents, list):
            # Convert list to dict with agent names
            for agent in self.agents:
                agent_name = agent.name
                # Ensure unique names
                if agent_name in self._agent_registry:
                    i = 1
                    while f"{agent_name}_{i}" in self._agent_registry:
                        i += 1
                    agent_name = f"{agent_name}_{i}"

                self._agent_registry[agent_name] = agent
                self._agent_order.append(agent_name)

        elif isinstance(self.agents, dict):
            # Use dict directly
            self._agent_registry.update(self.agents)
            self._agent_order.extend(self.agents.keys())
        else:
            raise ValueError("agents must be a list or dict")

        return self

    def setup_agent(self) -> None:
        """Setup multi-agent specific configuration."""
        # Set our state schema based on strategy
        if self.state_strategy == "minimal":
            self.state_schema = MinimalMultiAgentState
        elif self.state_strategy == "container":
            self.state_schema = ContainerMultiAgentState
        # else: use custom state_schema if provided

        # Force schema regeneration
        self.set_schema = True

    def build_graph(self) -> BaseGraph:
        """Build graph using AgentNodeV3 for each agent."""
        # Create graph with appropriate state schema
        graph = BaseGraph(
            name=f"{
                self.name}_graph",
            state_schema=self.state_schema,
        )

        # Add each agent using AgentNodeV3Config
        for agent_name, agent in self._agent_registry.items():
            # Create AgentNodeV3Config directly (no create function)
            node_config = AgentNodeV3Config(
                name=f"agent_{agent_name}",  # Node name
                agent_name=agent_name,  # Agent lookup key
                agent=agent,  # Agent instance
                project_state=True,  # Enable state projection
                extract_from_container=(self.state_strategy == "container"),
                shared_fields=self.shared_fields,
                update_container_state=(self.state_strategy == "container"),
            )

            # Add node to graph
            graph.add_node(f"agent_{agent_name}", node_config)

        # Build edges based on mode
        if self.mode == "sequential":
            self._build_sequential_edges(graph)
        elif self.mode == "conditional":
            self._build_conditional_edges(graph)
        elif self.mode == "parallel":
            self._build_parallel_edges(graph)

        return graph

    def _build_sequential_edges(self, graph: BaseGraph):
        """Build sequential execution edges."""
        # Simple sequential flow
        prev_node = START

        for agent_name in self._agent_order:
            node_name = f"agent_{agent_name}"
            graph.add_edge(prev_node, node_name)
            prev_node = node_name

        graph.add_edge(prev_node, END)

    def _build_conditional_edges(self, graph: BaseGraph):
        """Build conditional routing edges."""
        if not self.routing_function:
            raise ValueError("routing_function required for conditional mode")

        # Start with first agent
        first_agent = self._agent_order[0]
        graph.add_edge(START, f"agent_{first_agent}")

        # Add conditional routing after each agent
        for i, agent_name in enumerate(self._agent_order[:-1]):
            node_name = f"agent_{agent_name}"

            # Create routing map
            route_map = {
                next_agent: f"agent_{next_agent}"
                for next_agent in self._agent_order[i + 1 :]
            }
            route_map[END] = END

            # Add conditional edges
            graph.add_conditional_edges(node_name, self.routing_function, route_map)

        # Last agent goes to END
        last_agent = self._agent_order[-1]
        graph.add_edge(f"agent_{last_agent}", END)

    def _build_parallel_edges(self, graph: BaseGraph):
        """Build parallel execution edges."""

        # Add aggregator node
        def aggregate_results(_state: dict[str, Any]):
            """Aggregate results from parallel agents."""
            return {"final_result": "Aggregated results"}

        graph.add_node("aggregator", aggregate_results)

        # All agents start from START
        for agent_name in self._agent_order:
            node_name = f"agent_{agent_name}"
            graph.add_edge(START, node_name)
            graph.add_edge(node_name, "aggregator")

        graph.add_edge("aggregator", END)

    def __repr__(self) -> str:
        agent_info = f"agents={len(self._agent_registry)}"
        mode_info = f"mode={self.mode}"
        strategy_info = f"strategy={self.state_strategy}"
        return f"MultiAgent(name='{
            self.name}', {agent_info}, {mode_info}, {strategy_info})"


class SequentialAgent(MultiAgent):
    """Sequential multi-agent execution.

    Example:
        agent = SequentialAgent([react_agent, simple_agent])
    """

    mode: Literal["sequential"] = Field(default="sequential", const=True)

    def __init__(self, agents: list[Agent], **kwargs):
        """Initialize with list of agents for sequential execution."""
        super().__init__(agents=agents, mode="sequential", **kwargs)


class ConditionalAgent(MultiAgent):
    """Conditional routing multi-agent.

    Example:
        agent = ConditionalAgent(
            agents={"analyzer": analyzer, "synthesizer": synthesizer},
            routing_function=my_router
        )
    """

    mode: Literal["conditional"] = Field(default="conditional", const=True)

    def __init__(self, agents: dict[str, Agent], routing_function: Any, **kwargs):
        """Initialize with agents dict and routing function."""
        super().__init__(
            agents=agents,
            mode="conditional",
            routing_function=routing_function,
            **kwargs,
        )
