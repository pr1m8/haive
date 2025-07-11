"""Simple test showing the natural flow without complex serialization."""

import asyncio

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig
from haive.tools.tools.search_tools import tavily_search_tool
from langchain_core.messages import AIMessage, HumanMessage

from haive.agents.experiments.supervisor.agent_info import AgentInfo
from haive.agents.experiments.supervisor.component_2_tools import (
    SupervisorStateWithTools,
)
from haive.agents.experiments.supervisor.dynamic_supervisor_agent import (
    create_supervisor_agent,
)
from haive.agents.experiments.supervisor.test_utils import add, multiply
from haive.agents.simple.agent import SimpleAgent


async def test_simple_natural_flow():
    """Test the natural flow: start with 2 agents, need 3rd, add it, use it."""


    # Create search agent
    search_engine = AugLLMConfig(
        name="search_engine",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        tools=[tavily_search_tool],
        system_message="You are a web search specialist.",
    )
    search_agent = SimpleAgent(name="search_agent", engine=search_engine)

    # Create math agent
    math_engine = AugLLMConfig(
        name="math_engine",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        tools=[add, multiply],
        system_message="You are a math specialist.",
    )
    math_agent = SimpleAgent(name="math_agent", engine=math_engine)

    # Create translation agent (will be added later)
    translation_engine = AugLLMConfig(
        name="translation_engine",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        system_message="You are a translation specialist.",
    )
    translation_agent = SimpleAgent(name="translation_agent", engine=translation_engine)


    # Step 1: Create supervisor with only 2 agents
    supervisor = create_supervisor_agent("simple_supervisor")

    # Create state with only search and math agents
    state = SupervisorStateWithTools()
    state.messages = [
        HumanMessage(
            content="Find France population, calculate 15% of it, translate to Spanish"
        )
    ]

    # Add only 2 agents initially
    state.agents = {
        "search_agent": AgentInfo(
            agent=search_agent,
            name="search_agent",
            description="Web search specialist",
            active=True,
        ),
        "math_agent": AgentInfo(
            agent=math_agent,
            name="math_agent",
            description="Math calculation specialist",
            active=True,
        ),
    }
    state.active_agents = {"search_agent", "math_agent"}
    state.sync_agents()  # Generate tools


    # Step 2: Test supervisor recognizes missing capability

    # Call supervisor node directly to see its decision
    supervisor_result = supervisor.supervisor_node(state)


    if supervisor_result.get("need_new_agent"):
        pass")
    else:
        return

    # Step 3: Add translation agent

    state.agents["translation_agent"] = AgentInfo(
        agent=translation_agent,
        name="translation_agent",
        description="Language translation specialist",
        active=True,
    )
    state.active_agents.add("translation_agent")
    state.sync_agents()  # Regenerate tools


    # Step 4: Test supervisor now has all capabilities

    # Update message for retry
    state.messages = [
        HumanMessage(
            content="Now I have all agents. Find France population, calculate 15% of it, translate to Spanish"
        )
    ]

    supervisor_result2 = supervisor.supervisor_node(state)


    if supervisor_result2.get("next_agent"):
        pass
    else:
        passy")

    # Step 5: Test full workflow execution

    try:
        # Use the supervisor's arun with the complete state
        final_result = await supervisor.arun(
            state, debug=True  # Pass state object directly, not model_dump()
        )


    except Exception as e:
        import traceback

        traceback.print_exc()



if __name__ == "__main__":
    asyncio.run(test_simple_natural_flow())
