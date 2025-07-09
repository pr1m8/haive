"""Qualitative grading model for text-based evaluations.

This module implements a qualitative grading system that provides
text-based assessments with sentiment analysis and quality indicators.
"""

from enum import Enum
from typing import Any

from pydantic import Field, field_validator, model_validator

from haive.agents.common.models.grade.base import Grade, GradeType


class QualityLevel(str, Enum):
    """Quality levels for qualitative assessment.

    Attributes:
        EXCEPTIONAL: Outstanding quality, exceeds expectations
        EXCELLENT: High quality, meets all expectations
        GOOD: Satisfactory quality, meets most expectations
        FAIR: Adequate quality, meets basic expectations
        POOR: Below expectations, significant issues
        UNACCEPTABLE: Does not meet minimum standards
    """

    EXCEPTIONAL = "exceptional"
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    UNACCEPTABLE = "unacceptable"


class SentimentType(str, Enum):
    """Sentiment types for qualitative feedback.

    Attributes:
        VERY_POSITIVE: Highly positive feedback
        POSITIVE: Generally positive feedback
        NEUTRAL: Balanced or neutral feedback
        NEGATIVE: Generally negative feedback
        VERY_NEGATIVE: Highly negative feedback
    """

    VERY_POSITIVE = "very_positive"
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"
    VERY_NEGATIVE = "very_negative"


