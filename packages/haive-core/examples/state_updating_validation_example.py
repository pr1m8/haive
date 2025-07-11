"""Example demonstrating StateUpdatingValidationNode with dual state update and routing."""

from typing import Any, Dict, List, Union

from langchain_core.messages import AIMessage, ToolMessage
from langgraph.graph import END, StateGraph
from langgraph.types import Send

from haive.core.graph.node.state_updating_validation_node import (
    StateUpdatingValidationNode,
    ValidationMode,
)


class ExampleAgentState:
    """Example state for demonstration."""

    def __init__(self):
        self.messages = []
        self.tools = []
        self.tool_routes = {}
        self.engines = {}
        self.validation_state = None
        self.error_tool_calls = []
        self.iteration_count = 0

    def get_tool_calls(self) -> list[dict[str, Any]]:
        """Get tool calls from last AI message."""
        if not self.messages:
            return []

        last_msg = self.messages[-1]
        if isinstance(last_msg, AIMessage) and hasattr(last_msg, "tool_calls"):
            return last_msg.tool_calls or []
        return []

    def apply_validation_results(self, validation_state):
        """Apply validation results to state."""
        self.validation_state = validation_state


def setup_example_state() -> ExampleAgentState:
    """Create example state with tools and routes."""
    state = ExampleAgentState()

    # Mock tools
    class MockTool:
        def __init__(self, name, route):
            self.name = name
            self._route = route

    # Add tools
    state.tools = [
        MockTool("web_search", "langchain_tool"),
        MockTool("calculator", "function"),
        MockTool("DocumentGenerator", "pydantic_model"),
        MockTool("memory_retriever", "retriever"),
    ]

    # Set up routes
    state.tool_routes = {
        "web_search": "langchain_tool",
        "calculator": "function",
        "DocumentGenerator": "pydantic_model",
        "memory_retriever": "retriever",
    }

    return state


