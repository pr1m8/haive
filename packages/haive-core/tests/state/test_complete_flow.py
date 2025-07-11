#!/usr/bin/env python3
"""Complete test of the schema fix to verify the full flow works."""

import asyncio
import sys

sys.path.insert(0, "/home/will/Projects/haive/backend/haive")

from haive.agents.simple.agent_v2 import SimpleAgentV2
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from haive.core.engine.aug_llm import AugLLMConfig


# Define test models
class QueryRefinementSuggestion(BaseModel):
    """Individual query refinement suggestion."""

    refined_query: str = Field(description="The refined/improved query")
    improvement_type: str = Field(description="Type of improvement made")
    rationale: str = Field(description="Why this refinement improves the query")
    expected_benefit: str = Field(
        description="Expected improvement in retrieval or answering"
    )


class QueryRefinementResponse(BaseModel):
    """Query refinement analysis and suggestions."""

    original_query: str = Field(description="The original user query")
    query_analysis: str = Field(
        description="Analysis of the original query's strengths and weaknesses"
    )
    query_type: str = Field(description="Classification of query type")
    complexity_level: str = Field(description="simple, moderate, or complex")
    refinement_suggestions: list[QueryRefinementSuggestion] = Field(
        description="List of suggested query improvements"
    )
    best_refined_query: str = Field(description="The recommended best refined query")
    search_strategy_recommendations: list[str] = Field(
        description="Recommendations for search strategy"
    )


# Simple prompt template
RAG_QUERY_REFINEMENT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert query optimization specialist. Analyze and refine user queries.",
        ),
        ("human", "Analyze and refine the following user query: {query}"),
    ]
)


async def test_complete_flow():
    """Test the complete flow works end-to-end."""

    # Create agent with structured output
    agent = SimpleAgentV2(
        name="test_agent",
        engine=AugLLMConfig(
            prompt_template=RAG_QUERY_REFINEMENT,
            structured_output_model=QueryRefinementResponse,
            structured_output_version="v2",
        ),
    )


    # Test run
    try:
        result = await agent.arun({"query": "what is the tallest building in france"})

        # Check for the expected field
        expected_field = "query_refinement_response"
        if hasattr(result, "keys") and expected_field in result:
            field_value = result[expected_field]
            if isinstance(field_value, QueryRefinementResponse):
            else:
        else:

        return True

    except Exception as e:
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(test_complete_flow())
