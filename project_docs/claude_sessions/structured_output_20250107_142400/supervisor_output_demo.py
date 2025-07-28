#!/usr/bin/env python3
"""Simple demo showing supervisor's step-by-step decision output."""

import asyncio
import logging

from haive.agents.experiments.dynamic_supervisor import DynamicSupervisorAgent
from haive.agents.simple.agent import SimpleAgent
from langchain_core.messages import HumanMessage

# Configure logging to show supervisor's thinking
logging.basicConfig(level=logging.INFO, format="%(message)s")

# Quiet other loggers
for logger_name in ["haive.core", "httpx", "langchain"]:
    logging.getLogger(logger_name).setLevel(logging.WARNING)


async def main():
    """Run supervisor and show its decision process."""

    # Create supervisor with clear instructions
    supervisor = DynamicSupervisorAgent(
        name="Decision Supervisor",
        system_message="""You are a supervisor that shows clear decision-making.

For each task:
1. Use 'list_agents' to see what agents are available
2. Analyze what type of agent would be best for this task
3. Check if a suitable agent exists
4. If yes: use 'handoff_to_X' to delegate
5. If no: use 'end_supervision' and explain what agent would be needed

Always explain your reasoning step by step.""",
        debug=True,  # This will show the execution flow
    )

    # Add a general agent
    supervisor.add_agent_to_registry(
        name="general_agent",
        description="Basic assistant for simple questions",
        agent_class=SimpleAgent,
        config={
            "name": "General Assistant",
            "system_message": "You are a helpful assistant.",
        },
    )


    # Test with different tasks
    tasks = [
        "What is the capital of France?",  # Simple - should use general_agent
        "Write Python code to sort a list",  # Complex - no coding agent exists
    ]

    for i, task in enumerate(tasks, 1):

        # Prepare input
        input_data = {
            "messages": [HumanMessage(content=task)],
            "current_iteration": 0,
            "max_iterations": 3,
        }


        try:
            # Run supervisor
            result = await supervisor.ainvoke(input_data)

            # Show the decision
            if result.get("next_agent"):
                print("pass")
            else:
                passt)")

        except Exception as e:
            pass")



if __name__ == "__main__":
    asyncio.run(main())