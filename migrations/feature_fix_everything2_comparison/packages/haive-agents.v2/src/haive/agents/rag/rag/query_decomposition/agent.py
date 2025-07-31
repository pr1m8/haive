"""Query Decomposition Agents.

Modular agents for breaking down complex queries into manageable sub-queries.
Can be plugged into any workflow with compatible I/O schemas.
"""

import logging
from enum import Enum
from typing import Any, Literal

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.models.llm.base import AzureLLMConfig, LLMConfig
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import END, START
from pydantic import BaseModel, Field

from haive.agents.base.agent import Agent

logger = logging.getLogger(__name__)


# Query decomposition models
class QueryType(str, Enum):
    """Types of queries for decomposition strategy."""

    SIMPLE = "simple"
    COMPOUND = "compound"
    MULTI_HOP = "multi_hop"
    COMPARATIVE = "comparative"
    TEMPORAL = "temporal"
    CAUSAL = "causal"
    HYPOTHETICAL = "hypothetical"


class SubQuery(BaseModel):
    """Individual sub-query in decomposition."""

    query_text: str = Field(description="The sub-query text")
    query_type: QueryType = Field(description="Type of this sub-query")
    priority: int = Field(
        ge=1, le=5, description="Priority level (1=highest, 5=lowest)"
    )
    dependencies: list[int] = Field(
        default_factory=list, description="Indices of sub-queries this depends on"
    )
    expected_info_type: str = Field(description="Type of information expected")
    reasoning: str = Field(description="Why this sub-query is needed")


class QueryDecomposition(BaseModel):
    """Complete query decomposition result."""

    original_query: str = Field(description="Original complex query")
    query_type: QueryType = Field(description="Type of the original query")
    complexity_score: float = Field(
        ge=0.0, le=1.0, description="Query complexity (0-1)"
    )

    sub_queries: list[SubQuery] = Field(description="List of decomposed sub-queries")
    execution_order: list[int] = Field(
        description="Suggested execution order (indices)"
    )

    synthesis_strategy: str = Field(description="How to combine results")
    estimated_difficulty: Literal["easy", "moderate", "hard", "very_hard"] = Field(
        description="Estimated difficulty level"
    )

    reasoning: str = Field(description="Overall decomposition reasoning")
    alternative_approaches: list[str] = Field(
        default_factory=list, description="Alternative decomposition approaches"
    )


class HierarchicalDecomposition(BaseModel):
    """Hierarchical query decomposition with levels."""

    original_query: str = Field(description="Original query")

    # Hierarchical structure
    main_question: str = Field(description="Primary question to answer")
    sub_questions: list[str] = Field(description="Supporting sub-questions")
    detail_questions: list[str] = Field(description="Detailed follow-up questions")

    # Execution strategy
    execution_levels: list[list[int]] = Field(
        description="Execution levels (parallel within level, sequential between levels)"
    )
    dependency_map: dict[str, list[str]] = Field(
        description="Dependencies between questions"
    )

    # Integration strategy
    synthesis_plan: str = Field(description="How to synthesize answers")
    confidence_level: float = Field(
        ge=0.0, le=1.0, description="Confidence in decomposition"
    )


class ContextualDecomposition(BaseModel):
    """Context-aware query decomposition."""

    original_query: str = Field(description="Original query")
    context_analysis: str = Field(description="Analysis of available context")

    # Context-driven sub-queries
    context_dependent_queries: list[str] = Field(
        description="Queries that require context"
    )
    context_independent_queries: list[str] = Field(
        description="Queries that can be answered independently"
    )

    # Strategy adaptation
    retrieval_strategy: Literal["broad", "focused", "mixed"] = Field(
        description="Recommended retrieval strategy"
    )
    context_sufficiency: float = Field(
        ge=0.0, le=1.0, description="How sufficient current context is"
    )

    missing_context_queries: list[str] = Field(
        default_factory=list, description="Queries to gather missing context"
    )


# Enhanced prompts for query decomposition
BASIC_DECOMPOSITION_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert at breaking down complex queries into simpler, manageable sub-queries.

Your goal is to decompose complex questions into a series of simpler questions that, when answered together, fully address the original query.

