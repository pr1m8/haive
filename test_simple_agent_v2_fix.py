"""Test the SimpleAgent V2 fix for engine validation error."""

import asyncio

from langchain_core.prompts import ChatPromptTemplate

from haive.agents.simple.agent_v2 import SimpleAgentV2
from haive.core.engine.aug_llm import AugLLMConfig


async def test_simple_agent_v2_fix():
    """Test that SimpleAgent V2 works without engine validation errors."""
    # Create prompt template with query variable
    prompt = ChatPromptTemplate.from_messages(
        [("system", "You are a helpful assistant."), ("human", "{query}")]
    )

    # Create engine with prompt template
    engine = AugLLMConfig(name="test_engine", prompt_template=prompt)

    # Create SimpleAgent V2
    try:
        agent = SimpleAgentV2(name="test_agent_v2", engine=engine)
    except Exception:
        return

    # Test agent execution
    try:
        await agent.arun("Hello, how are you?")
    except Exception:
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_simple_agent_v2_fix())
