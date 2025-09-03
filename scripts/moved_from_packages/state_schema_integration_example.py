"""Example showing how StateUpdatingValidationNode integrates with state schemas."""

from dataclasses import dataclass
from enum import Enum
from typing import Any


# Mock the state schema components for demonstration
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


@dataclass
class MockValidationResult:
    tool_call_id: str
    tool_name: str
    status: MockValidationStatus
    route_recommendation: MockRouteRecommendation = MockRouteRecommendation.EXECUTE
    errors: list[str] = None
    target_node: str | None = None
    metadata: dict[str, Any] = None
    priority: int = 0

    def __post_init__(self):
        self.errors = self.errors or []
        self.metadata = self.metadata or {}


class MockValidationRoutingState:
    """Mock validation routing state that matches the real implementation."""

    def __init__(self):
        self.tool_validations: dict[str, MockValidationResult] = {}
        self.valid_tool_calls: list[str] = []
        self.invalid_tool_calls: list[str] = []
        self.error_tool_calls: list[str] = []
        self.target_nodes: set = set()
        self.next_action = MockRouteRecommendation.EXECUTE
        self.total_tools = 0

    def add_validation_result(self, result: MockValidationResult):
        """Add a validation result to the state."""
        self.tool_validations[result.tool_call_id] = result
        self.total_tools += 1

        if result.status == MockValidationStatus.VALID:
            self.valid_tool_calls.append(result.tool_call_id)
            if result.target_node:
                self.target_nodes.add(result.target_node)
        elif result.status == MockValidationStatus.INVALID:
            self.invalid_tool_calls.append(result.tool_call_id)
        elif result.status == MockValidationStatus.ERROR:
            self.error_tool_calls.append(result.tool_call_id)

    def get_routing_decision(self) -> dict[str, Any]:
        """Get routing decision data for conditional branching."""
        return {
            "valid_count": len(self.valid_tool_calls),
            "invalid_count": len(self.invalid_tool_calls),
            "error_count": len(self.error_tool_calls),
            "total_count": self.total_tools,
            "has_valid_tools": len(self.valid_tool_calls) > 0,
            "has_errors": len(self.error_tool_calls) > 0,
            "should_continue": len(self.valid_tool_calls) > 0,
            "target_nodes": list(self.target_nodes),
        }

    def get_valid_tool_calls(self) -> list[MockValidationResult]:
        """Get results for valid tool calls."""
        return [self.tool_validations[tool_id] for tool_id in self.valid_tool_calls]

    def get_routing_summary(self) -> str:
        """Get summary for logging."""
        decision = self.get_routing_decision()
        return f"Valid: {decision['valid_count']}, Invalid: {decision['invalid_count']}, Error: {decision['error_count']}"


class MockAIMessage:
    """Mock AI message with tool calls."""

    def __init__(self, content: str, tool_calls: list[dict[str, Any]] | None = None):
        self.content = content
        self.tool_calls = tool_calls or []


class MockTool:
    """Mock tool with name and optional schema."""

    def __init__(self, name: str, args_schema=None):
        self.name = name
        self.args_schema = args_schema


class MockSend:
    """Mock Send object for routing."""

    def __init__(self, node: str, arg: Any):
        self.node = node
        self.arg = arg


