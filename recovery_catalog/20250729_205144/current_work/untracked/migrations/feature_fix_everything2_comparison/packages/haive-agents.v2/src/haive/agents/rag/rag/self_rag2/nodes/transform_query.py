"""Transform_Query core module.

This module provides transform query functionality for the Haive framework.

Functions:
    transform_query: Transform Query functionality.
"""

from typing import Any


def transform_query(state: dict[str, Any]):
    """Transform the query to produce a better question.

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Updates question key with a re-phrased question
    """
    question = state["question"]
    documents = state["documents"]

    # Re-write question
    better_question = question_rewriter.invoke({"question": question})
    return {"documents": documents, "question": better_question}
