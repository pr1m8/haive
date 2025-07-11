"""Test dynamic agent management - adding/removing agents at runtime."""

import asyncio

from langchain_core.messages import HumanMessage

# Create some test tools
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
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig
from haive.tools.tools.search_tools import tavily_search_tool


@tool
def calculate(expression: str) -> str:
    """Calculate a mathematical expression."""
    try:
        result = eval(expression)
        return f"The result is: {result}"
    except Exception as e:
        return f"Error calculating: {e}"


@tool
def get_weather(location: str) -> str:
    """Get weather for a location (mock)."""
    return f"Weather in {location}: Sunny, 72°F"


async def test_dynamic_agents():
    """Test adding and removing agents dynamically."""
    # Create initial search agent
    search_engine = AugLLMConfig(
        name="search_engine",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        tools=[tavily_search_tool],
        system_message="You are a search specialist. Use the search tool to find information.",
    )

    search_agent = ReactAgent(name="search_agent", engine=search_engine)

    # Create supervisor
    supervisor_engine = AugLLMConfig(
        name="supervisor_engine",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        force_tool_use=True,
        tools=[],  # Tools come from state
        system_message="""You are a task router. Use handoff tools to delegate work to specialist agents.
Always analyze the task and choose the most appropriate agent.
If no suitable agent exists, explain what capability is missing.""",
    )

    supervisor = DynamicSupervisorAgent(
        name="dynamic_supervisor", engine=supervisor_engine
    )

    # Create initial state with just search agent
    state = SupervisorStateWithTools()
    state.messages = [HumanMessage(content="What's the capital of France?")]
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

    # Run supervisor
    await supervisor.arun(state, debug=False)

    # Create math agent
    math_engine = AugLLMConfig(
        name="math_engine",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        tools=[calculate],
        system_message="You are a math specialist. Use the calculate tool for computations.",
    )

    math_agent = SimpleAgent(name="math_agent", engine=math_engine)

    # Add to existing state
    state.add_agent("math_agent", math_agent, "Mathematics specialist", active=True)
    state.sync_agents()

    # New math task
    state.messages.append(HumanMessage(content="Calculate 25 * 37 + 128"))

    await supervisor.arun(state, debug=False)

    # Create weather agent
    weather_engine = AugLLMConfig(
        name="weather_engine",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        tools=[get_weather],
        system_message="You are a weather specialist. Use the weather tool to get conditions.",
    )

    weather_agent = SimpleAgent(name="weather_agent", engine=weather_engine)

    # Add weather agent
    state.add_agent(
        "weather_agent", weather_agent, "Weather information specialist", active=True
    )

    # Deactivate search agent
    state.deactivate_agent("search_agent")
    state.sync_agents()

    # Weather task
    state.messages.append(HumanMessage(content="What's the weather in Paris?"))

    await supervisor.arun(state, debug=False)

    # Reactivate search agent
    state.activate_agent("search_agent")
    state.sync_agents()

    # Multi-agent task
    state.messages.append(
        HumanMessage(
            content="Find the population of Tokyo and calculate how many times it fits into 100 million"
        )
    )

    await supervisor.arun(state, debug=False)

    # Remove weather agent
    state.remove_agent("weather_agent")
    state.sync_agents()


if __name__ == "__main__":
    asyncio.run(test_dynamic_agents())
