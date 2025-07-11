"""Test if real LLM calls provide token usage metadata."""

import asyncio

from haive.agents.simple.agent import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig


async def test_real_llm_token_metadata():
    """Test what metadata real LLM calls provide."""
    # Create agent with real LLM
    config = AugLLMConfig(
        temperature=0.1,
        max_tokens=50,
    )

    agent = SimpleAgent(name="llm_token_test", engine=config)

    # Make a real call and examine the raw response

    # Try to get the raw LLM response
    response = await agent.arun("What is 2 + 2?")

    # Check if the response has messages
    if hasattr(response, "messages"):
        for _i, msg in enumerate(response.messages):
            if hasattr(msg, "response_metadata"):
                pass
            if hasattr(msg, "usage_metadata"):
                pass

    # Try to access the agent's graph state
    if hasattr(agent, "graph") and hasattr(agent.graph, "get_state"):
        try:
            # This might require a thread_id or config
            thread_config = {"configurable": {"thread_id": "test-thread"}}
            agent.graph.get_state(thread_config)
        except Exception:
            pass

    # Try to access the engine directly
    if hasattr(agent.engine, "llm_config"):
        pass


async def test_direct_engine_call():
    """Test calling the engine directly to see token metadata."""
    from langchain_core.messages import HumanMessage

    config = AugLLMConfig(
        temperature=0.1,
        max_tokens=50,
    )

    # Try to call the engine directly
    try:
        # Create a runnable from the engine
        runnable = config.create_runnable()

        # Make a direct call
        messages = [HumanMessage(content="What is 2 + 2?")]
        result = await runnable.ainvoke({"messages": messages})

        # Check if result has token usage
        if hasattr(result, "response_metadata"):
            pass
        if hasattr(result, "usage_metadata"):
            pass

    except Exception:
        pass


async def main():
    """Run all tests."""
    try:
        await test_real_llm_token_metadata()
        await test_direct_engine_call()

    except Exception:
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