# State schema implementations
class BaseToolState:
    """Base tool state that matches ToolState functionality."""

    def __init__(self):
        self.messages = []
        self.tools = []
        self.tool_routes = {}
        self.engines = {}
        self.tool_metadata = {}
        self.tool_priorities = {}
        self.tool_dependencies = {}
        self.engine_route_config = {
            "llm": ["langchain_tool", "function", "pydantic_model"],
            "aug_llm": ["langchain_tool", "function", "pydantic_model"],
            "retriever": ["retriever"],
            "parser": ["pydantic_model"],
        }

    def get_tool_calls(self) -> list[dict[str, Any]]:
        """Get tool calls from last AI message (computed field equivalent)."""
        if not self.messages:
            return []

        last_msg = self.messages[-1]
        if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
            return last_msg.tool_calls
        return []

    def add_tool(
        self,
        tool: Any,
        route: str | None = None,
        target_engine: str | None = None,
    ):
        """Add a tool to the state."""
        self.tools.append(tool)
        tool_name = getattr(tool, "name", str(tool))

        if route:
            self.tool_routes[tool_name] = route
        elif callable(tool):
            self.tool_routes[tool_name] = "function"
        else:
            self.tool_routes[tool_name] = "langchain_tool"

    def get_tool_by_name(self, name: str) -> Any | None:
        """Get tool by name."""
        for tool in self.tools:
            if getattr(tool, "name", str(tool)) == name:
                return tool
        return None


class EnhancedToolState(BaseToolState):
    """Enhanced tool state with validation capabilities."""

    def __init__(self):
        super().__init__()
        # Validation and routing state
        self.validation_state = MockValidationRoutingState()

        # Enhanced tool management
        self.tool_performance = {}
        self.tool_execution_history = []
        self.tool_categories = {}

        # Message management
        self.tool_message_status = {}

        # Conditional branching support
        self.branch_conditions = {}

        # Error tracking
        self.error_tool_calls = []

    def apply_validation_results(self, validation_state: MockValidationRoutingState):
        """Apply validation results to update tool message states."""
        # Update our validation state
        self.validation_state = validation_state

        # Update tool message statuses
        for tool_call_id, result in validation_state.tool_validations.items():
            self.tool_message_status[tool_call_id] = result.status.value

        # Update branch conditions with routing data
        self.branch_conditions.update(validation_state.get_routing_decision())

    def get_validation_routing_data(self) -> dict[str, Any]:
        """Get data for conditional branching based on validation results."""
        base_data = self.validation_state.get_routing_decision()

        # Add additional routing information
        base_data.update(
            {
                "tool_message_statuses": self.tool_message_status.copy(),
                "available_categories": list(self.tool_categories.keys()),
                "total_tools_in_state": len(self.tools),
                "has_dependencies": len(self.tool_dependencies) > 0,
            }
        )

        return base_data

    def should_continue_to_tools(self) -> bool:
        """Check if execution should continue to tool nodes."""
        return self.validation_state.get_routing_decision()["should_continue"]

    def should_return_to_agent(self) -> bool:
        """Check if execution should return to agent for clarification."""
        decision = self.validation_state.get_routing_decision()
        return decision["error_count"] > 0 and decision["valid_count"] == 0

    def get_next_nodes(self) -> list[str]:
        """Get recommended next nodes based on validation results."""
        return list(self.validation_state.target_nodes)


