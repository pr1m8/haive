"""Branches core module.

This module provides branches functionality for the Haive framework.

Classes:
    ToTBranch: ToTBranch implementation.
    for: for implementation.

Functions:
    evaluate: Evaluate functionality.
"""

from typing import Any

from haive.core.graph.branches import Branch
from langchain_core.messages import AIMessage
from langgraph.graph import END
from langgraph.types import Command, Send


class ToTBranch(Branch):
    """Branch class for Tree of Thoughts routing logic.

    Handles the logic of deciding whether to continue exploration or
    terminate the search and return the best solution found.
    """

    def __init__(self, agent: Any):
        """Initialize with reference to parent agent for config access."""
        self.agent = agent

    def evaluate(self, state: dict[str, Any]) -> str | tuple | list[Send] | Command:
        """Evaluate the current state and determine the next steps."""
        # Check termination conditions
        if hasattr(state, "depth") and hasattr(state, "max_depth"):
            max_depth_reached = state.depth >= state.max_depth
        else:
            max_depth_reached = state.get("depth", 0) >= state.get("max_depth", 3)

        # Get candidates
        if hasattr(state, "candidates"):
            candidates = state.candidates
        else:
            candidates = state.get("candidates", [])

        # Get best candidate
        best_candidate = None
        if candidates:
            best_candidate = candidates[0]
        elif hasattr(state, "best_candidate") and state.best_candidate:
            best_candidate = state.best_candidate
        else:
            best_candidate = state.get("best_candidate")

        if not best_candidate:
            return END

        # Check threshold
        threshold_reached = False
        score = None
        content = ""

        # Handle different types of candidate objects
        if isinstance(best_candidate, dict):
            score = best_candidate.get("score")
            content = best_candidate.get("content", "")
            threshold_reached = (
                score is not None and score >= self.agent.config.threshold
            )
        else:
            # Assume it's a Candidate object with attributes
            score = getattr(best_candidate, "score", None)
            content = getattr(best_candidate, "content", "")
            threshold_reached = (
                score is not None and score >= self.agent.config.threshold
            )

        # If we should terminate
        if max_depth_reached or threshold_reached:
            # Create message text safely
            message_text = "I've found a solution"
            if score is not None:
                message_text += f" with confidence {score}"
            message_text += f":\n\n{content}"

            # Create a final message with the solution
            final_message = AIMessage(content=message_text)

            # Return END with the final state updates, setting answer explicitly
            return END, {
                "messages": [*state.messages, final_message],
                "answef": content,  # Make sure this is set explicitly
            }

        # Continue with best candidate as seed
        return self.agent.config.expand_node_name, {"current_seed": best_candidate}

        # Continue with best candidate as seed
        return self.agent.config.expand_node_name, {"current_seed": candidates[0]}
