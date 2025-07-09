"""Numeric grading models for score-based evaluations.

This module implements numeric grading systems including general numeric
scores and percentage-based grading.
"""

from typing import Any

from pydantic import Field, field_validator, model_validator

from haive.agents.common.models.grade.base import Grade, GradeType


class NumericGrade(Grade):
    """Numeric grading model for score-based evaluations.

    This grade model represents numeric scores within a configurable range,
    such as 0-10, 1-5, 0-100, etc.

    Attributes:
        value: The numeric score value
        min_value: Minimum possible score (default 0)
        max_value: Maximum possible score (default 10)
        passing_threshold: Minimum score considered passing (default 60% of range)

    Example:
        ```python
        # 0-10 scale
        grade = NumericGrade(
            value=8.5,
            min_value=0,
            max_value=10,
            justification="Strong performance with minor areas for improvement"
        )

        # 1-5 scale
        grade = NumericGrade(
            value=4,
            min_value=1,
            max_value=5,
            passing_threshold=3,
            justification="Above average quality"
        )

        # Custom range
        grade = NumericGrade(
            value=850,
            min_value=200,
            max_value=800,  # This will raise an error - value exceeds max
            justification="SAT score"
        )
        ```
    """

    grade_type: GradeType = Field(
        default=GradeType.NUMERIC, description="Type of grade model (always numeric)"
    )

    value: int | float = Field(
        ..., description="The numeric score value", examples=[8.5, 7, 92.3, 4.2]
    )

    min_value: int | float = Field(
        default=0,
        description="Minimum possible score in the range",
        examples=[0, 1, -10, 200],
    )

    max_value: int | float = Field(
        default=10,
        description="Maximum possible score in the range",
        examples=[10, 5, 100, 800],
    )

    passing_threshold: int | float | None = Field(
        default=None,
        description="Minimum score considered passing. If None, defaults to 60% of range",
        examples=[6, 3, 70, 500],
    )

    @model_validator(mode="after")
    def validate_score_range(self) -> "NumericGrade":
        """Validate that the score is within the specified range.

        Returns:
            Self if validation passes

        Raises:
            ValueError: If score is outside the valid range
        """
        if self.min_value >= self.max_value:
            raise ValueError(
                f"min_value ({self.min_value}) must be less than max_value ({self.max_value})"
            )

        if not (self.min_value <= self.value <= self.max_value):
            raise ValueError(
                f"Score {self.value} is outside valid range [{self.min_value}, {self.max_value}]"
            )

        # Validate passing threshold if provided
        if self.passing_threshold is not None:
            if not (self.min_value <= self.passing_threshold <= self.max_value):
                raise ValueError(
                    f"Passing threshold {self.passing_threshold} is outside valid range [{self.min_value}, {self.max_value}]"
                )

        return self

    def get_normalized_score(self) -> float:
        """Get the grade as a normalized score between 0.0 and 1.0.

        Returns:
            Normalized score calculated as (value - min) / (max - min)
        """
        score_range = self.max_value - self.min_value
        if score_range == 0:
            return 1.0

        return (self.value - self.min_value) / score_range

    def get_percentage_score(self) -> float:
        """Get the grade as a percentage (0-100).

        Returns:
            Percentage score (normalized score * 100)
        """
        return self.get_normalized_score() * 100

    def is_passing(self, threshold: float | None = None) -> bool:
        """Determine if the grade represents a passing score.

        Args:
            threshold: Custom threshold to use. If None, uses instance threshold
                      or 60% of range as default

        Returns:
            True if the score meets or exceeds the passing threshold
        """
        if threshold is not None:
            return self.value >= threshold

        if self.passing_threshold is not None:
            return self.value >= self.passing_threshold

        # Default to 60% of range
        default_threshold = self.min_value + (self.max_value - self.min_value) * 0.6
        return self.value >= default_threshold

    def get_letter_equivalent(self) -> str:
        """Get an approximate letter grade equivalent.

        Uses standard grading scale based on percentage:
        A: 90-100%, B: 80-89%, C: 70-79%, D: 60-69%, F: <60%

        Returns:
            Letter grade string (A, B, C, D, F)
        """
        percentage = self.get_percentage_score()

        if percentage >= 90:
            return "A"
        if percentage >= 80:
            return "B"
        if percentage >= 70:
            return "C"
        if percentage >= 60:
            return "D"
        return "F"

    def distance_from_threshold(self, threshold: float | None = None) -> float:
        """Calculate distance from passing threshold.

        Args:
            threshold: Custom threshold to use. If None, uses instance threshold

        Returns:
            Positive value if above threshold, negative if below
        """
        if threshold is not None:
            return self.value - threshold

        if self.passing_threshold is not None:
            return self.value - self.passing_threshold

        # Default to 60% of range
        default_threshold = self.min_value + (self.max_value - self.min_value) * 0.6
        return self.value - default_threshold

    def to_display_string(self) -> str:
        """Convert grade to a human-readable display string.

        Returns:
            Formatted string representation of the numeric grade
        """
        percentage = self.get_percentage_score()
        letter = self.get_letter_equivalent()
        passing_status = "✅" if self.is_passing() else "❌"

        return f"{passing_status} {self.value}/{self.max_value} ({percentage:.1f}% | {letter}) | {self.justification[:30]}..."

    def validate_grade_value(self, value: Any) -> bool:
        """Validate that a value is numeric and within range.

        Args:
            value: The value to validate

        Returns:
            True if the value is valid, False otherwise
        """
        try:
            numeric_value = float(value)
            return self.min_value <= numeric_value <= self.max_value
        except (ValueError, TypeError):
            return False


