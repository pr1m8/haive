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

        print("✅ Successfully imported ParserNodeConfig")
    except Exception as e:
        print(f"❌ Import failed: {e}")
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

    print("🧪 Test Case 1: State schema WITHOUT structured output field")
    print(f"   Schema fields: {list(minimal_state_schema.model_fields.keys())}")

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

    print(f"   Parser config created: {parser_config.name}")

    # Try to execute parser
    try:
        print("   🔄 Executing parser node...")
        result_command = parser_config(state)

        print(f"   ✅ Parser executed successfully!")
        print(f"   📋 Command type: {type(result_command)}")

        if hasattr(result_command, "update") and result_command.update:
            print(f"   📝 Update fields: {list(result_command.update.keys())}")

            # Check if parser added the structured field
            if "testresult" in result_command.update:
                structured_result = result_command.update["testresult"]
                print(f"   🎯 Found structured result: {type(structured_result)}")
                print(f"      Summary: {getattr(structured_result, 'summary', 'N/A')}")
                print(
                    f"      Completed: {getattr(structured_result, 'completed', 'N/A')}"
                )
                print(
                    f"      Confidence: {getattr(structured_result, 'confidence', 'N/A')}"
                )
                print("   ✅ Parser CAN add fields dynamically!")
            else:
                print(f"   ⚠️  No 'testresult' field in update")
                print(
                    f"       Available update fields: {list(result_command.update.keys())}"
                )
        else:
            print(f"   ❌ No update in command result")

    except Exception as e:
        print(f"   ❌ Parser execution failed: {e}")
        print(f"      This might mean parser REQUIRES pre-existing field")

    print("\n" + "=" * 60)

    # Test Case 2: State schema WITH the structured output field pre-defined
    enhanced_state_schema = create_model(
        "EnhancedState",
        messages=(list, Field(default_factory=list)),
        testresult=(TestResult, Field(default=None)),  # Pre-defined field
    )

    print("🧪 Test Case 2: State schema WITH structured output field pre-defined")
    print(f"   Schema fields: {list(enhanced_state_schema.model_fields.keys())}")

    # Create enhanced state
    enhanced_state = enhanced_state_schema()
    enhanced_state.engines = {"test_engine": mock_engine}
    enhanced_state.messages = [ai_message, tool_message]

    # Try parser with pre-defined field
    try:
        print("   🔄 Executing parser node...")
        result_command = parser_config(enhanced_state)

        print(f"   ✅ Parser executed successfully!")

        if hasattr(result_command, "update") and result_command.update:
            print(f"   📝 Update fields: {list(result_command.update.keys())}")

            if "testresult" in result_command.update:
                print("   ✅ Parser updated pre-defined field successfully!")
            else:
                print("   ⚠️  Parser didn't update the pre-defined field")
        else:
            print("   ❌ No update in command result")

    except Exception as e:
        print(f"   ❌ Parser execution failed even with pre-defined field: {e}")

    print("\n" + "=" * 60)
    print("📊 Summary:")
    print("   This test reveals whether parser node can:")
    print("   1. Add structured output fields dynamically (Case 1)")
    print("   2. Requires fields to be pre-defined in schema (Case 2)")
    print("   3. The approach SimpleAgent should use")


def test_state_update_mechanics():
    """Test the basic mechanics of state updates with new fields."""

    print("\n🔬 Testing State Update Mechanics:")

    # Create a basic state model
    BasicState = create_model(
        "BasicState",
        messages=(list, Field(default_factory=list)),
        counter=(int, Field(default=0)),
    )

    state = BasicState()
    print(f"   Original state fields: {list(state.model_fields.keys())}")
    print(f"   Original state: {state.model_dump()}")

    # Test 1: Can we update existing fields?
    try:
        # Simulate a state update
        update_dict = {"counter": 5, "messages": ["test"]}

        # This is how LangGraph updates state
        new_state = BasicState(**{**state.model_dump(), **update_dict})
        print(f"   ✅ Updated existing fields: {new_state.model_dump()}")

    except Exception as e:
        print(f"   ❌ Failed to update existing fields: {e}")

    # Test 2: Can we add completely new fields?
    try:
        # Try to add a field that doesn't exist in schema
        update_dict = {"counter": 10, "new_field": "dynamic value"}

        new_state = BasicState(**{**state.model_dump(), **update_dict})
        print(f"   Result: {new_state.model_dump()}")

    except Exception as e:
        print(f"   ❌ Cannot add new fields dynamically: {e}")
        print("   📝 This suggests parser NEEDS pre-defined fields!")

    print("\n📋 State Update Conclusion:")
    print("   - Pydantic models have fixed schemas")
    print("   - Cannot add fields that aren't defined in model")
    print("   - Parser likely requires fields to be pre-defined")


if __name__ == "__main__":
    test_parser_node_dynamic_field_addition()
    test_state_update_mechanics()
    print("\n🎯 Key Question Answered:")
    print("   Does parser need pre-existing fields in state schema?")
    print("   Run this test to find out!")
