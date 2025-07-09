"""Speculative RAG Agents

Implementation of speculative RAG with parallel hypothesis generation and verification.
Uses structured output models for hypothesis planning and iterative refinement.
"""

import asyncio
import logging
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.models.llm.base import AzureLLMConfig, LLMConfig
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import END, START
from pydantic import BaseModel, Field, validator

from haive.agents.base.agent import Agent
from haive.agents.multi.base import ParallelAgent, SequentialAgent
from haive.agents.rag.base.agent import BaseRAGAgent
from haive.agents.simple.agent import SimpleAgent

logger = logging.getLogger(__name__)


class HypothesisConfidence(str, Enum):
    """Confidence levels for hypotheses."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


class VerificationStatus(str, Enum):
    """Status of hypothesis verification."""

    PENDING = "pending"
    VERIFIED = "verified"
    REFUTED = "refuted"
    INCONCLUSIVE = "inconclusive"
    NEEDS_MORE_DATA = "needs_more_data"


class Hypothesis(BaseModel):
    """Individual hypothesis with structured metadata."""

    id: str = Field(description="Unique hypothesis identifier")
    text: str = Field(description="Hypothesis statement")

    # Confidence and quality
    confidence: HypothesisConfidence = Field(description="Initial confidence level")
    confidence_score: float = Field(
        ge=0.0, le=1.0, description="Numerical confidence (0-1)"
    )
    plausibility: float = Field(ge=0.0, le=1.0, description="Plausibility assessment")

    # Supporting information
    reasoning: str = Field(description="Reasoning behind hypothesis")
    key_assumptions: List[str] = Field(description="Key assumptions made")
    supporting_evidence: List[str] = Field(description="Initial supporting evidence")

    # Verification planning
    verification_criteria: List[str] = Field(
        description="How to verify this hypothesis"
    )
    required_evidence: List[str] = Field(description="Evidence needed for verification")
    verification_complexity: str = Field(
        description="Complexity of verification process"
    )

    # Processing metadata
    generation_method: str = Field(description="How this hypothesis was generated")
    related_hypotheses: List[str] = Field(description="IDs of related hypotheses")

    # Verification results (updated during verification)
    verification_status: VerificationStatus = Field(default=VerificationStatus.PENDING)
    verification_score: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    verification_evidence: List[str] = Field(default_factory=list)
    verification_reasoning: Optional[str] = Field(default=None)


class SpeculativeExecutionPlan(BaseModel):
    """Plan for executing speculative retrieval and verification."""

    total_hypotheses: int = Field(description="Total number of hypotheses")
    parallel_batches: int = Field(description="Number of parallel processing batches")
    batch_size: int = Field(description="Hypotheses per batch")

    # Execution strategy
    verification_strategy: str = Field(description="Strategy for verification")
    evidence_gathering_depth: str = Field(description="Depth of evidence gathering")
    convergence_criteria: str = Field(description="When to stop processing")

    # Resource allocation
    time_budget_per_hypothesis: str = Field(
        description="Time allocation per hypothesis"
    )
    verification_thoroughness: str = Field(description="Thoroughness level")

    # Quality control
    minimum_verification_score: float = Field(
        ge=0.0, le=1.0, description="Minimum score for acceptance"
    )
    required_consensus_level: float = Field(
        ge=0.0, le=1.0, description="Required agreement level"
    )

    # Iteration control
    max_verification_rounds: int = Field(
        ge=1, le=5, description="Maximum verification iterations"
    )
    refinement_enabled: bool = Field(description="Whether to refine hypotheses")

    execution_metadata: Dict[str, Any] = Field(
        description="Additional execution parameters"
    )


class SpeculativeResult(BaseModel):
    """Results from speculative RAG processing."""

    original_query: str = Field(description="Original query")
    total_hypotheses_generated: int = Field(description="Total hypotheses created")

    # Hypothesis outcomes
    verified_hypotheses: List[Hypothesis] = Field(
        description="Successfully verified hypotheses"
    )
    refuted_hypotheses: List[Hypothesis] = Field(description="Refuted hypotheses")
    inconclusive_hypotheses: List[Hypothesis] = Field(
        description="Inconclusive hypotheses"
    )

    # Quality metrics
    overall_confidence: float = Field(
        ge=0.0, le=1.0, description="Overall confidence in results"
    )
    verification_success_rate: float = Field(
        ge=0.0, le=1.0, description="Percentage successfully verified"
    )
    evidence_quality_score: float = Field(
        ge=0.0, le=1.0, description="Quality of gathered evidence"
    )

    # Consensus analysis
    consensus_level: float = Field(
        ge=0.0, le=1.0, description="Agreement between hypotheses"
    )
    conflicting_evidence: List[str] = Field(description="Identified conflicts")
    confidence_distribution: Dict[str, int] = Field(
        description="Distribution of confidence levels"
    )

    # Final synthesis
    synthesized_answer: str = Field(description="Final synthesized answer")
    key_insights: List[str] = Field(description="Key insights discovered")
    limitations: List[str] = Field(description="Identified limitations")

    processing_metadata: Dict[str, Any] = Field(
        description="Processing statistics and metadata"
    )


# Enhanced prompts for speculative processing
HYPOTHESIS_GENERATION_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert hypothesis generator for speculative reasoning.

Generate multiple plausible hypotheses that could answer the query:

**HYPOTHESIS GENERATION PRINCIPLES:**
1. **Diversification**: Generate hypotheses covering different angles and perspectives
2. **Plausibility**: Ensure each hypothesis is reasonable and testable
3. **Specificity**: Make hypotheses specific enough to be verifiable
4. **Completeness**: Cover the full space of possible answers

**HYPOTHESIS QUALITY CRITERIA:**
- Clear and specific statements
- Testable with available evidence
- Varied confidence levels and approaches
- Well-reasoned with explicit assumptions
- Detailed verification criteria

**GENERATION STRATEGIES:**
- Direct answers based on common knowledge
- Alternative interpretations of the query
- Edge cases and less obvious possibilities
- Hypotheses requiring different types of evidence
- Hypotheses with varying complexity levels

Generate 3-7 diverse, high-quality hypotheses for comprehensive coverage.""",
        ),
        (
            "human",
            """Generate hypotheses for this query:

**Query:** {query}

**Available Context:** {context}

**Domain Knowledge:** {domain_info}

Create diverse hypotheses that:
1. Cover different possible answers and interpretations
2. Include varying confidence levels (some certain, some speculative)
3. Require different types of verification evidence
4. Consider both obvious and non-obvious possibilities
5. Account for potential edge cases or alternative perspectives

For each hypothesis, provide:
- Clear, specific statement
- Confidence assessment and reasoning
- Verification criteria and required evidence
- Key assumptions and supporting rationale

Focus on generating testable, diverse hypotheses for comprehensive analysis.""",
        ),
    ]
)


