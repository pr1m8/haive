#!/usr/bin/env python3
"""Plan and Execute Guide - Strategic Multi-Step Problem Solving.

Difficulty: ⭐⭐⭐ Intermediate
Estimated Time: 15 minutes
Learning Objectives:
  • Create strategic planning agents
  • Understand multi-step execution
  • Handle complex workflows
  • Use replanning when needed

Next Steps:
  → Try multi_agent_coordination.py for team workflows
  → Explore advanced workflow patterns
"""

import asyncio
import logging

from haive.agents.planning.plan_and_execute import (
    create_plan_and_execute_agent,
)
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.tools import tool

# Setup logging to see the planning process
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Research tools for the agent
@tool
def web_search(query: str) -> str:
    """Search the web for information.

    Args:
        query: Search query

    Returns:
        Search results (simulated for this example)
    """
    # Simulated search results
    search_results = {
        "ai trends": "AI trends include: Large Language Models, Multimodal AI, AI Ethics, Edge AI, and Autonomous Systems.",
        "machine learning": "Machine learning is a subset of AI that enables systems to learn from data without explicit programming.",
        "python frameworks": "Popular Python frameworks include: Django, Flask, FastAPI, PyTorch, TensorFlow, and Streamlit.",
        "climate change": "Climate change refers to long-term shifts in global temperatures and weather patterns.",
    }

    # Simple keyword matching for simulation
    for keyword, result in search_results.items():
        if keyword in query.lower():
            return result

    return f"Search results for '{query}': [Simulated results - detailed information about {query}]"


@tool
def data_analyzer(data: str) -> str:
    """Analyze data and provide insights.

    Args:
        data: Data to analyze

    Returns:
        Analysis results and insights
    """
    word_count = len(data.split())
    char_count = len(data)

    return f"""Data Analysis:
• Word count: {word_count}
• Character count: {char_count}
• Key insights: The data contains structured information suitable for further processing
• Recommendation: Consider categorizing the main themes for better organization"""


@tool
def report_generator(content: str) -> str:
    """Generate a structured report from content.

    Args:
        content: Content to format into a report

    Returns:
        Formatted report
    """
    return f"""RESEARCH REPORT
================

EXECUTIVE SUMMARY:
{content[:200]}...

KEY FINDINGS:
• Research completed successfully
• Data analysis performed
• Insights generated

RECOMMENDATIONS:
• Continue monitoring developments
• Consider implementation strategies
• Plan follow-up research

Generated on: {asyncio.get_event_loop().time()}"""


async def main():
    """Run the Plan and Execute guide."""
    # Step 1: Create specialized configurations

    # Planner config - focused on strategic thinking
    planner_config = AugLLMConfig(
        temperature=0.7,
        system_message="""You are a strategic planner. Create detailed, actionable plans
for complex tasks. Break down problems into logical steps.""",
    )

    # Executor config - focused on execution
    executor_config = AugLLMConfig(
        temperature=0.3,
        system_message="""You are a task executor. Follow plans precisely and use
available tools effectively to complete each step.""",
    )

    # Step 2: Create the Plan and Execute agent

    # Method 1: Using the factory function (recommended)
    agent = create_plan_and_execute_agent(
        name="research_agent",
        planner_config=planner_config,
        executor_config=executor_config,
        tools=[web_search, data_analyzer, report_generator],
    )

    # Step 3: Run complex planning examples

    # Example tasks that require strategic planning
    complex_tasks = [
        "Research the current trends in AI and create a comprehensive report",
        "Analyze the impact of climate change on technology development and provide recommendations",
        "Create a learning plan for someone who wants to become a Python developer",
    ]

    for _i, task in enumerate(complex_tasks, 1):
        # The agent will first create a plan
        await agent.arun(task)

        # Small pause between tasks
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
