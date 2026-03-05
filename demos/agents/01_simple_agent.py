"""Demo 01: SimpleAgent - Basic conversational agent.

Tests: import, instantiate, arun
"""

import asyncio
import sys
sys.path.insert(0, ".")

from dotenv import load_dotenv
load_dotenv()

from haive.core.engine.aug_llm import AugLLMConfig
from haive.agents.simple.agent import SimpleAgent


async def main():
    print("=" * 60)
    print("Demo 01: SimpleAgent")
    print("=" * 60)

    config = AugLLMConfig(
        temperature=0.7,
        system_message="You are a helpful assistant. Keep responses brief (1-2 sentences).",
    )

    agent = SimpleAgent(name="simple_demo", engine=config)
    print(f"[OK] Instantiated: {agent.name}")

    print("\n--- Running arun ---")
    result = await agent.arun("What is the capital of France? Reply in one sentence.")
    print(f"Result type: {type(result)}")

    # Extract content from result
    if hasattr(result, "messages"):
        content = result.messages[-1].content if result.messages else str(result)
    elif isinstance(result, dict) and "messages" in result:
        content = result["messages"][-1].content if result["messages"] else str(result)
    elif isinstance(result, str):
        content = result
    else:
        content = str(result)

    print(f"Response: {content[:200]}")
    print("\n[OK] SimpleAgent demo complete")


if __name__ == "__main__":
    asyncio.run(main())
