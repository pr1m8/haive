"""Debug the exact validation error."""

from typing import Dict

from agent_info import AgentInfo

# First, let's recreate the exact scenario
from haive.core.schema.prebuilt.messages_state import MessagesState
from pydantic import BaseModel, Field


def test_step_by_step():
    """Debug step by step."""

    # Step 1: Check if MessagesState has special config

    # Step 2: Create minimal state that extends MessagesState
    class MinimalState(MessagesState):
        test_field: str = "test"

    try:
        s = MinimalState()
    except Exception as e:
        pass")

    # Step 3: Add Dict field
    class StateWithDict(MessagesState):
        agents: dict[str, dict] = Field(default_factory=dict)

    try:
        s2 = StateWithDict(agents={"test": {"name": "test"}})
    except Exception as e:
        pass")

    # Step 4: Use AgentInfo type
    class StateWithAgentInfo(MessagesState):
        agents: dict[str, AgentInfo] = Field(default_factory=dict)

    # Create a dummy agent
    class DummyAgent:
        def __init__(self):
            self.name = "dummy"

    agent = DummyAgent()
    info = AgentInfo(agent=agent, name="test", description="Test")


    try:
        # Try with dict first
        StateWithAgentInfo(
            agents={"test": {"agent": agent, "name": "test", "description": "Test"}}
        )
    except Exception as e:
        pass")

    try:
        # Try with AgentInfo instance
        StateWithAgentInfo(agents={"test": info})
    except Exception as e:

        # Get more details about the error
        if hasattr(e, "errors"):
            for err in e.errors():

    # Step 5: Check if model_config helps

    class StateWithConfig(MessagesState):
        agents: dict[str, AgentInfo] = Field(default_factory=dict)
        model_config = {"arbitrary_types_allowed": True}

    try:
        StateWithConfig(agents={"test": info})
    except Exception as e:
        pass")


if __name__ == "__main__":
    test_step_by_step()
