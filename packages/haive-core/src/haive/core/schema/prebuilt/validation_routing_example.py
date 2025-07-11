"""Example of LangGraph validation nodes with Send branching for tool routing.

This example demonstrates:
1. How validation nodes return routing decisions using Send objects
2. How Send objects are created from validation results
3. How tool routes map to destination nodes
4. Examples of splitting tool calls based on validation
"""

from typing import Any, Dict, List, Union

from langchain_core.messages import AIMessage, ToolMessage
from langgraph.graph import END, StateGraph
from langgraph.types import Send
from pydantic import BaseModel, Field

from haive.core.schema.prebuilt.tool_state_with_validation import EnhancedToolState
from haive.core.schema.prebuilt.tools.validation_state import (
    RouteRecommendation,
    ValidationStateManager,
    ValidationStatus,
)


class ValidationExample(BaseModel):
    """Example state that extends EnhancedToolState for validation routing."""

    # Inherit all the validation routing capabilities
    class Config:
        arbitrary_types_allowed = True

    # Additional fields for example
    current_step: str = Field(default="start", description="Current processing step")
    error_count: int = Field(default=0, description="Number of errors encountered")


def validation_node(state: EnhancedToolState) -> Union[str, List[Send]]:
    """Validation node that routes tool calls based on validation results.

    This node demonstrates:
    1. Validating tool calls from the last AI message
    2. Creating Send objects for valid tools based on their routes
    3. Handling different validation statuses (valid, invalid, error)
    4. Routing to different nodes based on tool_routes from state/engine

    Returns:
        - List[Send]: For routing valid tool calls to appropriate nodes
        - "agent": To return to agent for clarification
        - END: To end processing if no valid tools
    """
    # Get tool calls from the last AI message
    last_ai_message = state.messages.last_ai_message
    if not last_ai_message or not hasattr(last_ai_message, "tool_calls"):
        return END

    tool_calls = last_ai_message.tool_calls
    if not tool_calls:
        return END

    # Create validation state manager
    validation_state = ValidationStateManager.create_routing_state()

    # Validate each tool call
    for tool_call in tool_calls:
        tool_name = tool_call.get("name")
        tool_args = tool_call.get("args", {})
        tool_call_id = tool_call.get("id")

        # Get the tool route from state (this is how we know where to send it)
        tool_route = state.tool_routes.get(tool_name, "unknown")

        # Perform validation (example logic)
        if tool_name not in state.tool_routes:
            # Tool doesn't exist
            result = ValidationStateManager.create_validation_result(
                tool_call_id=tool_call_id,
                tool_name=tool_name,
                status=ValidationStatus.INVALID,
                route_recommendation=RouteRecommendation.SKIP,
                errors=[f"Unknown tool: {tool_name}"],
            )
        elif not tool_args and tool_route == "pydantic_model":
            # Pydantic models need arguments
            result = ValidationStateManager.create_validation_result(
                tool_call_id=tool_call_id,
                tool_name=tool_name,
                status=ValidationStatus.INVALID,
                route_recommendation=RouteRecommendation.AGENT,
                errors=["Pydantic model requires arguments"],
                corrected_args={"default_field": "default_value"},
            )
        elif tool_route == "langchain_tool" and "dangerous" in tool_name.lower():
            # Example: block dangerous tools
            result = ValidationStateManager.create_validation_result(
                tool_call_id=tool_call_id,
                tool_name=tool_name,
                status=ValidationStatus.ERROR,
                route_recommendation=RouteRecommendation.END,
                errors=["Tool blocked by security policy"],
            )
        else:
            # Valid tool call - determine target node based on route
            target_node = _get_target_node_for_route(tool_route)

            result = ValidationStateManager.create_validation_result(
                tool_call_id=tool_call_id,
                tool_name=tool_name,
                status=ValidationStatus.VALID,
                route_recommendation=RouteRecommendation.EXECUTE,
                target_node=target_node,
                engine_name=state.engines.get(tool_route, {}).get("name"),
                priority=state.tool_priorities.get(tool_name, 0),
            )

        validation_state.add_validation_result(result)

    # Apply validation results to state
    state.apply_validation_results(validation_state)

    # Now create Send objects based on validation results
    sends = []

    # Group valid tool calls by their target nodes
    tools_by_node = {}
    for result in validation_state.get_valid_tool_calls():
        target = result.target_node or "tools"  # Default to "tools" node
        if target not in tools_by_node:
            tools_by_node[target] = []

        # Find the original tool call
        tool_call = next(
            (tc for tc in tool_calls if tc.get("id") == result.tool_call_id), None
        )
        if tool_call:
            # Add validation metadata to the tool call
            enhanced_call = tool_call.copy()
            enhanced_call["validation"] = {
                "status": result.status.value,
                "priority": result.priority,
                "engine": result.engine_name,
            }
            tools_by_node[target].append(enhanced_call)

    # Create Send objects for each target node
    for node_name, node_tools in tools_by_node.items():
        for tool_call in node_tools:
            # Each Send creates a separate execution branch
            sends.append(Send(node_name, tool_call))

    # Handle routing based on overall validation state
    if sends:
        # We have valid tools to execute
        return sends
    elif validation_state.should_return_to_agent():
        # Need agent clarification
        return "agent"
    else:
        # No valid tools, end processing
        return END


