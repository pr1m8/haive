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

    def get_tool_calls(self) -> List[Dict[str, Any]]:
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

        print(
            f"\\n🤖 Agent (Iteration {state.iteration_count}): Generated {len(tool_calls)} tool calls"
        )
        for tc in tool_calls:
            print(f"  - {tc['name']} (id: {tc['id']})")

        return state

    # State updating validation node
    def state_validator_node(state: ExampleAgentState) -> ExampleAgentState:
        """Update state with validation results."""
        print(f"\\n📋 State Validator: Processing validation and updating state...")

        # This updates the state with validation results
        updated_state = validation_updater(state, {})

        # Print validation summary
        if updated_state.validation_state:
            vs = updated_state.validation_state
            summary = vs.get_routing_decision()
            print(f"  ✅ Valid tools: {summary['valid_count']}")
            print(f"  ❌ Invalid tools: {summary['invalid_count']}")
            print(f"  💥 Error tools: {summary['error_count']}")

            # Show error details
            for tool_id in vs.error_tool_calls:
                result = vs.tool_validations[tool_id]
                print(f"    - {result.tool_name}: {', '.join(result.errors)}")

        return updated_state

    # Router node that uses validation state
    def router_node(state: ExampleAgentState) -> Union[List[Send], str]:
        """Route based on validation state."""
        print(f"\\n🔀 Router: Making routing decisions...")

        # Use the router function to get routing decision
        routing_result = validation_router(state)

        if isinstance(routing_result, list):
            print(f"  📤 Created {len(routing_result)} Send branches:")
            for send in routing_result:
                tool_name = send.arg.get("name", "unknown")
                print(f"    - {tool_name} → {send.node}")
            return routing_result
        elif isinstance(routing_result, str):
            print(f"  🎯 Single route: {routing_result}")
            return routing_result
        else:
            print(f"  🏁 Ending: {routing_result}")
            return routing_result

    # Tool execution nodes
    def tool_executor_node(
        state: ExampleAgentState, tool_call: Dict[str, Any]
    ) -> ExampleAgentState:
        """Execute a tool call."""
        tool_name = tool_call["name"]
        tool_id = tool_call["id"]
        args = tool_call.get("args", {})

        print(f"🔧 Tool Executor: Executing {tool_name}")

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

        print(f"  ✅ Result: {result}")
        return state

    def structured_parser_node(
        state: ExampleAgentState, tool_call: Dict[str, Any]
    ) -> ExampleAgentState:
        """Handle structured output parsing."""
        tool_name = tool_call["name"]
        tool_id = tool_call["id"]
        args = tool_call.get("args", {})

        print(f"📄 Structured Parser: Processing {tool_name}")

        # Simulate structured parsing
        result = f"Generated structured output: {tool_name} with title '{args.get('title', 'Unknown')}'"

        tool_msg = ToolMessage(content=result, tool_call_id=tool_id, name=tool_name)
        state.messages.append(tool_msg)

        print(f"  ✅ Parsed: {result}")
        return state

    def memory_retriever_node(
        state: ExampleAgentState, tool_call: Dict[str, Any]
    ) -> ExampleAgentState:
        """Handle memory retrieval."""
        tool_name = tool_call["name"]
        tool_id = tool_call["id"]
        args = tool_call.get("args", {})

        print(f"🧠 Memory Retriever: Retrieving for {tool_name}")

        result = f"Retrieved memories for query: {args.get('query', 'N/A')}"

        tool_msg = ToolMessage(content=result, tool_call_id=tool_id, name=tool_name)
        state.messages.append(tool_msg)

        print(f"  ✅ Retrieved: {result}")
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
        else:
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

    print("🚀 Dual Validation Node Demonstration")
    print("=" * 60)
    print("This shows a validation node that:")
    print("1. Updates state with validation results")
    print("2. Provides dynamic routing based on validation")
    print("3. Tracks errors and adds validation metadata")
    print("=" * 60)

    # Create graph
    graph = create_dual_validation_graph()

    # Setup initial state
    initial_state = setup_example_state()

    print(f"\\n📚 Available Tools:")
    for tool in initial_state.tools:
        route = initial_state.tool_routes.get(tool.name, "unknown")
        print(f"  - {tool.name} (route: {route})")

    # Run the graph
    print(f"\\n🌊 Execution Flow:")
    print("-" * 40)

    try:
        # Execute graph
        result = graph.invoke(initial_state)

        print(f"\\n🏁 Final State Summary:")
        print(f"  - Total messages: {len(result.messages)}")
        print(f"  - Iterations: {result.iteration_count}")

        if result.validation_state:
            vs = result.validation_state
            summary = vs.get_routing_decision()
            print(
                f"  - Final validation: {summary['valid_count']} valid, {summary['error_count']} errors"
            )

        if result.error_tool_calls:
            print(f"  - Error tools tracked: {len(result.error_tool_calls)}")

    except Exception as e:
        print(f"❌ Error during execution: {e}")
        import traceback

        traceback.print_exc()


def explain_pattern():
    """Explain the dual validation pattern."""

    print(f"\\n💡 Key Concepts:")
    print("-" * 30)

    print(f"\\n1. **Dual Function Pattern**:")
    print("   - create_node_function(): Updates state with validation results")
    print("   - create_router_function(): Routes based on updated validation state")
    print("   - Same validation logic, different responsibilities")

    print(f"\\n2. **State Updates**:")
    print("   - Validation results stored in state.validation_state")
    print("   - Error tools tracked in state.error_tool_calls")
    print("   - Validation metadata added to tool calls")
    print("   - Error messages added to state.messages")

    print(f"\\n3. **Dynamic Routing**:")
    print("   - Router function reads validation state from state")
    print("   - Creates Send objects for valid tools")
    print("   - Routes to agent on failures (configurable)")
    print("   - Supports different validation modes (STRICT, PARTIAL, PERMISSIVE)")

    print(f"\\n4. **Validation Modes**:")
    print("   - STRICT: Any failure routes to agent")
    print("   - PARTIAL: Continue with valid tools (default)")
    print("   - PERMISSIVE: Only route to agent if all fail")

    print(f"\\n5. **Integration Pattern**:")
    print("   - Use state_validator node to update state")
    print("   - Use router node to make routing decisions")
    print("   - Router function can change behavior based on state")
    print("   - Both functions share same validation configuration")


if __name__ == "__main__":
    demonstrate_dual_validation()
    explain_pattern()

    print(f"\\n🔍 Implementation Notes:")
    print("-" * 40)
    print("- StateUpdatingValidationNode provides both functions")
    print("- Node function and router function can be used independently")
    print("- Router adapts to changes in validation state")
    print("- Pattern enables complex validation workflows")
    print("- Maintains backward compatibility with existing code")
