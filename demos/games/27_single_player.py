"""Demo 27: Single Player Game Agents.

Tests: Wordle, Rubik's, Flow Free
"""

import asyncio
import importlib
import sys
sys.path.insert(0, ".")

from dotenv import load_dotenv
load_dotenv()


async def main():
    print("=" * 60)
    print("Demo 27: Single Player Game Agents")
    print("=" * 60)

    game_modules = [
        ("wordle", "haive.games.single_player.wordle.agent"),
        ("flow_free", "haive.games.single_player.flow_free.agent"),
        # rubiks is incomplete skeleton (missing config.py, cube_ops.py, engines.py)
    ]

    ok = broken = 0
    for name, module_path in game_modules:
        try:
            mod = importlib.import_module(module_path)
            classes = [c for c in dir(mod) if "Agent" in c and not c.startswith("_")]
            print(f"  [OK] {name:<20} {classes[:2]}")
            ok += 1
        except Exception as e:
            print(f"  [XX] {name:<20} {type(e).__name__}: {str(e)[:60]}")
            broken += 1

    print(f"\n  Single player games: {ok}/{ok+broken} OK")
    print("\n[OK] Single player game agents demo complete")


if __name__ == "__main__":
    asyncio.run(main())
