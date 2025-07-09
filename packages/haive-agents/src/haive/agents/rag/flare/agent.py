"""FLARE (Forward-Looking Active REtrieval) RAG Agents

Implementation of FLARE RAG with forward-looking retrieval and iterative generation.
Uses structured output models for planning and managing active retrieval decisions.
"""

import logging
import re
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.models.llm.base import AzureLLMConfig, LLMConfig
from haive.core.schema.prebuilt.rag_state import RAGState
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import END, START
from pydantic import BaseModel, Field

from haive.agents.base.agent import Agent
from haive.agents.multi.base import ConditionalAgent, SequentialAgent
from haive.agents.rag.base.agent import BaseRAGAgent
from haive.agents.simple.agent import SimpleAgent

logger = logging.getLogger(__name__)


class ConfidenceLevel(str, Enum):
    """Confidence levels for generation."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


class RetrievalDecision(str, Enum):
    """Decisions for active retrieval."""

    RETRIEVE = "retrieve"
    CONTINUE = "continue"
    COMPLETE = "complete"


class FLAREPlan(BaseModel):
    """Forward-looking plan for active retrieval."""

    current_query: str = Field(description="Current query being processed")
    generation_so_far: str = Field(description="Text generated so far")

    # Forward-looking analysis
    next_sentences_needed: int = Field(
        ge=1, le=5, description="Number of sentences to generate next"
    )
    confidence_in_current: ConfidenceLevel = Field(
        description="Confidence in current generation"
    )
    uncertainty_tokens: List[str] = Field(description="Tokens indicating uncertainty")

    # Retrieval planning
    retrieval_decision: RetrievalDecision = Field(
        description="Whether to retrieve more information"
    )
    retrieval_queries: List[str] = Field(description="Specific queries for retrieval")
    retrieval_justification: str = Field(description="Why retrieval is needed")

    # Generation planning
    next_generation_focus: str = Field(
        description="What to focus on in next generation"
    )
    expected_length: int = Field(description="Expected length of next generation")
    completion_criteria: str = Field(description="When to consider generation complete")

    # Quality control
    hallucination_risk: float = Field(
        ge=0.0, le=1.0, description="Risk of hallucination"
    )
    evidence_sufficiency: float = Field(
        ge=0.0, le=1.0, description="Sufficiency of current evidence"
    )

    planning_metadata: Dict[str, Any] = Field(
        description="Additional planning metadata"
    )


class FLAREResult(BaseModel):
    """Results from FLARE processing."""

    original_query: str = Field(description="Original query")
    final_response: str = Field(description="Final generated response")

    # Generation metrics
    total_iterations: int = Field(description="Total FLARE iterations")
    retrieval_rounds: int = Field(description="Number of retrieval rounds")
    generation_confidence: float = Field(
        ge=0.0, le=1.0, description="Overall generation confidence"
    )

    # Retrieval analytics
    retrieval_queries_used: List[str] = Field(description="All retrieval queries used")
    documents_retrieved: int = Field(description="Total documents retrieved")
    retrieval_efficiency: float = Field(
        ge=0.0, le=1.0, description="Retrieval efficiency score"
    )

    # Quality metrics
    evidence_coverage: float = Field(
        ge=0.0, le=1.0, description="Evidence coverage of response"
    )
    uncertainty_reduction: float = Field(
        ge=0.0, le=1.0, description="How much uncertainty was reduced"
    )
    factual_grounding: float = Field(
        ge=0.0, le=1.0, description="Factual grounding score"
    )

    # Iteration details
    iteration_history: List[Dict[str, Any]] = Field(
        description="History of each iteration"
    )
    retrieval_decisions: List[str] = Field(description="Retrieval decisions made")

    processing_metadata: Dict[str, Any] = Field(description="Processing statistics")


# Enhanced prompts for FLARE
FLARE_PLANNING_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert at Forward-Looking Active REtrieval (FLARE) planning.

FLARE generates responses iteratively, actively retrieving information when encountering uncertainty.

**FLARE PRINCIPLES:**
1. **Forward-Looking**: Plan ahead for what information will be needed
2. **Active Retrieval**: Retrieve information when uncertainty is detected
3. **Iterative Generation**: Generate text in chunks, evaluating at each step
4. **Uncertainty Detection**: Identify when more information is needed

**UNCERTAINTY INDICATORS:**
- Vague or general statements
- Hedging language ("might", "could", "possibly")
- Missing specific details or facts
- Low confidence in assertions
- Need for current/specific information

**RETRIEVAL TRIGGERS:**
- Confidence drops below threshold
- Specific facts or data needed
- Current information required
- Technical details missing
- Verification needed

Create detailed plans for active retrieval and iterative generation.""",
        ),
        (
            "human",
            """Create FLARE plan for this query and current generation:

**Original Query:** {query}

**Generation So Far:** {generation_so_far}

**Current Context:** {current_context}

**Iteration:** {iteration_number}

Analyze the current state and create a forward-looking plan:
1. Assess confidence in current generation
2. Identify uncertainty indicators and missing information
3. Decide whether active retrieval is needed
4. Plan specific retrieval queries if needed
5. Plan next generation steps and completion criteria

Focus on proactive information gathering and uncertainty reduction.""",
        ),
    ]
)


