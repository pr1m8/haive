"""Comprehensive Document Grading System.

Advanced document relevance, quality, and hallucination detection for RAG systems.
"""

from enum import Enum

from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field


class DocumentRelevanceLevel(str, Enum):
    """Document relevance levels."""

    HIGHLY_RELEVANT = "highly_relevant"  # Directly answers query
    RELEVANT = "relevant"  # Contains useful information
    PARTIALLY_RELEVANT = "partially_relevant"  # Some relevant info
    MARGINALLY_RELEVANT = "marginally_relevant"  # Minimal relevance
    NOT_RELEVANT = "not_relevant"  # No relevance


class DocumentQualityLevel(str, Enum):
    """Document quality levels."""

    EXCELLENT = "excellent"  # Authoritative, comprehensive
    GOOD = "good"  # Solid information, minor gaps
    FAIR = "fair"  # Basic information, some issues
    POOR = "poor"  # Limited value, quality concerns
    UNRELIABLE = "unreliable"  # Questionable accuracy


class HallucinationRisk(str, Enum):
    """Hallucination risk levels."""

    VERY_LOW = "very_low"  # Factual, verifiable content
    LOW = "low"  # Mostly factual with minor gaps
    MODERATE = "moderate"  # Some unsupported claims
    HIGH = "high"  # Multiple unsupported claims
    VERY_HIGH = "very_high"  # Likely contains misinformation


class ComprehensiveDocumentGrade(BaseModel):
    """Comprehensive document assessment."""

    document_id: str = Field(description="Unique document identifier")

    # Relevance Assessment
    relevance_level: DocumentRelevanceLevel = Field(description="Relevance to query")
    relevance_score: float = Field(ge=0.0, le=1.0, description="Relevance score 0-1")
    relevance_justification: str = Field(description="Why this relevance level")

    # Quality Assessment
    quality_level: DocumentQualityLevel = Field(description="Information quality")
    quality_score: float = Field(ge=0.0, le=1.0, description="Quality score 0-1")
    quality_justification: str = Field(description="Quality assessment reasoning")

    # Hallucination Risk Assessment
    hallucination_risk: HallucinationRisk = Field(description="Risk of hallucination")
    hallucination_score: float = Field(
        ge=0.0, le=1.0, description="Hallucination risk 0-1"
    )
    hallucination_justification: str = Field(description="Hallucination risk reasoning")

    # Content Analysis
    key_facts: list[str] = Field(default_factory=list, description="Verifiable facts")
    potential_issues: list[str] = Field(
        default_factory=list, description="Quality/accuracy concerns"
    )
    supporting_evidence: list[str] = Field(
        default_factory=list, description="Evidence quality indicators"
    )

    # Overall Assessment
    overall_score: float = Field(ge=0.0, le=1.0, description="Weighted overall score")
    recommendation: str = Field(description="Usage recommendation")

    # Metadata
    processing_notes: list[str] = Field(
        default_factory=list, description="Processing observations"
    )


class ComprehensiveGradingResponse(BaseModel):
    """Response for comprehensive document grading."""

    query: str = Field(description="Original query")
    total_documents: int = Field(description="Number of documents graded")

    # Individual grades
    document_grades: list[ComprehensiveDocumentGrade] = Field(
        description="Individual document assessments"
    )

    # Aggregate Analysis
    average_relevance: float = Field(
        ge=0.0, le=1.0, description="Average relevance score"
    )
    average_quality: float = Field(ge=0.0, le=1.0, description="Average quality score")
    average_hallucination_risk: float = Field(
        ge=0.0, le=1.0, description="Average hallucination risk"
    )

    # Recommendations
    recommended_documents: list[str] = Field(description="IDs of recommended documents")
    flagged_documents: list[str] = Field(description="IDs of documents with issues")

    # Summary
    overall_assessment: str = Field(
        description="Summary of document collection quality"
    )
    retrieval_recommendations: list[str] = Field(
        description="Suggestions for improving retrieval"
    )


# Enhanced prompts for comprehensive grading
COMPREHENSIVE_DOCUMENT_GRADING_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert document evaluator with expertise in information quality assessment,
fact-checking, and hallucination detection. Your role is to provide comprehensive assessments of
documents for RAG systems.

**EVALUATION FRAMEWORK:**

**1. RELEVANCE ASSESSMENT:**
- HIGHLY_RELEVANT: Directly answers the query with specific information
- RELEVANT: Contains substantial information related to the query
- PARTIALLY_RELEVANT: Has some relevant information but missing key aspects
- MARGINALLY_RELEVANT: Tangentially related with minimal useful information
- NOT_RELEVANT: No meaningful connection to the query

