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

    return {"math_agent": math_agent, "planning_agent": planning_agent}


def test_basic_setup():
    """Test basic supervisor setup without execution."""

    # Create supervisor
    supervisor = DynamicSupervisorV2(
        name="test_supervisor", state_schema=None  # Will use default SupervisorState
    )

    if supervisor.agent_registry.list_available():
        pass")
    else:
        pass")

    # Test choice model
    if supervisor.agent_choice_model:
        options = supervisor.agent_choice_model.option_names
    else:
        pass")

    # Test initial tools (should be minimal)
    if hasattr(supervisor, "engine") and supervisor.engine:
        tool_names = [getattr(t, "name", "unknown") for t in supervisor.engine.tools]
    else:
        passet")

    return supervisor


def test_agent_addition():
    """Test adding agents to supervisor."""

    # Create supervisor
    supervisor = DynamicSupervisorV2(name="test_supervisor")

    # Create test agents
    agents = create_test_agents()

    supervisor.add_agent(
        "math_agent", agents["math_agent"], "Performs mathematical calculations"
    )

    # Check registry
    available = supervisor.agent_registry.list_available()

    # Check choice model
    if supervisor.agent_choice_model:
        options = supervisor.agent_choice_model.option_names

    supervisor.add_agent(
        "planning_agent",
        agents["planning_agent"],
        "Creates structured plans and organizes tasks",
    )

    # Check registry again
    available = supervisor.agent_registry.list_available()

    # Check choice model again
    if supervisor.agent_choice_model:
        options = supervisor.agent_choice_model.option_names

    # Check tools
    if hasattr(supervisor, "engine") and supervisor.engine:
        tool_names = [getattr(t, "name", "unknown") for t in supervisor.engine.tools]

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

        for expected in expected_tools:
            if expected in tool_names:
                pass")
            else:
                pass")

    return supervisor


def test_choice_model_validation():
    """Test choice model validation."""

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

        try:
            choice1 = ChoiceModel(choice="math_agent")
        except Exception as e:
            pass")

        try:
            choice2 = ChoiceModel(choice="planning_agent")
        except Exception as e:
            pass")

        try:
            choice3 = ChoiceModel(choice="END")
        except Exception as e:
            pass")

        try:
            invalid_choice = ChoiceModel(choice="nonexistent_agent")
        except Exception as e:
            pass")

    return supervisor


def test_tool_execution():
    """Test basic tool execution."""

    # Create supervisor with agents
    supervisor = DynamicSupervisorV2(name="test_supervisor")
    agents = create_test_agents()

    supervisor.add_agent("math_agent", agents["math_agent"], "Math specialist")

    # Test list_agents tool
    if hasattr(supervisor, "engine") and supervisor.engine:
        list_tool = None
        for tool in supervisor.engine.tools:
            if tool.name == "list_agents":
                list_tool = tool
                break

        if list_tool:
            try:
                result = list_tool.invoke({})
            except Exception as e:
                pass")
        else:
            pass")

    return supervisor


def run_all_tests():
    """Run all tests."""

    try:
        # Test 1: Basic setup
        test_basic_setup()

        # Test 2: Agent addition
        test_agent_addition()

        # Test 3: Choice model validation
        test_choice_model_validation()

        # Test 4: Tool execution
        supervisor4 = test_tool_execution()

        return supervisor4  # Return the fully configured supervisor

    except Exception as e:
        raise


if __name__ == "__main__":
    supervisor = run_all_tests()
