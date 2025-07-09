"""Test direct dict approach to understand the issue."""

from typing import Any, Dict

from pydantic import BaseModel, Field


# Test with a simple base model first
class SimpleState(BaseModel):
    agents: Dict[str, Any] = Field(default_factory=dict)
    model_config = {"arbitrary_types_allowed": True}


class TestAgent:
    def __init__(self, name):
        self.name = name


def test_simple():
    """Test with simple models."""
    print("\n=== Testing Simple Models ===\n")

    # Create test agent
    agent = TestAgent("test")
    print(f"Created agent: {agent.name}")

    # Test 1: Direct dict with Any
    try:
        state = SimpleState(agents={"test": agent})
        print("✅ Simple model with Any works")
        print(f"   Agent type: {type(state.agents['test'])}")
    except Exception as e:
        print(f"❌ Simple model failed: {e}")

    # Test 2: Let's try with AgentInfo type annotation
    from agent_info import AgentInfo

    class TypedState(BaseModel):
        agents: Dict[str, AgentInfo] = Field(default_factory=dict)
        model_config = {"arbitrary_types_allowed": True}

    try:
        # Create AgentInfo
        info = AgentInfo(agent=agent, name="test", description="Test agent")
        state2 = TypedState(agents={"test": info})
        print("\n✅ Typed model with AgentInfo works")
        print(f"   AgentInfo type: {type(state2.agents['test'])}")
    except Exception as e:
        print(f"\n❌ Typed model failed: {e}")

    # Test 3: With inheritance
    from haive.core.schema.prebuilt.messages_state import MessagesState

    class InheritedState(MessagesState):
        agents: Dict[str, Any] = Field(default_factory=dict)
        model_config = {"arbitrary_types_allowed": True}

    try:
        state3 = InheritedState(agents={"test": agent})
        print("\n✅ Inherited model works")
        print(f"   Has messages attr: {hasattr(state3, 'messages')}")
    except Exception as e:
        print(f"\n❌ Inherited model failed: {e}")


if __name__ == "__main__":
    test_simple()
