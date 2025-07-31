"""Enhanced MultiAgent with proper generics for contained agents.

MultiAgent[AgentsT] where AgentsT represents the agents it contains.
"""

import logging
from typing import Any, Generic, Literal, TypeVar

from haive.core.graph.node.agent_node_v3 import AgentNodeV3Config
from haive.core.graph.node.engine_node import EngineNodeConfig
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from langgraph.graph import END, START
from pydantic import Field, field_validator

# Import base enhanced agent when available
# from haive.agents.base.enhanced_agent import Agent
# For now, use our working base class
from haive.agents.simple.enhanced_simple_real import EnhancedAgentBase

# Define Agent as alias to avoid import issues
Agent = EnhancedAgentBase

logger = logging.getLogger(__name__)

# Generic type for agents contained in MultiAgent
AgentsT = TypeVar("AgentsT", bound=dict[str, Agent] | list[Agent])


class MultiAgent(Agent, Generic[AgentsT]):
    """Enhanced MultiAgent generic on the agents it contains.

    MultiAgent[AgentsT] = Agent[AugLLMConfig] + agents: AgentsT

    This properly represents that MultiAgent is:
    1. An agent itself (uses AugLLMConfig for coordination)
    2. Generic on the agents it contains

    Examples:
        With typed dict of agents::

            agents: Dict[str, Agent] = {
                "planner": PlannerAgent(...),
                "executor": ExecutorAgent(...)
            }
            multi: MultiAgent[Dict[str, Agent]] = MultiAgent(
                name="coordinator",
                agents=agents
            )

        With list of agents::

            agent_list: List[ReactAgent] = [agent1, agent2, agent3]
            multi: MultiAgent[List[ReactAgent]] = MultiAgent(
                name="ensemble",
                agents=agent_list
            )

        With specific agent types::

            from typing import TypedDict

            class MyAgents(TypedDict):
                researcher: RAGAgent
                analyzer: ReactAgent
                writer: SimpleAgent

            agents = MyAgents(
                researcher=rag_agent,
                analyzer=react_agent,
                writer=simple_agent
            )

            multi: MultiAgent[MyAgents] = MultiAgent(
                name="report_team",
                agents=agents
            )
    """

    # The agents this MultiAgent coordinates (generic)
    agents: AgentsT = Field(..., description="Agents to coordinate - generic type")

    # Execution mode
    mode: Literal["sequential", "parallel", "conditional", "branch"] = Field(
        default="sequential", description="Execution mode for agents"
    )

    # Branching configuration
    branch_condition: Any | None = Field(
        default=None, description="Condition function for branching"
    )

    branch_map: dict[str, str] | None = Field(
        default=None, description="Mapping of condition outputs to agent names"
    )

    # Other MultiAgent specific fields
    max_iterations: int = Field(
        default=10, description="Maximum iterations for conditional/branch modes"
    )

    @field_validator("agents")
    @classmethod
    def validate_agents(cls, v: AgentsT) -> AgentsT:
        """Validate agents based on type."""
        if isinstance(v, dict):
            if not v:
                raise ValueError("Agent dict cannot be empty")
            # Validate all values are agents
            for name, agent in v.items():
                if not hasattr(agent, "run") and not hasattr(agent, "arun"):
                    raise ValueError(f"Agent '{name}' must have run/arun method")
        elif isinstance(v, list):
            if not v:
                raise ValueError("Agent list cannot be empty")
            # Validate all items are agents
            for i, agent in enumerate(v):
                if not hasattr(agent, "run") and not hasattr(agent, "arun"):
                    raise ValueError(f"Agent at index {i} must have run/arun method")
        else:
            raise ValueError("Agents must be dict or list")

        return v

    def get_agent_names(self) -> list[str]:
        """Get list of agent names."""
        if isinstance(self.agents, dict):
            return list(self.agents.keys())
        # For list, generate names
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

    def __repr__(self) -> str:
        """String representation."""
        engine_type = type(self.engine).__name__ if self.engine else "None"
        agent_count = len(self.agents)
        agents_type = type(self.agents).__name__

        return (
            f"MultiAgent[{agents_type}]("
            f"name='{self.name}', "
            f"engine={engine_type}, "
            f"agents={agent_count}, "
            f"mode='{self.mode}')"
        )


# Specialized MultiAgent variants


class BranchingMultiAgent(MultiAgent[dict[str, Agent]]):
    """MultiAgent specialized for branching execution.

    Routes to different agents based on conditions.
    """

    mode: Literal["branch"] = Field(default="branch", description="Always branch mode")

    def build_graph(self) -> BaseGraph:
        """Build branching execution graph."""
        graph = BaseGraph(name=f"{self.name}_branching_graph")

        # Add router node (uses the MultiAgent's engine)
        router_node = EngineNodeConfig(name="router", engine=self.engine)
        graph.add_node("router", router_node)
        graph.add_edge(START, "router")

        # Add agent nodes
        for agent_name, agent in self.agents.items():
            agent_node = AgentNodeV3Config(name=agent_name, agent=agent)
            graph.add_node(agent_name, agent_node)
            graph.add_edge(agent_name, END)

        # Branching logic
        def route_condition(state: dict[str, Any]) -> str:
            """Route based on state or condition."""
            if self.branch_condition:
                result = self.branch_condition(state)
                if result in self.branch_map:
                    return self.branch_map[result]

            # Default routing based on content
            messages = state.get("messages", [])
            if messages:
                last_content = str(messages[-1].content).lower()

                # Simple key routing
                for agent_name in self.agents:
                    if agent_name.lower() in last_content:
                        return agent_name

            # Default to first agent
            return next(iter(self.agents.keys()))

        # Add conditional edges from router
        graph.add_conditional_edges(
            "routef", route_condition, {name: name for name in self.agents}
        )

        return graph


