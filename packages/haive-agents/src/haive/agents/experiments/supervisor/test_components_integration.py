"""Test integration of Components 2 and 3."""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from component_2_tools import SupervisorStateWithTools
from component_3_agent_execution import create_agent_execution_node
from langchain_core.messages import HumanMessage
from test_utils import create_test_agents


async def test_components_integration():
    """Test Component 2 (tools) with Component 3 (execution)."""
    print("\n=== Testing Components 2 & 3 Integration ===\n")

    # Create test agents
    agents_dict = await create_test_agents()

    # Create state with agents (AgentInfo objects)
    state = SupervisorStateWithTools(
        messages=[HumanMessage(content="Calculate 25 + 15")],
        agents=agents_dict,  # Pass AgentInfo objects directly
        active_agents={"search_agent", "math_agent"},
    )

    print("Initial state created:")
    print(f"  Agents: {list(state.agents.keys())}")
    print(f"  Active agents: {state.active_agents}")
    print(f"  Generated tool names: {state.generated_tools}")

    # Get actual tool objects
    tools = state.get_all_tools()
    tool_names = [tool.name for tool in tools]
    print(f"  Actual tools: {tool_names}")

    # Test tool generation
    print("\n1. Testing tool generation from state...")
    assert "handoff_to_search_agent" in tool_names
    assert "handoff_to_math_agent" in tool_names
    assert "choose_agent" in tool_names
    print("✅ Tools generated correctly")

    # Test agent selection
    print("\n2. Testing agent selection...")
    # Find the choose_agent tool
    choose_tool = next(tool for tool in tools if tool.name == "choose_agent")
    result = choose_tool.invoke({"task_description": "I need to calculate 25 plus 15"})
    print(f"   Choose agent result: {result}")

    # Set routing based on choice
    state.next_agent = "math_agent"
    state.agent_task = "Calculate 25 + 15"

    # Test agent execution node
    print("\n3. Testing agent execution node...")
    execution_node = create_agent_execution_node()

    try:
        result = await execution_node(state)
        print(f"   Execution result: {result}")

        if "agent_response" in result:
            print(f"   Agent response: {result['agent_response']}")

        # Verify state was updated
        assert result.get("next_agent") is None  # Should be cleared
        assert result.get("agent_task") == ""  # Should be cleared

        print("✅ Agent execution successful")

    except Exception as e:
        print(f"❌ Agent execution failed: {e}")
        raise

    # Test with inactive agent
    print("\n4. Testing with inactive agent...")
    state.next_agent = "planning_agent"  # This is inactive
    state.agent_task = "Create a plan"

    result = await execution_node(state)
    print(f"   Result: {result}")
    assert "inactive" in result.get("agent_response", "").lower()
    print("✅ Inactive agent handled correctly")

    print("\n✅ All component integration tests passed!")


if __name__ == "__main__":
    asyncio.run(test_components_integration())
