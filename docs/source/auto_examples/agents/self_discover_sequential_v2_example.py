"""Example of using the Self-Discover Sequential V2 agent with proper patterns."""

import asyncio
import os
import sys

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "src"))

from haive.agents.reasoning_and_critique.self_discover.self_discover_sequential_v2 import (
    DEFAULT_REASONING_MODULES,
    create_self_discover_sequential,
)


async def main():
    """Example of using the Self-Discover sequential agent."""
    print("Creating Self-Discover Sequential V2 agent...")

    # Create the agent
    self_discover = create_self_discover_sequential()

    # Example task
    task = """This SVG path element <path d="M 55.57,80.69 L 57.38,65.80 M 57.38,65.80 L 48.90,57.46 M 48.90,57.46 L
45.58,47.78 M 45.58,47.78 L 53.25,36.07 L 66.29,48.90 L 78.69,61.09 L 55.57,80.69"/> draws a:
(A) circle (B) heptagon (C) hexagon (D) kite (E) line (F) octagon (G) pentagon (H) rectangle (I) sector (J) triangle"""

    print(f"\nTask: {task[:100]}...")
    print("\nExecuting Self-Discover Sequential process...")
    print("This will run through 4 stages:")
    print("1. Selector - Choose relevant reasoning modules")
    print("2. Adapter - Customize modules for the task")
    print("3. Structurer - Create step-by-step plan")
    print("4. Executor - Execute plan and solve task")

    # Prepare input - note that we need to provide all fields that might be used
    initial_state = {
        "available_modules": DEFAULT_REASONING_MODULES,
        "task_description": task,
        "selected_modules_formatted": "",  # Will be populated by selector
        "adapted_modules_formatted": "",  # Will be populated by adapter
        "reasoning_plan_formatted": "",  # Will be populated by structurer
        "system_message": "You are a helpful assistant.",  # Add system message
    }

    try:
        # Execute the workflow
        print("\n" + "=" * 50)
        result = await self_discover.arun(initial_state)

        print("\n" + "=" * 50)
        print("Self-Discover completed successfully!")
        print("\nFinal Result:")

        # Check if result is a dict or object
        if isinstance(result, dict):
            for key, value in result.items():
                if key in ["final_answer", "answer", "output"]:
                    print(f"\n{key.upper()}: {value}")
                elif isinstance(value, str) and len(value) > 100:
                    print(f"\n{key}: {value[:100]}...")
                else:
                    print(f"\n{key}: {value}")
        else:
            print(result)

    except Exception as e:
        print(f"\nError during execution: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
