#!/usr/bin/env python3
"""Working demo that shows actual supervisor execution with step-by-step output."""

import asyncio
import json
import logging

from haive.agents.experiments.dynamic_supervisor import (
    AgentRegistry,
    DynamicSupervisorAgent,
)
from haive.agents.simple.agent import SimpleAgent
from langchain_core.messages import AIMessage, HumanMessage

# Configure logging to show all output
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(message)s")

# Disable some verbose loggers
logging.getLogger("haive.core.engine").setLevel(logging.WARNING)
logging.getLogger("haive.core.persistence").setLevel(logging.WARNING)


async def run_supervisor_with_output():
    """Run supervisor and capture its decision-making process."""

    # Create supervisor
    supervisor = DynamicSupervisorAgent(
        name="Autonomous Supervisor",
        system_message="""You are an intelligent supervisor that analyzes tasks step-by-step.

For EVERY task you receive:
1. First use 'list_agents' to see available agents
2. Think about what type of agent would best handle this task
3. Check if a suitable agent exists
4. If yes: delegate using 'handoff_to_X'
5. If no: explain what type of agent would be needed

Show your thinking process clearly.""",
        debug=True,
        verbose=True,
    )

    # Add one basic agent to start
    supervisor.add_agent_to_registry(
        name="general_agent",
        description="General purpose assistant for basic tasks",
        agent_class=SimpleAgent,
        config={
            "name": "General Assistant",
            "system_message": "You are a helpful general assistant.",
        },
    )

    agents = supervisor.agent_registry.list_agents()

    # Test tasks to show decision process
    test_tasks = [
        "What is 2 + 2?",  # Simple task - should use general_agent
        "Write a Python function to sort a list",  # Coding task - no coding agent available
        "Analyze sales data and create a report",  # Data task - no data agent available
    ]


    for i, task in enumerate(test_tasks, 1):

        # Create input for supervisor
        supervisor_input = {
            "messages": [HumanMessage(content=task)],
            "current_iteration": 0,
            "max_iterations": 5,
        }

        try:
            # Run supervisor
            result = await supervisor.ainvoke(supervisor_input)

            # Extract and display the response
            if "messages" in result:
                # Show supervisor's decision process
                for msg in result["messages"]:
                    if hasattr(msg, "content") and msg.content:
                        print("pass")

                    # Show tool calls if any
                    if hasattr(msg, "tool_calls") and msg.tool_calls:
                        for tool_call in msg.tool_calls:

            # Show outcome
            if result.get("next_agent"):
                print("pass")
            else:
                passnt")

        except Exception as e:
            import traceback

            traceback.print_exc()

        await asyncio.sleep(0.5)  # Brief pause between tasks

    final_agents = supervisor.agent_registry.list_agents()

    return supervisor


async def simple_working_example():
    """Even simpler example that definitely works."""

    # Create basic supervisor
    supervisor = DynamicSupervisorAgent(
        name="Simple Supervisor", debug=False  # Less verbose
    )

    # Show initial tools
    for tool in supervisor.tools:
        pass

    # Manual demonstration of decision process




if __name__ == "__main__":

    # Try the full demo
    try:
        supervisor = asyncio.run(run_supervisor_with_output())
    except Exception as e:
        asyncio.run(simple_working_example())