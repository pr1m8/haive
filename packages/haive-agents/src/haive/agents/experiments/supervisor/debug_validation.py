"""Debug the exact validation error."""

from typing import Dict

from agent_info import AgentInfo

# First, let's recreate the exact scenario
from haive.core.schema.prebuilt.messages_state import MessagesState
from pydantic import BaseModel, Field


def test_step_by_step():
    """Debug step by step."""
    print("\n=== Step by Step Debug ===\n")

    # Step 1: Check if MessagesState has special config
    print("1. Checking MessagesState config:")
    print(
        f"   MessagesState model_config: {getattr(MessagesState, 'model_config', 'Not set')}"
    )
    print(
        f"   MessagesState __config__: {getattr(MessagesState, '__config__', 'Not set')}"
    )

    # Step 2: Create minimal state that extends MessagesState
    class MinimalState(MessagesState):
        test_field: str = "test"

    try:
        s = MinimalState()
        print("\n2. ✅ Can create MinimalState")
        print(f"   Has messages: {hasattr(s, 'messages')}")
    except Exception as e:
        print(f"\n2. ❌ MinimalState failed: {e}")

    # Step 3: Add Dict field
    class StateWithDict(MessagesState):
        agents: Dict[str, dict] = Field(default_factory=dict)

    try:
        s2 = StateWithDict(agents={"test": {"name": "test"}})
        print("\n3. ✅ Can create StateWithDict")
        print(f"   agents type: {type(s2.agents)}")
    except Exception as e:
        print(f"\n3. ❌ StateWithDict failed: {e}")

    # Step 4: Use AgentInfo type
    class StateWithAgentInfo(MessagesState):
        agents: Dict[str, AgentInfo] = Field(default_factory=dict)

    # Create a dummy agent
    class DummyAgent:
        def __init__(self):
            self.name = "dummy"

    agent = DummyAgent()
    info = AgentInfo(agent=agent, name="test", description="Test")

    print(f"\n4. Testing AgentInfo:")
    print(f"   AgentInfo instance type: {type(info)}")
    print(f"   AgentInfo.__class__.__name__: {info.__class__.__name__}")
    print(f"   Is instance of AgentInfo: {isinstance(info, AgentInfo)}")

    try:
        # Try with dict first
        s3 = StateWithAgentInfo(
            agents={"test": {"agent": agent, "name": "test", "description": "Test"}}
        )
        print("\n   ✅ StateWithAgentInfo works with dict")
    except Exception as e:
        print(f"\n   ❌ StateWithAgentInfo with dict failed: {e}")

    try:
        # Try with AgentInfo instance
        s4 = StateWithAgentInfo(agents={"test": info})
        print("\n   ✅ StateWithAgentInfo works with AgentInfo instance")
    except Exception as e:
        print(f"\n   ❌ StateWithAgentInfo with instance failed: {e}")

        # Get more details about the error
        if hasattr(e, "errors"):
            for err in e.errors():
                print(f"\n   Error details:")
                print(f"     loc: {err.get('loc')}")
                print(f"     msg: {err.get('msg')}")
                print(f"     type: {err.get('type')}")
                print(f"     input: {err.get('input')}")

    # Step 5: Check if model_config helps
    print("\n5. Testing with model_config:")

    class StateWithConfig(MessagesState):
        agents: Dict[str, AgentInfo] = Field(default_factory=dict)
        model_config = {"arbitrary_types_allowed": True}

    try:
        s5 = StateWithConfig(agents={"test": info})
        print("   ✅ StateWithConfig works!")
    except Exception as e:
        print(f"   ❌ StateWithConfig failed: {e}")


if __name__ == "__main__":
    test_step_by_step()
