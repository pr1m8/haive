"""Grade_Generation_V_Documents_And_Question core module.

This module provides grade generation v documents and question functionality for the Haive framework.

Functions:
    grade_generation_v_documents_and_question: Grade Generation V Documents And Question functionality.
"""

from typing import Any


def grade_generation_v_documents_and_question(state: dict[str, Any]):
    """Determines whether the generation is grounded in the document and answers question.

    Args:
        state (dict): The current graph state

    Returns:
        str: Decision for next node to call
    """
    question = state["question"]
    documents = state["documents"]
    generation = state["generation"]

    score = hallucination_grader.invoke(
        {"documents": documents, "generation": generation}
    )
    grade = score.binary_score

    # Check hallucination
    if grade == "yes":
        # Check question-answering
        score = answer_grader.invoke({"question": question, "generation": generation})
        grade = score.binary_score
        if grade == "yes":
            return "useful"
        return "not useful"
    pprint("---DECISION: GENERATION IS NOT GROUNDED IN DOCUMENTS, RE-TRY---")
    return "not supported"
