"""Example of Self-Discover V4 with proper state handling."""

import asyncio
import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "src"))

import contextlib

from haive.agents.reasoning_and_critique.self_discover.self_discover_v4 import (
    create_self_discover_v4,
)


async def example_basic():
    """Basic example of Self-Discover V4."""
    agent = create_self_discover_v4()

    task = """Analyze this SVG path and determine what shape it draws:
<path d="M 55.57,80.69 L 57.38,65.80 M 57.38,65.80 L 48.90,57.46 M 48.90,57.46 L
45.58,47.78 M 45.58,47.78 L 53.25,36.07 L 66.29,48.90 L 78.69,61.09 L 55.57,80.69"/>

Options: (A) circle (B) heptagon (C) hexagon (D) kite (E) line (F) octagon
(G) pentagon (H) rectangle (I) sector (J) triangle"""

    try:
        # Use the convenience method
        await agent.solve(task)

    except Exception:
        pass


async def example_custom_modules():
    """Example with custom reasoning modules."""
    # Define custom modules for a specific domain
    custom_modules = """1. User Research: Understand user needs and pain points
2. Market Analysis: Analyze market trends and competition
3. Technical Feasibility: Assess technical requirements and constraints
4. Business Model: Evaluate revenue and cost structures
5. Risk Assessment: Identify potential risks and mitigation strategies
6. MVP Planning: Define minimum viable product features
7. Growth Strategy: Plan for scaling and expansion
8. Metrics Definition: Define success metrics and KPIs"""

    agent = create_self_discover_v4()

    task = "How can I create a successful food delivery app for college students?"

    with contextlib.suppress(Exception):
        await agent.solve(task, modules=custom_modules)


async def example_step_by_step():
    """Example showing step-by-step execution."""
    agent = create_self_discover_v4()

    task = "Design an efficient system for managing hospital emergency room wait times"

    # Prepare initial state manually to see intermediate results
    state = agent.prepare_initial_state(task)

    # We can't easily intercept intermediate results with EnhancedMultiAgentV4
    # So just run the full workflow
    try:
        result = await agent.arun(state)

        if isinstance(result, dict):
            # Try to extract key information
            for key in ["selected", "adapted", "plan", "answer"]:
                if result.get(key):
                    str(result[key])

    except Exception:
        import traceback

        traceback.print_exc()


async def main():
    """Run all examples."""
    # Run examples
    await example_basic()
    await example_custom_modules()
    await example_step_by_step()


if __name__ == "__main__":
    asyncio.run(main())
