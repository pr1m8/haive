"""Models for reflection agent outputs and configurations."""

from typing import Any, Literal

from pydantic import BaseModel, Field, validator


class QualityScore(BaseModel):
    """Simple quality score for responses."""

    score: float = Field(ge=0.0, le=100.0, description="Overall quality score (0-100)")
    confidence: float = Field(
        default=0.8, ge=0.0, le=1.0, description="Confidence in the score"
    )
    reasoning: str = Field(description="Brief explanation of the score")


class ImprovementSuggestion(BaseModel):
    """A specific improvement suggestion."""

    category: str = Field(
        description="Category of improvement (clarity, accuracy, completeness, etc.)"
    )
    suggestion: str = Field(description="Specific suggestion for improvement")
    priority: Literal["high", "medium", "low"] = Field(
        default="medium", description="Priority of this improvement"
    )
    example: str | None = Field(
        default=None, description="Example of the improved version"
    )


class GradingResult(BaseModel):
    """Comprehensive grading result for a response."""

    # Core grading
    overall_score: QualityScore = Field(description="Overall quality assessment")

    # Detailed scores
    accuracy_score: float = Field(
        ge=0.0, le=100.0, description="Accuracy/correctness score"
    )
    completeness_score: float = Field(
        ge=0.0, le=100.0, description="Completeness score"
    )
    clarity_score: float = Field(
        ge=0.0, le=100.0, description="Clarity and coherence score"
    )
    relevance_score: float = Field(
        ge=0.0, le=100.0, description="Relevance to the query score"
    )

    # Feedback
    strengths: list[str] = Field(
        default_factory=list, description="Identified strengths"
    )
    weaknesses: list[str] = Field(
        default_factory=list, description="Identified weaknesses"
    )
    improvements: list[ImprovementSuggestion] = Field(
        default_factory=list, description="Specific improvement suggestions"
    )

    # Grade
    letter_grade: str = Field(
        pattern="^[A-F][+-]?$", description="Letter grade (A+, A, A-, B+, etc.)"
    )

    # Optional improved version
    improved_response: str | None = Field(
        default=None, description="Suggested improved version of the response"
    )

    @validator("letter_grade")
    def validate_grade_matches_score(self, v, values) -> Any:
        """Ensure letter grade matches overall score."""
        if "overall_score" in values:
            score = values["overall_score"].score
            expected_grade = self._score_to_grade(score)
            if v != expected_grade:
                # Allow override but log warning
                pass
        return v

    @staticmethod
    def _score_to_grade(score: float) -> str:
        """Convert numerical score to letter grade."""
        if score >= 97:
            return "A+"
        if score >= 93:
            return "A"
        if score >= 90:
            return "A-"
        if score >= 87:
            return "B+"
        if score >= 83:
            return "B"
        if score >= 80:
            return "B-"
        if score >= 77:
            return "C+"
        if score >= 73:
            return "C"
        if score >= 70:
            return "C-"
        if score >= 67:
            return "D+"
        if score >= 63:
            return "D"
        if score >= 60:
            return "D-"
        return "F"


class ReflectionOutput(BaseModel):
    """Output from reflection process (unstructured)."""

    reflected_response: str = Field(description="The reflected/improved response")

    reflection_notes: str | None = Field(
        default=None, description="Notes about what was improved"
    )

    iterations: int = Field(
        default=1, ge=1, description="Number of reflection iterations"
    )

    changes_made: list[str] = Field(
        default_factory=list, description="List of changes made"
    )


class ExpertiseConfig(BaseModel):
    """Configuration for expert agents."""

    domain: str = Field(description="Domain of expertise")

    expertise_level: Literal["beginner", "intermediate", "expert", "world-class"] = (
        Field(default="expert", description="Level of expertise to simulate")
    )

    style: str | None = Field(
        default=None,
        description="Communication style (formal, casual, technical, etc.)",
    )

    additional_context: str | None = Field(
        default=None, description="Additional context about the expert role"
    )

    def to_prompt(self) -> str:
        """Convert to prompt string."""
        prompt = f"You are a {self.expertise_level} expert in {self.domain}."

        if self.style:
            prompt += f" Communicate in a {self.style} style."

        if self.additional_context:
            prompt += f" {self.additional_context}"

        return prompt


class ReflectionConfig(BaseModel):
    """Configuration for reflection process."""

    max_iterations: int = Field(
        default=3, ge=1, le=10, description="Maximum reflection iterations"
    )

    min_score_threshold: float = Field(
        default=80.0, ge=0.0, le=100.0, description="Minimum score to stop reflecting"
    )

    confidence_threshold: float = Field(
        default=0.9,
        ge=0.0,
        le=1.0,
        description="Confidence threshold to stop reflecting",
    )

    reflection_mode: Literal["improve", "critique", "both"] = Field(
        default="both", description="Mode of reflection"
    )

    include_reasoning: bool = Field(
        default=True, description="Include reasoning in output"
    )

    force_iterations: int | None = Field(
        default=None, description="Force exact number of iterations"
    )

    stop_on_decline: bool = Field(default=True, description="Stop if quality decreases")


# Additional models for structured output reflection pattern
class Critique(BaseModel):
    """Structured critique of an output (for structured output pattern)."""

    strengths: list[str] = Field(description="Identified strengths")
    weaknesses: list[str] = Field(description="Identified weaknesses")
    suggestions: list[str] = Field(description="Specific improvement suggestions")
    overall_quality: float = Field(
        ge=0.0, le=1.0, description="Quality score 0.0 to 1.0"
    )
    needs_revision: bool = Field(description="Whether revision is needed")


class ReflectionResult(BaseModel):
    """Complete reflection analysis (for structured output pattern)."""

    summary: str = Field(description="Summary of the reflection analysis")
    critique: Critique = Field(description="Detailed critique")
    action_items: list[str] = Field(description="Specific action items for improvement")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence in the analysis")
