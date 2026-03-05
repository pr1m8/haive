"""Demo 15: Go Agent.

Tests: GoAgent from haive-games
"""

import asyncio
import sys
sys.path.insert(0, ".")

from dotenv import load_dotenv
load_dotenv()

from haive.core.engine.aug_llm import AugLLMConfig


async def main():
    print("=" * 60)
    print("Demo 15: Go Agent")
    print("=" * 60)

    try:
        from haive.games.go.agent import GoAgent
        print("[OK] GoAgent imported")
    except ImportError as e:
        print(f"[BROKEN] Import failed: {e}")
        return

    try:
        from haive.games.go.config import GoAgentConfig
        config = GoAgentConfig()
        agent = GoAgent(config)
        print(f"[OK] Instantiated GoAgent")
    except Exception as e:
        print(f"[BROKEN] Instantiation failed: {e}")

    print("\n[OK] GoAgent demo complete")


if __name__ == "__main__":
    asyncio.run(main())
