"""Quick test of component fixes."""

from haive.agents.experiments.supervisor.component_2_tools import (
    SupervisorStateWithTools,
)
from haive.agents.experiments.supervisor.test_component_1_state import (
    create_real_agents,
)


def test_validation_fix():
    """Test that field validation now works."""
    print("🧪 Testing field validation fix...")

    state = SupervisorStateWithTools()
    agents = create_real_agents()
    state.add_agent("search_agent", agents["search_agent"], "Test", True)

    # Test valid assignment
    try:
        state.next_agent = "search_agent"
        print("✅ Valid assignment works")
    except Exception as e:
        print(f"❌ Valid assignment failed: {e}")

    # Test invalid assignment
    try:
        state.next_agent = "nonexistent_agent"
        print("❌ Invalid assignment should have failed")
    except ValueError as e:
        print(f"✅ Invalid assignment correctly rejected: {e}")


def test_tool_names():
    """Test that tool names are now correct."""
    print("\n🧪 Testing tool name fix...")

    state = SupervisorStateWithTools()
    agents = create_real_agents()
    state.add_agent("search_agent", agents["search_agent"], "Test", True)

    tools = state.get_all_tools()
    print(f"Generated {len(tools)} tools:")

    found_handoff = False
    for tool in tools:
        print(f"  - {tool.name}: {type(tool).__name__}")
        if tool.name == "handoff_to_search_agent":
            found_handoff = True

    if found_handoff:
        print("✅ Handoff tool has correct name")
    else:
        print("❌ Handoff tool name not found")


if __name__ == "__main__":
    print("🚀 Quick Component Fixes Test")
    print("=" * 40)

    try:
        test_validation_fix()
        test_tool_names()
        print("\n🎉 Component fixes work!")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback

        traceback.print_exc()
