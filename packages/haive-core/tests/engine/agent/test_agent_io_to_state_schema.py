"""
Tests for AgentConfig with the new IO-to-State schema composition approach.

These tests verify that the AgentConfig correctly composes state schemas from
input and output schemas, rather than deriving input/output schemas from state schemas.
"""

import logging
from typing import Any, Dict, List

from langchain_core.messages import BaseMessage, HumanMessage
from pydantic import BaseModel, Field

from haive.core.engine.agent.config import AgentConfig
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig
from haive.core.schema.state_schema import StateSchema
from haive.core.schema.ui import SchemaUI

# Set up logging for tests
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CustomInputSchema(BaseModel):
    """Custom input schema for testing."""

    messages: List[BaseMessage] = Field(default_factory=list)
    query: str = Field(default="", description="User query")
    context: List[str] = Field(default_factory=list, description="Context documents")


class CustomOutputSchema(BaseModel):
    """Custom output schema for testing."""

    messages: List[BaseMessage] = Field(default_factory=list)
    response: str = Field(default="", description="Generated response")
    sources: List[Dict[str, Any]] = Field(
        default_factory=list, description="Source documents"
    )
    confidence: float = Field(default=0.0, description="Confidence score")


def test_agent_io_to_state_composition():
    """Test that AgentConfig correctly composes state schema from input and output schemas."""
    # Create agent config with explicit input and output schemas
    agent_config = AgentConfig(
        name="test_agent",
        input_schema=CustomInputSchema,
        output_schema=CustomOutputSchema,
        engine=AugLLMConfig(
            system_message="You are a helpful assistant.",
            llm_config=AzureLLMConfig(model="gpt-4o"),
        ),
    )

    # Derive schemas using our new approach
    input_schema = agent_config.derive_input_schema()
    output_schema = agent_config.derive_output_schema()
    state_schema = agent_config.derive_schema()

    # Log schema info
    logger.info(f"Input schema: {input_schema.__name__}")
    logger.info(f"Input schema fields: {list(input_schema.model_fields.keys())}")
    logger.info(f"Output schema: {output_schema.__name__}")
    logger.info(f"Output schema fields: {list(output_schema.model_fields.keys())}")
    logger.info(f"State schema: {state_schema.__name__}")
    logger.info(f"State schema fields: {list(state_schema.model_fields.keys())}")

    # Check engine_io_mappings in state schema
    if hasattr(state_schema, "__engine_io_mappings__"):
        logger.info(f"Engine I/O mappings: {state_schema.__engine_io_mappings__}")

    # Verify that the schemas are correctly related
    assert issubclass(state_schema, StateSchema)
    assert hasattr(state_schema, "model_fields")

    # Verify state schema includes all fields from both input and output schemas
    assert "messages" in state_schema.model_fields
    assert "query" in state_schema.model_fields
    assert "context" in state_schema.model_fields
    assert "response" in state_schema.model_fields
    assert "sources" in state_schema.model_fields
    assert "confidence" in state_schema.model_fields

    # Our implementation uses composition rather than inheritance
    # So we shouldn't expect the state schema to be a subclass of input/output schemas
    # assert issubclass(state_schema, CustomInputSchema)
    # assert issubclass(state_schema, CustomOutputSchema)

    # Display schema with SchemaUI if available
    try:
        SchemaUI.display_schema(state_schema, "Agent State Schema")
    except Exception as e:
        logger.warning(f"Could not display schema: {e}")

    # Create a state instance to test functionality
    state = state_schema(
        query="What is the capital of France?",
        context=["France is a country in Europe.", "Paris is a city in France."],
    )

    # Test updating the state
    state.response = "The capital of France is Paris."
    state.sources = [
        {"url": "wikipedia.org", "content": "Paris is the capital of France."}
    ]
    state.confidence = 0.95

    # Verify state values
    assert state.query == "What is the capital of France?"
    assert len(state.context) == 2
    assert state.response == "The capital of France is Paris."
    assert len(state.sources) == 1
    assert state.confidence == 0.95

    # Test with messages
    state.messages.append(HumanMessage(content="Tell me about Paris"))
    assert len(state.messages) == 1


def test_agent_with_component_derived_schemas():
    """Test that AgentConfig correctly composes state schema from components."""
    # Create agent config with a component but no explicit schemas
    agent_config = AgentConfig(
        name="component_test_agent",
        engine=AugLLMConfig(
            system_message="You are a helpful assistant.",
            llm_config=AzureLLMConfig(model="gpt-4o"),
        ),
    )

    # Derive schemas using our new approach
    input_schema = agent_config.derive_input_schema()
    output_schema = agent_config.derive_output_schema()
    state_schema = agent_config.derive_schema()

    # Log schema info
    logger.info(f"Input schema: {input_schema.__name__}")
    logger.info(f"Input schema fields: {list(input_schema.model_fields.keys())}")
    logger.info(f"Output schema: {output_schema.__name__}")
    logger.info(f"Output schema fields: {list(output_schema.model_fields.keys())}")
    logger.info(f"State schema: {state_schema.__name__}")
    logger.info(f"State schema fields: {list(state_schema.model_fields.keys())}")

    # Verify that the schemas are correctly related
    assert issubclass(state_schema, StateSchema)
    assert hasattr(state_schema, "model_fields")

    # Verify common fields are present
    assert "messages" in state_schema.model_fields  # Common field

    # Create a state instance to test functionality
    state = state_schema()
    state.messages.append(HumanMessage(content="Hello"))
    assert len(state.messages) == 1
