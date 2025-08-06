"""Retrieve core module.

This module provides retrieve functionality for the Haive framework.

Functions:
    retrieve: Retrieve functionality.
"""

from __future__ import annotations

from typing import Any


def retrieve(state: dict[str, Any]):
    """Retrieve documents.

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, documents, that contains retrieved documents
    """
    question = state["question"]

    # Retrieval
    documents = retriever.invoke(question)
    return {"documents": documents, "question": question}
