"""Demo 45: Flow Free.

Tests: FlowFreeAgent - single-player path puzzle
"""

import asyncio
import sys

sys.path.insert(0, ".")
from dotenv import load_dotenv

load_dotenv()


async def main():
    print("=" * 60)
    print("Demo 45: Flow Free")
    print("=" * 60)
    from haive.games.single_player.flow_free.agent import FlowFreeAgent
    from haive.games.single_player.flow_free.config import FlowFreeConfig

    try:
        config = FlowFreeConfig(enable_analysis=False, visualize=False)
    except Exception:
        config = FlowFreeConfig()
    agent = FlowFreeAgent(config)
    print(f"[OK] Agent: {type(agent).__name__}, App: {type(agent.app).__name__}")
    print("[OK] Flow Free demo complete")


if __name__ == "__main__":
    asyncio.run(main())
