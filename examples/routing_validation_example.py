"""Example of using routing validation node with Send branching."""

from typing import Any

from langchain_core.messages import AIMessage, ToolMessage
from langgraph.graph import END, StateGraph
from langgraph.types import Send


# Example state that inherits from ToolState
class AgentState:
    """Example state with tool management."""

    def __init__(self):
        self.messages = []
        self.tools = []
        self.tool_routes = {}
        self.engines = {}

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
        # This would update tool message statuses, branch conditions, etc.


def create_example_graph():
    """Create example graph with routing validation."""

    # Define the graph
    graph = StateGraph(AgentState)

    # Agent node that generates tool calls
    def agent_node(state: AgentState) -> AgentState:
        # Agent would generate an AI message with tool calls
        ai_message = AIMessage(
            content="I'll search for that information and calculate the result.",
            tool_calls=[
                {
                    "id": "call_001",
                    "name": "search_tool",
                    "args": {"query": "python tutorials"},
                },
                {
                    "id": "call_002",
                    "name": "calculator",
                    "args": {"expression": "2 + 2"},
                },
                {
                    "id": "call_003",
                    "name": "create_document",
                    "args": {"title": "Results", "content": "..."},
                },
            ],
        )
        state.messages.append(ai_message)
        return state

    # Routing validation node
    from haive.core.graph.node.routing_validation_node import (
        create_routing_validation_node,
    )

    routing_validator = create_routing_validation_node(
        engine_name="main_engine",
        route_to_node_mapping={
            "langchain_tool": "tool_executor",
            "pydantic_model": "structured_output",
            "function": "tool_executor",
        },
    )

    # Tool execution node
    def tool_executor(state: AgentState, tool_call: dict[str, Any]) -> AgentState:
        """Execute a validated tool call."""
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]

        # Execute the tool (simplified)
        if tool_name == "search_tool":
            result = f"Found 10 results for: {tool_args['query']}"
        elif tool_name == "calculator":
            result = "4"
        else:
            result = f"Executed {tool_name}"

        # Create tool message
        tool_message = ToolMessage(content=result, tool_call_id=tool_call["id"])
        state.messages.append(tool_message)

        return state

    # Structured output node for Pydantic models
    def structured_output_node(
        state: AgentState,
        tool_call: dict[str, Any],
    ) -> AgentState:
        """Handle structured output validation."""
        # This would validate against Pydantic schema
        result = f"Validated structured output: {tool_call['name']}"

        tool_message = ToolMessage(content=result, tool_call_id=tool_call["id"])
        state.messages.append(tool_message)

        return state

    # Add nodes to graph
    graph.add_node("agent", agent_node)
    graph.add_node("validate", routing_validator)
    graph.add_node("tool_executor", tool_executor)
    graph.add_node("structured_output", structured_output_node)

    # Add edges
    graph.add_edge("agent", "validate")

    # The validation node returns Send objects that create parallel branches
    # Each Send routes a tool call to its appropriate handler

    # After tools execute, they converge back
    graph.add_edge("tool_executor", END)
    graph.add_edge("structured_output", END)

    # Compile the graph
    return graph.compile()


def demonstrate_routing():
    """Demonstrate how routing validation works."""

    # Create initial state
    state = AgentState()

    # Set up tools and routes
    state.tools = [
        {"name": "search_tool", "type": "tool"},
        {"name": "calculator", "type": "tool"},
        {"name": "create_document", "type": "pydantic_model"},
    ]

    state.tool_routes = {
        "search_tool": "langchain_tool",
        "calculator": "function",
        "create_document": "pydantic_model",
    }

    # Simulate what the validation node would do
    print("🔍 Validation Node Routing Example")
    print("=" * 50)

    # Create AI message with tool calls
    ai_message = AIMessage(
        content="Processing your request...",
        tool_calls=[
            {"id": "1", "name": "search_tool", "args": {"query": "test"}},
            {"id": "2", "name": "calculator", "args": {"expression": "2+2"}},
            {"id": "3", "name": "create_document", "args": {"title": "Doc"}},
            {"id": "4", "name": "unknown_tool", "args": {}},  # This will fail
        ],
    )
    state.messages.append(ai_message)

    print("\n📋 Tool Calls:")
    for tc in ai_message.tool_calls:
        print(f"  - {tc['name']} (id: {tc['id']})")

    print("\n🔀 Tool Routes:")
    for name, route in state.tool_routes.items():
        print(f"  - {name}: {route}")

    # Simulate validation and routing
    print("\n✅ Validation Results:")
    sends = []

    for tool_call in ai_message.tool_calls:
        tool_name = tool_call["name"]

        if tool_name in state.tool_routes:
            route = state.tool_routes[tool_name]

            # Map route to node
            target_node = "structured_output" if route == "pydantic_model" else "tool_executor"

            print(f"  ✓ {tool_name} → {target_node} (route: {route})")
            sends.append(Send(target_node, tool_call))
        else:
            print(f"  ✗ {tool_name} → FAILED (tool not found)")

    print(f"\n📤 Created {len(sends)} Send objects for parallel execution")

    # Show what would happen
    print("\n🚀 Execution Flow:")
    print("  1. Agent generates tool calls")
    print("  2. Validation node validates each tool")
    print("  3. Creates Send objects for valid tools:")
    for send in sends:
        print(f"     - Send('{send.node}', tool_call)")
    print("  4. Each Send creates a parallel branch")
    print("  5. Tools execute in parallel")
    print("  6. Results converge back to state")


if __name__ == "__main__":
    demonstrate_routing()

    print("\n\n💡 Key Concepts:")
    print("- Validation node returns List[Send] for parallel routing")
    print("- Each tool call is validated against available tools")
    print("- Tool routes determine which node handles execution")
    print("- Failed validations can route to agent or skip")
    print("- Send objects enable parallel tool execution")
