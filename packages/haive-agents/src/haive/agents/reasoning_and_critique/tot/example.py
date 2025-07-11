"""Example demonstrating the use of the Tree of Thoughts agent.

This example shows how to instantiate and run the ToT agent
with different problem types.
"""

import asyncio
import logging

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig

from haive.agents.reasoning_and_critique.tot.agent import ToTAgent
from haive.agents.reasoning_and_critique.tot.config import TOTAgentConfig

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def run_basic_example():
    """Run a basic example of the ToT agent."""
    logger.info("=== Running Basic Example ===")

    # Create a standard ToT agent with default configuration
    agent = ToTAgent()

    # Define a problem to solve
    problem = "What is the most effective way to reduce carbon emissions?"

    # Run the agent
    result = await agent.run(problem)

    # Print the result
    logger.info(f"Problem: {problem}")
    logger.info(f"Answer: {result.get('answer', 'No answer found')}")
    logger.info(f"Search depth: {result.get('search_depth', 0)}")
    logger.info(f"Score: {result.get('score', 0)}")

    return result


async def run_math_example():
    """Run a math example with the ToT agent."""
    logger.info("=== Running Math Example ===")

    # Create a ToT agent optimized for equation problems
    config = TOTAgentConfig.create_for_problem_type(
        content_type="equation",
        max_depth=4,
        beam_width=3,
        expansion_count=5,
        threshold=0.95,
        engines={
            "generator": AugLLMConfig(
                name="math_generator",
                description="Generates mathematical solutions",
                llm_config=AzureLLMConfig(
                    model="gpt-4o", parameters={"temperature": 0.7}
                ),
            ),
            "evaluator": AugLLMConfig(
                name="math_evaluator",
                description="Evaluates mathematical solutions",
                llm_config=AzureLLMConfig(
                    model="gpt-4o", parameters={"temperature": 0.1}
                ),
            ),
        },
    )

    agent = ToTAgent(config)

    # Define a Game of 24 problem
    problem = "Use the numbers 4, 7, 8, and 9 exactly once with basic operations (+, -, *, /) to get 24."

    # Run the agent
    result = await agent.run(problem)

    # Print the result
    logger.info(f"Problem: {problem}")
    logger.info(f"Answer: {result.get('answer', 'No answer found')}")
    logger.info(f"Search depth: {result.get('search_depth', 0)}")
    logger.info(f"Score: {result.get('score', 0)}")

    return result


async def run_complex_reasoning_example():
    """Run a complex reasoning example with the ToT agent."""
    logger.info("=== Running Complex Reasoning Example ===")

    # Create a ToT agent with custom configuration
    config = TOTAgentConfig(
        max_depth=5,
        beam_width=4,
        expansion_count=6,
        threshold=0.9,
        parallel_evaluation=True,
        parallel_expansion=True,
        engines={
            "generator": AugLLMConfig(
                name="reasoning_generator",
                description="Generates solutions for complex reasoning problems",
                llm_config=AzureLLMConfig(
                    model="gpt-4o", parameters={"temperature": 0.8, "max_tokens": 2000}
                ),
            ),
            "evaluator": AugLLMConfig(
                name="reasoning_evaluator",
                description="Evaluates solutions for complex reasoning problems",
                llm_config=AzureLLMConfig(
                    model="gpt-4o", parameters={"temperature": 0.1, "max_tokens": 1000}
                ),
            ),
        },
    )

    agent = ToTAgent(config)

    # Define a complex reasoning problem
    problem = """
    You have 5 pirates of different ages: 20, 30, 40, 50, and 60 years old.
    They find 100 gold coins and need to decide how to distribute them.
    The pirates have a strict order of seniority, with the oldest being the captain.
    The captain proposes a distribution plan that all pirates vote on.
    If at least half of the pirates (including the captain) accept the plan, they keep the coins.
    If the majority rejects the plan, the captain is thrown overboard, and the process starts
    again with the next oldest pirate.

    Each pirate's priorities are:
    1. Stay alive
    2. Get as many coins as possible
    3. Throw others overboard if it doesn't affect their survival or coins

    What is the optimal distribution plan for the 60-year-old captain?
    """

    # Run the agent with extended depth
    result = await agent.run({"problem": problem, "max_depth": 6, "beam_width": 5})

    # Print the result
    logger.info("Problem: Complex Pirate Problem")
    logger.info(f"Answer: {result.get('answer', 'No answer found')}")
    logger.info(f"Search depth: {result.get('search_depth', 0)}")
    logger.info(f"Score: {result.get('score', 0)}")

    return result


async def main():
    """Run all examples."""
    await run_basic_example()
    await run_math_example()
    await run_complex_reasoning_example()


if __name__ == "__main__":
    # Run the examples
    asyncio.run(main())
