#!/usr/bin/env python
"""Test schema composition with PlanAndExecuteAgent using hybrid PlanExecuteState."""

from langchain_core.messages import HumanMessage

from haive.agents.planning.p_and_e.agent import PlanAndExecuteAgent
from haive.agents.planning.p_and_e.state import PlanExecuteState

# Create PlanAndExecuteAgent
agent = PlanAndExecuteAgent(name="test_p_and_e")


# The agent should have composed a schema that extends PlanExecuteState
fields = agent.state_schema.model_fields

# Check for key fields from PlanExecuteState
plan_execute_fields = [
    "messages",
    "plan",
    "context",
    "final_answer",
    "execution_results",
]
for field in plan_execute_fields:
    if field in fields:
        pass")
    else:
        pass")

# Check for engine management fields
engine_fields = ["engine", "engines"]
for field in engine_fields:
    if field in fields:
        pass")
    else:
        pass")

try:
    # Create state instance
    state = agent.state_schema()

    # Check inherited behavior

except Exception as e:
    pass")

try:
    input_data = {
        "messages": [HumanMessage(content="Create a simple web scraper in Python")]
    }


    # Run the agent (this will fail for now due to graph building issues, but shows the schema works)
    result = agent.run(input_data=input_data, debug=True)


except Exception as e:

    # Even if execution fails, we can check if the schema was properly composed

