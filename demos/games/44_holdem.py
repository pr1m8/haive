"""Demo 44: Texas Hold'em.

Tests: HoldemGameAgent - poker variant
"""

import asyncio
import sys

sys.path.insert(0, ".")
from dotenv import load_dotenv

load_dotenv()


async def main():
    print("=" * 60)
    print("Demo 44: Texas Hold'em")
    print("=" * 60)
    from haive.games.hold_em.config import HoldemGameAgentConfig
    from haive.games.hold_em.game_agent import HoldemGameAgent

    try:
        config = HoldemGameAgentConfig(enable_analysis=False, visualize=False)
    except Exception:
        config = HoldemGameAgentConfig()
    agent = HoldemGameAgent(config)
    print(f"[OK] Agent: {type(agent).__name__}, App: {type(agent.app).__name__}")
    print("[OK] Hold'em demo complete")


if __name__ == "__main__":
    asyncio.run(main())
