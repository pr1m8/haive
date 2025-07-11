import json
import uuid
from datetime import datetime
from typing import Any, Dict, Generic, List, Literal, Optional, TypeVar, Union

from langchain_core.messages import BaseMessage
from pydantic import BaseModel, Field, field_validator

# Generic type for candidate content
T = TypeVar("T")


class Candidate(BaseModel, Generic[T]):
    """Generic candidate that can hold any type of content."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    content: T  # Can be str, dict, BaseModel, BaseMessage, etc.
    metadata: dict[str, Any] = Field(default_factory=dict)
    depth: int = 0
    parent_id: str | None = None
    expansion_index: int = 0
    created_at: datetime = Field(default_factory=datetime.now)

    @field_validator("content", mode="before")
    @classmethod
    def validate_content(cls, v: Any) -> Any:
        """Convert various types to a consistent format."""
        # If it's already processed, return as-is
        if isinstance(v, str | dict | BaseModel):
            return v

        # Convert BaseMessage to dict representation
        if isinstance(v, BaseMessage):
            return {
                "type": v.__class__.__name__,
                "content": v.content,
                "additional_kwargs": v.additional_kwargs,
            }

        # Convert other objects to dict if possible
        if hasattr(v, "dict"):
            return v.dict()
        if hasattr(v, "__dict__"):
            return v.__dict__

        # Default: convert to string
        return str(v)

    def get_content_str(self) -> str:
        """Get string representation of content for prompts."""
        if isinstance(self.content, str):
            return self.content
        if isinstance(self.content, dict):
            return json.dumps(self.content, indent=2)
        if isinstance(self.content, BaseModel):
            return self.content.model_dump_json(indent=2)
        return str(self.content)

    def __str__(self) -> str:
        """String representation for use in prompts."""
        content_str = self.get_content_str()
        if len(content_str) > 100:
            content_str = content_str[:100] + "..."
        return f"[Candidate {self.id[:8]}... depth={self.depth}] {content_str}"


class ScoredCandidate(Candidate[T], Generic[T]):
    """A candidate that has been evaluated with a score."""

    score: float = Field(description="Evaluation score")
    feedback: str = Field(description="Evaluation feedback/reasoning")
    scoring_metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional scoring information"
    )

    @field_validator("score")
    @classmethod
    def validate_score(cls, v: float) -> float:
        """Ensure score is in valid range."""
        if not 0 <= v <= 1:
            raise ValueError("Score must be between 0 and 1")
        return v

    @classmethod
    def from_candidate(
        cls, candidate: Candidate[T], score: float, feedback: str, **kwargs
    ) -> "ScoredCandidate[T]":
        """Create a ScoredCandidate from a Candidate."""
        return cls(
            id=candidate.id,
            content=candidate.content,
            metadata=candidate.metadata,
            depth=candidate.depth,
            parent_id=candidate.parent_id,
            expansion_index=candidate.expansion_index,
            created_at=candidate.created_at,
            score=score,
            feedback=feedback,
            scoring_metadata=kwargs,
        )

    def __str__(self) -> str:
        """Enhanced string representation with score."""
        base_str = super().__str__()
        return f"{base_str} [Score: {self.score:.3f}]"


# Structured output models for agents
class CandidateGeneration(BaseModel):
    """Output from expansion agent."""

    candidates: list[dict[str, Any]] = Field(
        description="List of generated candidate solutions"
    )
    reasoning: str = Field(description="Overall reasoning for this expansion")
    strategy: Literal["explore", "exploit", "refine"] = Field(
        default="explore", description="Strategy used for generation"
    )


class CandidateEvaluation(BaseModel):
    """Output from scoring agent."""

    score: float = Field(ge=0, le=1)
    feedback: str
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)
    confidence: float = Field(default=0.8, ge=0, le=1)


class SearchControl(BaseModel):
    """Output from control/pruning agent."""

    selected_indices: list[int] = Field(description="Indices of candidates to keep")
    should_terminate: bool
    termination_reason: str | None = None
    next_strategy: Literal["explore", "exploit", "refine", "terminate"] = Field(
        default="explore"
    )
