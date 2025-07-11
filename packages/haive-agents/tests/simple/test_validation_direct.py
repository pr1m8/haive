"""Direct test of validation node v2 - bypassing __init__.py imports."""

import os
import sys

# Add direct path to the validation node file
current_dir = os.path.dirname(__file__)
core_src = os.path.join(current_dir, "..", "..", "..", "haive-core", "src")
sys.path.insert(0, core_src)


def test_direct_validation_node_import():
    """Test importing validation node directly."""

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
            return kwargs.get("default")

        mock_pydantic = unittest.mock.MagicMock()
        mock_pydantic.BaseModel = MockBaseModel
        mock_pydantic.Field = mock_field

        # Add mocks to sys.modules before executing
        sys.modules["langchain_core.messages"] = mock_langchain_messages
        sys.modules["langgraph.types"] = mock_langgraph_types
        sys.modules["pydantic"] = mock_pydantic

        # Execute the module
        spec.loader.exec_module(validation_module)


        # Test basic functionality
        ValidationMode = validation_module.ValidationMode
        StateUpdatingValidationNodeV2 = validation_module.StateUpdatingValidationNodeV2
        ValidationResult = validation_module.ValidationResult


        # Test enum values
        assert hasattr(ValidationMode, "STRICT")
        assert hasattr(ValidationMode, "PARTIAL")
        assert hasattr(ValidationMode, "PERMISSIVE")

        # Test ValidationResult creation
        ValidationResult(
            tool_call_id="test", tool_name="test_tool", status="valid"
        )

        # Test StateUpdatingValidationNodeV2 creation
        node = StateUpdatingValidationNodeV2(
            name="test_node", validation_mode=ValidationMode.PARTIAL
        )

        # Test function creation
        state_updater = node.create_state_updater()
        router = node.create_router()

        assert callable(state_updater)
        assert callable(router)

        return True

    except Exception as e:
        import traceback

        traceback.print_exc()
        return False


def test_simple_workflow():
    """Test a simple workflow with mock state."""

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

        # Test router
        router = node.create_router()
        routing_result = router(updated_state)

        # Should route to agent since there are errors and we're using mock Send
        assert routing_result is not None

        return True

    except Exception as e:
        import traceback

        traceback.print_exc()
        return False


def run_direct_tests():
    """Run direct tests."""

    # Memory anchor
    MEMORY_ANCHOR = {
        "goal": "Test v2 validation node works without full haive imports",
        "approach": "Direct module import with mocked dependencies",
        "validation": "Core functionality and workflow",
    }

    for key, value in MEMORY_ANCHOR.items():
        pass

    tests = [
        ("Direct Import Test", test_direct_validation_node_import),
        ("Simple Workflow Test", test_simple_workflow),
    ]

    results = []
    for test_name, test_func in tests:

        try:
            result = test_func()
            results.append((test_name, "PASS" if result else "FAIL"))
        except Exception as e:
            results.append((test_name, "ERROR"))

    # Summary

    for test_name, status in results:
        icon = "✅" if status == "PASS" else "❌"

    passed = sum(1 for _, status in results if status == "PASS")
    total = len(results)


    if passed == total:

    return passed == total


if __name__ == "__main__":
    success = run_direct_tests()
    sys.exit(0 if success else 1)
