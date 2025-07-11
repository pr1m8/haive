"""Test ReWOO Planner Agent."""

import asyncio
import logging
from typing import Any

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig
from langchain_core.tools import tool

from haive.agents.planning.rewoo.planner.agent import ReWOOPlannerAgent

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Create mock tools to test with
@tool
def mock_search_tool(query: str) -> str:
    """Search for information using a mock search tool."""
    return f"Mock search results for: {query}"


@tool
def mock_finance_tool(symbol: str) -> str:
    """Get financial information using a mock finance tool."""
    return f"Mock financial data for: {symbol}"


@tool
def mock_news_tool(topic: str) -> str:
    """Get news information using a mock news tool."""
    return f"Mock news about: {topic}"


async def test_rewoo_planner():
    """Test the ReWOO planner agent."""

    # Create mock tools list
    tools = [mock_search_tool, mock_finance_tool, mock_news_tool]

    # Create planner with mock tools
    planner = ReWOOPlannerAgent(
        name="test_planner",
        engine=AugLLMConfig(llm_config=AzureLLMConfig(model="gpt-4"), temperature=0.7),
        tools=tools,
    )

    # Test query
    query = "What is the current stock price of Apple (AAPL) and what are the latest news about the company?"


    try:
        # Generate plan
        plan = await planner.create_plan(query)

        if plan.evidence_map:
            pass

        for i, step in enumerate(plan.steps, 1):
            if step.evidence:
                pass
            if step.tool_call:
                if hasattr(step.tool_call, "arguments"):
                    pass

        if plan.evidence_map:
            for eid, evidence in plan.evidence_map.items():

        return plan

    except Exception as e:
        import traceback

        traceback.print_exc()
        return None


if __name__ == "__main__":
    asyncio.run(test_rewoo_planner())
