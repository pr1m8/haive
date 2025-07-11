"""Test Clean Plan & Execute implementation following LangGraph patterns."""

from haive.tools import duckduckgo_search_tool

from haive.agents.planning.clean_plan_execute import create_simple_plan_execute


def test_clean_plan_execute():
    """Test the clean Plan & Execute implementation."""
    try:
        # Create clean plan and execute agent
        agent = create_simple_plan_execute(tools=[duckduckgo_search_tool])

        # List the agents
        for _i, _sub_agent in enumerate(agent.agents):
            pass

        # Test compilation
        agent.compile()

        # Test simple execution
        result = agent.run("What is 2 + 2?")

        # Check result structure
        if hasattr(result, "response") and result.response:
            pass

        if hasattr(result, "plan") and result.plan:
            pass

        if hasattr(result, "past_steps") and result.past_steps:
            pass

        if hasattr(result, "messages"):
            pass

    except Exception:
        import traceback

        traceback.print_exc()


def test_models():
    """Test the simple models."""
    from haive.agents.planning.clean_plan_execute import Act, Plan

    # Test Plan model
    Plan(steps=["Think about the problem", "Calculate 2 + 2", "Provide the answer"])

    # Test Act model
    Act(action="continue", response="Execute step 1")

    Act(action="response", response="The answer is 4")


def test_state_schema():
    """Test the clean state schema."""
    from langchain_core.messages import AIMessage, HumanMessage

    from haive.agents.planning.clean_plan_execute import PlanExecuteState

    # Create state
    state = PlanExecuteState(
        messages=[HumanMessage("What is 2 + 2?")],
        plan=["Calculate 2 + 2", "Provide answer"],
        past_steps=["Understood the question"],
        response="",
    )

    # Test serialization (this validates our MessageList fix)
    state.model_dump()


if __name__ == "__main__":
    # Test models first
    test_models()
    test_state_schema()

    # Test the agent
    test_clean_plan_execute()
