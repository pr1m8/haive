"""Test the updated schema inheritance hierarchy.

This script validates that the new inheritance hierarchy works correctly:
MessagesState → MessagesStateWithTokenUsage → ToolState → LLMState

And that SchemaComposer detects the appropriate base class.
"""

import asyncio

from langchain_core.tools import tool

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.schema.prebuilt.llm_state import LLMState
from haive.core.schema.prebuilt.messages.messages_with_token_usage import (
    MessagesStateWithTokenUsage,
)
from haive.core.schema.prebuilt.messages_state import MessagesState
from haive.core.schema.prebuilt.tool_state import ToolState
from haive.core.schema.schema_composer import SchemaComposer


def test_inheritance_hierarchy():
    """Test that the inheritance hierarchy is correct."""
    print("🧪 Testing inheritance hierarchy...")

    # Test inheritance chain
    assert issubclass(MessagesStateWithTokenUsage, MessagesState)
    assert issubclass(ToolState, MessagesStateWithTokenUsage)
    assert issubclass(LLMState, ToolState)

    print("✅ Inheritance hierarchy correct:")
    print("   MessagesState → MessagesStateWithTokenUsage → ToolState → LLMState")


def test_field_inheritance():
    """Test that fields are properly inherited through the chain."""
    print("\n🧪 Testing field inheritance...")

    # Create LLMState instance
    engine = AugLLMConfig(name="test_engine")
    llm_state = LLMState(engine=engine)

    # Check that it has fields from all parent classes
    assert hasattr(llm_state, "messages")  # From MessagesState
    assert hasattr(llm_state, "token_usage")  # From MessagesStateWithTokenUsage
    assert hasattr(llm_state, "tools")  # From ToolState
    assert hasattr(llm_state, "tool_routes")  # From ToolState
    assert hasattr(llm_state, "engine")  # From LLMState
    assert hasattr(llm_state, "warning_threshold")  # From LLMState

    print("✅ All fields inherited correctly")


def test_schema_composer_detection():
    """Test that SchemaComposer detects the right base classes."""
    print("\n🧪 Testing SchemaComposer base class detection...")

    # Test 1: Just messages → MessagesStateWithTokenUsage
    composer1 = SchemaComposer(name="MessageOnlyState")
    composer1.add_field("messages", list, default_factory=list)
    composer1._detect_base_class_requirements()

    expected_base = composer1.detected_base_class
    print(f"   Messages only → {expected_base.__name__}")
    assert expected_base.__name__ == "MessagesStateWithTokenUsage"

    # Test 2: Tools (without LLM) → ToolState
    @tool
    def dummy_tool(query: str) -> str:
        """A dummy tool."""
        return f"Result for {query}"

    composer2 = SchemaComposer(name="ToolOnlyState")
    composer2.add_field("tools", list, default_factory=list)
    composer2.add_field("tool_routes", dict, default_factory=dict)
    composer2._detect_base_class_requirements()

    expected_base = composer2.detected_base_class
    print(f"   Tools only → {expected_base.__name__}")
    assert expected_base.__name__ == "ToolState"

    # Test 3: Tools + Single LLM Engine → LLMState
    engine = AugLLMConfig(name="test_llm")
    composer3 = SchemaComposer(name="LLMWithToolsState")
    composer3.add_engine(engine)
    composer3.add_field("tools", list, default_factory=list)
    composer3._detect_base_class_requirements()

    expected_base = composer3.detected_base_class
    print(f"   Tools + Single LLM → {expected_base.__name__}")
    assert expected_base.__name__ == "LLMState"

    print("✅ SchemaComposer detection working correctly")


def test_tool_syncing():
    """Test that tools sync properly through the inheritance chain."""
    print("\n🧪 Testing tool syncing...")

    @tool
    def calculator(expression: str) -> str:
        """Calculate mathematical expressions."""
        return str(eval(expression))

    # Create LLMState with tools
    engine = AugLLMConfig(name="llm_with_tools", tools=[calculator])
    llm_state = LLMState(engine=engine)

    # Check that tools synced properly
    assert len(llm_state.tools) > 0
    assert hasattr(llm_state, "tool_routes")
    assert len(llm_state.tool_routes) > 0

    # Check engine references
    assert "main" in llm_state.engines
    assert "llm" in llm_state.engines
    assert llm_state.engines["main"] == engine

    print("✅ Tool syncing working correctly")


def test_token_tracking():
    """Test that token tracking works through inheritance."""
    print("\n🧪 Testing token tracking inheritance...")

    from langchain_core.messages import AIMessage

    # Create LLMState
    engine = AugLLMConfig(name="token_test")
    llm_state = LLMState(engine=engine)

    # Add message with token usage (OpenAI pattern)
    ai_message = AIMessage(
        content="Test response",
        response_metadata={
            "usage": {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15}
        },
    )

    # Debug: Test token extraction first
    from haive.core.schema.prebuilt.messages.token_usage import (
        extract_token_usage_from_message,
    )

    extracted_usage = extract_token_usage_from_message(ai_message)
    print(f"   Extracted usage: {extracted_usage}")

    llm_state.add_message(ai_message)

    # Debug: Check what happened
    print(f"   Messages: {len(llm_state.messages)}")
    print(f"   Token usage: {llm_state.token_usage}")
    print(f"   Token usage history: {llm_state.token_usage_history}")

    # Verify token tracking works
    assert (
        llm_state.token_usage is not None
    ), f"Token usage is None, but should be tracked. Messages: {len(llm_state.messages)}"
    assert llm_state.token_usage.total_tokens == 15

    # Test LLMState-specific features
    assert hasattr(llm_state, "token_usage_percentage")
    assert hasattr(llm_state, "context_length")
    assert hasattr(llm_state, "is_approaching_token_limit")

    print("✅ Token tracking inheritance working correctly")


def main():
    """Run all tests."""
    print("🚀 Testing Updated Schema Inheritance Hierarchy\n")

    try:
        test_inheritance_hierarchy()
        test_field_inheritance()
        test_schema_composer_detection()
        test_tool_syncing()
        test_token_tracking()

        print("\n🎉 All tests passed! The inheritance hierarchy is working correctly.")
        print("\nSummary:")
        print("✅ MessagesState → MessagesStateWithTokenUsage → ToolState → LLMState")
        print("✅ SchemaComposer detects appropriate base classes")
        print("✅ Field inheritance works across the chain")
        print("✅ Tool syncing works properly")
        print("✅ Token tracking inherited correctly")

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
