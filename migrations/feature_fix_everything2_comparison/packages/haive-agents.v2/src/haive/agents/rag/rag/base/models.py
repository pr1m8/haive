"""Models model module.

This module provides models functionality for the Haive framework.

Classes:
    Query: Query implementation.
    GradeHallucinations: GradeHallucinations implementation.
    GradeAnswer: GradeAnswer implementation.
"""

from pydantic import BaseModel, Field


class Query(BaseModel):
    question: str = Field(
        ..., description="The question to search the RAG database with."
    )


# Data model
class GradeHallucinations(BaseModel):
    """Binary score for hallucination present in generation answer."""

    binary_score: str = Field(
        description="Answer is grounded in the facts, 'yes' or 'no'"
    )


# Data model
class GradeAnswer(BaseModel):
    """Binary score to assess answer addresses question."""

    binary_score: str = Field(
        description="Answer addresses the question, 'yes' or 'no'"
    )
