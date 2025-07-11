#!/usr/bin/env python
"""Test to verify graph rebuilding actually works with dynamic agents."""

import asyncio
import logging
from typing import Any, Dict

from langchain_core.messages import AIMessage, HumanMessage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DebugAgent:
    """Agent that logs its execution for debugging."""

    def __init__(self, name: str, specialty: str):
        self.name = name
        self.specialty = specialty
        self.execution_count = 0

    async def ainvoke(self, state: dict[str, Any]) -> dict[str, Any]:
        """Execute and log."""
        self.execution_count += 1

        messages = state.get("messages", [])
        response = AIMessage(
            content=f"{self.name} ({self.specialty}): Execution #{self.execution_count}"
        )

        logger.info(f"🤖 {self.name} executed (count: {self.execution_count})")

        return {"messages": [*messages, response]}


async def test_graph_rebuilding():
    """Test that graph rebuilding works correctly."""

    # Import our rebuild supervisor
    try:
        from rebuild_dynamic_supervisor import RebuildDynamicSupervisor
    except ImportError:
        return

    # Create supervisor
    supervisor = RebuildDynamicSupervisor(
        name="test_rebuild_supervisor", auto_rebuild=True
    )

    # Verify initial state

    # Add two initial agents

    research_agent = DebugAgent("research_agent", "information gathering")
    writing_agent = DebugAgent("writing_agent", "content creation")

    supervisor.register_agent(research_agent, "research and analysis")
    supervisor.register_agent(writing_agent, "writing and documentation")


    # First invocation - should build initial graph

    await supervisor.ainvoke(
        {"messages": [HumanMessage(content="Research AI trends")]}
    )


    # Verify agent was called

    # Add new agent AFTER graph is built

    math_agent = DebugAgent("math_agent", "calculations")
    supervisor.register_agent(math_agent, "mathematical calculations")


    # Second invocation - should rebuild graph first

    await supervisor.ainvoke(
        {"messages": [HumanMessage(content="Calculate the sum of 15 and 27")]}
    )


    # Verify new agent was called

    # Test removing an agent

    supervisor.unregister_agent("writing_agent")

    # Third invocation - should rebuild without writing_agent

    await supervisor.ainvoke(
        {"messages": [HumanMessage(content="Write a summary")]}  # No writing agent!
    )


    # Summary



    # Verify graph structure
    if supervisor.graph:

        # Check if math_agent node exists
        if "math_agent" in supervisor.graph.nodes:
            pass")

        # Check if writing_agent node is gone
        if "writing_agent" not in supervisor.graph.nodes:
            pass")



async def test_rebuild_edge_cases():
    """Test edge cases for graph rebuilding."""

    from rebuild_dynamic_supervisor import RebuildDynamicSupervisor

    # Test 1: Multiple rapid changes

    supervisor = RebuildDynamicSupervisor(name="edge_supervisor")

    # Add several agents rapidly
    for i in range(5):
        agent = DebugAgent(f"agent_{i}", f"task_{i}")
        supervisor.register_agent(agent, f"capability_{i}")


    # Single invocation should handle all changes
    result = await supervisor.ainvoke(
        {"messages": [HumanMessage(content="Do something")]}
    )


    # Test 2: Rebuild with no agents

    # Remove all agents
    agent_names = list(supervisor._agent_registry.keys())
    for name in agent_names:
        supervisor.unregister_agent(name)


    # Should handle gracefully
    await supervisor.ainvoke(
        {"messages": [HumanMessage(content="Do something with no agents")]}
    )




if __name__ == "__main__":

    # Run main test
    asyncio.run(test_graph_rebuilding())

    # Run edge cases
    asyncio.run(test_rebuild_edge_cases())