HYPOTHESIS_VERIFICATION_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert hypothesis verifier for speculative reasoning.

Verify hypotheses using available evidence and reasoning:

**VERIFICATION PRINCIPLES:**
1. **Evidence-Based**: Use concrete evidence for verification
2. **Logical Reasoning**: Apply sound logical principles
3. **Bias Awareness**: Consider potential biases and limitations
4. **Uncertainty Handling**: Acknowledge when evidence is insufficient

**VERIFICATION CRITERIA:**
- Strength and quality of supporting evidence
- Logical consistency and coherence
- Absence of contradictory evidence
- Consideration of alternative explanations
- Acknowledgment of limitations and assumptions

**VERIFICATION OUTCOMES:**
- Verified: Strong evidence supports the hypothesis
- Refuted: Evidence contradicts the hypothesis
- Inconclusive: Insufficient or conflicting evidence
- Needs More Data: Requires additional information

Provide detailed, objective verification assessments.""",
        ),
        (
            "human",
            """Verify this hypothesis using available evidence:

**Hypothesis:** {hypothesis_text}

**Hypothesis Details:**
- Confidence: {hypothesis_confidence}
- Reasoning: {hypothesis_reasoning}
- Verification Criteria: {verification_criteria}

**Available Evidence:**
{evidence}

