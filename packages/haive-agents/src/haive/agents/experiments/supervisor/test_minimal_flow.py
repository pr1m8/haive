"""Minimal test - supervisor delegates to ReactAgent and returns human message."""

import asyncio

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig
from haive.tools.tools.search_tools import tavily_search_tool
from langchain_core.messages import HumanMessage

from haive.agents.react.agent import ReactAgent


async def test_minimal_flow():
    """Test ReactAgent directly - verify it returns human message."""
    print("🔧 Testing ReactAgent search functionality...")

    # Create ReactAgent with tavily search tool
    search_engine = AugLLMConfig(
        name="search_engine",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        tools=[tavily_search_tool],
        system_message="You are a search specialist. Use the search tool to find information and provide a clear answer.",
    )

    search_agent = ReactAgent(name="search_agent", engine=search_engine)

    print(f"✅ Created ReactAgent: {search_agent.name}")
    print(f"📋 Agent tools: {len(search_agent.engine.tools)}")

    # Test ReactAgent directly
    print("\n1. Testing ReactAgent search...")
    try:
        # Call ReactAgent with simple message input
        result = await search_agent.arun("Find information about France")
        print(f"   Result type: {type(result)}")

        # Check the final messages
        if hasattr(result, "messages") and result.messages:
            print(f"   Total messages: {len(result.messages)}")

            # Look for the final human message (agent's response)
            last_msg = result.messages[-1]
            print(f"   Last message type: {type(last_msg).__name__}")

            if hasattr(last_msg, "content"):
                content = last_msg.content
                print(f"   Last message content (first 200 chars): {content[:200]}...")

                # Check if it contains search results about France
                if "France" in content and len(content) > 50:
                    print(
                        "   ✅ ReactAgent successfully returned detailed information!"
                    )
                    print(
                        f"   ✅ This is the human message the supervisor should return"
                    )
                else:
                    print("   ⚠️  Limited information in response")
            else:
                print("   ❌ No content in last message")
        else:
            print("   ❌ No messages in result")

    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback

        traceback.print_exc()

    print("\n🎉 ReactAgent test complete!")
    print("\nNext step: Create supervisor that:")
    print("- Has handoff_to_search_agent tool")
    print("- Calls this ReactAgent")
    print("- Returns the ReactAgent's final message as a human message")


if __name__ == "__main__":
    asyncio.run(test_minimal_flow())
