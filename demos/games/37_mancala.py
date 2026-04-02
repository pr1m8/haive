"""Demo 37: Mancala.

Tests: MancalaAgent - seed-sowing board game
"""

import asyncio
import sys

sys.path.insert(0, ".")
from dotenv import load_dotenv

load_dotenv()


async def main():
    print("=" * 60)
    print("Demo 37: Mancala")
    print("=" * 60)
    from haive.games.mancala.agent import MancalaAgent
    from haive.games.mancala.config import MancalaConfig

    config = MancalaConfig(enable_analysis=False, visualize=False)
    agent = MancalaAgent(config)
    print(f"[OK] Agent: {type(agent).__name__}, App: {type(agent.app).__name__}")
    print("[OK] Mancala demo complete")


if __name__ == "__main__":
    asyncio.run(main())
