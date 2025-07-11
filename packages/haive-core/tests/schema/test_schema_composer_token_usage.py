#!/usr/bin/env python3
"""Test that SchemaComposer uses MessagesStateWithTokenUsage by default."""

import sys
from typing import Any, Dict

from haive.core.schema import SchemaComposer
from haive.core.schema.prebuilt import MessagesState, MessagesStateWithTokenUsage


def test_auto_detection_uses_token_aware_state():
    """Test that auto-detection uses MessagesStateWithTokenUsage for messages."""

    # Create a mock component that requires messages
    class MockLLMEngine:
        engine_type = "llm"
        name = "test_llm"

        def get_input_fields(self) -> Dict[str, Any]:
            return {"messages": list}

    # Create schema using auto-detection
    composer = SchemaComposer(name="TestState")
    composer._detect_base_class_requirements([MockLLMEngine()])

    # Should detect MessagesStateWithTokenUsage
    assert (
        composer.detected_base_class == MessagesStateWithTokenUsage
    ), f"Expected MessagesStateWithTokenUsage, got {composer.detected_base_class}"

    print("✓ Auto-detection uses MessagesStateWithTokenUsage for messages")


def test_custom_base_schema_override():
    """Test that custom base schema overrides auto-detection."""
    # Use regular MessagesState as custom base
    composer = SchemaComposer(name="TestState", base_state_schema=MessagesState)

    # Should use the custom base even if we detect messages
    class MockLLMEngine:
        engine_type = "llm"
        name = "test_llm"

    composer._detect_base_class_requirements([MockLLMEngine()])

    # Should keep the custom base
    assert (
        composer.detected_base_class == MessagesState
    ), f"Expected MessagesState (custom), got {composer.detected_base_class}"

    print("✓ Custom base schema properly overrides auto-detection")


def test_from_components_with_custom_base():
    """Test from_components class method with custom base schema."""

    # Mock component
    class MockComponent:
        def get_input_fields(self):
            return {"messages": list}

    # Create with custom base
    schema_class = SchemaComposer.from_components(
        [MockComponent()], name="TestState", base_state_schema=MessagesState
    )

    # Check the created schema
    assert issubclass(schema_class, MessagesState)
    print("✓ from_components accepts custom base schema")


def test_build_creates_correct_schema():
    """Test that build() creates a schema with the correct base."""
    composer = SchemaComposer(name="TestState")

    # Add a field that triggers messages detection
    composer.add_field("messages", list, default_factory=list)

    # Build the schema
    schema_class = composer.build()

    # Should be based on MessagesStateWithTokenUsage
    assert issubclass(
        schema_class, MessagesStateWithTokenUsage
    ), f"Expected subclass of MessagesStateWithTokenUsage, got {schema_class.__bases__}"

    # Should have token tracking capabilities
    instance = schema_class()
    assert hasattr(instance, "token_usage"), "Schema should have token_usage field"
    assert hasattr(
        instance, "get_token_usage_summary"
    ), "Schema should have token usage methods"

    print("✓ Built schema has token tracking capabilities")


def main():
    """Run all tests."""
    print("Testing SchemaComposer token usage improvements...\n")

    try:
        test_auto_detection_uses_token_aware_state()
        test_custom_base_schema_override()
        test_from_components_with_custom_base()
        test_build_creates_correct_schema()

        print("\n✅ All tests passed!")

    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