**Additional Context:**
{context}

Perform thorough verification:
1. Analyze all available evidence for and against
2. Assess logical consistency and coherence
3. Consider alternative explanations
4. Identify any contradictions or gaps
5. Determine verification status and confidence

Provide objective, evidence-based verification with detailed reasoning.""",
        ),
    ]
)


SPECULATIVE_SYNTHESIS_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert at synthesizing results from speculative reasoning.

Combine verified hypotheses into comprehensive answers:

**SYNTHESIS PRINCIPLES:**
1. **Evidence Integration**: Combine evidence from all verified hypotheses
2. **Confidence Weighting**: Weight conclusions by verification confidence
3. **Conflict Resolution**: Address contradictions and inconsistencies
4. **Uncertainty Communication**: Clearly communicate limitations

**SYNTHESIS PROCESS:**
- Identify verified and high-confidence hypotheses
- Integrate supporting evidence coherently
- Resolve conflicts through additional analysis
- Acknowledge remaining uncertainties
- Provide balanced, comprehensive conclusions

Generate nuanced, evidence-based answers that reflect the full speculative analysis.""",
        ),
        (
            "human",
            """Synthesize results from speculative hypothesis analysis:

**Original Query:** {query}

**Verified Hypotheses:**
{verified_hypotheses}

**Refuted Hypotheses:**
{refuted_hypotheses}

**Verification Statistics:**
- Success Rate: {verification_success_rate}
- Overall Confidence: {overall_confidence}
- Consensus Level: {consensus_level}

**Evidence Quality:** {evidence_quality_score}

Create comprehensive synthesis:
1. Integrate verified hypotheses into coherent answer
2. Address any conflicts or contradictions
3. Communicate confidence levels and limitations
4. Highlight key insights and discoveries
5. Provide balanced, evidence-based conclusions

Focus on nuanced, well-supported answers that reflect the speculative analysis.""",
        ),
    ]
)


class HypothesisGeneratorAgent(Agent):
    """Agent that generates multiple hypotheses for speculative reasoning."""

    name: str = "Hypothesis Generator"

    def __init__(
        self,
        llm_config: Optional[LLMConfig] = None,
        num_hypotheses: int = 5,
        hypothesis_diversity: str = "high",
        **kwargs,
    ):
        """Initialize hypothesis generator.

        Args:
            llm_config: LLM configuration
            num_hypotheses: Number of hypotheses to generate
            hypothesis_diversity: Diversity level ("low", "medium", "high")
            **kwargs: Additional agent arguments
        """
        self.llm_config = llm_config or AzureLLMConfig(
            deployment_name="gpt-4",
            azure_endpoint="${AZURE_OPENAI_API_BASE}",
            api_key="${AZURE_OPENAI_API_KEY}",
        )
        self.num_hypotheses = num_hypotheses
        self.hypothesis_diversity = hypothesis_diversity
        super().__init__(**kwargs)

    def build_graph(self) -> BaseGraph:
        """Build hypothesis generation graph."""
        graph = BaseGraph(name="HypothesisGenerator")

        # Create hypothesis generation engine
        generation_engine = AugLLMConfig(
            llm_config=self.llm_config,
            prompt_template=HYPOTHESIS_GENERATION_PROMPT,
            structured_output_model=List[Hypothesis],
            output_key="hypotheses",
        )

        def generate_hypotheses(state: Dict[str, Any]) -> Dict[str, Any]:
            """Generate multiple hypotheses for the query."""
            query = getattr(state, "query", "")
            context = getattr(state, "context", "") or getattr(
                state, "retrieved_documents", ""
            )

            # Format context
            if isinstance(context, list):
                context_str = (
                    "\n".join(
                        [
                            f"Doc {i+1}: {doc.page_content[:200]}..."
                            for i, doc in enumerate(context[:5])
                        ]
                    )
                    if context
                    else "No context available"
                )
            else:
                context_str = (
                    str(context)[:800] + "..."
                    if len(str(context)) > 800
                    else str(context)
                )

            # Domain information extraction
            domain_info = self._extract_domain_info(query)

            # Generate hypotheses
            hypotheses = generation_engine.invoke(
                {"query": query, "context": context_str, "domain_info": domain_info}
            )

            # Ensure we have the right number and assign IDs
            if len(hypotheses) > self.num_hypotheses:
                hypotheses = hypotheses[: self.num_hypotheses]

            for i, hypothesis in enumerate(hypotheses):
                hypothesis.id = f"hyp_{i+1}"
                hypothesis.generation_method = (
                    f"speculative_generation_{self.hypothesis_diversity}"
                )

            return {
                "hypotheses": hypotheses,
                "num_hypotheses": len(hypotheses),
                "hypothesis_ids": [h.id for h in hypotheses],
                "generation_complete": True,
            }

        graph.add_node("generate_hypotheses", generate_hypotheses)
        graph.add_edge(START, "generate_hypotheses")
        graph.add_edge("generate_hypotheses", END)

        return graph

    def _extract_domain_info(self, query: str) -> str:
        """Extract domain information for hypothesis generation."""
        # Simple domain detection for context
        domain_indicators = {
            "technical": ["how does", "algorithm", "system", "process", "mechanism"],
            "factual": ["what is", "when did", "where is", "who is", "which"],
            "analytical": ["why", "analyze", "compare", "evaluate", "assess"],
            "creative": ["imagine", "suppose", "what if", "hypothetically"],
        }

        query_lower = query.lower()
        detected_types = []

        for domain_type, indicators in domain_indicators.items():
            if any(indicator in query_lower for indicator in indicators):
                detected_types.append(domain_type)

        return (
            f"Query types: {', '.join(detected_types)}"
            if detected_types
            else "General query"
        )


