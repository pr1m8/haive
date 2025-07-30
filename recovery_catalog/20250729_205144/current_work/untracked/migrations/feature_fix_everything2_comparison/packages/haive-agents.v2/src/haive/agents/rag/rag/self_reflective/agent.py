"""Self-Reflective Agentic RAG Agent.

from typing import Any
Implementation of self-reflective RAG with critique and iterative improvement.
Uses reflection loops to assess and enhance answer quality.
"""

import logging
from enum import Enum
from typing import Any

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.models.llm.base import AzureLLMConfig, LLMConfig
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import END, START
from pydantic import BaseModel, Field

from haive.agents.base.agent import Agent

logger = logging.getLogger(__name__)


class ReflectionType(str, Enum):
    """Types of reflection analysis."""

    ACCURACY = "accuracy"
    COMPLETENESS = "completeness"
    RELEVANCE = "relevance"
    CLARITY = "clarity"
    CONSISTENCY = "consistency"
    EVIDENCE = "evidence"


class ReflectionCritique(BaseModel):
    """Structured critique from reflection."""

    reflection_type: ReflectionType = Field(description="Type of reflection")
    current_score: float = Field(ge=0.0, le=1.0, description="Current quality score")

    # Issues identified
    issues_found: list[str] = Field(description="Specific issues identified")
    missing_elements: list[str] = Field(description="What's missing from the answer")
    strengths: list[str] = Field(description="Strong points in the answer")

    # Improvement suggestions
    improvement_suggestions: list[str] = Field(
        description="Specific improvements needed"
    )
    requires_more_retrieval: bool = Field(
        description="Whether more retrieval is needed"
    )
    requires_rephrasing: bool = Field(description="Whether rephrasing is needed")

    # Priority
    improvement_priority: float = Field(
        ge=0.0, le=1.0, description="Priority of improvements"
    )
    estimated_improvement: float = Field(
        ge=0.0, le=1.0, description="Potential improvement"
    )


class ReflectionPlan(BaseModel):
    """Plan for iterative improvement based on reflection."""

    iteration_number: int = Field(description="Current iteration number")
    overall_quality: float = Field(ge=0.0, le=1.0, description="Overall answer quality")

    # Critiques
    critiques: list[ReflectionCritique] = Field(description="All reflection critiques")
    critical_issues: list[str] = Field(description="Most critical issues to address")

    # Improvement plan
    improvement_actions: list[str] = Field(description="Ordered improvement actions")
    retrieval_queries: list[str] = Field(description="New queries for retrieval")
    focus_areas: list[str] = Field(description="Areas to focus improvement on")

    # Decision
    needs_improvement: bool = Field(description="Whether improvement is needed")
    improvement_strategy: str = Field(description="Strategy for improvement")
    termination_reason: str = Field(description="Reason if stopping iterations")

    confidence_in_plan: float = Field(
        ge=0.0, le=1.0, description="Confidence in improvement plan"
    )


class ImprovedAnswer(BaseModel):
    """Result of answer improvement iteration."""

    iteration_number: int = Field(description="Iteration that produced this answer")
    improved_answer: str = Field(description="The improved answer")

    # Changes made
    changes_made: list[str] = Field(description="Specific changes from previous")
    new_evidence_added: list[str] = Field(description="New evidence incorporated")
    clarifications_added: list[str] = Field(description="Clarifications added")

    # Quality metrics
    quality_score: float = Field(ge=0.0, le=1.0, description="New quality score")
    improvement_delta: float = Field(description="Improvement from previous")

    # Confidence
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence in improvement")
    remaining_issues: list[str] = Field(description="Issues still remaining")


