"""Simple test of StateUpdatingValidationNode without LangGraph dependencies."""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Any, Dict, List

from src.haive.core.graph.node.state_updating_validation_node import (
    StateUpdatingValidationNode,
    ValidationMode,
)
from src.haive.core.schema.prebuilt.tools.validation_state import (
    RouteRecommendation,
    ValidationStatus,
)


class MockAIMessage:
    """Mock AI message for testing."""

    def __init__(self, content: str, tool_calls: List[Dict[str, Any]] = None):
        self.content = content
        self.tool_calls = tool_calls or []


class MockToolMessage:
    """Mock tool message."""

    def __init__(self, content: str, name: str = None, **kwargs):
        self.content = content
        self.name = name
        for k, v in kwargs.items():
            setattr(self, k, v)


class MockState:
    """Mock state for testing."""

    def __init__(self):
        self.messages = []
        self.tools = []
        self.tool_routes = {}
        self.engines = {}
        self.validation_state = None
        self.error_tool_calls = []

    def get_tool_calls(self) -> List[Dict[str, Any]]:
        """Get tool calls from last AI message."""
        if not self.messages:
            return []

        last_msg = self.messages[-1]
        if hasattr(last_msg, "tool_calls"):
            return last_msg.tool_calls or []
        return []

    def apply_validation_results(self, validation_state):
        """Apply validation results to state."""
        self.validation_state = validation_state


class MockTool:
    """Mock tool for testing."""

    def __init__(self, name: str, has_schema: bool = False):
        self.name = name
        self.args_schema = None
        if has_schema:
            # Mock schema that validates everything
            class MockSchema:
                @staticmethod
                def model_validate(args):
                    if args.get("invalid"):
                        raise ValueError("Invalid arguments")
                    return args

            self.args_schema = MockSchema()


def test_basic_functionality():
    """Test basic StateUpdatingValidationNode functionality."""

    print("🧪 Testing StateUpdatingValidationNode")
    print("=" * 50)

    # Create node
    node = StateUpdatingValidationNode(
        name="test_validator",
        validation_mode=ValidationMode.PARTIAL,
        update_messages=True,
        track_error_tools=True,
    )

    print(f"✅ Created node: {node.name}")
    print(f"   Mode: {node.validation_mode}")
    print(f"   Update messages: {node.update_messages}")
    print(f"   Track errors: {node.track_error_tools}")

    # Get functions
    node_func = node.create_node_function()
    router_func = node.create_router_function()

    print(f"✅ Created node function and router function")

    return node, node_func, router_func


def test_validation_scenarios():
    """Test different validation scenarios."""

    print(f"\\n🎯 Testing Validation Scenarios")
    print("-" * 40)

    node, node_func, router_func = test_basic_functionality()

    # Scenario 1: Valid tools
    print(f"\\n📝 Scenario 1: Valid Tools")
    state = MockState()
    state.tools = [MockTool("search"), MockTool("calculator")]
    state.tool_routes = {"search": "langchain_tool", "calculator": "function"}

    ai_msg = MockAIMessage(
        content="Processing request",
        tool_calls=[
            {"id": "1", "name": "search", "args": {"query": "test"}},
            {"id": "2", "name": "calculator", "args": {"expr": "2+2"}},
        ],
    )
    state.messages.append(ai_msg)

    # Run validation
    updated_state = node_func(state)
    print(f"  ✅ State updated with validation results")

    # Check validation state
    if updated_state.validation_state:
        vs = updated_state.validation_state
        summary = vs.get_routing_decision()
        print(f"     Valid: {summary['valid_count']}, Errors: {summary['error_count']}")

    # Run router
    routing_result = router_func(updated_state)
    print(f"  🔀 Router result type: {type(routing_result).__name__}")
    if isinstance(routing_result, list):
        print(f"     Created {len(routing_result)} routing branches")

    # Scenario 2: Invalid tools
    print(f"\\n📝 Scenario 2: Invalid Tools")
    state2 = MockState()
    state2.tools = [MockTool("search")]
    state2.tool_routes = {"search": "langchain_tool"}

    ai_msg2 = MockAIMessage(
        content="Bad request",
        tool_calls=[{"id": "3", "name": "unknown_tool", "args": {}}],
    )
    state2.messages.append(ai_msg2)

    updated_state2 = node_func(state2)
    print(f"  ✅ State updated with validation results")

    if updated_state2.validation_state:
        vs2 = updated_state2.validation_state
        summary2 = vs2.get_routing_decision()
        print(
            f"     Valid: {summary2['valid_count']}, Errors: {summary2['error_count']}"
        )

    routing_result2 = router_func(updated_state2)
    print(f"  🔀 Router result: {routing_result2}")

    # Scenario 3: Mixed tools
    print(f"\\n📝 Scenario 3: Mixed Valid/Invalid Tools")
    state3 = MockState()
    state3.tools = [MockTool("search"), MockTool("writer", has_schema=True)]
    state3.tool_routes = {"search": "langchain_tool", "writer": "pydantic_model"}

    ai_msg3 = MockAIMessage(
        content="Mixed request",
        tool_calls=[
            {"id": "4", "name": "search", "args": {"query": "test"}},
            {"id": "5", "name": "unknown_tool", "args": {}},
            {"id": "6", "name": "writer", "args": {"text": "hello"}},
        ],
    )
    state3.messages.append(ai_msg3)

    updated_state3 = node_func(state3)
    print(f"  ✅ State updated with validation results")

    if updated_state3.validation_state:
        vs3 = updated_state3.validation_state
        summary3 = vs3.get_routing_decision()
        print(
            f"     Valid: {summary3['valid_count']}, Errors: {summary3['error_count']}"
        )

    routing_result3 = router_func(updated_state3)
    print(f"  🔀 Router result type: {type(routing_result3).__name__}")
    if isinstance(routing_result3, list):
        print(f"     Created {len(routing_result3)} routing branches")


