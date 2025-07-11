"""Task solvability and readiness assessment.

This module analyzes whether tasks are currently solvable, what barriers exist,
and what would be required to make unsolvable tasks solvable.
"""

from datetime import timedelta
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator

from haive.agents.common.models.task_analysis.base import SolvabilityStatus


class SolvabilityBarrier(str, Enum):
    """Types of barriers that prevent task solvability.

    Attributes:
        KNOWLEDGE_GAP: Missing fundamental knowledge or understanding
        TECHNOLOGY_LIMITATION: Current technology is insufficient
        RESOURCE_CONSTRAINT: Insufficient computational, financial, or material resources
        THEORETICAL_IMPOSSIBILITY: Task violates known physical or logical laws
        REGULATORY_BARRIER: Legal, ethical, or regulatory constraints
        COORDINATION_COMPLEXITY: Too complex to coordinate effectively
        TIME_CONSTRAINT: Not enough time available given current methods
        DATA_UNAVAILABILITY: Required data doesn't exist or isn't accessible
        EXPERT_UNAVAILABILITY: Required human expertise not available
        INFRASTRUCTURE_LIMITATION: Missing necessary infrastructure or systems
        ETHICAL_CONCERN: Ethical issues prevent pursuit of solution
        SAFETY_RISK: Safety risks are too high to attempt
    """

    KNOWLEDGE_GAP = "knowledge_gap"
    TECHNOLOGY_LIMITATION = "technology_limitation"
    RESOURCE_CONSTRAINT = "resource_constraint"
    THEORETICAL_IMPOSSIBILITY = "theoretical_impossibility"
    REGULATORY_BARRIER = "regulatory_barrier"
    COORDINATION_COMPLEXITY = "coordination_complexity"
    TIME_CONSTRAINT = "time_constraint"
    DATA_UNAVAILABILITY = "data_unavailability"
    EXPERT_UNAVAILABILITY = "expert_unavailability"
    INFRASTRUCTURE_LIMITATION = "infrastructure_limitation"
    ETHICAL_CONCERN = "ethical_concern"
    SAFETY_RISK = "safety_risk"


