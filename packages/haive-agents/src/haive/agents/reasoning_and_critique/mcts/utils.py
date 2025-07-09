# src/haive/agents/mcts/utils.py

import logging
from typing import Any

from agents.mcts.agent import MCTSAgent
from agents.mcts.config import MCTSAgentConfig
from agents.mcts.models import Reflection
from haive.core.models.llm.base import AzureLLMConfig, LLMConfig
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import BaseTool

# Set up logging
logger = logging.getLogger(__name__)


def create_mcts_agent(
    tools: list[BaseTool] | None = None,
    llm_config: LLMConfig | None = None,
    system_prompt: str | None = None,
    max_rollouts: int = 5,
    candidates_per_rollout: int = 5,
    exploration_weight: float = 1.0,
    name: str | None = None,
    **kwargs,
) -> MCTSAgent:
    """Create a Monte Carlo Tree Search agent.

    Args:
        tools: List of tools available to the agent
        llm_config: Configuration for the LLM
        system_prompt: System prompt for the agent
        max_rollouts: Maximum depth of rollouts
        candidates_per_rollout: Number of candidates to generate per rollout
        exploration_weight: Exploration weight for UCB calculation
        name: Name for the agent
        **kwargs: Additional configuration parameters

    Returns:
        MCTSAgent instance
    """
    # Set defaults
    llm_config = llm_config or AzureLLMConfig(
        model="gpt-4o", parameters={"temperature": 0.7}
    )
    tools = tools or []
    system_prompt = system_prompt or "You are an AI assistant."
    name = name or "mcts_agent"

    # Create default prompt templates if not in kwargs
    if "initial_prompt_template" not in kwargs:
        initial_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("user", "{input}"),
                MessagesPlaceholder(variable_name="messages", optional=True),
            ]
        )
        kwargs["initial_prompt_template"] = initial_prompt

    if "expansion_prompt_template" not in kwargs:
        expansion_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("user", "{input}"),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )
        kwargs["expansion_prompt_template"] = expansion_prompt

    if "reflection_prompt_template" not in kwargs:
        reflection_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "Reflect and grade the assistant response to the user question below.",
                ),
                ("user", "{input}"),
                MessagesPlaceholder(variable_name="candidate"),
            ]
        )
        kwargs["reflection_prompt_template"] = reflection_prompt

    # Create agent config
    config = MCTSAgentConfig(
        name=name,
        llm_config=llm_config,
        tools=tools,
        system_prompt=system_prompt,
        max_rollouts=max_rollouts,
        candidates_per_rollout=candidates_per_rollout,
        exploration_weight=exploration_weight,
        **kwargs,
    )

    # Build and return the agent
    return config.build_agent()


def extract_best_solution(result: dict[str, Any]) -> dict[str, Any] | None:
    """Extract the best solution from an MCTS agent result.

    Args:
        result: Result from an MCTS agent run

    Returns:
        Dictionary with best solution data, or None if no solution found
    """
    if "nodes" not in result:
        return None

    nodes = result["nodes"]
    best_solution = nodes.get_best_solution()

    if not best_solution:
        return None

    # Extract solution information
    solution_messages = nodes.deserialize_messages(
        nodes.get_trajectory(best_solution.node_id, include_reflections=False)
    )

    reflection_data = best_solution.reflection
    reflection = Reflection(**reflection_data)

    return {
        "messages": solution_messages,
        "output": solution_messages[-1].content if solution_messages else None,
        "reflection": reflection,
        "score": reflection.score,
        "found_solution": reflection.found_solution,
        "tree_height": nodes.get_tree_height(),
        "node_count": len(nodes.nodes),
    }


def print_tree_stats(result: dict[str, Any]) -> None:
    """Print statistics about the MCTS search tree.

    Args:
        result: Result from an MCTS agent run
    """
    if "nodes" not in result:
        print("No search tree found in result")
        return

    nodes = result["nodes"]

    print("=== MCTS Tree Statistics ===")
    print(f"Total nodes: {len(nodes.nodes)}")
    print(f"Tree height: {nodes.get_tree_height()}")
    print(f"Steps taken: {result.get('current_step', 0)}")

    # Get best solution
    best_solution = nodes.get_best_solution()
    if best_solution:
        print(f"Best solution found: {best_solution.is_solved}")
        print(f"Best solution score: {best_solution.value:.2f}")
        print(f"Best solution visits: {best_solution.visits}")
    else:
        print("No solution found")
