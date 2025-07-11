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


# Run the agent
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


    # Check if we have a plan in the result
    if hasattr(result, "plan") and result.plan:
        for step in result.plan.steps:
            pass

    # Check the last message for parsed output
    if hasattr(result, "messages") and len(result.messages) > 0:
        last_msg = result.messages[-1]
        if hasattr(last_msg, "parsed") and isinstance(last_msg.parsed, Plan):
            pass")

except Exception as e:
    import traceback

    traceback.print_exc()
