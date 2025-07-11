"""Minimal test for MultiAgentBase with proper state schema."""

import asyncio
from typing import Literal

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.models.llm.base import AzureLLMConfig
from haive.core.schema.agent_schema_composer import BuildMode
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import END

# Import our working components
from haive.agents.experiments.supervisor.component_2_tools import (
    SupervisorStateWithTools,
)
from haive.agents.experiments.supervisor.component_3_agent_execution import (
    create_agent_execution_node,
)
from haive.agents.experiments.supervisor.test_utils import create_test_agents
from haive.agents.multi.enhanced_base import MultiAgentBase
from haive.agents.simple.agent import SimpleAgent


async def test_minimal_multiagent():
    """Test minimal MultiAgentBase setup."""
    # Create test agents
    agents_dict = await create_test_agents()

    # Create initial state
    initial_state = SupervisorStateWithTools(
        messages=[HumanMessage(content="Calculate 10 + 5")],
        agents=agents_dict,
        active_agents={"search_agent", "math_agent"},
    )

    for _name, _info in initial_state.agents.items():
        pass

    # Create agent execution node
    agent_execution_node = create_agent_execution_node()

    # Simple routing function
    def route_based_on_state(state) -> Literal["execute", "END"]:
        """Route based on state.next_agent."""
        if state.next_agent and state.agent_task:
            return "execute"
        return "END"

    # Create a simple workflow function that sets routing
    def supervisor_workflow(state):
        """Simple supervisor that routes to math agent."""
        # For testing, just route to math agent
        return {
            "next_agent": "math_agent",
            "agent_task": "Calculate 10 + 5",
            "messages": [*state.messages, AIMessage(content="Routing to math agent")],
        }

    # Test 1: Build graph manually first
    try:
        graph = BaseGraph(
            name="supervisor_graph", state_schema=SupervisorStateWithTools
        )
        graph.add_node("supervisor", supervisor_workflow)
        graph.add_node("execute", agent_execution_node)
        graph.add_conditional_edges(
            "supervisor", route_based_on_state, {"execute": "execute", "END": END}
        )
        graph.set_entry_point("supervisor")
        graph.add_edge("execute", END)

        graph.compile()

    except Exception:
        import traceback

        traceback.print_exc()
        return

    # Test 2: Now try with MultiAgentBase
    try:
        # Create a dummy agent to satisfy MultiAgentBase validation
        dummy_agent = SimpleAgent(
            name="coordinator",
            engine=AugLLMConfig(name="coordinator_engine"),
            system_prompt="You are a coordinator agent.",
        )

        system = MultiAgentBase(
            agents=[dummy_agent],  # Include dummy agent to satisfy validation
            workflow_nodes={
                "supervisor": supervisor_workflow,
                "execute": agent_execution_node,
            },
            branches=[
                ("supervisor", route_based_on_state, {"execute": "execute", "END": END})
            ],
            entry_points=[
                "supervisor"
            ],  # Start with supervisor workflow node, not coordinator agent!
            state_schema_override=SupervisorStateWithTools,
            schema_build_mode=BuildMode.SEQUENCE,
            name="Test Supervisor System",
        )

        # Ensure state schema is set

        # Don't compile the graph directly - let the agent handle it
        system.compile()

        # Test execution

        # Debug: Check what gets serialized
        serialized = initial_state.model_dump()
        if "agents" in serialized:
            for _agent_name, agent_data in serialized["agents"].items():
                if isinstance(agent_data, dict) and "agent" in agent_data:
                    agent_obj = agent_data["agent"]
                    if isinstance(agent_obj, dict) and "engine" in agent_obj:
                        engine_data = agent_obj["engine"]
                        if isinstance(engine_data, dict):
                            pass

        result = await system.arun("Calculate 10 + 5")

        if result.get("agent_response"):
            pass

    except Exception:
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_minimal_multiagent())
