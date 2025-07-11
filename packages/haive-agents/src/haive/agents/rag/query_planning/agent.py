"""Query Planning Agentic RAG Agent.

Implementation of query planning RAG with structured decomposition and execution.
Provides intelligent query analysis, planning, and multi-stage retrieval strategies.
"""

import logging
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.models.llm.base import AzureLLMConfig, LLMConfig
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import END, START
from pydantic import BaseModel, Field

from haive.agents.base.agent import Agent
from haive.agents.simple.agent import SimpleAgent

logger = logging.getLogger(__name__)


class QueryComplexity(str, Enum):
    """Query complexity levels."""

    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    MULTI_FACETED = "multi_faceted"


class QueryType(str, Enum):
    """Types of queries for planning."""

    FACTUAL = "factual"
    ANALYTICAL = "analytical"
    COMPARATIVE = "comparative"
    EXPLORATORY = "exploratory"
    PROCEDURAL = "procedural"
    CONCEPTUAL = "conceptual"


class SubQuery(BaseModel):
    """Individual sub-query in a decomposed plan."""

    query_id: str = Field(description="Unique identifier for this sub-query")
    query_text: str = Field(description="The sub-query text")
    query_type: QueryType = Field(description="Type of this sub-query")

    dependencies: list[str] = Field(description="IDs of sub-queries this depends on")
    priority: int = Field(ge=1, le=10, description="Priority level (1=highest)")

    expected_info: str = Field(description="What information this should retrieve")
    success_criteria: str = Field(description="How to determine if successful")

    retrieval_strategy: str = Field(description="Suggested retrieval approach")
    estimated_difficulty: float = Field(
        ge=0.0, le=1.0, description="Estimated difficulty"
    )


class QueryPlan(BaseModel):
    """Complete query execution plan."""

    original_query: str = Field(description="Original user query")
    query_complexity: QueryComplexity = Field(description="Overall query complexity")
    primary_intent: str = Field(description="Primary intent of the query")

    # Decomposition
    sub_queries: list[SubQuery] = Field(description="Decomposed sub-queries")
    execution_order: list[str] = Field(description="Order to execute sub-queries")
    parallel_groups: list[list[str]] = Field(
        description="Groups that can run in parallel"
    )

    # Strategy
    retrieval_strategy: str = Field(description="Overall retrieval strategy")
    synthesis_approach: str = Field(description="How to combine sub-query results")
    fallback_plan: str = Field(description="Fallback if primary plan fails")

    # Resource planning
    estimated_time: float = Field(description="Estimated total execution time")
    estimated_retrievals: int = Field(description="Estimated number of retrievals")
    resource_requirements: dict[str, Any] = Field(description="Required resources")

    planning_confidence: float = Field(ge=0.0, le=1.0, description="Confidence in plan")
    planning_rationale: str = Field(description="Rationale for this plan")


class SubQueryResult(BaseModel):
    """Result from executing a sub-query."""

    query_id: str = Field(description="ID of the executed sub-query")
    query_text: str = Field(description="The sub-query that was executed")

    # Execution details
    execution_successful: bool = Field(description="Whether execution succeeded")
    execution_time: float = Field(description="Time taken to execute")
    retrieval_count: int = Field(description="Number of documents retrieved")

    # Results
    answer: str = Field(description="Answer to the sub-query")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence in answer")
    supporting_documents: list[Document] = Field(description="Supporting documents")

    # Quality metrics
    relevance_score: float = Field(ge=0.0, le=1.0, description="Relevance of results")
    completeness_score: float = Field(
        ge=0.0, le=1.0, description="Completeness of answer"
    )

    metadata: dict[str, Any] = Field(description="Additional metadata")