class QualitativeGrade(Grade):
    """Qualitative grading model for text-based evaluations.

    This grade model provides detailed text-based assessments with
    quality levels, sentiment analysis, and structured feedback
    including strengths, weaknesses, and recommendations.

    Attributes:
        quality_level: Overall quality assessment
        sentiment: Sentiment of the feedback
        strengths: List of identified strengths
        weaknesses: List of identified weaknesses
        recommendations: List of improvement recommendations
        detailed_feedback: Extended qualitative feedback

    Example:
        ```python
        grade = QualitativeGrade(
            quality_level=QualityLevel.GOOD,
            sentiment=SentimentType.POSITIVE,
            strengths=[
                "Clear logical structure",
                "Strong supporting evidence",
                "Engaging writing style"
            ],
            weaknesses=[
                "Minor grammatical errors",
                "Could use more varied sentence structure"
            ],
            recommendations=[
                "Proofread for grammatical accuracy",
                "Vary sentence length and structure for better flow"
            ],
            justification="Well-written piece with strong content but needs polish",
            detailed_feedback="This work demonstrates a solid understanding..."
        )
        ```
    """

    grade_type: GradeType = Field(
        default=GradeType.QUALITATIVE,
        description="Type of grade model (always qualitative)",
    )

    quality_level: QualityLevel = Field(
        ...,
        description="Overall quality assessment level",
        examples=["good", "excellent", "fair"],
    )

    sentiment: SentimentType = Field(
        default=SentimentType.NEUTRAL,
        description="Sentiment tone of the evaluation",
        examples=["positive", "neutral", "negative"],
    )

    strengths: list[str] = Field(
        default_factory=list,
        description="List of identified strengths",
        max_length=10,
        examples=[
            ["Clear writing", "Good research", "Strong conclusions"],
            ["Creative approach", "Well-organized", "Thorough analysis"],
        ],
    )

    weaknesses: list[str] = Field(
        default_factory=list,
        description="List of identified weaknesses or areas for improvement",
        max_length=10,
        examples=[
            ["Grammar issues", "Weak introduction", "Needs more examples"],
            ["Unclear thesis", "Poor citations", "Repetitive content"],
        ],
    )

    recommendations: list[str] = Field(
        default_factory=list,
        description="List of specific recommendations for improvement",
        max_length=10,
        examples=[
            ["Proofread carefully", "Strengthen introduction", "Add more examples"],
            ["Clarify main argument", "Improve citation format", "Reduce repetition"],
        ],
    )

    detailed_feedback: str | None = Field(
        default=None,
        description="Extended qualitative feedback and commentary",
        max_length=5000,
        examples=[
            "This essay demonstrates a strong understanding of the topic...",
            "The analysis is thorough but could benefit from...",
        ],
    )

    @field_validator("strengths", "weaknesses", "recommendations")
    @classmethod
    def validate_feedback_items(cls, v: list[str]) -> list[str]:
        """Validate that feedback items are meaningful.

        Args:
            v: List of feedback items to validate

        Returns:
            Validated list of feedback items

        Raises:
            ValueError: If items are empty or too vague
        """
        validated_items = []
        for item in v:
            if not item or item.strip() == "":
                continue  # Skip empty items

            item_clean = item.strip()
            if len(item_clean) < 3:
                raise ValueError(f"Feedback item '{item_clean}' is too short")

            # Check for overly vague items
            vague_items = {"good", "bad", "ok", "fine", "nice", "poor", "great"}
            if item_clean.lower() in vague_items:
                raise ValueError(f"Feedback item '{item_clean}' is too vague")

            validated_items.append(item_clean)

        return validated_items

    @model_validator(mode="after")
    def validate_feedback_consistency(self) -> "QualitativeGrade":
        """Validate that feedback is consistent with quality level.

        Returns:
            Self if validation passes

        Raises:
            ValueError: If feedback is inconsistent with quality level
        """
        # Check sentiment consistency with quality level
        quality_to_sentiment = {
            QualityLevel.EXCEPTIONAL: [
                SentimentType.VERY_POSITIVE,
                SentimentType.POSITIVE,
            ],
            QualityLevel.EXCELLENT: [
                SentimentType.VERY_POSITIVE,
                SentimentType.POSITIVE,
            ],
            QualityLevel.GOOD: [SentimentType.POSITIVE, SentimentType.NEUTRAL],
            QualityLevel.FAIR: [SentimentType.NEUTRAL, SentimentType.NEGATIVE],
            QualityLevel.POOR: [SentimentType.NEGATIVE, SentimentType.VERY_NEGATIVE],
            QualityLevel.UNACCEPTABLE: [
                SentimentType.NEGATIVE,
                SentimentType.VERY_NEGATIVE,
            ],
        }

        expected_sentiments = quality_to_sentiment[self.quality_level]
        if self.sentiment not in expected_sentiments:
            raise ValueError(
                f"Sentiment '{self.sentiment}' is inconsistent with quality level '{self.quality_level}'"
            )

        return self

    def get_normalized_score(self) -> float:
        """Get the grade as a normalized score between 0.0 and 1.0.

        Based on quality level mapping to numeric equivalents.

        Returns:
            Normalized score based on quality level
        """
        quality_scores = {
            QualityLevel.EXCEPTIONAL: 0.95,
            QualityLevel.EXCELLENT: 0.85,
            QualityLevel.GOOD: 0.75,
            QualityLevel.FAIR: 0.65,
            QualityLevel.POOR: 0.45,
            QualityLevel.UNACCEPTABLE: 0.25,
        }

        return quality_scores[self.quality_level]

    def is_passing(self, threshold: float | None = None) -> bool:
        """Determine if the grade represents a passing score.

        Args:
            threshold: Custom threshold for passing (0.0 to 1.0).
                      If None, uses 0.6 (equivalent to "fair" quality)

        Returns:
            True if the quality level meets or exceeds the threshold
        """
        if threshold is None:
            # Default: "fair" and above is passing
            passing_levels = {
                QualityLevel.EXCEPTIONAL,
                QualityLevel.EXCELLENT,
                QualityLevel.GOOD,
                QualityLevel.FAIR,
            }
            return self.quality_level in passing_levels

        return self.get_normalized_score() >= threshold

    def get_feedback_summary(self) -> dict[str, Any]:
        """Get a structured summary of all feedback.

        Returns:
            Dictionary containing organized feedback information
        """
        return {
            "quality_level": self.quality_level.value,
            "sentiment": self.sentiment.value,
            "strengths_count": len(self.strengths),
            "weaknesses_count": len(self.weaknesses),
            "recommendations_count": len(self.recommendations),
            "has_detailed_feedback": bool(self.detailed_feedback),
            "feedback_balance": self._calculate_feedback_balance(),
            "improvement_areas": self.weaknesses[:3],  # Top 3 weaknesses
            "key_strengths": self.strengths[:3],  # Top 3 strengths
        }

    def _calculate_feedback_balance(self) -> str:
        """Calculate the balance between positive and negative feedback.

        Returns:
            String describing the feedback balance
        """
        strength_count = len(self.strengths)
        weakness_count = len(self.weaknesses)

        if strength_count == 0 and weakness_count == 0:
            return "no_specific_feedback"
        if strength_count > weakness_count * 2:
            return "predominantly_positive"
        if weakness_count > strength_count * 2:
            return "predominantly_negative"
        if abs(strength_count - weakness_count) <= 1:
            return "balanced"
        if strength_count > weakness_count:
            return "mostly_positive"
        return "mostly_negative"

    def get_improvement_priority(self) -> list[str]:
        """Get prioritized improvement recommendations.

        Returns top weaknesses with corresponding recommendations.

        Returns:
            List of prioritized improvement items
        """
        improvements = []

        # Add weaknesses with recommendations
        for i, weakness in enumerate(self.weaknesses[:3]):
            if i < len(self.recommendations):
                improvements.append(f"{weakness} → {self.recommendations[i]}")
            else:
                improvements.append(weakness)

        # Add remaining recommendations
        if len(self.recommendations) > len(self.weaknesses):
            remaining_recs = self.recommendations[len(self.weaknesses) :]
            improvements.extend(remaining_recs[:2])  # Add up to 2 more

        return improvements[:5]  # Return top 5 priorities

    def generate_narrative_summary(self) -> str:
        """Generate a narrative summary of the qualitative assessment.

        Returns:
            Human-readable narrative summary
        """
        quality_desc = {
            QualityLevel.EXCEPTIONAL: "exceptional work that exceeds expectations",
            QualityLevel.EXCELLENT: "excellent work that meets all expectations",
            QualityLevel.GOOD: "good work that meets most expectations",
            QualityLevel.FAIR: "fair work that meets basic expectations",
            QualityLevel.POOR: "work that falls below expectations",
            QualityLevel.UNACCEPTABLE: "work that does not meet minimum standards",
        }

        summary = f"This represents {quality_desc[self.quality_level]}. "

        if self.strengths:
            summary += f"Key strengths include: {', '.join(self.strengths[:3])}. "

        if self.weaknesses:
            summary += f"Areas for improvement: {', '.join(self.weaknesses[:3])}. "

        if self.recommendations:
            summary += f"Recommended actions: {', '.join(self.recommendations[:2])}."

        return summary.strip()

    def to_display_string(self) -> str:
        """Convert grade to a human-readable display string.

        Returns:
            Formatted string representation of the qualitative grade
        """
        quality_emoji = {
            QualityLevel.EXCEPTIONAL: "🌟",
            QualityLevel.EXCELLENT: "✨",
            QualityLevel.GOOD: "✅",
            QualityLevel.FAIR: "⚖️",
            QualityLevel.POOR: "⚠️",
            QualityLevel.UNACCEPTABLE: "❌",
        }

        emoji = quality_emoji[self.quality_level]
        percentage = self.get_normalized_score() * 100

        return f"{emoji} {self.quality_level.value.title()} ({percentage:.0f}%) | {len(self.strengths)}+ / {len(self.weaknesses)}- | {self.justification[:25]}..."

    def validate_grade_value(self, value: Any) -> bool:
        """Validate that a value can be converted to a quality level.

        Args:
            value: The value to validate

        Returns:
            True if the value can be converted to QualityLevel, False otherwise
        """
        try:
            if isinstance(value, QualityLevel):
                return True
            if isinstance(value, str):
                QualityLevel(value.lower())
                return True
            return False
        except ValueError:
            return False

    @classmethod
    def create_positive_feedback(
        cls,
        justification: str,
        strengths: list[str],
        minor_improvements: list[str] | None = None,
        quality_level: QualityLevel = QualityLevel.GOOD,
        **kwargs,
    ) -> "QualitativeGrade":
        """Create predominantly positive qualitative feedback.

        Args:
            justification: Main justification
            strengths: List of strengths to highlight
            minor_improvements: Optional minor areas for improvement
            quality_level: Quality level (default GOOD)
            **kwargs: Additional parameters

        Returns:
            QualitativeGrade with positive sentiment
        """
        return cls(
            quality_level=quality_level,
            sentiment=SentimentType.POSITIVE,
            strengths=strengths,
            weaknesses=minor_improvements or [],
            justification=justification,
            **kwargs,
        )

    @classmethod
    def create_constructive_feedback(
        cls,
        justification: str,
        strengths: list[str],
        weaknesses: list[str],
        recommendations: list[str],
        quality_level: QualityLevel = QualityLevel.FAIR,
        **kwargs,
    ) -> "QualitativeGrade":
        """Create balanced constructive feedback.

        Args:
            justification: Main justification
            strengths: List of strengths
            weaknesses: List of weaknesses
            recommendations: List of improvement recommendations
            quality_level: Quality level (default FAIR)
            **kwargs: Additional parameters

        Returns:
            QualitativeGrade with balanced feedback
        """
        return cls(
            quality_level=quality_level,
            sentiment=SentimentType.NEUTRAL,
            strengths=strengths,
            weaknesses=weaknesses,
            recommendations=recommendations,
            justification=justification,
            **kwargs,
        )
