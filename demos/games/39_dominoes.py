"""Demo 39: Dominoes.

Tests: DominoesAgent - tile-matching game
"""

import asyncio
import sys

sys.path.insert(0, ".")
from dotenv import load_dotenv

load_dotenv()


async def main():
    print("=" * 60)
    print("Demo 39: Dominoes")
    print("=" * 60)
    from haive.games.dominoes.agent import DominoesAgent
    from haive.games.dominoes.config import DominoesAgentConfig

    config = DominoesAgentConfig(enable_analysis=False, visualize=False)
    agent = DominoesAgent(config)
    print(f"[OK] Agent: {type(agent).__name__}, App: {type(agent.app).__name__}")
    print("[OK] Dominoes demo complete")


if __name__ == "__main__":
    asyncio.run(main())
