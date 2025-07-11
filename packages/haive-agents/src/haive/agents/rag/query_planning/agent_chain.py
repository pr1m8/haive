"""Query Planning RAG using ChainAgent.

Simplified version using the new ChainAgent approach.
"""

from typing import Any, Dict, List, Optional

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig, LLMConfig
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from haive.agents.chain import ChainAgent, flow_with_edges


class QueryPlan(BaseModel):
    """Simplified query plan."""

    sub_queries: list[str] = Field(description="Sub-queries to execute")
    execution_strategy: str = Field(description="How to execute them")
    synthesis_approach: str = Field(description="How to combine results")


class SubQueryResult(BaseModel):
    """Result from a sub-query."""

    query: str = Field(description="The sub-query")
    answer: str = Field(description="Answer to the sub-query")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence")


def create_query_planning_chain(
    documents: list[Document],
    llm_config: LLMConfig | None = None,
    name: str = "Query Planning RAG",
) -> ChainAgent:
    """Create query planning RAG using ChainAgent."""
    if not llm_config:
        llm_config = AzureLLMConfig(
            deployment_name="gpt-4",
            azure_endpoint="${AZURE_OPENAI_API_BASE}",
            api_key="${AZURE_OPENAI_API_KEY}",
        )

    # Query planner
    planner = AugLLMConfig(
        llm_config=llm_config,
        prompt_template=ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """Break down complex queries into 2-3 simple sub-queries.
            Focus on atomic, answerable questions.""",
                ),
                ("human", "Query: {query}\nCreate execution plan."),
            ]
        ),
        structured_output_model=QueryPlan,
        output_key="plan",
    )

    # Sub-query executor
    def execute_sub_queries(state: dict[str, Any]) -> dict[str, Any]:
        """Execute all sub-queries."""
        plan = state.get("plan", {})
        sub_queries = plan.get("sub_queries", [])

        # Simple mock execution - in real implementation would use retrieval
        results = []
        for i, sub_query in enumerate(sub_queries[:3]):  # Limit to 3
            # Mock answer generation
            answer = f"Answer to sub-query {i+1}: {sub_query}"
            results.append({"query": sub_query, "answer": answer, "confidence": 0.8})

        return {"sub_results": results, "total_sub_queries": len(sub_queries)}

    # Result synthesizer
    synthesizer = AugLLMConfig(
        llm_config=llm_config,
        prompt_template=ChatPromptTemplate.from_messages(
            [
                ("system", "Synthesize sub-query results into a comprehensive answer"),
                (
                    "human",
                    """Original query: {query}
            Sub-query results: {sub_results}

            Create a complete, coherent response.""",
                ),
            ]
        ),
        output_key="final_response",
    )

    # Simple 3-step chain
    return ChainAgent(
        planner,  # Plan the query
        execute_sub_queries,  # Execute sub-queries
        synthesizer,  # Synthesize results
        name=name,
    )


def create_simple_decomposition_chain(
    documents: list[Document], llm_config: LLMConfig | None = None
) -> ChainAgent:
    """Even simpler version - just decompose and answer."""
    if not llm_config:
        llm_config = AzureLLMConfig(
            deployment_name="gpt-4",
            azure_endpoint="${AZURE_OPENAI_API_BASE}",
            api_key="${AZURE_OPENAI_API_KEY}",
        )

    # Step 1: Decompose query
    decomposer = AugLLMConfig(
        llm_config=llm_config,
        prompt_template=ChatPromptTemplate.from_messages(
            [("system", "Break query into 2-3 simple questions"), ("human", "{query}")]
        ),
        output_key="sub_queries",
    )

    # Step 2: Answer each (simplified)
    def answer_all(state: dict[str, Any]) -> dict[str, Any]:
        sub_queries = state.get("sub_queries", "").split("\n")
        answers = [f"Answer: {q}" for q in sub_queries if q.strip()]
        return {"answers": answers}

    # Step 3: Combine
    combiner = AugLLMConfig(
        llm_config=llm_config,
        prompt_template=ChatPromptTemplate.from_messages(
            [
                ("system", "Combine these answers into one response"),
                ("human", "Original: {query}\nAnswers: {answers}"),
            ]
        ),
        output_key="response",
    )

    return ChainAgent(decomposer, answer_all, combiner)


# With conditional execution based on complexity
def create_adaptive_planning_chain(
    documents: list[Document], llm_config: LLMConfig | None = None
) -> ChainAgent:
    """Adaptive planning based on query complexity."""
    if not llm_config:
        llm_config = AzureLLMConfig(
            deployment_name="gpt-4",
            azure_endpoint="${AZURE_OPENAI_API_BASE}",
            api_key="${AZURE_OPENAI_API_KEY}",
        )

    # Complexity analyzer
    analyzer = AugLLMConfig(
        llm_config=llm_config,
        prompt_template=ChatPromptTemplate.from_messages(
            [
                ("system", "Rate query complexity: 'simple' or 'complex'"),
                ("human", "{query}"),
            ]
        ),
        output_key="complexity",
    )

    # Simple answering
    simple_answer = AugLLMConfig(
        llm_config=llm_config,
        prompt_template=ChatPromptTemplate.from_messages(
            [("system", "Answer this simple query directly"), ("human", "{query}")]
        ),
        output_key="response",
    )

    # Complex planning chain
    complex_planning = create_query_planning_chain(
        documents, llm_config, "Complex Planning"
    )

    # Route based on complexity
    return flow_with_edges(
        [analyzer, simple_answer, complex_planning],
        (0, {"simple": 1, "complex": 2}, lambda s: s.get("complexity", "simple")),
    )


# I/O schema
def get_query_planning_chain_io_schema() -> dict[str, list[str]]:
    """Get I/O schema for query planning chain."""
    return {
        "inputs": ["query", "context", "messages"],
        "outputs": ["plan", "sub_results", "final_response", "response", "messages"],
    }
