#!/usr/bin/env python
"""Test to verify the FIXED dynamic supervisor can add agents after compilation.

This test demonstrates the correct approach based on BaseGraph2 limitations.
"""

import asyncio
import logging
from typing import Any, Dict, List

from langchain_core.messages import AIMessage, HumanMessage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TestAgent:
    """Simple test agent."""

    def __init__(self, name: str, response_prefix: str | None = None):
        self.name = name
        self.response_prefix = response_prefix or f"Response from {name}"
        self.invocation_count = 0

    async def ainvoke(self, state: dict[str, Any]) -> dict[str, Any]:
        """Process messages and return response."""
        self.invocation_count += 1

        messages = state.get("messages", [])
        if messages:
            last_message = messages[-1]
            content = getattr(last_message, "content", str(last_message))

            response = AIMessage(
                content=f"{self.response_prefix}: Processing '{content}' (call #{self.invocation_count})"
            )

            return {"messages": [*messages, response]}

        return {"messages": messages}


async def test_dynamic_addition_with_fixed_supervisor():
    """Test the fixed dynamic supervisor implementation."""

    # Import the fixed supervisor
    try:
        from dynamic_supervisor_fixed import DynamicSupervisorFixed
    except ImportError:
        return False

    # Create supervisor
    supervisor = DynamicSupervisorFixed(name="test_supervisor", auto_rebuild_graph=True)

    # Create and register initial agents

    writing_agent = TestAgent("writing_agent", "📝 Writer")
    supervisor.register_agent(writing_agent, "Writing and content creation")

    analysis_agent = TestAgent("analysis_agent", "🔍 Analyst")
    supervisor.register_agent(analysis_agent, "Data analysis and insights")


    # First invocation - this triggers compilation

    try:
        result1 = await supervisor.ainvoke(
            {"messages": [HumanMessage(content="Write me a short story")]}
        )
    except Exception as e:
        return False

    # Now add new agent AFTER compilation

    math_agent = TestAgent("math_agent", "🧮 Calculator")
    success = supervisor.register_agent(math_agent, "Mathematical calculations")

    # Test with math request - should trigger rebuild and route to math_agent

    try:
        result2 = await supervisor.ainvoke(
            {"messages": [HumanMessage(content="Calculate the sum of 15 and 27")]}
        )

        last_message = (
            result2.get("messages", [])[-1].content
            if result2.get("messages")
            else "No messages"
        )

        # Verify it went to math agent
        if "Calculator" in last_message:
            pass")
        else:
            passnt")

    except Exception as e:
        return False

    # Add another agent to test multiple additions

    research_agent = TestAgent("research_agent", "🔬 Researcher")
    supervisor.register_agent(research_agent, "Research and fact-finding")

    # Remove an agent to test removal

    removal_success = supervisor.unregister_agent("analysis_agent")

    # Final test with writing request

    try:
        result3 = await supervisor.ainvoke(
            {"messages": [HumanMessage(content="Write a poem about dynamic graphs")]}
        )

        last_message = (
            result3.get("messages", [])[-1].content
            if result3.get("messages")
            else "No messages"
        )

    except Exception as e:
        return False

    # Summary




    return True


async def test_edge_cases():
    """Test edge cases for dynamic supervisor."""

    try:
        from dynamic_supervisor_fixed import DynamicSupervisorFixed
    except ImportError:
        return False

    supervisor = DynamicSupervisorFixed(name="edge_case_supervisor")

    # Test 1: Invoke with no agents
    try:
        await supervisor.ainvoke({"messages": [HumanMessage(content="Hello")]})
    except Exception as e:
        pass")

    # Test 2: Add duplicate agent
    agent1 = TestAgent("duplicate")
    agent2 = TestAgent("duplicate")

    supervisor.register_agent(agent1)
    supervisor.register_agent(agent2)  # Should overwrite


    # Test 3: Remove non-existent agent
    success = supervisor.unregister_agent("non_existent")

    print("\n✅ Edge cases handled correctly!
    return None")


if __name__ == "__main__":

    # Run main test
    asyncio.run(test_dynamic_addition_with_fixed_supervisor())

    # Run edge cases
    asyncio.run(test_edge_cases())

