#!/usr/bin/env python3
"""Test to reproduce the exact issue from notebook Untitled83.ipynb."""

import logging
from typing import List, Literal, Optional

from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field


# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Define the prompt template from the notebook
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


# Define the structured output model
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


# Now test the agent creation from the notebook
try:
    from haive.agents.simple.agent_v2 import SimpleAgentV2
    from haive.core.engine.aug_llm import AugLLMConfig

    logger.info("Creating SimpleAgentV2...")

    # Create the agent with the same config as in the notebook
    agent = SimpleAgentV2(
        engine=AugLLMConfig(
            prompt_template=RAG_QUERY_REFINEMENT,
            structured_output_model=QueryRefinementResponse,
            structured_output_version="v2",
        )
    )

    logger.info("Agent created successfully")

    # Test input schema
    logger.info("Testing input schema...")
    input_schema = agent.input_schema(query="hello")
    logger.info(f"Input schema fields: {input_schema.model_fields}")

    # Test the state schema
    logger.info("Testing state schema...")
    state = agent.state_schema()
    logger.info(f"State schema fields: {list(state.model_fields.keys())}")
    logger.info(f"State engine field: {state.engine}")

    # Now try to run the agent
    logger.info("Running agent...")
    result = agent.run({"query": "what is the tallest building in france"}, debug=True)
    logger.info(f"Result: {result}")

except Exception as e:
    logger.exception(f"Error: {type(e).__name__}: {e}")
    import traceback

    traceback.print_exc()
