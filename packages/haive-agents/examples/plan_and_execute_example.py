"""Example of using the Plan and Execute Agent.

This example demonstrates how to use the PlanAndExecuteAgent to:
1. Create a plan for a complex task
2. Execute steps with tool access
3. Handle replanning when needed
"""

import asyncio
import logging

from haive.core.llm import AugLLMConfig
from haive.tools.tools.search_tools import tavily_search

from haive.agents.planning.plan_and_execute import (
    PlanAndExecuteAgent,
    create_plan_and_execute_agent,
)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    """Run a Plan and Execute agent example."""

    # Create configurations for each agent
    planner_config = AugLLMConfig(
        model="gpt-4", temperature=0.7, system_message="You are a strategic planner."
    )

    executor_config = AugLLMConfig(
        model="gpt-4",
        temperature=0.3,  # Lower temperature for execution
        system_message="You are a precise executor.",
    )

    replanner_config = AugLLMConfig(
        model="gpt-4", temperature=0.5, system_message="You are a thoughtful replanner."
    )

    # Create the Plan and Execute agent
    agent = create_plan_and_execute_agent(
        planner_config=planner_config,
        executor_config=executor_config,
        replanner_config=replanner_config,
        executor_tools=[tavily_search],  # Executor has access to search
        max_replanning_attempts=2,
        name="Research Assistant",
    )

    # Example task: Research and summarize a topic
    task = """
    Research the latest developments in quantum computing and create a comprehensive summary.
    Include information about recent breakthroughs, key players, and potential applications.
    """

    logger.info("Starting Plan and Execute workflow...")

    try:
        # Run the agent
        result = await agent.arun(task)

        logger.info("Task completed!")
        logger.info(f"Final result: {result}")

    except Exception as e:
        logger.error(f"Error during execution: {e}")
        raise


async def advanced_example():
    """Advanced example with custom agent configuration."""

    # Create a Plan and Execute agent using the class directly
    agent = PlanAndExecuteAgent(
        planner_config=AugLLMConfig(model="gpt-4", temperature=0.7),
        executor_config=AugLLMConfig(
            model="gpt-4",
            temperature=0.3,
            tools=[tavily_search],  # Tools can be set here too
        ),
        replanner_config=AugLLMConfig(model="gpt-4", temperature=0.5),
        executor_tools=[tavily_search],
        max_replanning_attempts=3,
        name="Advanced Research Assistant",
    )

    # Complex multi-step task
    complex_task = """
    Analyze the impact of artificial intelligence on the job market:
    1. Research current AI adoption rates across industries
    2. Identify jobs most at risk of automation
    3. Find emerging job categories created by AI
    4. Analyze geographical differences in AI impact
    5. Provide recommendations for workforce adaptation
    """

    logger.info("Starting advanced Plan and Execute workflow...")

    # Run with streaming to see progress
    async for chunk in agent.astream(complex_task):
        if chunk:
            logger.info(f"Progress update: {chunk}")

    logger.info("Advanced task completed!")


async def minimal_example():
    """Minimal example without replanner."""

    # Create without replanner for simpler workflows
    agent = PlanAndExecuteAgent(
        planner_config=AugLLMConfig(model="gpt-4"),
        executor_config=AugLLMConfig(model="gpt-4"),
        # No replanner_config - will execute plan to completion
        executor_tools=[tavily_search],
    )

    simple_task = "Find and summarize the latest news about renewable energy."

    result = await agent.arun(simple_task)
    logger.info(f"Simple task result: {result}")


if __name__ == "__main__":
    # Run the main example
    asyncio.run(main())

    # Uncomment to run other examples:
    # asyncio.run(advanced_example())
    # asyncio.run(minimal_example())
