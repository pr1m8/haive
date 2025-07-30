"""Models model module.

This module provides models functionality for the Haive framework.

Classes:
    HallucinationType: HallucinationType implementation.
    HallucinationClaim: HallucinationClaim implementation.
    HallucinationDetectionResponse: HallucinationDetectionResponse implementation.
"""

# ============================================================================
# HALLUCINATION DETECTION MODELS
# ============================================================================

from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class HallucinationType(str, Enum):
    """Types of hallucinations detected."""

    FACTUAL = "factual"
    INFERENTIAL = "inferential"
    ATTRIBUTIONAL = "attributional"
    TEMPORAL = "temporal"
    QUANTITATIVE = "quantitative"
    CAUSAL = "causal"


class HallucinationClaim(BaseModel):
    """Individual claim analysis for hallucination detection."""

    claim: str = Field(description="The specific claim being evaluated")
    is_supported: bool = Field(description="Whether the claim is supported by sources")
    support_type: str = Field(
        description="Type of support: explicit, inferred, or unsupported"
    )
    source_reference: str | None = Field(
        default=None, description="Reference to supporting source if available"
    )
    hallucination_type: HallucinationType | None = Field(
        default=None, description="Type of hallucination if detected"
    )
    severity: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Severity of hallucination (0.0 = no hallucination)",
    )


class HallucinationDetectionResponse(BaseModel):
    """Comprehensive hallucination detection response."""

    query: str = Field(description="Original query")
    generated_answer: str = Field(description="The AI-generated answer being evaluated")
    overall_hallucination_score: float = Field(
        ge=0.0,
        le=1.0,
        description="Overall hallucination score (0.0 = no hallucinations)",
    )
    claim_analysis: list[HallucinationClaim] = Field(
        description="Analysis of individual claims"
    )
    supported_claims: list[str] = Field(description="Claims well-supported by sources")
    unsupported_claims: list[str] = Field(description="Claims lacking source support")
    contradictory_claims: list[str] = Field(
        default_factory=list, description="Claims that contradict the sources"
    )
    recommendations: list[str] = Field(
        description="Recommendations for improving answer accuracy"
    )


class HallucinationBinaryResponse(BaseModel):
    """Binary hallucination detection response."""

    query: str = Field(description="Original query")
    generated_answer: str = Field(description="Answer being evaluated")
    hallucination_detected: bool = Field(
        description="Whether hallucination was detected"
    )
    severity_level: Literal["none", "minor", "moderate", "major", "severe"] = Field(
        description="none, minor, moderate, major, or severe"
    )
    justification: str = Field(description="Detailed reasoning for the decision")
    specific_issues: list[str] = Field(
        default_factory=list, description="Specific hallucinated content identified"
    )
