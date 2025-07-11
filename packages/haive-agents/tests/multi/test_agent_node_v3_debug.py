"""Debug test for AgentNodeV3 schema validation issues."""

import asyncio
from typing import List

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.schema.prebuilt.multi_agent_state import MultiAgentState
from haive.core.schema.state_schema import StateSchema
from langchain_core.messages import HumanMessage
from pydantic import Field

# Import Agent for model_rebuild
from haive.agents.base.agent import Agent
from haive.agents.simple.agent import SimpleAgent

# Fix forward reference issue
MultiAgentState.model_rebuild()


class PlannerState(StateSchema):
    """State for planner agent."""

    messages: list = Field(default_factory=list)
    plan: str = Field(default="")
    steps: list[str] = Field(default_factory=list)


async def test_debug_schema_validation():
    """Debug schema validation in AgentNodeV3."""

    # Create simple agent
    planner = SimpleAgent(
        name="planner", engine=AugLLMConfig(temperature=0.7), state_schema=PlannerState
    )


    # Check schema fields
    for field_name, field_info in planner.state_schema.model_fields.items():
        pass

    # Test direct schema instantiation
    try:
        test_data = {
            "messages": [HumanMessage(content="test")],
            "plan": "test plan",
            "steps": ["step1", "step2"],
        }


        # Try to instantiate the schema directly
        schema_instance = planner.state_schema(**test_data)

        # Try to dump back to dict
        dumped = schema_instance.model_dump()

    except Exception as e:

        # Check for engine fields
        for field_name, field_info in planner.state_schema.model_fields.items():
            if hasattr(field_info.annotation, "__origin__"):
                pass
            else:
                pass

    # Test MultiAgentState
    try:
        state = MultiAgentState(
            agents=[planner], messages=[HumanMessage(content="test message")]
        )


        # Try to get agent state
        agent_state = state.get_agent_state("planner")

    except Exception as e:

    return True


if __name__ == "__main__":
    result = asyncio.run(test_debug_schema_validation())