def test_validation_modes():
    """Test different validation modes."""

    print(f"\\n⚙️ Testing Validation Modes")
    print("-" * 40)

    # Setup test state with mixed results
    def create_mixed_state():
        state = MockState()
        state.tools = [MockTool("good_tool")]
        state.tool_routes = {"good_tool": "function"}

        ai_msg = MockAIMessage(
            content="Mixed tools",
            tool_calls=[
                {"id": "1", "name": "good_tool", "args": {}},
                {"id": "2", "name": "bad_tool", "args": {}},
            ],
        )
        state.messages.append(ai_msg)
        return state

    # Test STRICT mode
    print(f"\\n🔒 STRICT Mode:")
    strict_node = StateUpdatingValidationNode(validation_mode=ValidationMode.STRICT)
    node_func = strict_node.create_node_function()
    router_func = strict_node.create_router_function()

    state = create_mixed_state()
    updated_state = node_func(state)
    result = router_func(updated_state)
    print(f"   Result: {result} (should route to agent due to failure)")

    # Test PERMISSIVE mode
    print(f"\\n🔓 PERMISSIVE Mode:")
    permissive_node = StateUpdatingValidationNode(
        validation_mode=ValidationMode.PERMISSIVE
    )
    node_func = permissive_node.create_node_function()
    router_func = permissive_node.create_router_function()

    state = create_mixed_state()
    updated_state = node_func(state)
    result = router_func(updated_state)
    print(
        f"   Result type: {type(result).__name__} (should create Send branches for valid tools)"
    )

    # Test PARTIAL mode (default)
    print(f"\\n⚖️ PARTIAL Mode:")
    partial_node = StateUpdatingValidationNode(validation_mode=ValidationMode.PARTIAL)
    node_func = partial_node.create_node_function()
    router_func = partial_node.create_router_function()

    state = create_mixed_state()
    updated_state = node_func(state)
    result = router_func(updated_state)
    print(
        f"   Result type: {type(result).__name__} (should create Send branches for valid tools)"
    )


def test_dynamic_behavior():
    """Test dynamic router behavior based on state changes."""

    print(f"\\n🔄 Testing Dynamic Behavior")
    print("-" * 40)

    node = StateUpdatingValidationNode()
    node_func = node.create_node_function()
    router_func = node.create_router_function()

    # Initial state
    state = MockState()
    state.tools = [MockTool("tool1")]
    state.tool_routes = {"tool1": "function"}

    ai_msg = MockAIMessage(
        content="First request", tool_calls=[{"id": "1", "name": "tool1", "args": {}}]
    )
    state.messages.append(ai_msg)

    # First validation
    state = node_func(state)
    result1 = router_func(state)
    print(f"   First result: {type(result1).__name__}")

    # Add new tool and update routes
    state.tools.append(MockTool("tool2"))
    state.tool_routes["tool2"] = "langchain_tool"

    # New tool calls
    ai_msg2 = MockAIMessage(
        content="Second request",
        tool_calls=[
            {"id": "2", "name": "tool1", "args": {}},
            {"id": "3", "name": "tool2", "args": {}},
        ],
    )
    state.messages.append(ai_msg2)

    # Second validation - router should adapt
    state = node_func(state)
    result2 = router_func(state)
    print(f"   Second result: {type(result2).__name__}")

    if isinstance(result2, list):
        print(f"   Router adapted: now routing {len(result2)} tools")


def main():
    """Run all tests."""

    print("🚀 StateUpdatingValidationNode Test Suite")
    print("=" * 60)

    try:
        test_validation_scenarios()
        test_validation_modes()
        test_dynamic_behavior()

        print(f"\\n✅ All tests completed successfully!")

        print(f"\\n💡 Key Features Demonstrated:")
        print("   - Dual functionality: state updates + routing")
        print("   - Different validation modes (STRICT, PARTIAL, PERMISSIVE)")
        print("   - Dynamic router behavior based on state")
        print("   - Error tracking and message updates")
        print("   - Tool route mapping and Send branch creation")

    except Exception as e:
        print(f"\\n❌ Test failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
