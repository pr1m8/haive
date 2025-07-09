# src/haive/agents/reasoning/models.py

from datetime import datetime
from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, Field, computed_field

# ============================================================================
# ENUMS - Fundamental Reasoning Categories
# ============================================================================


class ReasoningType(str, Enum):
    """Fundamental patterns of reasoning.

    These represent core ways humans and AI systems process information:
    - DEDUCTIVE: From general principles to specific conclusions
    - INDUCTIVE: From specific observations to general principles
    - ABDUCTIVE: Best explanation for observations
    - ANALOGICAL: Reasoning by comparison/similarity
    - CAUSAL: Understanding cause-effect relationships
    - PROBABILISTIC: Reasoning under uncertainty
    - COUNTERFACTUAL: What-if analysis
    - DIALECTICAL: Thesis-antithesis-synthesis
    """

    DEDUCTIVE = "deductive"
    INDUCTIVE = "inductive"
    ABDUCTIVE = "abductive"
    ANALOGICAL = "analogical"
    CAUSAL = "causal"
    PROBABILISTIC = "probabilistic"
    COUNTERFACTUAL = "counterfactual"
    DIALECTICAL = "dialectical"


class EvidenceType(str, Enum):
    """Types of evidence that support reasoning."""

    EMPIRICAL = "empirical"  # Observable data
    STATISTICAL = "statistical"  # Numerical/quantitative
    TESTIMONIAL = "testimonial"  # Expert opinions
    DOCUMENTARY = "documentary"  # Written records
    LOGICAL = "logical"  # Formal proofs
    EXPERIENTIAL = "experiential"  # Personal experience
    THEORETICAL = "theoretical"  # Models/frameworks
    ANALOGICAL = "analogical"  # Similar cases


class ArgumentStrength(str, Enum):
    """Strength of logical arguments."""

    CONCLUSIVE = "conclusive"  # Logically certain
    VERY_STRONG = "very_strong"  # Highly compelling
    STRONG = "strong"  # Good support
    MODERATE = "moderate"  # Reasonable support
    WEAK = "weak"  # Limited support
    VERY_WEAK = "very_weak"  # Minimal support
    FALLACIOUS = "fallacious"  # Contains logical errors


class CertaintyLevel(str, Enum):
    """Degree of certainty in conclusions."""

    CERTAIN = "certain"  # 100% confidence
    HIGHLY_LIKELY = "highly_likely"  # 90-99%
    LIKELY = "likely"  # 70-89%
    POSSIBLE = "possible"  # 40-69%
    UNLIKELY = "unlikely"  # 10-39%
    HIGHLY_UNLIKELY = "highly_unlikely"  # 1-9%
    IMPOSSIBLE = "impossible"  # 0%


class BiasType(str, Enum):
    """Common cognitive biases that affect reasoning."""

    CONFIRMATION = "confirmation"  # Seeking confirming evidence
    ANCHORING = "anchoring"  # Over-relying on first info
    AVAILABILITY = "availability"  # Overweighting recent/memorable
    HINDSIGHT = "hindsight"  # "I knew it all along"
    DUNNING_KRUGER = "dunning_kruger"  # Overconfidence from ignorance
    SUNK_COST = "sunk_cost"  # Past investment bias
    FRAMING = "framing"  # Presentation affects judgment
    SELECTION = "selection"  # Cherry-picking data


class LogicalFallacy(str, Enum):
    """Common logical fallacies to detect."""

    AD_HOMINEM = "ad_hominem"
    STRAW_MAN = "straw_man"
    FALSE_DILEMMA = "false_dilemma"
    SLIPPERY_SLOPE = "slippery_slope"
    CIRCULAR_REASONING = "circular_reasoning"
    APPEAL_TO_AUTHORITY = "appeal_to_authority"
    HASTY_GENERALIZATION = "hasty_generalization"
    POST_HOC = "post_hoc"
    FALSE_CAUSE = "false_cause"
    BANDWAGON = "bandwagon"


# ============================================================================
# CORE MODELS - Reasoning Components
# ============================================================================


class Premise(BaseModel):
    """A single premise in a logical argument."""

    statement: str = Field(description="The premise statement")
    premise_type: Literal["fact", "assumption", "axiom", "hypothesis"] = Field(
        description="Type of premise"
    )
    evidence: list["Evidence"] = Field(
        default_factory=list, description="Supporting evidence for this premise"
    )
    certainty: CertaintyLevel = Field(
        description="How certain we are about this premise"
    )
    source: str | None = Field(default=None, description="Source of this premise")
    is_contested: bool = Field(
        default=False, description="Whether this premise is disputed"
    )


class Evidence(BaseModel):
    """Evidence supporting a claim or premise."""

    evidence_type: EvidenceType
    description: str = Field(description="Description of the evidence")
    source: str = Field(description="Where this evidence comes from")
    strength: ArgumentStrength = Field(
        description="How strongly this supports the claim"
    )
    reliability: float = Field(
        ge=0.0, le=1.0, description="Reliability of the source (0-1)"
    )
    relevance: float = Field(ge=0.0, le=1.0, description="Relevance to the claim (0-1)")
    date_collected: datetime | None = None
    limitations: list[str] = Field(
        default_factory=list, description="Known limitations of this evidence"
    )


