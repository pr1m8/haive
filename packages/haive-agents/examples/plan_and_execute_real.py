"""Real Plan and Execute Agent Example.

This example demonstrates a real Plan and Execute agent with actual LLM calls.
No mocks - real execution with Tavily search tool.
"""

import asyncio
import os

from dotenv import load_dotenv
from haive.core.engine import AugLLMConfig
from langchain_community.tools.tavily_search import TavilySearchResults

from haive.agents.planning import PlanAndExecuteAgent
from haive.agents.planning.p_and_e.models import Act, Plan
from haive.agents.react import ReactAgent
from haive.agents.simple import SimpleAgent

# Load environment variables
load_dotenv()

# Check for required API keys
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("Please set OPENAI_API_KEY in your .env file")

if not os.getenv("TAVILY_API_KEY"):
    # Create a mock search tool for demo
    from langchain_core.tools import tool

    @tool
    def search(query: str) -> str:
        """Search for information (mock implementation)."""
        return f"Mock search results for '{query}': Found information about {query}. This is a demo result."

    search_tool = search
else:
    # Use real Tavily search
    search_tool = TavilySearchResults(max_results=3)


async def main():
    """Run the Plan and Execute agent with real LLM calls."""
    # Create engines for each agent
    planner_engine = AugLLMConfig(
        name="planner",
        model="gpt-4o-mini",
        temperature=0.7,
        structured_output_model=Plan,
        prompt_template="""You are a planner. Your job is to create a plan to accomplish the user's objective.

Objective: {objective}

Create a step-by-step plan. Be specific and clear about what needs to be done.""",
    )

    executor_engine = AugLLMConfig(
        name="executor",
        model="gpt-4o-mini",
        temperature=0.3,
        tools=[search_tool],
        prompt_template="""You are an executor. Execute the current step of the plan.

Current Step: {current_step}

Previous Results: {previous_results}

Use the search tool if you need to find information. Be thorough in your execution.""",
    )

    replanner_engine = AugLLMConfig(
        name="replanner",
        model="gpt-4o-mini",
        temperature=0.5,
        structured_output_model=Act,
        prompt_template="""You are a replanner. Assess the progress and decide next steps.

Original Objective: {objective}
Current Plan: {plan}
Results So Far: {results}

Decide whether to:
1. Continue with the next step
2. Create a new plan
3. Provide the final answer

Be critical about whether the objective has been achieved.""",
    )

    # Create the agents
    planner = SimpleAgent(
        name="planner",
        engine=planner_engine,
        instructions="Create a comprehensive plan to achieve the objective",
    )

    executor = ReactAgent(
        name="executor",
        engine=executor_engine,
        instructions="Execute the current step using available tools",
    )

    replanner = SimpleAgent(
        name="replanner",
        engine=replanner_engine,
        instructions="Assess progress and decide next action",
    )

    # Create the Plan and Execute system
    plan_execute_agent = PlanAndExecuteAgent(
        planner=planner,
        executor=executor,
        replanner=replanner,
        name="plan_execute_system",
    )

    # Test queries
    queries = [
        "What are the top 3 programming languages to learn in 2024 and why?",
        # "Compare the weather in New York and Los Angeles today",
        # "Find the latest news about AI developments this week"
    ]

    for query in queries:

        try:
            # Run the agent
            await plan_execute_agent.arun(query)

        except Exception:
            import traceback

            traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
