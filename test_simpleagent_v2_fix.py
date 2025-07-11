#!/usr/bin/env python3
"""Test SimpleAgent v2 fix for engine validation error."""

import asyncio

from haive.agents.simple.agent_v2 import SimpleAgentV2
from haive.core.engine.aug_llm import AugLLMConfig


async def test_simpleagent_v2():
    """Test SimpleAgent v2 with the engine fix."""

    # Create a simple AugLLMConfig (defaults to gpt-4o-mini)
    config = AugLLMConfig(temperature=0.7)

    # Create SimpleAgent v2
    agent = SimpleAgentV2(name="TestAgent_v2", engine=config)


    # Test simple query
    try:
        result = await agent.arun("Hello! What's 2+2?")
        return True
    except Exception as e:
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(test_simpleagent_v2())
    if success:
        pass!")
    else:
        passs")
