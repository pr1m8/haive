"""Test natural multi-task flow: search → compute → translate with dynamic agent addition."""

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
    create_supervisor_agent,
)
from haive.agents.experiments.supervisor.test_utils import add, multiply
from haive.agents.simple.agent import SimpleAgent


async def create_prebuilt_agents():
    """Create our 3 distinct agent types with clear purposes."""

    # 1. Search Agent - for finding information
    search_engine = AugLLMConfig(
        name="search_engine",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        tools=[tavily_search_tool],
        system_message="You are a web search specialist. Use the tavily_search tool to find current information on the internet. Provide accurate, up-to-date results with sources.",
    )

    search_agent = SimpleAgent(
        name="search_agent",
        engine=search_engine,
        description="Web search and research specialist - finds current information online",
    )

    # 2. Math Agent - for calculations
    math_engine = AugLLMConfig(
        name="math_engine",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        tools=[add, multiply],
        system_message="You are a mathematical computation specialist. Use the add and multiply tools for precise calculations. Show your work step by step.",
    )

    math_agent = SimpleAgent(
        name="math_agent",
        engine=math_engine,
        description="Mathematical calculations and numerical analysis specialist",
    )

    # 3. Translation Agent - for language translation (will be added dynamically)
    translation_engine = AugLLMConfig(
        name="translation_engine",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        system_message="You are an expert multilingual translator. Translate text accurately between languages while preserving meaning, tone, and cultural context. Always specify the source and target languages.",
    )

    translation_agent = SimpleAgent(
        name="translation_agent",
        engine=translation_engine,
        description="Expert language translator for multiple languages and cultural contexts",
    )


    return search_agent, math_agent, translation_agent


async def test_multi_task_natural_flow():
    """Test: Find population → Calculate percentage → Translate result."""

    # Create all agents but only give supervisor 2 initially
    search_agent, math_agent, translation_agent = await create_prebuilt_agents()

    # Create supervisor with only search and math agents initially
    supervisor = create_supervisor_agent("task_supervisor")

    # Start with only 2 agents - missing translation!
    initial_state = SupervisorStateWithTools(
        messages=[
            HumanMessage(
                content="""I need you to:
1. Find the current population of France
2. Calculate what 15% of that population would be
3. Translate the final result to Spanish

Please complete all three steps."""
            )
        ],
        agents={
            "search_agent": AgentInfo(
                agent=search_agent,
                name="search_agent",
                description="Web search and research specialist - finds current information online",
                active=True,
            ),
            "math_agent": AgentInfo(
                agent=math_agent,
                name="math_agent",
                description="Mathematical calculations and numerical analysis specialist",
                active=True,
            ),
            # Note: translation_agent NOT included initially!
        },
        active_agents={"search_agent", "math_agent"},
    )

    for name, info in initial_state.agents.items():
        pass")


    # Step 1: Run the multi-task - should identify missing translation capability

    try:
        result1 = await supervisor.arun(
            initial_state, debug=True  # Pass state object directly, not serialized
        )


        # Check if supervisor recognized the need for translation
        messages = result1.get("messages", [])
        supervisor_response = messages[-1].content if messages else ""

        if (
            "translation" in supervisor_response.lower()
            or "translate" in supervisor_response.lower()
        ):
            pass")
        else:
            passd")

    except Exception as e:
        import traceback

        traceback.print_exc()
        return

    # Step 2: Simulate adding translation agent dynamically

    # Add the translation agent to state
    initial_state.agents["translation_agent"] = AgentInfo(
        agent=translation_agent,
        name="translation_agent",
        description="Expert language translator for multiple languages and cultural contexts",
        active=True,
    )
    initial_state.active_agents.add("translation_agent")

    # Sync the dynamic tools
    initial_state.sync_agents()

    for name, info in initial_state.agents.items():
        pass")

    # Step 3: Re-run with all agents available

    # Update the message to retry the full task
    initial_state.messages = [
        HumanMessage(
            content="""Now I have all the agents I need. Please:
1. Find the current population of France
2. Calculate what 15% of that population would be
3. Translate the final result to Spanish

Execute step by step using the appropriate specialist agents."""
        )
    ]

    try:
        result2 = await supervisor.arun(
            initial_state, debug=True  # Pass state object directly
        )


        if result2.get("agent_response"):
            pass

        # Show the natural progression
        if result2.get("next_agent") == "search_agent":
            pass")
        elif result2.get("next_agent") == "math_agent":
            passn")
        elif result2.get("next_agent") == "translation_agent":
            passg")

    except Exception as e:
        import traceback

        traceback.print_exc()

    # Step 4: Show final capabilities


    # Show available handoff tools
    tool_names = [tool.name for tool in initial_state.generated_tools]
    handoff_tools = [name for name in tool_names if name.startswith("handoff_to_")]



if __name__ == "__main__":
    asyncio.run(test_multi_task_natural_flow())
