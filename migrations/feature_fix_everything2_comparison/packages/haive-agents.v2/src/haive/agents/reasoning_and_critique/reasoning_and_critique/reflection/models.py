"""Models for the Reflection Agent."""

from typing import Any

from pydantic import BaseModel, Field


class ReflectionResult(BaseModel):
    """Model for structured reflection output."""

    reflection: str = Field(description="Detailed critique of the response")
    missing: str = Field(description="Analysis of what is missing in the response")
    superfluous: str = Field(
        description="Analysis of what is superfluous in the response"
    )
    score: int = Field(
        description="Score from 0-10 on the quality of the response", ge=0, le=10
    )
    found_solution: bool = Field(
        description="Whether this response fully solves the problem"
    )

    @property
    def normalized_score(self) -> float:
        """Return the score normalized to 0-1."""
        return self.score / 10.0

    def as_message(self) -> dict[str, Any]:
        """Convert to a message format."""
        return {
            "content": f"Reflection: {self.reflection}\nMissing: {self.missing}\nSuperfluous: {self.superfluous}\nScore: {self.score}\nFound solution: {self.found_solution}"
        }


class SearchQuery(BaseModel):
    """Model for a search query."""

    query: str = Field(description="Search query text")

    def __str__(self) -> str:
        return self.query


class ReflectionOutput(BaseModel):
    """Model for the output of the reflection step."""

    answer: str = Field(description="The improved answer based on reflection")
    reflection: ReflectionResult = Field(
        description="The reflection on the original answer"
    )
    search_queries: list[str] = Field(
        default_factory=list,
        description="Potential search queries for improving the answer",
    )
