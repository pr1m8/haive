"""Main task analysis model combining all analysis components.

This module provides the comprehensive TaskAnalysis model that combines
complexity assessment, solvability analysis, task decomposition, and
execution strategy recommendations.
"""

from datetime import datetime, timedelta
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from haive.agents.common.models.task_analysis.base import (
    ComplexityType,
    PlanningRequirement,
    TaskComplexity,
    TaskDimension,
)
from haive.agents.common.models.task_analysis.branching import (
    TaskDecomposition,
)
from haive.agents.common.models.task_analysis.solvability import (
    SolvabilityAssessment,
    SolvabilityBarrier,
    SolvabilityStatus,
)


class AnalysisMethod(str, Enum):
    """Methods for analyzing task complexity and requirements.

    Attributes:
        HEURISTIC: Rule-based heuristic analysis
        PATTERN_MATCHING: Pattern matching against known task types
        DECOMPOSITION: Bottom-up analysis through task decomposition
        EXPERT_SYSTEM: Expert system with domain knowledge
        MACHINE_LEARNING: ML-based complexity prediction
        HYBRID: Combination of multiple methods
    """

    HEURISTIC = "heuristic"
    PATTERN_MATCHING = "pattern_matching"
    DECOMPOSITION = "decomposition"
    EXPERT_SYSTEM = "expert_system"
    MACHINE_LEARNING = "machine_learning"
    HYBRID = "hybrid"


class ExecutionStrategy(BaseModel):
    """Recommended execution strategy for a task.

    Provides specific recommendations for how to approach task execution
    based on the complexity and solvability analysis.

    Attributes:
        strategy_type: Primary execution approach
        priority_level: Urgency/priority level for the task
        recommended_approach: Detailed approach description
        resource_allocation: How to allocate resources
        timeline_strategy: How to manage timing and sequencing
        risk_mitigation: Risk mitigation strategies
        success_factors: Key factors for success
        fallback_options: Alternative approaches if primary fails

    Example:
        ```python
        strategy = ExecutionStrategy(
            strategy_type="parallel_execution",
            priority_level="high",
            recommended_approach="Execute independent branches in parallel while managing dependencies",
            resource_allocation={"computational": 0.4, "human_expert": 0.3, "time": 0.3},
            timeline_strategy="front_load_critical_path",
            risk_mitigation=["backup_data_sources", "expert_consultation", "iterative_validation"],
            success_factors=["clear_requirements", "adequate_resources", "expert_oversight"]
        )
        ```
    """

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        str_strip_whitespace=True,
    )

    strategy_type: str = Field(
        ...,
        description="Primary execution approach",
        examples=[
            "sequential_execution",
            "parallel_execution",
            "iterative_research",
            "incremental_approach",
            "breakthrough_research",
            "collaborative_effort",
        ],
    )

    priority_level: str = Field(
        ...,
        description="Urgency/priority level for the task",
        examples=["low", "medium", "high", "critical", "research_priority"],
    )

    recommended_approach: str = Field(
        ...,
        description="Detailed approach description",
        min_length=20,
        max_length=500,
        examples=[
            "Execute independent branches in parallel while carefully managing dependencies",
            "Conduct systematic literature review followed by expert consultation and pilot studies",
            "Break into small incremental steps with validation at each stage",
        ],
    )

    resource_allocation: dict[str, float] = Field(
        ...,
        description="Recommended resource allocation (proportions sum to 1.0)",
        examples=[
            {"computational": 0.4, "human_expert": 0.3, "time": 0.3},
            {"research": 0.5, "development": 0.3, "validation": 0.2},
            {"data_collection": 0.25, "analysis": 0.35, "interpretation": 0.4},
        ],
    )

    timeline_strategy: str = Field(
        ...,
        description="How to manage timing and sequencing",
        examples=[
            "front_load_critical_path",
            "parallel_with_checkpoints",
            "iterative_sprints",
            "milestone_driven",
            "research_then_apply",
            "continuous_development",
        ],
    )

    risk_mitigation: list[str] = Field(
        ...,
        description="Risk mitigation strategies",
        min_length=1,
        max_length=10,
        examples=[
            ["backup_data_sources", "expert_consultation", "iterative_validation"],
            ["redundant_approaches", "early_testing", "stakeholder_engagement"],
            ["contingency_planning", "resource_buffers", "alternative_methods"],
        ],
    )

    success_factors: list[str] = Field(
        ...,
        description="Key factors for success",
        min_length=1,
        max_length=10,
        examples=[
            ["clear_requirements", "adequate_resources", "expert_oversight"],
            ["stakeholder_buy_in", "iterative_feedback", "quality_control"],
            ["breakthrough_insights", "sustained_funding", "collaborative_environment"],
        ],
    )

    fallback_options: list[str] = Field(
        default_factory=list,
        description="Alternative approaches if primary strategy fails",
        max_length=5,
        examples=[
            ["simplified_version", "manual_approach", "external_collaboration"],
            ["incremental_delivery", "proof_of_concept", "literature_review_only"],
            ["theoretical_analysis", "simulation_study", "expert_opinion_synthesis"],
        ],
    )

    @field_validator("resource_allocation")
    @classmethod
    def validate_resource_allocation(cls, v: dict[str, float]) -> dict[str, float]:
        """Validate that resource allocation proportions sum to approximately 1.0.

        Args:
            v: Resource allocation dictionary

        Returns:
            Validated resource allocation

        Raises:
            ValueError: If proportions don't sum to approximately 1.0
        """
        total = sum(v.values())
        if abs(total - 1.0) > 0.1:  # Allow 10% tolerance
            raise ValueError(
                f"Resource allocation proportions must sum to 1.0, got {total:.2f}"
            )

        for resource, proportion in v.items():
            if not 0.0 <= proportion <= 1.0:
                raise ValueError(
                    f"Resource allocation for {resource} must be between 0.0 and 1.0"
                )

        return v


