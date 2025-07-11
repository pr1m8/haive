#!/usr/bin/env python3
"""Real Plan & Execute Multi-Agent System Test using existing components.

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


    # Create Plan & Execute system using our new MultiAgentBase
    system = create_plan_execute_multi_agent(
        planner_agent=planner,
        executor_agent=executor,
        replanner_agent=replanner,
        schema_build_mode=BuildMode.PARALLEL,
    )


    # Test objective
    objective = "What is the current population of Tokyo and how does it compare to New York City?"


    try:
        # Build and compile the graph
        graph = system.build_graph()
        compiled = graph.compile()

        # Create initial state
        initial_state = {
            "messages": [{"role": "user", "content": objective}],
            "objective": objective,
        }


        step_count = 0
        async for event in compiled.astream(initial_state):
            step_count += 1

            for node_name, state_update in event.items():

                # Show key state changes to verify sharing
                if isinstance(state_update, dict):
                    if state_update.get("plan"):
                        plan = state_update["plan"]
                        if hasattr(plan, "objective"):
                            pass
                        if hasattr(plan, "steps"):
                            for i, step in enumerate(plan.steps[:3], 1):  # Show first 3
                                status = (
                                    step.status
                                    if hasattr(step, "status")
                                    else "unknown"
                                )

                    if (
                        state_update.get("execution_results")
                    ):
                        for result in state_update["execution_results"][
                            -2:
                        ]:  # Show last 2
                            if hasattr(result, "output"):
                                output = (
                                    result.output[:100] + "..."
                                    if len(result.output) > 100
                                    else result.output
                                )

                    if state_update.get("final_answer"):
                        pass

                    if "messages" in state_update:
                        passl")

            # Limit to prevent runaway
            if step_count > 15:
                break



    except Exception as e:
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