class SolvabilityAssessment(BaseModel):
    """Comprehensive assessment of task solvability and readiness.

    Analyzes whether a task can be solved with current capabilities,
    what barriers exist, and what would be required to overcome them.

    Attributes:
        solvability_status: Current solvability classification
        is_currently_solvable: Whether task can be solved right now
        confidence_level: Confidence in the solvability assessment
        primary_barriers: Main obstacles preventing solution
        secondary_barriers: Additional challenges that may arise
        enabling_factors: Factors that make the task more solvable
        breakthrough_requirements: What breakthroughs would be needed
        estimated_time_to_solvable: Time until task becomes solvable
        alternative_approaches: Possible alternative solution paths

    Example:
        ```python
        # Simple factual lookup - highly solvable
        assessment = SolvabilityAssessment(
            solvability_status=SolvabilityStatus.READY,
            is_currently_solvable=True,
            confidence_level=0.95,
            primary_barriers=[],
            enabling_factors=["web_search", "public_databases"],
            estimated_time_to_solvable=timedelta(0)
        )

        # Cancer cure - major breakthrough required
        assessment = SolvabilityAssessment(
            solvability_status=SolvabilityStatus.THEORETICAL,
            is_currently_solvable=False,
            confidence_level=0.7,
            primary_barriers=[
                SolvabilityBarrier.KNOWLEDGE_GAP,
                SolvabilityBarrier.TECHNOLOGY_LIMITATION,
                SolvabilityBarrier.RESOURCE_CONSTRAINT
            ],
            breakthrough_requirements=[
                "fundamental_understanding_of_cancer_biology",
                "advanced_genetic_engineering_tools",
                "personalized_medicine_capabilities"
            ],
            estimated_time_to_solvable=timedelta(days=7300)  # ~20 years
        )
        ```
    """

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        use_enum_values=True,
        str_strip_whitespace=True,
    )

    solvability_status: SolvabilityStatus = Field(
        ...,
        description="Current solvability classification",
        examples=["ready", "researchable", "theoretical", "impossible"],
    )

    is_currently_solvable: bool = Field(
        ...,
        description="Whether task can be solved with current capabilities",
        examples=[True, False],
    )

    confidence_level: float = Field(
        ...,
        description="Confidence in the solvability assessment (0.0-1.0)",
        ge=0.0,
        le=1.0,
        examples=[0.95, 0.8, 0.6, 0.3],
    )

    primary_barriers: list[SolvabilityBarrier] = Field(
        default_factory=list,
        description="Main obstacles preventing solution",
        max_length=10,
        examples=[
            [],
            [SolvabilityBarrier.KNOWLEDGE_GAP],
            [
                SolvabilityBarrier.TECHNOLOGY_LIMITATION,
                SolvabilityBarrier.RESOURCE_CONSTRAINT,
            ],
            [SolvabilityBarrier.THEORETICAL_IMPOSSIBILITY],
        ],
    )

    secondary_barriers: list[SolvabilityBarrier] = Field(
        default_factory=list,
        description="Additional challenges that may arise",
        max_length=15,
        examples=[
            [SolvabilityBarrier.REGULATORY_BARRIER],
            [
                SolvabilityBarrier.COORDINATION_COMPLEXITY,
                SolvabilityBarrier.TIME_CONSTRAINT,
            ],
            [SolvabilityBarrier.EXPERT_UNAVAILABILITY, SolvabilityBarrier.SAFETY_RISK],
        ],
    )

    enabling_factors: list[str] = Field(
        default_factory=list,
        description="Factors that make the task more solvable",
        max_length=20,
        examples=[
            ["web_search", "public_databases", "existing_research"],
            ["computational_power", "machine_learning", "big_data"],
            [
                "international_collaboration",
                "funding_availability",
                "regulatory_support",
            ],
        ],
    )

    breakthrough_requirements: list[str] = Field(
        default_factory=list,
        description="Specific breakthroughs needed to make task solvable",
        max_length=15,
        examples=[
            [],
            ["better_algorithms", "quantum_computing"],
            ["unified_theory_of_quantum_gravity", "room_temperature_superconductors"],
            ["cure_for_aging", "faster_than_light_travel"],
        ],
    )

    estimated_time_to_solvable: timedelta | None = Field(
        default=None,
        description="Estimated time until task becomes solvable (None if never)",
        examples=[timedelta(0), timedelta(days=365), timedelta(days=3650), None],
    )

    alternative_approaches: list[str] = Field(
        default_factory=list,
        description="Possible alternative solution paths",
        max_length=10,
        examples=[
            ["direct_search", "expert_consultation"],
            ["approximation_methods", "heuristic_approaches"],
            ["incremental_progress", "paradigm_shift", "collaborative_breakthrough"],
        ],
    )

    success_probability: float = Field(
        default=0.5,
        description="Estimated probability of eventual success (0.0-1.0)",
        ge=0.0,
        le=1.0,
        examples=[0.95, 0.8, 0.3, 0.05],
    )

    @model_validator(mode="after")
    def validate_solvability_consistency(self) -> "SolvabilityAssessment":
        """Validate that solvability assessment is internally consistent.

        Returns:
            Self if validation passes

        Raises:
            ValueError: If assessment has inconsistencies
        """
        # Check consistency between status and is_currently_solvable
        if (
            self.solvability_status == SolvabilityStatus.READY
            and not self.is_currently_solvable
        ):
            raise ValueError("Status 'ready' requires is_currently_solvable=True")

        if (
            self.solvability_status == SolvabilityStatus.IMPOSSIBLE
            and self.is_currently_solvable
        ):
            raise ValueError(
                "Status 'impossible' cannot have is_currently_solvable=True"
            )

        # Check barriers consistency
        if self.is_currently_solvable and self.primary_barriers:
            raise ValueError(
                "Currently solvable tasks should not have primary barriers"
            )

        if self.solvability_status == SolvabilityStatus.IMPOSSIBLE:
            theoretical_impossibility_present = (
                SolvabilityBarrier.THEORETICAL_IMPOSSIBILITY in self.primary_barriers
            )
            if not theoretical_impossibility_present:
                raise ValueError(
                    "Impossible tasks should have theoretical_impossibility as primary barrier"
                )

        # Check time consistency
        if self.is_currently_solvable and self.estimated_time_to_solvable is not None:
            if self.estimated_time_to_solvable.total_seconds() > 0:
                raise ValueError(
                    "Currently solvable tasks should have time_to_solvable of 0 or None"
                )

        if (
            self.solvability_status == SolvabilityStatus.IMPOSSIBLE
            and self.estimated_time_to_solvable is not None
        ):
            raise ValueError("Impossible tasks should have time_to_solvable=None")

        return self

    def get_solvability_score(self) -> float:
        """Get solvability as a normalized score (0.0-1.0).

        Returns:
            Normalized solvability score
        """
        status_scores = {
            SolvabilityStatus.READY: 1.0,
            SolvabilityStatus.RESEARCHABLE: 0.8,
            SolvabilityStatus.THEORETICAL: 0.6,
            SolvabilityStatus.UNSOLVED: 0.4,
            SolvabilityStatus.IMPOSSIBLE: 0.0,
            SolvabilityStatus.UNDEFINED: 0.5,
        }

        base_score = status_scores[self.solvability_status]

        # Adjust based on barriers
        barrier_penalty = (
            len(self.primary_barriers) * 0.1 + len(self.secondary_barriers) * 0.05
        )
        barrier_penalty = min(0.4, barrier_penalty)  # Cap penalty at 0.4

        # Adjust based on enabling factors
        enabling_bonus = len(self.enabling_factors) * 0.02
        enabling_bonus = min(0.2, enabling_bonus)  # Cap bonus at 0.2

        final_score = base_score - barrier_penalty + enabling_bonus
        return max(0.0, min(1.0, final_score))

    def has_showstopper_barriers(self) -> bool:
        """Check if task has barriers that are absolute showstoppers.

        Returns:
            True if task has insurmountable barriers
        """
        showstoppers = {
            SolvabilityBarrier.THEORETICAL_IMPOSSIBILITY,
            SolvabilityBarrier.SAFETY_RISK,
            SolvabilityBarrier.ETHICAL_CONCERN,
        }

        return any(barrier in showstoppers for barrier in self.primary_barriers)

    def get_addressable_barriers(self) -> list[SolvabilityBarrier]:
        """Get barriers that could potentially be addressed.

        Returns:
            List of barriers that might be overcome
        """
        addressable = {
            SolvabilityBarrier.KNOWLEDGE_GAP,
            SolvabilityBarrier.TECHNOLOGY_LIMITATION,
            SolvabilityBarrier.RESOURCE_CONSTRAINT,
            SolvabilityBarrier.REGULATORY_BARRIER,
            SolvabilityBarrier.COORDINATION_COMPLEXITY,
            SolvabilityBarrier.TIME_CONSTRAINT,
            SolvabilityBarrier.DATA_UNAVAILABILITY,
            SolvabilityBarrier.EXPERT_UNAVAILABILITY,
            SolvabilityBarrier.INFRASTRUCTURE_LIMITATION,
        }

        return [
            barrier
            for barrier in self.primary_barriers + self.secondary_barriers
            if barrier in addressable
        ]

    def estimate_breakthrough_timeline(self) -> dict[str, Any]:
        """Estimate timeline for required breakthroughs.

        Returns:
            Dictionary with breakthrough timeline analysis
        """
        if not self.breakthrough_requirements:
            return {"total_time": timedelta(0), "breakthroughs": []}

        # Rough estimates for different types of breakthroughs
        breakthrough_estimates = {
            "algorithmic": timedelta(days=365),  # 1 year
            "technological": timedelta(days=1095),  # 3 years
            "scientific": timedelta(days=3650),  # 10 years
            "fundamental": timedelta(days=7300),  # 20 years
            "paradigm_shift": timedelta(days=18250),  # 50 years
        }

        breakthrough_analysis = []
        total_time = timedelta(0)

        for requirement in self.breakthrough_requirements:
            req_lower = requirement.lower()

            if any(
                word in req_lower for word in ["algorithm", "software", "computing"]
            ):
                estimate = breakthrough_estimates["algorithmic"]
                category = "algorithmic"
            elif any(
                word in req_lower for word in ["technology", "engineering", "tool"]
            ):
                estimate = breakthrough_estimates["technological"]
                category = "technological"
            elif any(
                word in req_lower for word in ["understanding", "mechanism", "biology"]
            ):
                estimate = breakthrough_estimates["scientific"]
                category = "scientific"
            elif any(
                word in req_lower for word in ["fundamental", "theory", "unified"]
            ):
                estimate = breakthrough_estimates["fundamental"]
                category = "fundamental"
            else:
                estimate = breakthrough_estimates["paradigm_shift"]
                category = "paradigm_shift"

            breakthrough_analysis.append(
                {
                    "requirement": requirement,
                    "category": category,
                    "estimated_time": estimate,
                }
            )

            # Use maximum time for parallel breakthroughs
            total_time = max(total_time, estimate)

        return {
            "total_time": total_time,
            "breakthroughs": breakthrough_analysis,
            "parallel_possible": len(self.breakthrough_requirements) > 1,
        }

    def get_immediate_actions(self) -> list[str]:
        """Get recommended immediate actions to improve solvability.

        Returns:
            List of actionable recommendations
        """
        actions = []

        # Address knowledge gaps
        if SolvabilityBarrier.KNOWLEDGE_GAP in self.primary_barriers:
            actions.append("Conduct comprehensive literature review")
            actions.append("Consult domain experts")
            actions.append("Identify knowledge gaps systematically")

        # Address technology limitations
        if SolvabilityBarrier.TECHNOLOGY_LIMITATION in self.primary_barriers:
            actions.append("Survey current technology landscape")
            actions.append("Explore emerging technologies")
            actions.append("Consider technology development partnerships")

        # Address resource constraints
        if SolvabilityBarrier.RESOURCE_CONSTRAINT in self.primary_barriers:
            actions.append("Develop resource requirements analysis")
            actions.append("Identify potential funding sources")
            actions.append("Explore resource sharing opportunities")

        # Address data availability
        if SolvabilityBarrier.DATA_UNAVAILABILITY in self.primary_barriers:
            actions.append("Map available data sources")
            actions.append("Design data collection strategy")
            actions.append("Consider synthetic or proxy data")

        # Address coordination complexity
        if SolvabilityBarrier.COORDINATION_COMPLEXITY in self.primary_barriers:
            actions.append("Develop coordination framework")
            actions.append("Identify key stakeholders")
            actions.append("Design communication protocols")

        # Leverage enabling factors
        for factor in self.enabling_factors[:3]:  # Top 3 factors
            actions.append(f"Leverage {factor.replace('_', ' ')} capabilities")

        return actions[:10]  # Limit to top 10 actions

    def generate_solvability_report(self) -> str:
        """Generate a comprehensive solvability report.

        Returns:
            Formatted report string
        """
        report_lines = []

        # Header
        report_lines.append("SOLVABILITY ASSESSMENT")
        report_lines.append(f"Status: {self.solvability_status.value.title()}")
        report_lines.append(
            f"Currently Solvable: {'Yes' if self.is_currently_solvable else 'No'}"
        )
        report_lines.append(f"Confidence: {self.confidence_level:.1%}")
        report_lines.append("")

        # Barriers
        if self.primary_barriers:
            report_lines.append("PRIMARY BARRIERS:")
            for barrier in self.primary_barriers:
                report_lines.append(f"  • {barrier.value.replace('_', ' ').title()}")
            report_lines.append("")

        if self.secondary_barriers:
            report_lines.append("SECONDARY BARRIERS:")
            for barrier in self.secondary_barriers:
                report_lines.append(f"  • {barrier.value.replace('_', ' ').title()}")
            report_lines.append("")

        # Enabling factors
        if self.enabling_factors:
            report_lines.append("ENABLING FACTORS:")
            for factor in self.enabling_factors:
                report_lines.append(f"  + {factor.replace('_', ' ').title()}")
            report_lines.append("")

        # Breakthrough requirements
        if self.breakthrough_requirements:
            report_lines.append("BREAKTHROUGH REQUIREMENTS:")
            for requirement in self.breakthrough_requirements:
                report_lines.append(f"  → {requirement.replace('_', ' ').title()}")
            report_lines.append("")

        # Timeline
        if self.estimated_time_to_solvable is not None:
            if self.estimated_time_to_solvable.total_seconds() == 0:
                report_lines.append("Timeline: Immediately solvable")
            else:
                days = self.estimated_time_to_solvable.days
                if days < 30:
                    timeline = f"{days} days"
                elif days < 365:
                    timeline = f"{days // 30} months"
                else:
                    timeline = f"{days // 365} years"
                report_lines.append(f"Estimated Time to Solvable: {timeline}")
        else:
            report_lines.append("Timeline: Never (impossible)")

        report_lines.append("")

        # Success probability
        report_lines.append(f"Success Probability: {self.success_probability:.1%}")

        # Immediate actions
        actions = self.get_immediate_actions()
        if actions:
            report_lines.append("")
            report_lines.append("RECOMMENDED IMMEDIATE ACTIONS:")
            for action in actions[:5]:  # Top 5 actions
                report_lines.append(f"  1. {action}")

        return "\n".join(report_lines)