class SelfReflectiveResult(BaseModel):
    """Complete result from self-reflective RAG process."""

    original_query: str = Field(description="Original query")
    final_answer: str = Field(description="Final refined answer")

    # Iteration history
    iterations_performed: int = Field(description="Number of reflection iterations")
    iteration_history: list[ImprovedAnswer] = Field(description="All iteration results")
    reflection_history: list[ReflectionPlan] = Field(description="All reflection plans")

    # Quality journey
    initial_quality: float = Field(ge=0.0, le=1.0, description="Initial answer quality")
    final_quality: float = Field(ge=0.0, le=1.0, description="Final answer quality")
    total_improvement: float = Field(description="Total quality improvement")

    # Retrieval statistics
    initial_retrievals: int = Field(description="Initial retrieval count")
    additional_retrievals: int = Field(
        description="Additional retrievals during reflection"
    )
    unique_sources_used: int = Field(description="Unique sources referenced")

    # Process insights
    most_effective_improvements: list[str] = Field(
        description="Most effective improvements"
    )
    persistent_challenges: list[str] = Field(description="Challenges that remained")
    termination_reason: str = Field(description="Why reflection loop ended")

    processing_metadata: dict[str, Any] = Field(description="Process metadata")


# Enhanced prompts for self-reflective RAG
INITIAL_ANSWER_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            """system""",
            """You are an expert at providing comprehensive answers using retrieved information.

Generate an initial answer that will later be refined through self-reflection.
Focus on accuracy and use of evidence, knowing that the answer will be critiqued and improved.""",
        ),
        (
            """human""",
            """Answer this query using the retrieved documents:

**Query:** {query}

**Retrieved Documents:** {documents}

Provide a comprehensive initial answer with clear evidence references.""",
        ),
    ]
)


REFLECTION_CRITIQUE_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            """system""",
            """You are an expert critic for RAG-generated answers.

**REFLECTION FRAMEWORK:**
1. **Accuracy**: Are all facts correct and properly sourced?
2. **Completeness**: Does the answer fully address the query?
3. **Relevance**: Is all information relevant to the query?
4. **Clarity**: Is the answer clear and well-structured?
5. **Consistency**: Are there any contradictions?
6. **Evidence**: Is evidence properly used and cited?

**CRITIQUE APPROACH:**
- Be specific about issues found
- Identify missing elements
- Acknowledge strengths
- Suggest concrete improvements
- Determine if more retrieval is needed
- Prioritize improvements by impact

Provide constructive, actionable critique for improvement.""",
        ),
        (
            """human""",
            """Critique this answer for the given query:

**Original Query:** {query}

**Current Answer:** {answer}

**Iteration Number:** {iteration}

**Previous Critiques:** {previous_critiques}

Analyze the answer across all dimensions and provide specific improvement guidance.""",
        ),
    ]
)


IMPROVEMENT_PLANNING_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            """system""",
            """You are an expert at planning iterative improvements for RAG answers.

**PLANNING PRINCIPLES:**
1. **Prioritize**: Address most critical issues first
2. **Actionable**: Create specific, executable improvements
3. **Iterative**: Plan for gradual enhancement
4. **Efficient**: Know when to stop iterating
5. **Evidence-based**: Ground improvements in retrieval

**IMPROVEMENT STRATEGIES:**
- Targeted retrieval for missing information
- Rephrasing for clarity
- Adding evidence and citations
- Resolving contradictions
- Enhancing structure and flow
- Deepening analysis

**TERMINATION CRITERIA:**
- Quality threshold reached (>0.9)
- Marginal improvements (<0.05)
- Maximum iterations reached
- All critical issues addressed

Create effective improvement plans.""",
        ),
        (
            """human""",
            """Plan improvements based on reflection critiques:

**Query:** {query}

**Current Answer Quality:** {current_quality}

**Critiques:** {critiques}

**Iteration:** {iteration}

**Max Iterations:** {max_iterations}

Create an improvement plan or decide to terminate with reasoning.""",
        ),
    ]
)


