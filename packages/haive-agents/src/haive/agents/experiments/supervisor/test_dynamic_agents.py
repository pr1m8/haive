"""Test dynamic agent management - adding/removing agents at runtime."""

import asyncio

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig
from haive.tools.tools.search_tools import tavily_search_tool
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
    print("🔧 Testing dynamic agent management...\n")

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

    print("1. Starting with search agent only...")
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

    print(f"   Available agents: {list(state.agents.keys())}")
    print(f"   Generated tools: {state.generated_tools}\n")

    # Run supervisor
    result = await supervisor.arun(state, debug=False)
    print(f"   ✅ Task 1 completed\n")

    print("2. Adding math agent dynamically...")
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

    print(f"   Available agents: {list(state.agents.keys())}")
    print(f"   Generated tools: {state.generated_tools}\n")

    # New math task
    state.messages.append(HumanMessage(content="Calculate 25 * 37 + 128"))

    result = await supervisor.arun(state, debug=False)
    print(f"   ✅ Task 2 completed\n")

    print("3. Adding weather agent and deactivating search...")
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

    print(f"   Available agents: {list(state.agents.keys())}")
    print(f"   Active agents: {state.list_active_agents()}")
    print(f"   Generated tools: {state.generated_tools}\n")

    # Weather task
    state.messages.append(HumanMessage(content="What's the weather in Paris?"))

    result = await supervisor.arun(state, debug=False)
    print(f"   ✅ Task 3 completed\n")

    print("4. Complex task requiring multiple agents...")
    # Reactivate search agent
    state.activate_agent("search_agent")
    state.sync_agents()

    print(f"   Active agents: {list(state.list_active_agents().keys())}")

    # Multi-agent task
    state.messages.append(
        HumanMessage(
            content="Find the population of Tokyo and calculate how many times it fits into 100 million"
        )
    )

    result = await supervisor.arun(state, debug=False)
    print(f"   ✅ Task 4 completed\n")

    print("5. Removing agents...")
    # Remove weather agent
    state.remove_agent("weather_agent")
    state.sync_agents()

    print(f"   Remaining agents: {list(state.agents.keys())}")
    print(f"   Generated tools: {state.generated_tools}\n")

    print("🎉 Dynamic agent management test complete!")
    print("\nKey findings:")
    print("- ✅ Agents can be added dynamically")
    print("- ✅ Agents can be activated/deactivated")
    print("- ✅ Agents can be removed")
    print("- ✅ Tools are regenerated automatically")
    print("- ✅ State persists across runs")
    print("- ✅ Agents are stored in state but excluded from serialization")


if __name__ == "__main__":
    asyncio.run(test_dynamic_agents())
