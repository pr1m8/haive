"""RAG Agent Models.

This module contains all Pydantic models used by RAG agents for structured
data validation and type safety. These models represent different outputs
and intermediate results from various RAG patterns.

Example:
    >>> from haive.agents.rag.models import HyDEResult
    >>> result = HyDEResult(
    ...     hypothetical_doc="Generated document content...",
    ...     refined_query="Refined query text",
    ...     confidence=0.85
    ... )

Typical usage:
    - Import specific models for agent implementations
    - Use for structured output from LLM engines
    - Validate intermediate results in RAG pipelines
    - Type hints for function parameters and returns
"""

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class RAGModuleType(str, Enum):
    """Types of RAG modules for modular composition.

    Attributes:
        QUERY_EXPANSION: Query expansion and refinement module.
        DOCUMENT_FILTERING: Document relevance filtering module.
        CONTEXT_RANKING: Context relevance ranking module.
        ANSWER_GENERATION: Answer generation module.
        ANSWER_VERIFICATION: Answer quality verification module.
        RESPONSE_SYNTHESIS: Final response synthesis module.
    """

    QUERY_EXPANSION = "query_expansion"
    DOCUMENT_FILTERING = "document_filtering"
    CONTEXT_RANKING = "context_ranking"
    ANSWER_GENERATION = "answer_generation"
    ANSWER_VERIFICATION = "answer_verification"
    RESPONSE_SYNTHESIS = "response_synthesis"


class QueryType(str, Enum):
    """Types of queries for branched RAG routing.

    Attributes:
        FACTUAL: Factual information queries.
        ANALYTICAL: Analysis and reasoning queries.
        CREATIVE: Creative and ideation queries.
        PROCEDURAL: Step-by-step procedure queries.
    """

    FACTUAL = "factual"
    ANALYTICAL = "analytical"
    CREATIVE = "creative"
    PROCEDURAL = "procedural"


class ReActStep(str, Enum):
    """ReAct pattern step types.

    Attributes:
        THOUGHT: Reasoning and planning step.
        ACTION: Action execution step.
        OBSERVATION: Observation and analysis step.
        REFLECTION: Reflection and evaluation step.
    """

    THOUGHT = "thought"
    ACTION = "action"
    OBSERVATION = "observation"
    REFLECTION = "reflection"


class MemoryType(str, Enum):
    """Types of memory for memory-aware RAG.

    Attributes:
        SHORT_TERM: Short-term conversational memory.
        LONG_TERM: Long-term knowledge memory.
        EPISODIC: Episodic interaction memory.
        SEMANTIC: Semantic knowledge memory.
    """

    SHORT_TERM = "short_term"
    LONG_TERM = "long_term"
    EPISODIC = "episodic"
    SEMANTIC = "semantic"


class HyDEResult(BaseModel):
    """Hypothetical Document Enhanced (HyDE) result.

    Contains the generated hypothetical document and refined query used in
    the HyDE RAG pattern for improved retrieval performance.

    Attributes:
        hypothetical_doc (str): Generated hypothetical document that would answer the query.
        refined_query (str): Query refined based on the hypothetical document.
        confidence (float): Confidence score in the hypothesis (0.0 to 1.0).
    """

    hypothetical_doc: str = Field(description="Generated hypothetical document")
    refined_query: str = Field(description="Refined query for retrieval")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence in hypothesis")


class FusionResult(BaseModel):
    """Fusion ranking result from multi-query RAG.

    Contains documents ranked using reciprocal rank fusion or similar
    techniques for combining multiple retrieval results.

    Attributes:
        fused_documents (List[str]): Documents ranked by fusion algorithm.
        fusion_scores (List[float]): Corresponding fusion scores.
        ranking_method (str): Method used for ranking (e.g., "reciprocal_rank_fusion").
    """

    fused_documents: List[str] = Field(description="Documents ranked by fusion")
    fusion_scores: List[float] = Field(description="Fusion scores")
    ranking_method: str = Field(description="Method used for ranking")


