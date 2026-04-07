"""Demo 40: Fox and Geese.

Tests: FoxAndGeeseAgent - asymmetric hunt game
"""

import asyncio
import sys

sys.path.insert(0, ".")
from dotenv import load_dotenv

load_dotenv()


async def main():
    print("=" * 60)
    print("Demo 40: Fox and Geese")
    print("=" * 60)
    from haive.games.fox_and_geese.agent import FoxAndGeeseAgent
    from haive.games.fox_and_geese.config import FoxAndGeeseConfig

    config = FoxAndGeeseConfig(enable_analysis=False, visualize=False)
    agent = FoxAndGeeseAgent(config)
    print(f"[OK] Agent: {type(agent).__name__}, App: {type(agent.app).__name__}")
    print("[OK] Fox and Geese demo complete")


if __name__ == "__main__":
    asyncio.run(main())
