"""Decide_To_Generate core module.

This module provides decide to generate functionality for the Haive framework.

Functions:
    decide_to_generate: Decide To Generate functionality.
"""

from typing import Any


def decide_to_generate(state: dict[str, Any]):
    """Determines whether to generate an answer, or re-generate a question.

    Args:
        state (dict): The current graph state

    Returns:
        str: Binary decision for next node to call
    """
    filtered_documents = state["documents"]

    if not filtered_documents:
        # All documents have been filtered check_relevance
        # We will re-generate a new query
        return "transform_query"
    # We have relevant documents, so generate answer
    return "generate"