class StepBackResult(BaseModel):
    """Step-back reasoning result for abstract thinking.

    Contains results from step-back prompting where the agent first
    reasons about high-level concepts before specific answers.

    Attributes:
        abstract_question (str): High-level abstract question derived from the query.
        abstract_answer (str): Answer to the abstract question.
        specific_answer (str): Specific answer to the original query.
    """

    abstract_question: str = Field(description="High-level abstract question")
    abstract_answer: str = Field(description="Answer to abstract question")
    specific_answer: str = Field(description="Specific answer to original query")


class SpeculativeResult(BaseModel):
    """Speculative reasoning result with hypothesis verification.

    Contains hypotheses generated and verified during speculative RAG,
    where multiple potential answers are explored and validated.

    Attributes:
        hypotheses (List[str]): Generated hypotheses for the query.
        verified_hypotheses (List[str]): Hypotheses verified against evidence.
        final_answer (str): Answer based on verified hypotheses.
    """

    hypotheses: List[str] = Field(description="Generated hypotheses")
    verified_hypotheses: List[str] = Field(description="Verified hypotheses")
    final_answer: str = Field(description="Answer based on verified hypotheses")


class MemoryEntry(BaseModel):
    """Memory entry for memory-aware RAG systems.

    Represents a single memory entry with content, type, and metadata
    for use in conversation-aware RAG agents.

    Attributes:
        content (str): Memory content or summary.
        memory_type (MemoryType): Type of memory (short-term, long-term, etc.).
        timestamp (str): When this memory was created.
        relevance_score (float): Relevance to current query (0.0 to 1.0).
        context_tags (List[str]): Tags for categorizing memory content.
    """

    content: str = Field(description="Memory content")
    memory_type: MemoryType = Field(description="Type of memory")
    timestamp: str = Field(description="When this memory was created")
    relevance_score: float = Field(
        ge=0.0, le=1.0, description="Relevance to current query"
    )
    context_tags: List[str] = Field(default_factory=list, description="Context tags")


class MemoryAnalysis(BaseModel):
    """Memory analysis result for context-aware processing.

    Contains analysis of relevant memories and identified knowledge gaps
    for enhanced context-aware response generation.

    Attributes:
        relevant_memories (List[MemoryEntry]): Relevant memories found.
        memory_gaps (List[str]): Identified knowledge gaps.
        temporal_context (str): Temporal context of memories.
        confidence (float): Overall memory confidence (0.0 to 1.0).
    """

    relevant_memories: List[MemoryEntry] = Field(description="Relevant memories found")
    memory_gaps: List[str] = Field(description="Identified knowledge gaps")
    temporal_context: str = Field(description="Temporal context of memories")
    confidence: float = Field(ge=0.0, le=1.0, description="Overall memory confidence")


class ReActStepResult(BaseModel):
    """Result from a single ReAct pattern step.

    Contains the output and metadata from executing a step in the
    ReAct (Reasoning + Acting) pattern.

    Attributes:
        step_type (ReActStep): Type of step executed.
        content (str): Content or result of the step.
        confidence (float): Confidence in this step (0.0 to 1.0).
        next_action (Optional[str]): Next action to take, if any.
    """

    step_type: ReActStep = Field(description="Type of step")
    content: str = Field(description="Step content")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence in this step")
    next_action: Optional[str] = Field(default=None, description="Next action to take")


class QueryClassification(BaseModel):
    """Query classification result for routing decisions.

    Contains classification results used for routing queries to
    appropriate RAG strategies or processing branches.

    Attributes:
        primary_type (QueryType): Primary query type.
        secondary_type (Optional[QueryType]): Secondary type if applicable.
        complexity (str): Query complexity level.
        confidence (float): Classification confidence (0.0 to 1.0).
    """

    primary_type: QueryType = Field(description="Primary query type")
    secondary_type: Optional[QueryType] = Field(
        default=None, description="Secondary type if applicable"
    )
    complexity: str = Field(description="Query complexity")
    confidence: float = Field(ge=0.0, le=1.0, description="Classification confidence")


