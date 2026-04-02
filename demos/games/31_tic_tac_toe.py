"""Demo 31: Tic-Tac-Toe.

Tests: TicTacToeAgent - classic 3x3 grid game
"""

import asyncio
import sys

sys.path.insert(0, ".")
from dotenv import load_dotenv

load_dotenv()


async def main():
    print("=" * 60)
    print("Demo 31: Tic-Tac-Toe")
    print("=" * 60)

    from haive.games.tic_tac_toe.agent import TicTacToeAgent
    from haive.games.tic_tac_toe.config import TicTacToeConfig

    config = TicTacToeConfig(enable_analysis=False, visualize=False)
    agent = TicTacToeAgent(config)
    print(f"[OK] Agent: {type(agent).__name__}")
    print(f"[OK] App: {type(agent.app).__name__}")

    state = agent.state_manager.initialize()
    print(f"[OK] Board: {state.board}")
    print(f"[OK] Status: {state.game_status}")
    print("[OK] Tic-Tac-Toe demo complete")


if __name__ == "__main__":
    asyncio.run(main())
