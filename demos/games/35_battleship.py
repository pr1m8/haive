"""Demo 35: Battleship.

Tests: BattleshipAgent - naval strategy game
"""

import asyncio
import sys

sys.path.insert(0, ".")
from dotenv import load_dotenv

load_dotenv()


async def main():
    print("=" * 60)
    print("Demo 35: Battleship")
    print("=" * 60)
    from haive.games.battleship.agent import BattleshipAgent
    from haive.games.battleship.config import BattleshipAgentConfig

    config = BattleshipAgentConfig(enable_analysis=False, visualize=False)
    agent = BattleshipAgent(config)
    print(f"[OK] Agent: {type(agent).__name__}, App: {type(agent.app).__name__}")
    print("[OK] Battleship demo complete")


if __name__ == "__main__":
    asyncio.run(main())
