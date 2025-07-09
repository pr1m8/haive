from typing import Any

from pydantic import BaseModel, Field


class Candidate(BaseModel):
    """A candidate solution in the Tree of Thoughts algorithm."""

    content: str = Field(description="The candidate solution content")
    score: float | None = Field(
        default=None, description="Score assigned to this candidate"
    )
    feedback: str | None = Field(default=None, description="Feedback on this candidate")
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata"
    )

    def __str__(self) -> str:
        """String representation of the candidate."""
        if self.content and len(self.content) > 50:
            preview = self.content[:47] + "..."
        else:
            preview = self.content
        return f"Candidate(content='{preview}', score={self.score})"


class CandidateContent(BaseModel):
    """A potential solution to the problem."""

    content: str = Field(description="The complete reasoning and solution approach")


class CandidateList(BaseModel):
    """A list of candidate solutions."""

    candidates: list[CandidateContent] = Field(
        description="List of different candidate solutions to the problem"
    )
    reasoning: str | None = Field(
        default=None,
        description="Reasoning about different approaches to solving the problem",
    )


class CandidateScore(BaseModel):
    """Score and feedback for a candidate solution."""

    score: float = Field(
        description="Numerical score between 0.0 and 1.0, where 1.0 is perfect"
    )
    feedback: str = Field(
        description="Detailed feedback explaining the score and reasoning"
    )
