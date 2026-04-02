"""Demo 33: Checkers.

Tests: CheckersAgent - classic draughts game
"""

import asyncio
import sys

sys.path.insert(0, ".")
from dotenv import load_dotenv

load_dotenv()


async def main():
    print("=" * 60)
    print("Demo 33: Checkers")
    print("=" * 60)

    from haive.games.checkers.agent import CheckersAgent
    from haive.games.checkers.config import CheckersAgentConfig

    config = CheckersAgentConfig(enable_analysis=False, visualize=False)
    agent = CheckersAgent(config)
    print(f"[OK] Agent: {type(agent).__name__}")
    print(f"[OK] App: {type(agent.app).__name__}")
    print("[OK] Checkers demo complete")


if __name__ == "__main__":
    asyncio.run(main())
