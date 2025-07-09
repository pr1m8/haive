#!/usr/bin/env python
"""Simple test of schema composition with direct run() call."""

from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import HumanMessage

from haive.agents.planning.p_and_e.models import Plan
from haive.agents.planning.p_and_e.prompts import planner_prompt
from haive.agents.simple.agent import SimpleAgent

# Create planner engine
planner_aug = AugLLMConfig(
    name="planner",
    structured_output_model=Plan,
    structured_output_version="v2",
    prompt_template=planner_prompt,
    temperature=0.1,
)

# Create SimpleAgent with planner engine
planner_simple_agent = SimpleAgent(name="planner_agent", engine=planner_aug)

print("Schema Composition Test\n" + "=" * 50)
print(f"✓ Schema name: {planner_simple_agent.state_schema.__name__}")
print(f"✓ Schema fields: {list(planner_simple_agent.state_schema.model_fields.keys())}")
print(f"✓ Has 'plan' field: {'plan' in planner_simple_agent.state_schema.model_fields}")

# Run the agent
print("\nRunning agent...")
try:
    result = planner_simple_agent.run(
        input_data={
            "messages": [
                HumanMessage(
                    content="What is the population of Tokyo and calculate its population density if the area is 2194 km²?"
                )
            ]
        },
        debug=True,
    )

    print("\n✓ Agent executed successfully!")

    # Check if we have a plan in the result
    if hasattr(result, "plan") and result.plan:
        print(f"\nGenerated Plan:")
        print(f"- Objective: {result.plan.objective}")
        print(f"- Total steps: {result.plan.total_steps}")
        for step in result.plan.steps:
            print(f"  Step {step.step_id}: {step.description}")

    # Check the last message for parsed output
    if hasattr(result, "messages") and len(result.messages) > 0:
        last_msg = result.messages[-1]
        if hasattr(last_msg, "parsed") and isinstance(last_msg.parsed, Plan):
            print("\n✓ Last message contains parsed Plan!")

except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback

    traceback.print_exc()
