"""Debug our actual SupervisorState."""

from agent_info import AgentInfo
from supervisor_state import SupervisorState


def test_supervisor_state():
    """Test the actual SupervisorState."""
    print("\n=== Testing SupervisorState ===\n")

    # Create dummy agent
    class DummyAgent:
        def __init__(self):
            self.name = "dummy"

    agent = DummyAgent()
    info = AgentInfo(agent=agent, name="test", description="Test")

    print(f"1. AgentInfo created: {info}")
    print(f"   Type: {type(info)}")
    print(f"   model_config in SupervisorState: {SupervisorState.model_config}")

    # Test 1: Empty state
    try:
        state = SupervisorState()
        print("\n2. ✅ Empty SupervisorState works")
    except Exception as e:
        print(f"\n2. ❌ Empty SupervisorState failed: {e}")

    # Test 2: With dict
    try:
        state2 = SupervisorState(
            agents={"test": {"agent": agent, "name": "test", "description": "Test"}}
        )
        print("\n3. ✅ SupervisorState with dict works")
        print(f"   Agent type in state: {type(state2.agents.get('test'))}")
    except Exception as e:
        print(f"\n3. ❌ SupervisorState with dict failed: {e}")

    # Test 3: With AgentInfo
    try:
        state3 = SupervisorState(agents={"test": info})
        print("\n4. ✅ SupervisorState with AgentInfo works!")
        print(f"   Agent type in state: {type(state3.agents.get('test'))}")
    except Exception as e:
        print(f"\n4. ❌ SupervisorState with AgentInfo failed: {e}")
        import traceback

        traceback.print_exc()

        # Let's inspect the class more
        print("\n   Debugging SupervisorState class:")
        print(f"   MRO: {[c.__name__ for c in SupervisorState.__mro__]}")
        print(f"   Fields: {list(SupervisorState.model_fields.keys())}")
        print(f"   agents field info: {SupervisorState.model_fields.get('agents')}")


if __name__ == "__main__":
    test_supervisor_state()
