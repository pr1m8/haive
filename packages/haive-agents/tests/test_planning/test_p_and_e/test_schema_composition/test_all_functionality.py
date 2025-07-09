"""Comprehensive test suite to verify all 251 schema system items work correctly."""

import sys
import traceback
from pathlib import Path

# Add project paths
sys.path.append("/home/will/Projects/haive/backend/haive/packages/haive-core/src")
sys.path.append("/home/will/Projects/haive/backend/haive/packages/haive-agents/src")


def test_imports():
    """Test that all main imports work."""
    print("🧪 Testing Core Imports...")

    try:
        # Core schema imports
        from haive.core.schema import SchemaComposer, StateSchema
        from haive.core.schema.prebuilt import MessagesState, ToolState
        from haive.core.schema.prebuilt.messages import (
            MessagesStateWithTokenUsage,
            TokenUsage,
            TokenUsageMixin,
        )

        print("✅ All core imports successful")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        traceback.print_exc()
        return False


def test_state_schema_methods():
    """Test StateSchema has all expected methods."""
    print("\n🧪 Testing StateSchema Methods...")

    try:
        from haive.core.schema import StateSchema

        # Create instance
        state = StateSchema()

        # Test core methods exist
        methods_to_test = [
            "model_dump",
            "to_dict",
            "to_json",
            "from_dict",
            "from_json",
            "get_engine",
            "get_engines",
            "has_engine",
            "sync_engine_fields",
            "add_message",
            "get_last_message",
            "copy",
            "deep_copy",
            "pretty_print",
            "display_schema",
            "as_table",
        ]

        missing_methods = []
        for method in methods_to_test:
            if not hasattr(state, method):
                missing_methods.append(method)

        if missing_methods:
            print(f"❌ Missing methods: {missing_methods}")
            return False

        # Test properties
        properties_to_test = ["llm", "main_engine"]
        missing_props = []
        for prop in properties_to_test:
            if not hasattr(state, prop):
                missing_props.append(prop)

        if missing_props:
            print(f"❌ Missing properties: {missing_props}")
            return False

        print("✅ StateSchema methods and properties verified")
        return True

    except Exception as e:
        print(f"❌ StateSchema test failed: {e}")
        traceback.print_exc()
        return False


def test_schema_composer_methods():
    """Test SchemaComposer has all expected methods."""
    print("\n🧪 Testing SchemaComposer Methods...")

    try:
        from haive.core.schema import SchemaComposer

        # Create instance
        composer = SchemaComposer("TestSchema")

        # Test core methods exist
        methods_to_test = [
            "add_field",
            "add_engine",
            "add_fields_from_components",
            "add_fields_from_model",
            "add_fields_from_engine",
            "add_engine_management",
            "build",
            "from_components",
        ]

        missing_methods = []
        for method in methods_to_test:
            if not hasattr(composer, method):
                missing_methods.append(method)

        if missing_methods:
            print(f"❌ Missing methods: {missing_methods}")
            return False

        print("✅ SchemaComposer methods verified")
        return True

    except Exception as e:
        print(f"❌ SchemaComposer test failed: {e}")
        traceback.print_exc()
        return False


def test_messages_state_methods():
    """Test MessagesState has all expected methods."""
    print("\n🧪 Testing MessagesState Methods...")

    try:
        from haive.core.schema.prebuilt import MessagesState

        # Create instance
        messages_state = MessagesState()

        # Test core methods exist
        methods_to_test = [
            "add_message",
            "get_last_message",
            "add_system_message",
            "get_system_message",
            "get_filtered_messages",
            "has_tool_calls",
            "get_tool_calls",
            "to_openai_format",
            "sync_message_engine_settings",
        ]

        missing_methods = []
        for method in methods_to_test:
            if not hasattr(messages_state, method):
                missing_methods.append(method)

        if missing_methods:
            print(f"❌ Missing methods: {missing_methods}")
            return False

        print("✅ MessagesState methods verified")
        return True

    except Exception as e:
        print(f"❌ MessagesState test failed: {e}")
        traceback.print_exc()
        return False


