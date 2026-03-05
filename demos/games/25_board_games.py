"""Demo 25: Board Game Agents.

Tests: All board game agents from haive-games
"""

import asyncio
import importlib
import sys
sys.path.insert(0, ".")

from dotenv import load_dotenv
load_dotenv()


async def main():
    print("=" * 60)
    print("Demo 25: Board Game Agents")
    print("=" * 60)

    game_modules = [
        ("chess", "haive.games.chess.agent"),
        ("go", "haive.games.go.agent"),
        ("checkers", "haive.games.checkers.agent"),
        ("tic_tac_toe", "haive.games.tic_tac_toe.agent"),
        ("connect4", "haive.games.connect4.agent"),
        ("reversi", "haive.games.reversi.agent"),
        ("mancala", "haive.games.mancala.agent"),
        ("nim", "haive.games.nim.agent"),
        ("dominoes", "haive.games.dominoes.agent"),
        ("fox_and_geese", "haive.games.fox_and_geese.agent"),
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

    print(f"\n  Board games: {ok}/{ok+broken} OK")
    print("\n[OK] Board game agents demo complete")


if __name__ == "__main__":
    asyncio.run(main())
