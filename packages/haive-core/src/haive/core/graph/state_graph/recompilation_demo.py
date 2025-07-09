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

    print("=" * 70)
    print("🔄 BASEGRAPH2 RECOMPILATION TRACKING DEMO")
    print("=" * 70)

    # Create a new graph
    graph = BaseGraph(name="recompilation_demo")

    print(f"\n📊 Initial State:")
    info = graph.get_compilation_info()
    print(f"  Needs recompile: {info['needs_recompile']}")
    print(f"  Last compiled: {info['last_compiled_at']}")
    print(f"  State hash: {info['current_state_hash']}")

    # Add some nodes - should mark as needing recompilation
    print(f"\n➕ Adding nodes...")

    def start_func(state):
        return {"status": "started"}

    def process_func(state):
        return {"status": "processed"}

    def finish_func(state):
        return {"status": "finished"}

    graph.add_node("start", start_func)
    print(f"  After adding 'start': needs_recompile = {graph.needs_recompile()}")

    graph.add_node("process", process_func)
    print(f"  After adding 'process': needs_recompile = {graph.needs_recompile()}")

    graph.add_node("finish", finish_func)
    print(f"  After adding 'finish': needs_recompile = {graph.needs_recompile()}")

    # Add edges - should mark as needing recompilation
    print(f"\n🔗 Adding edges...")
    graph.add_edge("start", "process")
    print(
        f"  After adding edge start->process: needs_recompile = {graph.needs_recompile()}"
    )

    graph.add_edge("process", "finish")
    print(
        f"  After adding edge process->finish: needs_recompile = {graph.needs_recompile()}"
    )

    # Add conditional routing - should mark as needing recompilation
    print(f"\n🔀 Adding conditional edges...")

    def router(state):
        return "continue" if state.get("count", 0) < 5 else "finish"

    destinations = {"continue": "process", "finish": "finish"}

    graph.add_conditional_edges("process", router, destinations)
    print(
        f"  After adding conditional edges: needs_recompile = {graph.needs_recompile()}"
    )

    # Set state schema - should mark as needing recompilation
    print(f"\n📋 Setting state schema...")
    graph.set_state_schema(SimpleState)
    print(f"  After setting state schema: needs_recompile = {graph.needs_recompile()}")

    # Show compilation info before "compilation"
    print(f"\n📊 Before compilation:")
    info = graph.get_compilation_info()
    print(f"  Needs recompile: {info['needs_recompile']}")
    print(f"  Current state hash: {info['current_state_hash']}")
    print(f"  State matches last: {info['state_matches']}")

    # Simulate compilation by calling to_langgraph
    print(f"\n🔨 Simulating compilation...")
    try:
        # This would normally convert to LangGraph and mark as compiled
        graph.mark_compiled()  # Manually mark as compiled for demo
        print(f"  Graph marked as compiled")
    except Exception as e:
        print(f"  Compilation simulation: {e}")

    # Show compilation info after "compilation"
    print(f"\n📊 After compilation:")
    info = graph.get_compilation_info()
    print(f"  Needs recompile: {info['needs_recompile']}")
    print(f"  Last compiled: {info['last_compiled_at']}")
    print(f"  Compilation hash: {info['compilation_state_hash']}")
    print(f"  Current hash: {info['current_state_hash']}")
    print(f"  State matches: {info['state_matches']}")

    # Now make changes that require recompilation
    print(f"\n🚨 Making changes that require recompilation...")

    print(f"\n  Adding new node 'validate'...")

    def validate_func(state):
        return {"status": "validated"}

    graph.add_node("validate", validate_func)
    print(f"    Needs recompile: {graph.needs_recompile()}")

    print(f"\n  Changing state schema...")
    graph.set_state_schema(ExtendedState)
    print(f"    Needs recompile: {graph.needs_recompile()}")

    print(f"\n  Removing an edge...")
    graph.remove_edge("process", "finish")
    print(f"    Needs recompile: {graph.needs_recompile()}")

    # Show final state
    print(f"\n📊 Final compilation state:")
    info = graph.get_compilation_info()
    print(f"  Needs recompile: {info['needs_recompile']}")
    print(
        f"  State hash changed: {info['current_state_hash'] != info['compilation_state_hash']}"
    )

    return graph


def demo_what_needs_recompilation():
    """Show what changes require recompilation vs what doesn't."""

    print("\n" + "=" * 70)
    print("📋 WHAT REQUIRES RECOMPILATION")
    print("=" * 70)

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

    print("\n🔨 Changes that REQUIRE recompilation:")
    for change in changes_requiring_recompilation:
        print(f"  {change}")

    print("\n⚡ Changes that do NOT require recompilation:")
    for change in changes_not_requiring_recompilation:
        print(f"  {change}")

    print(f"\n💡 Key insight: Graph structure changes require recompilation,")
    print(f"   runtime configuration does not.")


def demo_usage_patterns():
    """Show recommended usage patterns."""

    print("\n" + "=" * 70)
    print("🎯 RECOMMENDED USAGE PATTERNS")
    print("=" * 70)

    print(f"\n1. 🔍 Check before operations:")
    print(f"   if graph.needs_recompile():")
    print(f"       compiled_graph = graph.to_langgraph()")
    print(f"       app = compiled_graph.compile(checkpointer=checkpointer)")

    print(f"\n2. 📊 Monitor compilation state:")
    print(f"   info = graph.get_compilation_info()")
    print(f"   print(f'Last compiled: {{info[\"last_compiled_at\"]}}')")

    print(f"\n3. 🔄 Dynamic agent addition pattern:")
    print(f"   def add_agent_dynamically(self, agent):")
    print(f"       # Add to graph")
    print(f"       self.graph.add_node(agent.name, agent)")
    print(f"       ")
    print(f"       # Check if recompilation needed")
    print(f"       if self.graph.needs_recompile():")
    print(f"           self._recompile_graph()")

    print(f"\n4. ⚡ Efficient batch changes:")
    print(f"   # Make multiple changes")
    print(f"   graph.add_node('node1', func1)")
    print(f"   graph.add_node('node2', func2)")
    print(f"   graph.add_edge('node1', 'node2')")
    print(f"   ")
    print(f"   # Compile once at the end")
    print(f"   if graph.needs_recompile():")
    print(f"       compiled = graph.to_langgraph()")


def main():
    """Run all demonstrations."""

    # Run the recompilation tracking demo
    graph = demo_recompilation_tracking()

    # Show what needs recompilation
    demo_what_needs_recompilation()

    # Show usage patterns
    demo_usage_patterns()

    print("\n" + "=" * 70)
    print("🎉 RECOMPILATION TRACKING COMPLETE!")
    print("=" * 70)

    print(f"\n✅ BaseGraph2 now tracks when recompilation is needed")
    print(f"✅ Use graph.needs_recompile() to check status")
    print(f"✅ Use graph.get_compilation_info() for detailed info")
    print(f"✅ Graph automatically marks as compiled after to_langgraph()")
    print(f"✅ All structure changes trigger recompilation flag")

    return graph


if __name__ == "__main__":
    main()
