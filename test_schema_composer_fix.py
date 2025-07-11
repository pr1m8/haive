#!/usr/bin/env python3
"""Test the schema composer fix for engine field handling."""

import asyncio

from haive.agents.simple.agent_v2 import SimpleAgentV2
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field


# Test model like in the notebook
class QueryRefinementResponse(BaseModel):
    """Query refinement analysis and suggestions."""

    original_query: str = Field(description="The original user query")
    best_refined_query: str = Field(description="The recommended best refined query")


# Test prompt template like in the notebook
RAG_QUERY_REFINEMENT = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an expert query optimization specialist."),
        ("human", "Analyze and refine: {query}"),
    ]
)


async def test_schema_composer_fix():
    """Test that schema composer correctly handles engine field with LLMState."""

    # Create the same setup as the notebook
    config = AugLLMConfig(
        prompt_template=RAG_QUERY_REFINEMENT,
        structured_output_model=QueryRefinementResponse,
        structured_output_version="v2",
    )

    agent = SimpleAgentV2(name="test_schema_composer", engine=config)


    # Check the schema fields
    if hasattr(agent.state_schema, "model_fields"):

        # Check if we have engine field from LLMState but not duplicated
        if "engine" in agent.state_schema.model_fields:
            pass")
        else:
            pass")

        # Check if we have query field from prompt template
        if "query" in agent.state_schema.model_fields:
            pass")
        else:
            pass")

    # Check input schema separately
    if hasattr(agent.input_schema, "model_fields"):

        # Engine should NOT be in input schema
        if "engine" in agent.input_schema.model_fields:
            pass")
        else:
            pass")

        # Query should be in input schema
        if "query" in agent.input_schema.model_fields:
            pass")
        else:
            pass")

    # Check if state schema has derive_input_schema method
    if hasattr(agent.state_schema, "derive_input_schema"):
        pass")
    else:
        pass")

    # Test input schema creation manually
    try:
        input_instance = agent.input_schema(query="test query")

        # Check if the input instance can be used to create state
        agent.state_schema(**input_instance.model_dump())

    except Exception as e:

    # Test actual usage with string input first
    try:
        result = await agent.arun("what is the tallest building in france")
        return True
    except Exception as e:

        # Try with dict input
        try:
            result = await agent.arun(
                {"query": "what is the tallest building in france"}
            )
            return True
        except Exception as e2:
            return False


if __name__ == "__main__":
    success = asyncio.run(test_schema_composer_fix())
    if success:
        pass!")
    else:
        passs")
