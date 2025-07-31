"""Enhanced Clean Multi-Agent Implementation using Agent[AugLLMConfig].

MultiAgent = Agent[AugLLMConfig] + agent coordination + state management.

This combines the enhanced agent pattern with the clean multi-agent approach:
- Uses Agent[AugLLMConfig] as the base
- Supports AgentNodeV3 for state projection
- Maintains the engines dict pattern
- Provides multiple state management strategies
"""

import logging
from typing import Any, Literal

from haive.core.engine.aug_llm.config import AugLLMConfig
from haive.core.graph.node.agent_node_v3 import AgentNodeV3Config
from haive.core.graph.node.engine_node import EngineNodeConfig
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.schema.state_schema import StateSchema
from langchain_core.messages import BaseMessage
from langgraph.graph import END, START
from pydantic import Field, field_validator, model_validator
from typing_extensions import TypedDict

# Import base enhanced agent when available
# from haive.agents.base.enhanced_agent import Agent
from haive.agents.simple.enhanced_simple_real import EnhancedAgentBase as Agent

logger = logging.getLogger(__name__)


# State schemas for different strategies
class MinimalMultiAgentState(TypedDict):
    """Minimal state for multi-agent coordination."""

    current_agent: str | None
    completed_agents: list[str]
    final_result: Any | None
    error: str | None
    messages: list[BaseMessage]


class ContainerMultiAgentState(StateSchema):
    """Container pattern with isolated agent states and MetaStateSchema support."""

    # Agent storage
    agents: dict[str, Agent] = Field(default_factory=dict)
    agent_states: dict[str, dict[str, Any]] = Field(default_factory=dict)

    # Shared context
    shared_context: dict[str, Any] = Field(default_factory=dict)
    messages: list[BaseMessage] = Field(default_factory=list)

    # Coordination fields
    current_agent: str | None = Field(default=None)
    completed_agents: list[str] = Field(default_factory=list)
    final_result: Any | None = Field(default=None)
    error: str | None = Field(default=None)

    # MetaStateSchema compatibility
    execution_count: int = Field(default=0)
    needs_recompile: bool = Field(default=False)


