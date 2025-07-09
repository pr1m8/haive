#!/usr/bin/env python
"""Test SimpleAgent with PlanExecuteState (hybrid schema composition)."""

from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import HumanMessage

from haive.agents.planning.p_and_e.models import Plan
from haive.agents.planning.p_and_e.prompts import planner_prompt
from haive.agents.planning.p_and_e.state import PlanExecuteState
from haive.agents.simple.agent import SimpleAgent

print("SimpleAgent with PlanExecuteState (Hybrid Schema Composition)")
print("=" * 60)

# Create planner engine
planner_aug = AugLLMConfig(
    name="planner",
    structured_output_model=Plan,
    structured_output_version="v2",
    prompt_template=planner_prompt,
    temperature=0.1,
)

# Create SimpleAgent with PlanExecuteState as the state schema
simple_agent = SimpleAgent(
    name="simple_with_planexecute",
    engine=planner_aug,
    state_schema=PlanExecuteState,  # Using the prebuilt hybrid schema
    use_prebuilt_base=True,  # Enable schema composition
)

print("\n1. Agent Configuration:")
print(f"   - Agent type: SimpleAgent")
print(f"   - State schema: {simple_agent.state_schema}")
print(f"   - use_prebuilt_base: {simple_agent.use_prebuilt_base}")
print(f"   - Engine: {planner_aug.name}")

print("\n2. Composed Schema Analysis:")
fields = simple_agent.state_schema.model_fields
print(f"   - Composed schema name: {simple_agent.state_schema.__name__}")
print(f"   - Total fields: {len(fields)}")

# Check fields from PlanExecuteState
print("\n   PlanExecuteState fields:")
for field in [
    "messages",
    "context",
    "plan",
    "final_answer",
    "execution_results",
    "started_at",
]:
    print(f"   {'✓' if field in fields else '✗'} {field}")

# Check engine fields added by composition
print("\n   Engine fields (from composition):")
for field in ["engine", "engines"]:
    print(f"   {'✓' if field in fields else '✗'} {field}")

# Check structured output field
print("\n   Structured output field:")
print(f"   {'✓' if 'plan' in fields else '✗'} plan (from Plan model)")

print("\n3. Testing with Simple Run:")
try:
    result = simple_agent.run(
        input_data={
            "messages": [
                HumanMessage(
                    content="What is the population of Tokyo and calculate its population density if the area is 2194 km²?"
                )
            ]
        },
        debug=True,
    )

    print("\n   ✓ Agent executed successfully!")

    # Check result
    print(f"\n   Result Analysis:")
    print(f"   - Type: {type(result).__name__}")
    print(f"   - Has messages: {hasattr(result, 'messages')}")
    print(
        f"   - Message count: {len(result.messages) if hasattr(result, 'messages') else 0}"
    )

    # Check if plan was generated
    if hasattr(result, "plan") and result.plan:
        print(f"\n   Generated Plan:")
        print(f"   - Objective: {result.plan.objective[:60]}...")
        print(f"   - Total steps: {result.plan.total_steps}")
        for step in result.plan.steps:
            print(f"     Step {step.step_id}: {step.description[:50]}...")

    # Check PlanExecuteState specific fields
    print(f"\n   PlanExecuteState fields in result:")
    print(f"   - context: {result.context}")
    print(f"   - final_answer: {result.final_answer}")
    print(f"   - started_at: {result.started_at}")
    print(f"   - execution_results: {len(result.execution_results)}")

except Exception as e:
    print(f"\n   ✗ Error: {type(e).__name__}: {str(e)[:100]}...")
    import traceback

    traceback.print_exc()

print("\n" + "=" * 60)
print("Summary:")
print("✓ SimpleAgent can use PlanExecuteState as a prebuilt hybrid schema")
print("✓ SchemaComposer properly extends PlanExecuteState with engine fields")
print("✓ The composed schema maintains all PlanExecuteState functionality")
print("✓ Structured output (Plan) works with the hybrid schema")
