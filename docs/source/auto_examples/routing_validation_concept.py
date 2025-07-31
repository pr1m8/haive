"""Conceptual demonstration of routing validation with Send branching."""


def demonstrate_routing_validation_concept():
    """Show how routing validation works conceptually."""

    print("🔍 Routing Validation Node Concept")
    print("=" * 50)

    # Example state with tool calls
    tool_calls = [
        {"id": "call_001", "name": "search_tool", "args": {"query": "python"}},
        {"id": "call_002", "name": "calculator", "args": {"a": 5, "b": 3}},
        {"id": "call_003", "name": "DocumentSchema", "args": {"title": "Report"}},
        {"id": "call_004", "name": "unknown_tool", "args": {}},
    ]

    # Tool routes from engine/state
    tool_routes = {
        "search_tool": "langchain_tool",
        "calculator": "function",
        "DocumentSchema": "pydantic_model",
    }

    # Available tools
    available_tools = ["search_tool", "calculator", "DocumentSchema"]

    print("\n📋 Input Tool Calls:")
    for tc in tool_calls:
        print(f"  - {tc['name']} (id: {tc['id']})")

    print("\n🗺️ Tool Routes (from engine):")
    for name, route in tool_routes.items():
        print(f"  - {name} → {route}")

    print("\n✅ Validation Process:")

    # Simulate validation
    validation_results = []
    sends = []

    for tool_call in tool_calls:
        tool_name = tool_call["name"]
        tool_id = tool_call["id"]

        # Validate tool exists
        if tool_name not in available_tools:
            print(f"  ❌ {tool_name}: Tool not found")
            validation_results.append(
                {"tool_id": tool_id, "status": "error", "reason": "Tool not found"}
            )
            continue

        # Get route and target node
        route = tool_routes.get(tool_name, "unknown")

        # Map route to node
        route_to_node = {
            "langchain_tool": "tool_executor",
            "function": "tool_executor",
            "pydantic_model": "structured_output",
            "unknown": "tool_executor",
        }

        target_node = route_to_node[route]

        print(f"  ✅ {tool_name}: Valid → {target_node} (route: {route})")

        validation_results.append(
            {"tool_id": tool_id, "status": "valid", "target_node": target_node}
        )

        # Create Send object (conceptually)
        sends.append(
            f"Send('{target_node}', {{'id': '{tool_id}', 'name': '{tool_name}'}})"
        )

    print("\n📤 Routing Decision:"n:")

    if sends:
        print(f"  Return: List[Send] with {len(sends)} branches")
        for send in sends:
            print(f"    - {send}")
    else:
        print("  Return: 'agent' (all validations failed)")

    print("\n🌊 Execution Flow:")
    print("  1. State has tool_calls from AI message")
    print("  2. Validation node gets tool_routes from engine/state")
    print("  3. Each tool is validated:")
    print("     - Check if tool exists")
    print("     - Validate arguments (if schema available)")
    print("     - Determine target node from route")
    print("  4. Create Send objects for valid tools")
    print("  5. Return List[Send] for parallel execution")

    print("\n💡 Key Points:")
    print("- Validation node is a router, not an executor")
    print("- Uses tool_routes to determine destinations")
    print("- Returns Send objects for parallel branching")
    print("- Failed validations can route to 'agent' node")
    print("- Each Send creates independent execution branch")


if __name__ == "__main__":
    demonstrate_routing_validation_concept()
