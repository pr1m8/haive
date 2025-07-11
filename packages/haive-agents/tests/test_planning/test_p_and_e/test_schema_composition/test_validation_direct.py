"""Direct test of StateUpdatingValidationNode without complex imports."""

import os
import sys

# Add the package to Python path
sys.path.insert(0, "packages/haive-core/src")

from enum import Enum

# Direct imports of only what we need


# Mock the required dependencies
class MockValidationStatus(str, Enum):
    PENDING = "pending"
    VALID = "valid"
    INVALID = "invalid"
    ERROR = "error"
    SKIPPED = "skipped"


class MockRouteRecommendation(str, Enum):
    EXECUTE = "execute"
    RETRY = "retry"
    SKIP = "skip"
    REDIRECT = "redirect"
    AGENT = "agent"
    END = "end"


class MockValidationResult:
    def __init__(
        self,
        tool_call_id,
        tool_name,
        status,
        route_recommendation=None,
        errors=None,
        target_node=None,
        metadata=None,
        priority=0,
    ):
        self.tool_call_id = tool_call_id
        self.tool_name = tool_name
        self.status = status
        self.route_recommendation = route_recommendation
        self.errors = errors or []
        self.target_node = target_node
        self.metadata = metadata or {}
        self.priority = priority


class MockValidationRoutingState:
    def __init__(self):
        self.tool_validations = {}
        self.valid_tool_calls = []
        self.invalid_tool_calls = []
        self.error_tool_calls = []

    def add_validation_result(self, result):
        self.tool_validations[result.tool_call_id] = result
        if result.status == MockValidationStatus.VALID:
            self.valid_tool_calls.append(result.tool_call_id)
        elif result.status == MockValidationStatus.INVALID:
            self.invalid_tool_calls.append(result.tool_call_id)
        elif result.status == MockValidationStatus.ERROR:
            self.error_tool_calls.append(result.tool_call_id)

    def get_routing_decision(self):
        return {
            "valid_count": len(self.valid_tool_calls),
            "invalid_count": len(self.invalid_tool_calls),
            "error_count": len(self.error_tool_calls),
            "total_count": len(self.tool_validations),
        }

    def get_valid_tool_calls(self):
        return [self.tool_validations[tool_id] for tool_id in self.valid_tool_calls]

    def get_error_tool_calls(self):
        return [self.tool_validations[tool_id] for tool_id in self.error_tool_calls]

    def get_invalid_tool_calls(self):
        return [self.tool_validations[tool_id] for tool_id in self.invalid_tool_calls]


class MockValidationStateManager:
    @staticmethod
    def create_routing_state():
        return MockValidationRoutingState()

    @staticmethod
    def create_validation_result(**kwargs):
        return MockValidationResult(**kwargs)


# Mock Send class
class MockSend:
    def __init__(self, node, arg):
        self.node = node
        self.arg = arg


# Mock END
END = "__END__"


# Now let's implement a simplified version of the validation node
class ValidationMode(str, Enum):
    STRICT = "strict"
    PARTIAL = "partial"
    PERMISSIVE = "permissive"