class QueryPlanningResult(BaseModel):
    """Complete result from query planning execution."""

    original_query: str = Field(description="Original query")
    final_answer: str = Field(description="Final synthesized answer")

    # Planning analytics
    query_plan: QueryPlan = Field(description="The executed query plan")
    plan_execution_rate: float = Field(
        ge=0.0, le=1.0, description="How much of plan was executed"
    )
    plan_success_rate: float = Field(
        ge=0.0, le=1.0, description="Success rate of sub-queries"
    )

    # Execution analytics
    sub_query_results: list[SubQueryResult] = Field(description="All sub-query results")
    total_execution_time: float = Field(description="Total execution time")
    total_retrievals: int = Field(description="Total documents retrieved")

    # Quality metrics
    answer_confidence: float = Field(
        ge=0.0, le=1.0, description="Confidence in final answer"
    )
    answer_completeness: float = Field(
        ge=0.0, le=1.0, description="Completeness of answer"
    )
    synthesis_quality: float = Field(ge=0.0, le=1.0, description="Quality of synthesis")

    # Process insights
    bottlenecks: list[str] = Field(description="Identified bottlenecks")
    improvements: list[str] = Field(description="Suggested improvements")

    execution_metadata: dict[str, Any] = Field(description="Execution metadata")


# Enhanced prompts for query planning
QUERY_PLANNING_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            """system""",
            """You are an expert query planner for RAG systems.

**QUERY PLANNING PRINCIPLES:**
1. **Decomposition**: Break complex queries into atomic, answerable sub-queries
2. **Dependencies**: Identify which sub-queries depend on others
3. **Parallelization**: Determine what can be executed in parallel
4. **Prioritization**: Order sub-queries by importance and dependencies
5. **Strategy**: Select optimal retrieval strategies for each component

**QUERY COMPLEXITY ANALYSIS:**
- **Simple**: Single fact or direct lookup
- **Moderate**: 2-3 related concepts or comparisons
- **Complex**: Multiple facets requiring integration
- **Multi-faceted**: Broad exploratory queries with many aspects

**DECOMPOSITION STRATEGIES:**
1. **Temporal**: Break by time periods or sequences
2. **Conceptual**: Separate by distinct concepts
3. **Hierarchical**: From general to specific
4. **Comparative**: Isolate items being compared
5. **Procedural**: Step-by-step breakdowns

**EXECUTION PLANNING:**
- Identify critical path through sub-queries
- Group independent queries for parallel execution
- Plan fallbacks for likely failure points
- Estimate resource requirements
- Design synthesis approach upfront

Create comprehensive, executable query plans.""",
        ),
        (
            """human""",
            """Create a query execution plan:

**Query:** {query}

**Context:** {context}

**Available Resources:** {available_resources}

**Requirements:** {requirements}

**PLANNING TASK:**
1. Analyze query complexity and intent
2. Decompose into atomic sub-queries
3. Identify dependencies and execution order
4. Plan retrieval strategies for each component
5. Design synthesis approach for combining results
6. Estimate resource requirements and timing

Provide a complete, actionable query plan.""",
        ),
    ]
)


SUB_QUERY_EXECUTION_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            """system""",
            """You are an expert at executing sub-queries in a query plan.

**EXECUTION PRINCIPLES:**
1. **Focus**: Execute exactly the specified sub-query
2. **Context**: Use results from dependent queries appropriately
3. **Precision**: Retrieve only relevant information
4. **Efficiency**: Minimize retrieval operations
5. **Quality**: Ensure high-quality, complete answers

**EXECUTION STRATEGIES:**
- Direct retrieval for factual queries
- Multi-hop reasoning for complex queries
- Comparative analysis for comparison queries
- Exploratory search for open-ended queries
- Synthesis for conceptual queries

**QUALITY CONTROL:**
- Verify answer addresses the specific sub-query
- Check completeness against success criteria
- Validate with supporting evidence
- Assess confidence based on evidence quality
- Track execution metrics

Execute sub-queries with precision and efficiency.""",
        ),
        (
            """human""",
            """Execute this sub-query:

**Sub-Query:** {sub_query}

**Query Type:** {query_type}

**Expected Information:** {expected_info}

**Success Criteria:** {success_criteria}

**Dependent Results:** {dependent_results}

**Available Documents:** {documents_summary}

**EXECUTION TASK:**
1. Retrieve relevant information for this specific sub-query
2. Consider results from dependent queries if applicable
3. Generate precise answer meeting success criteria
4. Assess confidence and completeness
5. Track execution metrics

Focus on this sub-query only, not the broader context.""",
        ),
    ]
)


