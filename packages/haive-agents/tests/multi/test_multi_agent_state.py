"""Test MultiAgentState with before_validator for agent hierarchy."""

from typing import Any, Dict, List, Optional, Set, Union

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.schema.prebuilt.tool_state import ToolState
from pydantic import Field, field_validator, model_validator

from haive.agents.base import Agent
from haive.agents.simple.agent import SimpleAgent


class MultiAgentState(ToolState):
    """Multi-agent state that contains agents without flattening schemas."""

    # Agents can be passed as list or dict
    agents: list[Agent] | dict[str, Agent] = Field(
        default_factory=dict, description="Agent instances contained in this state"
    )

    # Hierarchical state management
    agent_states: dict[str, dict[str, Any]] = Field(
        default_factory=dict, description="Isolated state for each agent"
    )

    # Execution tracking
    active_agent: str | None = Field(default=None)
    agent_outputs: dict[str, Any] = Field(default_factory=dict)

    # Recompilation tracking
    agents_needing_recompile: set[str] = Field(default_factory=set)
    recompile_count: int = Field(default=0)

    @field_validator("agents", mode="before")
    @classmethod
    def convert_agents_to_dict(cls, v):
        """Convert list of agents to dict keyed by name."""
        if isinstance(v, list):
            # Convert list to dict using agent names
            return {agent.name: agent for agent in v}
        return v

    @model_validator(mode="after")
    def setup_agent_states(self) -> "MultiAgentState":
        """Initialize agent states from contained agents."""
        if isinstance(self.agents, dict):
            for agent_name, agent in self.agents.items():
                if agent_name not in self.agent_states:
                    # Initialize empty state for each agent
                    self.agent_states[agent_name] = {}

                # Sync engines from agents to parent state
                if hasattr(agent, "engines"):
                    for engine_name, engine in agent.engines.items():
                        # Namespace the engine to avoid conflicts
                        namespaced_engine = f"{agent_name}.{engine_name}"
                        self.engines[namespaced_engine] = engine

        return self

    def get_agent_state(self, agent_name: str) -> dict[str, Any]:
        """Get isolated state for a specific agent."""
        return self.agent_states.get(agent_name, {})

    def update_agent_state(self, agent_name: str, updates: dict[str, Any]):
        """Update isolated state for a specific agent."""
        if agent_name not in self.agent_states:
            self.agent_states[agent_name] = {}
        self.agent_states[agent_name].update(updates)

    def mark_for_recompile(self, agent_name: str):
        """Mark an agent as needing recompilation."""
        self.agents_needing_recompile.add(agent_name)


def test_multi_agent_state():
    """Test MultiAgentState with list and dict inputs."""
    # Create some agents
    planner = SimpleAgent(name="planner", engine=AugLLMConfig())
    executor = SimpleAgent(name="executor", engine=AugLLMConfig())

    # Test 1: Create with list of agents
    MultiAgentState(agents=[planner, executor])

    # Test 2: Create with dict of agents
    state2 = MultiAgentState(agents={"plan": planner, "exec": executor})

    # Test 3: Update agent state
    state2.update_agent_state("plan", {"current_plan": "Step 1"})

    # Test 4: Recompilation tracking
    state2.mark_for_recompile("plan")

    return state2


if __name__ == "__main__":
    state = test_multi_agent_state()
