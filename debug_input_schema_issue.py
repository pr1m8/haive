#!/usr/bin/env python3
"""Debug why engine field is in input schema."""

import logging

from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s - %(message)s")
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

    logger.info("\n=== State Schema Analysis ===")
    logger.info(f"State schema class: {state_schema}")
    logger.info(f"State schema fields: {list(state_schema.model_fields.keys())}")

    # Check engine_io_mappings
    if hasattr(state_schema, "__engine_io_mappings__"):
        logger.info(f"\nEngine I/O mappings: {state_schema.__engine_io_mappings__}")

    # Now derive input schema manually to see what happens
    logger.info("\n=== Manual Input Schema Derivation ===")

    # Get input fields
    if hasattr(state_schema, "__engine_io_mappings__"):
        all_input_fields = []
        for engine_name, mapping in state_schema.__engine_io_mappings__.items():
            input_fields = mapping.get("inputs", [])
            logger.info(f"Engine '{engine_name}' input fields: {input_fields}")
            all_input_fields.extend(input_fields)

        logger.info(f"\nAll input fields from mappings: {all_input_fields}")

    # Check what derive_input_schema returns
    derived_input = state_schema.derive_input_schema()
    logger.info(f"\nDerived input schema: {derived_input}")
    logger.info(
        f"Derived input schema fields: {list(derived_input.model_fields.keys())}"
    )

    # Check if engine field is in derived input
    if "engine" in derived_input.model_fields:
        logger.warning("ENGINE FIELD FOUND IN DERIVED INPUT SCHEMA!")
        engine_field = derived_input.model_fields["engine"]
        logger.info(f"Engine field info: {engine_field}")
        logger.info(f"Engine field required: {engine_field.is_required()}")

    # Now check what the agent's input_schema property is
    logger.info("\n=== Agent's Input Schema ===")
    agent_input_schema = agent.input_schema
    logger.info(f"Agent input schema: {agent_input_schema}")
    logger.info(
        f"Agent input schema fields: {list(agent_input_schema.model_fields.keys())}"
    )

    # Check base classes
    logger.info(f"\nAgent input schema base classes: {agent_input_schema.__bases__}")

    # Check if SimpleAgentV2 itself has an input_schema class attribute
    logger.info("\n=== SimpleAgentV2 Class Attributes ===")
    if hasattr(SimpleAgentV2, "input_schema"):
        logger.info(f"SimpleAgentV2.input_schema: {SimpleAgentV2.input_schema}")
    if hasattr(SimpleAgentV2, "model_fields"):
        logger.info(
            f"SimpleAgentV2 model fields: {list(SimpleAgentV2.model_fields.keys())}"
        )
        if "engine" in SimpleAgentV2.model_fields:
            logger.info("SimpleAgentV2 has engine field!")

except Exception as e:
    logger.exception(f"Error: {type(e).__name__}: {e}")
    import traceback

    traceback.print_exc()
