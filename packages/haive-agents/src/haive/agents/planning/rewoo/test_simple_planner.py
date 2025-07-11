"""Test simple ReWOO plan generation with SimpleAgent."""

import asyncio
import logging
from typing import Any

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig
from langchain_core.tools import tool

from haive.agents.planning.rewoo.models import ReWOOPlan
from haive.agents.planning.rewoo.planner.prompts import REWOO_PLANNING_TEMPLATE
from haive.agents.simple.agent import SimpleAgent

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Create mock tools
@tool
def search_tool(query: str) -> str:
    """Search for information."""
    return f"Search results for: {query}"


@tool
def finance_tool(symbol: str) -> str:
    """Get financial information."""
    return f"Financial data for: {symbol}"


@tool
def news_tool(topic: str) -> str:
    """Get news information."""
    return f"News about: {topic}"


async def test_simple_rewoo_planner():
    """Test simple ReWOO plan generation using basic SimpleAgent."""
    # Create simple agent with structured output for ReWOO plans
    agent = SimpleAgent(
        name="rewoo_planner",
        engine=AugLLMConfig(
            llm_config=AzureLLMConfig(model="gpt-4"),
            temperature=0.7,
            structured_output_model=ReWOOPlan,
            structured_output_version="v2",  # Use v2 for tool call parsing
        ),
        tools=[search_tool, finance_tool, news_tool],
    )

    # Test query
    query = "What is the current stock price of Apple (AAPL) and what are the latest news about the company?"

    try:
        # Format the prompt with available tools
        tool_options = [t.name for t in [search_tool, finance_tool, news_tool]]
        formatted_prompt = REWOO_PLANNING_TEMPLATE.format_messages(
            tool_options=tool_options, query=query
        )

        # Run agent with the formatted prompt
        result = await agent.arun(formatted_prompt)

        # Check if we got a structured ReWOO plan
        if hasattr(result, "name") and hasattr(result, "steps"):

            for _i, step in enumerate(result.steps, 1):
                if step.tool_call:
                    pass
        else:

            # Try to extract plan from different possible locations
            if hasattr(result, "rewooplan"):
                pass
            if hasattr(result, "re_woo_plan"):
                pass
            if hasattr(result, "structured_output"):
                pass

    except Exception:
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_simple_rewoo_planner())
