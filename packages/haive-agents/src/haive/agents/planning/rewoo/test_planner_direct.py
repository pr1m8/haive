"""Direct test of ReWOO planner with v2 structured output."""

import asyncio
import logging
from typing import Any

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig
from langchain_core.utils.function_calling import convert_pydantic_to_openai_tool

from haive.agents.planning.rewoo.models import ReWOOPlan
from haive.agents.planning.rewoo.planner.prompts import REWOO_PLANNING_TEMPLATE

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_direct_rewoo_planning():
    """Test ReWOO plan generation directly with AugLLMConfig."""

    # Format the prompt with available tools
    available_tools = ["tavily_search_tool", "tavily_qna", "yahoo_finance_news"]
    planning_prompt = REWOO_PLANNING_TEMPLATE.format(tools=str(available_tools))

    # Create engine with ReWOO planning configuration - v2 without tool_choice
    planning_engine = AugLLMConfig(
        name="planning_engine",
        llm_config=AzureLLMConfig(model="gpt-4"),
        temperature=0.7,
        structured_output_model=ReWOOPlan,
        structured_output_version="v2",
        system_message=planning_prompt,
    )

    # Test query
    query = "What is the current stock price of Apple (AAPL) and what are the latest news about the company?"


    try:
        # Invoke the engine directly
        from langchain_core.messages import HumanMessage

        result = await planning_engine.ainvoke(
            {"messages": [HumanMessage(content=query)]}
        )


        # Check if we got tool calls
        if hasattr(result, "tool_calls") and result.tool_calls:
            for tc in result.tool_calls:
                if tc["name"] == "ReWOOPlan":
                    plan_args = tc["args"]
                    if "steps" in plan_args:
                        for j, step in enumerate(plan_args["steps"], 1):
                            if "tool_call" in step:
                                pass
                else:
                    pass
        else:

    except Exception as e:
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_direct_rewoo_planning())