**DECOMPOSITION PRINCIPLES:**
1. Each sub-query should be specific and focused
2. Sub-queries should be logically ordered
3. Dependencies between sub-queries should be clear
4. The combination of answers should fully address the original query

**QUERY TYPES:**
- **Simple**: Single concept, direct answer
- **Compound**: Multiple related concepts
- **Multi-hop**: Requires reasoning across multiple steps
- **Comparative**: Comparing different entities/concepts
- **Temporal**: Involves time-based relationships
- **Causal**: Cause-and-effect relationships
- **Hypothetical**: What-if scenarios

Break down the query systematically and logically.""",
        ),
        (
            "human",
            """Decompose this complex query into manageable sub-queries:

**Query:** {query}

**Available Context (if any):**
{context_info}

**Instructions:**
1. Identify the query type and complexity
2. Break it into logical sub-queries
3. Determine execution order and dependencies
4. Suggest how to synthesize the results

Provide a structured decomposition.""",
        ),
    ]
)


HIERARCHICAL_DECOMPOSITION_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert at hierarchical query decomposition.

Create a hierarchical breakdown where:
- **Level 1**: Main question (broad, overarching)
- **Level 2**: Sub-questions (supporting the main question)
- **Level 3**: Detail questions (specific facts and details)

Each level can be processed in parallel, but levels must be processed sequentially.
Higher levels provide context for lower levels.""",
        ),
        (
            "human",
            """Create a hierarchical decomposition:

**Query:** {query}
**Context:** {retrieved_documents}

Break this into a clear hierarchy of questions that build upon each other.""",
        ),
    ]
)


CONTEXTUAL_DECOMPOSITION_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert at context-aware query decomposition.

Analyze the available context and create a decomposition strategy that:
1. Leverages existing context effectively
2. Identifies what context is missing
3. Prioritizes queries based on context availability
4. Adapts strategy based on context quality

Consider both what can be answered with current context and what requires additional retrieval.""",
        ),
        (
            "human",
            """Create a context-aware decomposition:

**Query:** {query}

**Available Context:**
{retrieved_documents}

**Additional Information:**
- Messages: {messages}
- Previous results: {previous_results}

Analyze context sufficiency and create an appropriate decomposition strategy.""",
        ),
    ]
)


ADAPTIVE_DECOMPOSITION_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an adaptive query decomposition expert.

Your decomposition strategy should adapt based on:
- Query complexity and type
- Available context and resources
- Previous decomposition results
- Time and resource constraints

Provide multiple decomposition approaches and select the best one based on the situation.""",
        ),
        (
            "human",
            """Create an adaptive decomposition strategy:

**Query:** {query}
**Context:** {retrieved_documents}
**Constraints:** {constraints}
**Previous attempts:** {previous_decompositions}

Provide the optimal decomposition approach for this situation.""",
        ),
    ]
)


class QueryDecomposerAgent(Agent):
    """Basic query decomposition agent."""

    name: str = "Query Decomposer"

    def __init__(
        self, llm_config: LLMConfig | None = None, max_sub_queries: int = 5, **kwargs
    ):
        """Initialize query decomposer.

        Args:
            llm_config: LLM configuration
            max_sub_queries: Maximum number of sub-queries to generate
            **kwargs: Additional agent arguments
        """
        self.llm_config = llm_config or AzureLLMConfig(
            deployment_name="gpt-4",
            azure_endpoint="${AZURE_OPENAI_API_BASE}",
            api_key="${AZURE_OPENAI_API_KEY}",
        )
        self.max_sub_queries = max_sub_queries
        super().__init__(**kwargs)

    def build_graph(self) -> BaseGraph:
        """Build query decomposition graph."""
        graph = BaseGraph(name="QueryDecomposer")

        # Create decomposition engine
        decomposition_engine = AugLLMConfig(
            llm_config=self.llm_config,
            prompt_template=BASIC_DECOMPOSITION_PROMPT,
            structured_output_model=QueryDecomposition,
            output_key="query_decomposition",
        )

        def decompose_query(state: dict[str, Any]) -> dict[str, Any]:
            """Decompose complex query into sub-queries."""
            query = getattr(state, "query", "")
            retrieved_documents = getattr(state, "retrieved_documents", [])

            # Format context info
            context_info = ""
            if retrieved_documents:
                context_info = (
                    f"Available documents: {len(retrieved_documents)} documents"
                )
                context_info += (
                    f"\nSample content: {retrieved_documents[0].page_content[:200]}..."
                    if retrieved_documents
                    else ""
                )
            else:
                context_info = "No context documents available"

            # Get decomposition
            decomposition = decomposition_engine.invoke(
                {"query": query, "context_info": context_info}
            )

            # Limit number of sub-queries
            if len(decomposition.sub_queries) > self.max_sub_queries:
                decomposition.sub_queries = decomposition.sub_queries[
                    : self.max_sub_queries
                ]
                decomposition.execution_order = decomposition.execution_order[
                    : self.max_sub_queries
                ]

            # Extract sub-query texts for easy access
            sub_query_texts = [sq.query_text for sq in decomposition.sub_queries]

            return {
                "query_decomposition": decomposition,
                "sub_queries": sub_query_texts,
                "execution_order": decomposition.execution_order,
                "needs_decomposition": len(sub_query_texts) > 1,
                "complexity_score": decomposition.complexity_score,
                "synthesis_strategy": decomposition.synthesis_strategy,
            }

        graph.add_node("decompose", decompose_query)
        graph.add_edge(START, "decompose")
        graph.add_edge("decompose", END)

        return graph


