#!/usr/bin/env python3
"""Quick example of using SequentialAgent with imported AugLLMConfig components.

This demonstrates how to easily chain together pre-configured components
for a sequential reasoning workflow.
"""

from haive.core.utils.pydantic_utils import pretty_print

# Import the pre-configured AugLLMConfigs directly
from haive.agents.reasoning_and_critique.self_discover.aug_llms import (
    adapt_chain,
    select_chain,
    structured_chain,
)
from haive.agents.sequential.config import SequentialAgentConfig

# Create the sequential agent with the imported components
agent = SequentialAgentConfig.from_components(
    components=[select_chain, adapt_chain, structured_chain],
    name="reasoning_workflow_agent",
    # Optionally provide custom step names
    step_names=["select_modules", "adapt_modules", "create_plan"],
).build_agent()

# Print the workflow
print("\n=== SEQUENTIAL REASONING WORKFLOW ===\n")
print(agent.explain_workflow())


def run_example():
    # Define a task
    task = "Design an algorithm to detect fraudulent credit card transactions"

    print(f"\nTask: {task}\n")
    print("Running sequential reasoning workflow...\n")

    # Run the agent (automatically handles data passing between steps)
    result = agent.run({"task_description": task})

    # Display the final plan
    print("\n=== FINAL REASONING PLAN ===\n")

    if "plan" in result:
        pretty_print(result["plan"], "Reasoning Plan")
    else:
        pretty_print(result, "Complete Result")

    return result


if __name__ == "__main__":
    run_example()
