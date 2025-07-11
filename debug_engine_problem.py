"""Debug the Engine serialization problem in MultiAgent systems."""

from haive.agents.planning.p_and_e.state import PlanExecuteState
from haive.agents.simple.agent import SimpleAgent
from langchain_core.messages import HumanMessage


def test_simple_agent_alone():
    """Test if a simple agent works by itself."""

    try:
        agent = SimpleAgent(name="test_simple")
        result = agent.run("What is 2 + 2?")
        return True
    except Exception as e:
        return False


def test_plan_execute_state_serialization():
    """Test the PlanExecuteState serialization."""

    try:
        # Create state
        state = PlanExecuteState(messages=[HumanMessage("Test")])


        # Test serialization
        serialized = state.model_dump()

        # Test deserialization
        new_state = PlanExecuteState(**serialized)

        return True
    except Exception as e:
        import traceback

        traceback.print_exc()
        return False


def test_multiagent_creation():
    """Test MultiAgentBase creation without running."""

    try:
        from haive.agents.planning.proper_plan_execute import create_proper_plan_execute

        agent = create_proper_plan_execute()

        # Check if state schema has engine field
        if hasattr(agent.state_schema, "model_fields"):
            engine_field = agent.state_schema.model_fields.get("engine")
            if engine_field:
                pass

        return agent
    except Exception as e:
        import traceback

        traceback.print_exc()
        return None


def show_engine_field_problem():
    """Show the exact problem with Engine field."""

    import inspect

    from haive.agents.planning.p_and_e.state import PlanExecuteState
    from haive.core.engine.base import Engine

    # Show Engine class
    # Show PlanExecuteState engine field
    engine_field = PlanExecuteState.model_fields.get("engine")
    if engine_field:

    # Show the field validator
    validators = PlanExecuteState.__pydantic_validators__


def debug_langgraph_input_model():
    """Debug what LangGraph is doing with the input model."""

    try:
        from haive.agents.planning.proper_plan_execute import create_proper_plan_execute

        agent = create_proper_plan_execute()

        # Try to access the LangGraph app
        if hasattr(agent, "_app"):
            app = agent._app

            if hasattr(app, "input_model"):
                input_model = app.input_model

                if hasattr(input_model, "model_fields"):
                    engine_field = input_model.model_fields.get("engine")
                    if engine_field:

    except Exception as e:
        import traceback

        traceback.print_exc()


if __name__ == "__main__":

    # Test components individually
    simple_works = test_simple_agent_alone()
    state_works = test_plan_execute_state_serialization()

    # Test multiagent creation
    multiagent = test_multiagent_creation()

    # Show detailed analysis
    show_engine_field_problem()

    if multiagent:
        debug_langgraph_input_model()