FLARE_GENERATION_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert at iterative response generation for FLARE RAG.

Generate the next portion of the response based on:
- Original query requirements
- Previously generated content
- Currently available context and evidence
- Forward-looking plan guidance

**GENERATION PRINCIPLES:**
1. **Incremental**: Generate in manageable chunks
2. **Evidence-Based**: Ground statements in retrieved evidence
3. **Uncertainty-Aware**: Flag areas needing more information
4. **Coherent**: Maintain flow with previous generation
5. **Forward-Looking**: Consider what comes next

**UNCERTAINTY HANDLING:**
- Use hedging language when evidence is insufficient
- Flag areas needing verification
- Request specific information when needed
- Maintain appropriate confidence levels

Generate natural, evidence-grounded text that builds toward a complete response.""",
        ),
        (
            "human",
            """Generate next portion of response:

**Original Query:** {query}

**Generation So Far:** {generation_so_far}

**Current Evidence:** {current_evidence}

**FLARE Plan:** {flare_plan}

**Generation Focus:** {generation_focus}

Continue the response following the FLARE plan:
1. Build naturally on previous generation
2. Incorporate available evidence appropriately
3. Generate approximately {expected_length} words
4. Flag any areas where more information is needed
5. Maintain appropriate confidence levels

Focus on natural, evidence-based progression toward complete answer.""",
        ),
    ]
)


def create_flare_planner_callable(llm_config: LLMConfig):
    """Create callable function for FLARE planning."""

    planning_engine = AugLLMConfig(
        llm_config=llm_config,
        prompt_template=FLARE_PLANNING_PROMPT,
        structured_output_model=FLAREPlan,
        output_key="flare_plan",
    )

    def plan_flare_iteration(state: Dict[str, Any]) -> Dict[str, Any]:
        """Plan the next FLARE iteration."""
        query = getattr(state, "query", "")
        generation_so_far = getattr(state, "generation_so_far", "")
        current_context = getattr(state, "current_context", "")
        iteration_number = getattr(state, "iteration_number", 1)

        # Format current context
        if isinstance(current_context, list):
            context_str = (
                "\n".join(
                    [
                        f"Evidence {i+1}: {doc.page_content[:200]}..."
                        for i, doc in enumerate(current_context[:3])
                    ]
                )
                if current_context
                else "No context available"
            )
        else:
            context_str = (
                str(current_context)[:500] + "..."
                if len(str(current_context)) > 500
                else str(current_context)
            )

        # Create FLARE plan
        flare_plan = planning_engine.invoke(
            {
                "query": query,
                "generation_so_far": generation_so_far,
                "current_context": context_str,
                "iteration_number": iteration_number,
            }
        )

        logger.info(
            f"FLARE iteration {iteration_number}: {flare_plan.retrieval_decision} - {flare_plan.retrieval_justification}"
        )

        return {
            "flare_plan": flare_plan,
            "retrieval_decision": flare_plan.retrieval_decision,
            "retrieval_queries": flare_plan.retrieval_queries,
            "next_generation_focus": flare_plan.next_generation_focus,
            "expected_length": flare_plan.expected_length,
            "confidence_level": flare_plan.confidence_in_current,
            "hallucination_risk": flare_plan.hallucination_risk,
            "should_retrieve": flare_plan.retrieval_decision
            == RetrievalDecision.RETRIEVE,
            "should_complete": flare_plan.retrieval_decision
            == RetrievalDecision.COMPLETE,
        }

    return plan_flare_iteration


def create_active_retrieval_callable(
    documents: List[Document], embedding_model: Optional[str] = None
):
    """Create callable function for active retrieval."""

    def active_retrieve(state: Dict[str, Any]) -> Dict[str, Any]:
        """Perform active retrieval based on FLARE plan."""
        retrieval_queries = getattr(state, "retrieval_queries", [])

        if not retrieval_queries:
            logger.info("No retrieval queries specified, skipping retrieval")
            return {
                "new_documents": [],
                "retrieval_performed": False,
                "total_new_docs": 0,
            }

        # Create retriever on-demand
        retriever = BaseRAGAgent.from_documents(
            documents=documents,
            embedding_model=embedding_model,
            name="FLARE Active Retriever",
        )

        # Retrieve for each query
        all_new_docs = []

        for i, retrieval_query in enumerate(retrieval_queries):
            try:
                logger.debug(f"Active retrieval for query {i}: {retrieval_query}")
                result = retriever.run({"query": retrieval_query})

                docs = []
                if hasattr(result, "retrieved_documents"):
                    docs = result.retrieved_documents
                elif isinstance(result, dict) and "retrieved_documents" in result:
                    docs = result["retrieved_documents"]

                # Limit docs per query
                docs = docs[:3]  # Conservative for FLARE
                all_new_docs.extend(docs)
                logger.debug(f"Retrieved {len(docs)} documents for active query {i}")

            except Exception as e:
                logger.warning(
                    f"Active retrieval failed for query '{retrieval_query}': {e}"
                )

        logger.info(f"Active retrieval completed: {len(all_new_docs)} new documents")

        return {
            "new_documents": all_new_docs,
            "retrieval_performed": True,
            "total_new_docs": len(all_new_docs),
            "active_retrieval_queries": retrieval_queries,
        }

    return active_retrieve


class FLAREPlannerAgent(Agent):
    """Agent that creates FLARE plans for iterative generation and active retrieval."""

    name: str = "FLARE Planner"
    llm_config: LLMConfig = Field(description="LLM configuration for planning")

    def build_graph(self) -> BaseGraph:
        """Build FLARE planning graph."""
        graph = BaseGraph(name="FLAREPlanner")

        # Create callable function using the Pydantic field
        flare_planner = create_flare_planner_callable(self.llm_config)

        # Add callable node to graph
        graph.add_node("plan_flare", flare_planner)
        graph.add_edge(START, "plan_flare")
        graph.add_edge("plan_flare", END)

        return graph


class ActiveRetrievalAgent(Agent):
    """Agent that performs active retrieval based on FLARE plans."""

    name: str = "Active Retrieval"
    documents: List[Document] = Field(description="Documents for retrieval")
    embedding_model: Optional[str] = Field(default=None, description="Embedding model")

    def build_graph(self) -> BaseGraph:
        """Build active retrieval graph."""
        graph = BaseGraph(name="ActiveRetrieval")

        # Create callable function using the Pydantic fields
        active_retriever = create_active_retrieval_callable(
            documents=self.documents, embedding_model=self.embedding_model
        )

        # Add callable node to graph
        graph.add_node("active_retrieve", active_retriever)
        graph.add_edge(START, "active_retrieve")
        graph.add_edge("active_retrieve", END)

        return graph


class FLARERAGAgent(SequentialAgent):
    """Complete FLARE RAG agent with forward-looking active retrieval."""

    @classmethod
    def from_documents(
        cls,
        documents: List[Document],
        llm_config: Optional[LLMConfig] = None,
        max_iterations: int = 5,
        confidence_threshold: float = 0.7,
        **kwargs,
    ):
        """Create FLARE RAG agent from documents.

        Args:
            documents: Documents to index
            llm_config: LLM configuration
            max_iterations: Maximum FLARE iterations
            confidence_threshold: Confidence threshold for retrieval
            **kwargs: Additional arguments

        Returns:
            FLARERAGAgent instance
        """
        if not llm_config:
            llm_config = AzureLLMConfig(
                deployment_name="gpt-4",
                azure_endpoint="${AZURE_OPENAI_API_BASE}",
                api_key="${AZURE_OPENAI_API_KEY}",
            )

        # Step 1: FLARE planning with structured output
        flare_planner = FLAREPlannerAgent(llm_config=llm_config, name="FLARE Planner")

        # Step 2: Active retrieval based on plan
        active_retriever = ActiveRetrievalAgent(
            documents=documents,
            embedding_model=kwargs.get("embedding_model"),
            name="Active Retrieval",
        )

        # Step 3: Iterative generation
        iterative_generator = SimpleAgent(
            engine=AugLLMConfig(
                llm_config=llm_config, prompt_template=FLARE_GENERATION_PROMPT
            ),
            name="FLARE Generator",
        )

        # Step 4: Result synthesis
        result_synthesizer = SimpleAgent(
            engine=AugLLMConfig(
                llm_config=llm_config,
                prompt_template=ChatPromptTemplate.from_messages(
                    [
                        (
                            "system",
                            "You are an expert at synthesizing FLARE results into final responses.",
                        ),
                        (
                            "human",
                            "Synthesize final response from FLARE iterations: {flare_history}",
                        ),
                    ]
                ),
                structured_output_model=FLAREResult,
                output_key="flare_result",
            ),
            structured_output_model=FLAREResult,
            name="FLARE Synthesizer",
        )

        return cls(
            agents=[
                flare_planner,
                active_retriever,
                iterative_generator,
                result_synthesizer,
            ],
            name=kwargs.get("name", "FLARE RAG Agent"),
            **kwargs,
        )


# Factory function
def create_flare_rag_agent(
    documents: List[Document],
    llm_config: Optional[LLMConfig] = None,
    flare_mode: str = "adaptive",
    **kwargs,
) -> FLARERAGAgent:
    """Create a FLARE RAG agent.

    Args:
        documents: Documents for retrieval
        llm_config: LLM configuration
        flare_mode: FLARE mode ("conservative", "adaptive", "aggressive")
        **kwargs: Additional arguments

    Returns:
        Configured FLARE RAG agent
    """
    # Adjust parameters based on FLARE mode
    if flare_mode == "conservative":
        kwargs.setdefault("max_iterations", 3)
        kwargs.setdefault("confidence_threshold", 0.8)
    elif flare_mode == "aggressive":
        kwargs.setdefault("max_iterations", 7)
        kwargs.setdefault("confidence_threshold", 0.5)
    else:  # adaptive
        kwargs.setdefault("max_iterations", 5)
        kwargs.setdefault("confidence_threshold", 0.7)

    return FLARERAGAgent.from_documents(
        documents=documents, llm_config=llm_config, **kwargs
    )


# I/O schema for compatibility
def get_flare_rag_io_schema() -> Dict[str, List[str]]:
    """Get I/O schema for FLARE RAG agents."""
    return {
        "inputs": [
            "query",
            "generation_so_far",
            "current_context",
            "iteration_number",
            "messages",
        ],
        "outputs": [
            "flare_plan",
            "retrieval_decision",
            "retrieval_queries",
            "next_generation_focus",
            "expected_length",
            "confidence_level",
            "should_retrieve",
            "should_complete",
            "new_documents",
            "retrieval_performed",
            "flare_result",
            "response",
            "messages",
        ],
    }
