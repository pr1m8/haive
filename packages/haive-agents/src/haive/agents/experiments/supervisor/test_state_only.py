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

    try:
        serialized = ormsgpack.packb(state.model_dump())
    except Exception as e:
        pass")

    state.agents = {
        "search_agent": AgentInfo(
            agent=search_agent,
            name="search_agent",
            description="Web search specialist",
            active=True,
        )
    }
    state.active_agents = {"search_agent"}

    try:
        state_dict = state.model_dump()
        if "agents" in state_dict:
            pass
    except Exception as e:
        pass")

    try:
        state_dict = state.model_dump()
        serialized = ormsgpack.packb(state_dict)
    except Exception as e:
        pass")

    try:
        ormsgpack.packb(state)
    except Exception as e:
        pass")

    try:
        agent_info_dict = state.agents["search_agent"].model_dump()
    except Exception as e:
        pass


if __name__ == "__main__":
    asyncio.run(test_state_serialization())