QUERY_SYNTHESIS_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            """system""",
            """You are an expert at synthesizing sub-query results into comprehensive answers.

**SYNTHESIS PRINCIPLES:**
1. **Integration**: Combine all sub-query results coherently
2. **Completeness**: Ensure all aspects of original query are addressed
3. **Coherence**: Create a unified, flowing response
4. **Accuracy**: Maintain factual accuracy from sub-results
5. **Clarity**: Present information clearly and logically

**SYNTHESIS STRATEGIES:**
- **Hierarchical**: Build from foundational to complex
- **Thematic**: Organize by themes or topics
- **Chronological**: Order by time sequence
- **Comparative**: Highlight comparisons and contrasts
- **Analytical**: Draw insights and conclusions

**QUALITY ASSESSMENT:**
- Check coverage of all query aspects
- Verify consistency across sub-results
- Assess overall answer quality
- Identify any gaps or weaknesses
- Suggest improvements for future

Create comprehensive, high-quality synthesized answers.""",
        ),
        (
            """human""",
            """Synthesize sub-query results into final answer:

**Original Query:** {original_query}

**Query Plan:** {query_plan_summary}

**Sub-Query Results:** {sub_query_results}

**Execution Statistics:** {execution_stats}

**Synthesis Approach:** {synthesis_approach}

**SYNTHESIS TASK:**
1. Integrate all sub-query answers coherently
2. Ensure complete coverage of original query
3. Resolve any conflicts between sub-results
4. Create clear, comprehensive final answer
5. Assess overall quality and completeness

Generate the best possible answer from all available sub-results.""",
        ),
    ]
)


