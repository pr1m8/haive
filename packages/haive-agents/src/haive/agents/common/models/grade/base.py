"""Base classes for grade models.

This module defines the fundamental abstractions for all grading models
including the grade type enumeration and abstract base class.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class GradeType(str, Enum):
    """Types of grade models available.

    Attributes:
        BINARY: Simple pass/fail or yes/no grading
        NUMERIC: Numeric scoring with configurable ranges
        PERCENTAGE: Percentage-based scoring (0-100%)
        LETTER: Traditional letter-based grading (A-F)
        RUBRIC: Multi-criteria rubric-based evaluation
        QUALITATIVE: Text-based qualitative assessment
        SCALE: Likert-scale or custom scale grading
        COMPOSITE: Combination of multiple grade types
    """

    BINARY = "binary"
    NUMERIC = "numeric"
    PERCENTAGE = "percentage"
    LETTER = "letter"
    RUBRIC = "rubric"
    QUALITATIVE = "qualitative"
    SCALE = "scale"
    COMPOSITE = "composite"


class Grade(BaseModel, ABC):
    """Abstract base class for all grade models.

    This class provides the common interface and functionality that all
    grade models must implement. It includes metadata, validation,
    and utility methods.

    Attributes:
        grade_type: The type of grade model
        justification: Explanation for the grade assigned
        confidence: Confidence level in the grade (0.0 to 1.0)
        metadata: Additional metadata about the grading
        grader_id: Identifier of the grader (agent, human, etc.)
        timestamp: When the grade was assigned

    Example:
        ```python
        # This is an abstract class, use concrete implementations
        grade = BinaryGrade(
            value=True,
            justification="Response meets all criteria",
            confidence=0.95
        )
        ```
    """

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        use_enum_values=True,
        str_strip_whitespace=True,
    )

    grade_type: GradeType = Field(..., description="Type of grade model being used")

    justification: str = Field(
        ...,
        description="Explanation or reasoning for the grade assigned",
        min_length=1,
        max_length=2000,
        examples=[
            "Response directly answers the question with accurate information",
            "Code compiles and runs correctly with good style",
            "Essay demonstrates clear understanding but lacks supporting evidence",
        ],
    )

    confidence: float = Field(
        default=1.0,
        description="Confidence level in the grade assigned (0.0 to 1.0)",
        ge=0.0,
        le=1.0,
        examples=[0.85, 0.95, 1.0],
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata about the grading process",
        examples=[
            {"rubric_version": "2.1", "total_time_seconds": 45.2},
            {
                "model_used": "gpt-4",
                "criteria_weights": {"accuracy": 0.4, "clarity": 0.6},
            },
        ],
    )

    grader_id: str | None = Field(
        default=None,
        description="Identifier of the entity that assigned the grade",
        examples=["human_grader_001", "agent_evaluator_v2", "peer_review_bot"],
    )

    timestamp: datetime = Field(
        default_factory=datetime.now, description="When the grade was assigned"
    )

    @field_validator("justification")
    @classmethod
    def validate_justification(cls, v: str) -> str:
        """Validate that justification is meaningful.

        Args:
            v: The justification string to validate

        Returns:
            The validated justification string

        Raises:
            ValueError: If justification is empty, too short, or meaningless
        """
        if not v or v.strip() == "":
            raise ValueError("Justification cannot be empty")

        # Check for common meaningless responses
        meaningless_phrases = {
            "good",
            "bad",
            "ok",
            "fine",
            "no comment",
            "n/a",
            "na",
            "none",
            "idk",
            "dunno",
            "whatever",
            "because",
            "yes",
            "no",
        }

        if v.strip().lower() in meaningless_phrases:
            raise ValueError(
                f"Justification '{v}' is too vague. Please provide specific reasoning."
            )

        # Require minimum word count for meaningful justification
        word_count = len(v.split())
        if word_count < 3:
            raise ValueError("Justification must contain at least 3 words")

        return v.strip()

    @abstractmethod
    def get_normalized_score(self) -> float:
        """Get the grade as a normalized score between 0.0 and 1.0.

        This method must be implemented by all concrete grade classes
        to provide a common way to compare grades across different types.

        Returns:
            A float between 0.0 and 1.0 representing the normalized grade
        """

    @abstractmethod
    def is_passing(self, threshold: float | None = None) -> bool:
        """Determine if the grade represents a passing score.

        Args:
            threshold: Optional custom threshold for passing.
                      If None, uses grade type default.

        Returns:
            True if the grade is considered passing, False otherwise
        """

    def get_grade_summary(self) -> dict[str, Any]:
        """Get a summary of the grade information.

        Returns:
            Dictionary containing key grade information for display
        """
        return {
            "grade_type": self.grade_type.value,
            "normalized_score": self.get_normalized_score(),
            "is_passing": self.is_passing(),
            "confidence": self.confidence,
            "justification_preview": (
                self.justification[:100] + "..."
                if len(self.justification) > 100
                else self.justification
            ),
            "grader_id": self.grader_id,
            "timestamp": self.timestamp.isoformat(),
        }

    def compare_to(self, other: "Grade") -> dict[str, float | str]:
        """Compare this grade to another grade.

        Args:
            other: Another Grade instance to compare against

        Returns:
            Dictionary containing comparison information

        Raises:
            TypeError: If other is not a Grade instance
        """
        if not isinstance(other, Grade):
            raise TypeError("Can only compare with other Grade instances")

        self_score = self.get_normalized_score()
        other_score = other.get_normalized_score()

        return {
            "score_difference": self_score - other_score,
            "better_grade": (
                "self"
                if self_score > other_score
                else "other" if other_score > self_score else "tie"
            ),
            "confidence_difference": self.confidence - other.confidence,
            "same_type": self.grade_type == other.grade_type,
            "comparison_summary": self._generate_comparison_summary(other),
        }

    def _generate_comparison_summary(self, other: "Grade") -> str:
        """Generate a human-readable comparison summary.

        Args:
            other: Another Grade instance to compare against

        Returns:
            String summary of the comparison
        """
        self_score = self.get_normalized_score()
        other_score = other.get_normalized_score()
        diff = abs(self_score - other_score)

        if diff < 0.05:
            return "Grades are essentially equivalent"
        if self_score > other_score:
            return f"This grade is {diff:.1%} higher than the comparison grade"
        return f"This grade is {diff:.1%} lower than the comparison grade"

    def to_display_string(self) -> str:
        """Convert grade to a human-readable display string.

        Returns:
            Formatted string representation of the grade
        """
        return f"{self.grade_type.value.title()} Grade | Score: {self.get_normalized_score():.1%} | {self.justification[:50]}..."

    def validate_grade_value(self, value: Any) -> bool:
        """Validate that a grade value is appropriate for this grade type.

        This method should be overridden by concrete classes to provide
        type-specific validation.

        Args:
            value: The value to validate

        Returns:
            True if valid, False otherwise
        """
        return True  # Base implementation accepts any value
