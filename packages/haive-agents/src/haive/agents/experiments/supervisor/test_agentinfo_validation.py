"""Test AgentInfo validation and serialization."""

import asyncio

# Import AgentInfo
from agent_info import AgentInfo
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig
from langchain_core.tools import tool
from pydantic import BaseModel
from supervisor_state import SupervisorState

from haive.agents.simple.agent import SimpleAgent


@tool
def test_tool():
    """A test tool."""
    return "test"


async def test_agentinfo():
    """Test AgentInfo creation and validation."""
    print("\n=== Testing AgentInfo ===\n")

    # Create a simple agent
    engine = AugLLMConfig(
        name="test_engine",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        tools=[test_tool],
        system_message="Test agent",
    )

    agent = SimpleAgent(name="test_agent", engine=engine)

    print(f"Created agent: {agent.name}")

    # Create AgentInfo
    try:
        agent_info = AgentInfo(
            agent=agent,
            name="test_agent",
            description="Test agent for validation",
            active=True,
        )
        print("✅ AgentInfo created successfully")
        print(f"   Agent type in AgentInfo: {type(agent_info.agent)}")

        # Test serialization
        agent_dict = agent_info.model_dump()
        print(f"\n✅ Serialized to dict")
        print(f"   Keys: {list(agent_dict.keys())}")

        # Test deserialization
        agent_info2 = AgentInfo(**agent_dict)
        print(f"\n✅ Deserialized from dict")
        print(f"   Agent type after deser: {type(agent_info2.agent)}")

    except Exception as e:
        print(f"❌ Error creating AgentInfo: {e}")
        import traceback

        traceback.print_exc()

    # Test in SupervisorState
    print("\n\n=== Testing SupervisorState ===\n")

    try:
        # Method 1: Direct assignment
        state = SupervisorState()
        state.agents["test_agent"] = agent_info
        print("✅ Direct assignment works")

        # Method 2: Through constructor
        state2 = SupervisorState(agents={"test_agent": agent_info})
        print("✅ Constructor with AgentInfo works")

        # Method 3: With dict
        state3 = SupervisorState(agents={"test_agent": agent_dict})
        print("✅ Constructor with dict works")
        print(f"   Agent type in state: {type(state3.agents['test_agent'])}")

    except Exception as e:
        print(f"❌ Error with SupervisorState: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_agentinfo())
