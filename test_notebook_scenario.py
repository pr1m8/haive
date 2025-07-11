#!/usr/bin/env python3
"""Test the exact scenario from notebooks/Untitled83.ipynb."""

import asyncio
from typing import List, Literal, Optional

from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

# Define the prompt template (from the notebook)
RAG_QUERY_REFINEMENT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert query optimization specialist for RAG systems. Your role is to analyze user queries and suggest improvements that will lead to better document retrieval and more accurate answers.

**Query Analysis Dimensions:**

1. **Clarity**: Is the query clear and unambiguous?
2. **Specificity**: Is the query specific enough to retrieve relevant documents?
3. **Scope**: Is the query scope appropriate (not too broad or narrow)?
4. **Terminology**: Does the query use appropriate domain-specific terms?
5. **Intent**: Is the user's intent clearly expressed?
6. **Context**: Is sufficient context provided for understanding?

**Refinement Strategies:**

- **Add Specificity**: Include specific terms, entities, timeframes, or constraints
- **Clarify Intent**: Make the desired outcome or answer type explicit
- **Expand Context**: Add background information that helps with retrieval
- **Use Better Terminology**: Replace colloquial terms with domain-specific language
- **Break Down Complex Queries**: Split multi-part questions into focused sub-queries
- **Add Constraints**: Include relevant filters or limitations

**Query Types to Consider:**
- Factual (seeking specific facts)
- Analytical (requiring analysis or comparison)
- Procedural (asking for step-by-step guidance)
- Conceptual (understanding abstract ideas)
- Temporal (time-based information)
- Causal (cause-and-effect relationships)

Provide multiple refinement suggestions with clear rationales.""",
        ),
        (
            "human",
            """Analyze and refine the following user query to improve retrieval and answer quality.

**Original Query:** {query}

**Context (if provided):** {context}

**Analysis Required:**
1. Analyze the current query's strengths and weaknesses
2. Classify the query type and complexity
3. Provide multiple refinement suggestions
4. Recommend the best refined query
5. Suggest optimal search strategies

Focus on improvements that will lead to better document retrieval and more comprehensive answers.""",
        ),
    ]
).partial(context="")


# Define the Pydantic models (from the notebook)
class QueryRefinementSuggestion(BaseModel):
    """Individual query refinement suggestion."""

    refined_query: str = Field(description="The refined/improved query")
    improvement_type: str = Field(
        description="Type of improvement made (clarity, specificity, scope, etc.)"
    )
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


# Import SimpleAgent v2
from haive.agents.simple.agent_v2 import SimpleAgentV2
from haive.core.engine.aug_llm import AugLLMConfig


def agent_tester(prompt, model, test_prompt):
    """Function from the notebook."""
    agent = SimpleAgentV2(
        engine=AugLLMConfig(
            prompt_template=prompt,
            structured_output_model=model,
            structured_output_version="v2",
        )
    )
    return agent


async def main():

    # Create the agent (same as notebook)
    agent = agent_tester(
        RAG_QUERY_REFINEMENT,
        QueryRefinementResponse,
        {"query": "what is the tallest building in france"},
    )

    # Check the input schema
    input_schema_fields = list(agent.input_schema(query="hello").model_fields.keys())

    # Verify no engine field in input schema
    if "engine" not in input_schema_fields and "engines" not in input_schema_fields:
        pass")
    else:
        return

    # Check state schema
    state_schema_fields = list(agent.state_schema.model_fields.keys())
    if "engine" in state_schema_fields:
        pass")

    # Test running the agent
    try:
        response = await agent.arun({"query": "what is the tallest building in france"})

        # Check the response structure
        if hasattr(response, "__dict__"):
            pass


    except Exception as e:
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
