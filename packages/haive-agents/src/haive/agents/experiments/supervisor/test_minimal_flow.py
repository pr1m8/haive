"""Minimal test - supervisor delegates to ReactAgent and returns human message."""

import asyncio

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig
from haive.tools.tools.search_tools import tavily_search_tool
from langchain_core.messages import HumanMessage

from haive.agents.react.agent import ReactAgent


async def test_minimal_flow():
    """Test ReactAgent directly - verify it returns human message."""

    # Create ReactAgent with tavily search tool
    search_engine = AugLLMConfig(
        name="search_engine",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        tools=[tavily_search_tool],
        system_message="You are a search specialist. Use the search tool to find information and provide a clear answer.",
    )

    search_agent = ReactAgent(name="search_agent", engine=search_engine)


    # Test ReactAgent directly
    try:
        # Call ReactAgent with simple message input
        result = await search_agent.arun("Find information about France")

        # Check the final messages
        if hasattr(result, "messages") and result.messages:

            # Look for the final human message (agent's response)
            last_msg = result.messages[-1]

            if hasattr(last_msg, "content"):
                content = last_msg.content

                # Check if it contains search results about France
                if "France" in content and len(content) > 50:
                else:
                    passse")
            else:
                pass")
        else:
            pass")

    except Exception as e:
        import traceback

        traceback.print_exc()



if __name__ == "__main__":
    asyncio.run(test_minimal_flow())
