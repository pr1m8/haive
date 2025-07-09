"""Rubric grading model for multi-criteria evaluations.

This module implements a rubric-based grading system that evaluates
multiple criteria with individual scores and weights.
"""

from typing import Any

from pydantic import BaseModel, Field, field_validator, model_validator

from haive.agents.common.models.grade.base import Grade, GradeType


class RubricCriterion(BaseModel):
    """Individual criterion within a rubric.

    Represents a single evaluation criterion with its own score,
    weight, and justification.

    Attributes:
        name: Name of the criterion
        score: Score for this criterion
        max_score: Maximum possible score for this criterion
        weight: Relative weight of this criterion (default 1.0)
        justification: Explanation for the score given

    Example:
        ```python
        criterion = RubricCriterion(
            name="Content Quality",
            score=8.5,
            max_score=10,
            weight=0.4,
            justification="Strong content with minor gaps in coverage"
        )
        ```
    """

    name: str = Field(
        ...,
        description="Name or description of the evaluation criterion",
        min_length=1,
        max_length=200,
        examples=["Content Quality", "Organization", "Grammar & Style", "Originality"],
    )

    score: int | float = Field(
        ..., description="Score achieved for this criterion", examples=[8.5, 7, 4.2, 9]
    )

    max_score: int | float = Field(
        ...,
        description="Maximum possible score for this criterion",
        gt=0,
        examples=[10, 5, 100, 4],
    )

    weight: float = Field(
        default=1.0,
        description="Relative weight/importance of this criterion",
        gt=0,
        examples=[1.0, 0.5, 2.0, 0.25],
    )

    justification: str = Field(
        ...,
        description="Explanation for the score given to this criterion",
        min_length=3,
        max_length=1000,
        examples=[
            "Strong logical flow with clear transitions",
            "Minor grammatical errors throughout",
            "Highly original approach to the problem",
        ],
    )

    @field_validator("score")
    @classmethod
    def validate_score_range(cls, v: int | float, info) -> int | float:
        """Validate that score is within valid range.

        Args:
            v: The score value
            info: Validation context containing other field values

        Returns:
            Validated score

        Raises:
            ValueError: If score is outside valid range
        """
        # Note: In Pydantic v2, we can't access other fields during validation
        # This validation will be handled at the model level
        if v < 0:
            raise ValueError("Score cannot be negative")
        return v

    @model_validator(mode="after")
    def validate_score_within_max(self) -> "RubricCriterion":
        """Validate that score does not exceed max_score.

        Returns:
            Self if validation passes

        Raises:
            ValueError: If score exceeds max_score
        """
        if self.score > self.max_score:
            raise ValueError(
                f"Score {self.score} exceeds max_score {self.max_score} for criterion '{self.name}'"
            )
        return self

    def get_normalized_score(self) -> float:
        """Get the criterion score as a normalized value (0.0 to 1.0).

        Returns:
            Normalized score (score / max_score)
        """
        if self.max_score == 0:
            return 0.0
        return self.score / self.max_score

    def get_percentage_score(self) -> float:
        """Get the criterion score as a percentage.

        Returns:
            Percentage score (normalized score * 100)
        """
        return self.get_normalized_score() * 100

    def get_weighted_score(self) -> float:
        """Get the weighted score for this criterion.

        Returns:
            Score multiplied by weight
        """
        return self.score * self.weight

    def get_weighted_max_score(self) -> float:
        """Get the weighted maximum score for this criterion.

        Returns:
            Max score multiplied by weight
        """
        return self.max_score * self.weight