# Simplified StateUpdatingValidationNode
class StateSchemaValidationNode:
    """Validation node designed to work with state schemas."""

    def __init__(self, name="schema_validator"):
        self.name = name

    def create_node_function(self):
        """Create function that updates state with validation results."""

        def validation_node(state: EnhancedToolState) -> EnhancedToolState:
            # Get tool calls using state's computed field equivalent
            tool_calls = state.get_tool_calls()
            if not tool_calls:
                return state

            # Create validation state
            validation_state = MockValidationRoutingState()

            # Validate each tool call against state's tools and routes
            for tool_call in tool_calls:
                result = self._validate_tool_call(tool_call, state)
                validation_state.add_validation_result(result)

                if result.errors:
                    pass

            # Apply validation results to state using state's method
            state.apply_validation_results(validation_state)

            # Show state updates
            state.get_validation_routing_data()

            return state

        return validation_node

    def create_router_function(self):
        """Create function that routes based on state's validation results."""

        def validation_router(state: EnhancedToolState) -> list[MockSend] | str:
            # Use state's validation data for routing
            state.get_validation_routing_data()

            # Check if we should return to agent
            if state.should_return_to_agent():
                return "agent"

            # Check if we should continue to tools
            if not state.should_continue_to_tools():
                return "__END__"

            # Create Send objects for valid tools
            sends = []
            valid_results = state.validation_state.get_valid_tool_calls()
            tool_calls = state.get_tool_calls()
            tool_call_map = {tc["id"]: tc for tc in tool_calls}

            for result in valid_results:
                tool_call = tool_call_map.get(result.tool_call_id)
                if tool_call:
                    # Enhance tool call with validation metadata
                    enhanced_call = tool_call.copy()
                    enhanced_call["validation_metadata"] = {
                        "status": result.status.value,
                        "target_node": result.target_node,
                        "route": state.tool_routes.get(result.tool_name),
                    }

                    sends.append(MockSend(result.target_node, enhanced_call))

            return sends

        return validation_router

    def _validate_tool_call(
        self, tool_call: dict[str, Any], state: EnhancedToolState
    ) -> MockValidationResult:
        """Validate a tool call against state's tools and routes."""
        tool_name = tool_call.get("name", "unknown")
        tool_id = tool_call.get("id", f"call_{id(tool_call)}")

        # Check if tool exists in state
        tool = state.get_tool_by_name(tool_name)
        if not tool:
            return MockValidationResult(
                tool_call_id=tool_id,
                tool_name=tool_name,
                status=MockValidationStatus.ERROR,
                route_recommendation=MockRouteRecommendation.AGENT,
                errors=[f"Tool '{tool_name}' not found in state"],
                target_node="agent",
            )

        # Get route from state
        route = state.tool_routes.get(tool_name, "unknown")

        # Determine target node based on route
        route_to_node = {
            "langchain_tool": "tool_executor",
            "function": "tool_executor",
            "pydantic_model": "structured_parser",
            "retriever": "retriever_node",
            "unknown": "tool_executor",
        }
        target_node = route_to_node.get(route, "tool_executor")

        # Tool is valid
        return MockValidationResult(
            tool_call_id=tool_id,
            tool_name=tool_name,
            status=MockValidationStatus.VALID,
            route_recommendation=MockRouteRecommendation.EXECUTE,
            target_node=target_node,
            metadata={"route": route},
        )


def demonstrate_state_schema_integration():
    """Demonstrate how validation node works with state schemas."""
    # Create validation node
    validator = StateSchemaValidationNode("schema_validator")
    node_func = validator.create_node_function()
    router_func = validator.create_router_function()

    # Create enhanced state
    state = EnhancedToolState()

    # Setup tools in state (like ToolState would)
    state.add_tool(MockTool("web_search"), route="langchain_tool")
    state.add_tool(MockTool("calculator"), route="function")
    state.add_tool(MockTool("DocumentGenerator"), route="pydantic_model")

    # Add AI message with tool calls
    ai_message = MockAIMessage(
        content="Processing multiple tools",
        tool_calls=[
            {"id": "call_1", "name": "web_search", "args": {"query": "python"}},
            {"id": "call_2", "name": "calculator", "args": {"expr": "2+2"}},
            {"id": "call_3", "name": "unknown_tool", "args": {}},  # This will fail
            {"id": "call_4", "name": "DocumentGenerator", "args": {"title": "Report"}},
        ],
    )
    state.messages.append(ai_message)

    # Step 1: Run validation node (updates state)

    updated_state = node_func(state)

    # Show state after validation
    updated_state.get_validation_routing_data()

    # Step 2: Run router (uses updated state)

    routing_result = router_func(updated_state)

    # Show routing results
    if isinstance(routing_result, list):
        for _i, send in enumerate(routing_result):
            send.arg.get("name", "unknown")
    else:
        pass

    # Step 3: Show how state can be used for conditional branching

    # Show how to use branch conditions in graph

    # Show state schema benefits


def show_schema_structure():
    """Show the state schema structure and relationships."""


if __name__ == "__main__":
    demonstrate_state_schema_integration()
    show_schema_structure()
