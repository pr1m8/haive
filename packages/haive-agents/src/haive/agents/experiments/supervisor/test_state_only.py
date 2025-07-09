"""Test just the state serialization without running the agent."""

import asyncio

import ormsgpack
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig
from haive.tools.tools.search_tools import tavily_search_tool
from langchain_core.messages import HumanMessage

from haive.agents.experiments.supervisor.agent_info import AgentInfo
from haive.agents.experiments.supervisor.component_2_tools import (
    SupervisorStateWithTools,
)
from haive.agents.react.agent import ReactAgent


async def test_state_serialization():
    """Test state serialization directly."""
    print("🔧 Testing state serialization...\n")

    # Create ReactAgent
    search_engine = AugLLMConfig(
        name="search_engine",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        tools=[tavily_search_tool],
        system_message="You are a search specialist.",
    )

    search_agent = ReactAgent(name="search_agent", engine=search_engine)

    # Create state with agent
    state = SupervisorStateWithTools()
    state.messages = [HumanMessage(content="Find information about France")]

    print("1. Testing empty state:")
    try:
        serialized = ormsgpack.packb(state.model_dump())
        print("✅ Empty state is serializable")
    except Exception as e:
        print(f"❌ Empty state failed: {e}")

    print("\n2. Adding agent to state:")
    state.agents = {
        "search_agent": AgentInfo(
            agent=search_agent,
            name="search_agent",
            description="Web search specialist",
            active=True,
        )
    }
    state.active_agents = {"search_agent"}

    print("\n3. Testing state.model_dump():")
    try:
        state_dict = state.model_dump()
        print("✅ model_dump() succeeded")
        print(f"   Keys: {list(state_dict.keys())}")
        if "agents" in state_dict:
            print(f"   Agents: {list(state_dict['agents'].keys())}")
    except Exception as e:
        print(f"❌ model_dump() failed: {e}")

    print("\n4. Testing serialization of model_dump():")
    try:
        state_dict = state.model_dump()
        serialized = ormsgpack.packb(state_dict)
        print("✅ state.model_dump() is serializable")
    except Exception as e:
        print(f"❌ state.model_dump() not serializable: {e}")

    print("\n5. Testing direct state serialization:")
    try:
        serialized = ormsgpack.packb(state)
        print("✅ Direct state is serializable")
    except Exception as e:
        print(f"❌ Direct state not serializable: {e}")

    print("\n6. Checking what's in AgentInfo after model_dump:")
    try:
        agent_info_dict = state.agents["search_agent"].model_dump()
        print(f"   AgentInfo keys: {list(agent_info_dict.keys())}")
        print(f"   Agent field type: {type(agent_info_dict.get('agent'))}")
        print(f"   Agent field content: {agent_info_dict.get('agent')}")
    except Exception as e:
        print(f"   Error: {e}")


if __name__ == "__main__":
    asyncio.run(test_state_serialization())
