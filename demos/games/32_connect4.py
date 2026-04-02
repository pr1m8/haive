"""Demo 32: Connect 4.

Tests: Connect4Agent - four-in-a-row strategy game
"""

import asyncio
import sys

sys.path.insert(0, ".")
from dotenv import load_dotenv

load_dotenv()


async def main():
    print("=" * 60)
    print("Demo 32: Connect 4")
    print("=" * 60)

    from haive.games.connect4.agent import Connect4Agent
    from haive.games.connect4.config import Connect4AgentConfig

    config = Connect4AgentConfig(enable_analysis=False, visualize=False)
    agent = Connect4Agent(config)
    print(f"[OK] Agent: {type(agent).__name__}")
    print(f"[OK] App: {type(agent.app).__name__}")

    state = agent.state_manager.initialize()
    print(f"[OK] Board size: {len(state.board)}x{len(state.board[0])}")
    print(f"[OK] Status: {state.game_status}")
    print("[OK] Connect 4 demo complete")


if __name__ == "__main__":
    asyncio.run(main())
