"""Hallucination Grading Agents.

Modular agents for detecting and grading hallucinations in RAG responses.
Can be plugged into any workflow with compatible I/O schemas.
"""

import logging
from typing import Any, Literal

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.node.agent_node import AgentNodeConfig
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.models.llm.base import AzureLLMConfig, LLMConfig
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import END, START
from pydantic import BaseModel, Field

from haive.agents.base.agent import Agent
from haive.agents.simple.agent import SimpleAgent

logger = logging.getLogger(__name__)


# Hallucination grading models
class HallucinationGrade(BaseModel):
    """Single hallucination assessment."""

    has_hallucination: bool = Field(
        description="Whether response contains hallucinations"
    )
    confidence_score: float = Field(
        ge=0.0, le=1.0, description="Confidence in assessment (0-1)"
    )
    hallucination_type: Literal["factual", "contextual", "logical", "none"] = Field(
        description="Type of hallucination detected"
    )
    severity: Literal["low", "medium", "high", "critical"] = Field(
        description="Severity of hallucination"
    )
    evidence: list[str] = Field(
        default_factory=list, description="Specific evidence of hallucination"
    )
    reasoning: str = Field(description="Detailed reasoning for the assessment")


class AdvancedHallucinationGrade(BaseModel):
    """Advanced hallucination assessment with detailed analysis."""

    # Basic assessment
    has_hallucination: bool = Field(
        description="Whether response contains hallucinations"
    )
    overall_confidence: float = Field(
        ge=0.0, le=1.0, description="Overall confidence in assessment"
    )

    # Detailed analysis
    factual_accuracy: float = Field(
        ge=0.0, le=1.0, description="Factual accuracy score"
    )
    contextual_consistency: float = Field(
        ge=0.0, le=1.0, description="Consistency with context"
    )
    logical_coherence: float = Field(
        ge=0.0, le=1.0, description="Logical coherence score"
    )
    source_attribution: float = Field(
        ge=0.0, le=1.0, description="Proper source attribution"
    )

    # Specific hallucination types
    hallucination_types: list[str] = Field(
        default_factory=list, description="Types of hallucinations found"
    )

    # Evidence and examples
    fabricated_facts: list[str] = Field(
        default_factory=list, description="Specific fabricated facts identified"
    )
    unsupported_claims: list[str] = Field(
        default_factory=list, description="Claims not supported by context"
    )
    contradictions: list[str] = Field(
        default_factory=list, description="Contradictions with source material"
    )

    # Recommendations
    severity_level: Literal["none", "low", "medium", "high", "critical"] = Field(
        description="Overall severity level"
    )
    action_needed: Literal["none", "review", "revise", "regenerate", "reject"] = Field(
        description="Recommended action"
    )

    # Detailed analysis
    detailed_reasoning: str = Field(description="Comprehensive reasoning")
    improvement_suggestions: list[str] = Field(
        default_factory=list, description="Specific suggestions for improvement"
    )


class RealtimeHallucinationCheck(BaseModel):
    """Quick hallucination check for real-time applications."""

    is_safe: bool = Field(description="Whether response is safe to use")
    risk_level: Literal["very_low", "low", "medium", "high", "very_high"] = Field(
        description="Risk level for hallucination"
    )
    quick_flags: list[str] = Field(
        default_factory=list, description="Quick warning flags"
    )
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence in assessment")


# Enhanced prompts for hallucination detection
BASIC_HALLUCINATION_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert at detecting hallucinations in AI-generated responses.

A hallucination occurs when the response contains information that is:
- Not supported by the provided context/documents
- Factually incorrect or fabricated
- Contradicts the source material
- Makes unsupported claims or assumptions

Assess the response carefully and identify any hallucinations.""",
        ),
        (
            "human",
            """Evaluate this response for hallucinations:

Query: {query}
Context Documents: {retrieved_documents}
AI Response: {generated_response}

