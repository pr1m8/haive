"""Generate core module.

This module provides generate functionality for the Haive framework.

Functions:
    generate: Generate functionality.
"""

from typing import Any


def generate(state: dict[str, Any]):
    """Generate answer.

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, generation, that contains LLM generation
    """
    question = state["question"]
    documents = state["documents"]

    # RAG generation
    generation = rag_chain.invoke({"context": documents, "question": question})
    return {"documents": documents, "question": question, "generation": generation}
