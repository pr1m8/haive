"""Direct test of validation node v2 - bypassing __init__.py imports."""

import os
import sys

# Add direct path to the validation node file
current_dir = os.path.dirname(__file__)
core_src = os.path.join(current_dir, "..", "..", "..", "haive-core", "src")
sys.path.insert(0, core_src)


def test_direct_validation_node_import():
    """Test importing validation node directly."""
    print("🧪 Testing Direct ValidationNode V2 Import")

    try:
        # Import directly, bypassing __init__.py
        module_path = os.path.join(
            core_src,
            "haive",
            "core",
            "graph",
            "node",
            "state_updating_validation_node_v2.py",
        )

        print(f"Module path: {module_path}")
        print(f"Module exists: {os.path.exists(module_path)}")

        # Try direct import without using haive.core.__init__.py
        import importlib.util

        spec = importlib.util.spec_from_file_location("validation_node_v2", module_path)
        validation_module = importlib.util.module_from_spec(spec)

        # Mock the dependencies before loading
        import unittest.mock

        # Create proper message mocks
        class MockAIMessage:
            def __init__(self, **kwargs):
                for key, value in kwargs.items():
                    setattr(self, key, value)

        class MockToolMessage:
            def __init__(self, content="", name=None, **kwargs):
                self.content = content
                self.name = name
                for key, value in kwargs.items():
                    setattr(self, key, value)

        mock_langchain_messages = unittest.mock.MagicMock()
        mock_langchain_messages.AIMessage = MockAIMessage
        mock_langchain_messages.ToolMessage = MockToolMessage

        mock_langgraph_types = unittest.mock.MagicMock()
        mock_langgraph_types.Send = type(
            "Send", (), {"__init__": lambda self, node, arg: None}
        )
        mock_langgraph_types.END = "__END__"

        # Create proper Pydantic mocks
        class MockBaseModel:
            def __init__(self, **kwargs):
                for key, value in kwargs.items():
                    setattr(self, key, value)

        def mock_field(**kwargs):
            if "default_factory" in kwargs:
                return kwargs["default_factory"]()
            return kwargs.get("default", None)

        mock_pydantic = unittest.mock.MagicMock()
        mock_pydantic.BaseModel = MockBaseModel
        mock_pydantic.Field = mock_field

        # Add mocks to sys.modules before executing
        sys.modules["langchain_core.messages"] = mock_langchain_messages
        sys.modules["langgraph.types"] = mock_langgraph_types
        sys.modules["pydantic"] = mock_pydantic

        # Execute the module
        spec.loader.exec_module(validation_module)

        print("✅ Module imported successfully")

        # Test basic functionality
        ValidationMode = validation_module.ValidationMode
        StateUpdatingValidationNodeV2 = validation_module.StateUpdatingValidationNodeV2
        ValidationResult = validation_module.ValidationResult

        print("✅ Core classes accessible")

        # Test enum values
        assert hasattr(ValidationMode, "STRICT")
        assert hasattr(ValidationMode, "PARTIAL")
        assert hasattr(ValidationMode, "PERMISSIVE")
        print("✅ ValidationMode enum working")

        # Test ValidationResult creation
        result = ValidationResult(
            tool_call_id="test", tool_name="test_tool", status="valid"
        )
        print("✅ ValidationResult creation working")

        # Test StateUpdatingValidationNodeV2 creation
        node = StateUpdatingValidationNodeV2(
            name="test_node", validation_mode=ValidationMode.PARTIAL
        )
        print("✅ StateUpdatingValidationNodeV2 creation working")

        # Test function creation
        state_updater = node.create_state_updater()
        router = node.create_router()

        assert callable(state_updater)
        assert callable(router)
        print("✅ Function creation working")

        print("✅ All direct tests passed!")
        return True

    except Exception as e:
        print(f"❌ Direct test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_simple_workflow():
    """Test a simple workflow with mock state."""
    print("\n🧪 Testing Simple Workflow")

    try:
        # Re-import the working module
        module_path = os.path.join(
            core_src,
            "haive",
            "core",
            "graph",
            "node",
            "state_updating_validation_node_v2.py",
        )

        import importlib.util

        spec = importlib.util.spec_from_file_location("validation_node_v2", module_path)
        validation_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(validation_module)

        ValidationMode = validation_module.ValidationMode
        StateUpdatingValidationNodeV2 = validation_module.StateUpdatingValidationNodeV2

        # Create validation node
        node = StateUpdatingValidationNodeV2(
            name="workflow_test", validation_mode=ValidationMode.PARTIAL
        )

        # Create mock state
        class MockState:
            def __init__(self):
                self.messages = []
                self.tools = []
                self.tool_routes = {}
                self.validation_results = []
                self.error_tool_calls = []

            def get_tool_calls(self):
                return [
                    {"id": "1", "name": "test_tool", "args": {}},
                    {"id": "2", "name": "unknown_tool", "args": {}},
                ]

        # Create mock tool
        class MockTool:
            def __init__(self, name):
                self.name = name

        state = MockState()
        state.tools = [MockTool("test_tool")]
        state.tool_routes = {"test_tool": "langchain_tool"}

        # Test state updater
        state_updater = node.create_state_updater()
        updated_state = state_updater(state)

        assert hasattr(updated_state, "validation_results")
        assert len(updated_state.validation_results) == 2
        print("✅ State updater working")

        # Test router
        router = node.create_router()
        routing_result = router(updated_state)

        # Should route to agent since there are errors and we're using mock Send
        assert routing_result is not None
        print("✅ Router working")

        print("✅ Simple workflow test passed!")
        return True

    except Exception as e:
        print(f"❌ Workflow test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def run_direct_tests():
    """Run direct tests."""
    print("🚀 Running Direct Validation Node V2 Tests")
    print("=" * 60)

    # Memory anchor
    MEMORY_ANCHOR = {
        "goal": "Test v2 validation node works without full haive imports",
        "approach": "Direct module import with mocked dependencies",
        "validation": "Core functionality and workflow",
    }

    print("🧠 Memory Anchor:")
    for key, value in MEMORY_ANCHOR.items():
        print(f"   {key}: {value}")
    print()

    tests = [
        ("Direct Import Test", test_direct_validation_node_import),
        ("Simple Workflow Test", test_simple_workflow),
    ]

    results = []
    for test_name, test_func in tests:
        print(f"{'='*60}")
        print(f"🧪 {test_name}")
        print(f"{'='*60}")

        try:
            result = test_func()
            results.append((test_name, "PASS" if result else "FAIL"))
        except Exception as e:
            print(f"❌ {test_name} failed: {e}")
            results.append((test_name, "ERROR"))

    # Summary
    print(f"\n{'='*60}")
    print("🎯 DIRECT TEST SUMMARY")
    print(f"{'='*60}")

    for test_name, status in results:
        icon = "✅" if status == "PASS" else "❌"
        print(f"   {icon} {test_name}: {status}")

    passed = sum(1 for _, status in results if status == "PASS")
    total = len(results)

    print(f"\n📊 Results: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All direct tests passed!")
        print("\n💡 V2 Implementation Status:")
        print("   ✅ Core validation node functional")
        print("   ✅ Can be imported independently")
        print("   ✅ Basic workflow operational")
        print("   ✅ Ready for integration when dependencies available")

    return passed == total


if __name__ == "__main__":
    success = run_direct_tests()
    sys.exit(0 if success else 1)
