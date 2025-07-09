"""Test utilities for dynamic supervisor components."""

from typing import Any, Dict

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig
from haive.tools.tools.search_tools import tavily_search_tool
from langchain_core.tools import tool

from haive.agents.experiments.supervisor.agent_info import AgentInfo
from haive.agents.simple.agent import SimpleAgent


# Create test tools
@tool
def add(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b


@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers together."""
    return a * b


@tool
def create_plan(task: str) -> str:
    """Create a structured plan for a given task."""
    return f"Plan for {task}:\n1. Analyze requirements\n2. Break down into steps\n3. Execute\n4. Verify"


async def create_test_agents() -> Dict[str, AgentInfo]:
    """Create test agents for supervisor testing."""

    # Search agent with tavily tool
    search_engine = AugLLMConfig(
        name="search_engine",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        tools=[tavily_search_tool],
        system_message="You are a web search specialist. Use the tavily_search tool to find information.",
    )

    search_agent = SimpleAgent(name="search_agent", engine=search_engine)

    # Math agent with calculation tools
    math_engine = AugLLMConfig(
        name="math_engine",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        tools=[add, multiply],
        system_message="You are a math specialist. Use the add and multiply tools for calculations.",
    )

    math_agent = SimpleAgent(name="math_agent", engine=math_engine)

    # Planning agent (inactive by default)
    planning_engine = AugLLMConfig(
        name="planning_engine",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        tools=[create_plan],
        system_message="You are a planning specialist. Create structured plans for tasks.",
    )

    planning_agent = SimpleAgent(name="planning_agent", engine=planning_engine)

    # Create agent info dictionary
    agents_dict = {
        "search_agent": AgentInfo(
            agent=search_agent,
            name="search_agent",
            description="Web search and research specialist",
            active=True,
        ),
        "math_agent": AgentInfo(
            agent=math_agent,
            name="math_agent",
            description="Mathematical calculations specialist",
            active=True,
        ),
        "planning_agent": AgentInfo(
            agent=planning_agent,
            name="planning_agent",
            description="Task planning and organization specialist",
            active=False,  # Inactive placeholder
        ),
    }

    return agents_dict


def get_test_state_with_agents():
    """Get a test state with agents pre-configured."""
    from .component_2_tools import SupervisorStateWithTools

    state = SupervisorStateWithTools()

    # This would trigger the model validator to create tools
    # But we need to set agents first

    return state
