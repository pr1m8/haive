"""Example showing how ReWOO models, state, and nodes work together.

This demonstrates the integration without reimplementing the existing agent.
"""

from typing import Any

from haive.core.graph import END, START, BaseGraph
from haive.core.tools import tool

from haive.agents.planning.rewoo.models import (
    EvidenceStatus,
    ReWOOPlan,
)
from haive.agents.planning.rewoo.state import ReWOOState


# Example tools
@tool
def search_tool(query: str) -> str:
    """Search for information."""
    return f"Results for: {query}"


@tool
def analyze_tool(data: str) -> str:
    """Analyze data."""
    return f"Analysis of: {data}"


# Example nodes showing the integration
async def planning_node(state: ReWOOState) -> dict[str, Any]:
    """Create ReWOO plan with evidence dependencies.

    This shows how models work with state.
    """
    # Create plan
    plan = ReWOOPlan(name="example_plan", objective=state.objective)

    # Add evidence steps
    plan.add_rewoo_step(
        name="search_step",
        evidence_id="#E1",
        evidence_description="Initial search results",
        tool_name="search_tool",
        tool_args={"query": state.objective},
    )

    plan.add_rewoo_step(
        name="analyze_step",
        evidence_id="#E2",
        evidence_description="Analysis of search results",
        tool_name="analyze_tool",
        tool_args={"data": "#E1"},  # References E1
        depends_on=["#E1"],
    )

    # Update state
    state.plan = plan
    state.evidence_map = plan.evidence_map.copy()

    return {"messages": [f"Created plan with {len(plan.steps)} steps"]}


async def evidence_collection_node(state: ReWOOState) -> dict[str, Any]:
    """Collect evidence using tools from state.

    This shows how state provides tools and tracks evidence.
    """
    # Get ready evidence (respects dependencies)
    ready = state.ready_evidence

    if not ready:
        return {"messages": ["No evidence ready"]}

    evidence = ready[0]

    # Get tool from state (inherited from ToolState)
    tool = state.get_tool_by_name(evidence.source)
    if not tool:
        state.update_evidence(
            evidence.id, status=EvidenceStatus.FAILED, error="Tool not found"
        )
        return {"messages": [f"Tool {evidence.source} not found"]}

    # If evidence has dependencies, resolve them
    if evidence.depends_on:
        # Get the tool call from the step
        step = next(
            (
                s
                for s in state.plan.steps
                if s.evidence and s.evidence.id == evidence.id
            ),
            None,
        )

        if step and step.tool_call:
            # Resolve arguments (replace #E1 with actual content)
            resolved_args = step.tool_call.resolve_arguments(state.evidence_map)

            # Execute tool with resolved args
            result = await tool.ainvoke(resolved_args)
        else:
            # Direct execution
            result = await tool.ainvoke({"query": state.objective})
    else:
        # No dependencies, execute directly
        result = await tool.ainvoke({"query": state.objective})

    # Update evidence
    state.update_evidence(evidence.id, status=EvidenceStatus.COLLECTED, content=result)

    return {"messages": [f"Collected {evidence.id}: {result}"]}


async def routing_node(state: ReWOOState) -> str:
    """Route based on evidence completion."""
    if state.is_evidence_complete:
        return "finalize"
    return "collect"


async def finalize_node(state: ReWOOState) -> dict[str, Any]:
    """Final node using all evidence."""
    # Get evidence context
    context = state.get_evidence_context()

    # Create final answer
    answer = f"Based on evidence:\n{context}\n\nAnswer: {state.objective}"

    return {"messages": [answer]}


# Build example graph
def build_example_graph() -> BaseGraph:
    """Build graph showing ReWOO integration."""
    graph = BaseGraph()

    # Add nodes
    graph.add_node("plan", planning_node)
    graph.add_node("collect", evidence_collection_node)
    graph.add_node("route", routing_node)
    graph.add_node("finalize", finalize_node)

    # Connect
    graph.add_edge(START, "plan")
    graph.add_edge("plan", "collect")
    graph.add_edge("collect", "route")

    # Conditional routing
    graph.add_conditional_edges(
        "route", routing_node, {"collect": "collect", "finalize": "finalize"}
    )

    graph.add_edge("finalize", END)

    return graph.compile()


# Example usage
async def run_example():
    """Run the example showing integration."""
    # Create state with tools
    state = ReWOOState(
        objective="What is the weather in Tokyo?", tools=[search_tool, analyze_tool]
    )

    # Build and run graph
    graph = build_example_graph()

    # Execute
    await graph.ainvoke(state)


# Key integration points:
# 1. Models (ReWOOPlan, Evidence) define the structure
# 2. State (ReWOOState) manages tools and evidence
# 3. Nodes use state methods to execute tools and track progress
# 4. Evidence references (#E1) are resolved automatically