class LogicalStep(BaseModel):
    """A single step in a reasoning chain."""

    step_number: int = Field(description="Order in the reasoning chain")
    reasoning_type: ReasoningType = Field(description="Type of reasoning used")
    from_premises: list[int] = Field(description="Indices of premises used")
    inference_rule: str = Field(description="Logical rule applied (e.g., modus ponens)")
    conclusion: str = Field(description="What we conclude from this step")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence in this step")
    alternative_conclusions: list[str] = Field(
        default_factory=list, description="Other possible conclusions"
    )


class Assumption(BaseModel):
    """An assumption made during reasoning."""

    statement: str = Field(description="The assumption being made")
    justification: str = Field(description="Why we're making this assumption")
    impact: Literal["critical", "significant", "moderate", "minor"] = Field(
        description="Impact if assumption is wrong"
    )
    testable: bool = Field(default=True, description="Whether this can be verified")
    alternatives: list[str] = Field(
        default_factory=list, description="Alternative assumptions possible"
    )


class CounterArgument(BaseModel):
    """A counter-argument to consider."""

    argument: str = Field(description="The counter-argument")
    strength: ArgumentStrength = Field(description="Strength of this counter-argument")
    rebuttal: str | None = Field(
        default=None, description="Our response to this counter-argument"
    )
    unresolved: bool = Field(
        default=False, description="Whether this remains unaddressed"
    )


class ReasoningChain(BaseModel):
    """A complete chain of reasoning from premises to conclusion."""

    # Identity
    chain_id: str = Field(description="Unique identifier")
    question: str = Field(description="What we're trying to answer")
    context: dict[str, Any] = Field(
        default_factory=dict, description="Relevant context"
    )

    # Components
    premises: list[Premise] = Field(description="Starting premises")
    assumptions: list[Assumption] = Field(
        default_factory=list, description="Assumptions made"
    )
    logical_steps: list[LogicalStep] = Field(
        description="Steps from premises to conclusion"
    )

    # Conclusion
    conclusion: str = Field(description="Final conclusion reached")
    conclusion_strength: ArgumentStrength = Field(
        description="How strong the argument is"
    )
    certainty_level: CertaintyLevel = Field(description="How certain we are")

    # Alternative paths
    alternative_conclusions: list[dict[str, Any]] = Field(
        default_factory=list, description="Other possible conclusions"
    )
    counter_arguments: list[CounterArgument] = Field(
        default_factory=list, description="Arguments against our conclusion"
    )

    # Quality metrics
    logical_validity: bool = Field(description="Whether reasoning is logically valid")
    soundness: bool | None = Field(
        default=None, description="Valid + true premises (if verifiable)"
    )
    completeness: float = Field(
        ge=0.0, le=1.0, description="How thoroughly we've reasoned"
    )

    @computed_field
    @property
    def num_steps(self) -> int:
        """Number of reasoning steps."""
        return len(self.logical_steps)

    @computed_field
    @property
    def max_inference_chain(self) -> int:
        """Longest chain of inferences."""
        if not self.logical_steps:
            return 0
        return max(step.step_number for step in self.logical_steps)


# ============================================================================
# ANALYSIS MODELS - Reasoning Analysis Results
# ============================================================================


class BiasAssessment(BaseModel):
    """Assessment of potential biases."""

    bias_type: BiasType
    description: str = Field(description="How this bias might be affecting reasoning")
    severity: Literal["high", "medium", "low"] = Field(
        description="How severely this affects conclusions"
    )
    evidence: list[str] = Field(description="Evidence of this bias")
    mitigation: str = Field(description="How to counteract this bias")


class FallacyDetection(BaseModel):
    """Detection of logical fallacies."""

    fallacy_type: LogicalFallacy
    location: str = Field(description="Where in reasoning this occurs")
    description: str = Field(description="How this fallacy manifests")
    impact: ArgumentStrength = Field(description="How much this weakens the argument")
    correction: str = Field(description="How to fix this fallacy")


class UncertaintyAnalysis(BaseModel):
    """Analysis of uncertainty in reasoning."""

    # Sources of uncertainty
    epistemic_uncertainty: float = Field(
        ge=0.0, le=1.0, description="Uncertainty from lack of knowledge"
    )
    aleatory_uncertainty: float = Field(
        ge=0.0, le=1.0, description="Inherent randomness/variability"
    )

    # Specific uncertainties
    premise_uncertainty: dict[int, float] = Field(
        description="Uncertainty in each premise"
    )
    inference_uncertainty: dict[int, float] = Field(
        description="Uncertainty in each inference"
    )

    # Propagated uncertainty
    conclusion_uncertainty: float = Field(
        ge=0.0, le=1.0, description="Total uncertainty in conclusion"
    )
    confidence_interval: tuple[float, float] = Field(
        description="Confidence interval for conclusion"
    )

    # Sensitivity
    sensitive_assumptions: list[str] = Field(
        description="Assumptions that most affect conclusion"
    )
    robustness_score: float = Field(
        ge=0.0, le=1.0, description="How robust conclusion is to uncertainties"
    )