class RubricGrade(Grade):
    """Rubric grading model for multi-criteria evaluations.

    This grade model evaluates multiple criteria, each with their own
    scores, weights, and justifications, then combines them into an
    overall grade.

    Attributes:
        criteria: List of individual rubric criteria
        grade_type: Always GradeType.RUBRIC
        overall_justification: Overall summary justification

    Example:
        ```python
        criteria = [
            RubricCriterion(
                name="Content Quality",
                score=8.5,
                max_score=10,
                weight=0.4,
                justification="Strong content with comprehensive coverage"
            ),
            RubricCriterion(
                name="Organization",
                score=7.0,
                max_score=10,
                weight=0.3,
                justification="Good structure but some transitions unclear"
            ),
            RubricCriterion(
                name="Grammar",
                score=9.0,
                max_score=10,
                weight=0.3,
                justification="Excellent grammar with only minor errors"
            )
        ]

        grade = RubricGrade(
            criteria=criteria,
            justification="Overall strong performance with room for improvement in organization"
        )
        ```
    """

    grade_type: GradeType = Field(
        default=GradeType.RUBRIC, description="Type of grade model (always rubric)"
    )

    criteria: list[RubricCriterion] = Field(
        ...,
        description="List of individual rubric criteria",
        min_length=1,
        max_length=20,
    )

    @field_validator("criteria")
    @classmethod
    def validate_criteria_names_unique(
        cls, v: list[RubricCriterion]
    ) -> list[RubricCriterion]:
        """Validate that all criterion names are unique.

        Args:
            v: List of criteria to validate

        Returns:
            Validated criteria list

        Raises:
            ValueError: If criterion names are not unique
        """
        names = [criterion.name.lower().strip() for criterion in v]
        if len(names) != len(set(names)):
            raise ValueError("All criterion names must be unique")
        return v

    def get_normalized_score(self) -> float:
        """Get the overall grade as a normalized score between 0.0 and 1.0.

        Calculates weighted average of all criteria scores.

        Returns:
            Weighted normalized score across all criteria
        """
        if not self.criteria:
            return 0.0

        total_weighted_score = sum(
            criterion.get_normalized_score() * criterion.weight
            for criterion in self.criteria
        )
        total_weight = sum(criterion.weight for criterion in self.criteria)

        if total_weight == 0:
            return 0.0

        return total_weighted_score / total_weight

    def get_raw_weighted_score(self) -> float:
        """Get the total raw weighted score.

        Returns:
            Sum of all weighted scores
        """
        return sum(criterion.get_weighted_score() for criterion in self.criteria)

    def get_max_weighted_score(self) -> float:
        """Get the maximum possible weighted score.

        Returns:
            Sum of all weighted maximum scores
        """
        return sum(criterion.get_weighted_max_score() for criterion in self.criteria)

    def is_passing(self, threshold: float | None = None) -> bool:
        """Determine if the rubric grade represents a passing score.

        Args:
            threshold: Custom threshold for passing (0.0 to 1.0).
                      If None, uses 0.7 (70%) as default

        Returns:
            True if the overall score meets or exceeds the threshold
        """
        if threshold is None:
            threshold = 0.7  # Default 70% passing threshold

        return self.get_normalized_score() >= threshold

    def get_criterion_by_name(self, name: str) -> RubricCriterion | None:
        """Get a specific criterion by name.

        Args:
            name: Name of the criterion to find

        Returns:
            RubricCriterion if found, None otherwise
        """
        name_lower = name.lower().strip()
        for criterion in self.criteria:
            if criterion.name.lower().strip() == name_lower:
                return criterion
        return None

    def get_criteria_summary(self) -> dict[str, dict[str, Any]]:
        """Get a summary of all criteria performance.

        Returns:
            Dictionary mapping criterion names to their summary info
        """
        return {
            criterion.name: {
                "score": criterion.score,
                "max_score": criterion.max_score,
                "percentage": criterion.get_percentage_score(),
                "normalized": criterion.get_normalized_score(),
                "weight": criterion.weight,
                "weighted_score": criterion.get_weighted_score(),
                "justification": criterion.justification,
            }
            for criterion in self.criteria
        }

    def get_weakest_criteria(self, count: int = 3) -> list[RubricCriterion]:
        """Get the criteria with the lowest normalized scores.

        Args:
            count: Number of weakest criteria to return

        Returns:
            List of criteria sorted by normalized score (lowest first)
        """
        sorted_criteria = sorted(self.criteria, key=lambda c: c.get_normalized_score())
        return sorted_criteria[:count]

    def get_strongest_criteria(self, count: int = 3) -> list[RubricCriterion]:
        """Get the criteria with the highest normalized scores.

        Args:
            count: Number of strongest criteria to return

        Returns:
            List of criteria sorted by normalized score (highest first)
        """
        sorted_criteria = sorted(
            self.criteria, key=lambda c: c.get_normalized_score(), reverse=True
        )
        return sorted_criteria[:count]

    def get_improvement_suggestions(self) -> list[str]:
        """Generate improvement suggestions based on weakest criteria.

        Returns:
            List of suggestions for improvement
        """
        weakest = self.get_weakest_criteria(2)
        suggestions = []

        for criterion in weakest:
            if criterion.get_normalized_score() < 0.7:
                suggestions.append(
                    f"Focus on improving '{criterion.name}' "
                    f"(currently {criterion.get_percentage_score():.1f}%): "
                    f"{criterion.justification}"
                )

        return suggestions

    def to_display_string(self) -> str:
        """Convert grade to a human-readable display string.

        Returns:
            Formatted string representation of the rubric grade
        """
        overall_percentage = self.get_normalized_score() * 100
        passing_status = "✅" if self.is_passing() else "❌"
        criteria_count = len(self.criteria)

        return f"{passing_status} Rubric: {overall_percentage:.1f}% ({criteria_count} criteria) | {self.justification[:30]}..."

    def validate_grade_value(self, value: Any) -> bool:
        """Validate that a value represents valid rubric criteria.

        Args:
            value: The value to validate (should be list of criteria)

        Returns:
            True if the value can be converted to valid criteria, False otherwise
        """
        try:
            if not isinstance(value, list):
                return False

            if len(value) == 0:
                return False

            # Check if all items can be converted to RubricCriterion
            for item in value:
                if isinstance(item, dict):
                    RubricCriterion(**item)
                elif isinstance(item, RubricCriterion):
                    continue
                else:
                    return False

            return True
        except Exception:
            return False

    @classmethod
    def create_simple_rubric(
        cls,
        criteria_scores: dict[str, float | dict[str, Any]],
        justification: str,
        max_score: float = 10.0,
        **kwargs,
    ) -> "RubricGrade":
        """Create a simple rubric with equal weights.

        Args:
            criteria_scores: Dict mapping criterion names to scores or score dicts
            justification: Overall justification
            max_score: Maximum score for all criteria (default 10.0)
            **kwargs: Additional parameters for the grade

        Returns:
            RubricGrade instance with equal-weighted criteria

        Example:
            ```python
            grade = RubricGrade.create_simple_rubric(
                criteria_scores={
                    "Content": 8.5,
                    "Style": {"score": 7.0, "justification": "Good style overall"},
                    "Accuracy": 9.0
                },
                justification="Strong overall performance",
                max_score=10
            )
            ```
        """
        criteria = []

        for name, score_data in criteria_scores.items():
            if isinstance(score_data, (int, float)):
                # Simple score
                criterion = RubricCriterion(
                    name=name,
                    score=score_data,
                    max_score=max_score,
                    weight=1.0,
                    justification=f"Score: {score_data}/{max_score}",
                )
            elif isinstance(score_data, dict):
                # Detailed score data
                criterion = RubricCriterion(
                    name=name,
                    score=score_data.get("score", 0),
                    max_score=score_data.get("max_score", max_score),
                    weight=score_data.get("weight", 1.0),
                    justification=score_data.get(
                        "justification", f"Score: {score_data.get('score', 0)}"
                    ),
                )
            else:
                raise ValueError(
                    f"Invalid score data for criterion '{name}': {score_data}"
                )

            criteria.append(criterion)

        return cls(criteria=criteria, justification=justification, **kwargs)
