#!/usr/bin/env python
"""Test SimpleAgent with PlanExecuteState (hybrid schema composition)."""

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

# Create SimpleAgent with PlanExecuteState as the state schema
simple_agent = SimpleAgent(
    name="simple_with_planexecute",
    engine=planner_aug,
    state_schema=PlanExecuteState,  # Using the prebuilt hybrid schema
    use_prebuilt_base=True,  # Enable schema composition
)


fields = simple_agent.state_schema.model_fields

# Check fields from PlanExecuteState
for field in [
    "messages",
    "context",
    "plan",
    "final_answer",
    "execution_results",
    "started_at",
]:
    passd}")

# Check engine fields added by composition
for field in ["engine", "engines"]:
    passd}")

# Check structured output field

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


    # Check result

    # Check if plan was generated
    if hasattr(result, "plan") and result.plan:
        for step in result.plan.steps:
            pass

    # Check PlanExecuteState specific fields

except Exception as e:
    import traceback

    traceback.print_exc()

