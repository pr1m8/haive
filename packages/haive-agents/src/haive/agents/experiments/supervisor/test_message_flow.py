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
    print("🔧 Creating supervisor with agents...")

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

    print(f"✅ State created with {len(state.agents)} agents")
    print(f"📋 Available agents: {list(state.agents.keys())}")

    # Test 1: Check supervisor setup
    print("\n1. Testing supervisor setup...")
    print(
        f"   Supervisor engine: {supervisor.engine.name if supervisor.engine else 'None'}"
    )
    print(
        f"   Supervisor tools: {len(supervisor.engine.tools) if supervisor.engine else 0}"
    )
    print(f"   State agents: {len(state.agents)}")
    print(f"   State tools: {len(state.generated_tools)}")

    # Test 2: Full workflow via arun with just message
    print("\n2. Testing full workflow via arun with just message...")
    try:
        result2 = await supervisor.arun("Find information about France", debug=True)
        print(
            f"   Final result keys: {list(result2.keys()) if isinstance(result2, dict) else 'not dict'}"
        )
        if isinstance(result2, dict) and "agents" in result2:
            print(f"   Agents preserved: {len(result2['agents'])} agents")
        else:
            print("   ⚠️  Agents field missing from final result")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback

        traceback.print_exc()

    print("\n🎉 Message flow test complete!")


if __name__ == "__main__":
    asyncio.run(test_message_based_flow())
