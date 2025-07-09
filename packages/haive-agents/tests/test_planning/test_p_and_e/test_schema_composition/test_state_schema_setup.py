#!/usr/bin/env python
"""Test different ways to set state schema in SimpleAgent."""

from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import HumanMessage

from haive.agents.planning.p_and_e.models import Plan
from haive.agents.planning.p_and_e.prompts import planner_prompt
from haive.agents.planning.p_and_e.state import PlanExecuteState
from haive.agents.simple.agent import SimpleAgent

# Create planner engine
planner_aug = AugLLMConfig(
    name="planner",
    structured_output_model=Plan,
    structured_output_version="v2",
    prompt_template=planner_prompt,
    temperature=0.1,
)

print("Different ways to set state schema in SimpleAgent")
print("=" * 60)

print("\n1. Default behavior (no state_schema specified):")
planner_simple_agent = SimpleAgent(engine=planner_aug)
print(f"   - Schema: {planner_simple_agent.state_schema.__name__}")
print(f"   - Fields: {len(planner_simple_agent.state_schema.model_fields)}")
print(
    f"   - Has 'plan' field: {'plan' in planner_simple_agent.state_schema.model_fields}"
)

print("\n2. Explicitly setting state_schema to PlanExecuteState:")
planner_with_plan_state = SimpleAgent(
    engine=planner_aug, state_schema=PlanExecuteState  # Specify the state schema
)
print(f"   - Schema: {planner_with_plan_state.state_schema.__name__}")
print(f"   - Fields: {len(planner_with_plan_state.state_schema.model_fields)}")
print(f"   - Has PlanExecuteState fields:")
for field in ["context", "final_answer", "execution_results", "started_at"]:
    has_field = field in planner_with_plan_state.state_schema.model_fields
    print(f"     {'✓' if has_field else '✗'} {field}")

print("\n3. Using use_prebuilt_base parameter:")
planner_with_prebuilt = SimpleAgent(
    engine=planner_aug,
    state_schema=PlanExecuteState,
    use_prebuilt_base=True,  # Enable composition with prebuilt schema
)
print(f"   - Schema: {planner_with_prebuilt.state_schema.__name__}")
print(f"   - Fields: {len(planner_with_prebuilt.state_schema.model_fields)}")

print("\n4. Comparing field counts:")
print(
    f"   - Default SimpleAgent: {len(planner_simple_agent.state_schema.model_fields)} fields"
)
print(
    f"   - With PlanExecuteState: {len(planner_with_plan_state.state_schema.model_fields)} fields"
)
print(
    f"   - With prebuilt composition: {len(planner_with_prebuilt.state_schema.model_fields)} fields"
)

print("\n5. Creating state instances:")
print("   Default state:")
default_state = planner_simple_agent.state_schema()
print(f"   - Type: {type(default_state).__name__}")
print(f"   - Has plan: {hasattr(default_state, 'plan')}")

print("\n   PlanExecuteState:")
plan_state = planner_with_plan_state.state_schema()
print(f"   - Type: {type(plan_state).__name__}")
print(f"   - Has plan: {hasattr(plan_state, 'plan')}")
print(f"   - Has context: {hasattr(plan_state, 'context')}")
print(f"   - Has execution_results: {hasattr(plan_state, 'execution_results')}")

print("\n6. Constructor options summary:")
print(
    """
   SimpleAgent(
       engine=your_engine,
       state_schema=YourStateClass,     # Optional: specify state schema
       use_prebuilt_base=True          # Optional: enable composition
   )
   
   Examples:
   - SimpleAgent(engine=planner_aug)                           # Auto-generated schema
   - SimpleAgent(engine=planner_aug, state_schema=PlanExecuteState)  # Use specific schema
   - SimpleAgent(engine=planner_aug, state_schema=PlanExecuteState, use_prebuilt_base=True)  # Hybrid composition
"""
)
