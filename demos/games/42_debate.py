"""Demo 42: Debate.

Tests: DebateAgent - multi-agent structured debate
"""

import asyncio
import sys

sys.path.insert(0, ".")
from dotenv import load_dotenv

load_dotenv()


async def main():
    print("=" * 60)
    print("Demo 42: Debate")
    print("=" * 60)
    from haive.games.debate.agent import DebateAgent
    from haive.games.debate.config import DebateAgentConfig

    try:
        config = DebateAgentConfig(enable_analysis=False, visualize=False)
    except Exception:
        config = DebateAgentConfig()
    agent = DebateAgent(config)
    print(f"[OK] Agent: {type(agent).__name__}, App: {type(agent.app).__name__}")
    print("[OK] Debate demo complete")


if __name__ == "__main__":
    asyncio.run(main())