class TaskAnalysis(BaseModel):
    """Comprehensive task analysis combining all analysis components.

    This is the main model that brings together complexity assessment,
    solvability analysis, task decomposition, and execution recommendations
    into a unified analysis.

    Attributes:
        task_description: Original task description
        domain: Task domain or field
        analysis_method: Method used for analysis
        complexity: Complexity assessment
        solvability: Solvability assessment
        decomposition: Task decomposition (optional)
        planning: Planning requirements
        execution_strategy: Recommended execution approach
        analysis_timestamp: When analysis was performed
        analysis_confidence: Overall confidence in the analysis

    Example:
        ```python
        # Analyze a simple research task
        analysis = TaskAnalysis.analyze_task(
            task_description="Find the birthday of the most recent Wimbledon winner",
            domain="sports_research",
            context="Factual lookup requiring web search"
        )

        # Analyze a complex research problem
        analysis = TaskAnalysis.analyze_task(
            task_description="Develop a cure for cancer through novel therapeutic approaches",
            domain="medical_research",
            context="Breakthrough research requiring novel discoveries"
        )

        print(f"Complexity: {analysis.complexity.overall_complexity}")
        print(f"Solvable: {analysis.solvability.is_currently_solvable}")
        print(f"Strategy: {analysis.execution_strategy.strategy_type}")
        ```
    """

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        use_enum_values=True,
        str_strip_whitespace=True,
    )

    task_description: str = Field(
        ...,
        description="Original task description",
        min_length=10,
        max_length=2000,
        examples=[
            "Find the birthday of the most recent Wimbledon winner",
            "Calculate Tom Clancy's birthday + sun's age + feet in mile, then square the result",
            "Develop a cure for cancer through novel therapeutic approaches",
            "Prove or disprove the Riemann Hypothesis",
        ],
    )

    domain: str = Field(
        ...,
        description="Task domain or field",
        examples=[
            "sports_research",
            "mathematical_calculation",
            "medical_research",
            "pure_mathematics",
            "software_engineering",
            "data_analysis",
            "scientific_research",
            "business_intelligence",
            "creative_writing",
        ],
    )

    context: str | None = Field(
        default=None,
        description="Additional context about the task",
        max_length=1000,
        examples=[
            "Factual lookup requiring web search and data verification",
            "Multi-step calculation with arithmetic operations",
            "Breakthrough research requiring novel scientific discoveries",
            "Unsolved mathematical problem requiring proof or disproof",
        ],
    )

    analysis_method: AnalysisMethod = Field(
        default=AnalysisMethod.HYBRID, description="Method used for analysis"
    )

    complexity: TaskComplexity = Field(..., description="Complexity assessment results")

    solvability: SolvabilityAssessment = Field(
        ..., description="Solvability assessment results"
    )

    decomposition: TaskDecomposition | None = Field(
        default=None, description="Task decomposition (if applicable)"
    )

    planning: PlanningRequirement = Field(
        ..., description="Planning requirements and constraints"
    )

    execution_strategy: ExecutionStrategy = Field(
        ..., description="Recommended execution approach"
    )

    analysis_timestamp: datetime = Field(
        default_factory=datetime.now, description="When analysis was performed"
    )

    analysis_confidence: float = Field(
        ...,
        description="Overall confidence in the analysis (0.0-1.0)",
        ge=0.0,
        le=1.0,
        examples=[0.95, 0.8, 0.6, 0.3],
    )

    @model_validator(mode="after")
    def validate_analysis_consistency(self) -> "TaskAnalysis":
        """Validate that all analysis components are consistent.

        Returns:
            Self if validation passes

        Raises:
            ValueError: If analysis components are inconsistent
        """
        # Check complexity-solvability consistency
        if (
            self.complexity.overall_complexity == ComplexityType.TRIVIAL
            and not self.solvability.is_currently_solvable
        ):
            raise ValueError("Trivial complexity should be currently solvable")

        if (
            self.complexity.overall_complexity == ComplexityType.UNSOLVABLE
            and self.solvability.solvability_status != SolvabilityStatus.IMPOSSIBLE
        ):
            raise ValueError(
                "Unsolvable complexity should have impossible solvability status"
            )

        # Check decomposition consistency
        if self.decomposition:
            if (
                self.complexity.overall_complexity == ComplexityType.TRIVIAL
                and len(self.decomposition.branches) > 3
            ):
                raise ValueError("Trivial tasks should not have complex decomposition")

        # Check confidence consistency
        avg_confidence = (
            self.complexity.confidence + self.solvability.confidence_level
        ) / 2
        if abs(self.analysis_confidence - avg_confidence) > 0.3:
            raise ValueError(
                "Overall confidence should be consistent with component confidences"
            )

        return self

    def get_overall_assessment(self) -> dict[str, Any]:
        """Get overall assessment summary.

        Returns:
            Dictionary with key assessment metrics
        """
        return {
            "complexity_level": self.complexity.overall_complexity.value,
            "complexity_score": self.complexity.get_complexity_score(),
            "solvability_status": self.solvability.solvability_status.value,
            "solvability_score": self.solvability.get_solvability_score(),
            "is_ready_to_execute": self.solvability.is_currently_solvable,
            "estimated_effort": self.complexity.estimated_steps,
            "dominant_complexity_dimensions": self.complexity.get_dominant_dimensions(),
            "primary_barriers": [b.value for b in self.solvability.primary_barriers],
            "strategy_type": self.execution_strategy.strategy_type,
            "analysis_confidence": self.analysis_confidence,
        }

    def generate_executive_summary(self) -> str:
        """Generate an executive summary of the analysis.

        Returns:
            Formatted executive summary
        """
        summary_lines = []

        # Header
        summary_lines.append("TASK ANALYSIS EXECUTIVE SUMMARY")
        summary_lines.append("=" * 40)
        summary_lines.append("")

        # Task info
        summary_lines.append(f"Task: {self.task_description[:80]}...")
        summary_lines.append(f"Domain: {self.domain.replace('_', ' ').title()}")
        summary_lines.append("")

        # Key findings
        summary_lines.append("KEY FINDINGS:")
        summary_lines.append(
            f"• Complexity: {self.complexity.overall_complexity.value.title()}"
        )
        summary_lines.append(
            f"• Solvability: {self.solvability.solvability_status.value.title()}"
        )
        summary_lines.append(
            f"• Ready to Execute: {'Yes' if self.solvability.is_currently_solvable else 'No'}"
        )
        summary_lines.append(f"• Estimated Steps: {self.complexity.estimated_steps}")

        if self.decomposition:
            summary_lines.append(
                f"• Execution Branches: {len(self.decomposition.branches)}"
            )

        summary_lines.append("")

        # Strategy
        summary_lines.append("RECOMMENDED STRATEGY:")
        summary_lines.append(
            f"• Approach: {self.execution_strategy.strategy_type.replace('_', ' ').title()}"
        )
        summary_lines.append(
            f"• Priority: {self.execution_strategy.priority_level.title()}"
        )
        summary_lines.append(
            f"• Timeline: {self.execution_strategy.timeline_strategy.replace('_', ' ').title()}"
        )
        summary_lines.append("")

        # Barriers and enablers
        if self.solvability.primary_barriers:
            summary_lines.append("PRIMARY BARRIERS:")
            for barrier in self.solvability.primary_barriers[:3]:
                summary_lines.append(f"• {barrier.value.replace('_', ' ').title()}")
            summary_lines.append("")

        if self.solvability.enabling_factors:
            summary_lines.append("ENABLING FACTORS:")
            for factor in self.solvability.enabling_factors[:3]:
                summary_lines.append(f"• {factor.replace('_', ' ').title()}")
            summary_lines.append("")

        # Confidence
        summary_lines.append(f"Analysis Confidence: {self.analysis_confidence:.1%}")

        return "\n".join(summary_lines)

    def get_execution_recommendations(self) -> list[str]:
        """Get prioritized execution recommendations.

        Returns:
            List of actionable recommendations
        """
        recommendations = []

        # Immediate readiness recommendations
        if self.solvability.is_currently_solvable:
            recommendations.append("Task is ready for immediate execution")
            recommendations.extend(self.execution_strategy.success_factors[:2])
        else:
            recommendations.extend(self.solvability.get_immediate_actions()[:3])

        # Complexity-based recommendations
        if self.complexity.overall_complexity in [
            ComplexityType.COMPLEX,
            ComplexityType.HIGHLY_COMPLEX,
        ]:
            recommendations.append("Break task into smaller, manageable subtasks")
            recommendations.append("Establish clear milestones and checkpoints")

        if self.complexity.requires_expertise():
            recommendations.append("Engage domain experts early in the process")

        if self.complexity.requires_research():
            recommendations.append(
                "Allocate significant time for research and discovery"
            )

        # Decomposition-based recommendations
        if self.decomposition:
            if len(self.decomposition.parallelization_opportunities) > 0:
                recommendations.append("Leverage parallel execution opportunities")

            if self.decomposition.bottlenecks:
                recommendations.append("Address identified bottlenecks proactively")

        # Risk mitigation
        recommendations.extend(self.execution_strategy.risk_mitigation[:2])

        return recommendations[:10]  # Limit to top 10

    @classmethod
    def analyze_task(
        cls,
        task_description: str,
        domain: str | None = None,
        context: str | None = None,
        analysis_method: AnalysisMethod = AnalysisMethod.HYBRID,
    ) -> "TaskAnalysis":
        """Analyze a task and return comprehensive analysis.

        This is the main entry point for task analysis. It performs
        heuristic analysis based on task characteristics.

        Args:
            task_description: Description of the task to analyze
            domain: Optional domain specification
            context: Optional additional context
            analysis_method: Method to use for analysis

        Returns:
            Complete TaskAnalysis instance
        """
        # Infer domain if not provided
        if domain is None:
            domain = cls._infer_domain(task_description)

        # Perform complexity analysis
        complexity = cls._analyze_complexity(task_description, domain, context)

        # Perform solvability analysis
        solvability = cls._analyze_solvability(task_description, domain, complexity)

        # Generate planning requirements
        planning = cls._generate_planning_requirements(complexity, solvability)

        # Generate execution strategy
        execution_strategy = cls._generate_execution_strategy(
            complexity, solvability, planning
        )

        # Generate decomposition if appropriate
        decomposition = None
        if complexity.overall_complexity not in [
            ComplexityType.TRIVIAL,
            ComplexityType.SIMPLE,
        ]:
            decomposition = cls._generate_decomposition(task_description, complexity)

        # Calculate overall confidence
        analysis_confidence = (complexity.confidence + solvability.confidence_level) / 2

        return cls(
            task_description=task_description,
            domain=domain,
            context=context,
            analysis_method=analysis_method,
            complexity=complexity,
            solvability=solvability,
            decomposition=decomposition,
            planning=planning,
            execution_strategy=execution_strategy,
            analysis_confidence=analysis_confidence,
        )

    @classmethod
    def _infer_domain(cls, task_description: str) -> str:
        """Infer task domain from description."""
        text_lower = task_description.lower()

        # Domain keywords mapping
        domain_keywords = {
            "medical_research": [
                "cancer",
                "cure",
                "disease",
                "medicine",
                "therapy",
                "clinical",
            ],
            "mathematics": [
                "prove",
                "theorem",
                "equation",
                "calculate",
                "formula",
                "hypothesis",
            ],
            "sports_research": [
                "wimbledon",
                "championship",
                "tournament",
                "sports",
                "athlete",
            ],
            "scientific_research": [
                "research",
                "study",
                "experiment",
                "analysis",
                "investigation",
            ],
            "data_analysis": ["data", "statistics", "analyze", "dataset", "metrics"],
            "software_engineering": [
                "code",
                "program",
                "software",
                "application",
                "system",
            ],
            "factual_lookup": [
                "find",
                "birthday",
                "age",
                "when",
                "who",
                "what",
                "where",
            ],
            "mathematical_calculation": [
                "add",
                "multiply",
                "square",
                "sum",
                "calculate",
            ],
        }

        # Score each domain
        domain_scores = {}
        for domain, keywords in domain_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                domain_scores[domain] = score

        # Return highest scoring domain or default
        if domain_scores:
            return max(domain_scores.items(), key=lambda x: x[1])[0]
        return "general"

    @classmethod
    def _analyze_complexity(
        cls, task_description: str, domain: str, context: str | None
    ) -> TaskComplexity:
        """Analyze task complexity using heuristics."""
        text_lower = task_description.lower()

        # Complexity indicators
        simple_indicators = [
            "find",
            "lookup",
            "what is",
            "birthday",
            "age",
            "calculate",
            "add",
        ]
        complex_indicators = [
            "develop",
            "create",
            "cure",
            "solve",
            "prove",
            "design",
            "build",
        ]
        research_indicators = [
            "novel",
            "breakthrough",
            "new",
            "innovative",
            "research",
            "discover",
        ]
        impossible_indicators = [
            "impossible",
            "violate",
            "faster than light",
            "perpetual motion",
        ]

        # Calculate base complexity scores
        simple_score = sum(
            1 for indicator in simple_indicators if indicator in text_lower
        )
        complex_score = sum(
            1 for indicator in complex_indicators if indicator in text_lower
        )
        research_score = sum(
            1 for indicator in research_indicators if indicator in text_lower
        )
        impossible_score = sum(
            1 for indicator in impossible_indicators if indicator in text_lower
        )

        # Determine overall complexity
        if impossible_score > 0:
            overall_complexity = ComplexityType.UNSOLVABLE
        elif research_score > 1 or "cure cancer" in text_lower:
            overall_complexity = ComplexityType.BREAKTHROUGH
        elif research_score > 0 or complex_score > 2:
            overall_complexity = ComplexityType.RESEARCH_GRADE
        elif complex_score > 0:
            overall_complexity = ComplexityType.COMPLEX
        elif simple_score > 0:
            overall_complexity = ComplexityType.SIMPLE
        else:
            overall_complexity = ComplexityType.MODERATE

        # Calculate dimension scores
        dimension_scores = {
            TaskDimension.DEPTH: min(1.0, (complex_score + research_score) * 0.2),
            TaskDimension.BREADTH: min(1.0, len(text_lower.split()) * 0.01),
            TaskDimension.KNOWLEDGE: min(1.0, (complex_score + research_score) * 0.25),
            TaskDimension.RESEARCH: min(1.0, research_score * 0.4),
            TaskDimension.COORDINATION: min(1.0, complex_score * 0.15),
            TaskDimension.TEMPORAL: 0.3,  # Default moderate
            TaskDimension.UNCERTAINTY: min(1.0, research_score * 0.3),
            TaskDimension.RESOURCE: min(1.0, (complex_score + research_score) * 0.2),
        }

        # Estimate parameters
        if overall_complexity == ComplexityType.SIMPLE:
            depth_levels = 2
            branch_count = 1
            estimated_steps = 3
        elif overall_complexity == ComplexityType.MODERATE:
            depth_levels = 3
            branch_count = 2
            estimated_steps = 8
        elif overall_complexity == ComplexityType.COMPLEX:
            depth_levels = 5
            branch_count = 4
            estimated_steps = 25
        elif overall_complexity == ComplexityType.RESEARCH_GRADE:
            depth_levels = 8
            branch_count = 10
            estimated_steps = 100
        elif overall_complexity == ComplexityType.BREAKTHROUGH:
            depth_levels = 12
            branch_count = 20
            estimated_steps = 500
        else:  # UNSOLVABLE
            depth_levels = 15
            branch_count = 50
            estimated_steps = 1000

        return TaskComplexity(
            overall_complexity=overall_complexity,
            dimension_scores=dimension_scores,
            depth_levels=depth_levels,
            branch_count=branch_count,
            estimated_steps=estimated_steps,
            confidence=0.8,
        )

    @classmethod
    def _analyze_solvability(
        cls, task_description: str, domain: str, complexity: TaskComplexity
    ) -> SolvabilityAssessment:
        """Analyze task solvability."""
        text_lower = task_description.lower()

        # Determine base solvability
        if complexity.overall_complexity == ComplexityType.UNSOLVABLE:
            solvability_status = SolvabilityStatus.IMPOSSIBLE
            is_currently_solvable = False
            primary_barriers = [SolvabilityBarrier.THEORETICAL_IMPOSSIBILITY]
        elif complexity.overall_complexity == ComplexityType.BREAKTHROUGH:
            solvability_status = SolvabilityStatus.THEORETICAL
            is_currently_solvable = False
            primary_barriers = [
                SolvabilityBarrier.KNOWLEDGE_GAP,
                SolvabilityBarrier.TECHNOLOGY_LIMITATION,
            ]
        elif complexity.overall_complexity == ComplexityType.RESEARCH_GRADE:
            solvability_status = SolvabilityStatus.RESEARCHABLE
            is_currently_solvable = False
            primary_barriers = [SolvabilityBarrier.KNOWLEDGE_GAP]
        elif complexity.overall_complexity in [
            ComplexityType.SIMPLE,
            ComplexityType.TRIVIAL,
        ]:
            solvability_status = SolvabilityStatus.READY
            is_currently_solvable = True
            primary_barriers = []
        else:
            solvability_status = SolvabilityStatus.READY
            is_currently_solvable = True
            primary_barriers = []

        # Identify enabling factors
        enabling_factors = []
        if "find" in text_lower or "lookup" in text_lower:
            enabling_factors.extend(["web_search", "databases", "public_information"])
        if "calculate" in text_lower:
            enabling_factors.extend(["computational_tools", "mathematical_knowledge"])
        if "research" in text_lower:
            enabling_factors.extend(
                ["academic_literature", "research_methods", "expert_knowledge"]
            )

        # Estimate time to solvable
        if is_currently_solvable:
            time_to_solvable = timedelta(0)
        elif solvability_status == SolvabilityStatus.RESEARCHABLE:
            time_to_solvable = timedelta(days=365)
        elif solvability_status == SolvabilityStatus.THEORETICAL:
            time_to_solvable = timedelta(days=3650)  # 10 years
        else:
            time_to_solvable = None

        return SolvabilityAssessment(
            solvability_status=solvability_status,
            is_currently_solvable=is_currently_solvable,
            confidence_level=0.8,
            primary_barriers=primary_barriers,
            enabling_factors=enabling_factors,
            estimated_time_to_solvable=time_to_solvable,
            success_probability=0.9 if is_currently_solvable else 0.3,
        )

    @classmethod
    def _generate_planning_requirements(
        cls, complexity: TaskComplexity, solvability: SolvabilityAssessment
    ) -> PlanningRequirement:
        """Generate planning requirements based on complexity and solvability."""
        if complexity.overall_complexity == ComplexityType.TRIVIAL:
            planning_depth = "minimal"
        elif complexity.overall_complexity == ComplexityType.SIMPLE:
            planning_depth = "basic"
        elif complexity.overall_complexity == ComplexityType.MODERATE:
            planning_depth = "detailed"
        elif complexity.overall_complexity == ComplexityType.COMPLEX:
            planning_depth = "comprehensive"
        else:
            planning_depth = "strategic"

        return PlanningRequirement(
            planning_depth=planning_depth,
            coordination_needs=["multi_agent"] if complexity.branch_count > 3 else [],
            resource_requirements=(
                ["computational", "domain_expert"]
                if complexity.requires_expertise()
                else ["computational"]
            ),
            time_constraints={"real_time": False},
            risk_factors=(
                ["complexity"]
                if complexity.overall_complexity.value in ["complex", "highly_complex"]
                else []
            ),
        )

    @classmethod
    def _generate_execution_strategy(
        cls,
        complexity: TaskComplexity,
        solvability: SolvabilityAssessment,
        planning: PlanningRequirement,
    ) -> ExecutionStrategy:
        """Generate execution strategy."""
        if not solvability.is_currently_solvable:
            strategy_type = "research_approach"
            priority_level = "research_priority"
        elif complexity.branch_count > 3:
            strategy_type = "parallel_execution"
            priority_level = "high"
        else:
            strategy_type = "sequential_execution"
            priority_level = "medium"

        return ExecutionStrategy(
            strategy_type=strategy_type,
            priority_level=priority_level,
            recommended_approach="Execute based on complexity and solvability analysis",
            resource_allocation={"computational": 0.4, "human": 0.3, "time": 0.3},
            timeline_strategy="milestone_driven",
            risk_mitigation=["iterative_validation", "expert_consultation"],
            success_factors=["clear_requirements", "adequate_resources"],
        )

    @classmethod
    def _generate_decomposition(
        cls, task_description: str, complexity: TaskComplexity
    ) -> TaskDecomposition | None:
        """Generate basic task decomposition."""
        if complexity.overall_complexity in [
            ComplexityType.TRIVIAL,
            ComplexityType.SIMPLE,
        ]:
            return None

        # Create simple sequential decomposition based on complexity
        branch_descriptions = [
            "Initial analysis and planning",
            "Core execution phase",
            "Validation and refinement",
            "Final integration and delivery",
        ]

        return TaskDecomposition.create_simple_sequential(
            task_description=task_description,
            branch_descriptions=branch_descriptions[: complexity.branch_count],
        )
