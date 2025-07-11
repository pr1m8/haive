#!/usr/bin/env python3
"""Debug the derive_input_schema issue."""

import logging

from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

# Set up logging
logging.basicConfig(level=logging.DEBUG, format="%(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Disable noisy logs
logging.getLogger("haive.dataflow.registry.core").setLevel(logging.WARNING)
logging.getLogger("hpack").setLevel(logging.WARNING)

# Create prompt
RAG_QUERY_REFINEMENT = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an expert query optimization specialist."),
        ("human", "Analyze and refine: {query}"),
    ]
).partial(context="")


# Define the model
class QueryRefinementResponse(BaseModel):
    """Query refinement analysis and suggestions."""

    original_query: str = Field(description="The original user query")


try:
    from haive.agents.simple.agent_v2 import SimpleAgentV2
    from haive.core.engine.aug_llm import AugLLMConfig
    from haive.core.schema.prebuilt.llm_state import LLMState

    # Create the engine
    engine = AugLLMConfig(
        prompt_template=RAG_QUERY_REFINEMENT,
        structured_output_model=QueryRefinementResponse,
        structured_output_version="v2",
    )

    # Create the agent
    agent = SimpleAgentV2(engine=engine)

    # Get the state schema
    state_schema = agent.state_schema
    logger.info("\n=== State Schema ===")
    logger.info(f"State schema: {state_schema}")
    logger.info(f"State schema base: {state_schema.__bases__}")
    logger.info(f"State schema fields: {list(state_schema.model_fields.keys())}")

    # Check if it's using LLMState
    logger.info(f"Is subclass of LLMState: {issubclass(state_schema, LLMState)}")

    # Get the input schema
    input_schema = agent.input_schema
    logger.info("\n=== Input Schema ===")
    logger.info(f"Input schema: {input_schema}")
    logger.info(f"Input schema base: {input_schema.__bases__}")
    logger.info(f"Input schema fields: {list(input_schema.model_fields.keys())}")

    # Check engine field in each
    logger.info("\n=== Engine Field Analysis ===")

    # State schema engine field
    if "engine" in state_schema.model_fields:
        engine_field = state_schema.model_fields["engine"]
        logger.info(f"State schema engine field: {engine_field}")
        logger.info(f"  - Required: {engine_field.is_required()}")
        logger.info(f"  - Type: {engine_field.annotation}")
    else:
        logger.error("State schema missing engine field!")

    # Input schema engine field
    if "engine" in input_schema.model_fields:
        engine_field = input_schema.model_fields["engine"]
        logger.info(f"Input schema engine field: {engine_field}")
        logger.info(f"  - Required: {engine_field.is_required()}")
        logger.info(f"  - Type: {engine_field.annotation}")
    else:
        logger.warning("Input schema missing engine field - this is expected")

    # Try to create instances
    logger.info("\n=== Instance Creation ===")

    # Create state with engine
    try:
        state = state_schema(engine=engine)
        logger.info("✓ State created with engine")
    except Exception as e:
        logger.exception(f"✗ State creation failed: {e}")

    # Create input without engine (should work)
    try:
        input_instance = input_schema(query="test")
        logger.info("✓ Input created without engine")
    except Exception as e:
        logger.exception(f"✗ Input creation failed: {e}")

    # Now test the execution flow
    logger.info("\n=== Execution Flow ===")

    # The issue is that _prepare_input tries to create an input schema instance
    # but the execution mixin needs to then convert that to a state schema instance
    # Let's trace this

    # Get the graph
    graph = agent.compiled_graph
    logger.info(f"Graph: {graph}")

    # Try to trace the actual execution
    logger.info("\nAttempting to run agent...")
    try:
        result = agent.run({"query": "test"})
        logger.info(f"Success! Result: {result}")
    except Exception as e:
        logger.exception(f"Failed: {e}")
        import traceback

        traceback.print_exc()

except Exception as e:
    logger.exception(f"Error: {type(e).__name__}: {e}")
    import traceback

    traceback.print_exc()