class BranchResult(BaseModel):
    """Result from a single retrieval branch.

    Contains results from executing a specific branch in branched RAG,
    where multiple retrieval strategies are executed in parallel.

    Attributes:
        branch_type (str): Type of branch executed.
        retrieved_docs (List[str]): Documents retrieved by this branch.
        branch_answer (str): Answer generated by this branch.
        relevance_score (float): Relevance score for this branch (0.0 to 1.0).
    """

    branch_type: str = Field(description="Type of branch")
    retrieved_docs: List[str] = Field(description="Retrieved documents")
    branch_answer: str = Field(description="Answer from this branch")
    relevance_score: float = Field(ge=0.0, le=1.0, description="Relevance score")


class MergedResult(BaseModel):
    """Final merged result from multiple branches or strategies.

    Contains the final synthesized result after combining outputs
    from multiple RAG branches or strategies.

    Attributes:
        primary_answer (str): Primary synthesized answer.
        supporting_evidence (List[str]): Supporting evidence from branches.
        confidence_score (float): Overall confidence (0.0 to 1.0).
        sources_used (List[str]): Sources used in the final answer.
    """

    primary_answer: str = Field(description="Primary answer")
    supporting_evidence: List[str] = Field(
        description="Supporting evidence from branches"
    )
    confidence_score: float = Field(ge=0.0, le=1.0, description="Overall confidence")
    sources_used: List[str] = Field(description="Sources used")


class EnhancedResponse(BaseModel):
    """Enhanced response with reasoning and memory integration.

    Contains a comprehensive response that includes the main answer,
    reasoning chain, memory context, and metadata.

    Attributes:
        answer (str): Main answer to the query.
        reasoning_chain (List[ReActStepResult]): ReAct reasoning steps taken.
        memory_used (List[MemoryEntry]): Memories used in generating response.
        new_memories (List[MemoryEntry]): New memories to store from this interaction.
        confidence (float): Response confidence (0.0 to 1.0).
    """

    answer: str = Field(description="Main answer")
    reasoning_chain: List[ReActStepResult] = Field(description="ReAct reasoning steps")
    memory_used: List[MemoryEntry] = Field(description="Memories used in response")
    new_memories: List[MemoryEntry] = Field(description="New memories to store")
    confidence: float = Field(ge=0.0, le=1.0, description="Response confidence")


class StrategyDecision(BaseModel):
    """Strategy selection decision for agentic routing.

    Contains the decision made by an agentic router about which
    RAG strategy to use for a given query.

    Attributes:
        strategy (str): Selected RAG strategy name.
        confidence (float): Confidence in strategy selection (0.0 to 1.0).
        reasoning (str): Explanation for why this strategy was chosen.
    """

    strategy: str = Field(description="Selected strategy")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence")
    reasoning: str = Field(description="Why this strategy was chosen")


class QueryPlan(BaseModel):
    """Query planning result for complex query decomposition.

    Contains a plan for executing a complex query, including
    sub-queries and execution strategy.

    Attributes:
        sub_queries (List[str]): Sub-queries to execute.
        execution_strategy (str): How to execute them.
        synthesis_approach (str): How to combine results.
    """

    sub_queries: List[str] = Field(description="Sub-queries to execute")
    execution_strategy: str = Field(description="How to execute them")
    synthesis_approach: str = Field(description="How to combine results")


class SubQueryResult(BaseModel):
    """Result from executing a single sub-query.

    Contains the result of executing one sub-query in a
    query planning pipeline.

    Attributes:
        query (str): The sub-query that was executed.
        answer (str): Answer to the sub-query.
        confidence (float): Confidence in this result (0.0 to 1.0).
    """

    query: str = Field(description="The sub-query")
    answer: str = Field(description="Answer to the sub-query")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence")


# Type aliases for commonly used model unions
RAGResult = HyDEResult | FusionResult | StepBackResult | SpeculativeResult
MemoryResult = MemoryEntry | MemoryAnalysis
ProcessingResult = ReActStepResult | QueryClassification | BranchResult | MergedResult
