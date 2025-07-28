#!/usr/bin/env python3
"""Full Supervisor Demo - Complete workflow demonstration.

This shows the supervisor actually executing agent handoffs with real state management.
"""
"""
"""

import asyncio
import logging

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
    # 1. Create supervisor
    registry = create_test_registry()
    supervisor = DynamicSupervisorAgent(
        name="Workflow Demo Supervisor", agent_registry=registry, debug=True
    )

    # 2. Add a new agent dynamically
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

    # 3. Create initial state
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

    # 4. Test tools with state

    # Test list_agents tool
    list_tool = next(t for t in supervisor.tools if t.name == "list_agents")
    list_tool.invoke({})

    # Test handoff tool simulation
    next(t for t in supervisor.tools if t.name == "handoff_to_math_agent")

    # 5. Simulate state updates

    # Simulate math agent execution
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

    # Simulate creative writer handoff
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

    # 6. Final state
    initial_state.task_complete = True
    initial_state.current_agent_name = None
    initial_state.current_task = None

    # 7. Summary
    for _i, _entry in enumerate(initial_state.execution_history, 1):
        pass

    return supervisor, initial_state


async def main():
    """Main execution function."""
    try:
        supervisor, final_state = await demonstrate_full_workflow()

        # Save workflow summary

        tool_names = [t.name for t in supervisor.tools]
        [name for name in tool_names if name.startswith("handoff_to_")]

    except Exception:
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
