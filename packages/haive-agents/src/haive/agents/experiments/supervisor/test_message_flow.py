"""Test message-based flow to demonstrate the fix."""

import asyncio

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig
from haive.tools.tools.search_tools import tavily_search_tool
from langchain_core.messages import HumanMessage

from haive.agents.experiments.supervisor.agent_info import AgentInfo
from haive.agents.experiments.supervisor.component_2_tools import (
    SupervisorStateWithTools,
)
from haive.agents.experiments.supervisor.dynamic_supervisor_agent import (
    DynamicSupervisorAgent,
)
from haive.agents.experiments.supervisor.test_utils import add, multiply
from haive.agents.simple.agent import SimpleAgent


async def test_message_based_flow():
    """Test the fixed message-based supervisor flow."""

    # Create a simple search agent
    search_engine = AugLLMConfig(
        name="search_engine",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        tools=[tavily_search_tool],
        system_message="You are a search specialist.",
    )
    search_agent = SimpleAgent(name="search_agent", engine=search_engine)

    # Create supervisor with engine that forces tool use
    supervisor_engine = AugLLMConfig(
        name="supervisor_engine",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        force_tool_use=True,  # Force the supervisor to always call a tool
        system_message="""You are a task router that MUST use tools to delegate work.

Available agents:
{agent_list}

IMPORTANT: You MUST call one of the available tools. Do not respond with text.

Your available tools:
- handoff_to_[agent_name]: Delegate work to a specific agent
- choose_agent: Select an option (use "END" if no agent is suitable)

For each request:
1. Analyze what type of work is needed
2. Call the appropriate handoff tool to delegate to the right agent
3. If no agent matches, call choose_agent with "END"

You are a routing system - always use tools, never provide text responses.""",
    )

    supervisor = DynamicSupervisorAgent(
        name="message_supervisor",
        engine=supervisor_engine,
        force_tool_use=True,  # Also set on the agent level
    )

    # Create state with agent
    state = SupervisorStateWithTools()
    state.messages = [HumanMessage(content="Find information about France")]
    state.agents = {
        "search_agent": AgentInfo(
            agent=search_agent,
            name="search_agent",
            description="Web search specialist",
            active=True,
        )
    }
    state.active_agents = {"search_agent"}
    state.sync_agents()


    # Test 1: Check supervisor setup

    # Test 2: Full workflow via arun with just message
    try:
        result2 = await supervisor.arun("Find information about France", debug=True)
        if isinstance(result2, dict) and "agents" in result2:
            pass
        else:
            passlt")
    except Exception as e:
        import traceback

        traceback.print_exc()



if __name__ == "__main__":
    asyncio.run(test_message_based_flow())
