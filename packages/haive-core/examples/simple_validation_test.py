"""Simple test of StateUpdatingValidationNode without LangGraph dependencies."""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Any

from src.haive.core.graph.node.state_updating_validation_node import (
    StateUpdatingValidationNode,
    ValidationMode,
)


class MockAIMessage:
    """Mock AI message for testing."""

    def __init__(self, content: str, tool_calls: list[dict[str, Any]] | None = None):
        self.content = content
        self.tool_calls = tool_calls or []


class MockToolMessage:
    """Mock tool message."""

    def __init__(self, content: str, name: str | None = None, **kwargs):
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

    def get_tool_calls(self) -> list[dict[str, Any]]:
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
    # Create node
    node = StateUpdatingValidationNode(
        name="test_validator",
        validation_mode=ValidationMode.PARTIAL,
        update_messages=True,
        track_error_tools=True,
    )

    # Get functions
    node_func = node.create_node_function()
    router_func = node.create_router_function()

    return node, node_func, router_func


def test_validation_scenarios():
    """Test different validation scenarios."""
    node, node_func, router_func = test_basic_functionality()

    # Scenario 1: Valid tools
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

    # Check validation state
    if updated_state.validation_state:
        vs = updated_state.validation_state
        vs.get_routing_decision()

    # Run router
    routing_result = router_func(updated_state)
    if isinstance(routing_result, list):
        pass

    # Scenario 2: Invalid tools
    state2 = MockState()
    state2.tools = [MockTool("search")]
    state2.tool_routes = {"search": "langchain_tool"}

    ai_msg2 = MockAIMessage(
        content="Bad request",
        tool_calls=[{"id": "3", "name": "unknown_tool", "args": {}}],
    )
    state2.messages.append(ai_msg2)

    updated_state2 = node_func(state2)

    if updated_state2.validation_state:
        vs2 = updated_state2.validation_state
        vs2.get_routing_decision()

    router_func(updated_state2)

    # Scenario 3: Mixed tools
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

    if updated_state3.validation_state:
        vs3 = updated_state3.validation_state
        vs3.get_routing_decision()

    routing_result3 = router_func(updated_state3)
    if isinstance(routing_result3, list):
        pass


def test_validation_modes():
    """Test different validation modes."""

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
    strict_node = StateUpdatingValidationNode(validation_mode=ValidationMode.STRICT)
    node_func = strict_node.create_node_function()
    router_func = strict_node.create_router_function()

    state = create_mixed_state()
    updated_state = node_func(state)
    router_func(updated_state)

    # Test PERMISSIVE mode
    permissive_node = StateUpdatingValidationNode(
        validation_mode=ValidationMode.PERMISSIVE
    )
    node_func = permissive_node.create_node_function()
    router_func = permissive_node.create_router_function()

    state = create_mixed_state()
    updated_state = node_func(state)
    router_func(updated_state)

    # Test PARTIAL mode (default)
    partial_node = StateUpdatingValidationNode(validation_mode=ValidationMode.PARTIAL)
    node_func = partial_node.create_node_function()
    router_func = partial_node.create_router_function()

    state = create_mixed_state()
    updated_state = node_func(state)
    router_func(updated_state)


def test_dynamic_behavior():
    """Test dynamic router behavior based on state changes."""
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
    router_func(state)

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

    if isinstance(result2, list):
        pass


def main():
    """Run all tests."""
    try:
        test_validation_scenarios()
        test_validation_modes()
        test_dynamic_behavior()

    except Exception:
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