class SimpleStateUpdatingValidationNode:
    """Simplified version for testing core functionality."""

    def __init__(
        self,
        name="state_validation",
        validation_mode=ValidationMode.PARTIAL,
        update_messages=True,
        track_error_tools=True,
        add_validation_metadata=True,
        agent_node="agent",
        tool_node="tool_node",
        parser_node="parser_node",
    ):
        self.name = name
        self.validation_mode = validation_mode
        self.update_messages = update_messages
        self.track_error_tools = track_error_tools
        self.add_validation_metadata = add_validation_metadata
        self.agent_node = agent_node
        self.tool_node = tool_node
        self.parser_node = parser_node

        self.route_to_node_mapping = {
            "langchain_tool": tool_node,
            "function": tool_node,
            "pydantic_model": parser_node,
            "retriever": "retriever_node",
            "unknown": tool_node,
        }

    def create_node_function(self):
        """Create the state-updating validation node function."""

        def validation_node(state, config=None):

            # Get tool calls
            tool_calls = self._extract_tool_calls(state)
            if not tool_calls:
                return state

            # Get tools and routes
            available_tools, tool_routes = self._get_tools_and_routes(state)

            # Create validation state
            routing_state = MockValidationStateManager.create_routing_state()

            # Validate each tool
            for tool_call in tool_calls:
                result = self._validate_tool_call(
                    tool_call, available_tools, tool_routes
                )
                routing_state.add_validation_result(result)

            # Apply to state
            self._apply_validation_to_state(state, routing_state, tool_calls)

            routing_state.get_routing_decision()

            return state

        return validation_node

    def create_router_function(self):
        """Create the dynamic router function."""

        def validation_router(state):

            # Get validation state
            validation_state = getattr(state, "validation_state", None)
            if not validation_state:
                return END

            # Get routing decision
            routing_decision = validation_state.get_routing_decision()

            # Check validation mode
            if self.validation_mode == ValidationMode.STRICT:
                if (
                    routing_decision["error_count"] > 0
                    or routing_decision["invalid_count"] > 0
                ):
                    return self.agent_node

            elif self.validation_mode == ValidationMode.PERMISSIVE:
                if routing_decision["valid_count"] == 0:
                    return self.agent_node

            # Get valid tools
            valid_results = validation_state.get_valid_tool_calls()
            if not valid_results:
                return self.agent_node if routing_decision["total_count"] > 0 else END

            # Create Send objects
            sends = self._create_send_branches(state, valid_results)

            if sends:
                return sends
            return self.agent_node

        return validation_router

    def _extract_tool_calls(self, state):
        """Extract tool calls from state."""
        if hasattr(state, "get_tool_calls"):
            return state.get_tool_calls()

        messages = getattr(state, "messages", [])
        if not messages:
            return []

        last_msg = messages[-1]
        if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
            return last_msg.tool_calls

        return []

    def _get_tools_and_routes(self, state):
        """Get available tools and routes."""
        available_tools = {}
        tool_routes = {}

        # Get from state
        if hasattr(state, "tools"):
            for tool in state.tools:
                tool_name = getattr(tool, "name", str(tool))
                available_tools[tool_name] = tool

        if hasattr(state, "tool_routes"):
            tool_routes.update(state.tool_routes)

        return available_tools, tool_routes

    def _validate_tool_call(self, tool_call, available_tools, tool_routes):
        """Validate a single tool call."""
        tool_name = tool_call.get("name", "unknown")
        tool_id = tool_call.get("id", f"call_{id(tool_call)}")
        tool_call.get("args", {})

        # Check if tool exists
        if tool_name not in available_tools:
            return MockValidationStateManager.create_validation_result(
                tool_call_id=tool_id,
                tool_name=tool_name,
                status=MockValidationStatus.ERROR,
                route_recommendation=MockRouteRecommendation.AGENT,
                errors=[f"Tool '{tool_name}' not found"],
                target_node=self.agent_node,
            )

        # Get route and target
        route = tool_routes.get(tool_name, "unknown")
        target_node = self.route_to_node_mapping.get(route, self.tool_node)

        # For this test, assume all found tools are valid
        return MockValidationStateManager.create_validation_result(
            tool_call_id=tool_id,
            tool_name=tool_name,
            status=MockValidationStatus.VALID,
            route_recommendation=MockRouteRecommendation.EXECUTE,
            target_node=target_node,
            metadata={"route": route},
        )

    def _apply_validation_to_state(self, state, routing_state, original_tool_calls):
        """Apply validation results to state."""
        # Apply validation state
        if not hasattr(state, "validation_state"):
            state.validation_state = routing_state
        else:
            state.validation_state = routing_state

        # Track error tools
        if self.track_error_tools:
            if not hasattr(state, "error_tool_calls"):
                state.error_tool_calls = []

            for tool_id in routing_state.error_tool_calls:
                error_result = routing_state.tool_validations[tool_id]
                state.error_tool_calls.append(
                    {
                        "tool_name": error_result.tool_name,
                        "tool_id": tool_id,
                        "errors": error_result.errors,
                    }
                )

    def _create_send_branches(self, state, valid_results):
        """Create Send branches for valid tools."""
        sends = []

        # Get original tool calls
        tool_calls = self._extract_tool_calls(state)
        tool_call_map = {tc["id"]: tc for tc in tool_calls}

        for result in valid_results:
            tool_call = tool_call_map.get(result.tool_call_id)
            if not tool_call:
                continue

            # Create enhanced tool call
            enhanced_call = tool_call.copy()
            enhanced_call["validation_metadata"] = {
                "status": result.status.value,
                "target_node": result.target_node,
                "route": result.metadata.get("route") if result.metadata else None,
            }

            # Create Send
            sends.append(MockSend(result.target_node, enhanced_call))

        return sends


