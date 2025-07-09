#!/usr/bin/env python
"""Test schema composition with SimpleAgent and planner engine."""

from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import HumanMessage

from haive.agents.planning.p_and_e.models import Plan
from haive.agents.planning.p_and_e.prompts import planner_prompt
from haive.agents.simple.agent import SimpleAgent


def test_schema_composition():
    """Test that schema composition works with prebuilt base schemas."""

    print("=== Testing Schema Composition with SimpleAgent + Planner Engine ===\n")

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
    print("1. Checking composed schema fields:")
    fields = planner_simple_agent.state_schema.model_fields
    print(f"   - Schema name: {planner_simple_agent.state_schema.__name__}")
    print(f"   - Total fields: {len(fields)}")
    print(f"   - Fields: {list(fields.keys())}")
    print()

    # Check specific fields we expect
    expected_fields = ["messages", "engine", "engines", "plan"]
    for field in expected_fields:
        if field in fields:
            print(f"   ✓ {field}: {fields[field].annotation}")
        else:
            print(f"   ✗ {field}: MISSING!")
    print()

    # Test creating state instance
    print("2. Testing state instantiation:")
    try:
        state = planner_simple_agent.state_schema()
        print("   ✓ State created successfully")
        print(f"   - messages type: {type(state.messages)}")
        print(f"   - engine: {state.engine}")
        print(f"   - engines: {state.engines}")
        if hasattr(state, "plan"):
            print(f"   - plan: {state.plan}")
    except Exception as e:
        print(f"   ✗ Error creating state: {e}")
    print()

    # Test running the agent
    print("3. Testing agent execution:")
    try:
        input_data = {
            "messages": [
                HumanMessage(
                    content="What is the population of Tokyo and calculate its population density if the area is 2194 km²?"
                )
            ]
        }

        print("   Running agent with input:")
        print(f"   {input_data['messages'][0].content}")
        print()

        result = planner_simple_agent.run(input_data=input_data, debug=True)

        print("\n   ✓ Agent executed successfully!")
        print(f"\n   Result type: {type(result)}")

        # Check if we got a plan in the result
        if hasattr(result, "plan") and result.plan:
            print(f"\n   Generated Plan:")
            print(f"   - Objective: {result.plan.objective}")
            print(f"   - Total steps: {result.plan.total_steps}")
            for step in result.plan.steps:
                print(f"     Step {step.step_id}: {step.description}")

        # Check messages in result
        if hasattr(result, "messages"):
            print(f"\n   Messages count: {len(result.messages)}")
            last_msg = result.messages[-1]
            print(f"   Last message type: {type(last_msg)}")
            if hasattr(last_msg, "parsed") and last_msg.parsed:
                print(f"   Parsed output type: {type(last_msg.parsed)}")
                if isinstance(last_msg.parsed, Plan):
                    print("   ✓ Successfully parsed as Plan!")

    except Exception as e:
        print(f"   ✗ Error running agent: {e}")
        import traceback

        traceback.print_exc()

    print("\n=== Test Complete ===")


if __name__ == "__main__":
    test_schema_composition()
