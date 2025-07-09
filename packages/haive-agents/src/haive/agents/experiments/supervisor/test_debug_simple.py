"""Debug supervisor basic setup - correct approach with ReactAgent delegation."""

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
from haive.agents.react.agent import ReactAgent
from haive.agents.simple.agent import SimpleAgent


async def test_debug_simple():
    """Debug supervisor that delegates to ReactAgent with search tool."""
    print("🔧 Debug supervisor with ReactAgent delegation...")

    # Create ReactAgent with tavily search tool
    search_engine = AugLLMConfig(
        name="search_engine",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        tools=[tavily_search_tool],
        system_message="You are a search specialist that helps find information using web search.",
    )

    search_agent = ReactAgent(name="search_agent", engine=search_engine)

    # Create initial state with the search agent
    state = SupervisorStateWithTools()
    state.messages = [HumanMessage(content="Find information about France")]
    state.agents = {
        "search_agent": AgentInfo(
            agent=search_agent,
            name="search_agent",
            description="Web search specialist using Tavily",
            active=True,
        )
    }
    state.active_agents = {"search_agent"}
    state.sync_agents()  # This generates the handoff tools dynamically

    # Create supervisor with NO tools - tools come from state sync
    supervisor_engine = AugLLMConfig(
        name="debug_supervisor",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        force_tool_use=True,
        tools=[],  # NO tools - they come from state.sync_agents()
        system_message="You are a task router. Use handoff tools to delegate work to specialist agents.",
    )

    supervisor = DynamicSupervisorAgent(
        name="debug_supervisor", engine=supervisor_engine
    )

    print(f"✅ Created supervisor: {supervisor.name}")
    print(f"✅ Created ReactAgent: {search_agent.name}")
    print(f"📋 State agents: {list(state.agents.keys())}")
    print(f"🔧 State generated tools: {len(state.generated_tools)}")

    # Test the full workflow
    print("\n1. Testing supervisor delegation to ReactAgent...")
    try:
        # The state has the agents and generates tools dynamically
        result = await supervisor.arun(state, debug=False)
        print(f"   Result type: {type(result)}")

        # Check if the ReactAgent was called and returned a human message
        if hasattr(result, "messages") and result.messages:
            last_msg = result.messages[-1]
            print(f"   Last message type: {type(last_msg)}")
            print(
                f"   Last message content: {getattr(last_msg, 'content', 'No content')[:100]}..."
            )

            # Check if it's a human message from agent execution
            if hasattr(last_msg, "content") and "France" in str(last_msg.content):
                print("   ✅ Successfully got search results from ReactAgent!")
            else:
                print("   ⚠️  No search results found in response")
        else:
            print("   ❌ No messages in result")

    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback

        traceback.print_exc()

    print("\n🎉 Debug ReactAgent delegation complete!")


if __name__ == "__main__":
    asyncio.run(test_debug_simple())