class EnhancedMultiAgent(Agent):  # Will be Agent[AugLLMConfig] when imports fixed
    """Enhanced Multi-Agent coordinator with flexible state management.

    MultiAgent = Agent[AugLLMConfig] + agent coordination + state projection.

    Key features:
    1. Uses AgentNodeV3 for proper state projection
    2. Supports multiple execution modes (sequential, parallel, conditional)
    3. Flexible state management strategies
    4. Compatible with MetaStateSchema for meta-capabilities

    Attributes:
        agents: List or dict of agents to coordinate
        mode: Execution mode (sequential, parallel, conditional)
        state_strategy: State management approach
        shared_fields: Fields shared between agents
        state_transfer_map: Rules for transferring state between agents

    Examples:
        Sequential with state transfer::

            multi = EnhancedMultiAgent(
                name="pipeline",
                agents=[planner, executor, reviewer],
                mode="sequential",
                state_transfer_map={
                    ("planner", "executof"): {"plan": "task_plan"},
                    ("executor", "reviewef"): {"result": "execution_result"}
                }
            )

        Parallel with aggregation::

            multi = EnhancedMultiAgent(
                name="ensemble",
                agents={"expert1": agent1, "expert2": agent2},
                mode="parallel",
                state_strategy="containef"
            )

        With MetaStateSchema::

            from haive.core.schema.prebuilt.meta_state import MetaStateSchema

            meta_multi = MetaStateSchema.from_agent(
                agent=multi,
                initial_state={"shared_context": {"project": "AI"}}
            )
    """

    # Agent storage - emulating engines dict pattern
    agents: list[Agent] | dict[str, Agent] = Field(
        ..., description="Agents to coordinate - list or dict like engines"
    )

    # Execution mode
    mode: Literal["sequential", "parallel", "conditional"] = Field(
        default="sequential", description="How agents are executed"
    )

    # State management
    state_strategy: Literal["minimal", "container", "custom"] = Field(
        default="minimal", description="State management approach"
    )

    state_schema: type[StateSchema] | None = Field(
        default=None, description="Custom state schema if strategy is 'custom'"
    )

    # State sharing configuration
    shared_fields: list[str] = Field(
        default_factory=lambda: ["messages"],
        description="Fields shared between all agents",
    )

    state_transfer_map: dict[tuple[str, str], dict[str, str]] = Field(
        default_factory=dict, description="State transfer rules between agents"
    )

    # Coordinator configuration
    coordinator_prompt: str | None = Field(
        default=None, description="Custom coordinator prompt"
    )

    temperature: float = Field(default=0.3, ge=0.0, le=2.0)

    @field_validator("agents")
    @classmethod
    def validate_agents(
        cls, v: list[Agent] | dict[str, Agent]
    ) -> list[Agent] | dict[str, Agent]:
        """Validate and normalize agents."""
        if isinstance(v, list):
            if not v:
                raise ValueError("Agent list cannot be empty")
            # Convert to dict for consistency
            return {f"agent_{i}": agent for i, agent in enumerate(v)}
        if isinstance(v, dict):
            if not v:
                raise ValueError("Agent dict cannot be empty")
            return v
        raise ValueError("Agents must be list or dict")

    @model_validator(mode="after")
    def setup_state_schema(self) -> "EnhancedMultiAgent":
        """Setup appropriate state schema based on strategy."""
        if self.state_strategy == "minimal":
            self.state_schema = MinimalMultiAgentState
        elif self.state_strategy == "container":
            self.state_schema = ContainerMultiAgentState
        elif self.state_strategy == "custom" and not self.state_schema:
            raise ValueError("Custom strategy requires state_schema")

        return self

    def get_agent_names(self) -> list[str]:
        """Get list of agent names."""
        if isinstance(self.agents, dict):
            return list(self.agents.keys())
        return [f"agent_{i}" for i in range(len(self.agents))]

    def get_agent(self, name: str) -> Agent | None:
        """Get agent by name."""
        if isinstance(self.agents, dict):
            return self.agents.get(name)
        # Handle list case
        if name.startswith("agent_"):
            try:
                idx = int(name.split("_")[1])
                return self.agents[idx] if idx < len(self.agents) else None
            except (IndexError, ValueError):
                return None
        return None

    def setup_agent(self) -> None:
        """Setup multi-agent coordinator."""
        if isinstance(self.engine, AugLLMConfig):
            self.engine.temperature = self.temperature

            if not self.engine.system_message and not self.coordinator_prompt:
                self.engine.system_message = self._get_default_coordinator_prompt()
            elif self.coordinator_prompt:
                self.engine.system_message = self.coordinator_prompt

    def _get_default_coordinator_prompt(self) -> str:
        """Get default coordinator prompt."""
        agent_info = "\n".join(
            [
                f"- {name}: {type(agent).__name__}"
                for name, agent in (
                    self.agents.items()
                    if isinstance(self.agents, dict)
                    else enumerate(self.agents)
                )
            ]
        )

        return f"""You are coordinating a multi-agent system.

Agents:
{agent_info}

Execution mode: {self.mode}
State strategy: {self.state_strategy}

Your role:
1. Route tasks to appropriate agents
2. Manage state between agents
3. Handle errors gracefully
4. Synthesize final results

Make decisions based on the current state and task requirements."""

    def build_graph(self) -> BaseGraph:
        """Build multi-agent execution graph."""
        graph = BaseGraph(
            name=f"{self.name}_multi_graph", state_schema=self.state_schema
        )

        # Add coordinator node
        coord_node = EngineNodeConfig(name="coordinator", engine=self.engine)
        graph.add_node("coordinator", coord_node)
        graph.add_edge(START, "coordinatof")

        # Get agents dict
        agents_dict = (
            self.agents
            if isinstance(self.agents, dict)
            else {f"agent_{i}": agent for i, agent in enumerate(self.agents)}
        )

        # Add agent nodes using AgentNodeV3
        for agent_name, agent in agents_dict.items():
            # Use AgentNodeV3 for state projection
            agent_node = AgentNodeV3Config(
                name=agent_name,
                agent=agent,
                # State projection configuration
                input_schema=(
                    agent.input_schema if hasattr(agent, "input_schema") else None
                ),
                output_schema=(
                    agent.output_schema if hasattr(agent, "output_schema") else None
                ),
                state_fields=self.shared_fields,
                private_state_key=f"{agent_name}_state",
            )
            graph.add_node(agent_name, agent_node)

        # Build execution pattern based on mode
        if self.mode == "sequential":
            self._build_sequential_pattern(graph, list(agents_dict.keys()))
        elif self.mode == "parallel":
            self._build_parallel_pattern(graph, list(agents_dict.keys()))
        elif self.mode == "conditional":
            self._build_conditional_pattern(graph, list(agents_dict.keys()))

        return graph

    def _build_sequential_pattern(
        self, graph: BaseGraph, agent_names: list[str]
    ) -> None:
        """Build sequential execution pattern."""
        # Coordinator -> Agent1 -> Agent2 -> ... -> END
        prev_node = "coordinator"

        for agent_name in agent_names:
            graph.add_edge(prev_node, agent_name)
            prev_node = agent_name

        graph.add_edge(prev_node, END)

    def _build_parallel_pattern(self, graph: BaseGraph, agent_names: list[str]) -> None:
        """Build parallel execution pattern."""
        # Coordinator -> All Agents (parallel) -> Aggregator -> END
        for agent_name in agent_names:
            graph.add_edge("coordinator", agent_name)

        # Add aggregator node
        graph.add_node(
            "aggregator", EngineNodeConfig(name="aggregator", engine=self.engine)
        )

        for agent_name in agent_names:
            graph.add_edge(agent_name, "aggregator")

        graph.add_edge("aggregator", END)

    def _build_conditional_pattern(
        self, graph: BaseGraph, agent_names: list[str]
    ) -> None:
        """Build conditional execution pattern."""
        # Coordinator decides which agent(s) to execute

        def route_to_agent(state: dict[str, Any]) -> str:
            """Route based on coordinator decision."""
            # In real implementation, parse coordinator output
            current = state.get("current_agent")
            if current in agent_names:
                return current
            return "end"

        # Add conditional routing
        routes = {name: name for name in agent_names}
        routes["end"] = END

        graph.add_conditional_edges("coordinator", route_to_agent, routes)

        # Agents can return to coordinator or end
        for agent_name in agent_names:
            graph.add_edge(agent_name, "coordinator")

    def __repr__(self) -> str:
        """String representation."""
        engine_type = type(self.engine).__name__ if self.engine else "None"
        agent_count = len(self.agents)
        return (
            f"EnhancedMultiAgent[{engine_type}]("
            f"name='{self.name}', "
            f"agents={agent_count}, "
            f"mode='{self.mode}', "
            f"state='{self.state_strategy}')"
        )


