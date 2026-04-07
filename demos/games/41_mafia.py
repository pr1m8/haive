"""Demo 41: Mafia.

Tests: MafiaAgent - social deduction game
"""

import asyncio
import sys

sys.path.insert(0, ".")
from dotenv import load_dotenv

load_dotenv()


async def main():
    print("=" * 60)
    print("Demo 41: Mafia")
    print("=" * 60)
    from haive.games.mafia.agent import MafiaAgent
    from haive.games.mafia.config import MafiaAgentConfig

    try:
        config = MafiaAgentConfig(enable_analysis=False, visualize=False)
    except Exception:
        config = MafiaAgentConfig()
    agent = MafiaAgent(config)
    print(f"[OK] Agent: {type(agent).__name__}, App: {type(agent.app).__name__}")
    print("[OK] Mafia demo complete")


if __name__ == "__main__":
    asyncio.run(main())
