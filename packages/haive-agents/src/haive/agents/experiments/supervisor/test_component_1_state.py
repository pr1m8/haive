"""Test Component 1: AgentInfo & State Foundation with real agents."""

from haive.core.engine import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig
from haive.tools.tools.search_tools import tavily_search_tool
from langchain_core.tools import tool

from haive.agents.experiments.supervisor.agent_info import AgentInfo
from haive.agents.experiments.supervisor.supervisor_state import SupervisorState
from haive.agents.simple.agent import SimpleAgent


# Create real domain tools
@tool
def add(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b


@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers together."""
    return a * b


@tool
def create_plan(goal: str, steps: int = 3) -> str:
    """Create a simple plan for achieving a goal."""
    return f"Plan for '{goal}':\n" + "\n".join(
        [f"{i+1}. Step {i+1}" for i in range(steps)]
    )


def create_real_agents():
    """Create the 3 real agents for testing."""

    # 1. Search agent with tavily
    search_engine = AugLLMConfig(
        name="search_engine",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        tools=[tavily_search_tool],
        system_message="You are a web search and research specialist. Use tavily to find information.",
    )
    search_agent = SimpleAgent(name="search_agent", engine=search_engine)

    # 2. Math agent with calculation tools
    math_engine = AugLLMConfig(
        name="math_engine",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        tools=[add, multiply],
        system_message="You are a mathematical calculations specialist.",
    )
    math_agent = SimpleAgent(name="math_agent", engine=math_engine)

    # 3. Planning agent (inactive placeholder)
    planning_engine = AugLLMConfig(
        name="planning_engine",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        tools=[create_plan],
        system_message="You are a task planning and organization specialist.",
    )
    planning_agent = SimpleAgent(name="planning_agent", engine=planning_engine)

    return {
        "search_agent": search_agent,
        "math_agent": math_agent,
        "planning_agent": planning_agent,
    }


def test_agent_info():
    """Test AgentInfo with real agents."""

    agents = create_real_agents()

    # Test AgentInfo creation with automatic name/description extraction
    search_info = AgentInfo(
        agent=agents["search_agent"],
        name="search_agent",
        description="Web search and research specialist",
    )


    # Test activation/deactivation
    search_info.deactivate()

    search_info.activate()


def test_supervisor_state():
    """Test SupervisorState with real agents."""

    # Create state
    state = SupervisorState()

    # Create real agents
    agents = create_real_agents()

    # Add agents to state (2 active, 1 inactive)
    state.add_agent(
        "search_agent",
        agents["search_agent"],
        "Web search and research specialist",
        active=True,
    )

    state.add_agent(
        "math_agent",
        agents["math_agent"],
        "Mathematical calculations specialist",
        active=True,
    )

    state.add_agent(
        "planning_agent",
        agents["planning_agent"],
        "Task planning and organization specialist",
        active=False,  # Inactive placeholder
    )

    # Test state queries

    for name, desc in state.list_active_agents().items():
        pass

    for name, desc in state.list_all_agents().items():
        active_status = "🟢" if name in state.active_agents else "🔴"

    # Test routing
    state.set_routing("math_agent", "Calculate 25 * 8")

    # Test agent retrieval
    math_agent = state.get_agent("math_agent")

    # Test activation/deactivation
    state.activate_agent("planning_agent")

    state.deactivate_agent("search_agent")

    # Test serialization capability
    try:
        state.model_dump()
    except Exception as e:
        pass")


def test_state_operations():
    """Test various state operations."""

    state = SupervisorState()
    agents = create_real_agents()

    # Add all agents
    for name, agent in agents.items():
        descriptions = {
            "search_agent": "Web search and research specialist",
            "math_agent": "Mathematical calculations specialist",
            "planning_agent": "Task planning and organization specialist",
        }
        active = name != "planning_agent"  # Planning starts inactive

        state.add_agent(name, agent, descriptions[name], active)

    # Test remove operation
    removed = state.remove_agent("planning_agent")

    # Test clearing routing
    state.set_routing("search_agent", "Search for Python tutorials")
    state.clear_routing()


if __name__ == "__main__":

    try:
        test_agent_info()
        test_supervisor_state()
        test_state_operations()


    except Exception as e:
        raise