# Example usage
if __name__ == "__main__":
    from haive.agents.react.enhanced_react_agent import ReactAgent
    from haive.agents.simple.enhanced_simple_real import SimpleAgent

    # Create example agents
    planner = ReactAgent(name="planner", temperature=0.3)
    executor = SimpleAgent(name="executor", temperature=0.7)
    reviewer = SimpleAgent(name="reviewer", temperature=0.1)

    # Sequential multi-agent
    sequential = EnhancedMultiAgent(
        name="project_pipeline",
        agents=[planner, executor, reviewer],
        mode="sequential",
        state_transfer_map={
            ("planner", "executof"): {"plan": "task_list"},
            ("executor", "reviewef"): {"result": "execution_output"},
        },
    )

    print(f"Created: {sequential}")
    print(f"Agents: {sequential.get_agent_names()}")

    # Parallel multi-agent
    parallel = EnhancedMultiAgent(
        name="expert_ensemble",
        agents={
            "analyst": SimpleAgent(name="analyst"),
            "researcher": ReactAgent(name="researcher"),
            "strategist": SimpleAgent(name="strategist"),
        },
        mode="parallel",
        state_strategy="container",
    )

    print(f"\nCreated: {parallel}")
    print(f"State strategy: {parallel.state_strategy}")

    # With MetaStateSchema (when imports work)
    # from haive.core.schema.prebuilt.meta_state import MetaStateSchema
    # meta_multi = MetaStateSchema.from_agent(agent=sequential)
    # print(f"\nMeta-capable: {meta_multi}")