# Test classes
class MockTool:
    def __init__(self, name):
        self.name = name


class MockAIMessage:
    def __init__(self, content, tool_calls=None):
        self.content = content
        self.tool_calls = tool_calls or []


class MockState:
    def __init__(self):
        self.messages = []
        self.tools = []
        self.tool_routes = {}
        self.validation_state = None
        self.error_tool_calls = []

    def get_tool_calls(self):
        if not self.messages:
            return []
        last_msg = self.messages[-1]
        if hasattr(last_msg, "tool_calls"):
            return last_msg.tool_calls
        return []


def test_validation_node():
    """Test the validation node functionality."""
    # Create validation node
    node = SimpleStateUpdatingValidationNode(
        name="test_validator",
        validation_mode=ValidationMode.PARTIAL,
        update_messages=True,
        track_error_tools=True,
    )

    # Get both functions
    node_func = node.create_node_function()
    router_func = node.create_router_function()

    # Test scenario 1: Valid tools
    state1 = MockState()
    state1.tools = [MockTool("search"), MockTool("calculator")]
    state1.tool_routes = {"search": "langchain_tool", "calculator": "function"}

    ai_msg1 = MockAIMessage(
        content="Process request",
        tool_calls=[
            {"id": "1", "name": "search", "args": {"query": "test"}},
            {"id": "2", "name": "calculator", "args": {"expr": "2+2"}},
        ],
    )
    state1.messages.append(ai_msg1)

    # Run validation (state update)
    updated_state1 = node_func(state1)

    # Check validation results
    if updated_state1.validation_state:
        updated_state1.validation_state.get_routing_decision()

    # Run router
    routing_result1 = router_func(updated_state1)
    if isinstance(routing_result1, list):
        for send in routing_result1:
            send.arg.get("name", "unknown")

    # Test scenario 2: Invalid tools
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
        updated_state2.validation_state.get_routing_decision()

    router_func(updated_state2)

    # Test scenario 3: Mixed tools
    state3 = MockState()
    state3.tools = [MockTool("search"), MockTool("writer")]
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
        updated_state3.validation_state.get_routing_decision()

    routing_result3 = router_func(updated_state3)
    if isinstance(routing_result3, list):
        for send in routing_result3:
            send.arg.get("name", "unknown")

    # Test validation modes

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

    # STRICT mode
    strict_node = SimpleStateUpdatingValidationNode(
        validation_mode=ValidationMode.STRICT
    )
    strict_func = strict_node.create_node_function()
    strict_router = strict_node.create_router_function()

    state = create_mixed_state()
    state = strict_func(state)
    result = strict_router(state)

    # PERMISSIVE mode
    permissive_node = SimpleStateUpdatingValidationNode(
        validation_mode=ValidationMode.PERMISSIVE
    )
    permissive_func = permissive_node.create_node_function()
    permissive_router = permissive_node.create_router_function()

    state = create_mixed_state()
    state = permissive_func(state)
    result = permissive_router(state)
    if isinstance(result, list):
        pass


if __name__ == "__main__":
    test_validation_node()