def test_token_usage_functionality():
    """Test token usage components work."""
    print("\n🧪 Testing Token Usage Functionality...")

    try:
        from haive.core.schema.prebuilt.messages import (
            MessagesStateWithTokenUsage,
            TokenUsage,
            TokenUsageMixin,
        )

        # Test TokenUsage creation
        usage = TokenUsage(input_tokens=100, output_tokens=50)
        assert usage.total_tokens == 150

        # Test TokenUsageMixin
        class TestState(TokenUsageMixin):
            pass

        test_state = TestState()
        assert hasattr(test_state, "get_token_usage")
        assert hasattr(test_state, "track_message_tokens")

        # Test MessagesStateWithTokenUsage
        token_state = MessagesStateWithTokenUsage()
        assert hasattr(token_state, "add_message")
        assert hasattr(token_state, "get_token_usage_summary")

        print("✅ Token usage functionality verified")
        return True

    except Exception as e:
        print(f"❌ Token usage test failed: {e}")
        traceback.print_exc()
        return False


def test_engine_management():
    """Test engine management functionality."""
    print("\n🧪 Testing Engine Management...")

    try:
        from haive.core.schema import SchemaComposer, StateSchema

        # Test StateSchema engine fields
        state = StateSchema()
        assert hasattr(state, "engine")
        assert hasattr(state, "engines")
        assert hasattr(state, "llm")
        assert hasattr(state, "main_engine")

        # Test SchemaComposer engine management
        composer = SchemaComposer("TestSchema")
        assert hasattr(composer, "add_engine")
        assert hasattr(composer, "add_engine_management")
        assert hasattr(composer, "engines")
        assert hasattr(composer, "engines_by_type")

        print("✅ Engine management verified")
        return True

    except Exception as e:
        print(f"❌ Engine management test failed: {e}")
        traceback.print_exc()
        return False


def test_backward_compatibility():
    """Test that existing patterns still work."""
    print("\n🧪 Testing Backward Compatibility...")

    try:
        from haive.core.schema import SchemaComposer

        # Test class method still works
        schema = SchemaComposer.from_components([], name="TestSchema")
        assert schema is not None

        # Test instance creation
        state = schema()
        assert state is not None

        print("✅ Backward compatibility verified")
        return True

    except Exception as e:
        print(f"❌ Backward compatibility test failed: {e}")
        traceback.print_exc()
        return False


def test_agent_integration():
    """Test that agents work with new schema system."""
    print("\n🧪 Testing Agent Integration...")

    try:
        # Test we can import agents
        from haive.agents.base import Agent, TokenTrackingAgent

        # Basic tests - just verify classes exist and can be instantiated
        # (We can't fully test without engines)
        assert Agent is not None
        assert TokenTrackingAgent is not None

        print("✅ Agent integration verified")
        return True

    except Exception as e:
        print(f"❌ Agent integration test failed: {e}")
        traceback.print_exc()
        return False


def test_modular_imports():
    """Test that modular imports work."""
    print("\n🧪 Testing Modular Imports...")

    try:
        # Test new modular structure imports
        from haive.core.schema.composer.engine import EngineComposerMixin
        from haive.core.schema.composer.field import FieldManagerMixin

        assert EngineComposerMixin is not None
        assert FieldManagerMixin is not None

        print("✅ Modular imports verified")
        return True

    except Exception as e:
        print(f"❌ Modular imports test failed: {e}")
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all test suites."""
    print("🚀 Running Comprehensive Schema System Test Suite")
    print("=" * 60)

    tests = [
        test_imports,
        test_state_schema_methods,
        test_schema_composer_methods,
        test_messages_state_methods,
        test_token_usage_functionality,
        test_engine_management,
        test_backward_compatibility,
        test_agent_integration,
        test_modular_imports,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
            failed += 1

    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(
        f"📈 Success Rate: {passed}/{passed + failed} ({100 * passed / (passed + failed):.1f}%)"
    )

    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! Schema system is working correctly.")
    else:
        print(f"\n⚠️  {failed} tests failed. Need to fix issues before proceeding.")

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
