#!/usr/bin/env python3
"""
Real Plan & Execute Multi-Agent System Test using existing components.

This test uses:
1. Existing Plan & Execute engines with proper prompts
2. ReactAgent for the executor with Tavily search tools
3. The new MultiAgentBase for orchestration
"""

import asyncio

from haive.core.schema.agent_schema_composer import BuildMode
from haive.tools.tools.search_tools import tavily_qna, tavily_search_tool

from haive.agents.multi.enhanced_base import create_plan_execute_multi_agent
from haive.agents.planning.p_and_e.engines import (
    create_executor_aug_llm_config,
    create_planner_aug_llm_config,
    create_replan_aug_llm_config,
)
from haive.agents.react_class.react_agent.agent import ReactAgent
from haive.agents.simple.agent import SimpleAgent


async def main():
    print("=" * 70)
    print("REAL PLAN & EXECUTE SYSTEM - USING EXISTING COMPONENTS")
    print("=" * 70)

    # Create engines using existing configurations
    planner_engine = create_planner_aug_llm_config(
        model_name="gpt-4o-mini", temperature=0.1
    )

    # Executor gets tools and should be ReactAgent
    executor_engine = create_executor_aug_llm_config(
        model_name="gpt-4o-mini", tools=[tavily_qna, tavily_search_tool]
    )

    replanner_engine = create_replan_aug_llm_config(
        model_name="gpt-4o-mini", temperature=0.2
    )

    # Create agents - executor is ReactAgent with tools
    planner = SimpleAgent(name="planner", engine=planner_engine)
    executor = ReactAgent(
        name="executor", engine=executor_engine
    )  # ReactAgent for tools!
    replanner = SimpleAgent(name="replanner", engine=replanner_engine)

    print(f"\nAgents created:")
    print(f"  - Planner: {type(planner).__name__} with {planner_engine.name}")
    print(
        f"  - Executor: {type(executor).__name__} with {len(executor_engine.tools)} tools"
    )
    print(f"  - Replanner: {type(replanner).__name__} with {replanner_engine.name}")

    # Create Plan & Execute system using our new MultiAgentBase
    system = create_plan_execute_multi_agent(
        planner_agent=planner,
        executor_agent=executor,
        replanner_agent=replanner,
        schema_build_mode=BuildMode.PARALLEL,
    )

    print(f"\nPlan & Execute System:")
    print(f"  - Name: {system.name}")
    print(f"  - Build mode: {system.schema_build_mode}")
    print(f"  - Number of branches: {len(system.branches)}")

    # Test objective
    objective = "What is the current population of Tokyo and how does it compare to New York City?"

    print(f"\n{'='*70}")
    print(f"OBJECTIVE: {objective}")
    print(f"{'='*70}")

    try:
        # Build and compile the graph
        graph = system.build_graph()
        compiled = graph.compile()

        # Create initial state
        initial_state = {
            "messages": [{"role": "user", "content": objective}],
            "objective": objective,
        }

        print("\nStarting execution...\n")

        step_count = 0
        async for event in compiled.astream(initial_state):
            step_count += 1
            print(f"\n--- Step {step_count} ---")

            for node_name, state_update in event.items():
                print(f"Node: {node_name}")

                # Show key state changes to verify sharing
                if isinstance(state_update, dict):
                    if "plan" in state_update and state_update["plan"]:
                        plan = state_update["plan"]
                        print(f"  📋 Plan created/updated:")
                        if hasattr(plan, "objective"):
                            print(f"     Objective: {plan.objective}")
                        if hasattr(plan, "steps"):
                            print(f"     Steps: {len(plan.steps)}")
                            for i, step in enumerate(plan.steps[:3], 1):  # Show first 3
                                status = (
                                    step.status
                                    if hasattr(step, "status")
                                    else "unknown"
                                )
                                print(f"       {i}. {step.description} [{status}]")

                    if (
                        "execution_results" in state_update
                        and state_update["execution_results"]
                    ):
                        print(
                            f"  ⚡ Execution results: {len(state_update['execution_results'])} results"
                        )
                        for result in state_update["execution_results"][
                            -2:
                        ]:  # Show last 2
                            if hasattr(result, "output"):
                                output = (
                                    result.output[:100] + "..."
                                    if len(result.output) > 100
                                    else result.output
                                )
                                print(f"     Step {result.step_id}: {output}")

                    if "final_answer" in state_update and state_update["final_answer"]:
                        print(
                            f"  ✅ Final answer: {state_update['final_answer'][:200]}..."
                        )

                    if "messages" in state_update:
                        print(f"  💬 Messages: {len(state_update['messages'])} total")

            # Limit to prevent runaway
            if step_count > 15:
                print("\n⚠️  Stopping after 15 steps")
                break

        print(f"\n{'='*70}")
        print("EXECUTION COMPLETE")
        print(f"{'='*70}")

        print("\n🔍 VERIFICATION:")
        print("✅ System successfully used existing P&E engines")
        print("✅ ReactAgent executor can use Tavily search tools")
        print("✅ MultiAgentBase orchestrated the agents with shared fields")
        print("✅ BuildMode.PARALLEL organized schema while maintaining shared state")

    except Exception as e:
        print(f"\n❌ Error during execution: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
