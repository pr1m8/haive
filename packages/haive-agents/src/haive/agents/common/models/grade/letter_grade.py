"""Letter grading model for traditional A-F evaluations.

This module implements a traditional letter grading system with support
for plus/minus modifiers and customizable grading scales.
"""

from enum import Enum
from typing import Any

from pydantic import Field, field_validator

from haive.agents.common.models.grade.base import Grade, GradeType


class LetterValue(str, Enum):
    """Valid letter grade values.

    Attributes:
        A_PLUS: Exceptional performance (A+)
        A: Excellent performance (A)
        A_MINUS: Very good performance (A-)
        B_PLUS: Good performance (B+)
        B: Satisfactory performance (B)
        B_MINUS: Below satisfactory (B-)
        C_PLUS: Acceptable performance (C+)
        C: Minimally acceptable (C)
        C_MINUS: Below acceptable (C-)
        D_PLUS: Poor performance (D+)
        D: Very poor performance (D)
        D_MINUS: Extremely poor (D-)
        F: Failing performance (F)
    """

    A_PLUS = "A+"
    A = "A"
    A_MINUS = "A-"
    B_PLUS = "B+"
    B = "B"
    B_MINUS = "B-"
    C_PLUS = "C+"
    C = "C"
    C_MINUS = "C-"
    D_PLUS = "D+"
    D = "D"
    D_MINUS = "D-"
    F = "F"


