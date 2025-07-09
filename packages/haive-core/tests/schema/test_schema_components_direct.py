"""Direct test of schema components without engine dependencies."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../src"))


def test_direct_imports():
    """Test direct imports of schema components."""
    print("🧪 Testing Direct Schema Component Imports...")

    try:
        # Import schema components directly
        from haive.core.schema.prebuilt.messages.token_usage import TokenUsage
        from haive.core.schema.prebuilt.messages.token_usage_mixin import (
            TokenUsageMixin,
        )
        from haive.core.schema.prebuilt.messages_state import MessagesState
        from haive.core.schema.schema_composer import SchemaComposer
        from haive.core.schema.state_schema import StateSchema

        print("✅ Direct imports successful")
        return True
    except Exception as e:
        print(f"❌ Direct import failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_state_schema_direct():
    """Test StateSchema directly."""
    print("🧪 Testing StateSchema Direct...")

    try:
        from haive.core.schema.state_schema import StateSchema

        # Create instance
        state = StateSchema()

        # Test basic functionality
        assert hasattr(state, "engines")
        assert isinstance(state.engines, dict)

        # Test methods exist (just check they exist, don't call them)
        assert hasattr(state, "model_dump")
        assert hasattr(state, "to_dict")

        print("✅ StateSchema direct test successful")
        return True
    except Exception as e:
        print(f"❌ StateSchema direct test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_schema_composer_direct():
    """Test SchemaComposer directly."""
    print("🧪 Testing SchemaComposer Direct...")

    try:
        from haive.core.schema.schema_composer import SchemaComposer

        # Create instance
        composer = SchemaComposer("TestSchema")

        # Test methods exist
        assert hasattr(composer, "add_field")
        assert hasattr(composer, "build")

        # Test building a simple schema
        schema_class = composer.build()
        assert schema_class is not None

        # Test instance creation
        instance = schema_class()
        assert instance is not None

        print("✅ SchemaComposer direct test successful")
        return True
    except Exception as e:
        print(f"❌ SchemaComposer direct test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_messages_state_direct():
    """Test MessagesState directly."""
    print("🧪 Testing MessagesState Direct...")

    try:
        from haive.core.schema.prebuilt.messages_state import MessagesState

        # Create instance
        messages_state = MessagesState()

        # Test basic functionality
        assert hasattr(messages_state, "messages")
        assert isinstance(messages_state.messages, list)

        # Test methods exist
        assert hasattr(messages_state, "add_message")
        assert hasattr(messages_state, "get_last_message")

        print("✅ MessagesState direct test successful")
        return True
    except Exception as e:
        print(f"❌ MessagesState direct test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_token_usage_direct():
    """Test TokenUsage directly."""
    print("🧪 Testing TokenUsage Direct...")

    try:
        from haive.core.schema.prebuilt.messages.token_usage import TokenUsage
        from haive.core.schema.prebuilt.messages.token_usage_mixin import (
            TokenUsageMixin,
        )

        # Test TokenUsage creation
        usage = TokenUsage(input_tokens=100, output_tokens=50)
        assert usage.input_tokens == 100
        assert usage.output_tokens == 50
        assert usage.total_tokens == 150

        # Test TokenUsageMixin
        class TestState(TokenUsageMixin):
            test_field: str = "test"

        state = TestState()
        assert hasattr(state, "get_token_usage")

        print("✅ TokenUsage direct test successful")
        return True
    except Exception as e:
        print(f"❌ TokenUsage direct test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_multi_agent_state_direct():
    """Test MultiAgentStateSchema directly."""
    print("🧪 Testing MultiAgentStateSchema Direct...")

    try:
        from haive.core.schema.multi_agent_state_schema import MultiAgentStateSchema

        # Create instance
        multi_state = MultiAgentStateSchema()

        # Test basic functionality
        assert multi_state is not None
        assert hasattr(multi_state, "engines")

        print("✅ MultiAgentStateSchema direct test successful")
        return True
    except Exception as e:
        print(f"❌ MultiAgentStateSchema direct test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def run_all_tests():
    """Run all direct schema component tests."""
    print("🚀 Running Direct Schema Component Tests")
    print("=" * 50)

    tests = [
        test_direct_imports,
        test_state_schema_direct,
        test_schema_composer_direct,
        test_messages_state_direct,
        test_token_usage_direct,
        test_multi_agent_state_direct,
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

    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(
        f"📈 Success Rate: {passed}/{passed + failed} ({100 * passed / (passed + failed):.1f}%)"
    )

    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! Schema components work correctly.")
        print("✅ Fixed import issues and verified core functionality.")
    else:
        print(f"\n⚠️  {failed} tests failed. Need to fix issues before proceeding.")

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