class HierarchicalQueryDecomposerAgent(Agent):
    """Hierarchical query decomposition agent."""

    name: str = "Hierarchical Query Decomposer"

    def __init__(
        self, llm_config: LLMConfig | None = None, max_levels: int = 3, **kwargs
    ):
        """Initialize hierarchical query decomposer.

        Args:
            llm_config: LLM configuration
            max_levels: Maximum hierarchy levels
            **kwargs: Additional agent arguments
        """
        self.llm_config = llm_config or AzureLLMConfig(
            deployment_name="gpt-4",
            azure_endpoint="${AZURE_OPENAI_API_BASE}",
            api_key="${AZURE_OPENAI_API_KEY}",
        )
        self.max_levels = max_levels
        super().__init__(**kwargs)

    def build_graph(self) -> BaseGraph:
        """Build hierarchical decomposition graph."""
        graph = BaseGraph(name="HierarchicalQueryDecomposer")

        # Create hierarchical decomposition engine
        decomposition_engine = AugLLMConfig(
            llm_config=self.llm_config,
            prompt_template=HIERARCHICAL_DECOMPOSITION_PROMPT,
            structured_output_model=HierarchicalDecomposition,
            output_key="hierarchical_decomposition",
        )

        def hierarchical_decompose(state: dict[str, Any]) -> dict[str, Any]:
            """Create hierarchical decomposition."""
            query = getattr(state, "query", "")
            retrieved_documents = getattr(state, "retrieved_documents", [])

            # Format documents
            doc_context = (
                "\n\n".join(
                    [
                        f"Document {i+1}: {doc.page_content[:300]}..."
                        for i, doc in enumerate(retrieved_documents[:3])
                    ]
                )
                if retrieved_documents
                else "No documents available"
            )

            # Get hierarchical decomposition
            decomposition = decomposition_engine.invoke(
                {"query": query, "retrieved_documents": doc_context}
            )

            # Build execution plan
            all_questions = [
                decomposition.main_question,
                *decomposition.sub_questions,
                *decomposition.detail_questions,
            ]

            return {
                "hierarchical_decomposition": decomposition,
                "main_question": decomposition.main_question,
                "sub_questions": decomposition.sub_questions,
                "detail_questions": decomposition.detail_questions,
                "all_questions": all_questions,
                "execution_levels": decomposition.execution_levels,
                "synthesis_plan": decomposition.synthesis_plan,
                "hierarchy_confidence": decomposition.confidence_level,
            }

        graph.add_node("hierarchical_decompose", hierarchical_decompose)
        graph.add_edge(START, "hierarchical_decompose")
        graph.add_edge("hierarchical_decompose", END)

        return graph


