#!/usr/bin/env python
"""Test schema composition with SimpleAgent and planner engine."""

from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import HumanMessage

from haive.agents.planning.p_and_e.models import Plan
from haive.agents.planning.p_and_e.prompts import planner_prompt
from haive.agents.simple.agent import SimpleAgent


def test_schema_composition():
    """Test that schema composition works with prebuilt base schemas."""

    # Create planner engine
    planner_aug = AugLLMConfig(
        name="planner",
        structured_output_model=Plan,
        structured_output_version="v2",
        prompt_template=planner_prompt,
        temperature=0.1,
    )

    # Create SimpleAgent with planner engine
    planner_simple_agent = SimpleAgent(
        name="planner_agent",
        engine=planner_aug,
        use_prebuilt_base=True,  # This should trigger schema composition
    )

    # Check the composed schema
    fields = planner_simple_agent.state_schema.model_fields

    # Check specific fields we expect
    expected_fields = ["messages", "engine", "engines", "plan"]
    for field in expected_fields:
        if field in fields:
            pass")
        else:
            pass")

    # Test creating state instance
    try:
        state = planner_simple_agent.state_schema()
        if hasattr(state, "plan"):
            pass
    except Exception as e:
        pass")

    # Test running the agent
    try:
        input_data = {
            "messages": [
                HumanMessage(
                    content="What is the population of Tokyo and calculate its population density if the area is 2194 km²?"
                )
            ]
        }


        result = planner_simple_agent.run(input_data=input_data, debug=True)


        # Check if we got a plan in the result
        if hasattr(result, "plan") and result.plan:
            for step in result.plan.steps:
                pass

        # Check messages in result
        if hasattr(result, "messages"):
            last_msg = result.messages[-1]
            if hasattr(last_msg, "parsed") and last_msg.parsed:
                if isinstance(last_msg.parsed, Plan):
                    pass")

    except Exception as e:
        import traceback

        traceback.print_exc()



if __name__ == "__main__":
    test_schema_composition()
