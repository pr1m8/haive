"""Example of using the Self-Discover agent."""

import asyncio
import os
import sys

# Add the src directory to the path so we can import the modules
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "src"))

from haive.agents.reasoning_and_critique.self_discover.agent import (
    create_self_discover_agent,
    get_default_modules,
)


async def main():
    """Example usage of Self-Discover agent."""
    print("Creating Self-Discover agent...")

    # Create Self-Discover agent
    agent = create_self_discover_agent()

    # Example task
    task_example = """This SVG path element <path d="M 55.57,80.69 L 57.38,65.80 M 57.38,65.80 L 48.90,57.46 M 48.90,57.46 L
45.58,47.78 M 45.58,47.78 L 53.25,36.07 L 66.29,48.90 L 78.69,61.09 L 55.57,80.69"/> draws a:
(A) circle (B) heptagon (C) hexagon (D) kite (E) line (F) octagon (G) pentagon(H) rectangle (I) sector (J) triangle"""

    print(f"\nTask: {task_example[:100]}...")
    print("\nExecuting Self-Discover process...")

    # Prepare input with modules and task
    input_data = {
        "available_modules": get_default_modules(),
        "task_description": task_example,
    }

    try:
        # Execute the Self-Discover process
        result = await agent.arun(input_data)
        print("\nSelf-Discover completed successfully!")
        print(f"Result: {result}")
    except Exception as e:
        print(f"\nError during execution: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
