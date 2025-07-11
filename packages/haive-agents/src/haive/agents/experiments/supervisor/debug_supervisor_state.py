"""Debug our actual SupervisorState."""

from agent_info import AgentInfo
from supervisor_state import SupervisorState


def test_supervisor_state():
    """Test the actual SupervisorState."""

    # Create dummy agent
    class DummyAgent:
        def __init__(self):
            self.name = "dummy"

    agent = DummyAgent()
    info = AgentInfo(agent=agent, name="test", description="Test")


    # Test 1: Empty state
    try:
        SupervisorState()
    except Exception as e:
        pass")

    # Test 2: With dict
    try:
        state2 = SupervisorState(
            agents={"test": {"agent": agent, "name": "test", "description": "Test"}}
        )
    except Exception as e:
        pass")

    # Test 3: With AgentInfo
    try:
        state3 = SupervisorState(agents={"test": info})
    except Exception as e:
        import traceback

        traceback.print_exc()

        # Let's inspect the class more


if __name__ == "__main__":
    test_supervisor_state()
