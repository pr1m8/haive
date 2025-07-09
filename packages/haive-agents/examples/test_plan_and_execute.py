"""
Test the Plan and Execute Agent implementation.

This example demonstrates how to use the PlanAndExecuteAgent with proper
Pydantic field configuration and MultiAgentBase inheritance.
"""

import asyncio
import os
from datetime import datetime

from haive.core.engines.llm.aug_llm_engine import AugLLMEngine
from haive.core.engines.llm.llm_engine import LLMEngine

from haive.agents.planning.plan_and_execute import PlanAndExecuteAgent


async def main():
    """Run the Plan and Execute agent example."""

    # Create LLM engine
    print("Creating LLM engine...")
    base_engine = LLMEngine(
        model="gpt-4",
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    # Create AugLLMEngine (enhanced with tool support)
    aug_engine = AugLLMEngine(
        llm_engine=base_engine, system_prompt="You are a helpful AI assistant."
    )

    # Create the Plan and Execute agent
    print("\nCreating Plan and Execute agent...")
    agent = PlanAndExecuteAgent(
        engine=aug_engine,
        name="research_assistant",
        include_tavily_search=True,  # Include Tavily search tool
        max_replanning_attempts=2,  # Allow up to 2 replanning attempts
    )

    # Test queries
    test_queries = [
        "What are the latest developments in quantum computing as of 2024?",
        "Compare the top 3 programming languages for machine learning and provide pros/cons for each.",
        "Research the environmental impact of electric vehicles vs traditional cars and summarize the key findings.",
    ]

    for query in test_queries[:1]:  # Run first query for demo
        print(f"\n{'='*60}")
        print(f"Query: {query}")
        print(f"{'='*60}")

        start_time = datetime.now()

        try:
            # Run the agent
            result = await agent.arun(query)

            # Display results
            print(f"\n{'='*60}")
            print("FINAL RESULT:")
            print(f"{'='*60}")
            print(result)

            # Show execution time
            elapsed = (datetime.now() - start_time).total_seconds()
            print(f"\n{'='*60}")
            print(f"Execution time: {elapsed:.2f} seconds")

            # Access the state to show plan details
            if hasattr(agent, "_state") and agent._state:
                state = agent._state

                # Show plan details
                if hasattr(state, "plan") and state.plan:
                    print(f"\n{'='*60}")
                    print("PLAN EXECUTION SUMMARY:")
                    print(f"{'='*60}")
                    print(f"Total steps: {state.plan.total_steps}")
                    print(f"Completed: {len(state.plan.completed_steps)}")
                    print(f"Failed: {len(state.plan.failed_steps)}")
                    print(f"Progress: {state.plan.progress_percentage:.1f}%")

                    if state.plan.steps:
                        print("\nSteps:")
                        for step in state.plan.steps:
                            status_icon = "✓" if step.status == "completed" else "○"
                            print(
                                f"  {status_icon} Step {step.step_id}: {step.description}"
                            )

                # Show replanning history
                if hasattr(state, "replan_count") and state.replan_count > 0:
                    print(f"\n{'='*60}")
                    print(f"Replanning occurred {state.replan_count} time(s)")

        except Exception as e:
            print(f"\nError: {e}")
            import traceback

            traceback.print_exc()


async def test_with_custom_prompts():
    """Test with custom prompts for agents."""

    # Create engine
    base_engine = LLMEngine(
        model="gpt-4",
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    aug_engine = AugLLMEngine(
        llm_engine=base_engine, system_prompt="You are a research assistant."
    )

    # Create agent with custom prompts
    agent = PlanAndExecuteAgent(
        engine=aug_engine,
        name="custom_researcher",
        planner_prompt="""You are a strategic planner specializing in research tasks.
        
Create a detailed research plan for: {objective}

Focus on:
1. Identifying key information sources
2. Structuring the analysis approach
3. Planning synthesis of findings

Generate 3-5 clear, actionable steps.""",
        executor_prompt="""You are a research executor with access to web search.

Objective: {objective}
Current Task: {current_step}

Previous findings:
{previous_results}

Execute this research step thoroughly and provide detailed findings.""",
        replanner_prompt="""You are a research supervisor reviewing progress.

Original goal: {objective}
Progress so far: {plan_status}
Research findings: {previous_results}

Decide whether to:
1. Provide a final synthesized answer if research is complete
2. Create additional research steps if gaps remain
3. Continue with the current plan""",
    )

    # Run a research task
    result = await agent.arun(
        "What are the main differences between REST and GraphQL APIs? "
        "Include performance considerations and use cases."
    )

    print("Research Result:")
    print(result)


if __name__ == "__main__":
    # Run the main example
    asyncio.run(main())

    # Uncomment to test with custom prompts
    # asyncio.run(test_with_custom_prompts())
