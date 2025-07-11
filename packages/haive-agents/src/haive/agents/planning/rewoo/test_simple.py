"""Simple ReWOO planner agent."""

from typing import List

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig
from haive.core.schema.prebuilt.llm_state import LLMState
from pydantic import Field

from haive.agents.planning.rewoo.models import ReWOOPlan
from haive.agents.planning.rewoo.planner.prompts import REWOO_PLANNING_TEMPLATE
from haive.agents.simple.agent import SimpleAgent


class ReWOOPlannerState(LLMState):
    """State for ReWOO planner with available tools."""

    available_tools: list[str] = Field(
        default_factory=list, description="List of available tool names for planning"
    )


# Define engine
engine = AugLLMConfig(
    llm_config=AzureLLMConfig(model="gpt-4"),
    temperature=0.7,
    structured_output_model=ReWOOPlan,
    structured_output_version="v2",
    system_message=REWOO_PLANNING_TEMPLATE,
)

# Create simple agent with state
agent = SimpleAgent(name="rewoo_planner", engine=engine, state_schema=ReWOOPlannerState)
