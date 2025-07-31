"""Example core module.

This module provides example functionality for the Haive framework.

Functions:
    setup_tavily_tool: Setup Tavily Tool functionality.
    run_mcts_agent_example: Run Mcts Agent Example functionality.
"""

# src/haive/agents/mcts/example.py

import logging
from typing import Any

from haive.core.models.llm.base import AzureLLMConfig
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper
from langchain_core.tools import BaseTool

from haive.agents.reasoning_and_critique.mcts.utils import (
    create_mcts_agent,
    extract_best_solution,
    print_tree_stats,
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def setup_tavily_tool() -> BaseTool:
    """Set up Tavily search tool."""
    search = TavilySearchAPIWrapper()
    return TavilySearchResults(api_wrapper=search, max_results=5)


def run_mcts_agent_example(
    question: str, tools: list[BaseTool] | None = None
) -> dict[str, Any]:
    """Run an example MCTS agent workflow with the given question.

    Args:
        question: User question to answer
        tools: Optional list of tools to use

    Returns:
        Result of the agent run
    """
    # Set up tools
    if tools is None:
        try:
            tools = [setup_tavily_tool()]
        except Exception as e:
            logger.warning(f"Failed to set up Tavily tool: {e}. Using no tools.")
            tools = []

    # Set up LLM config
    llm_config = AzureLLMConfig(model="gpt-4o", parameters={"temperature": 0.7})

    # Create the MCTS agent
    agent = create_mcts_agent(
        tools=tools,
        llm_config=llm_config,
        system_prompt="You are a helpful AI assistant.",
        max_rollouts=5,
        candidates_per_rollout=5,
        name="research_mcts_agent",
    )
    for step in agent.stream(question, debug=True):
        pass

    logger.info(f"Running MCTS agent on question: {question}")

    # Track progress
    step_count = 0
    results = None

    # Use stream to show progress
    for step in agent.stream(question, debug=True):
        step_count += 1
        results = step

        # Extract relevant step name
        step_name = next(iter(step.keys())) if isinstance(step, dict) else "unknown"

        # Get current tree height
        tree_height = 0
        if "nodes" in step[step_name]:
            tree_height = step[step_name]["nodes"].get_tree_height()

        logger.info(f"Step {step_count} ({step_name}): Tree height {tree_height}")

    # Get final result
    final_result = next(iter(results.values())) if results else None

    if final_result:
        # Print tree statistics
        print_tree_stats(final_result)

        # Extract and print best solution
        solution = extract_best_solution(final_result)
        if solution:
            logger.info(f"Found solution: {solution['found_solution']}")
            logger.info(f"Solution score: {solution['score']}/10")
            if solution["output"]:
                logger.info("Solution output:")

    return final_result


if __name__ == "__main__":
    # Example usage
    question = "Generate a table with the average size and weight, as well as the oldest recorded instance for each of the top 5 most common birds."
    result = run_mcts_agent_example(question)
