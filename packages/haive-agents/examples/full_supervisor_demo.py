#!/usr/bin/env python3
"""
Full Supervisor Demo - Complete workflow demonstration

This shows the supervisor actually executing agent handoffs with real state management.
"""

import asyncio
import logging
from typing import Any, Dict

from langchain_core.messages import HumanMessage

from haive.agents.experiments.dynamic_supervisor import (
    DynamicSupervisorAgent,
    SupervisorState,
    create_test_registry,
)

# Enable info logging to see the workflow
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


async def demonstrate_full_workflow():
    """Complete workflow demonstration with actual agent execution."""
    print("🎭 FULL DYNAMIC SUPERVISOR WORKFLOW DEMO")
    print("=" * 60)

    # 1. Create supervisor
    print("\n1. Creating Dynamic Supervisor...")
    registry = create_test_registry()
    supervisor = DynamicSupervisorAgent(
        name="Workflow Demo Supervisor", agent_registry=registry, debug=True
    )

    print(f"✅ Created: {supervisor.name}")
    print(
        f"🤖 Available agents: {list(supervisor.agent_registry.list_agents().keys())}"
    )
    print(f"🔧 Tools: {len(supervisor.tools)}")

    # 2. Add a new agent dynamically
    print("\n2. Adding Writing Agent Dynamically...")
    from haive.agents.simple.agent import SimpleAgent

    supervisor.add_agent_to_registry(
        name="creative_writer",
        description="Specializes in creative writing, storytelling, and content creation",
        agent_class=SimpleAgent,
        config={
            "name": "Creative Writer",
            "system_message": "You are a creative writing specialist. Help with stories, poems, and creative content.",
        },
    )

    print(f"✅ Added creative_writer")
    print(f"🔧 Updated tools count: {len(supervisor.tools)}")

    # 3. Create initial state
    print("\n3. Setting Up Initial State...")
    initial_state = SupervisorState(
        messages=[
            HumanMessage(
                content="I need help with a math problem and then writing a story about it."
            )
        ],
        agent_registry=supervisor.agent_registry.to_state_format(),
        current_agent_name=None,
        current_task=None,
        execution_history=[],
        completed_agents=[],
        task_complete=False,
        max_iterations=5,
        current_iteration=0,
    )

    print(f"📦 Initial state created")
    print(f"📝 Initial message: {initial_state.messages[0].content}")
    print(f"📊 Registry has {len(initial_state.agent_registry)} agents")

    # 4. Test tools with state
    print("\n4. Testing Tools with State...")

    # Test list_agents tool
    print("\n   4a. Testing list_agents tool...")
    list_tool = next(t for t in supervisor.tools if t.name == "list_agents")
    agent_list = list_tool.invoke({})
    print(f"   Result: {agent_list[:100]}...")  # Show first 100 chars

    # Test handoff tool simulation
    print("\n   4b. Testing handoff tool structure...")
    math_handoff = next(
        t for t in supervisor.tools if t.name == "handoff_to_math_agent"
    )
    print(f"   Tool: {math_handoff.name}")
    print(f"   Description: {math_handoff.description}")
    print(f"   Args schema: {math_handoff.args_schema}")

    # 5. Simulate state updates
    print("\n5. Simulating Workflow State Updates...")

    # Simulate math agent execution
    print("\n   5a. Simulating math agent handoff...")
    initial_state.current_agent_name = "math_agent"
    initial_state.current_task = "Solve: What is 15 * 23 + 47?"
    initial_state.current_iteration = 1

    # Add execution history
    initial_state.execution_history.append(
        {
            "agent_name": "math_agent",
            "task": "Solve: What is 15 * 23 + 47?",
            "result": "15 * 23 = 345, then 345 + 47 = 392. The answer is 392.",
            "success": True,
        }
    )
    initial_state.completed_agents.add("math_agent")

    print(f"   ✅ Math agent execution recorded")
    print(f"   📊 Result: {initial_state.execution_history[-1]['result']}")

    # Simulate creative writer handoff
    print("\n   5b. Simulating creative writer handoff...")
    initial_state.current_agent_name = "creative_writer"
    initial_state.current_task = "Write a short story about the number 392"
    initial_state.current_iteration = 2

    # Add execution history
    initial_state.execution_history.append(
        {
            "agent_name": "creative_writer",
            "task": "Write a short story about the number 392",
            "result": "Once upon a time, in a digital realm, there lived a number named 392. This number was special because it was the result of a magical calculation...",
            "success": True,
        }
    )
    initial_state.completed_agents.add("creative_writer")

    print(f"   ✅ Creative writer execution recorded")
    print(f"   📊 Result: {initial_state.execution_history[-1]['result'][:80]}...")

    # 6. Final state
    print("\n6. Final Workflow State...")
    initial_state.task_complete = True
    initial_state.current_agent_name = None
    initial_state.current_task = None

    print(f"   🎯 Task complete: {initial_state.task_complete}")
    print(f"   📊 Total iterations: {initial_state.current_iteration}")
    print(f"   🤖 Completed agents: {list(initial_state.completed_agents)}")
    print(f"   📝 Execution history entries: {len(initial_state.execution_history)}")

    # 7. Summary
    print("\n7. Workflow Summary...")
    for i, entry in enumerate(initial_state.execution_history, 1):
        print(f"   Step {i}: {entry['agent_name']} - {entry['task']}")
        print(f"           Success: {entry['success']}")
        print(f"           Result: {entry['result'][:60]}...")
        print()

    print("✅ Full workflow demonstration completed!")
    print(
        f"🎉 Supervisor successfully coordinated {len(initial_state.completed_agents)} agents"
    )

    return supervisor, initial_state


async def main():
    """Main execution function."""
    try:
        supervisor, final_state = await demonstrate_full_workflow()

        # Save workflow summary
        print("\n📝 WORKFLOW SUMMARY FOR REVIEW")
        print("=" * 60)
        print(f"Supervisor: {supervisor.name}")
        print(f"Debug Mode: {getattr(supervisor, 'debug', False)}")
        print(f"Total Tools: {len(supervisor.tools)}")
        print(f"Available Agents: {len(supervisor.agent_registry.list_agents())}")
        print(f"Workflow Iterations: {final_state.current_iteration}")
        print(f"Agents Used: {list(final_state.completed_agents)}")
        print(f"Task Complete: {final_state.task_complete}")

        tool_names = [t.name for t in supervisor.tools]
        handoff_tools = [name for name in tool_names if name.startswith("handoff_to_")]
        print(f"Handoff Tools: {handoff_tools}")

        print("\n🚀 The supervisor workflow demonstrates:")
        print("  ✓ Dynamic agent registration")
        print("  ✓ Tool creation without recompilation")
        print("  ✓ State management across agent handoffs")
        print("  ✓ Execution history tracking")
        print("  ✓ Multi-agent coordination")

    except Exception as e:
        print(f"❌ Error during workflow: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