def _get_target_node_for_route(tool_route: str) -> str:
    """Map tool routes to target node names.

    This demonstrates how different tool types can be routed to different nodes.
    """
    route_to_node = {
        "langchain_tool": "langchain_tools",
        "pydantic_model": "pydantic_tools",
        "function": "function_tools",
        "retriever": "retriever_tools",
        "agent": "sub_agents",
        "unknown": "generic_tools",
    }
    return route_to_node.get(tool_route, "tools")


def langchain_tools_node(tool_call: Dict[str, Any]) -> Dict[str, Any]:
    """Execute LangChain tools."""
    # This node receives individual tool calls via Send
    tool_name = tool_call.get("name")
    tool_args = tool_call.get("args", {})
    validation_info = tool_call.get("validation", {})

    print(f"Executing LangChain tool: {tool_name}")
    print(f"  Priority: {validation_info.get('priority', 0)}")
    print(f"  Engine: {validation_info.get('engine', 'default')}")

    # Execute the tool and return result
    result = f"Result from {tool_name}"

    return {
        "messages": [
            ToolMessage(
                content=result,
                tool_call_id=tool_call.get("id"),
                name=tool_name,
            )
        ]
    }


def pydantic_tools_node(tool_call: Dict[str, Any]) -> Dict[str, Any]:
    """Execute Pydantic model tools."""
    tool_name = tool_call.get("name")
    tool_args = tool_call.get("args", {})

    print(f"Executing Pydantic tool: {tool_name} with args: {tool_args}")

    # Validate args against Pydantic model and execute
    result = f"Pydantic result for {tool_name}"

    return {
        "messages": [
            ToolMessage(
                content=result,
                tool_call_id=tool_call.get("id"),
                name=tool_name,
            )
        ]
    }


def agent_node(state: EnhancedToolState) -> Dict[str, Any]:
    """Agent node that can make tool calls."""
    # Get validation feedback if any
    if state.validation_state.invalid_tool_calls:
        print("Agent received validation feedback:")
        for result in state.validation_state.get_invalid_tool_calls():
            print(f"  - {result.tool_name}: {', '.join(result.errors)}")

    # Make new tool calls or provide response
    return {
        "messages": [
            AIMessage(
                content="Making tool calls...",
                tool_calls=[
                    {"id": "1", "name": "search_tool", "args": {"query": "test"}},
                    {"id": "2", "name": "data_model", "args": {"field": "value"}},
                ],
            )
        ]
    }


def build_validation_graph() -> StateGraph:
    """Build a graph demonstrating validation routing with Send."""
    graph = StateGraph(EnhancedToolState)

    # Add nodes
    graph.add_node("agent", agent_node)
    graph.add_node("validation", validation_node)
    graph.add_node("langchain_tools", langchain_tools_node)
    graph.add_node("pydantic_tools", pydantic_tools_node)

    # Add edges
    graph.set_entry_point("agent")

    # From agent, go to validation when there are tool calls
    graph.add_conditional_edges(
        "agent",
        lambda state: "validation" if state.messages.has_tool_calls else END,
    )

    # Validation node returns Send objects or routing decisions
    # The Send objects automatically create parallel branches
    graph.add_edge("validation", END)  # Default edge

    # Tool nodes return to agent
    graph.add_edge("langchain_tools", "agent")
    graph.add_edge("pydantic_tools", "agent")

    return graph.compile()


# Example of using the validation routing pattern
if __name__ == "__main__":
    # Create initial state with tools configured
    initial_state = EnhancedToolState()

    # Add some example tools with routes
    initial_state.add_tool_enhanced(
        tool={"name": "search_tool", "description": "Search the web"},
        route="langchain_tool",
        category="retrieval",
        priority=10,
    )

    initial_state.add_tool_enhanced(
        tool={"name": "data_model", "description": "Data validation model"},
        route="pydantic_model",
        category="validation",
        priority=5,
    )

    initial_state.add_tool_enhanced(
        tool={"name": "dangerous_tool", "description": "A dangerous tool"},
        route="langchain_tool",
        category="restricted",
        priority=0,
    )

    # Build and run the graph
    graph = build_validation_graph()

    # The validation node will:
    # 1. Check tool calls from AI message
    # 2. Validate each tool based on routes and rules
    # 3. Create Send objects to route valid tools to appropriate nodes
    # 4. Return routing decisions for invalid tools