class QueryPlanningRAGAgent(Agent):
    """Query Planning RAG agent with structured decomposition and execution.

    This agent uses conditional edges to execute sub-queries in a planned order.
    """

    name: str = "Query Planning RAG Agent"
    documents: list[Document] = Field(description="Documents for retrieval")
    llm_config: LLMConfig = Field(description="LLM configuration")
    planning_depth: int = Field(
        default=3, description="Maximum depth of query decomposition"
    )

    # Engines for different stages (initialized in setup_agent)
    planning_engine: AugLLMConfig | None = Field(
        default=None, description="Engine for query planning"
    )
    execution_engine: AugLLMConfig | None = Field(
        default=None, description="Engine for sub-query execution"
    )
    synthesis_engine: AugLLMConfig | None = Field(
        default=None, description="Engine for result synthesis"
    )

    def setup_agent(self) -> None:
        """Initialize engines."""
        # Create planning engine
        self.planning_engine = AugLLMConfig(
            llm_config=self.llm_config,
            prompt_template=QUERY_PLANNING_PROMPT,
            structured_output_model=QueryPlan,
            output_key="query_plan",
        )

        # Create execution engine
        self.execution_engine = AugLLMConfig(
            llm_config=self.llm_config,
            prompt_template=SUB_QUERY_EXECUTION_PROMPT,
            structured_output_model=SubQueryResult,
            output_key="sub_query_result",
        )

        # Create synthesis engine
        self.synthesis_engine = AugLLMConfig(
            llm_config=self.llm_config,
            prompt_template=QUERY_SYNTHESIS_PROMPT,
            structured_output_model=QueryPlanningResult,
            output_key="planning_result",
        )

        # Add engines to registry
        self.engines["planning"] = self.planning_engine
        self.engines["execution"] = self.execution_engine
        self.engines["synthesis"] = self.synthesis_engine

    @classmethod
    def from_documents(
        cls,
        documents: list[Document],
        llm_config: LLMConfig | None = None,
        planning_depth: int = 3,
        **kwargs,
    ):
        """Create Query Planning RAG agent from documents.

        Args:
            documents: Documents to index for retrieval
            llm_config: LLM configuration
            planning_depth: Maximum depth of query decomposition
            **kwargs: Additional arguments

        Returns:
            QueryPlanningRAGAgent instance
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
            planning_depth=planning_depth,
            **kwargs,
        )

    def create_query_plan(self, state: dict[str, Any]) -> dict[str, Any]:
        """Create a query execution plan."""
        query = state.get("query", "")
        context = state.get("context", "")

        logger.info("Creating query execution plan...")
        query_plan = self.planning_engine.invoke(
            {
                "query": query,
                "context": context,
                "available_resources": f"{len(self.documents)} documents",
                "requirements": f"Planning depth: {self.planning_depth}",
            }
        )

        logger.info(f"Query plan created: {len(query_plan.sub_queries)} sub-queries")

        return {
            "query_plan": query_plan,
            "sub_query_results": [],
            "current_sub_query_idx": 0,
            "results_by_id": {},
        }

    def execute_sub_query(self, state: dict[str, Any]) -> dict[str, Any]:
        """Execute the current sub-query."""
        query_plan = state.get("query_plan")
        current_idx = state.get("current_sub_query_idx", 0)
        results_by_id = state.get("results_by_id", {})
        sub_results = state.get("sub_query_results", [])

        if (
            current_idx >= len(query_plan.execution_order)
            or current_idx >= self.planning_depth
        ):
            return state  # No more sub-queries to execute

        query_id = query_plan.execution_order[current_idx]
        sub_query = next(
            (sq for sq in query_plan.sub_queries if sq.query_id == query_id), None
        )

        if not sub_query:
            return {**state, "current_sub_query_idx": current_idx + 1}

        # Get dependent results
        dependent_results = {}
        for dep_id in sub_query.dependencies:
            if dep_id in results_by_id:
                dependent_results[dep_id] = results_by_id[dep_id].answer

        logger.info(f"Executing sub-query: {sub_query.query_id}")

        try:
            # Execute sub-query
            sub_result = self.execution_engine.invoke(
                {
                    "sub_query": sub_query.query_text,
                    "query_type": sub_query.query_type.value,
                    "expected_info": sub_query.expected_info,
                    "success_criteria": sub_query.success_criteria,
                    "dependent_results": str(dependent_results),
                    "documents_summary": f"{len(self.documents)} documents available",
                }
            )

            sub_results.append(sub_result)
            results_by_id[query_id] = sub_result

        except Exception as e:
            logger.exception(f"Sub-query execution failed: {e}")
            # Create failed result
            failed_result = SubQueryResult(
                query_id=query_id,
                query_text=sub_query.query_text,
                execution_successful=False,
                execution_time=0.0,
                retrieval_count=0,
                answer=f"Execution failed: {e!s}",
                confidence=0.0,
                supporting_documents=[],
                relevance_score=0.0,
                completeness_score=0.0,
                metadata={"error": str(e)},
            )
            sub_results.append(failed_result)
            results_by_id[query_id] = failed_result

        return {
            **state,
            "sub_query_results": sub_results,
            "results_by_id": results_by_id,
            "current_sub_query_idx": current_idx + 1,
        }

    def should_continue_execution(self, state: dict[str, Any]) -> str:
        """Determine if more sub-queries should be executed."""
        query_plan = state.get("query_plan")
        current_idx = state.get("current_sub_query_idx", 0)

        if (
            current_idx < len(query_plan.execution_order)
            and current_idx < self.planning_depth
        ):
            return "execute_sub_query"
        return "synthesize_results"

    def synthesize_results(self, state: dict[str, Any]) -> dict[str, Any]:
        """Synthesize sub-query results into final answer."""
        query = state.get("query", "")
        query_plan = state.get("query_plan")
        sub_results = state.get("sub_query_results", [])

        logger.info("Synthesizing sub-query results...")

        # Prepare sub-query results summary
        sub_results_summary = "\n\n".join(
            [
                f"Sub-Query {r.query_id}: {r.query_text}\nAnswer: {r.answer}\nConfidence: {r.confidence}"
                for r in sub_results
            ]
        )

        execution_stats = {
            "total_sub_queries": len(sub_results),
            "successful": sum(1 for r in sub_results if r.execution_successful),
            "total_time": sum(r.execution_time for r in sub_results),
            "total_retrievals": sum(r.retrieval_count for r in sub_results),
        }

        planning_result = self.synthesis_engine.invoke(
            {
                "original_query": query,
                "query_plan_summary": f"Complexity: {query_plan.query_complexity}, Sub-queries: {len(query_plan.sub_queries)}",
                "sub_query_results": sub_results_summary,
                "execution_stats": str(execution_stats),
                "synthesis_approach": query_plan.synthesis_approach,
            }
        )

        logger.info(
            f"Query planning completed: Confidence={planning_result.answer_confidence}"
        )

        return {
            "response": planning_result.final_answer,
            "planning_result": planning_result,
            "answer_confidence": planning_result.answer_confidence,
            "answer_completeness": planning_result.answer_completeness,
            "total_retrievals": planning_result.total_retrievals,
            "execution_time": planning_result.total_execution_time,
            "messages": state.get("messages", []),
        }

    def build_graph(self) -> BaseGraph:
        """Build the query planning graph with conditional edges."""
        graph = BaseGraph(name="QueryPlanningRAG")

        # Add nodes
        graph.add_node("create_plan", self.create_query_plan)
        graph.add_node("execute_sub_query", self.execute_sub_query)
        graph.add_node("synthesize_results", self.synthesize_results)

        # Connect the flow
        graph.add_edge(START, "create_plan")
        graph.add_edge("create_plan", "execute_sub_query")

        # Add conditional edge for sub-query execution loop
        graph.add_conditional_edges(
            "execute_sub_query",
            self.should_continue_execution,
            {
                "execute_sub_query": "execute_sub_query",  # Loop back
                "synthesize_results": "synthesize_results",  # Move to synthesis
            },
        )

        graph.add_edge("synthesize_results", END)

        return graph


# Factory function
def create_query_planning_rag_agent(
    documents: list[Document],
    llm_config: LLMConfig | None = None,
    planning_mode: str = "comprehensive",
    **kwargs,
) -> QueryPlanningRAGAgent:
    """Create a Query Planning RAG agent.

    Args:
        documents: Documents for retrieval
        llm_config: LLM configuration
        planning_mode: Planning mode ("simple", "moderate", "comprehensive")
        **kwargs: Additional arguments

    Returns:
        Configured Query Planning RAG agent
    """
    # Configure based on planning mode
    if planning_mode == "simple":
        kwargs.setdefault("planning_depth", 2)
    elif planning_mode == "moderate":
        kwargs.setdefault("planning_depth", 3)
    else:  # comprehensive
        kwargs.setdefault("planning_depth", 5)

    return QueryPlanningRAGAgent.from_documents(
        documents=documents, llm_config=llm_config, **kwargs
    )


# I/O schema for compatibility
def get_query_planning_rag_io_schema() -> dict[str, list[str]]:
    """Get I/O schema for Query Planning RAG agents."""
    return {
        "inputs": ["query", "context", "messages"],
        "outputs": [
            "response",
            "query_plan",
            "sub_query_results",
            "planning_result",
            "answer_confidence",
            "answer_completeness",
            "total_retrievals",
            "execution_time",
            "messages",
        ],
    }
