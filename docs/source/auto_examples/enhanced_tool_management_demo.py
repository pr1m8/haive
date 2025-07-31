"""Demo of enhanced tool management with validation routing."""

from typing import Any, Dict, List

from pydantic import BaseModel, Field

# Simulated imports (these would be the real imports in practice)
from tests.enhanced_tool_management.test_validation_state_standalone import (
    RouteRecommendation, ToolValidationResult, ValidationRoutingState,
    ValidationStatus)


class SearchTool(BaseModel):
    """Example search tool schema."""

    query: str = Field(..., description="Search query")
    limit: int = Field(default=10, description="Result limit", ge=1, le=100)
    category: str = Field(default="general", description="Search category")


class CreateTool(BaseModel):
    """Example creation tool schema."""

    title: str = Field(..., description="Title for creation")
    content: str = Field(..., description="Content to create")
    tags: list[str] = Field(default_factory=list, description="Tags")


def simulate_tool_call_validation():
    """Simulate validating tool calls and generating routing state."""
    print("🔧 Enhanced Tool Management Demo")
    print("=" * 50)

    # Create validation routing state
    routing_state = ValidationRoutingState()

    # Simulate various tool call validation scenarios
    print("\n📝 Scenario 1: Valid tool call")
    valid_result = ToolValidationResult(
        tool_call_id="call_001",
        tool_name="search_tool",
        status=ValidationStatus.VALID,
        route_recommendation=RouteRecommendation.EXECUTE,
        target_node="tool_node",
        engine_name="search_engine",
    )
    routing_state.add_validation_result(valid_result)
    print(f"✅ Added valid tool: {valid_result.tool_name}")

    print("\n📝 Scenario 2: Invalid tool call with corrections")
    invalid_result = ToolValidationResult(
        tool_call_id="call_002",
        tool_name="create_tool",
        status=ValidationStatus.INVALID,
        route_recommendation=RouteRecommendation.RETRY,
        errors=["Missing required field: title"],
        warnings=["Large content may be truncated"],
        corrected_args={"title": "Auto-generated Title", "content": "Sample content"},
        target_node="tool_node",
        engine_name="creation_engine",
    )
    routing_state.add_validation_result(invalid_result)
    print(f"⚠️  Added invalid tool with corrections: {invalid_result.tool_name}")

    print("\n📝 Scenario 3: Tool call with error")
    error_result = ToolValidationResult(
        tool_call_id="call_003",
        tool_name="unknown_tool",
        status=ValidationStatus.ERROR,
        route_recommendation=RouteRecommendation.AGENT,
        errors=["Tool 'unknown_tool' not found in registry"],
        target_node="agent_node",
    )
    routing_state.add_validation_result(error_result)
    print(f"❌ Added error tool: {error_result.tool_name}")

    return routing_state


