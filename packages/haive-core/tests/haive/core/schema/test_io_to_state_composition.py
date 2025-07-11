"""Tests for composing state schemas from input and output schemas.

These tests verify that the SchemaComposer can correctly create a state schema
by combining existing input and output schemas, rather than deriving them from a state schema.
"""

from typing import Any, Dict, List

from langchain_core.messages import BaseMessage, HumanMessage
from pydantic import BaseModel, Field

from haive.core.schema.schema_composer import SchemaComposer
from haive.core.schema.state_schema import StateSchema


class SampleInputSchema(BaseModel):
    """Input schema for testing."""

    messages: list[BaseMessage] = Field(default_factory=list)
    query: str = Field(default="")
    context: dict[str, Any] = Field(default_factory=dict)


class SampleOutputSchema(BaseModel):
    """Output schema for testing."""

    messages: list[BaseMessage] = Field(default_factory=list)
    response: str = Field(default="")
    sources: list[dict[str, Any]] = Field(default_factory=list)


def test_compose_state_from_io_schemas():
    """Test creating a state schema from input and output schemas."""
    # Create a state schema from input and output schemas
    state_schema = SchemaComposer.create_state_from_io_schemas(
        SampleInputSchema, SampleOutputSchema, name="ComposedTestSchema"
    )

    # Verify the result is a proper state schema
    assert issubclass(state_schema, StateSchema)
    assert issubclass(state_schema, SampleInputSchema)
    assert issubclass(state_schema, SampleOutputSchema)

    # Verify schema has the right name
    assert state_schema.__name__ == "ComposedTestSchema"

    # Verify all expected fields exist
    assert "messages" in state_schema.model_fields
    assert "query" in state_schema.model_fields
    assert "context" in state_schema.model_fields
    assert "response" in state_schema.model_fields
    assert "sources" in state_schema.model_fields

    # Verify engine I/O mappings have been properly assigned
    assert hasattr(state_schema, "__engine_io_mappings__")
    assert "default" in state_schema.__engine_io_mappings__

    # Verify messages field is properly configured as both input and output
    assert "messages" in state_schema.__engine_io_mappings__["default"]["inputs"]
    assert "messages" in state_schema.__engine_io_mappings__["default"]["outputs"]


def test_state_instance_creation():
    """Test creating and using a state instance from composed schema."""
    # Create a state schema from input and output schemas
    state_schema = SchemaComposer.create_state_from_io_schemas(
        SampleInputSchema, SampleOutputSchema, name="ComposedTestSchema"
    )

    # Create a state instance with some initial values
    state = state_schema(
        messages=[HumanMessage(content="Hello")],
        query="What is the weather?",
        context={"location": "New York"},
    )

    # Verify the instance has the expected values
    assert len(state.messages) == 1
    assert state.messages[0].content == "Hello"
    assert state.query == "What is the weather?"
    assert state.context["location"] == "New York"
    assert state.response == ""  # Default value
    assert len(state.sources) == 0  # Default empty list

    # Test updating the state
    state.response = "The weather is sunny"
    state.sources = [{"url": "weather.com", "content": "Sunny and 75°F"}]

    assert state.response == "The weather is sunny"
    assert len(state.sources) == 1
    assert state.sources[0]["url"] == "weather.com"


def test_compose_state_directly():
    """Test using the compose_state_from_io method directly."""
    # Create a composer
    composer = SchemaComposer(name="DirectComposedSchema")

    # Add some field definitions to the composer

    from langchain_core.messages import BaseMessage

    # Configure messages field with reducer
    try:
        from langgraph.graph import add_messages

        reducer = add_messages
    except ImportError:
        # Fallback
        def reducer(a, b):
            return (a or []) + (b or [])

    # Add messages field with reducer
    composer.add_field(
        name="messages",
        field_type=list[BaseMessage],
        default_factory=list,
        description="Messages for conversation",
        reducer=reducer,
        shared=True,
        input_for=["llm"],
        output_from=["llm"],
    )

    # Directly compose a state schema
    state_schema = composer.compose_state_from_io(SampleInputSchema, SampleOutputSchema)

    # Verify it inherits from both input and output schemas
    assert issubclass(state_schema, StateSchema)
    assert issubclass(state_schema, SampleInputSchema)
    assert issubclass(state_schema, SampleOutputSchema)

    # Verify shared fields were properly transferred
    assert "messages" in state_schema.__shared_fields__

    # Verify reducer was configured
    assert "messages" in state_schema.__serializable_reducers__
    assert "messages" in state_schema.__reducer_fields__

    # Verify engine I/O mapping was maintained
    assert "llm" in state_schema.__engine_io_mappings__
    assert "messages" in state_schema.__engine_io_mappings__["llm"]["inputs"]
    assert "messages" in state_schema.__engine_io_mappings__["llm"]["outputs"]
