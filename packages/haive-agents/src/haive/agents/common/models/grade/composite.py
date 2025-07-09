"""Composite grading model for combining multiple grade types.

This module implements a composite grading system that combines multiple
different grade types into a single comprehensive evaluation.
"""

from typing import Any

from pydantic import Field, field_validator, model_validator

from haive.agents.common.models.grade.base import Grade, GradeType


class CompositeGrade(Grade):
    """Composite grading model for combining multiple grade types.

    This grade model combines multiple individual grades of different types
    into a single comprehensive assessment. It supports weighted averaging,
    statistical analysis, and consensus building across different grading approaches.

    Attributes:
        grades: List of individual grades to combine
        weights: Optional weights for each grade (auto-normalized)
        combination_method: Method for combining grades
        primary_grade_index: Index of the primary/most important grade
        consensus_threshold: Threshold for consensus analysis

    Example:
        ```python
        # Individual grades
        binary_grade = BinaryGrade(value=True, justification="Meets requirements")
        numeric_grade = NumericGrade(value=8.5, max_value=10, justification="High quality work")
        letter_grade = LetterGrade(value="B+", justification="Good performance overall")

        # Composite grade
        composite = CompositeGrade(
            grades=[binary_grade, numeric_grade, letter_grade],
            weights=[0.2, 0.5, 0.3],  # Different importance levels
            combination_method="weighted_average",
            justification="Combined assessment across multiple criteria"
        )

        # Equal weight composite
        composite_equal = CompositeGrade(
            grades=[binary_grade, numeric_grade, letter_grade],
            combination_method="simple_average",
            justification="Balanced multi-perspective evaluation"
        )
        ```
    """

    grade_type: GradeType = Field(
        default=GradeType.COMPOSITE,
        description="Type of grade model (always composite)",
    )

    grades: list[Grade] = Field(
        ...,
        description="List of individual grades to combine",
        min_length=2,
        max_length=10,
    )

    weights: list[float] | None = Field(
        default=None,
        description="Optional weights for each grade (auto-normalized if provided)",
        examples=[[0.3, 0.4, 0.3], [1.0, 2.0, 1.0], [0.25, 0.25, 0.5]],
    )

    combination_method: str = Field(
        default="weighted_average",
        description="Method for combining grades",
        examples=[
            "weighted_average",
            "simple_average",
            "median",
            "conservative",
            "optimistic",
        ],
    )

    primary_grade_index: int | None = Field(
        default=None,
        description="Index of the primary/most important grade (0-based)",
        examples=[0, 1, 2],
    )

    consensus_threshold: float = Field(
        default=0.8,
        description="Threshold for determining grade consensus (0.0 to 1.0)",
        ge=0.0,
        le=1.0,
    )

    @field_validator("combination_method")
    @classmethod
    def validate_combination_method(cls, v: str) -> str:
        """Validate that combination method is supported.

        Args:
            v: Combination method string

        Returns:
            Validated combination method

        Raises:
            ValueError: If combination method is not supported
        """
        valid_methods = {
            "weighted_average",
            "simple_average",
            "median",
            "conservative",
            "optimistic",
            "consensus",
            "primary_with_validation",
        }

        if v not in valid_methods:
            raise ValueError(
                f"combination_method must be one of: {sorted(valid_methods)}"
            )

        return v

    @model_validator(mode="after")
    def validate_weights_and_indices(self) -> "CompositeGrade":
        """Validate weights match grades count and indices are valid.

        Returns:
            Self if validation passes

        Raises:
            ValueError: If weights or indices are invalid
        """
        # Validate weights if provided
        if self.weights is not None:
            if len(self.weights) != len(self.grades):
                raise ValueError(
                    f"Number of weights ({len(self.weights)}) must match number of grades ({len(self.grades)})"
                )

            if any(w < 0 for w in self.weights):
                raise ValueError("All weights must be non-negative")

            if sum(self.weights) == 0:
                raise ValueError("Sum of weights cannot be zero")

        # Validate primary grade index
        if self.primary_grade_index is not None:
            if not 0 <= self.primary_grade_index < len(self.grades):
                raise ValueError(
                    f"primary_grade_index must be between 0 and {len(self.grades) - 1}"
                )

        return self

    def get_normalized_weights(self) -> list[float]:
        """Get normalized weights that sum to 1.0.

        Returns:
            List of normalized weights (equal weights if none provided)
        """
        if self.weights is None:
            # Equal weights
            return [1.0 / len(self.grades)] * len(self.grades)

        # Normalize provided weights
        total_weight = sum(self.weights)
        if total_weight == 0:
            return [1.0 / len(self.grades)] * len(self.grades)

        return [w / total_weight for w in self.weights]

    def get_normalized_score(self) -> float:
        """Get the composite grade as a normalized score between 0.0 and 1.0.

        Uses the specified combination method to compute the final score.

        Returns:
            Combined normalized score across all grades
        """
        if not self.grades:
            return 0.0

        # Get individual normalized scores
        scores = [grade.get_normalized_score() for grade in self.grades]

        if self.combination_method == "simple_average":
            return sum(scores) / len(scores)

        if self.combination_method == "weighted_average":
            weights = self.get_normalized_weights()
            return sum(
                score * weight for score, weight in zip(scores, weights, strict=False)
            )

        if self.combination_method == "median":
            sorted_scores = sorted(scores)
            n = len(sorted_scores)
            if n % 2 == 0:
                return (sorted_scores[n // 2 - 1] + sorted_scores[n // 2]) / 2
            return sorted_scores[n // 2]

        if self.combination_method == "conservative":
            # Use the minimum score (most conservative)
            return min(scores)

        if self.combination_method == "optimistic":
            # Use the maximum score (most optimistic)
            return max(scores)

        if self.combination_method == "consensus":
            # Use average if consensus exists, otherwise median
            if self.has_consensus():
                return sum(scores) / len(scores)
            return self.get_normalized_score_using_method("median")

        if self.combination_method == "primary_with_validation":
            # Use primary grade if it's consistent with others
            if self.primary_grade_index is not None:
                primary_score = scores[self.primary_grade_index]
                avg_others = sum(
                    scores[i]
                    for i in range(len(scores))
                    if i != self.primary_grade_index
                ) / (len(scores) - 1)

                # If primary is within 20% of others average, use it
                if abs(primary_score - avg_others) <= 0.2:
                    return primary_score
                # Fall back to weighted average
                weights = self.get_normalized_weights()
                return sum(
                    score * weight
                    for score, weight in zip(scores, weights, strict=False)
                )
            # No primary grade specified, use weighted average
            weights = self.get_normalized_weights()
            return sum(
                score * weight for score, weight in zip(scores, weights, strict=False)
            )

        # Default to weighted average
        weights = self.get_normalized_weights()
        return sum(
            score * weight for score, weight in zip(scores, weights, strict=False)
        )

    def get_normalized_score_using_method(self, method: str) -> float:
        """Get normalized score using a specific combination method.

        Args:
            method: Combination method to use

        Returns:
            Normalized score using the specified method
        """
        original_method = self.combination_method
        self.combination_method = method
        score = self.get_normalized_score()
        self.combination_method = original_method
        return score

    def is_passing(self, threshold: float | None = None) -> bool:
        """Determine if the composite grade represents a passing score.

        Args:
            threshold: Custom threshold for passing (0.0 to 1.0).
                      If None, uses 0.6 as default

        Returns:
            True if the composite score meets or exceeds the threshold
        """
        if threshold is None:
            threshold = 0.6

        return self.get_normalized_score() >= threshold

    def has_consensus(self) -> bool:
        """Check if there's consensus among the individual grades.

        Returns:
            True if the variance in normalized scores is below consensus threshold
        """
        scores = [grade.get_normalized_score() for grade in self.grades]

        if len(scores) <= 1:
            return True

        # Calculate coefficient of variation
        mean_score = sum(scores) / len(scores)
        if mean_score == 0:
            return True

        variance = sum((score - mean_score) ** 2 for score in scores) / len(scores)
        std_dev = variance**0.5
        cv = std_dev / mean_score

        # Lower coefficient of variation indicates higher consensus
        return cv <= (1.0 - self.consensus_threshold)

    def get_grade_statistics(self) -> dict[str, float]:
        """Get statistical analysis of the individual grades.

        Returns:
            Dictionary containing statistical measures
        """
        scores = [grade.get_normalized_score() for grade in self.grades]

        if not scores:
            return {}

        mean_score = sum(scores) / len(scores)
        variance = sum((score - mean_score) ** 2 for score in scores) / len(scores)
        std_dev = variance**0.5

        sorted_scores = sorted(scores)
        n = len(sorted_scores)
        median = (
            (sorted_scores[n // 2 - 1] + sorted_scores[n // 2]) / 2
            if n % 2 == 0
            else sorted_scores[n // 2]
        )

        return {
            "mean": mean_score,
            "median": median,
            "min": min(scores),
            "max": max(scores),
            "std_dev": std_dev,
            "variance": variance,
            "range": max(scores) - min(scores),
            "cv": std_dev / mean_score if mean_score > 0 else 0,
            "consensus": self.has_consensus(),
        }

    def get_grade_breakdown(self) -> list[dict[str, Any]]:
        """Get detailed breakdown of individual grades.

        Returns:
            List of dictionaries with information about each grade
        """
        weights = self.get_normalized_weights()

        breakdown = []
        for i, grade in enumerate(self.grades):
            breakdown.append(
                {
                    "index": i,
                    "grade_type": grade.grade_type.value,
                    "normalized_score": grade.get_normalized_score(),
                    "weight": weights[i],
                    "weighted_contribution": grade.get_normalized_score() * weights[i],
                    "is_primary": i == self.primary_grade_index,
                    "is_passing": grade.is_passing(),
                    "justification_preview": (
                        grade.justification[:50] + "..."
                        if len(grade.justification) > 50
                        else grade.justification
                    ),
                }
            )

        return breakdown

    def get_outlier_grades(self, threshold: float = 0.3) -> list[int]:
        """Identify grades that are outliers compared to the group.

        Args:
            threshold: Deviation threshold for considering a grade an outlier

        Returns:
            List of indices of grades that are outliers
        """
        scores = [grade.get_normalized_score() for grade in self.grades]
        mean_score = sum(scores) / len(scores)

        outliers = []
        for i, score in enumerate(scores):
            if abs(score - mean_score) > threshold:
                outliers.append(i)

        return outliers

    def get_consensus_analysis(self) -> dict[str, Any]:
        """Get detailed consensus analysis.

        Returns:
            Dictionary with consensus analysis information
        """
        stats = self.get_grade_statistics()
        outliers = self.get_outlier_grades()

        consensus_level = (
            "high"
            if stats.get("cv", 1.0) < 0.1
            else "medium" if stats.get("cv", 1.0) < 0.3 else "low"
        )

        return {
            "has_consensus": self.has_consensus(),
            "consensus_level": consensus_level,
            "coefficient_of_variation": stats.get("cv", 0),
            "score_range": stats.get("range", 0),
            "outlier_count": len(outliers),
            "outlier_indices": outliers,
            "agreement_percentage": (1.0 - stats.get("cv", 1.0)) * 100,
        }

    def to_display_string(self) -> str:
        """Convert grade to a human-readable display string.

        Returns:
            Formatted string representation of the composite grade
        """
        composite_score = self.get_normalized_score() * 100
        passing_status = "✅" if self.is_passing() else "❌"
        consensus_status = "🤝" if self.has_consensus() else "🤔"
        grade_count = len(self.grades)
        method = self.combination_method.replace("_", " ").title()

        return f"{passing_status}{consensus_status} Composite: {composite_score:.1f}% ({grade_count} grades | {method}) | {self.justification[:25]}..."

    def validate_grade_value(self, value: Any) -> bool:
        """Validate that a value represents valid composite grade data.

        Args:
            value: The value to validate (should be list of grades)

        Returns:
            True if the value can be converted to valid grades, False otherwise
        """
        try:
            if not isinstance(value, list):
                return False

            if len(value) < 2:
                return False

            # Check if all items are Grade instances or can be converted
            for item in value:
                if not isinstance(item, Grade):
                    return False

            return True
        except Exception:
            return False

    @classmethod
    def create_from_grades(
        cls,
        grades: list[Grade],
        justification: str,
        weights: list[float] | None = None,
        method: str = "weighted_average",
        **kwargs,
    ) -> "CompositeGrade":
        """Create a CompositeGrade from a list of existing grades.

        Args:
            grades: List of Grade instances to combine
            justification: Overall justification for the composite
            weights: Optional weights for each grade
            method: Combination method to use
            **kwargs: Additional parameters

        Returns:
            CompositeGrade instance
        """
        return cls(
            grades=grades,
            weights=weights,
            combination_method=method,
            justification=justification,
            **kwargs,
        )

    @classmethod
    def create_consensus_grade(
        cls,
        grades: list[Grade],
        justification: str,
        consensus_threshold: float = 0.8,
        **kwargs,
    ) -> "CompositeGrade":
        """Create a CompositeGrade focused on consensus building.

        Args:
            grades: List of Grade instances to combine
            justification: Overall justification
            consensus_threshold: Threshold for consensus detection
            **kwargs: Additional parameters

        Returns:
            CompositeGrade configured for consensus analysis
        """
        return cls(
            grades=grades,
            combination_method="consensus",
            consensus_threshold=consensus_threshold,
            justification=justification,
            **kwargs,
        )