ANSWER_IMPROVEMENT_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            """system""",
            """You are an expert at improving RAG answers based on reflection feedback.

**IMPROVEMENT PRINCIPLES:**
1. **Targeted**: Address specific issues identified
2. **Evidence-based**: Use additional retrieval effectively
3. **Preserving**: Keep strong elements from previous version
4. **Clear**: Improve clarity and structure
5. **Comprehensive**: Ensure completeness

**IMPROVEMENT TECHNIQUES:**
- Incorporate new evidence seamlessly
- Clarify ambiguous statements
- Add missing information
- Improve logical flow
- Strengthen evidence usage
- Remove irrelevant content

Create improved answers that address all feedback.""",
        ),
        (
            """human""",
            """Improve this answer based on the improvement plan:

**Query:** {query}

**Current Answer:** {current_answer}

**Improvement Plan:** {improvement_plan}

**New Retrieved Information:** {new_retrievals}

**Focus Areas:** {focus_areas}

Generate an improved answer addressing all identified issues.""",
        ),
    ]
)


class SelfReflectiveRAGAgent(Agent):
    """Self-Reflective RAG agent with iterative improvement capabilities.

    This agent uses conditional edges to iterate through reflection loops.
    """

    name: str = "Self-Reflective RAG Agent"
    documents: list[Document] = Field(description="Documents for retrieval")
    llm_config: LLMConfig = Field(description="LLM configuration")
    max_iterations: int = Field(default=3, description="Maximum reflection iterations")
    quality_threshold: float = Field(
        default=0.85, description="Quality threshold to stop iterating"
    )

    # Engines for different stages (initialized in setup_agent)
    initial_answer_engine: AugLLMConfig | None = Field(
        default=None, description="Engine for initial answer"
    )
    critique_engine: AugLLMConfig | None = Field(
        default=None, description="Engine for reflection critique"
    )
    planning_engine: AugLLMConfig | None = Field(
        default=None, description="Engine for improvement planning"
    )
    improvement_engine: AugLLMConfig | None = Field(
        default=None, description="Engine for answer improvement"
    )
    synthesis_engine: AugLLMConfig | None = Field(
        default=None, description="Engine for result synthesis"
    )

    def setup_agent(self) -> None:
        """Initialize engines."""
        # Create initial answer engine
        self.initial_answer_engine = AugLLMConfig(
            llm_config=self.llm_config,
            prompt_template=INITIAL_ANSWER_PROMPT,
            output_key="initial_answer",
        )

        # Create critique engine
        self.critique_engine = AugLLMConfig(
            llm_config=self.llm_config,
            prompt_template=REFLECTION_CRITIQUE_PROMPT,
            structured_output_model=ReflectionCritique,
            output_key="critique",
        )

        # Create planning engine
        self.planning_engine = AugLLMConfig(
            llm_config=self.llm_config,
            prompt_template=IMPROVEMENT_PLANNING_PROMPT,
            structured_output_model=ReflectionPlan,
            output_key="reflection_plan",
        )

        # Create improvement engine
        self.improvement_engine = AugLLMConfig(
            llm_config=self.llm_config,
            prompt_template=ANSWER_IMPROVEMENT_PROMPT,
            structured_output_model=ImprovedAnswer,
            output_key="improved_answer",
        )

        # Create synthesis engine
        self.synthesis_engine = AugLLMConfig(
            llm_config=self.llm_config,
            prompt_template=ChatPromptTemplate.from_messages(
                [
                    ("system", "Synthesize the self-reflective RAG results."),
                    ("human", "{context}"),
                ]
            ),
            structured_output_model=SelfReflectiveResult,
            output_key="reflective_result",
        )

        # Add engines to registry
        self.engines["initial_answer"] = self.initial_answer_engine
        self.engines["critique"] = self.critique_engine
        self.engines["planning"] = self.planning_engine
        self.engines["improvement"] = self.improvement_engine
        self.engines["synthesis"] = self.synthesis_engine

    @classmethod
    def from_documents(
        cls,
        documents: list[Document],
        llm_config: LLMConfig | None = None,
        max_iterations: int = 3,
        quality_threshold: float = 0.85,
        **kwargs,
    ):
        """Create Self-Reflective RAG agent from documents.

        Args:
            documents: Documents to index for retrieval
            llm_config: LLM configuration
            max_iterations: Maximum reflection iterations
            quality_threshold: Quality threshold to stop iterating
            **kwargs: Additional arguments

        Returns:
            SelfReflectiveRAGAgent instance
        """
        if not llm_config:
            llm_config = AzureLLMConfig(
                deployment_name="gpt-4",
                azure_endpoint="${AZURE_OPENAI_API_BASE}",
                api_key="${AZURE_OPENAI_API_KEY}",
            )

        return cls(
            documents=documents,
            llm_config=llm_config,
            max_iterations=max_iterations,
            quality_threshold=quality_threshold,
            **kwargs,
        )

    def generate_initial_answer(self, state: dict[str, Any]) -> dict[str, Any]:
        """Generate initial answer."""
        query = state.get("query", "")

        logger.info("Generating initial answer...")
        initial_result = self.initial_answer_engine.invoke(
            {
                "query": query,
                "documents": "\n\n".join(
                    [
                        f"Document {i+1}: {doc.page_content[:500]}..."
                        for i, doc in enumerate(self.documents[:5])
                    ]
                ),
            }
        )

        current_answer = initial_result.get("initial_answer", "")

        return {
            "current_answer": current_answer,
            "iteration_history": [],
            "reflection_history": [],
            "current_iteration": 0,
            "current_quality": 0.6,  # Initial quality estimate
        }

    def reflect_and_critique(self, state: dict[str, Any]) -> dict[str, Any]:
        """Generate critiques and plan improvements."""
        query = state.get("query", "")
        current_answer = state.get("current_answer", "")
        iteration = state.get("current_iteration", 0)
        reflection_history = state.get("reflection_history", [])

        logger.info(f"Reflection iteration {iteration + 1}")

        # Create critiques for different aspects
        critiques = []
        for _reflection_type in [
            ReflectionType.ACCURACY,
            ReflectionType.COMPLETENESS,
            ReflectionType.CLARITY,
        ]:
            critique = self.critique_engine.invoke(
                {
                    "query": query,
                    "answer": current_answer,
                    "iteration": iteration + 1,
                    "previous_critiques": str(
                        reflection_history[-1].critiques
                        if reflection_history
                        else "None"
                    ),
                }
            )
            critiques.append(critique)

        # Plan improvements
        current_quality = sum(c.current_score for c in critiques) / len(critiques)

        reflection_plan = self.planning_engine.invoke(
            {
                "query": query,
                "current_quality": current_quality,
                "critiques": "\n".join([str(c) for c in critiques]),
                "iteration": iteration + 1,
                "max_iterations": self.max_iterations,
            }
        )

        reflection_history.append(reflection_plan)

        return {
            **state,
            "current_quality": current_quality,
            "reflection_plan": reflection_plan,
            "reflection_history": reflection_history,
            "critiques": critiques,
        }

    def should_continue_improving(self, state: dict[str, Any]) -> str:
        """Determine if improvement should continue."""
        reflection_plan = state.get("reflection_plan")
        current_quality = state.get("current_quality", 0)
        current_iteration = state.get("current_iteration", 0)

        if (
            (reflection_plan and not reflection_plan.needs_improvement)
            or current_quality >= self.quality_threshold
            or current_iteration >= self.max_iterations
        ):
            return "synthesize_result"
        return "improve_answer"

    def improve_answer(self, state: dict[str, Any]) -> dict[str, Any]:
        """Improve the answer based on reflection."""
        query = state.get("query", "")
        current_answer = state.get("current_answer", "")
        reflection_plan = state.get("reflection_plan")
        iteration_history = state.get("iteration_history", [])
        current_iteration = state.get("current_iteration", 0)

        # Improve answer
        improved = self.improvement_engine.invoke(
            {
                "query": query,
                "current_answer": current_answer,
                "improvement_plan": str(reflection_plan.improvement_actions),
                "new_retrievals": "Additional context from documents...",  # Simplified
                "focus_areas": ", ".join(reflection_plan.focus_areas),
            }
        )

        iteration_history.append(improved)

        return {
            **state,
            "current_answer": improved.improved_answer,
            "iteration_history": iteration_history,
            "current_iteration": current_iteration + 1,
        }

    def synthesize_result(self, state: dict[str, Any]) -> dict[str, Any]:
        """Create final self-reflective result."""
        query = state.get("query", "")
        current_answer = state.get("current_answer", "")
        iteration_history = state.get("iteration_history", [])
        current_quality = state.get("current_quality", 0.85)

        logger.info("Creating self-reflective result...")

        reflective_result = self.synthesis_engine.invoke(
            {
                "context": f"""
            Query: {query}
            Final Answer: {current_answer}
            Iterations: {len(iteration_history)}
            Initial Quality: 0.6
            Final Quality: {current_quality}
            """
            }
        )

        return {
            "response": current_answer,
            "reflective_result": reflective_result,
            "iterations_performed": len(iteration_history),
            "final_quality": current_quality,
            "improvement_history": iteration_history,
            "reflection_history": state.get("reflection_history", []),
            "messages": state.get("messages", []),
        }

    def build_graph(self) -> BaseGraph:
        """Build the self-reflective graph with conditional edges."""
        graph = BaseGraph(name="SelfReflectiveRAG")

        # Add nodes
        graph.add_node("generate_initial", self.generate_initial_answer)
        graph.add_node("reflect_critique", self.reflect_and_critique)
        graph.add_node("improve_answer", self.improve_answer)
        graph.add_node("synthesize_result", self.synthesize_result)

        # Connect the flow
        graph.add_edge(START, "generate_initial")
        graph.add_edge("generate_initial", "reflect_critique")

        # Add conditional edge for reflection loop
        graph.add_conditional_edges(
            "reflect_critique",
            self.should_continue_improving,
            {
                "improve_answer": "improve_answer",
                "synthesize_result": "synthesize_result",
            },
        )

        # Loop back from improvement to reflection
        graph.add_edge("improve_answer", "reflect_critique")

        # Synthesis leads to end
        graph.add_edge("synthesize_result", END)

        return graph


