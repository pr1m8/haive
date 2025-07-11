# src/haive/agents/plan_and_execute/example.py
"""Example usage of the Plan and Execute agent."""

from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool

from haive.agents.planning.p_and_e.agent import PlanAndExecuteAgent
from haive.agents.planning.p_and_e.models import Act, Plan
from haive.agents.planning.p_and_e.prompts import (
    executor_prompt,
    planner_prompt,
    replan_prompt,
)
from haive.agents.planning.p_and_e.state import PlanExecuteState


# Example tools
@tool
def search(query: str) -> str:
    """Search for information."""
    return f"Results for '{query}'"


@tool
def calculate(expression: str) -> float:
    """Calculate a mathematical expression."""
    return eval(expression)


# Example 1: Using default engines
agent = PlanAndExecuteAgent()

# Example 2: Customizing engines
agent_with_tools = PlanAndExecuteAgent(
    engines={
        "planner": AugLLMConfig(
            name="planner",
            structured_output_model=Plan,
            structured_output_version="v2",
            prompt_template=planner_prompt,
            temperature=0.1,
        ),
        "executor": AugLLMConfig(
            name="executor",
            tools=[search, calculate],
            prompt_template=executor_prompt,
            temperature=0.3,
        ),
        "replanner": AugLLMConfig(
            name="replanner",
            structured_output_model=Act,
            structured_output_version="v2",
            prompt_template=replan_prompt,
            temperature=0.2,
        ),
    }
)

# Use the agent
from haive.agents.simple.agent import SimpleAgent

planner_simple_agent = SimpleAgent(
    engine=agent_with_tools.engines["planner"], state_schema=PlanExecuteState
)

input_data = {
    "messages": [
        HumanMessage(
            content="What is the population of Tokyo and calculate its population density if the area is 2194 km²?"
        )
    ]
}

# Note: This will fail due to the serialization issue
# Messages are being converted to dicts somewhere in the persistence layer
try:
    result = planner_simple_agent.run(input_data=input_data, debug=False)
except Exception as e:
