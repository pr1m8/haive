"""Example core module.

This module provides example functionality for the Haive framework.

Functions:
    print_state: Print State functionality.
    run_tot_example: Run Tot Example functionality.
    run_game24_example: Run Game24 Example functionality.
"""

# examples/tot_agent_example.py

import os
import sys
from typing import Any

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.tot.modular.factory import (
    create_game24_tot_agent,
    create_math_tot_agent,
    create_tot_agent,
)


def print_state(state: dict[str, Any], detailed: bool = False) -> None:
    """Print the current state in a readable format."""
    if state.get("messages"):
        for msg in state["messages"]:
            if hasattr(msg, "content"):
                getattr(msg, "type", "unknown")

    if state.get("answer"):
        pass
    if detailed and "candidates" in state and state["candidates"]:
        for _i, candidate in enumerate(state["candidates"]):
            if candidate.feedback:
                pass

    if detailed and "best_candidate" in state and state["best_candidate"]:
        best = state["best_candidate"]
        if best.feedback:
            pass


def run_tot_example():
    """Run a basic Tree of Thoughts agent example."""
    # Create the agent
    agent = create_tot_agent(
        name="reasoning_tot",
        max_depth=3,
        beam_size=2,
        candidates_per_expansion=2,
        system_prompt="You are an expert at solving complex reasoning problems step by step.",
    )

    # Simple problem for demonstration
    problem = "How can I calculate the probability of drawing exactly 2 aces from a standard deck of 52 cards if I draw 5 cards without replacement?"

    # Run the agent and stream results
    agent.run(problem, debug=True)


def run_game24_example():
    """Run a Game of 24 example using Tree of Thoughts."""
    # Create the Game of 24 agent
    agent = create_game24_tot_agent(name="game24_agent")

    # Game of 24 problem
    problem = "3 8 9 4"

    # Run the agent
    agent.run(problem)

    # Print the result


def run_math_example():
    """Run a math problem example using Tree of Thoughts."""
    # Create the math-specialized agent
    agent = create_math_tot_agent(name="math_agent")

    # Math problem
    problem = "Find the area of a circle that has the same perimeter as a square with an area of 64 square units."

    # Run the agent
    agent.run(problem)

    # Print the result


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run Tree of Thoughts agent examples")
    parser.add_argument(
        "--example",
        choices=["basic", "game24", "math"],
        default="basic",
        help="Which example to run",
    )

    args = parser.parse_args()

    if args.example == "basic":
        run_tot_example()
    elif args.example == "game24":
        run_game24_example()
    elif args.example == "math":
        run_math_example()