# Factory function
def create_self_reflective_rag_agent(
    documents: list[Document],
    llm_config: LLMConfig | None = None,
    reflection_mode: str = "thorough",
    **kwargs,
) -> SelfReflectiveRAGAgent:
    """Create a Self-Reflective RAG agent.

    Args:
        documents: Documents for retrieval
        llm_config: LLM configuration
        reflection_mode: Mode ("quick", "balanced", "thorough")
        **kwargs: Additional arguments

    Returns:
        Configured Self-Reflective RAG agent
    """
    # Configure based on mode
    if reflection_mode == "quick":
        kwargs.setdefault("max_iterations", 1)
        kwargs.setdefault("quality_threshold", 0.75)
    elif reflection_mode == "balanced":
        kwargs.setdefault("max_iterations", 2)
        kwargs.setdefault("quality_threshold", 0.80)
    else:  # thorough
        kwargs.setdefault("max_iterations", 3)
        kwargs.setdefault("quality_threshold", 0.85)

    return SelfReflectiveRAGAgent.from_documents(
        documents=documents, llm_config=llm_config, **kwargs
    )


# I/O schema for compatibility
def get_self_reflective_rag_io_schema() -> dict[str, list[str]]:
    """Get I/O schema for Self-Reflective RAG agents."""
    return {
        "inputs": ["query", "context", "messages"],
        "outputs": [
            "response",
            "reflective_result",
            "iterations_performed",
            "final_quality",
            "improvement_history",
            "reflection_history",
            "messages",
        ],
    }
