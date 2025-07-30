"""Models model module.

This module provides models functionality for the Haive framework.

Classes:
    Reflection: Reflection implementation.
    AnswerQuestion: AnswerQuestion implementation.
    ReviseAnswer: ReviseAnswer implementation.
"""

from pydantic import BaseModel, Field


class Reflection(BaseModel):
    """Reflection on the answer."""

    missing: str = Field(description="Critique of what is missing.")
    superfluous: str = Field(description="Critique of what is superfluous")


from pydantic import BaseModel, Field


class AnswerQuestion(BaseModel):
    """Answer the question. Provide an answer, reflection, and follow up with search queries to improve the answer."""

    answer: str = Field(description="~250 word detailed answer to the question.")
    reflection: Reflection = Field(description="Your reflection on the initial answer.")
    search_queries: list[str] = Field(
        default_factory=list,  # ✅ Ensures search_queries is always present
        description="1-3 search queries for researching improvements to address the critique of your current answer.",
    )


class ReviseAnswer(AnswerQuestion):
    """Revise your original answer to your question. Provide an answer, reflection,.

    cite your reflection with references, and finally
    add search queries to improve the answer.
    """

    references: list[str] = Field(
        description="Citations motivating your updated answer."
    )