class ConditionalMultiAgent(MultiAgent[dict[str, Agent]]):
    """MultiAgent with conditional execution based on previous results.

    Executes agents conditionally based on outputs.
    """

    mode: Literal["conditional"] = Field(
        default="conditional", description="Always conditional mode"
    )

    # Condition rules
    condition_rules: dict[str, dict[str, Any]] = Field(
        default_factory=dict, description="Rules for conditional execution"
    )

    def should_continue(self, state: dict[str, Any], current_agent: str) -> str | None:
        """Determine next agent based on conditions."""
        # Check rules for current agent
        if current_agent in self.condition_rules:
            rules = self.condition_rules[current_agent]

            # Evaluate conditions
            for condition, next_agent in rules.items():
                if self._evaluate_condition(condition, state):
                    return next_agent

        return None

    def _evaluate_condition(self, condition: str, state: dict[str, Any]) -> bool:
        """Evaluate a condition against state."""
        # Simple implementation - can be enhanced
        if condition == "success":
            return not state.get("error")
        if condition == "error":
            return bool(state.get("error"))
        if condition.startswith("contains:"):
            key = condition.split(":", 1)[1]
            messages = state.get("messages", [])
            if messages:
                return key in str(messages[-1].content).lower()

        return False


class AdaptiveBranchingMultiAgent(BranchingMultiAgent):
    """Branching MultiAgent that adapts routing based on performance.

    Tracks agent performance and adjusts routing probabilities.
    """

    # Performance tracking
    agent_performance: dict[str, dict[str, float]] = Field(
        default_factory=dict, description="Performance metrics per agent"
    )

    adaptation_rate: float = Field(
        default=0.1, ge=0.0, le=1.0, description="How quickly to adapt routing"
    )

    def update_performance(
        self, agent_name: str, success: bool, duration: float
    ) -> None:
        """Update agent performance metrics."""
        if agent_name not in self.agent_performance:
            self.agent_performance[agent_name] = {
                "success_rate": 0.5,
                "avg_duration": duration,
                "task_count": 0,
            }

        metrics = self.agent_performance[agent_name]
        metrics["task_count"] += 1

        # Update success rate with exponential moving average
        current_rate = metrics["success_rate"]
        new_rate = (
            current_rate * (1 - self.adaptation_rate)
            + (1.0 if success else 0.0) * self.adaptation_rate
        )
        metrics["success_rate"] = new_rate

        # Update average duration
        metrics["avg_duration"] = (
            metrics["avg_duration"] * (metrics["task_count"] - 1) + duration
        ) / metrics["task_count"]

    def get_best_agent_for_task(self, task_type: str) -> str:
        """Get best performing agent for task type."""
        best_agent = None
        best_score = 0.0

        for agent_name, metrics in self.agent_performance.items():
            # Simple scoring: success_rate / avg_duration
            score = metrics["success_rate"] / max(metrics["avg_duration"], 0.1)
            if score > best_score:
                best_score = score
                best_agent = agent_name

        return best_agent or next(iter(self.agents.keys()))


# Example usage
if __name__ == "__main__":
    # Example of properly typed MultiAgent
    from typing import TypedDict

    class ReportTeamAgents(TypedDict):
        """Typed dict for report team agents."""

        researcher: Agent
        analyst: Agent
        writer: Agent

    # Create typed agents dict
    agents = ReportTeamAgents(
        researcher=Agent(name="researcher"),
        analyst=Agent(name="analyst"),
        writer=Agent(name="writer"),
    )

    # Create MultiAgent with proper typing
    report_team: MultiAgent[ReportTeamAgents] = MultiAgent(
        name="report_team", agents=agents, mode="sequential"
    )

    # Branching example
    branch_team = BranchingMultiAgent(
        name="branch_routef",
        agents={
            "technical": Agent(name="tech_expert"),
            "business": Agent(name="biz_expert"),
            "general": Agent(name="generalist"),
        },
        branch_map={
            "technical": "technical",
            "business": "business",
            "other": "general",
        },
    )

    # Adaptive branching
    adaptive = AdaptiveBranchingMultiAgent(
        name="adaptive_router",
        agents={
            "fast": Agent(name="fast_agent"),
            "accurate": Agent(name="accurate_agent"),
            "creative": Agent(name="creative_agent"),
        },
        adaptation_rate=0.2,
    )

    # The key insight: MultiAgent is generic on its agents!
    # MultiAgent[Dict[str, Agent]] for flexibility
    # MultiAgent[SpecificAgentsType] for type safety