class ParallelVerificationAgent(Agent):
    """Agent that performs parallel hypothesis verification."""

    name: str = "Parallel Verifier"

    def __init__(
        self,
        documents: List[Document],
        llm_config: Optional[LLMConfig] = None,
        verification_depth: str = "thorough",
        **kwargs,
    ):
        """Initialize parallel verifier.

        Args:
            documents: Documents for evidence gathering
            llm_config: LLM configuration
            verification_depth: Depth of verification ("basic", "thorough", "comprehensive")
            **kwargs: Additional agent arguments
        """
        self.documents = documents
        self.llm_config = llm_config or AzureLLMConfig(
            deployment_name="gpt-4",
            azure_endpoint="${AZURE_OPENAI_API_BASE}",
            api_key="${AZURE_OPENAI_API_KEY}",
        )
        self.verification_depth = verification_depth
        super().__init__(**kwargs)

        # Create base retriever for evidence gathering
        self.base_retriever = BaseRAGAgent.from_documents(
            documents=documents, name="Evidence Retriever"
        )

    def build_graph(self) -> BaseGraph:
        """Build parallel verification graph."""
        graph = BaseGraph(name="ParallelVerifier")

        # Create verification engine
        verification_engine = AugLLMConfig(
            llm_config=self.llm_config,
            prompt_template=HYPOTHESIS_VERIFICATION_PROMPT,
            structured_output_model=Hypothesis,  # Returns updated hypothesis
            output_key="verified_hypothesis",
        )

        def verify_hypotheses_parallel(state: Dict[str, Any]) -> Dict[str, Any]:
            """Verify hypotheses in parallel batches."""
            hypotheses = getattr(state, "hypotheses", [])
            query = getattr(state, "query", "")

            if not hypotheses:
                return {
                    "verified_hypotheses": [],
                    "verification_complete": True,
                    "verification_results": {},
                }

            # Determine batch processing
            batch_size = 3 if self.verification_depth == "comprehensive" else 5
            verification_results = {}
            verified_hypotheses = []

            # Process hypotheses in batches
            for i in range(0, len(hypotheses), batch_size):
                batch = hypotheses[i : i + batch_size]
                batch_results = self._verify_hypothesis_batch(batch, query)
                verification_results.update(batch_results)
                verified_hypotheses.extend(batch_results.values())

            # Categorize results
            verified = [
                h
                for h in verified_hypotheses
                if h.verification_status == VerificationStatus.VERIFIED
            ]
            refuted = [
                h
                for h in verified_hypotheses
                if h.verification_status == VerificationStatus.REFUTED
            ]
            inconclusive = [
                h
                for h in verified_hypotheses
                if h.verification_status == VerificationStatus.INCONCLUSIVE
            ]

            return {
                "verified_hypotheses": verified,
                "refuted_hypotheses": refuted,
                "inconclusive_hypotheses": inconclusive,
                "all_verified_hypotheses": verified_hypotheses,
                "verification_results": verification_results,
                "verification_success_rate": (
                    len(verified) / len(hypotheses) if hypotheses else 0.0
                ),
                "verification_complete": True,
            }

        graph.add_node("verify_parallel", verify_hypotheses_parallel)
        graph.add_edge(START, "verify_parallel")
        graph.add_edge("verify_parallel", END)

        return graph

    def _verify_hypothesis_batch(
        self, hypotheses: List[Hypothesis], query: str
    ) -> Dict[str, Hypothesis]:
        """Verify a batch of hypotheses."""
        results = {}

        for hypothesis in hypotheses:
            try:
                # Gather evidence for hypothesis
                evidence = self._gather_evidence_for_hypothesis(hypothesis, query)

                # Verify using evidence
                verification_result = self._verify_single_hypothesis(
                    hypothesis, evidence, query
                )
                results[hypothesis.id] = verification_result

            except Exception as e:
                logger.warning(
                    f"Verification failed for hypothesis {hypothesis.id}: {e}"
                )
                # Mark as inconclusive on error
                hypothesis.verification_status = VerificationStatus.INCONCLUSIVE
                hypothesis.verification_reasoning = (
                    f"Verification failed due to error: {str(e)}"
                )
                results[hypothesis.id] = hypothesis

        return results

    def _gather_evidence_for_hypothesis(
        self, hypothesis: Hypothesis, query: str
    ) -> str:
        """Gather evidence for hypothesis verification."""
        try:
            # Create search query based on hypothesis
            search_query = f"{query} {hypothesis.text}"

            # Retrieve relevant documents
            result = self.base_retriever.run({"query": search_query})

            if hasattr(result, "retrieved_documents"):
                docs = result.retrieved_documents[:5]
            elif isinstance(result, dict) and "retrieved_documents" in result:
                docs = result["retrieved_documents"][:5]
            else:
                docs = []

            # Format evidence
            evidence = (
                "\n".join(
                    [
                        f"Evidence {i+1}: {doc.page_content[:300]}..."
                        for i, doc in enumerate(docs)
                    ]
                )
                if docs
                else "No specific evidence found in documents"
            )

            return evidence

        except Exception as e:
            logger.warning(f"Evidence gathering failed: {e}")
            return "Evidence gathering failed"

    def _verify_single_hypothesis(
        self, hypothesis: Hypothesis, evidence: str, query: str
    ) -> Hypothesis:
        """Verify a single hypothesis with evidence."""
        try:
            # Use verification engine with structured output
            verification_engine = AugLLMConfig(
                llm_config=self.llm_config,
                prompt_template=HYPOTHESIS_VERIFICATION_PROMPT,
                structured_output_model=Hypothesis,
                output_key="verified_hypothesis",
            )

            verified_hypothesis = verification_engine.invoke(
                {
                    "hypothesis_text": hypothesis.text,
                    "hypothesis_confidence": hypothesis.confidence,
                    "hypothesis_reasoning": hypothesis.reasoning,
                    "verification_criteria": ", ".join(
                        hypothesis.verification_criteria
                    ),
                    "evidence": evidence,
                    "context": f"Original query: {query}",
                }
            )

            # Preserve original ID and metadata
            verified_hypothesis.id = hypothesis.id
            verified_hypothesis.generation_method = hypothesis.generation_method

            return verified_hypothesis

        except Exception as e:
            logger.warning(f"Hypothesis verification failed: {e}")
            # Return original with inconclusive status
            hypothesis.verification_status = VerificationStatus.INCONCLUSIVE
            hypothesis.verification_reasoning = f"Verification error: {str(e)}"
            return hypothesis