def demonstrate_routing_decisions(routing_state: ValidationRoutingState):
    """Demonstrate routing decisions based on validation results."""
    print("\n🔀 Routing Decisions")
    print("=" * 30)

    # Get routing decision data
    decision_data = routing_state.get_routing_decision()

    print("📊 Validation Summary:"y:")
    print(f"   • Total tools: {decision_data['total_count']}")
    print(f"   • Valid: {decision_data['valid_count']}")
    print(f"   • Invalid: {decision_data['invalid_count']}")
    print(f"   • Errors: {decision_data['error_count']}")
    print(f"   • Has corrections: {decision_data['has_corrections']}")

    print(f"\n🎯 Next Action: {decision_data['next_action']}")
    print(f"🎯 Target Nodes: {decision_data['target_nodes']}")

    # Demonstrate conditional branching logic
    print("\n🔀 Conditional Branching:"g:")
    print(
        f"   • Should continue execution: {routing_state.should_continue_execution()}"
    )
    print(f"   • Should return to agent: {routing_state.should_return_to_agent()}")
    print(f"   • Should end processing: {routing_state.should_end_processing()}")


def demonstrate_tool_message_updates(routing_state: ValidationRoutingState):
    """Demonstrate tool message updates."""
    print("\n📝 Tool Message Updates")
    print("=" * 30)

    for tool_call_id, updates in routing_state.tool_message_updates.items():
        print(f"\n🔧 Tool Call ID: {tool_call_id}")
        print(f"   Status: {updates.get('validation_status', 'unknown')}")

        if updates.get("validation_errors"):
            print(f"   Errors: {updates['validation_errors']}")

        if updates.get("validation_warnings"):
            print(f"   Warnings: {updates['validation_warnings']}")

        if updates.get("corrected_args"):
            print(f"   Corrections: {updates['corrected_args']}")

        print(f"   Route: {updates.get('route_recommendation', 'unknown')}")
        print(f"   Target: {updates.get('target_node', 'unknown')}")


def simulate_enhanced_validation_node():
    """Simulate the enhanced validation node in action."""
    print("\n🏗️  Enhanced Validation Node Simulation")
    print("=" * 45)

    # Simulate incoming state with tool calls
    incoming_state = {
        "messages": [
            # Simulated AI message with tool calls
            {
                "type": "ai",
                "content": "I'll help you search and create content.",
                "tool_calls": [
                    {
                        "id": "call_001",
                        "name": "search_tool",
                        "args": {"query": "python tutorial", "limit": 5},
                    },
                    {
                        "id": "call_002",
                        "name": "create_tool",
                        "args": {"content": "Sample content"},  # Missing title
                    },
                    {
                        "id": "call_003",
                        "name": "unknown_tool",
                        "args": {"param": "value"},
                    },
                ],
            }
        ],
        "tools": ["search_tool", "create_tool"],  # unknown_tool not available
        "tool_routes": {
            "search_tool": "langchain_tool",
            "create_tool": "pydantic_model",
        },
    }

    print("📥 Incoming state:")
    print(f"   • Tool calls: {len(incoming_state['messages'][0]['tool_calls'])}")
    print(f"   • Available tools: {incoming_state['tools']}")

    # Validate and create routing state
    routing_state = simulate_tool_call_validation()

    # Simulate updated state
    updated_state = incoming_state.copy()
    updated_state["validation_state"] = routing_state
    updated_state["routing_data"] = {
        "should_continue": routing_state.should_continue_execution(),
        "should_return_to_agent": routing_state.should_return_to_agent(),
        "should_end": routing_state.should_end_processing(),
        "target_nodes": list(routing_state.target_nodes),
        "next_action": routing_state.next_action.value,
    }

    print("\n📤 Updated state:")
    print(f"   • Validation complete: {routing_state.total_tools} tools processed")
    print(f"   • Routing decision: {updated_state['routing_data']['next_action']}")
    print(
        f"   • Continue execution: {updated_state['routing_data']['should_continue']}"
    )

    return updated_state


def demonstrate_conditional_branching(state: dict[str, Any]):
    """Demonstrate conditional branching logic."""
    print("\n🌊 Conditional Branching Logic")
    print("=" * 35)

    routing_data = state.get("routing_data", {})

    # Simulate different branching scenarios
    print("🔀 Branch Decision Tree:")

    if routing_data.get("should_return_to_agent"):
        print("   → BRANCH: Return to agent for clarification")
        print("   → REASON: Errors found or uncorrectable invalid tools")

    elif routing_data.get("should_continue"):
        print("   → BRANCH: Continue to tool execution")
        print("   → REASON: Valid tools found, ready for execution")

        # Show which nodes to route to
        target_nodes = routing_data.get("target_nodes", [])
        if target_nodes:
            print(f"   → TARGET NODES: {', '.join(target_nodes)}")

    elif routing_data.get("should_end"):
        print("   → BRANCH: End processing")
        print("   → REASON: No tool calls or processing complete")

    else:
        print("   → BRANCH: Default handling")
        print("   → REASON: Unexpected state")

    # Show available branch conditions for complex routing
    print("\n📋 Available Branch Conditions:"s:")
    for key, value in routing_data.items():
        print(f"   • {key}: {value}")


def main():
    """Run the enhanced tool management demo."""
    print("🚀 Starting Enhanced Tool Management Demo\n")

    # Step 1: Simulate validation
    routing_state = simulate_tool_call_validation()

    # Step 2: Show routing decisions
    demonstrate_routing_decisions(routing_state)

    # Step 3: Show tool message updates
    demonstrate_tool_message_updates(routing_state)

    # Step 4: Simulate the enhanced validation node
    updated_state = simulate_enhanced_validation_node()

    # Step 5: Demonstrate conditional branching
    demonstrate_conditional_branching(updated_state)

    print("\n✅ Demo completed successfully!")
    print("\n💡 Key Benefits:")
    print("   • Tool messages are updated with validation status")
    print("   • Routing state provides clear branching decisions")
    print("   • Automatic correction attempts for invalid tools")
    print("   • Error handling with fallback to agent")
    print("   • Rich metadata for debugging and monitoring")


if __name__ == "__main__":
    main()
