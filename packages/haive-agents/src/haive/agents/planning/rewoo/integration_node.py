"""Integration node for ReWOO with existing tool infrastructure.

This shows how ReWOO's structured output integrates with the tool node system.
"""

from typing import Any, Dict, List, Optional

from haive.core.graph.node.tool_node_config_v2 import ToolNodeConfig
from langchain_core.messages import AIMessage, BaseMessage, ToolMessage
from langgraph.types import Command
from pydantic import Field

from haive.agents.planning.rewoo.models import EvidenceStatus, ToolCall
from haive.agents.planning.rewoo.state import ReWOOState


async def rewoo_to_tool_calls_node(state: ReWOOState) -> dict[str, Any]:
    """Convert ReWOO plan into AIMessage with tool calls.

    This is the key integration point:
    1. ReWOO agent generates structured plan (ReWOOPlan)
    2. This node converts it to tool call messages
    3. Standard tool node executes the calls
    4. Evidence collection node updates ReWOO state
    """
    # Get ready evidence
    ready_evidence = state.ready_evidence

    if not ready_evidence:
        return {"messages": ["No evidence ready to collect"]}

    # Take first ready evidence
    evidence = ready_evidence[0]

    # Find the step that produces this evidence
    step = None
    for s in state.plan.steps:
        if hasattr(s, "evidence") and s.evidence and s.evidence.id == evidence.id:
            step = s
            break

    if not step or not step.tool_call:
        return {"messages": [f"No tool call found for evidence {evidence.id}"]}

    # Resolve evidence references in tool call
    resolved_args = step.tool_call.resolve_arguments(state.evidence_map)

    # Create proper tool call format for LangChain
    tool_call_data = {
        "name": step.tool_call.tool_name,
        "args": resolved_args,
        "id": f"call_{evidence.id}_{step.tool_call.tool_name}",
    }

    # Create AIMessage with tool calls (what LLM would normally produce)
    ai_message = AIMessage(
        content=f"I need to collect evidence {evidence.id}: {evidence.description}",
        tool_calls=[tool_call_data],
    )

    # Mark evidence as collecting
    state.update_evidence(evidence.id, status=EvidenceStatus.COLLECTING)

    # Add to messages (this will be processed by tool node)
    current_messages = state.messages or []
    updated_messages = [*current_messages, ai_message]

    return {
        "messages": updated_messages,
        "current_evidence_id": evidence.id,  # Track which evidence we're collecting
    }


async def tool_results_to_evidence_node(state: ReWOOState) -> dict[str, Any]:
    """Process tool results back into evidence.

    This runs after the tool node executes:
    1. Tool node adds ToolMessage to messages
    2. This node extracts the result
    3. Updates the evidence in ReWOO state
    """
    # Get the last few messages
    messages = state.messages or []
    if len(messages) < 2:
        return {"messages": ["No tool results to process"]}

    # Get the current evidence we're collecting
    current_evidence_id = getattr(state, "current_evidence_id", None)
    if not current_evidence_id:
        return {"messages": ["No current evidence to update"]}

    # Find the latest ToolMessage
    tool_message = None
    for msg in reversed(messages):
        if isinstance(msg, ToolMessage):
            tool_message = msg
            break

    if not tool_message:
        # Tool execution failed
        state.update_evidence(
            current_evidence_id,
            status=EvidenceStatus.FAILED,
            error="No tool result found",
        )
        return {"messages": ["Tool execution failed - no result"]}

    try:
        # Update evidence with tool result
        state.update_evidence(
            current_evidence_id,
            status=EvidenceStatus.COLLECTED,
            content=tool_message.content,
        )

        # Also track in tool_results
        state.add_tool_result(tool_message.name or "unknown", tool_message.content)

        return {
            "messages": [
                f"Collected evidence {current_evidence_id}: {tool_message.content[:100]}..."
            ]
        }

    except Exception as e:
        state.update_evidence(
            current_evidence_id, status=EvidenceStatus.FAILED, error=str(e)
        )
        return {"messages": [f"Failed to update evidence: {e!s}"]}


def create_rewoo_tool_node(
    engine_name: str = "aug_llm", name: str = "rewoo_tools"
) -> ToolNodeConfig:
    """Create a tool node configured for ReWOO.

    This uses the standard ToolNodeConfig but configured
    for ReWOO's needs.
    """
    return ToolNodeConfig(
        name=name,
        engine_name=engine_name,
        # Allow all tool types
        allowed_routes=["langchain_tool", "function", "pydantic_model"],
        # Don't require tool calls (we create them programmatically)
        require_tool_calls=True,
        # Create error messages for failed tools
        create_error_messages=True,
        # Use standard messages field
        messages_field="messages",
        tool_routes_field="tool_routes",
    )


# Example of how to integrate this in a ReWOO agent graph
def build_rewoo_integration_graph():
    """Build ReWOO graph that integrates with existing tool infrastructure."""
    from haive.core.graph import END, START, BaseGraph

    graph = BaseGraph()

    # Planning phase (creates ReWOOPlan)
    graph.add_node("plan", planning_node)  # Creates structured plan

    # Tool execution phase (integrates with existing tool system)
    graph.add_node("prepare_tools", rewoo_to_tool_calls_node)  # Convert to tool calls

    # Standard tool node (existing infrastructure)
    tool_node = create_rewoo_tool_node()
    graph.add_node("execute_tools", tool_node)  # Execute tools

    graph.add_node("process_results", tool_results_to_evidence_node)  # Back to evidence

    # Routing
    graph.add_node("check_complete", check_evidence_complete_node)

    # Final reasoning
    graph.add_node("reason", final_reasoning_node)

    # Flow
    graph.add_edge(START, "plan")
    graph.add_edge("plan", "prepare_tools")
    graph.add_edge("prepare_tools", "execute_tools")
    graph.add_edge("execute_tools", "process_results")
    graph.add_edge("process_results", "check_complete")

    # Conditional routing
    graph.add_conditional_edges(
        "check_complete",
        lambda state: "reason" if state.is_evidence_complete else "prepare_tools",
        {"prepare_tools": "prepare_tools", "reason": "reason"},
    )

    graph.add_edge("reason", END)

    return graph.compile()


# Placeholder nodes (would be actual implementations)
async def planning_node(state: ReWOOState) -> dict[str, Any]:
    """Create ReWOO plan (placeholder)."""
    return {"messages": ["Plan created"]}


async def check_evidence_complete_node(state: ReWOOState) -> str:
    """Check completion (placeholder)."""
    return "reason" if state.is_evidence_complete else "prepare_tools"


async def final_reasoning_node(state: ReWOOState) -> dict[str, Any]:
    """Final reasoning (placeholder)."""
    context = state.get_evidence_context()
    return {"messages": [f"Final answer based on: {context}"]}


# Key insight: The integration flow is:
# 1. ReWOO Plan (structured) -> Tool Call Messages -> Tool Node -> Tool Results -> Evidence Update
# 2. This bridges structured planning with existing tool execution infrastructure
# 3. Uses try/except in tool node execution (built into ToolNodeConfig)
# 4. ReWOO state tracks evidence, tool node handles execution
