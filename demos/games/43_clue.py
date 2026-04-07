"""Demo 43: Clue.

Tests: ClueAgent - mystery deduction game (Cluedo)
"""

import asyncio
import sys

sys.path.insert(0, ".")
from dotenv import load_dotenv

load_dotenv()


async def main():
    print("=" * 60)
    print("Demo 43: Clue")
    print("=" * 60)
    from haive.games.clue.agent import ClueAgent
    from haive.games.clue.config import ClueConfig

    try:
        config = ClueConfig(enable_analysis=False, visualize=False)
    except Exception:
        config = ClueConfig()
    agent = ClueAgent(config)
    print(f"[OK] Agent: {type(agent).__name__}, App: {type(agent.app).__name__}")
    print("[OK] Clue demo complete")


if __name__ == "__main__":
    asyncio.run(main())
