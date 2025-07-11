"""Test the simplified Plan and Execute Agent implementation."""

import asyncio
import os
from datetime import datetime

from haive.agents.planning import PlanAndExecuteAgent
from haive.agents.planning.p_and_e.models import Act
from haive.agents.react import ReactAgent
from haive.agents.simple import SimpleAgent


async def main():
    """Run the Plan and Execute agent example with debug output."""
    # Create the individual agents

    # Mock engine for testing
    class MockEngine:
        def __init__(self, name):
            self.name = name
            self.tools = []
            self.tool_routes = {}

        def model_copy(self):
            return MockEngine(self.name)

    engine = MockEngine("test_engine")

    # Create agents
    planner = SimpleAgent(
        name="planner",
        engine=engine,
        instructions="Create a plan to accomplish: {objective}",
        output_schema=Act,
        output_schema_strict=True,
    )

    executor = ReactAgent(
        name="executor",
        engine=engine,
        instructions="Execute this step: {current_step}",
    )

    replanner = SimpleAgent(
        name="replanner",
        engine=engine,
        instructions="Assess progress and decide next action",
        output_schema=Act,
        output_schema_strict=True,
    )

    # Create the Plan and Execute agent
    agent = PlanAndExecuteAgent(
        planner=planner,
        executor=executor,
        replanner=replanner,
        tools=[],  # No tools for now
        name="research_assistant",
    )

    # Test query
    query = "What are 3 key benefits of renewable energy?"

    start_time = datetime.now()

    try:
        # Run the agent with debug=True
        await agent.arun(query, debug=True)

        # Display results

        # Show execution time
        (datetime.now() - start_time).total_seconds()

    except Exception:
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