**2. QUALITY ASSESSMENT:**
- EXCELLENT: Authoritative source, comprehensive coverage, well-structured
- GOOD: Solid information with minor gaps, generally reliable
- FAIR: Basic information present, some unclear or incomplete areas
- POOR: Limited value, significant gaps or quality concerns
- UNRELIABLE: Questionable accuracy, poor sources, or misleading content

**3. HALLUCINATION RISK ASSESSMENT:**
- VERY_LOW: All claims are factual and verifiable, authoritative sources
- LOW: Mostly factual with solid basis, minor inferential content
- MODERATE: Mix of facts and unsupported claims, needs verification
- HIGH: Multiple unsupported claims, speculative content
- VERY_HIGH: Likely contains misinformation or fabricated details

**EVALUATION GUIDELINES:**
- Focus on verifiable facts vs. opinions or speculation
- Consider source credibility indicators
- Identify potential biases or one-sided perspectives
- Look for internal consistency and logical coherence
- Assess completeness relative to the query scope
- Flag any obviously false or misleading statements

Provide thorough, evidence-based assessments that help RAG systems make informed decisions about document usage.""",
        ),
        (
            "human",
            """Evaluate these documents for the given query using the comprehensive framework.

**Query:** {query}

**Documents to Evaluate:**
{documents_text}

**Instructions:**
1. Assess each document on relevance, quality, and hallucination risk
2. Provide detailed justifications for each assessment
3. Calculate an overall weighted score considering all factors
4. Make specific recommendations for document usage
5. Identify any concerning patterns across the document set

Return a structured assessment following the ComprehensiveGradingResponse format.""",
        ),
    ]
)


# Hallucination-specific detection prompt
HALLUCINATION_DETECTION_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a specialist in detecting hallucinations and misinformation in text content.
Your task is to identify potentially fabricated, unsupported, or misleading information that could
lead to hallucinations in AI responses.

**HALLUCINATION INDICATORS:**
- Specific claims without supporting evidence
- Unusual or suspicious statistics or numbers
- References to non-existent events, people, or places
- Contradictions with well-established facts
- Overly confident assertions about uncertain topics
- Mix of true and false information (most dangerous)
- Fabricated quotes or citations
- Impossible or implausible scenarios presented as fact

**DETECTION STRATEGY:**
1. Identify all factual claims in the document
2. Assess verifiability of each claim
3. Look for red flags indicating potential fabrication
4. Check for internal consistency
5. Evaluate the plausibility of claims
6. Consider the source and context reliability

Be particularly vigilant about subtle misinformation that mixes truth with falsehood.""",
        ),
        (
            "human",
            """Analyze this document for potential hallucination risks related to the query.

**Query:** {query}
**Document:** {document_text}

**Focus Areas:**
1. Identify specific claims that could lead to hallucinations
2. Assess the verifiability of key assertions
3. Flag any suspicious or implausible content
4. Evaluate the risk level for RAG system usage
5. Provide specific recommendations for handling this content

Return detailed analysis with specific examples and risk assessment.""",
        ),
    ]
)


# Document quality assessment prompt
QUALITY_ASSESSMENT_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an information quality specialist focused on evaluating document
reliability, comprehensiveness, and utility for knowledge systems.

**QUALITY DIMENSIONS:**

**Accuracy & Reliability:**
- Factual correctness of claims
- Source credibility indicators
- Presence of citations or references
- Internal consistency

**Completeness & Coverage:**
- How thoroughly the topic is addressed
- Presence of key information elements
- Gaps or missing critical details
- Depth vs. breadth of coverage

**Clarity & Structure:**
- Clear organization and presentation
- Logical flow of information
- Accessibility to target audience
- Absence of confusing or ambiguous content

**Currency & Relevance:**
- Up-to-date information (where applicable)
- Relevance to current context
- Consideration of temporal factors

**Objectivity & Bias:**
- Balanced perspective
- Acknowledgment of limitations
- Minimal obvious bias
- Distinction between fact and opinion

Provide detailed quality assessments that help determine document utility for knowledge systems.""",
        ),
        (
            "human",
            """Assess the quality of this document for use in answering the given query.

**Query:** {query}
**Document:** {document_text}

**Evaluation Requirements:**
1. Analyze accuracy and reliability indicators
2. Assess completeness relative to the query
3. Evaluate clarity and structure
4. Consider currency and relevance factors
5. Identify any bias or objectivity issues
6. Provide overall quality rating with justification
7. Suggest specific improvements or usage guidelines

Return comprehensive quality assessment with specific examples and recommendations.""",
        ),
    ]
)
