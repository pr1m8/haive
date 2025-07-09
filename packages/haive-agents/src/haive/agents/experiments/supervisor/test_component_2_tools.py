"""Test Component 2: Tool generation from state.agents with choice model."""

from haive.agents.experiments.supervisor.component_2_tools import (
    SupervisorStateWithTools,
)
from haive.agents.experiments.supervisor.test_component_1_state import (
    create_real_agents,
)


def test_choice_model_integration():
    """Test choice model syncs with agents in state."""
    print("\n🧪 Testing Choice Model Integration...")

    # Create state with choice model
    state = SupervisorStateWithTools()
    print(f"✅ State created with choice model: {state.agent_choice_model.model_name}")

    # Check initial choice model options
    initial_options = state.agent_choice_model.option_names
    print(f"Initial choice options: {initial_options}")

    # Create and add real agents
    agents = create_real_agents()

    # Add agents one by one and see choice model update
    state.add_agent(
        "search_agent",
        agents["search_agent"],
        "Web search and research specialist",
        active=True,
    )

    options_after_first = state.agent_choice_model.option_names
    print(f"After adding search_agent: {options_after_first}")

    state.add_agent(
        "math_agent",
        agents["math_agent"],
        "Mathematical calculations specialist",
        active=True,
    )

    options_after_second = state.agent_choice_model.option_names
    print(f"After adding math_agent: {options_after_second}")

    # Test choice model validation
    ChoiceModel = state.agent_choice_model.current_model

    # Test valid choices
    try:
        valid_choice = ChoiceModel(choice="search_agent")
        print(f"✅ Valid choice test passed: {valid_choice.choice}")
    except Exception as e:
        print(f"❌ Valid choice test failed: {e}")

    try:
        end_choice = ChoiceModel(choice="END")
        print(f"✅ END choice test passed: {end_choice.choice}")
    except Exception as e:
        print(f"❌ END choice test failed: {e}")

    # Test invalid choice
    try:
        invalid_choice = ChoiceModel(choice="nonexistent_agent")
        print(f"❌ Invalid choice should have failed: {invalid_choice.choice}")
    except Exception as e:
        print(f"✅ Invalid choice correctly rejected: {type(e).__name__}")


def test_tool_generation():
    """Test dynamic tool generation from agents."""
    print("\n🧪 Testing Tool Generation...")

    # Create state and add agents
    state = SupervisorStateWithTools()
    agents = create_real_agents()

    # Add all agents
    state.add_agent(
        "search_agent", agents["search_agent"], "Web search specialist", True
    )
    state.add_agent(
        "math_agent", agents["math_agent"], "Math calculations specialist", True
    )
    state.add_agent(
        "planning_agent", agents["planning_agent"], "Planning specialist", False
    )

    # Check generated tool names
    print(f"Generated tool names: {state.generated_tools}")

    # Get actual tool objects
    tools = state.get_all_tools()
    print(f"Generated {len(tools)} tool objects")

    for tool in tools:
        print(f"  - {tool.name}: {tool.description}")

    # Test tool removal when agent removed
    print(f"\nBefore removal: {len(state.generated_tools)} tools")
    state.remove_agent("planning_agent")
    print(f"After removal: {len(state.generated_tools)} tools")
    print(f"Updated tool names: {state.generated_tools}")


def test_handoff_tool_execution():
    """Test handoff tool execution."""
    print("\n🧪 Testing Handoff Tool Execution...")

    # Create state with agents
    state = SupervisorStateWithTools()
    agents = create_real_agents()

    state.add_agent(
        "search_agent", agents["search_agent"], "Web search specialist", True
    )
    state.add_agent("math_agent", agents["math_agent"], "Math specialist", True)

    # Get tools
    tools = state.get_all_tools()

    # Find handoff tool for search_agent
    search_handoff_tool = None
    for tool in tools:
        if tool.name == "handoff_to_search_agent":
            search_handoff_tool = tool
            break

    if search_handoff_tool:
        print(f"✅ Found handoff tool: {search_handoff_tool.name}")

        # Test tool execution
        result = search_handoff_tool.invoke(
            {"task_description": "Search for Python tutorials"}
        )
        print(f"Tool execution result: {result}")

        # Check if state was updated
        print(
            f"State routing after tool: next_agent={state.next_agent}, task={state.agent_task}"
        )
    else:
        print("❌ Handoff tool not found")


def test_choice_tool_execution():
    """Test choice tool execution."""
    print("\n🧪 Testing Choice Tool Execution...")

    # Create state with agents
    state = SupervisorStateWithTools()
    agents = create_real_agents()

    state.add_agent(
        "search_agent", agents["search_agent"], "Web search specialist", True
    )
    state.add_agent("math_agent", agents["math_agent"], "Math specialist", True)

    # Get tools
    tools = state.get_all_tools()

    # Find choice tool
    choice_tool = None
    for tool in tools:
        if tool.name == "choose_agent":
            choice_tool = tool
            break

    if choice_tool:
        print(f"✅ Found choice tool: {choice_tool.name}")

        # Test different task types
        test_tasks = [
            "Search for information about Python",
            "Calculate 25 multiplied by 8",
            "Create a plan for learning AI",
            "Some random task",
        ]

        for task in test_tasks:
            print(f"\nTask: {task}")
            result = choice_tool.invoke(
                {"task_description": task, "reasoning": "Testing choice logic"}
            )
            print(f"Choice result: {result}")
    else:
        print("❌ Choice tool not found")


def test_field_validation():
    """Test field validation with choice model."""
    print("\n🧪 Testing Field Validation...")

    # Create state with agents
    state = SupervisorStateWithTools()
    agents = create_real_agents()

    state.add_agent(
        "search_agent", agents["search_agent"], "Web search specialist", True
    )

    # Test valid agent assignment
    try:
        state.next_agent = "search_agent"
        print(f"✅ Valid assignment worked: {state.next_agent}")
    except Exception as e:
        print(f"❌ Valid assignment failed: {e}")

    # Test END assignment
    try:
        state.next_agent = "END"
        print(f"✅ END assignment worked: {state.next_agent}")
    except Exception as e:
        print(f"❌ END assignment failed: {e}")

    # Test invalid agent assignment
    try:
        state.next_agent = "nonexistent_agent"
        print(f"❌ Invalid assignment should have failed: {state.next_agent}")
    except Exception as e:
        print(f"✅ Invalid assignment correctly rejected: {type(e).__name__}")


if __name__ == "__main__":
    print("🚀 Testing Component 2: Tool Generation & Choice Model")
    print("=" * 60)

    try:
        test_choice_model_integration()
        test_tool_generation()
        test_handoff_tool_execution()
        test_choice_tool_execution()
        test_field_validation()

        print("\n🎉 Component 2 tests completed successfully!")

    except Exception as e:
        print(f"\n❌ Component 2 test failed: {e}")
        raise
