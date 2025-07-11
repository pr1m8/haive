"""Graph nodes for ReWOO agent execution.

This shows how ReWOO models and state work together in actual agent nodes.
"""

from typing import Any

from haive.agents.planning.rewoo.models import EvidenceStatus
from haive.agents.planning.rewoo.state import ReWOOState


async def collect_evidence_node(state: ReWOOState) -> dict[str, Any]:
    """Node that collects evidence using tools.

    This is where models, state, and tools come together:
    1. Get ready evidence from state
    2. Use tool from state to collect it
    3. Update evidence in state
    """
    # Get evidence that's ready to collect
    ready_evidence = state.ready_evidence

    if not ready_evidence:
        return {"messages": ["No evidence ready to collect"]}

    # Collect first ready evidence
    evidence = ready_evidence[0]

    # Mark as collecting
    state.update_evidence(evidence.id, status=EvidenceStatus.COLLECTING)

    # Get the tool from state (inherited from ToolState)
    tool = state.get_tool_by_name(evidence.source)
    if not tool:
        state.update_evidence(
            evidence.id,
            status=EvidenceStatus.FAILED,
            error=f"Tool {evidence.source} not found",
        )
        return {"messages": [f"Failed to find tool {evidence.source}"]}

    # Resolve evidence references in the collection method
    # This replaces #E1 with actual evidence content
    resolved_method = evidence.resolve_references(state.evidence_map)

    try:
        # Parse the method and args (simplified)
        # In real implementation, would parse "search(query='population of Tokyo')"
        if evidence.source == "search":
            # Extract query from resolved method
            query = resolved_method.split("query='")[1].split("'")[0]
            result = await tool.ainvoke({"query": query})
        else:
            # Generic tool execution
            result = await tool.ainvoke({})

        # Update evidence with result
        state.update_evidence(
            evidence.id, status=EvidenceStatus.COLLECTED, content=result
        )

        # Also track in tool_results
        state.add_tool_result(evidence.source, result)

        return {
            "messages": [f"Collected evidence {evidence.id}: {evidence.description}"]
        }

    except Exception as e:
        state.update_evidence(evidence.id, status=EvidenceStatus.FAILED, error=str(e))
        return {"messages": [f"Failed to collect {evidence.id}: {e!s}"]}


async def execute_tool_call_node(state: ReWOOState) -> dict[str, Any]:
    """Node that executes a specific tool call.

    Shows how ToolCall model integrates with state.
    """
    if not state.active_tool_calls:
        return {"messages": ["No active tool calls"]}

    tool_call = state.active_tool_calls[0]

    # Get tool from state
    tool = state.get_tool_by_name(tool_call.tool_name)
    if not tool:
        return {"messages": [f"Tool {tool_call.tool_name} not found"]}

    # Resolve arguments (replace #E1 references with actual evidence)
    resolved_args = tool_call.resolve_arguments(state.evidence_map)

    try:
        # Execute tool
        if tool_call.is_llm_call:
            # Use LLM for reasoning
            result = "LLM reasoning based on evidence"
        else:
            # Execute actual tool
            result = await tool.ainvoke(resolved_args)

        # Validate output if schema provided
        if tool_call.expected_output_schema and not tool_call.validate_output(result):
            return {"messages": ["Output validation failed"]}

        # Store result
        state.add_tool_result(tool_call.tool_name, result)

        # Remove from active calls
        state.active_tool_calls.pop(0)

        return {"messages": [f"Executed {tool_call.tool_name}"]}

    except Exception as e:
        return {"messages": [f"Tool execution failed: {e!s}"]}


async def check_evidence_complete_node(state: ReWOOState) -> str:
    """Conditional node to check if evidence collection is complete."""
    if state.is_evidence_complete:
        return "reason"  # Go to reasoning
    return "collect"  # Continue collecting


async def reason_with_evidence_node(state: ReWOOState) -> dict[str, Any]:
    """Final reasoning node using all collected evidence."""
    # Get evidence context
    state.get_evidence_context()

    # Create reasoning prompt

    # In real implementation, would use LLM here
    reasoning_result = f"Based on evidence, conclusion for: {state.objective}"

    return {"messages": [reasoning_result], "final_reasoning": reasoning_result}


# Example of how these work together in a graph
def build_rewoo_graph():
    """Build a ReWOO agent graph showing the integration."""
    from haive.core.graph import END, START, BaseGraph

    graph = BaseGraph()

    # Add nodes
    graph.add_node("collect_evidence", collect_evidence_node)
    graph.add_node("check_complete", check_evidence_complete_node)
    graph.add_node("reason", reason_with_evidence_node)

    # Connect nodes
    graph.add_edge(START, "collect_evidence")
    graph.add_edge("collect_evidence", "check_complete")

    # Conditional routing
    graph.add_conditional_edges(
        "check_complete",
        check_evidence_complete_node,
        {"collect": "collect_evidence", "reason": "reason"},
    )

    graph.add_edge("reason", END)

    return graph.compile()
