"""Test supervisor recognizing it needs a new agent and requesting it."""

import asyncio

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig
from haive.tools.tools.search_tools import tavily_search_tool
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool

from haive.agents.experiments.supervisor.agent_info import AgentInfo
from haive.agents.experiments.supervisor.component_2_tools import (
    SupervisorStateWithTools,
)
from haive.agents.experiments.supervisor.dynamic_supervisor_agent import (
    DynamicSupervisorAgent,
)
from haive.agents.react.agent import ReactAgent
from haive.agents.simple.agent import SimpleAgent

# We'll create agents without translation capability first
# When supervisor identifies need, we'll add a real agent that can handle it


async def test_add_agent_flow():
    """Test supervisor recognizing it needs a new agent."""

    # Create search agent only
    search_engine = AugLLMConfig(
        name="search_engine",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        tools=[tavily_search_tool],
        system_message="You are a search specialist. Use the search tool to find information.",
    )

    search_agent = ReactAgent(name="search_agent", engine=search_engine)

    # Create supervisor with enhanced prompt
    supervisor_engine = AugLLMConfig(
        name="supervisor_engine",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        force_tool_use=True,
        tools=[],  # Tools come from state
        system_message="""You are a task router that delegates work to specialist agents.

Available agents:
{agent_list}

IMPORTANT:
- Analyze each task to determine what capabilities are needed
- If you need a capability that's not available, use choose_agent with "END" and explain what's missing
- Always delegate to the most appropriate agent when available
- For multi-step tasks, break them down and handle each step

When you identify a missing capability:
1. Use choose_agent("END")
2. Explain clearly what agent/capability is needed
3. Describe what the missing agent should be able to do""",
    )

    supervisor = DynamicSupervisorAgent(
        name="capability_supervisor", engine=supervisor_engine
    )

    # Initial state with just search agent
    state = SupervisorStateWithTools()
    state.messages = [
        HumanMessage(
            content="Find information about Paris and then translate it to French"
        )
    ]
    state.agents = {
        "search_agent": AgentInfo(
            agent=search_agent,
            name="search_agent",
            description="Web search specialist",
            active=True,
        )
    }
    state.active_agents = ["search_agent"]
    state.sync_agents()


    # First run - supervisor should recognize it can search but not translate
    result = await supervisor.arun(state, debug=False)

    # Check if supervisor identified the need
    last_message = result.messages[-1]

    if (
        "translat" in last_message.content.lower()
        or "french" in last_message.content.lower()
    ):
        pass
    else:
        pass\n")

    # Create a powerful agent that can translate using its LLM capabilities
    translation_engine = AugLLMConfig(
        name="translation_engine",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        tools=[],  # No tools needed - uses LLM's native capabilities
        system_message="""You are a language specialist capable of translation between multiple languages.
When asked to translate, provide accurate translations using your language knowledge.
Always indicate the source and target languages in your response.""",
    )

    translation_agent = SimpleAgent(name="translation_agent", engine=translation_engine)

    # Add to state
    state.add_agent(
        "translation_agent",
        translation_agent,
        "Translation specialist for multiple languages",
        active=True,
    )
    state.sync_agents()


    # Add a message acknowledging the addition
    state.messages.append(
        HumanMessage(
            content="I've added a translation agent. Please complete the original task: Find information about Paris and translate it to French"
        )
    )

    result = await supervisor.arun(state, debug=False)

    # Create a math agent that uses LLM for calculations
    math_engine = AugLLMConfig(
        name="math_engine",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        tools=[],  # Uses LLM's math capabilities
        system_message="""You are a mathematics specialist.
Perform calculations and mathematical operations accurately.
Show your work and explain the calculations step by step.""",
    )

    math_agent = SimpleAgent(name="math_agent", engine=math_engine)

    # Add math agent
    state.add_agent(
        "math_agent", math_agent, "Mathematics and calculation specialist", active=True
    )
    state.sync_agents()

    # Complex task
    state.messages.append(
        HumanMessage(
            content="""
    1. Search for the population of Tokyo
    2. Calculate what percentage it is of Japan's total population (125 million)
    3. Translate the result to Spanish
    """
        )
    )


    result = await supervisor.arun(state, debug=False)



if __name__ == "__main__":
    asyncio.run(test_add_agent_flow())