class ContextualQueryDecomposerAgent(Agent):
    """Context-aware query decomposition agent."""

    name: str = "Contextual Query Decomposer"

    def __init__(
        self,
        llm_config: LLMConfig | None = None,
        context_threshold: float = 0.7,
        **kwargs,
    ):
        """Initialize contextual query decomposer.

        Args:
            llm_config: LLM configuration
            context_threshold: Threshold for context sufficiency
            **kwargs: Additional agent arguments
        """
        self.llm_config = llm_config or AzureLLMConfig(
            deployment_name="gpt-4",
            azure_endpoint="${AZURE_OPENAI_API_BASE}",
            api_key="${AZURE_OPENAI_API_KEY}",
        )
        self.context_threshold = context_threshold
        super().__init__(**kwargs)

    def build_graph(self) -> BaseGraph:
        """Build contextual decomposition graph."""
        graph = BaseGraph(name="ContextualQueryDecomposer")

        # Create contextual decomposition engine
        decomposition_engine = AugLLMConfig(
            llm_config=self.llm_config,
            prompt_template=CONTEXTUAL_DECOMPOSITION_PROMPT,
            structured_output_model=ContextualDecomposition,
            output_key="contextual_decomposition",
        )

        def contextual_decompose(state: dict[str, Any]) -> dict[str, Any]:
            """Create context-aware decomposition."""
            query = getattr(state, "query", "")
            retrieved_documents = getattr(state, "retrieved_documents", [])
            messages = getattr(state, "messages", [])
            previous_results = getattr(state, "previous_results", "")

            # Format inputs
            doc_context = (
                "\n\n".join(
                    [
                        f"Doc {i+1}: {doc.page_content[:200]}..."
                        for i, doc in enumerate(retrieved_documents[:5])
                    ]
                )
                if retrieved_documents
                else "No documents"
            )

            message_context = str(messages[-3:]) if messages else "No previous messages"

            # Get contextual decomposition
            decomposition = decomposition_engine.invoke(
                {
                    "query": query,
                    "retrieved_documents": doc_context,
                    "messages": message_context,
                    "previous_results": str(previous_results),
                }
            )

            # Determine strategy based on context sufficiency
            needs_more_context = (
                decomposition.context_sufficiency < self.context_threshold
            )

            return {
                "contextual_decomposition": decomposition,
                "context_dependent_queries": decomposition.context_dependent_queries,
                "context_independent_queries": decomposition.context_independent_queries,
                "missing_context_queries": decomposition.missing_context_queries,
                "context_sufficiency": decomposition.context_sufficiency,
                "needs_more_context": needs_more_context,
                "retrieval_strategy": decomposition.retrieval_strategy,
                "recommended_approach": (
                    "gather_context" if needs_more_context else "proceed_with_current"
                ),
            }

        graph.add_node("contextual_decompose", contextual_decompose)
        graph.add_edge(START, "contextual_decompose")
        graph.add_edge("contextual_decompose", END)

        return graph


