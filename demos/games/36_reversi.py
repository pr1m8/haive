"""Demo 36: Reversi.

Tests: ReversiAgent - disc-flipping strategy game (Othello)
"""

import asyncio
import sys

sys.path.insert(0, ".")
from dotenv import load_dotenv

load_dotenv()


async def main():
    print("=" * 60)
    print("Demo 36: Reversi")
    print("=" * 60)
    from haive.games.reversi.agent import ReversiAgent
    from haive.games.reversi.config import ReversiConfig

    config = ReversiConfig(enable_analysis=False, visualize=False)
    agent = ReversiAgent(config)
    print(f"[OK] Agent: {type(agent).__name__}, App: {type(agent.app).__name__}")
    print("[OK] Reversi demo complete")


if __name__ == "__main__":
    asyncio.run(main())
