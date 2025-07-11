"""Test ReWOO Agent with debug output."""

import asyncio
import logging
from typing import Any

from haive.core.engine.aug_llm import AugLLMConfig

# Import real tools from haive.tools
from haive.tools.tools.search_tools import tavily_qna, tavily_search_tool
from haive.tools.tools.yfinance_tool import yfinance_news_tool

from haive.agents.planning.rewoo.agent import ReWOOAgent
from haive.agents.planning.rewoo.models import ReWOOPlan

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_rewoo_agent():
    """Test ReWOO agent with debug output."""

    # Create agent
    from haive.core.models.llm.base import AzureLLMConfig

    agent = ReWOOAgent(
        name="test_rewoo_agent",
        engine=AugLLMConfig(llm_config=AzureLLMConfig(model="gpt-4"), temperature=0.7),
        tools=[tavily_search_tool, tavily_qna, yfinance_news_tool],
    )

    # Test query that should require multiple evidence steps
    query = "What is the current stock price of Apple (AAPL) and what are the latest news about the company?"


    try:
        # Run with debug - shorter output
        result = await agent.arun(query, debug=False)


        # Check if we got a structured ReWOO plan
        if hasattr(result, "name") and hasattr(result, "steps"):

            for i, step in enumerate(result.steps, 1):
                if step.evidence:
                    pass
                if step.tool_call:
                    pass

            for eid, evidence in result.evidence_map.items():
        else:
            if isinstance(result, str):
                pass

            # Debug - check what's in the result
            if hasattr(result, "__dict__"):
                for attr in dir(result):
                    if not attr.startswith("_"):
                        try:
                            val = getattr(result, attr)
                        except:
                            pass

            # Check messages for tool calls
            if hasattr(result, "messages"):
                for i, msg in enumerate(result.messages):
                    if hasattr(msg, "content"):
                        pass
                    if hasattr(msg, "tool_calls") and msg.tool_calls:
                        for tc in msg.tool_calls:
                            if tc["name"] == "ReWOOPlan":
                                plan_args = tc["args"]
                                if "steps" in plan_args:
                                    for j, step in enumerate(plan_args["steps"], 1):
                                        if "tool_call" in step:
                                            pass

    except Exception as e:
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_rewoo_agent())
