"""Scale grading model for Likert-style evaluations.

This module implements scale-based grading systems including Likert scales,
satisfaction ratings, and custom ordinal scales.
"""

from enum import Enum
from typing import Any

from pydantic import Field, field_validator, model_validator

from haive.agents.common.models.grade.base import Grade, GradeType


class LikertScale(str, Enum):
    """Standard 5-point Likert scale values.

    Attributes:
        STRONGLY_DISAGREE: Strongly disagree (1)
        DISAGREE: Disagree (2)
        NEUTRAL: Neither agree nor disagree (3)
        AGREE: Agree (4)
        STRONGLY_AGREE: Strongly agree (5)
    """

    STRONGLY_DISAGREE = "strongly_disagree"
    DISAGREE = "disagree"
    NEUTRAL = "neutral"
    AGREE = "agree"
    STRONGLY_AGREE = "strongly_agree"


class SatisfactionScale(str, Enum):
    """Standard satisfaction rating scale.

    Attributes:
        VERY_DISSATISFIED: Very dissatisfied (1)
        DISSATISFIED: Dissatisfied (2)
        NEUTRAL: Neutral (3)
        SATISFIED: Satisfied (4)
        VERY_SATISFIED: Very satisfied (5)
    """

    VERY_DISSATISFIED = "very_dissatisfied"
    DISSATISFIED = "dissatisfied"
    NEUTRAL = "neutral"
    SATISFIED = "satisfied"
    VERY_SATISFIED = "very_satisfied"


