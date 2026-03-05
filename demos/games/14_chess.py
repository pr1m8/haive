"""Demo 14: Chess Agent.

Tests: ChessAgent from haive-games
"""

import asyncio
import sys
sys.path.insert(0, ".")

from dotenv import load_dotenv
load_dotenv()

from haive.core.engine.aug_llm import AugLLMConfig


async def main():
    print("=" * 60)
    print("Demo 14: Chess Agent")
    print("=" * 60)

    try:
        from haive.games.chess.agent import ChessAgent
        print("[OK] ChessAgent imported")
    except ImportError as e:
        print(f"[BROKEN] Import failed: {e}")
        return

    try:
        from haive.games.chess.config import ChessConfig
        config = ChessConfig()
        agent = ChessAgent(config)
        print(f"[OK] Instantiated ChessAgent")
    except Exception as e:
        print(f"[BROKEN] Instantiation failed: {e}")

    print("\n[OK] ChessAgent demo complete")


if __name__ == "__main__":
    asyncio.run(main())
