"""Test the DynamicSupervisorAgent implementation."""

import asyncio

from langchain_core.messages import HumanMessage

from haive.agents.experiments.supervisor.component_2_tools import (
    SupervisorStateWithTools,
)
from haive.agents.experiments.supervisor.dynamic_supervisor_agent import (
    create_supervisor_agent,
)
from haive.agents.experiments.supervisor.test_utils import create_test_agents


async def test_supervisor_agent():
    """Test the DynamicSupervisorAgent with our working components."""

    # Create test agents using our working utility
    agents_dict = await create_test_agents()

    # Create supervisor agent (no engine needed for this test)
    supervisor = create_supervisor_agent("dynamic_supervisor")


    # Test with a math task

    initial_state = SupervisorStateWithTools(
        messages=[HumanMessage(content="Calculate 25 + 15 for me")],
        agents=agents_dict,
        active_agents={"search_agent", "math_agent"},
    )

    try:
        result = await supervisor.arun(initial_state.model_dump())

        if result.get("agent_response"):
            pass
        if result.get("next_agent"):
            pass

    except Exception as e:
        import traceback

        traceback.print_exc()

    # Test with search task

    search_state = SupervisorStateWithTools(
        messages=[HumanMessage(content="Search for information about Python")],
        agents=agents_dict,
        active_agents={"search_agent", "math_agent"},
    )

    try:
        result = await supervisor.arun(search_state.model_dump())

        if result.get("next_agent"):
            pass

    except Exception as e:
        pass")


if __name__ == "__main__":
    asyncio.run(test_supervisor_agent())
