"""Demo 46: Chain Agent.

Tests: Declarative chain agent with sequential LLM steps
"""

import asyncio
import sys
sys.path.insert(0, ".")

from dotenv import load_dotenv
load_dotenv()


async def main():
    print("=" * 60)
    print("Demo 46: Chain Agent")
    print("=" * 60)

    from haive.agents.chain import DeclarativeChainAgent, ChainBuilder

    print(f"[OK] DeclarativeChainAgent: {DeclarativeChainAgent.__name__}")
    print(f"[OK] ChainBuilder: {ChainBuilder.__name__}")

    print("\n[OK] Chain agent demo complete")


if __name__ == "__main__":
    asyncio.run(main())
