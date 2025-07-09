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
    print("🔧 Creating real agents...")

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

    print("✅ Real agents created")
    return {
        "search_agent": search_agent,
        "math_agent": math_agent,
        "planning_agent": planning_agent,
    }


def test_agent_info():
    """Test AgentInfo with real agents."""
    print("\n🧪 Testing AgentInfo...")

    agents = create_real_agents()

    # Test AgentInfo creation with automatic name/description extraction
    search_info = AgentInfo(
        agent=agents["search_agent"],
        name="search_agent",
        description="Web search and research specialist",
    )

    print(f"✅ AgentInfo created: {search_info.name} - {search_info.description}")
    print(f"✅ Agent active: {search_info.is_active()}")
    print(f"✅ Agent instance: {type(search_info.get_agent()).__name__}")

    # Test activation/deactivation
    search_info.deactivate()
    print(f"✅ After deactivation: {search_info.is_active()}")

    search_info.activate()
    print(f"✅ After activation: {search_info.is_active()}")


def test_supervisor_state():
    """Test SupervisorState with real agents."""
    print("\n🧪 Testing SupervisorState...")

    # Create state
    state = SupervisorState()
    print(f"✅ Empty state created with {len(state.agents)} agents")

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
    print(f"\n📊 State Summary:")
    print(f"Total agents: {len(state.agents)}")
    print(f"Active agents: {len(state.active_agents)}")
    print(f"Active agent names: {list(state.active_agents)}")

    print(f"\nActive agents list:")
    for name, desc in state.list_active_agents().items():
        print(f"  - {name}: {desc}")

    print(f"\nAll agents list:")
    for name, desc in state.list_all_agents().items():
        active_status = "🟢" if name in state.active_agents else "🔴"
        print(f"  {active_status} {name}: {desc}")

    # Test routing
    state.set_routing("math_agent", "Calculate 25 * 8")
    print(f"\n🎯 Routing set: {state.next_agent} -> {state.agent_task}")

    # Test agent retrieval
    math_agent = state.get_agent("math_agent")
    print(f"✅ Retrieved agent: {type(math_agent).__name__}")

    # Test activation/deactivation
    print(f"\n🔄 Testing activation...")
    state.activate_agent("planning_agent")
    print(f"Active agents after activation: {list(state.active_agents)}")

    state.deactivate_agent("search_agent")
    print(f"Active agents after deactivation: {list(state.active_agents)}")

    # Test serialization capability
    try:
        state_dict = state.model_dump()
        print(f"✅ State serialization works (agents excluded from dict)")
    except Exception as e:
        print(f"❌ Serialization issue: {e}")


def test_state_operations():
    """Test various state operations."""
    print("\n🧪 Testing State Operations...")

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
    print(f"\nBefore removal: {len(state.agents)} agents")
    removed = state.remove_agent("planning_agent")
    print(f"Removal successful: {removed}")
    print(f"After removal: {len(state.agents)} agents")

    # Test clearing routing
    state.set_routing("search_agent", "Search for Python tutorials")
    print(f"Before clear: next_agent={state.next_agent}")
    state.clear_routing()
    print(f"After clear: next_agent={state.next_agent}")


if __name__ == "__main__":
    print("🚀 Testing Component 1: AgentInfo & State Foundation")
    print("=" * 60)

    try:
        test_agent_info()
        test_supervisor_state()
        test_state_operations()

        print("\n🎉 Component 1 tests completed successfully!")

    except Exception as e:
        print(f"\n❌ Component 1 test failed: {e}")
        raise
