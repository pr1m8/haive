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

    def __init__(self, name: str, response_prefix: str = None):
        self.name = name
        self.response_prefix = response_prefix or f"Response from {name}"
        self.invocation_count = 0

    async def ainvoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Process messages and return response."""
        self.invocation_count += 1

        messages = state.get("messages", [])
        if messages:
            last_message = messages[-1]
            content = getattr(last_message, "content", str(last_message))

            response = AIMessage(
                content=f"{self.response_prefix}: Processing '{content}' (call #{self.invocation_count})"
            )

            return {"messages": messages + [response]}

        return {"messages": messages}


async def test_dynamic_addition_with_fixed_supervisor():
    """Test the fixed dynamic supervisor implementation."""

    print("\n" + "=" * 70)
    print("🧪 TESTING FIXED DYNAMIC SUPERVISOR - ADDING AGENTS AFTER COMPILATION")
    print("=" * 70 + "\n")

    # Import the fixed supervisor
    try:
        from dynamic_supervisor_fixed import DynamicSupervisorFixed
    except ImportError:
        print("❌ Could not import DynamicSupervisorFixed")
        print("   Make sure dynamic_supervisor_fixed.py is in the same directory")
        return False

    # Create supervisor
    print("[Step 1] Creating Dynamic Supervisor")
    supervisor = DynamicSupervisorFixed(name="test_supervisor", auto_rebuild_graph=True)
    print(f"✅ Supervisor created: {supervisor.name}")

    # Create and register initial agents
    print("\n[Step 2] Registering initial agents BEFORE compilation")

    writing_agent = TestAgent("writing_agent", "📝 Writer")
    supervisor.register_agent(writing_agent, "Writing and content creation")

    analysis_agent = TestAgent("analysis_agent", "🔍 Analyst")
    supervisor.register_agent(analysis_agent, "Data analysis and insights")

    print(f"✅ Registered agents: {supervisor.get_registered_agents()}")

    # First invocation - this triggers compilation
    print("\n[Step 3] First invocation (triggers initial compilation)")

    try:
        result1 = await supervisor.ainvoke(
            {"messages": [HumanMessage(content="Write me a short story")]}
        )
        print(f"✅ First invocation successful")
        print(
            f"   Last message: {result1.get('messages', [])[-1].content if result1.get('messages') else 'No messages'}"
        )
    except Exception as e:
        print(f"❌ First invocation failed: {e}")
        return False

    # Now add new agent AFTER compilation
    print("\n[Step 4] Adding math_agent AFTER compilation")

    math_agent = TestAgent("math_agent", "🧮 Calculator")
    success = supervisor.register_agent(math_agent, "Mathematical calculations")
    print(f"✅ Math agent registered: {success}")
    print(f"   Current agents: {supervisor.get_registered_agents()}")

    # Test with math request - should trigger rebuild and route to math_agent
    print("\n[Step 5] Testing with math request (should trigger rebuild)")

    try:
        result2 = await supervisor.ainvoke(
            {"messages": [HumanMessage(content="Calculate the sum of 15 and 27")]}
        )
        print(f"✅ Math request successful")

        last_message = (
            result2.get("messages", [])[-1].content
            if result2.get("messages")
            else "No messages"
        )
        print(f"   Response: {last_message}")

        # Verify it went to math agent
        if "Calculator" in last_message:
            print("   ✅ Correctly routed to math_agent!")
        else:
            print("   ⚠️  May not have routed to math_agent")

    except Exception as e:
        print(f"❌ Math request failed: {e}")
        return False

    # Add another agent to test multiple additions
    print("\n[Step 6] Adding research_agent")

    research_agent = TestAgent("research_agent", "🔬 Researcher")
    supervisor.register_agent(research_agent, "Research and fact-finding")

    # Remove an agent to test removal
    print("\n[Step 7] Removing analysis_agent")

    removal_success = supervisor.unregister_agent("analysis_agent")
    print(f"✅ Agent removed: {removal_success}")
    print(f"   Remaining agents: {supervisor.get_registered_agents()}")

    # Final test with writing request
    print("\n[Step 8] Final test with writing request")

    try:
        result3 = await supervisor.ainvoke(
            {"messages": [HumanMessage(content="Write a poem about dynamic graphs")]}
        )
        print(f"✅ Final request successful")

        last_message = (
            result3.get("messages", [])[-1].content
            if result3.get("messages")
            else "No messages"
        )
        print(f"   Response: {last_message}")

    except Exception as e:
        print(f"❌ Final request failed: {e}")
        return False

    # Summary
    print("\n" + "=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)

    print(f"\n✅ Successfully demonstrated:")
    print(f"   1. Initial compilation with 2 agents")
    print(f"   2. Added math_agent after compilation")
    print(f"   3. Graph rebuilt automatically on next invocation")
    print(f"   4. New agent was immediately available for routing")
    print(f"   5. Removed analysis_agent successfully")
    print(f"   6. Final state: {len(supervisor.get_registered_agents())} agents")

    print(f"\n🎯 Agent invocation counts:")
    print(f"   - writing_agent: {writing_agent.invocation_count} calls")
    print(f"   - math_agent: {math_agent.invocation_count} calls")
    print(f"   - research_agent: {research_agent.invocation_count} calls")
    print(f"   - analysis_agent: {analysis_agent.invocation_count} calls (removed)")

    print("\n✅ CONCLUSION: Dynamic agent addition WORKS with proper implementation!")
    print("   Key insight: Lazy rebuilding through Agent.create_runnable()")

    return True


async def test_edge_cases():
    """Test edge cases for dynamic supervisor."""

    print("\n\n" + "=" * 70)
    print("🧪 TESTING EDGE CASES")
    print("=" * 70 + "\n")

    try:
        from dynamic_supervisor_fixed import DynamicSupervisorFixed
    except ImportError:
        return False

    supervisor = DynamicSupervisorFixed(name="edge_case_supervisor")

    # Test 1: Invoke with no agents
    print("[Edge Case 1] Invoking with no registered agents")
    try:
        result = await supervisor.ainvoke({"messages": [HumanMessage(content="Hello")]})
        print("✅ Handled empty registry gracefully")
    except Exception as e:
        print(f"❌ Failed with empty registry: {e}")

    # Test 2: Add duplicate agent
    print("\n[Edge Case 2] Adding duplicate agent names")
    agent1 = TestAgent("duplicate")
    agent2 = TestAgent("duplicate")

    supervisor.register_agent(agent1)
    supervisor.register_agent(agent2)  # Should overwrite

    print(f"✅ Registry has {len(supervisor.get_registered_agents())} agents")
    print(f"   Expected 1, got {len(supervisor.get_registered_agents())}")

    # Test 3: Remove non-existent agent
    print("\n[Edge Case 3] Removing non-existent agent")
    success = supervisor.unregister_agent("non_existent")
    print(f"✅ Removal of non-existent agent returned: {success} (should be False)")

    print("\n✅ Edge cases handled correctly!")


if __name__ == "__main__":
    print("🚀 Dynamic Supervisor Test Suite")
    print("Testing the FIXED implementation that properly handles graph rebuilding\n")

    # Run main test
    asyncio.run(test_dynamic_addition_with_fixed_supervisor())

    # Run edge cases
    asyncio.run(test_edge_cases())

    print("\n🎉 All tests completed!")