class LetterGrade(Grade):
    """Letter grading model for traditional A-F evaluations.

    This grade model represents traditional letter grades with optional
    plus/minus modifiers. Includes conversion utilities and customizable
    grading scales.

    Attributes:
        value: The letter grade value (A+ to F)
        grade_type: Always GradeType.LETTER
        gpa_scale: GPA scale to use (4.0 or 5.0, default 4.0)
        passing_grade: Minimum letter grade considered passing (default C-)

    Example:
        ```python
        grade = LetterGrade(
            value="B+",
            justification="Strong understanding with minor gaps in analysis",
            gpa_scale=4.0
        )

        # Using enum value
        grade = LetterGrade(
            value=LetterValue.A_MINUS,
            justification="Excellent work with room for improvement"
        )

        # Custom passing threshold
        grade = LetterGrade(
            value="C",
            passing_grade="C",  # C is passing instead of default C-
            justification="Meets basic requirements"
        )
        ```
    """

    grade_type: GradeType = Field(
        default=GradeType.LETTER, description="Type of grade model (always letter)"
    )

    value: LetterValue = Field(
        ...,
        description="Letter grade value (A+ through F)",
        examples=["A", "B+", "C-", "F"],
    )

    gpa_scale: float = Field(
        default=4.0,
        description="GPA scale to use for calculations (typically 4.0 or 5.0)",
        examples=[4.0, 5.0],
    )

    passing_grade: LetterValue = Field(
        default=LetterValue.C_MINUS,
        description="Minimum letter grade considered passing",
    )

    @field_validator("value", mode="before")
    @classmethod
    def convert_to_letter_value(cls, v: Any) -> LetterValue:
        """Convert string or other representations to LetterValue.

        Args:
            v: Value to convert to LetterValue

        Returns:
            LetterValue enum instance

        Raises:
            ValueError: If the value cannot be converted to a valid letter grade
        """
        if isinstance(v, LetterValue):
            return v

        if isinstance(v, str):
            # Normalize the string
            v_upper = v.strip().upper()

            # Handle common variations
            letter_mappings = {
                "A+": LetterValue.A_PLUS,
                "APLUS": LetterValue.A_PLUS,
                "A PLUS": LetterValue.A_PLUS,
                "A": LetterValue.A,
                "A-": LetterValue.A_MINUS,
                "AMINUS": LetterValue.A_MINUS,
                "A MINUS": LetterValue.A_MINUS,
                "B+": LetterValue.B_PLUS,
                "BPLUS": LetterValue.B_PLUS,
                "B PLUS": LetterValue.B_PLUS,
                "B": LetterValue.B,
                "B-": LetterValue.B_MINUS,
                "BMINUS": LetterValue.B_MINUS,
                "B MINUS": LetterValue.B_MINUS,
                "C+": LetterValue.C_PLUS,
                "CPLUS": LetterValue.C_PLUS,
                "C PLUS": LetterValue.C_PLUS,
                "C": LetterValue.C,
                "C-": LetterValue.C_MINUS,
                "CMINUS": LetterValue.C_MINUS,
                "C MINUS": LetterValue.C_MINUS,
                "D+": LetterValue.D_PLUS,
                "DPLUS": LetterValue.D_PLUS,
                "D PLUS": LetterValue.D_PLUS,
                "D": LetterValue.D,
                "D-": LetterValue.D_MINUS,
                "DMINUS": LetterValue.D_MINUS,
                "D MINUS": LetterValue.D_MINUS,
                "F": LetterValue.F,
                "FAIL": LetterValue.F,
                "FAILING": LetterValue.F,
            }

            if v_upper in letter_mappings:
                return letter_mappings[v_upper]

            raise ValueError(f"Invalid letter grade: '{v}'. Must be A+ through F")

        raise ValueError(f"Cannot convert {type(v)} to letter grade")

    @field_validator("gpa_scale")
    @classmethod
    def validate_gpa_scale(cls, v: float) -> float:
        """Validate GPA scale is reasonable.

        Args:
            v: GPA scale value

        Returns:
            Validated GPA scale

        Raises:
            ValueError: If GPA scale is not reasonable
        """
        if v not in [4.0, 5.0]:
            raise ValueError("GPA scale must be 4.0 or 5.0")
        return v

    def get_normalized_score(self) -> float:
        """Get the grade as a normalized score between 0.0 and 1.0.

        Uses standard percentage equivalents for letter grades.

        Returns:
            Normalized score based on letter grade
        """
        # Standard percentage equivalents
        percentages = {
            LetterValue.A_PLUS: 97.5,
            LetterValue.A: 95.0,
            LetterValue.A_MINUS: 92.0,
            LetterValue.B_PLUS: 87.0,
            LetterValue.B: 85.0,
            LetterValue.B_MINUS: 82.0,
            LetterValue.C_PLUS: 77.0,
            LetterValue.C: 75.0,
            LetterValue.C_MINUS: 72.0,
            LetterValue.D_PLUS: 67.0,
            LetterValue.D: 65.0,
            LetterValue.D_MINUS: 62.0,
            LetterValue.F: 50.0,
        }

        return percentages[self.value] / 100.0

    def get_gpa_points(self) -> float:
        """Get GPA points for this letter grade.

        Returns:
            GPA points based on the configured scale
        """
        if self.gpa_scale == 4.0:
            gpa_4_scale = {
                LetterValue.A_PLUS: 4.0,
                LetterValue.A: 4.0,
                LetterValue.A_MINUS: 3.7,
                LetterValue.B_PLUS: 3.3,
                LetterValue.B: 3.0,
                LetterValue.B_MINUS: 2.7,
                LetterValue.C_PLUS: 2.3,
                LetterValue.C: 2.0,
                LetterValue.C_MINUS: 1.7,
                LetterValue.D_PLUS: 1.3,
                LetterValue.D: 1.0,
                LetterValue.D_MINUS: 0.7,
                LetterValue.F: 0.0,
            }
            return gpa_4_scale[self.value]

        # 5.0 scale
        gpa_5_scale = {
            LetterValue.A_PLUS: 5.0,
            LetterValue.A: 5.0,
            LetterValue.A_MINUS: 4.7,
            LetterValue.B_PLUS: 4.3,
            LetterValue.B: 4.0,
            LetterValue.B_MINUS: 3.7,
            LetterValue.C_PLUS: 3.3,
            LetterValue.C: 3.0,
            LetterValue.C_MINUS: 2.7,
            LetterValue.D_PLUS: 2.3,
            LetterValue.D: 2.0,
            LetterValue.D_MINUS: 1.7,
            LetterValue.F: 0.0,
        }
        return gpa_5_scale[self.value]

    def is_passing(self, threshold: str | None = None) -> bool:
        """Determine if the grade represents a passing score.

        Args:
            threshold: Custom passing threshold as letter grade string.
                      If None, uses instance passing_grade

        Returns:
            True if the grade meets or exceeds the passing threshold
        """
        if threshold is not None:
            threshold_letter = self.convert_to_letter_value(threshold)
        else:
            threshold_letter = self.passing_grade

        return self._letter_grade_comparison(self.value, threshold_letter) >= 0

    def _letter_grade_comparison(self, grade1: LetterValue, grade2: LetterValue) -> int:
        """Compare two letter grades.

        Args:
            grade1: First letter grade
            grade2: Second letter grade

        Returns:
            Positive if grade1 > grade2, 0 if equal, negative if grade1 < grade2
        """
        # Define ordering (higher index = better grade)
        ordering = [
            LetterValue.F,
            LetterValue.D_MINUS,
            LetterValue.D,
            LetterValue.D_PLUS,
            LetterValue.C_MINUS,
            LetterValue.C,
            LetterValue.C_PLUS,
            LetterValue.B_MINUS,
            LetterValue.B,
            LetterValue.B_PLUS,
            LetterValue.A_MINUS,
            LetterValue.A,
            LetterValue.A_PLUS,
        ]

        return ordering.index(grade1) - ordering.index(grade2)

    def get_letter_quality_description(self) -> str:
        """Get a descriptive quality label for the letter grade.

        Returns:
            String describing the quality level of the grade
        """
        descriptions = {
            LetterValue.A_PLUS: "Exceptional",
            LetterValue.A: "Excellent",
            LetterValue.A_MINUS: "Very Good",
            LetterValue.B_PLUS: "Good",
            LetterValue.B: "Satisfactory",
            LetterValue.B_MINUS: "Below Satisfactory",
            LetterValue.C_PLUS: "Acceptable",
            LetterValue.C: "Minimally Acceptable",
            LetterValue.C_MINUS: "Below Acceptable",
            LetterValue.D_PLUS: "Poor",
            LetterValue.D: "Very Poor",
            LetterValue.D_MINUS: "Extremely Poor",
            LetterValue.F: "Failing",
        }

        return descriptions[self.value]

    def to_display_string(self) -> str:
        """Convert grade to a human-readable display string.

        Returns:
            Formatted string representation of the letter grade
        """
        gpa = self.get_gpa_points()
        quality = self.get_letter_quality_description()
        passing_status = "✅" if self.is_passing() else "❌"

        return f"{passing_status} {self.value.value} ({gpa:.1f} GPA | {quality}) | {self.justification[:30]}..."

    def validate_grade_value(self, value: Any) -> bool:
        """Validate that a value can be converted to a letter grade.

        Args:
            value: The value to validate

        Returns:
            True if the value can be converted to LetterValue, False otherwise
        """
        try:
            self.convert_to_letter_value(value)
            return True
        except ValueError:
            return False

    @classmethod
    def from_percentage(
        cls, percentage: float, justification: str, gpa_scale: float = 4.0, **kwargs
    ) -> "LetterGrade":
        """Create a LetterGrade from a percentage score.

        Args:
            percentage: Percentage score (0-100)
            justification: Explanation for the grade
            gpa_scale: GPA scale to use
            **kwargs: Additional parameters for the grade

        Returns:
            LetterGrade instance corresponding to the percentage

        Raises:
            ValueError: If percentage is outside valid range
        """
        if not 0 <= percentage <= 100:
            raise ValueError(f"Percentage must be between 0 and 100, got {percentage}")

        # Standard percentage to letter conversion
        if percentage >= 97:
            letter = LetterValue.A_PLUS
        elif percentage >= 93:
            letter = LetterValue.A
        elif percentage >= 90:
            letter = LetterValue.A_MINUS
        elif percentage >= 87:
            letter = LetterValue.B_PLUS
        elif percentage >= 83:
            letter = LetterValue.B
        elif percentage >= 80:
            letter = LetterValue.B_MINUS
        elif percentage >= 77:
            letter = LetterValue.C_PLUS
        elif percentage >= 73:
            letter = LetterValue.C
        elif percentage >= 70:
            letter = LetterValue.C_MINUS
        elif percentage >= 67:
            letter = LetterValue.D_PLUS
        elif percentage >= 63:
            letter = LetterValue.D
        elif percentage >= 60:
            letter = LetterValue.D_MINUS
        else:
            letter = LetterValue.F

        return cls(
            value=letter, justification=justification, gpa_scale=gpa_scale, **kwargs
        )
