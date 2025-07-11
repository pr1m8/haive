#!/usr/bin/env python
"""Summary of schema composition working correctly."""

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
planner_simple_agent = SimpleAgent(engine=planner_aug)


result = planner_simple_agent.run(
    input_data={
        "messages": [
            HumanMessage(
                content="What is the population of Tokyo and calculate its population density if the area is 2194 km²?"
            )
        ]
    }
)

if hasattr(result, "plan") and result.plan:
    for _i, _step in enumerate(result.plan.steps):
        pass
