#!/usr/bin/env python3
"""Demonstration of BaseGraph2 recompilation tracking.

This script shows how the new recompilation tracking works and when
recompilation is needed vs when it's not.
"""

import logging
from typing import Any, Dict

from pydantic import BaseModel

from haive.core.graph.state_graph.base_graph2 import BaseGraph

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SimpleState(BaseModel):
    """Simple state schema for testing."""

    messages: list = []
    count: int = 0


class ExtendedState(BaseModel):
    """Extended state schema for testing."""

    messages: list = []
    count: int = 0
    status: str = "pending"


def demo_recompilation_tracking():
    """Demonstrate recompilation tracking functionality."""
    # Create a new graph
    graph = BaseGraph(name="recompilation_demo")

    info = graph.get_compilation_info()

    # Add some nodes - should mark as needing recompilation

    def start_func(state):
        return {"status": "started"}

    def process_func(state):
        return {"status": "processed"}

    def finish_func(state):
        return {"status": "finished"}

    graph.add_node("start", start_func)

    graph.add_node("process", process_func)

    graph.add_node("finish", finish_func)

    # Add edges - should mark as needing recompilation
    graph.add_edge("start", "process")

    graph.add_edge("process", "finish")

    # Add conditional routing - should mark as needing recompilation

    def router(state):
        return "continue" if state.get("count", 0) < 5 else "finish"

    destinations = {"continue": "process", "finish": "finish"}

    graph.add_conditional_edges("process", router, destinations)

    # Set state schema - should mark as needing recompilation
    graph.set_state_schema(SimpleState)

    # Show compilation info before "compilation"
    graph.get_compilation_info()

    # Simulate compilation by calling to_langgraph
    try:
        # This would normally convert to LangGraph and mark as compiled
        graph.mark_compiled()  # Manually mark as compiled for demo
    except Exception:
        pass

    # Show compilation info after "compilation"
    graph.get_compilation_info()

    # Now make changes that require recompilation

    def validate_func(state):
        return {"status": "validated"}

    graph.add_node("validate", validate_func)

    graph.set_state_schema(ExtendedState)

    graph.remove_edge("process", "finish")

    # Show final state
    graph.get_compilation_info()

    return graph


def demo_what_needs_recompilation():
    """Show what changes require recompilation vs what doesn't."""
    changes_requiring_recompilation = [
        "✅ Adding nodes (graph.add_node())",
        "✅ Removing nodes (graph.remove_node())",
        "✅ Adding edges (graph.add_edge())",
        "✅ Removing edges (graph.remove_edge())",
        "✅ Adding conditional edges (graph.add_conditional_edges())",
        "✅ Changing state schema (graph.set_state_schema())",
        "✅ Adding/removing branches",
        "✅ Modifying graph structure",
    ]

    changes_not_requiring_recompilation = [
        "❌ Runtime interrupt_before/interrupt_after",
        "❌ Checkpointer configuration",
        "❌ Thread configuration",
        "❌ Dynamic breakpoints (NodeInterrupt)",
        "❌ Runtime config parameters",
        "❌ Cache/store settings",
        "❌ Debug flags",
    ]

    for _change in changes_requiring_recompilation:
        pass

    for _change in changes_not_requiring_recompilation:
        pass


def demo_usage_patterns():
    """Show recommended usage patterns."""


def main():
    """Run all demonstrations."""
    # Run the recompilation tracking demo
    graph = demo_recompilation_tracking()

    # Show what needs recompilation
    demo_what_needs_recompilation()

    # Show usage patterns
    demo_usage_patterns()

    return graph


if __name__ == "__main__":
    main()
