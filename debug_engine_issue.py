#!/usr/bin/env python3
"""Debug the engine validation issue in SimpleAgent V2."""

import logging
from typing import List, Literal, Optional

from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

# Disable noisy logs
logging.getLogger("haive.dataflow.registry.core").setLevel(logging.WARNING)
logging.getLogger("hpack").setLevel(logging.WARNING)

# Set up our debug logging
logging.basicConfig(level=logging.DEBUG, format="%(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


# Define the models from the notebook
class QueryRefinementSuggestion(BaseModel):
    """Individual query refinement suggestion."""

    refined_query: str = Field(description="The refined/improved query")
    improvement_type: str = Field(description="Type of improvement made")
    rationale: str = Field(description="Why this refinement improves the query")
    expected_benefit: str = Field(description="Expected improvement in retrieval")


class QueryRefinementResponse(BaseModel):
    """Query refinement analysis and suggestions."""

    original_query: str = Field(description="The original user query")
    query_analysis: str = Field(description="Analysis of the original query")
    query_type: str = Field(description="Classification of query type")
    complexity_level: str = Field(description="simple, moderate, or complex")
    refinement_suggestions: list[QueryRefinementSuggestion] = Field(
        description="List of suggested improvements"
    )
    best_refined_query: str = Field(description="The recommended best refined query")
    search_strategy_recommendations: list[str] = Field(
        description="Recommendations for search strategy"
    )


# Create prompt
RAG_QUERY_REFINEMENT = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an expert query optimization specialist."),
        ("human", "Analyze and refine: {query}"),
    ]
).partial(context="")

try:
    from haive.agents.simple.agent_v2 import SimpleAgentV2
    from haive.core.engine.aug_llm import AugLLMConfig
    from haive.core.schema.prebuilt.llm_state import LLMState

    # Let's look at LLMState
    logger.info("=== Examining LLMState ===")
    logger.info(f"LLMState fields: {list(LLMState.model_fields.keys())}")
    for field_name, field_info in LLMState.model_fields.items():
        logger.info(f"  {field_name}: {field_info}")

    # Create the engine
    logger.info("\n=== Creating AugLLMConfig ===")
    engine = AugLLMConfig(
        prompt_template=RAG_QUERY_REFINEMENT,
        structured_output_model=QueryRefinementResponse,
        structured_output_version="v2",
    )
    logger.info(f"Engine created: {engine}")
    logger.info(f"Engine type: {type(engine)}")

    # Create the agent
    logger.info("\n=== Creating SimpleAgentV2 ===")
    agent = SimpleAgentV2(engine=engine)
    logger.info(f"Agent created: {agent}")

    # Check the agent's state schema
    logger.info("\n=== Checking State Schema ===")
    state_schema = agent.state_schema
    logger.info(f"State schema type: {type(state_schema)}")
    logger.info(f"State schema fields: {list(state_schema.model_fields.keys())}")

    # Check if engine field exists
    if "engine" in state_schema.model_fields:
        engine_field = state_schema.model_fields["engine"]
        logger.info(f"Engine field info: {engine_field}")
        logger.info(f"Engine field required: {engine_field.is_required()}")
        logger.info(f"Engine field default: {engine_field.default}")

    # Try to create a state instance
    logger.info("\n=== Creating State Instance ===")
    try:
        # First, try without engine
        state1 = state_schema()
        logger.info("Created state without args - OK")
    except Exception as e:
        logger.exception(f"Failed to create state without args: {e}")

    try:
        # Try with engine
        state2 = state_schema(engine=engine)
        logger.info("Created state with engine - OK")
        logger.info(f"State engine value: {state2.engine}")
    except Exception as e:
        logger.exception(f"Failed to create state with engine: {e}")

    # Check input schema
    logger.info("\n=== Checking Input Schema ===")
    input_schema = agent.input_schema
    logger.info(f"Input schema type: {type(input_schema)}")
    logger.info(f"Input schema fields: {list(input_schema.model_fields.keys())}")

    # Test input creation
    logger.info("\n=== Testing Input Creation ===")
    input_data = input_schema(query="hello")
    logger.info(f"Created input: {input_data}")
    logger.info(f"Input dict: {input_data.model_dump()}")

    # Now let's trace the execution
    logger.info("\n=== Testing Execution ===")

    # Hook into ExecutionMixin's _prepare_input
    original_prepare = agent._prepare_input

    def debug_prepare(input_data):
        logger.info(f"_prepare_input called with: {input_data}")
        logger.info(f"_prepare_input type: {type(input_data)}")
        result = original_prepare(input_data)
        logger.info(f"_prepare_input result: {result}")
        logger.info(f"_prepare_input result type: {type(result)}")
        return result

    agent._prepare_input = debug_prepare

    # Try to run
    result = agent.run({"query": "what is the tallest building in france"})
    logger.info(f"Result: {result}")

except Exception as e:
    logger.exception(f"Error: {type(e).__name__}: {e}")
    import traceback

    traceback.print_exc()
