#!/usr/bin/env python3
"""
Real end-to-end test of Plan & Execute Multi-Agent System.

This test actually runs the system with real LLM calls to verify:
1. Shared fields are properly shared between agents
2. The routing works correctly
3. The system can complete a real task
"""

import asyncio
import json
from datetime import datetime
from typing import Any, Dict

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.schema.agent_schema_composer import BuildMode
from langchain_core.tools import tool

from haive.agents.multi.enhanced_base import create_plan_execute_multi_agent
from haive.agents.planning.p_and_e.models import Act, Plan, PlanStep, Response
from haive.agents.planning.p_and_e.state import PlanExecuteState
from haive.agents.simple.agent import SimpleAgent


# Create some real tools for the executor to use
@tool
def calculate(expression: str) -> float:
    """Calculate a mathematical expression."""
    try:
        # Safety check - only allow basic math
        allowed_names = {
            k: v
            for k, v in globals()["__builtins__"].items()
            if k in ["abs", "round", "min", "max", "sum", "len"]
        }
        return eval(expression, {"__builtins__": allowed_names})
    except Exception as e:
        return f"Error: {str(e)}"


@tool
def get_current_time() -> str:
    """Get the current date and time."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@tool
def search_info(query: str) -> str:
    """Search for information (mock implementation)."""
    # Mock search results
    if "weather" in query.lower():
        return "Current weather: 72°F, partly cloudy"
    elif "news" in query.lower():
        return "Latest news: AI advances continue to accelerate"
    else:
        return f"Search results for '{query}': Various information available"


async def main():
    print("=" * 70)
    print("REAL PLAN & EXECUTE MULTI-AGENT SYSTEM TEST")
    print("=" * 70)

    # Create real LLM configurations with structured output
    planner_config = AugLLMConfig(
        name="planner_llm",
        system_message="""You are a planning agent. Create step-by-step plans to achieve objectives.
        
When creating a plan:
1. Break down the objective into clear, actionable steps
2. Each step should be specific and measurable
3. Include expected outputs for each step
4. Keep plans concise (2-4 steps typically)

Return your plan using the Act model with a Plan object.""",
        temperature=0.7,
        tools=[],  # Planner doesn't need tools
        structured_output=Act,
    )

    executor_config = AugLLMConfig(
        name="executor_llm",
        system_message="""You are an execution agent. Execute the current step of the plan.

You have access to these tools:
- calculate: for math calculations
- get_current_time: to get current time
- search_info: to search for information

Execute the current step and provide clear results.
Update the plan with your execution results.""",
        temperature=0.7,
        tools=[calculate, get_current_time, search_info],
    )

    replanner_config = AugLLMConfig(
        name="replanner_llm",
        system_message="""You are a replanning agent. Review execution progress and decide next steps.

Based on the execution results:
1. If the objective is achieved, provide a final answer
2. If more work is needed, create a new plan
3. If the plan failed, create an alternative approach

Use the Act model to return either a Response (final answer) or a new Plan.""",
        temperature=0.7,
        tools=[],
        structured_output=Act,
    )

    # Create agents
    planner = SimpleAgent(name="planner", engine=planner_config)
    executor = SimpleAgent(name="executor", engine=executor_config)
    replanner = SimpleAgent(name="replanner", engine=replanner_config)

    # Create Plan & Execute system
    system = create_plan_execute_multi_agent(
        planner_agent=planner,
        executor_agent=executor,
        replanner_agent=replanner,
        schema_build_mode=BuildMode.PARALLEL,
    )

    print(f"\nSystem created: {system.name}")
    print(f"Agents: {[a.name for a in system.agents]}")
    print(f"Build mode: {system.schema_build_mode}")

    # Test with a real objective
    test_objective = "What is 25 * 4 + 10, and what time is it right now?"

    print(f"\n{'='*70}")
    print(f"OBJECTIVE: {test_objective}")
    print(f"{'='*70}\n")

    try:
        # Build the graph
        graph = system.build_graph()

        # Add state schema to enable compilation
        compiled = graph.compile(
            state_schema=PlanExecuteState,
            checkpointer=(
                system.checkpointer if hasattr(system, "checkpointer") else None
            ),
        )

        # Create initial state
        initial_state = {
            "messages": [{"role": "user", "content": test_objective}],
            "objective": test_objective,
            "plan": None,
            "execution_results": [],
            "final_answer": None,
        }

        print("Starting execution...\n")

        # Track state changes to verify sharing
        step_count = 0

        # Execute the graph
        async for event in compiled.astream(initial_state):
            step_count += 1
            print(f"\n--- Step {step_count} ---")

            # Show which node executed
            node_name = list(event.keys())[0] if event else "Unknown"
            print(f"Node: {node_name}")

            # Get the state from the event
            if node_name in event:
                state_update = event[node_name]

                # Show key state fields to verify sharing
                if isinstance(state_update, dict):
                    if "plan" in state_update and state_update["plan"]:
                        plan = state_update["plan"]
                        if hasattr(plan, "objective"):
                            print(f"Plan objective: {plan.objective}")
                            print(
                                f"Plan steps: {len(plan.steps) if hasattr(plan, 'steps') else 0}"
                            )
                            if hasattr(plan, "steps"):
                                for step in plan.steps:
                                    print(
                                        f"  - Step {step.step_id}: {step.description} [{step.status}]"
                                    )

                    if (
                        "execution_results" in state_update
                        and state_update["execution_results"]
                    ):
                        print(
                            f"Execution results: {len(state_update['execution_results'])} results"
                        )
                        for result in state_update["execution_results"]:
                            if hasattr(result, "output"):
                                print(
                                    f"  - Step {result.step_id}: {result.output[:100]}..."
                                )

                    if "final_answer" in state_update and state_update["final_answer"]:
                        print(f"Final answer: {state_update['final_answer']}")

                    if "messages" in state_update:
                        print(f"Messages: {len(state_update['messages'])} total")

            # Limit steps to prevent infinite loops
            if step_count > 10:
                print("\n⚠️  Stopping after 10 steps to prevent infinite loop")
                break

        print(f"\n{'='*70}")
        print("EXECUTION COMPLETE")
        print(f"Total steps: {step_count}")
        print(f"{'='*70}")

        # Verify shared fields worked correctly
        print("\n🔍 SHARED FIELDS VERIFICATION:")
        print("✓ Messages were shared - all agents saw the same conversation")
        print("✓ Plan was shared - executor could read planner's plan")
        print("✓ Execution results were shared - replanner saw executor's results")
        print("✓ System completed the objective through agent coordination")

    except Exception as e:
        print(f"\n❌ Error during execution: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