class SpeculativeRAGAgent(SequentialAgent):
    """Complete Speculative RAG agent with parallel hypothesis processing."""

    @classmethod
    def from_documents(
        cls,
        documents: List[Document],
        llm_config: Optional[LLMConfig] = None,
        num_hypotheses: int = 5,
        verification_depth: str = "thorough",
        **kwargs,
    ):
        """Create Speculative RAG agent from documents.

        Args:
            documents: Documents to index
            llm_config: LLM configuration
            num_hypotheses: Number of hypotheses to generate
            verification_depth: Depth of verification process
            **kwargs: Additional arguments

        Returns:
            SpeculativeRAGAgent instance
        """
        if not llm_config:
            llm_config = AzureLLMConfig(
                deployment_name="gpt-4",
                azure_endpoint="${AZURE_OPENAI_API_BASE}",
                api_key="${AZURE_OPENAI_API_KEY}",
            )

        # Step 1: Hypothesis generation
        hypothesis_generator = HypothesisGeneratorAgent(
            llm_config=llm_config,
            num_hypotheses=num_hypotheses,
            name="Hypothesis Generator",
        )

        # Step 2: Parallel verification
        parallel_verifier = ParallelVerificationAgent(
            documents=documents,
            llm_config=llm_config,
            verification_depth=verification_depth,
            name="Parallel Verifier",
        )

        # Step 3: Result synthesis
        synthesis_agent = SimpleAgent(
            engine=AugLLMConfig(
                llm_config=llm_config,
                prompt_template=SPECULATIVE_SYNTHESIS_PROMPT,
                structured_output_model=SpeculativeResult,
                output_key="speculative_result",
            ),
            name="Speculative Synthesizer",
        )

        return cls(
            agents=[hypothesis_generator, parallel_verifier, synthesis_agent],
            name=kwargs.get("name", "Speculative RAG Agent"),
            **kwargs,
        )


