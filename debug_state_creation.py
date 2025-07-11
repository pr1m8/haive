#!/usr/bin/env python3
"""Debug state creation issue."""

import logging

from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Disable noisy logs
logging.getLogger("haive.dataflow.registry.core").setLevel(logging.WARNING)
logging.getLogger("hpack").setLevel(logging.WARNING)

# Create prompt
RAG_QUERY_REFINEMENT = ChatPromptTemplate.from_messages(
    [("system", "You are an expert."), ("human", "{query}")]
).partial(context="")


# Define the model
class QueryRefinementResponse(BaseModel):
    """Query refinement analysis."""

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
    logger.info(f"State schema: {state_schema}")
    logger.info(f"State schema base classes: {state_schema.__bases__}")
    logger.info(f"Is LLMState subclass: {issubclass(state_schema, LLMState)}")

    # Check engine field
    if "engine" in state_schema.model_fields:
        engine_field = state_schema.model_fields["engine"]
        logger.info("\nEngine field in state schema:")
        logger.info(f"  - Type: {engine_field.annotation}")
        logger.info(f"  - Required: {engine_field.is_required()}")
        logger.info(f"  - Default: {engine_field.default}")
        logger.info(f"  - Default factory: {engine_field.default_factory}")

    # Try to create state without engine
    logger.info("\n=== Creating state without engine ===")
    try:
        state1 = state_schema()
        logger.info("✓ Created state without engine!")
        logger.info(f"  - engine value: {state1.engine}")
    except Exception as e:
        logger.exception(f"✗ Failed: {e}")

    # Try to create state with engine
    logger.info("\n=== Creating state with engine ===")
    try:
        state2 = state_schema(engine=engine)
        logger.info("✓ Created state with engine!")
        logger.info(f"  - engine value: {state2.engine}")
    except Exception as e:
        logger.exception(f"✗ Failed: {e}")

    # Check default_factory on class
    logger.info("\n=== Checking class engines ===")
    if hasattr(state_schema, "__engines__"):
        logger.info(f"Class has __engines__: {state_schema.__engines__}")
    if hasattr(state_schema, "model_fields") and "engines" in state_schema.model_fields:
        engines_field = state_schema.model_fields["engines"]
        logger.info(f"Engines field default_factory: {engines_field.default_factory}")
        if engines_field.default_factory:
            logger.info(
                f"Calling engines default_factory: {engines_field.default_factory()}"
            )

    # Now check the input schema
    logger.info("\n=== Input Schema ===")
    input_schema = agent.input_schema
    logger.info(f"Input schema fields: {list(input_schema.model_fields.keys())}")
    logger.info(f"Has engine field: {'engine' in input_schema.model_fields}")

    # The issue flow
    logger.info("\n=== Testing execution flow ===")
    try:
        # This is what _prepare_input does
        input_data = {"query": "test"}
        input_instance = input_schema(**input_data)
        logger.info(f"✓ Created input instance: {input_instance}")

        # Now how does this become a state?
        # The graph needs to convert input to state...
        logger.info("\nTrying to convert input to state...")

        # This is the issue - the state requires engine but input doesn't have it
        state_data = input_instance.model_dump()
        logger.info(f"Input data: {state_data}")

        # Try to create state from input data
        try:
            state = state_schema(**state_data)
            logger.info("✓ Created state from input data!")
        except Exception as e:
            logger.exception(f"✗ Failed to create state from input: {e}")

            # The state schema expects the engine to be populated somehow
            # Let's see if the agent has a way to inject it
            logger.info("\nChecking if agent has engine to inject...")
            logger.info(f"Agent engine: {agent.engine}")

    except Exception as e:
        logger.exception(f"Failed in execution flow: {e}")

except Exception as e:
    logger.exception(f"Error: {type(e).__name__}: {e}")
    import traceback

    traceback.print_exc()