def create_dual_validation_graph():
    """Create a graph that uses both validation node functions."""
    # Define the graph
    graph = StateGraph(ExampleAgentState)

    # Create validation node with dual functionality
    validator = StateUpdatingValidationNode(
        name="dual_validator",
        validation_mode=ValidationMode.PARTIAL,
        update_messages=True,
        track_error_tools=True,
        add_validation_metadata=True,
        route_to_node_mapping={
            "langchain_tool": "tool_executor",
            "function": "tool_executor",
            "pydantic_model": "structured_parser",
            "retriever": "memory_retriever",
            "unknown": "tool_executor",
        },
    )

    # Get both functions from the validator
    validation_updater = validator.create_node_function()
    validation_router = validator.create_router_function()

    # Agent node that generates tool calls
    def agent_node(state: ExampleAgentState) -> ExampleAgentState:
        """Generate AI response with tool calls."""
        state.iteration_count += 1

        # Create different scenarios based on iteration
        if state.iteration_count == 1:
            # First iteration: valid tools
            tool_calls = [
                {
                    "id": "call_1",
                    "name": "web_search",
                    "args": {"query": "Python tutorials"},
                },
                {
                    "id": "call_2",
                    "name": "calculator",
                    "args": {"expression": "10 * 5"},
                },
            ]
        elif state.iteration_count == 2:
            # Second iteration: mixed valid/invalid
            tool_calls = [
                {
                    "id": "call_3",
                    "name": "DocumentGenerator",
                    "args": {"title": "Report"},
                },
                {"id": "call_4", "name": "unknown_tool", "args": {"param": "value"}},
                {
                    "id": "call_5",
                    "name": "memory_retriever",
                    "args": {"query": "previous results"},
                },
            ]
        else:
            # Final iteration: no tools
            ai_msg = AIMessage(content="Task completed successfully!")
            state.messages.append(ai_msg)
            return state

        ai_msg = AIMessage(
            content=f"Iteration {state.iteration_count}: Processing request...",
            tool_calls=tool_calls,
        )
        state.messages.append(ai_msg)

        for _tc in tool_calls:
            pass

        return state

    # State updating validation node
    def state_validator_node(state: ExampleAgentState) -> ExampleAgentState:
        """Update state with validation results."""
        # This updates the state with validation results
        updated_state = validation_updater(state, {})

        # Print validation summary
        if updated_state.validation_state:
            vs = updated_state.validation_state
            vs.get_routing_decision()

            # Show error details
            for tool_id in vs.error_tool_calls:
                vs.tool_validations[tool_id]

        return updated_state

    # Router node that uses validation state
    def router_node(state: ExampleAgentState) -> list[Send] | str:
        """Route based on validation state."""
        # Use the router function to get routing decision
        routing_result = validation_router(state)

        if isinstance(routing_result, list):
            for send in routing_result:
                send.arg.get("name", "unknown")
            return routing_result
        if isinstance(routing_result, str):
            return routing_result
        return routing_result

    # Tool execution nodes
    def tool_executor_node(
        state: ExampleAgentState, tool_call: dict[str, Any]
    ) -> ExampleAgentState:
        """Execute a tool call."""
        tool_name = tool_call["name"]
        tool_id = tool_call["id"]
        args = tool_call.get("args", {})

        # Simulate tool execution
        if tool_name == "web_search":
            result = f"Found 10 results for query: {args.get('query', 'N/A')}"
        elif tool_name == "calculator":
            result = f"Calculation result: {args.get('expression', 'N/A')} = 50"
        else:
            result = f"Executed {tool_name} with args: {args}"

        # Create tool message
        tool_msg = ToolMessage(content=result, tool_call_id=tool_id, name=tool_name)
        state.messages.append(tool_msg)

        return state

    def structured_parser_node(
        state: ExampleAgentState, tool_call: dict[str, Any]
    ) -> ExampleAgentState:
        """Handle structured output parsing."""
        tool_name = tool_call["name"]
        tool_id = tool_call["id"]
        args = tool_call.get("args", {})

        # Simulate structured parsing
        result = f"Generated structured output: {tool_name} with title '{args.get('title', 'Unknown')}'"

        tool_msg = ToolMessage(content=result, tool_call_id=tool_id, name=tool_name)
        state.messages.append(tool_msg)

        return state

    def memory_retriever_node(
        state: ExampleAgentState, tool_call: dict[str, Any]
    ) -> ExampleAgentState:
        """Handle memory retrieval."""
        tool_name = tool_call["name"]
        tool_id = tool_call["id"]
        args = tool_call.get("args", {})

        result = f"Retrieved memories for query: {args.get('query', 'N/A')}"

        tool_msg = ToolMessage(content=result, tool_call_id=tool_id, name=tool_name)
        state.messages.append(tool_msg)

        return state

    # Add nodes to graph
    graph.add_node("agent", agent_node)
    graph.add_node("state_validator", state_validator_node)
    graph.add_node("router", router_node)
    graph.add_node("tool_executor", tool_executor_node)
    graph.add_node("structured_parser", structured_parser_node)
    graph.add_node("memory_retriever", memory_retriever_node)

    # Define flow
    graph.set_entry_point("agent")

    # Conditional edge from agent
    def should_validate(state: ExampleAgentState) -> str:
        """Determine if we should validate tool calls."""
        if not state.messages:
            return END

        last_msg = state.messages[-1]
        if (
            isinstance(last_msg, AIMessage)
            and hasattr(last_msg, "tool_calls")
            and last_msg.tool_calls
        ):
            return "state_validator"
        return END

    graph.add_conditional_edges("agent", should_validate)

    # State validator always goes to router
    graph.add_edge("state_validator", "router")

    # Router uses Send objects - no explicit edges needed
    # Tool nodes return to agent
    graph.add_edge("tool_executor", "agent")
    graph.add_edge("structured_parser", "agent")
    graph.add_edge("memory_retriever", "agent")

    return graph.compile()


def demonstrate_dual_validation():
    """Demonstrate the dual validation pattern."""
    # Create graph
    graph = create_dual_validation_graph()

    # Setup initial state
    initial_state = setup_example_state()

    for tool in initial_state.tools:
        initial_state.tool_routes.get(tool.name, "unknown")

    # Run the graph

    try:
        # Execute graph
        result = graph.invoke(initial_state)

        if result.validation_state:
            vs = result.validation_state
            vs.get_routing_decision()

        if result.error_tool_calls:
            pass

    except Exception:
        import traceback

        traceback.print_exc()


def explain_pattern():
    """Explain the dual validation pattern."""


if __name__ == "__main__":
    demonstrate_dual_validation()
    explain_pattern()