Check if the response contains any information not supported by the context or any fabricated facts.
Provide a detailed assessment.""",
        ),
    ]
)


ADVANCED_HALLUCINATION_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a world-class expert in detecting and analyzing hallucinations in AI responses.
Your role is to provide comprehensive analysis of response quality and accuracy.

**HALLUCINATION TYPES:**

1. **Factual Hallucinations**: Incorrect facts, dates, numbers, or events
2. **Contextual Hallucinations**: Information not present in source material
3. **Logical Hallucinations**: Illogical conclusions or reasoning errors
4. **Attribution Hallucinations**: Misattributed quotes, sources, or claims

**ASSESSMENT CRITERIA:**

- **Factual Accuracy**: Are all facts correct and verifiable?
- **Contextual Consistency**: Is everything supported by the context?
- **Logical Coherence**: Does the reasoning make sense?
- **Source Attribution**: Are sources properly cited and accurate?

**SEVERITY LEVELS:**
- **None**: No hallucinations detected
- **Low**: Minor unsupported details that don't affect main message
- **Medium**: Some fabricated facts or unsupported claims
- **High**: Significant misinformation that could mislead
- **Critical**: Dangerous misinformation that could cause harm

Be thorough and provide specific examples for any hallucinations found.""",
        ),
        (
            "human",
            """Conduct a comprehensive hallucination analysis:

**Query:** {query}

**Source Documents:**
{retrieved_documents}

**AI Response to Analyze:**
{generated_response}

**Additional Context (if available):**
- Web search results: {web_search_results}
- Previous messages: {messages}
- Grading results: {grading_results}

Provide a detailed analysis with specific examples of any hallucinations found.""",
        ),
    ]
)


REALTIME_HALLUCINATION_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a fast hallucination detector for real-time applications.

Quickly assess if the response is safe to use. Focus on:
- Obviously fabricated facts
- Clear contradictions with context
- Dangerous misinformation
- Completely unsupported claims

Provide a quick safety assessment.""",
        ),
        (
            "human",
            """Quick hallucination check:

Query: {query}
Context: {retrieved_documents}
Response: {generated_response}

