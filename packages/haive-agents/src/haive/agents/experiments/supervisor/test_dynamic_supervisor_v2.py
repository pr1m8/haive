"""Test the dynamic supervisor v2 with basic setup."""

from haive.core.engine import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool

from haive.agents.experiments.supervisor.dynamic_supervisor_v2 import (
    DynamicSupervisorV2,
)
from haive.agents.simple.agent import SimpleAgent


# Create basic test tools
@tool
def add(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b


@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers together."""
    return a * b


def create_test_agents():
    """Create simple test agents."""
    print("🔧 Creating test agents...")

    # Math agent with calculation tools
    math_engine = AugLLMConfig(
        name="math_engine",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        tools=[add, multiply],
        system_message="You are a math specialist. Perform calculations as requested.",
    )

    math_agent = SimpleAgent(name="math_agent", engine=math_engine)

    # Planning agent with basic capabilities
    planning_engine = AugLLMConfig(
        name="planning_engine",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        tools=[],
        system_message="You are a planning specialist. Create structured plans and organize tasks.",
    )

    planning_agent = SimpleAgent(name="planning_agent", engine=planning_engine)

    print("✅ Test agents created")
    return {"math_agent": math_agent, "planning_agent": planning_agent}


def test_basic_setup():
    """Test basic supervisor setup without execution."""
    print("🚀 Testing Dynamic Supervisor V2 - Basic Setup")
    print("=" * 50)

    # Create supervisor
    supervisor = DynamicSupervisorV2(
        name="test_supervisor", state_schema=None  # Will use default SupervisorState
    )

    print("\n--- Testing Empty Registry ---")
    if supervisor.agent_registry.list_available():
        print("❌ Registry should be empty initially")
    else:
        print("✅ Registry is empty initially")

    # Test choice model
    print("\n--- Testing Choice Model ---")
    if supervisor.agent_choice_model:
        options = supervisor.agent_choice_model.option_names
        print(f"✅ Choice model initialized with options: {options}")
    else:
        print("❌ Choice model not initialized")

    # Test initial tools (should be minimal)
    print("\n--- Testing Initial Tools ---")
    if hasattr(supervisor, "engine") and supervisor.engine:
        tool_names = [getattr(t, "name", "unknown") for t in supervisor.engine.tools]
        print(f"Initial tools: {tool_names}")
    else:
        print("⚠️ No engine available yet")

    return supervisor


def test_agent_addition():
    """Test adding agents to supervisor."""
    print("\n🔧 Testing Agent Addition")
    print("=" * 30)

    # Create supervisor
    supervisor = DynamicSupervisorV2(name="test_supervisor")

    # Create test agents
    agents = create_test_agents()

    print("\n--- Adding Math Agent ---")
    supervisor.add_agent(
        "math_agent", agents["math_agent"], "Performs mathematical calculations"
    )

    # Check registry
    available = supervisor.agent_registry.list_available()
    print(f"Registry after adding math agent: {available}")

    # Check choice model
    if supervisor.agent_choice_model:
        options = supervisor.agent_choice_model.option_names
        print(f"Choice model options: {options}")

    print("\n--- Adding Planning Agent ---")
    supervisor.add_agent(
        "planning_agent",
        agents["planning_agent"],
        "Creates structured plans and organizes tasks",
    )

    # Check registry again
    available = supervisor.agent_registry.list_available()
    print(f"Registry after adding planning agent: {available}")

    # Check choice model again
    if supervisor.agent_choice_model:
        options = supervisor.agent_choice_model.option_names
        print(f"Choice model options: {options}")

    # Check tools
    if hasattr(supervisor, "engine") and supervisor.engine:
        tool_names = [getattr(t, "name", "unknown") for t in supervisor.engine.tools]
        print(f"Available tools: {tool_names}")

        # Check for expected tools
        expected_tools = [
            "list_agents",
            "choose_agent",
            "handoff_to_math_agent",
            "forward_to_math_agent",
            "handoff_to_planning_agent",
            "forward_to_planning_agent",
            "execution_status",
        ]

        print("\n--- Tool Verification ---")
        for expected in expected_tools:
            if expected in tool_names:
                print(f"✅ {expected}")
            else:
                print(f"❌ Missing: {expected}")

    return supervisor


def test_choice_model_validation():
    """Test choice model validation."""
    print("\n🧪 Testing Choice Model Validation")
    print("=" * 35)

    # Create supervisor with agents
    supervisor = DynamicSupervisorV2(name="test_supervisor")
    agents = create_test_agents()

    supervisor.add_agent("math_agent", agents["math_agent"], "Math specialist")
    supervisor.add_agent(
        "planning_agent", agents["planning_agent"], "Planning specialist"
    )

    # Test choice model directly
    if supervisor.agent_choice_model:
        ChoiceModel = supervisor.agent_choice_model.current_model

        print("--- Testing Valid Choices ---")
        try:
            choice1 = ChoiceModel(choice="math_agent")
            print(f"✅ Valid choice: {choice1.choice}")
        except Exception as e:
            print(f"❌ Error with valid choice: {e}")

        try:
            choice2 = ChoiceModel(choice="planning_agent")
            print(f"✅ Valid choice: {choice2.choice}")
        except Exception as e:
            print(f"❌ Error with valid choice: {e}")

        try:
            choice3 = ChoiceModel(choice="END")
            print(f"✅ Valid choice: {choice3.choice}")
        except Exception as e:
            print(f"❌ Error with valid choice: {e}")

        print("\n--- Testing Invalid Choice ---")
        try:
            invalid_choice = ChoiceModel(choice="nonexistent_agent")
            print(f"❌ Invalid choice should have failed: {invalid_choice.choice}")
        except Exception as e:
            print(f"✅ Invalid choice correctly rejected: {e}")

    return supervisor


def test_tool_execution():
    """Test basic tool execution."""
    print("\n🔧 Testing Tool Execution")
    print("=" * 25)

    # Create supervisor with agents
    supervisor = DynamicSupervisorV2(name="test_supervisor")
    agents = create_test_agents()

    supervisor.add_agent("math_agent", agents["math_agent"], "Math specialist")

    # Test list_agents tool
    print("--- Testing list_agents tool ---")
    if hasattr(supervisor, "engine") and supervisor.engine:
        list_tool = None
        for tool in supervisor.engine.tools:
            if tool.name == "list_agents":
                list_tool = tool
                break

        if list_tool:
            try:
                result = list_tool.invoke({})
                print(f"✅ list_agents result: {result}")
            except Exception as e:
                print(f"❌ list_agents error: {e}")
        else:
            print("❌ list_agents tool not found")

    return supervisor


def run_all_tests():
    """Run all tests."""
    print("🧪 Running All Dynamic Supervisor V2 Tests")
    print("=" * 45)

    try:
        # Test 1: Basic setup
        supervisor1 = test_basic_setup()

        # Test 2: Agent addition
        supervisor2 = test_agent_addition()

        # Test 3: Choice model validation
        supervisor3 = test_choice_model_validation()

        # Test 4: Tool execution
        supervisor4 = test_tool_execution()

        print("\n🎉 All tests completed!")
        return supervisor4  # Return the fully configured supervisor

    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        raise


if __name__ == "__main__":
    supervisor = run_all_tests()