class PercentageGrade(NumericGrade):
    """Percentage-based grading model (0-100%).

    A specialized numeric grade that's always in the 0-100 range,
    representing percentage scores.

    Attributes:
        value: Percentage value (0-100)
        min_value: Always 0
        max_value: Always 100
        passing_threshold: Minimum percentage considered passing (default 60)

    Example:
        ```python
        grade = PercentageGrade(
            value=87.5,
            justification="Excellent work with minor formatting issues",
            passing_threshold=70
        )

        # Automatically validates range
        bad_grade = PercentageGrade(
            value=105,  # This will raise an error
            justification="Invalid percentage"
        )
        ```
    """

    grade_type: GradeType = Field(
        default=GradeType.PERCENTAGE,
        description="Type of grade model (always percentage)",
    )

    min_value: int | float = Field(
        default=0, description="Minimum percentage (always 0)"
    )

    max_value: int | float = Field(
        default=100, description="Maximum percentage (always 100)"
    )

    passing_threshold: int | float = Field(
        default=60,
        description="Minimum percentage considered passing (default 60%)",
        ge=0,
        le=100,
    )

    value: int | float = Field(
        ...,
        description="Percentage value (0-100)",
        ge=0,
        le=100,
        examples=[87.5, 92, 68.2, 45],
    )

    @field_validator("min_value")
    @classmethod
    def validate_min_value(cls, v: int | float) -> int | float:
        """Ensure min_value is always 0 for percentages.

        Args:
            v: The min_value to validate

        Returns:
            Always returns 0
        """
        if v != 0:
            raise ValueError("PercentageGrade min_value must be 0")
        return 0

    @field_validator("max_value")
    @classmethod
    def validate_max_value(cls, v: int | float) -> int | float:
        """Ensure max_value is always 100 for percentages.

        Args:
            v: The max_value to validate

        Returns:
            Always returns 100
        """
        if v != 100:
            raise ValueError("PercentageGrade max_value must be 100")
        return 100

    def get_normalized_score(self) -> float:
        """Get the grade as a normalized score between 0.0 and 1.0.

        For percentages, this is simply value / 100.

        Returns:
            Normalized score (percentage / 100)
        """
        return self.value / 100.0

    def get_percentage_score(self) -> float:
        """Get the grade as a percentage (0-100).

        For PercentageGrade, this is just the value itself.

        Returns:
            The percentage value
        """
        return float(self.value)

    def to_display_string(self) -> str:
        """Convert grade to a human-readable display string.

        Returns:
            Formatted string representation of the percentage grade
        """
        letter = self.get_letter_equivalent()
        passing_status = "✅" if self.is_passing() else "❌"

        return (
            f"{passing_status} {self.value}% ({letter}) | {self.justification[:40]}..."
        )
