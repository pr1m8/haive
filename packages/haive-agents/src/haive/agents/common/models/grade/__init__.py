"""Grade models for structured output in Haive agents.

This module provides a comprehensive set of grading models that agents can use
for structured output across various evaluation tasks. The models support
different grading schemes including binary, numeric, letter grades, and
custom categorical evaluations.

Classes:
    GradeType: Enumeration of available grade model types
    Grade: Abstract base class for all grade models
    BinaryGrade: Simple pass/fail or yes/no grading
    NumericGrade: Numeric scoring with configurable ranges
    LetterGrade: Traditional letter-based grading (A-F)
    PercentageGrade: Percentage-based scoring (0-100%)
    RubricGrade: Multi-criteria rubric-based evaluation
    QualitativeGrade: Text-based qualitative assessment
    ScaleGrade: Likert-scale or custom scale grading
    CompositGrade: Combination of multiple grade types

Example:
    ```python
    from haive.agents.common.models.grade import BinaryGrade, NumericGrade

    # Simple binary evaluation
    grade = BinaryGrade(
        value=True,
        justification="Response directly answers the question",
        confidence=0.9
    )

    # Numeric scoring
    score = NumericGrade(
        value=8.5,
        min_value=0,
        max_value=10,
        justification="High quality with minor improvements needed"
    )
    ```
"""

from haive.agents.common.models.grade.base import Grade, GradeType
from haive.agents.common.models.grade.binary import BinaryGrade
from haive.agents.common.models.grade.composite import CompositeGrade
from haive.agents.common.models.grade.letter_grade import LetterGrade
from haive.agents.common.models.grade.numeric import NumericGrade, PercentageGrade
from haive.agents.common.models.grade.qualitative import QualitativeGrade
from haive.agents.common.models.grade.rubric import RubricCriterion, RubricGrade
from haive.agents.common.models.grade.scale import ScaleGrade

__all__ = [
    # Base classes
    "GradeType",
    "Grade",
    # Concrete grade models
    "BinaryGrade",
    "NumericGrade",
    "PercentageGrade",
    "LetterGrade",
    "RubricGrade",
    "RubricCriterion",
    "QualitativeGrade",
    "ScaleGrade",
    "CompositeGrade",
]

# Version info
__version__ = "1.0.0"
__author__ = "Haive Framework"
