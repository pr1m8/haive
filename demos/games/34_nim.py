"""Demo 34: Nim.

Tests: NimAgent - mathematical strategy game
"""

import asyncio
import sys

sys.path.insert(0, ".")
from dotenv import load_dotenv

load_dotenv()


async def main():
    print("=" * 60)
    print("Demo 34: Nim")
    print("=" * 60)
    from haive.games.nim.agent import NimAgent
    from haive.games.nim.config import NimConfig

    config = NimConfig(enable_analysis=False, visualize=False)
    agent = NimAgent(config)
    print(f"[OK] Agent: {type(agent).__name__}, App: {type(agent.app).__name__}")
    print("[OK] Nim demo complete")


if __name__ == "__main__":
    asyncio.run(main())
