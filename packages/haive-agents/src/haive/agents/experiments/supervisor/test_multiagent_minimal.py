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
    print("\n=== Testing Minimal MultiAgentBase ===\n")

    # Create test agents
    agents_dict = await create_test_agents()

    # Create initial state
    initial_state = SupervisorStateWithTools(
        messages=[HumanMessage(content="Calculate 10 + 5")],
        agents=agents_dict,
        active_agents={"search_agent", "math_agent"},
    )

    print("State created with agents:")
    for name, info in initial_state.agents.items():
        print(f"  - {name}: {info.description} (active: {info.active})")

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
            "messages": state.messages + [AIMessage(content="Routing to math agent")],
        }

    # Test 1: Build graph manually first
    print("\n1. Testing manual graph build...")
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

        compiled = graph.compile()
        print("✅ Manual graph compiled successfully!")

    except Exception as e:
        print(f"❌ Manual graph failed: {e}")
        import traceback

        traceback.print_exc()
        return

    # Test 2: Now try with MultiAgentBase
    print("\n2. Testing MultiAgentBase...")
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
        print(f"System state_schema: {system.state_schema}")
        print(f"System has setup_complete: {system._setup_complete}")

        # Don't compile the graph directly - let the agent handle it
        compiled2 = system.compile()
        print("✅ MultiAgentBase compiled successfully!")

        # Test execution
        print("\n3. Testing execution...")

        # Debug: Check what gets serialized
        print("DEBUG: Checking state serialization...")
        serialized = initial_state.model_dump()
        print(f"Serialized state keys: {list(serialized.keys())}")
        if "agents" in serialized:
            print(f"Agents in serialized state: {list(serialized['agents'].keys())}")
            for agent_name, agent_data in serialized["agents"].items():
                print(
                    f"  {agent_name}: {type(agent_data)} - keys: {list(agent_data.keys()) if isinstance(agent_data, dict) else 'not dict'}"
                )
                if isinstance(agent_data, dict) and "agent" in agent_data:
                    agent_obj = agent_data["agent"]
                    print(f"    Agent object type: {type(agent_obj)}")
                    if isinstance(agent_obj, dict):
                        print(f"    Agent object keys: {list(agent_obj.keys())}")
                        if "engine" in agent_obj:
                            engine_data = agent_obj["engine"]
                            print(f"    Engine type: {type(engine_data)}")
                            if isinstance(engine_data, dict):
                                print(f"    Engine keys: {list(engine_data.keys())}")

        result = await system.arun("Calculate 10 + 5")

        print(f"\nExecution result:")
        print(f"  Messages: {len(result.get('messages', []))}")
        if result.get("agent_response"):
            print(f"  Agent response: {result['agent_response']}")

    except Exception as e:
        print(f"❌ MultiAgentBase failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_minimal_multiagent())
