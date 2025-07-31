"""Simple multi-agent using use_prebuilt_base pattern."""

import sys

sys.path.insert(0, "packages/haive-agents/src")
sys.path.insert(0, "packages/haive-core/src")

from typing import Any, Dict, List

# Fix forward reference issues
from haive.agents.base.agent import Agent
from haive.agents.simple.agent import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.node import agent_node_v3
from haive.core.graph.node.agent_node_v3 import AgentNodeV3Config, create_agent_node_v3
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.schema.prebuilt import multi_agent_state
from haive.core.schema.prebuilt.multi_agent_state import MultiAgentState
from langchain_core.messages import HumanMessage
from langgraph.graph import END, START
from pydantic import Field, model_validator

multi_agent_state.Agent = Agent
agent_node_v3.Agent = Agent
MultiAgentState.model_rebuild()
AgentNodeV3Config.model_rebuild()


class SimpleMultiAgent(Agent):
    """Simple multi-agent using use_prebuilt_base pattern."""

    # Agents management
    agents: dict[str, Agent] = Field(default_factory=dict)
    execution_mode: str = Field(default="sequential")

    @model_validator(mode="before")
    @classmethod
    def normalize_agents(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Normalize agents to dict format."""
        if not isinstance(values, dict):
            return values

        # Convert list of agents to dict
        if "agents" in values and isinstance(values["agents"], list):
            agent_dict = {}
            for agent in values["agents"]:
                agent_dict[agent.name] = agent
            values["agents"] = agent_dict

        return values

    def setup_agent(self) -> None:
        """Setup agent using use_prebuilt_base pattern."""
        # Use MultiAgentState directly as prebuilt base
        self.state_schema = MultiAgentState
        self.use_prebuilt_base = True

        # Set initial agents in state schema
        if hasattr(self, "agents") and self.agents:
            # Create a custom state schema with agents pre-populated
            original_init = MultiAgentState.__init__

            def custom_init(state_self, **kwargs):
                # Always include agents if not provided
                if "agents" not in kwargs:
                    kwargs["agents"] = self.agents
                return original_init(state_self, **kwargs)

            # Monkey patch the __init__ method
            MultiAgentState.__init__ = custom_init

    def build_graph(self) -> BaseGraph:
        """Build graph with agent nodes."""
        graph = BaseGraph(name=f"{self.name}_graph")

        # Add agent nodes
        for agent_name, agent in self.agents.items():
            node = create_agent_node_v3(
                agent_name=agent_name, agent=agent, name=f"agent_{agent_name}"
            )
            graph.add_node(f"agent_{agent_name}", node)

        # Build sequential edges
        if self.execution_mode == "sequential":
            agent_names = list(self.agents.keys())
            graph.add_edge(START, f"agent_{agent_names[0]}")

            for i in range(len(agent_names) - 1):
                graph.add_edge(f"agent_{agent_names[i]}", f"agent_{agent_names[i+1]}")

            graph.add_edge(f"agent_{agent_names[-1]}", END)

        return graph


def test_simple_multi_agent():
    """Test the simple multi-agent implementation."""
    print("=== SIMPLE MULTI-AGENT TEST ===")

    # Create agents
    agent1 = SimpleAgent(
        name="agent1", engine=AugLLMConfig(system_message="You are agent 1")
    )
    agent2 = SimpleAgent(
        name="agent2", engine=AugLLMConfig(system_message="You are agent 2")
    )

    # Create multi-agent
    multi = SimpleMultiAgent(
        name="test_multi", agents=[agent1, agent2], execution_mode="sequential"
    )

    print(f"✅ Created multi-agent with: {list(multi.agents.keys())}")
    print(f"   State schema: {multi.state_schema.__name__}")
    print(f"   Use prebuilt base: {multi.use_prebuilt_base}")

    # Test state creation
    print("\\n📋 Testing state creation..."..")
    try:
        state = multi.state_schema(messages=[HumanMessage(content="Hello multi-agent")])
        print("   ✅ State created successfully"y")
        print(f"   State.agents: {list(state.agents.keys())}")
        print(f"   State.messages: {len(state.messages)}")

        # Test set_active_agent
        if state.agents:
            state.set_active_agent("agent1")
            print(f"   ✅ set_active_agent works: {state.active_agent}")

    except Exception as e:
        print(f"   ❌ State creation failed: {e}")
        import traceback

        traceback.print_exc()

    # Test execution
    print("\\n🚀 Testing execution..."..")
    try:
        result = multi.invoke({"messages": [HumanMessage(content="Hello")]})
        print("   ✅ Execution completed"d")
        print(f"   Result type: {type(result)}")
        if hasattr(result, "messages"):
            print(f"   Messages: {len(result.messages)}")

    except Exception as e:
        print(f"   ❌ Execution failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    test_simple_multi_agent()
