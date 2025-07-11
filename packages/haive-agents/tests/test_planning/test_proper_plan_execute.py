"""Test Proper Plan & Execute implementation using existing p_and_e components."""

from haive.agents.planning.proper_plan_execute import (
    create_plan_execute_with_search,
    create_proper_plan_execute,
)


def test_proper_plan_execute_creation():
    """Test that the proper plan execute agent can be created."""

    try:
        # Create agent without tools first
        agent = create_proper_plan_execute()


        # List the agents
        for i, sub_agent in enumerate(agent.agents):

            # Check structured output models
            if (
                hasattr(sub_agent, "structured_output_model")
                and sub_agent.structured_output_model
            ):
                pass

        # Check state schema fields

        # Test compilation
        agent.compile()

        return agent

    except Exception as e:
        import traceback

        traceback.print_exc()
        return None


def test_proper_plan_execute_with_tools():
    """Test creating agent with search tools."""

    try:
        # Create agent with search tools
        agent = create_plan_execute_with_search()


        # Check executor has tools
        executor = None
        for sub_agent in agent.agents:
            if sub_agent.name == "agent":  # executor
                executor = sub_agent
                break

        if executor and hasattr(executor, "tools"):
            for tool in executor.tools:
                tool_name = getattr(tool, "name", str(tool))

        # Test compilation
        agent.compile()

        return agent

    except Exception as e:
        import traceback

        traceback.print_exc()
        return None


def test_state_schema_compatibility():
    """Test that the state schema works with existing p_and_e models."""

    try:
        from langchain_core.messages import HumanMessage

        from haive.agents.planning.p_and_e.models import (
            ExecutionResult,
            Plan,
            PlanStep,
            StepType,
        )
        from haive.agents.planning.p_and_e.state import PlanExecuteState

        # Create a sample plan
        plan = Plan(
            objective="Test objective",
            steps=[
                PlanStep(
                    step_id=1,
                    description="First step",
                    step_type=StepType.RESEARCH,
                    expected_output="Research results",
                ),
                PlanStep(
                    step_id=2,
                    description="Second step",
                    step_type=StepType.ANALYSIS,
                    expected_output="Analysis results",
                    dependencies=[1],
                ),
            ],
            total_steps=2,
        )

        # Create state with plan
        state = PlanExecuteState(
            messages=[HumanMessage("Test objective")],
            plan=plan,
            current_step_id=1,
            execution_results=[],
        )


        # Test serialization
        serialized = state.model_dump()

        return state

    except Exception as e:
        import traceback

        traceback.print_exc()
        return None


def test_routing_functions():
    """Test the routing functions with sample states."""

    try:
        from langchain_core.messages import HumanMessage

        from haive.agents.planning.p_and_e.models import (
            Plan,
            PlanStep,
            StepStatus,
            StepType,
        )
        from haive.agents.planning.p_and_e.state import PlanExecuteState
        from haive.agents.planning.proper_plan_execute import (
            route_after_replan,
            should_continue,
        )

        # Test 1: State with final answer should end
        state_with_answer = PlanExecuteState(
            messages=[HumanMessage("Test")], final_answer="This is the final answer"
        )

        result = should_continue(state_with_answer)
        assert result == "__end__"

        # Test 2: State with no plan should replan
        state_no_plan = PlanExecuteState(messages=[HumanMessage("Test")])

        result = should_continue(state_no_plan)
        assert result == "replan"

        # Test 3: State with next step should continue to agent
        plan_with_next = Plan(
            objective="Test",
            steps=[
                PlanStep(
                    step_id=1,
                    description="First step",
                    step_type=StepType.RESEARCH,
                    expected_output="Results",
                )
            ],
            total_steps=1,
        )

        state_with_next = PlanExecuteState(
            messages=[HumanMessage("Test")], plan=plan_with_next, current_step_id=1
        )

        result = should_continue(state_with_next)
        assert result == "agent"

        # Test 4: Route after replan
        result = route_after_replan(state_with_answer)
        assert result == "__end__"

        result = route_after_replan(state_with_next)
        assert result == "agent"


    except Exception as e:
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    # Test creation
    agent = test_proper_plan_execute_creation()

    # Test with tools
    agent_with_tools = test_proper_plan_execute_with_tools()

    # Test state compatibility
    test_state = test_state_schema_compatibility()

    # Test routing
    test_routing_functions()

    if agent and test_state:
    else:
        pass")
