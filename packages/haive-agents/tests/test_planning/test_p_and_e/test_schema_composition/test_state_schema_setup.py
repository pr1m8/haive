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


planner_simple_agent = SimpleAgent(engine=planner_aug)

planner_with_plan_state = SimpleAgent(
    engine=planner_aug, state_schema=PlanExecuteState  # Specify the state schema
)
for field in ["context", "final_answer", "execution_results", "started_at"]:
    has_field = field in planner_with_plan_state.state_schema.model_fields

planner_with_prebuilt = SimpleAgent(
    engine=planner_aug,
    state_schema=PlanExecuteState,
    use_prebuilt_base=True,  # Enable composition with prebuilt schema
)


default_state = planner_simple_agent.state_schema()

plan_state = planner_with_plan_state.state_schema()
