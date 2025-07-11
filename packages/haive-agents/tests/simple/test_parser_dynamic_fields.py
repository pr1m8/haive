"""Test to see if parser node can add fields dynamically to state or needs pre-existing fields."""

import os
import sys
from unittest.mock import MagicMock, Mock, patch

from pydantic import BaseModel, Field, create_model

# Add packages to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../"))


def test_parser_node_dynamic_field_addition():
    """Test if parser node can add structured output to state dynamically."""
    try:
        from haive.core.graph.node.parser_node_config import ParserNodeConfig
        from langchain_core.messages import AIMessage, ToolMessage

    except Exception as e:
        return

    # Test model
    class TestResult(BaseModel):
        summary: str = Field(description="Task summary")
        completed: bool = Field(description="Whether completed")
        confidence: float = Field(ge=0.0, le=1.0, description="Confidence level")

    # Create mock engine with structured output model
    mock_engine = Mock()
    mock_engine.name = "test_engine"
    mock_engine.structured_output_model = TestResult
    mock_engine.pydantic_tools = [TestResult]

    # Test Case 1: State schema WITHOUT the structured output field
    minimal_state_schema = create_model(
        "MinimalState",
        messages=(list, Field(default_factory=list)),
        # NOTE: No 'testresult' field pre-defined!
    )


    # Create state instance
    state = minimal_state_schema()
    state.engines = {"test_engine": mock_engine}

    # Create mock messages with tool call and tool response
    tool_call_id = "test_call_123"

    # AI message with tool call
    ai_message = AIMessage(
        content="I'll analyze this for you.",
        tool_calls=[
            {
                "id": tool_call_id,
                "name": "TestResult",
                "args": {
                    "summary": "Analysis complete",
                    "completed": True,
                    "confidence": 0.95,
                },
            }
        ],
    )

    # Tool message with the result
    tool_message = ToolMessage(
        content='{"summary": "Analysis complete", "completed": true, "confidence": 0.95}',
        tool_call_id=tool_call_id,
        name="TestResult",
    )

    state.messages = [ai_message, tool_message]

    # Create parser node
    parser_config = ParserNodeConfig(name="test_parser", engine_name="test_engine")


    # Try to execute parser
    try:
        result_command = parser_config(state)


        if hasattr(result_command, "update") and result_command.update:

            # Check if parser added the structured field
            if "testresult" in result_command.update:
                structured_result = result_command.update["testresult"]
            else:
        else:
            pass")

    except Exception as e:


    # Test Case 2: State schema WITH the structured output field pre-defined
    enhanced_state_schema = create_model(
        "EnhancedState",
        messages=(list, Field(default_factory=list)),
        testresult=(TestResult, Field(default=None)),  # Pre-defined field
    )


    # Create enhanced state
    enhanced_state = enhanced_state_schema()
    enhanced_state.engines = {"test_engine": mock_engine}
    enhanced_state.messages = [ai_message, tool_message]

    # Try parser with pre-defined field
    try:
        result_command = parser_config(enhanced_state)


        if hasattr(result_command, "update") and result_command.update:

            if "testresult" in result_command.update:
                pass")
            else:
                passld")
        else:
            pass")

    except Exception as e:
        pass")



def test_state_update_mechanics():
    """Test the basic mechanics of state updates with new fields."""

    # Create a basic state model
    BasicState = create_model(
        "BasicState",
        messages=(list, Field(default_factory=list)),
        counter=(int, Field(default=0)),
    )

    state = BasicState()

    # Test 1: Can we update existing fields?
    try:
        # Simulate a state update
        update_dict = {"counter": 5, "messages": ["test"]}

        # This is how LangGraph updates state
        new_state = BasicState(**{**state.model_dump(), **update_dict})

    except Exception as e:
        pass")

    # Test 2: Can we add completely new fields?
    try:
        # Try to add a field that doesn't exist in schema
        update_dict = {"counter": 10, "new_field": "dynamic value"}

        new_state = BasicState(**{**state.model_dump(), **update_dict})

    except Exception as e:



if __name__ == "__main__":
    test_parser_node_dynamic_field_addition()
    test_state_update_mechanics()
