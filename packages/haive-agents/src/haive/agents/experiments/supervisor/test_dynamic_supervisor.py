"""Test the DynamicSupervisorAgent implementation."""

import asyncio

from langchain_core.messages import HumanMessage

from haive.agents.experiments.supervisor.component_2_tools import (
    SupervisorStateWithTools,
)
from haive.agents.experiments.supervisor.dynamic_supervisor_agent import (
    create_supervisor_agent,
)
from haive.agents.experiments.supervisor.test_utils import create_test_agents


async def test_supervisor_agent():
    """Test the DynamicSupervisorAgent with our working components."""
    print("\n=== Testing DynamicSupervisorAgent ===\n")

    # Create test agents using our working utility
    agents_dict = await create_test_agents()
    print(f"Created {len(agents_dict)} test agents")

    # Create supervisor agent (no engine needed for this test)
    supervisor = create_supervisor_agent("dynamic_supervisor")

    print(f"Supervisor agent created: {supervisor.name}")
    print(f"Supervisor state schema: {supervisor.state_schema}")
    print(f"Supervisor graph built: {supervisor._graph_built}")

    # Test with a math task
    print("\n1. Testing math task routing...")

    initial_state = SupervisorStateWithTools(
        messages=[HumanMessage(content="Calculate 25 + 15 for me")],
        agents=agents_dict,
        active_agents={"search_agent", "math_agent"},
    )

    try:
        result = await supervisor.arun(initial_state.model_dump())

        print("✅ Supervisor execution successful!")
        print(f"Final messages: {len(result.get('messages', []))}")
        if result.get("agent_response"):
            print(f"Agent response: {result['agent_response']}")
        if result.get("next_agent"):
            print(f"Routed to: {result['next_agent']}")

    except Exception as e:
        print(f"❌ Supervisor execution failed: {e}")
        import traceback

        traceback.print_exc()

    # Test with search task
    print("\n2. Testing search task routing...")

    search_state = SupervisorStateWithTools(
        messages=[HumanMessage(content="Search for information about Python")],
        agents=agents_dict,
        active_agents={"search_agent", "math_agent"},
    )

    try:
        result = await supervisor.arun(search_state.model_dump())

        print("✅ Search routing successful!")
        if result.get("next_agent"):
            print(f"Routed to: {result['next_agent']}")

    except Exception as e:
        print(f"❌ Search routing failed: {e}")


if __name__ == "__main__":
    asyncio.run(test_supervisor_agent())
