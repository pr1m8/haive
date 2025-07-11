# src/haive/agents/self_discovery/example.py
"""Example usage of the Self-Discovery reasoning system."""


from haive.agents.reasoning_and_critique.self_discover.v2.agent import (
    DEFAULT_REASONING_MODULES,
    self_discovery,
)
from haive.agents.reasoning_and_critique.self_discover.v2.state import (
    SelfDiscoveryState,
)


def run_self_discovery_example():
    """Run the self-discovery agent on example tasks."""
    # Example 1: Simple math problem
    task1 = "Lisa has 10 apples. She gives 3 apples to her friend and then buys 5 more apples from the store. How many apples does Lisa have now?"

    # Example 2: SVG shape identification
    task2 = """This SVG path element <path d="M 55.57,80.69 L 57.38,65.80 M 57.38,65.80 L 48.90,57.46 M 48.90,57.46 L
45.58,47.78 M 45.58,47.78 L 53.25,36.07 L 66.29,48.90 L 78.69,61.09 L 55.57,80.69"/> draws a:
(A) circle (B) heptagon (C) hexagon (D) kite (E) line (F) octagon (G) pentagon (H) rectangle (I) sector (J) triangle"""

    # Prepare reasoning modules string
    reasoning_modules_str = "\n".join(DEFAULT_REASONING_MODULES)

    # Run on first task

    state1 = SelfDiscoveryState(
        task_description=task1, reasoning_modules=reasoning_modules_str
    )

    self_discovery.invoke(state1)

    # Run on second task

    state2 = SelfDiscoveryState(
        task_description=task2, reasoning_modules=reasoning_modules_str
    )

    result2 = self_discovery.invoke(state2)

    # Show intermediate results

    if result2.selected_modules:
        for _i, _module in enumerate(result2.selected_modules, 1):
            pass

    if result2.adapted_modules:
        for _module_dict in result2.adapted_modules:
            pass

    if result2.reasoning_structure:
        pass


def run_custom_task(task_description: str, custom_modules: list[str] | None = None):
    """Run self-discovery on a custom task."""
    modules = custom_modules or DEFAULT_REASONING_MODULES
    reasoning_modules_str = "\n".join(modules)

    state = SelfDiscoveryState(
        task_description=task_description, reasoning_modules=reasoning_modules_str
    )

    result = self_discovery.invoke(state)

    return result


if __name__ == "__main__":
    run_self_discovery_example()