class AdaptiveQueryDecomposerAgent(Agent):
    """Adaptive query decomposition that selects best strategy."""

    name: str = "Adaptive Query Decomposer"

    def __init__(
        self,
        llm_config: LLMConfig | None = None,
        enable_fallback: bool = True,
        **kwargs,
    ):
        """Initialize adaptive query decomposer.

        Args:
            llm_config: LLM configuration
            enable_fallback: Whether to fallback to simpler decomposition if needed
            **kwargs: Additional agent arguments
        """
        self.llm_config = llm_config or AzureLLMConfig(
            deployment_name="gpt-4",
            azure_endpoint="${AZURE_OPENAI_API_BASE}",
            api_key="${AZURE_OPENAI_API_KEY}",
        )
        self.enable_fallback = enable_fallback
        super().__init__(**kwargs)

    def build_graph(self) -> BaseGraph:
        """Build adaptive decomposition graph."""
        graph = BaseGraph(name="AdaptiveQueryDecomposer")

        def adaptive_decompose(state: dict[str, Any]) -> dict[str, Any]:
            """Adaptively choose decomposition strategy."""
            query = getattr(state, "query", "")
            retrieved_documents = getattr(state, "retrieved_documents", [])
            constraints = getattr(state, "constraints", {})
            getattr(state, "previous_decompositions", [])

            # Analyze query to choose strategy
            query_length = len(query.split())
            has_context = len(retrieved_documents) > 0
            has_constraints = bool(constraints)

            # Choose decomposition strategy
            if query_length < 10 and not has_constraints:
                # Simple query - basic decomposition
                strategy = "basic"
                decomposer = QueryDecomposerAgent(llm_config=self.llm_config)
            elif has_context and len(retrieved_documents) > 3:
                # Rich context - contextual decomposition
                strategy = "contextual"
                decomposer = ContextualQueryDecomposerAgent(llm_config=self.llm_config)
            elif (
                "step" in query.lower()
                or "first" in query.lower()
                or "then" in query.lower()
            ):
                # Sequential indicators - hierarchical decomposition
                strategy = "hierarchical"
                decomposer = HierarchicalQueryDecomposerAgent(
                    llm_config=self.llm_config
                )
            else:
                # Default to basic decomposition
                strategy = "basic"
                decomposer = QueryDecomposerAgent(llm_config=self.llm_config)

            # Execute chosen strategy
            try:
                result = decomposer.run(state)

                # Add strategy metadata
                result_dict = result if isinstance(result, dict) else {"result": result}
                result_dict.update(
                    {
                        "decomposition_strategy_used": strategy,
                        "adaptive_choice_reasoning": f"Selected {strategy} based on query analysis",
                        "fallback_available": self.enable_fallback,
                        "strategy_confidence": 0.8,  # Could be improved with more sophisticated analysis
                    }
                )

                return result_dict

            except Exception as e:
                if self.enable_fallback:
                    logger.warning(
                        f"Decomposition strategy {strategy} failed, falling back to basic: {e}"
                    )
                    # Fallback to basic decomposition
                    basic_decomposer = QueryDecomposerAgent(llm_config=self.llm_config)
                    result = basic_decomposer.run(state)

                    result_dict = (
                        result if isinstance(result, dict) else {"result": result}
                    )
                    result_dict.update(
                        {
                            "decomposition_strategy_used": "basic_fallback",
                            "original_strategy": strategy,
                            "fallback_reason": str(e),
                            "strategy_confidence": 0.6,
                        }
                    )
                    return result_dict
                raise

        graph.add_node("adaptive_decompose", adaptive_decompose)
        graph.add_edge(START, "adaptive_decompose")
        graph.add_edge("adaptive_decompose", END)

        return graph


# Factory functions for easy creation
def create_query_decomposer(
    decomposer_type: Literal[
        "basic", "hierarchical", "contextual", "adaptive"
    ] = "basic",
    llm_config: LLMConfig | None = None,
    **kwargs,
) -> Agent:
    """Create a query decomposer agent.

    Args:
        decomposer_type: Type of decomposer to create
        llm_config: LLM configuration
        **kwargs: Additional arguments

    Returns:
        Configured query decomposer agent
    """
    if decomposer_type == "basic":
        return QueryDecomposerAgent(llm_config=llm_config, **kwargs)
    if decomposer_type == "hierarchical":
        return HierarchicalQueryDecomposerAgent(llm_config=llm_config, **kwargs)
    if decomposer_type == "contextual":
        return ContextualQueryDecomposerAgent(llm_config=llm_config, **kwargs)
    if decomposer_type == "adaptive":
        return AdaptiveQueryDecomposerAgent(llm_config=llm_config, **kwargs)
    raise ValueError(f"Unknown decomposer type: {decomposer_type}")


# I/O schema for compatibility checking
def get_query_decomposer_io_schema() -> dict[str, list[str]]:
    """Get I/O schema for query decomposers for compatibility checking."""
    return {
        "inputs": [
            "query",
            "retrieved_documents",
            "messages",
            "previous_results",
            "constraints",
            "previous_decompositions",
        ],
        "outputs": [
            "query_decomposition",
            "hierarchical_decomposition",
            "contextual_decomposition",
            "sub_queries",
            "execution_order",
            "needs_decomposition",
            "complexity_score",
            "synthesis_strategy",
            "main_question",
            "sub_questions",
            "detail_questions",
            "all_questions",
            "context_dependent_queries",
            "context_independent_queries",
            "missing_context_queries",
            "needs_more_context",
            "decomposition_strategy_used",
        ],
    }
