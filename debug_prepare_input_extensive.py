#!/usr/bin/env python3
"""Debug _prepare_input with extensive logging and traceback."""

import logging
import sys
import traceback

from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

# Configure logging with DEBUG level and detailed format
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)

# Disable noisy logs
logging.getLogger("haive.dataflow.registry.core").setLevel(logging.WARNING)
logging.getLogger("hpack").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

# Create prompt
RAG_QUERY_REFINEMENT = ChatPromptTemplate.from_messages(
    [("system", "You are an expert."), ("human", "{query}")]
).partial(context="")


# Define the model
class QueryRefinementResponse(BaseModel):
    """Query refinement analysis."""

    original_query: str = Field(description="The original user query")


try:
    logger.info("=" * 80)
    logger.info("STARTING DEBUG OF _prepare_input EXECUTION FLOW")
    logger.info("=" * 80)

    from haive.agents.simple.agent_v2 import SimpleAgentV2
    from haive.core.engine.aug_llm import AugLLMConfig

    # Create the engine
    engine = AugLLMConfig(
        prompt_template=RAG_QUERY_REFINEMENT,
        structured_output_model=QueryRefinementResponse,
        structured_output_version="v2",
    )
    logger.info(f"Created engine: {engine.name}")

    # Create the agent
    logger.info("\nCreating SimpleAgentV2...")
    agent = SimpleAgentV2(engine=engine)
    logger.info(f"Agent created: {agent.name}")

    # Log state schema info
    logger.info(f"\nState schema: {agent.state_schema}")
    logger.info(f"State schema fields: {list(agent.state_schema.model_fields.keys())}")

    # Log input schema info
    logger.info(f"\nInput schema: {agent.input_schema}")
    logger.info(f"Input schema fields: {list(agent.input_schema.model_fields.keys())}")

    # Now let's patch _prepare_input to add extensive logging
    from haive.agents.base.mixins.execution_mixin import ExecutionMixin

    original_prepare_input = ExecutionMixin._prepare_input

    def logged_prepare_input(self, input_data):
        """Wrapped _prepare_input with extensive logging."""
        logger.info("\n" + "=" * 60)
        logger.info("ENTERING _prepare_input")
        logger.info("=" * 60)

        # Log call stack
        logger.info("\nCall Stack:")
        for i, frame in enumerate(traceback.extract_stack()[:-1]):
            logger.info(f"  {i}: {frame.filename}:{frame.lineno} in {frame.name}")
            if frame.line:
                logger.info(f"     {frame.line.strip()}")

        # Log input parameters
        logger.info(f"\nInput type: {type(input_data)}")
        logger.info(f"Input data: {input_data}")

        # Log self attributes
        logger.info(f"\nSelf type: {type(self)}")
        logger.info(f"Self name: {getattr(self, 'name', 'NO NAME')}")
        logger.info(f"Has state_schema: {hasattr(self, 'state_schema')}")
        logger.info(f"Has input_schema: {hasattr(self, 'input_schema')}")
        logger.info(f"Has engine: {hasattr(self, 'engine')}")

        if hasattr(self, "state_schema"):
            logger.info(f"\nState schema type: {type(self.state_schema)}")
            logger.info(f"State schema: {self.state_schema}")
            logger.info(
                f"State schema fields: {list(self.state_schema.model_fields.keys())}"
            )

            # Check if engine is required in state schema
            if "engine" in self.state_schema.model_fields:
                engine_field = self.state_schema.model_fields["engine"]
                logger.info("\nState schema has engine field:")
                logger.info(f"  - Required: {engine_field.is_required()}")
                logger.info(f"  - Type: {engine_field.annotation}")
                logger.info(f"  - Default: {engine_field.default}")

        if hasattr(self, "input_schema"):
            logger.info(f"\nInput schema type: {type(self.input_schema)}")
            logger.info(f"Input schema: {self.input_schema}")
            logger.info(
                f"Input schema fields: {list(self.input_schema.model_fields.keys())}"
            )

            # Check if engine is in input schema
            if "engine" in self.input_schema.model_fields:
                logger.warning("ENGINE FIELD FOUND IN INPUT SCHEMA - THIS IS THE BUG!")

        if hasattr(self, "engine"):
            logger.info(f"\nAgent engine: {self.engine}")
            logger.info(f"Engine type: {type(self.engine)}")
            logger.info(f"Engine name: {getattr(self.engine, 'name', 'NO NAME')}")

        try:
            # Call original method
            logger.info("\nCalling original _prepare_input...")
            result = original_prepare_input(self, input_data)

            # Log result
            logger.info(f"\n_prepare_input returned type: {type(result)}")
            logger.info(f"Result: {result}")

            if isinstance(result, dict):
                logger.info(f"Result keys: {list(result.keys())}")
                if "engine" in result:
                    logger.info("ENGINE FIELD PRESENT IN RESULT")
                    logger.info(f"Engine value: {result['engine']}")

            logger.info("\n" + "=" * 60)
            logger.info("EXITING _prepare_input successfully")
            logger.info("=" * 60)

            return result

        except Exception as e:
            logger.exception(f"\nEXCEPTION in _prepare_input: {type(e).__name__}: {e}")
            logger.exception("Full traceback:")
            logger.exception(traceback.format_exc())

            # Log more context about the error
            if hasattr(e, "__dict__"):
                logger.exception(f"Exception attributes: {e.__dict__}")

            logger.exception("\n" + "=" * 60)
            logger.exception("EXITING _prepare_input with exception")
            logger.exception("=" * 60)

            raise

    # Patch the method
    ExecutionMixin._prepare_input = logged_prepare_input

    try:
        # Now run the agent with the patched method
        logger.info("\n" + "=" * 80)
        logger.info("RUNNING AGENT WITH PATCHED _prepare_input")
        logger.info("=" * 80)

        import asyncio

        async def test_run():
            try:
                result = await agent.arun("What is machine learning?")
                logger.info("\nAgent run successful!")
                logger.info(f"Result type: {type(result)}")
                logger.info(f"Result: {result}")
            except Exception as e:
                logger.exception(f"\nAgent run failed: {type(e).__name__}: {e}")
                logger.exception("Full traceback:")
                logger.exception(traceback.format_exc())

        asyncio.run(test_run())

    finally:
        # Restore original method
        ExecutionMixin._prepare_input = original_prepare_input
        logger.info("\nRestored original _prepare_input method")

except Exception as e:
    logger.exception(f"\nTop-level error: {type(e).__name__}: {e}")
    logger.exception("Full traceback:")
    logger.exception(traceback.format_exc())