class ArgumentStructure(BaseModel):
    """Structure analysis of an argument."""

    # Argument type
    structure_type: Literal[
        "deductive", "inductive", "abductive", "analogical", "pragmatic", "mixed"
    ] = Field(description="Overall structure type")

    # Complexity metrics
    depth: int = Field(description="Maximum inference depth")
    breadth: int = Field(description="Number of parallel reasoning paths")
    premise_count: int = Field(description="Total number of premises")

    # Dependencies
    premise_dependencies: dict[str, list[str]] = Field(
        description="Which conclusions depend on which premises"
    )
    critical_premises: list[int] = Field(
        description="Premises that support the most conclusions"
    )

    # Patterns
    reasoning_patterns: list[str] = Field(description="Common patterns identified")
    circular_dependencies: list[list[int]] = Field(
        default_factory=list, description="Any circular reasoning detected"
    )


class ReasoningQuality(BaseModel):
    """Overall quality assessment of reasoning."""

    # Logical quality
    validity_score: float = Field(
        ge=0.0, le=1.0, description="Logical validity (structure)"
    )
    soundness_score: float = Field(
        ge=0.0, le=1.0, description="Soundness (validity + truth)"
    )

    # Evidence quality
    evidence_quality: float = Field(
        ge=0.0, le=1.0, description="Quality of supporting evidence"
    )
    evidence_coverage: float = Field(
        ge=0.0, le=1.0, description="How well evidence covers claims"
    )

    # Completeness
    consideration_breadth: float = Field(
        ge=0.0, le=1.0, description="Breadth of factors considered"
    )
    alternative_exploration: float = Field(
        ge=0.0, le=1.0, description="How well alternatives were explored"
    )

    # Bias and fallacies
    bias_score: float = Field(
        ge=0.0, le=1.0, description="Freedom from bias (1 = unbiased)"
    )
    fallacy_score: float = Field(
        ge=0.0, le=1.0, description="Freedom from fallacies (1 = none)"
    )

    # Overall
    overall_quality: float = Field(
        ge=0.0, le=1.0, description="Weighted overall quality"
    )
    confidence_in_assessment: float = Field(
        ge=0.0, le=1.0, description="Our confidence in this assessment"
    )


class ReasoningAnalysis(BaseModel):
    """Complete analysis of a reasoning chain."""

    # Original reasoning
    reasoning_chain: ReasoningChain = Field(description="The reasoning being analyzed")

    # Structural analysis
    argument_structure: ArgumentStructure = Field(
        description="Structure of the argument"
    )

    # Quality assessment
    quality_assessment: ReasoningQuality = Field(description="Quality metrics")

    # Bias and fallacy detection
    detected_biases: list[BiasAssessment] = Field(
        default_factory=list, description="Potential biases found"
    )
    detected_fallacies: list[FallacyDetection] = Field(
        default_factory=list, description="Logical fallacies found"
    )

    # Uncertainty
    uncertainty_analysis: UncertaintyAnalysis = Field(
        description="Analysis of uncertainties"
    )

    # Improvements
    strengthening_suggestions: list[str] = Field(
        description="How to strengthen the argument"
    )
    missing_considerations: list[str] = Field(
        description="Important factors not considered"
    )
    additional_evidence_needed: list[str] = Field(
        description="Evidence that would help"
    )

    # Alternative perspectives
    alternative_framings: list[dict[str, Any]] = Field(
        description="Other ways to approach the question"
    )
    dialectical_synthesis: str | None = Field(
        default=None, description="Synthesis of opposing views"
    )


class ReasoningReport(BaseModel):
    """Comprehensive reasoning analysis report."""

    # Context
    question: str = Field(description="Original question")
    context: dict[str, Any] = Field(description="Provided context")
    timestamp: datetime = Field(default_factory=datetime.now)

    # Primary reasoning
    primary_chain: ReasoningChain = Field(description="Main line of reasoning")

    # Analysis
    analysis: ReasoningAnalysis = Field(description="Detailed analysis")

    # Alternative approaches
    alternative_chains: list[ReasoningChain] = Field(
        default_factory=list, description="Alternative reasoning paths"
    )

    # Synthesis
    synthesized_conclusion: str = Field(
        description="Conclusion considering all perspectives"
    )
    confidence_level: CertaintyLevel = Field(description="Overall confidence")

    # Recommendations
    decision_recommendation: str = Field(
        description="What we recommend based on reasoning"
    )
    key_uncertainties: list[str] = Field(description="Main uncertainties to track")
    follow_up_questions: list[str] = Field(
        description="Questions that would improve reasoning"
    )

    # Executive summary
    executive_summary: str = Field(description="Brief summary for decision-makers")
    key_insights: list[str] = Field(description="Most important insights")
