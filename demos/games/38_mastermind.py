"""Demo 38: Mastermind.

Tests: MastermindAgent - code-breaking logic game
"""

import asyncio
import sys

sys.path.insert(0, ".")
from dotenv import load_dotenv

load_dotenv()


async def main():
    print("=" * 60)
    print("Demo 38: Mastermind")
    print("=" * 60)
    from haive.games.mastermind.agent import MastermindAgent
    from haive.games.mastermind.config import MastermindConfig

    config = MastermindConfig(enable_analysis=False, visualize=False)
    agent = MastermindAgent(config)
    print(f"[OK] Agent: {type(agent).__name__}, App: {type(agent.app).__name__}")
    print("[OK] Mastermind demo complete")


if __name__ == "__main__":
    asyncio.run(main())