Is this response safe to use? Flag any obvious hallucinations.""",
        ),
    ]
)


class HallucinationGraderAgent(Agent):
    """Basic hallucination grading agent."""

    name: str = "Hallucination Grader"

    def __init__(
        self, llm_config: LLMConfig | None = None, threshold: float = 0.7, **kwargs
    ):
        """Initialize hallucination grader.

        Args:
            llm_config: LLM configuration
            threshold: Confidence threshold for flagging hallucinations
            **kwargs: Additional agent arguments
        """
        self.llm_config = llm_config or AzureLLMConfig(
            deployment_name="gpt-4",
            azure_endpoint="${AZURE_OPENAI_API_BASE}",
            api_key="${AZURE_OPENAI_API_KEY}",
        )
        self.threshold = threshold
        super().__init__(**kwargs)

    def build_graph(self) -> BaseGraph:
        """Build hallucination grading graph."""
        graph = BaseGraph(name="HallucinationGrader")

        # Create grading engine
        grading_engine = AugLLMConfig(
            llm_config=self.llm_config,
            prompt_template=BASIC_HALLUCINATION_PROMPT,
            structured_output_model=HallucinationGrade,
            output_key="hallucination_grade",
        )

        # Grading function
        def grade_hallucination(state: dict[str, Any]) -> dict[str, Any]:
            """Grade response for hallucinations."""
            query = getattr(state, "query", "")
            retrieved_documents = getattr(state, "retrieved_documents", [])
            generated_response = getattr(state, "generated_response", "") or getattr(
                state, "response", ""
            )

            # Format documents for context
            doc_context = (
                "\n\n".join(
                    [
                        f"Document {i+1}: {doc.page_content}"
                        for i, doc in enumerate(retrieved_documents[:5])
                    ]
                )
                if retrieved_documents
                else "No documents provided"
            )

            # Get structured grade
            grade = grading_engine.invoke(
                {
                    "query": query,
                    "retrieved_documents": doc_context,
                    "generated_response": generated_response,
                }
            )

            # Add processing metadata
            is_flagged = (
                grade.confidence_score >= self.threshold and grade.has_hallucination
            )

            return {
                "hallucination_grade": grade,
                "is_hallucination_flagged": is_flagged,
                "hallucination_confidence": grade.confidence_score,
                "needs_revision": is_flagged and grade.severity in ["high", "critical"],
            }

        # Add grading node
        AgentNodeConfig(
            name="hallucination_grader",
            agent=SimpleAgent(
                engine=grading_engine, name="Hallucination Grader Engine"
            ),
        )

        graph.add_node("grade_hallucination", grade_hallucination)
        graph.add_edge(START, "grade_hallucination")
        graph.add_edge("grade_hallucination", END)

        return graph


class AdvancedHallucinationGraderAgent(Agent):
    """Advanced hallucination grading with detailed analysis."""

    name: str = "Advanced Hallucination Grader"

    def __init__(
        self,
        llm_config: LLMConfig | None = None,
        enable_context_expansion: bool = True,
        **kwargs,
    ):
        """Initialize advanced hallucination grader.

        Args:
            llm_config: LLM configuration
            enable_context_expansion: Whether to use additional context sources
            **kwargs: Additional agent arguments
        """
        self.llm_config = llm_config or AzureLLMConfig(
            deployment_name="gpt-4",
            azure_endpoint="${AZURE_OPENAI_API_BASE}",
            api_key="${AZURE_OPENAI_API_KEY}",
        )
        self.enable_context_expansion = enable_context_expansion
        super().__init__(**kwargs)

    def build_graph(self) -> BaseGraph:
        """Build advanced hallucination analysis graph."""
        graph = BaseGraph(name="AdvancedHallucinationGrader")

        # Create advanced grading engine
        grading_engine = AugLLMConfig(
            llm_config=self.llm_config,
            prompt_template=ADVANCED_HALLUCINATION_PROMPT,
            structured_output_model=AdvancedHallucinationGrade,
            output_key="advanced_hallucination_grade",
        )

        def advanced_hallucination_analysis(state: dict[str, Any]) -> dict[str, Any]:
            """Comprehensive hallucination analysis."""
            query = getattr(state, "query", "")
            retrieved_documents = getattr(state, "retrieved_documents", [])
            generated_response = getattr(state, "generated_response", "") or getattr(
                state, "response", ""
            )

            # Get additional context if available
            web_search_results = getattr(state, "web_search_results", "")
            messages = getattr(state, "messages", [])
            grading_results = getattr(state, "grading_results", "")

            # Format context
            doc_context = (
                "\n\n".join(
                    [
                        f"Document {i+1}: {doc.page_content}"
                        for i, doc in enumerate(retrieved_documents[:10])
                    ]
                )
                if retrieved_documents
                else "No documents provided"
            )

            # Get comprehensive analysis
            grade = grading_engine.invoke(
                {
                    "query": query,
                    "retrieved_documents": doc_context,
                    "generated_response": generated_response,
                    "web_search_results": str(web_search_results),
                    "messages": (
                        str(messages[-3:]) if messages else ""
                    ),  # Last 3 messages
                    "grading_results": str(grading_results),
                }
            )

            # Calculate risk scores
            risk_score = 1.0 - min(
                grade.factual_accuracy,
                grade.contextual_consistency,
                grade.logical_coherence,
            )

            # Determine actions needed
            action_urgency = {
                "none": 0,
                "review": 1,
                "revise": 2,
                "regenerate": 3,
                "reject": 4,
            }.get(grade.action_needed, 1)

            return {
                "advanced_hallucination_grade": grade,
                "hallucination_risk_score": risk_score,
                "action_urgency_level": action_urgency,
                "needs_immediate_attention": grade.severity_level
                in ["high", "critical"],
                "is_response_reliable": grade.overall_confidence > 0.8
                and not grade.has_hallucination,
                "improvement_needed": len(grade.improvement_suggestions) > 0,
            }

        graph.add_node("advanced_analysis", advanced_hallucination_analysis)
        graph.add_edge(START, "advanced_analysis")
        graph.add_edge("advanced_analysis", END)

        return graph


class RealtimeHallucinationGraderAgent(Agent):
    """Fast hallucination checker for real-time applications."""

    name: str = "Realtime Hallucination Grader"

    def __init__(
        self,
        llm_config: LLMConfig | None = None,
        safety_threshold: float = 0.8,
        **kwargs,
    ):
        """Initialize realtime hallucination grader.

        Args:
            llm_config: LLM configuration
            safety_threshold: Threshold for considering response safe
            **kwargs: Additional agent arguments
        """
        self.llm_config = llm_config or AzureLLMConfig(
            deployment_name="gpt-4",
            azure_endpoint="${AZURE_OPENAI_API_BASE}",
            api_key="${AZURE_OPENAI_API_KEY}",
        )
        self.safety_threshold = safety_threshold
        super().__init__(**kwargs)

    def build_graph(self) -> BaseGraph:
        """Build realtime hallucination check graph."""
        graph = BaseGraph(name="RealtimeHallucinationGrader")

        # Create fast checking engine
        checking_engine = AugLLMConfig(
            llm_config=self.llm_config,
            prompt_template=REALTIME_HALLUCINATION_PROMPT,
            structured_output_model=RealtimeHallucinationCheck,
            output_key="realtime_hallucination_check",
        )

        def quick_hallucination_check(state: dict[str, Any]) -> dict[str, Any]:
            """Quick safety check for hallucinations."""
            query = getattr(state, "query", "")
            retrieved_documents = getattr(state, "retrieved_documents", [])
            generated_response = getattr(state, "generated_response", "") or getattr(
                state, "response", ""
            )

            # Quick context (fewer documents for speed)
            doc_context = (
                "\n\n".join(
                    [
                        f"Doc {i+1}: {doc.page_content[:200]}..."
                        for i, doc in enumerate(retrieved_documents[:3])
                    ]
                )
                if retrieved_documents
                else "No context"
            )

            # Get quick assessment
            check = checking_engine.invoke(
                {
                    "query": query,
                    "retrieved_documents": doc_context,
                    "generated_response": generated_response,
                }
            )

            # Safety decision
            is_safe_to_use = (
                check.is_safe
                and check.confidence >= self.safety_threshold
                and check.risk_level in ["very_low", "low"]
            )

            return {
                "realtime_hallucination_check": check,
                "is_safe_to_use": is_safe_to_use,
                "quick_risk_level": check.risk_level,
                "safety_confidence": check.confidence,
                "needs_full_check": not is_safe_to_use
                or check.risk_level not in ["very_low", "low"],
            }

        graph.add_node("quick_check", quick_hallucination_check)
        graph.add_edge(START, "quick_check")
        graph.add_edge("quick_check", END)

        return graph


# Factory functions for easy creation
def create_hallucination_grader(
    grader_type: Literal["basic", "advanced", "realtime"] = "basic",
    llm_config: LLMConfig | None = None,
    **kwargs,
) -> Agent:
    """Create a hallucination grader agent.

    Args:
        grader_type: Type of grader to create
        llm_config: LLM configuration
        **kwargs: Additional arguments

    Returns:
        Configured hallucination grader agent
    """
    if grader_type == "basic":
        return HallucinationGraderAgent(llm_config=llm_config, **kwargs)
    if grader_type == "advanced":
        return AdvancedHallucinationGraderAgent(llm_config=llm_config, **kwargs)
    if grader_type == "realtime":
        return RealtimeHallucinationGraderAgent(llm_config=llm_config, **kwargs)
    raise ValueError(f"Unknown grader type: {grader_type}")


# Example usage and I/O compatibility
def get_hallucination_grader_io_schema() -> dict[str, list[str]]:
    """Get I/O schema for hallucination graders for compatibility checking."""
    return {
        "inputs": [
            "query",
            "retrieved_documents",
            "generated_response",
            "response",
            "messages",
            "web_search_results",
            "grading_results",
        ],
        "outputs": [
            "hallucination_grade",
            "advanced_hallucination_grade",
            "realtime_hallucination_check",
            "is_hallucination_flagged",
            "hallucination_confidence",
            "needs_revision",
            "hallucination_risk_score",
            "is_response_reliable",
            "is_safe_to_use",
            "needs_full_check",
        ],
    }
