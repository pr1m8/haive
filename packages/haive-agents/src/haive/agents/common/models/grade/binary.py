"""Binary grading model for pass/fail evaluations.

This module implements a binary grading system suitable for pass/fail,
yes/no, correct/incorrect, and similar binary evaluations.
"""

from typing import Any

from pydantic import Field, field_validator

from haive.agents.common.models.grade.base import Grade, GradeType


class BinaryGrade(Grade):
    """Binary grading model for pass/fail evaluations.

    This grade model represents simple binary outcomes such as pass/fail,
    yes/no, correct/incorrect, acceptable/unacceptable, etc.

    Attributes:
        value: The binary grade value (True for pass/yes, False for fail/no)
        grade_type: Always GradeType.BINARY

    Example:
        ```python
        # Passing grade
        grade = BinaryGrade(
            value=True,
            justification="Response correctly identifies all key concepts",
            confidence=0.95
        )

        # Failing grade
        grade = BinaryGrade(
            value=False,
            justification="Response contains factual errors and misses main points",
            confidence=0.88
        )

        # Using string values (automatically converted)
        grade = BinaryGrade(
            value="pass",  # Converted to True
            justification="Meets minimum requirements"
        )
        ```
    """

    grade_type: GradeType = Field(
        default=GradeType.BINARY, description="Type of grade model (always binary)"
    )

    value: bool = Field(
        ...,
        description="Binary grade value (True=pass/yes/correct, False=fail/no/incorrect)",
        examples=[True, False],
    )

    @field_validator("value", mode="before")
    @classmethod
    def convert_value_to_bool(cls, v: Any) -> bool:
        """Convert various representations to boolean.

        Accepts boolean values, strings, and numbers and converts them
        to appropriate boolean values for grading.

        Args:
            v: Value to convert to boolean

        Returns:
            Boolean representation of the value

        Raises:
            ValueError: If the value cannot be converted to a meaningful boolean
        """
        if isinstance(v, bool):
            return v

        if isinstance(v, str):
            # Normalize string
            v_lower = v.strip().lower()

            # Positive values
            if v_lower in {
                "true",
                "pass",
                "yes",
                "correct",
                "acceptable",
                "good",
                "ok",
                "1",
                "success",
                "valid",
            }:
                return True

            # Negative values
            if v_lower in {
                "false",
                "fail",
                "no",
                "incorrect",
                "unacceptable",
                "bad",
                "0",
                "failure",
                "invalid",
            }:
                return False

            raise ValueError(
                f"Cannot convert string '{v}' to binary grade. Use 'pass'/'fail', 'yes'/'no', etc."
            )

        if isinstance(v, int | float):
            # Convert numbers: 0 = False, non-zero = True
            return bool(v)

        raise ValueError(f"Cannot convert type {type(v)} to binary grade value")

    def get_normalized_score(self) -> float:
        """Get the grade as a normalized score between 0.0 and 1.0.

        Returns:
            1.0 for True (pass), 0.0 for False (fail)
        """
        return 1.0 if self.value else 0.0

    def is_passing(self, threshold: float | None = None) -> bool:
        """Determine if the grade represents a passing score.

        For binary grades, this simply returns the boolean value.
        The threshold parameter is ignored for binary grades.

        Args:
            threshold: Ignored for binary grades

        Returns:
            The boolean value of the grade
        """
        return self.value

    def get_display_value(self) -> str:
        """Get a human-readable display value.

        Returns:
            "Pass" for True, "Fail" for False
        """
        return "Pass" if self.value else "Fail"

    def get_emoji_representation(self) -> str:
        """Get an emoji representation of the grade.

        Returns:
            ✅ for pass, ❌ for fail
        """
        return "✅" if self.value else "❌"

    def validate_grade_value(self, value: Any) -> bool:
        """Validate that a value can be converted to binary.

        Args:
            value: The value to validate

        Returns:
            True if the value can be converted to boolean, False otherwise
        """
        try:
            self.convert_value_to_bool(value)
            return True
        except ValueError:
            return False

    def flip(self) -> "BinaryGrade":
        """Create a new BinaryGrade with the opposite value.

        Useful for creating inverse grades or testing scenarios.

        Returns:
            New BinaryGrade instance with flipped value
        """
        return BinaryGrade(
            value=not self.value,
            justification=f"Flipped grade: {self.justification}",
            confidence=self.confidence,
            metadata={**self.metadata, "original_value": self.value},
            grader_id=self.grader_id,
        )

    def to_display_string(self) -> str:
        """Convert grade to a human-readable display string.

        Returns:
            Formatted string representation of the binary grade
        """
        emoji = self.get_emoji_representation()
        display_value = self.get_display_value()
        confidence_pct = f"{self.confidence:.0%}"

        return f"{emoji} {display_value} ({confidence_pct} confidence) | {self.justification[:50]}..."

    @classmethod
    def create_pass(
        cls, justification: str, confidence: float = 1.0, **kwargs
    ) -> "BinaryGrade":
        """Convenience method to create a passing grade.

        Args:
            justification: Explanation for the passing grade
            confidence: Confidence level (default 1.0)
            **kwargs: Additional parameters for the grade

        Returns:
            BinaryGrade instance with value=True
        """
        return cls(
            value=True, justification=justification, confidence=confidence, **kwargs
        )

    @classmethod
    def create_fail(
        cls, justification: str, confidence: float = 1.0, **kwargs
    ) -> "BinaryGrade":
        """Convenience method to create a failing grade.

        Args:
            justification: Explanation for the failing grade
            confidence: Confidence level (default 1.0)
            **kwargs: Additional parameters for the grade

        Returns:
            BinaryGrade instance with value=False
        """
        return cls(
            value=False, justification=justification, confidence=confidence, **kwargs
        )
