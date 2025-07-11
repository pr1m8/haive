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
    # Create a simple agent
    engine = AugLLMConfig(
        name="test_engine",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        tools=[test_tool],
        system_message="Test agent",
    )

    agent = SimpleAgent(name="test_agent", engine=engine)

    # Create AgentInfo
    try:
        agent_info = AgentInfo(
            agent=agent,
            name="test_agent",
            description="Test agent for validation",
            active=True,
        )

        # Test serialization
        agent_dict = agent_info.model_dump()

        # Test deserialization
        AgentInfo(**agent_dict)

    except Exception:
        import traceback

        traceback.print_exc()

    # Test in SupervisorState

    try:
        # Method 1: Direct assignment
        state = SupervisorState()
        state.agents["test_agent"] = agent_info

        # Method 2: Through constructor
        SupervisorState(agents={"test_agent": agent_info})

        # Method 3: With dict
        SupervisorState(agents={"test_agent": agent_dict})

    except Exception:
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_agentinfo())
