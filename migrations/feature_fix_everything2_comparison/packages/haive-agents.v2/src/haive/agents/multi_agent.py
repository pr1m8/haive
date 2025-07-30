"""Multi_Agent core module.

This module provides multi agent functionality for the Haive framework.

Classes:
    MultiAgent: MultiAgent implementation.

Functions:
    setup_agent: Setup Agent functionality.
    build_graph: Build Graph functionality.
"""

# src/haive/agents/multi/multi_agent.py

import logging
from typing import Any

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.node.agent_node_v3 import AgentNodeV3Config
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from langgraph.graph import END, START
from pydantic import Field

from haive.agents.base import Agent

logger = logging.getLogger(__name__)


class MultiAgent(Agent):
    """Multi-agent coordinator that manages multiple agents.

    This is a clean implementation that orchestrates multiple agents
    in sequence, parallel, or conditional execution patterns.

    The MultiAgent provides three execution modes:
    - sequence: Agents execute one after another
    - parallel: All agents execute simultaneously
    - conditional: A coordinator LLM routes to appropriate agents

    Attributes:
        agents: Dictionary of agents to coordinate by name.
        execution_mode: How to execute agents (sequence/parallel/conditional).
        coordinator_config: Optional LLM config for conditional routing.

    Examples:
        Sequential execution::

            from haive.agents.multi import MultiAgent
            from haive.agents.simple import SimpleAgent

            writer = SimpleAgent(name="writer")
            editor = SimpleAgent(name="editor")

            pipeline = MultiAgent(
                name="content_pipeline",
                agents={"writer": writer, "editor": editor},
                execution_mode="sequence"
            )
            result = pipeline.run("Write and edit a blog post about AI")

        Parallel execution::

            analyzer1 = SimpleAgent(name="sentiment")
            analyzer2 = SimpleAgent(name="keywords")
            analyzer3 = SimpleAgent(name="summary")

            parallel = MultiAgent(
                name="text_analysis",
                agents={
                    "sentiment": analyzer1,
                    "keywords": analyzer2,
                    "summary": analyzer3
                },
                execution_mode="parallel"
            )
            results = parallel.run("Analyze this text...")

        Conditional routing::

            from haive.core.engine.aug_llm import AugLLMConfig

            coder = SimpleAgent(name="coder")
            writer = SimpleAgent(name="writer")

            router = MultiAgent(
                name="smart_assistant",
                agents={"coder": coder, "writer": writer},
                execution_mode="conditional",
                coordinator_config=AugLLMConfig(temperature=0.1)
            )
            # Coordinator will route to appropriate agent
            result = router.run("Write a Python function to sort a list")

    Note:
        In conditional mode, the coordinator LLM decides which agent to use
        based on the input. The routing is done by simple name matching in
        the coordinator's response.

    See Also:
        haive.agents.supervisor.SupervisorAgent: More advanced routing logic
        haive.agents.simple.SimpleAgent: Basic agent implementation
    """

    # ========================================================================
    # MULTI-AGENT SPECIFIC FIELDS
    # ========================================================================

    agents: dict[str, Agent] = Field(
        default_factory=dict, description="Dictionary of agents to coordinate"
    )

    execution_mode: str = Field(
        default="sequence",
        description="Execution mode: sequence, parallel, or conditional",
    )

    # Coordinator LLM for routing decisions (optional)
    coordinator_config: AugLLMConfig | None = Field(
        default=None, description="LLM config for coordination decisions"
    )

    # ========================================================================
    # SETUP
    # ========================================================================

    def setup_agent(self) -> None:
        """Setup multi-agent coordination."""
        # If we have a coordinator config, use it as the engine
        if self.coordinator_config:
            self.engine = self.coordinator_config
            self.engines["coordinator"] = self.coordinator_config

        # Add all sub-agents to engines
        for name, agent in self.agents.items():
            self.engines[f"agent_{name}"] = agent

        # Set schema flag
        self.set_schema = True

    # ========================================================================
    # GRAPH BUILDING
    # ========================================================================

    def build_graph(self) -> BaseGraph:
        """Build multi-agent coordination graph."""
        graph = BaseGraph(name=self.name)

        if self.execution_mode == "sequence":
            return self._build_sequence_graph(graph)
        if self.execution_mode == "parallel":
            return self._build_parallel_graph(graph)
        if self.execution_mode == "conditional":
            return self._build_conditional_graph(graph)
        raise ValueError(f"Unknown execution mode: {self.execution_mode}")

    def _build_sequence_graph(self, graph: BaseGraph) -> BaseGraph:
        """Build sequential execution graph."""
        # Add agent nodes in sequence
        agent_names = list(self.agents.keys())

        if not agent_names:
            raise ValueError("No agents to coordinate")

        # Start with first agent
        first_agent = agent_names[0]
        first_node = AgentNodeV3Config(
            name=f"{first_agent}_node", agent=self.agents[first_agent]
        )
        graph.add_node(f"{first_agent}_node", first_node)
        graph.add_edge(START, f"{first_agent}_node")

        # Chain remaining agents
        for i in range(1, len(agent_names)):
            prev_agent = agent_names[i - 1]
            curr_agent = agent_names[i]

            curr_node = AgentNodeV3Config(
                name=f"{curr_agent}_node", agent=self.agents[curr_agent]
            )
            graph.add_node(f"{curr_agent}_node", curr_node)
            graph.add_edge(f"{prev_agent}_node", f"{curr_agent}_node")

        # Connect last agent to END
        last_agent = agent_names[-1]
        graph.add_edge(f"{last_agent}_node", END)

        return graph

    def _build_parallel_graph(self, graph: BaseGraph) -> BaseGraph:
        """Build parallel execution graph."""
        # Add all agents in parallel
        for name, agent in self.agents.items():
            node = AgentNodeV3Config(name=f"{name}_node", agent=agent)
            graph.add_node(f"{name}_node", node)
            graph.add_edge(START, f"{name}_node")
            graph.add_edge(f"{name}_node", END)

        return graph

    def _build_conditional_graph(self, graph: BaseGraph) -> BaseGraph:
        """Build conditional execution graph with coordinator."""
        if not self.coordinator_config:
            raise ValueError("Conditional mode requires coordinator_config")

        # Add coordinator node
        from haive.core.graph.node.engine_node import EngineNodeConfig

        coordinator_node = EngineNodeConfig(
            name="coordinator", engine=self.coordinator_config
        )
        graph.add_node("coordinator", coordinator_node)
        graph.add_edge(START, "coordinator")

        # Add agent nodes
        for name, agent in self.agents.items():
            node = AgentNodeV3Config(name=f"{name}_node", agent=agent)
            graph.add_node(f"{name}_node", node)
            graph.add_edge(f"{name}_node", END)

        # Add conditional routing from coordinator
        def route_to_agent(state: dict[str, Any]) -> str:
            """Route to appropriate agent based on coordinator output."""
            messages = state.get("messages", [])
            if messages and hasattr(messages[-1], "content"):
                content = messages[-1].content.lower()
                # Simple routing based on content
                for agent_name in self.agents:
                    if agent_name.lower() in content:
                        return f"{agent_name}_node"
            # Default to first agent
            return f"{next(iter(self.agents.keys()))}_node"

        # Create route map
        route_map = {f"{name}_node": f"{name}_node" for name in self.agents}

        graph.add_conditional_edges("coordinator", route_to_agent, route_map)

        return graph

    # ========================================================================
    # CONVENIENCE METHODS
    # ========================================================================

    def add_agent(self, name: str, agent: Agent) -> None:
        """Add an agent to the multi-agent system.

        Args:
            name: Unique name for the agent.
            agent: The agent instance to add.

        Note:
            The graph is not automatically rebuilt after adding agents.
            You may need to rebuild the graph for changes to take effect.
        """
        self.agents[name] = agent
        self.engines[f"agent_{name}"] = agent

    def remove_agent(self, name: str) -> None:
        """Remove an agent from the system.

        Args:
            name: Name of the agent to remove.

        Note:
            Does nothing if the agent doesn't exist.
            The graph is not automatically rebuilt.
        """
        if name in self.agents:
            del self.agents[name]
            del self.engines[f"agent_{name}"]

    def get_agent(self, name: str) -> Agent | None:
        """Get an agent by name.

        Args:
            name: Name of the agent to retrieve.

        Returns:
            The agent instance or None if not found.
        """
        return self.agents.get(name)