class ScaleGrade(Grade):
    """Scale grading model for Likert-style evaluations.

    This grade model represents ordinal scale ratings such as Likert scales,
    satisfaction ratings, or custom scales with labeled points.

    Attributes:
        scale_value: The selected scale value
        scale_labels: List of scale labels in order from lowest to highest
        scale_type: Optional scale type identifier
        numeric_value: Numeric equivalent of the scale position

    Example:
        ```python
        # Using predefined Likert scale
        grade = ScaleGrade(
            scale_value="agree",
            scale_labels=["strongly_disagree", "disagree", "neutral", "agree", "strongly_agree"],
            scale_type="likert_5",
            justification="Response shows good understanding with minor reservations"
        )

        # Custom satisfaction scale
        grade = ScaleGrade(
            scale_value="satisfied",
            scale_labels=["very_dissatisfied", "dissatisfied", "neutral", "satisfied", "very_satisfied"],
            scale_type="satisfaction",
            justification="User feedback indicates satisfaction with minor issues"
        )

        # Custom numeric scale with labels
        grade = ScaleGrade(
            scale_value="good",
            scale_labels=["poor", "fair", "good", "very_good", "excellent"],
            scale_type="quality_5",
            justification="Quality meets expectations"
        )
        ```
    """

    grade_type: GradeType = Field(
        default=GradeType.SCALE, description="Type of grade model (always scale)"
    )

    scale_value: str = Field(
        ...,
        description="The selected value from the scale",
        examples=["agree", "satisfied", "good", "4", "neutral"],
    )

    scale_labels: list[str] = Field(
        ...,
        description="Ordered list of scale labels from lowest to highest",
        min_length=2,
        max_length=10,
        examples=[
            ["poor", "fair", "good", "excellent"],
            ["strongly_disagree", "disagree", "neutral", "agree", "strongly_agree"],
            ["1", "2", "3", "4", "5"],
        ],
    )

    scale_type: str | None = Field(
        default=None,
        description="Optional identifier for the type of scale used",
        examples=["likert_5", "satisfaction", "quality", "numeric_7", "custom"],
    )

    numeric_value: int | None = Field(
        default=None,
        description="Numeric equivalent based on position in scale (1-indexed)",
    )

    @field_validator("scale_labels")
    @classmethod
    def validate_scale_labels_unique(cls, v: list[str]) -> list[str]:
        """Validate that all scale labels are unique.

        Args:
            v: List of scale labels to validate

        Returns:
            Validated scale labels list

        Raises:
            ValueError: If scale labels are not unique
        """
        normalized_labels = [label.strip().lower() for label in v]
        if len(normalized_labels) != len(set(normalized_labels)):
            raise ValueError("All scale labels must be unique")
        return [label.strip() for label in v]

    @model_validator(mode="after")
    def validate_scale_value_and_set_numeric(self) -> "ScaleGrade":
        """Validate scale_value is in scale_labels and set numeric_value.

        Returns:
            Self with numeric_value set

        Raises:
            ValueError: If scale_value is not in scale_labels
        """
        # Normalize for comparison
        scale_value_normalized = self.scale_value.strip().lower()
        labels_normalized = [label.strip().lower() for label in self.scale_labels]

        if scale_value_normalized not in labels_normalized:
            raise ValueError(
                f"scale_value '{self.scale_value}' must be one of: {self.scale_labels}"
            )

        # Set numeric value based on position (1-indexed)
        position = labels_normalized.index(scale_value_normalized)
        self.numeric_value = position + 1

        return self

    def get_normalized_score(self) -> float:
        """Get the grade as a normalized score between 0.0 and 1.0.

        Based on position within the scale range.

        Returns:
            Normalized score (position - 1) / (max_position - 1)
        """
        if len(self.scale_labels) == 1:
            return 1.0

        max_position = len(self.scale_labels)
        position = self.numeric_value or 1

        return (position - 1) / (max_position - 1)

    def get_scale_position(self) -> int:
        """Get the 1-indexed position of the value in the scale.

        Returns:
            Position of the selected value (1 = lowest, max = highest)
        """
        return self.numeric_value or 1

    def get_scale_percentage(self) -> float:
        """Get the scale position as a percentage.

        Returns:
            Percentage representing position in scale (0-100)
        """
        return self.get_normalized_score() * 100

    def is_passing(self, threshold: float | None = None) -> bool:
        """Determine if the scale grade represents a passing score.

        Args:
            threshold: Custom threshold (0.0 to 1.0). If None, uses
                      the middle point of the scale as threshold

        Returns:
            True if the scale position meets or exceeds the threshold
        """
        if threshold is None:
            # Use middle of scale as default threshold
            middle_position = (len(self.scale_labels) + 1) / 2
            threshold = (middle_position - 1) / (len(self.scale_labels) - 1)

        return self.get_normalized_score() >= threshold

    def is_top_tier(self, top_percent: float = 0.3) -> bool:
        """Check if the grade is in the top tier of the scale.

        Args:
            top_percent: What percentage of the scale constitutes "top tier"

        Returns:
            True if the grade is in the top tier
        """
        return self.get_normalized_score() >= (1.0 - top_percent)

    def is_bottom_tier(self, bottom_percent: float = 0.3) -> bool:
        """Check if the grade is in the bottom tier of the scale.

        Args:
            bottom_percent: What percentage of the scale constitutes "bottom tier"

        Returns:
            True if the grade is in the bottom tier
        """
        return self.get_normalized_score() <= bottom_percent

    def distance_from_neutral(self) -> float:
        """Calculate distance from the neutral/middle point of the scale.

        Returns:
            Signed distance from neutral (negative = below, positive = above)
        """
        neutral_position = (len(self.scale_labels) + 1) / 2
        current_position = self.numeric_value or 1
        return current_position - neutral_position

    def get_descriptive_assessment(self) -> str:
        """Get a descriptive assessment based on scale position.

        Returns:
            Descriptive string based on position in scale
        """
        normalized = self.get_normalized_score()

        if normalized >= 0.8:
            return "Highly Positive"
        if normalized >= 0.6:
            return "Positive"
        if normalized >= 0.4:
            return "Neutral/Mixed"
        if normalized >= 0.2:
            return "Negative"
        return "Highly Negative"

    def get_adjacent_values(self) -> dict[str, str | None]:
        """Get the adjacent scale values (one above and one below).

        Returns:
            Dictionary with 'lower' and 'higher' adjacent values
        """
        current_index = (self.numeric_value or 1) - 1

        return {
            "lower": (
                self.scale_labels[current_index - 1] if current_index > 0 else None
            ),
            "higher": (
                self.scale_labels[current_index + 1]
                if current_index < len(self.scale_labels) - 1
                else None
            ),
        }

    def to_display_string(self) -> str:
        """Convert grade to a human-readable display string.

        Returns:
            Formatted string representation of the scale grade
        """
        position = self.get_scale_position()
        max_position = len(self.scale_labels)
        percentage = self.get_scale_percentage()
        assessment = self.get_descriptive_assessment()

        return f"📊 {self.scale_value} ({position}/{max_position} | {percentage:.0f}% | {assessment}) | {self.justification[:30]}..."

    def validate_grade_value(self, value: Any) -> bool:
        """Validate that a value exists in the scale labels.

        Args:
            value: The value to validate

        Returns:
            True if the value is in scale_labels, False otherwise
        """
        if not isinstance(value, str):
            return False

        value_normalized = value.strip().lower()
        labels_normalized = [label.strip().lower() for label in self.scale_labels]

        return value_normalized in labels_normalized

    @classmethod
    def create_likert_5(
        cls, value: str | LikertScale, justification: str, **kwargs
    ) -> "ScaleGrade":
        """Create a 5-point Likert scale grade.

        Args:
            value: Likert scale value
            justification: Explanation for the rating
            **kwargs: Additional parameters

        Returns:
            ScaleGrade configured as 5-point Likert scale
        """
        if isinstance(value, LikertScale):
            value = value.value

        return cls(
            scale_value=value,
            scale_labels=[
                "strongly_disagree",
                "disagree",
                "neutral",
                "agree",
                "strongly_agree",
            ],
            scale_type="likert_5",
            justification=justification,
            **kwargs,
        )

    @classmethod
    def create_satisfaction_5(
        cls, value: str | SatisfactionScale, justification: str, **kwargs
    ) -> "ScaleGrade":
        """Create a 5-point satisfaction scale grade.

        Args:
            value: Satisfaction scale value
            justification: Explanation for the rating
            **kwargs: Additional parameters

        Returns:
            ScaleGrade configured as 5-point satisfaction scale
        """
        if isinstance(value, SatisfactionScale):
            value = value.value

        return cls(
            scale_value=value,
            scale_labels=[
                "very_dissatisfied",
                "dissatisfied",
                "neutral",
                "satisfied",
                "very_satisfied",
            ],
            scale_type="satisfaction_5",
            justification=justification,
            **kwargs,
        )

    @classmethod
    def create_numeric_scale(
        cls,
        value: int,
        min_value: int = 1,
        max_value: int = 5,
        justification: str = "",
        **kwargs,
    ) -> "ScaleGrade":
        """Create a numeric scale grade.

        Args:
            value: Numeric value selected
            min_value: Minimum value of the scale
            max_value: Maximum value of the scale
            justification: Explanation for the rating
            **kwargs: Additional parameters

        Returns:
            ScaleGrade configured as numeric scale
        """
        if not min_value <= value <= max_value:
            raise ValueError(
                f"Value {value} must be between {min_value} and {max_value}"
            )

        labels = [str(i) for i in range(min_value, max_value + 1)]

        return cls(
            scale_value=str(value),
            scale_labels=labels,
            scale_type=f"numeric_{min_value}_{max_value}",
            justification=justification,
            **kwargs,
        )

    @classmethod
    def create_quality_scale(
        cls, value: str, justification: str, scale_size: int = 5, **kwargs
    ) -> "ScaleGrade":
        """Create a quality assessment scale grade.

        Args:
            value: Quality level selected
            justification: Explanation for the rating
            scale_size: Size of the quality scale (3, 4, or 5)
            **kwargs: Additional parameters

        Returns:
            ScaleGrade configured as quality scale
        """
        quality_scales = {
            3: ["poor", "fair", "excellent"],
            4: ["poor", "fair", "good", "excellent"],
            5: ["poor", "fair", "good", "very_good", "excellent"],
        }

        if scale_size not in quality_scales:
            raise ValueError("scale_size must be 3, 4, or 5")

        labels = quality_scales[scale_size]

        return cls(
            scale_value=value,
            scale_labels=labels,
            scale_type=f"quality_{scale_size}",
            justification=justification,
            **kwargs,
        )