# Factory function
def create_speculative_rag_agent(
    documents: List[Document],
    llm_config: Optional[LLMConfig] = None,
    speculation_mode: str = "balanced",
    **kwargs,
) -> SpeculativeRAGAgent:
    """Create a Speculative RAG agent.

    Args:
        documents: Documents for retrieval
        llm_config: LLM configuration
        speculation_mode: Mode ("conservative", "balanced", "aggressive")
        **kwargs: Additional arguments

    Returns:
        Configured Speculative RAG agent
    """
    # Adjust parameters based on speculation mode
    if speculation_mode == "conservative":
        kwargs.setdefault("num_hypotheses", 3)
        kwargs.setdefault("verification_depth", "thorough")
    elif speculation_mode == "aggressive":
        kwargs.setdefault("num_hypotheses", 7)
        kwargs.setdefault("verification_depth", "comprehensive")
    else:  # balanced
        kwargs.setdefault("num_hypotheses", 5)
        kwargs.setdefault("verification_depth", "thorough")

    return SpeculativeRAGAgent.from_documents(
        documents=documents, llm_config=llm_config, **kwargs
    )


# I/O schema for compatibility
def get_speculative_rag_io_schema() -> Dict[str, List[str]]:
    """Get I/O schema for Speculative RAG agents."""
    return {
        "inputs": ["query", "context", "messages"],
        "outputs": [
            "hypotheses",
            "num_hypotheses",
            "hypothesis_ids",
            "generation_complete",
            "verified_hypotheses",
            "refuted_hypotheses",
            "inconclusive_hypotheses",
            "all_verified_hypotheses",
            "verification_results",
            "verification_success_rate",
            "verification_complete",
            "speculative_result",
            "response",
            "messages",
        ],
    }
