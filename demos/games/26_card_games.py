"""Demo 26: Card & Strategy Game Agents.

Tests: Card games, social deduction, strategy games
"""

import asyncio
import importlib
import sys
sys.path.insert(0, ".")

from dotenv import load_dotenv
load_dotenv()


async def main():
    print("=" * 60)
    print("Demo 26: Card & Strategy Game Agents")
    print("=" * 60)

    game_modules = [
        # Card games
        ("blackjack", "haive.games.cards.standard.blackjack.agent"),
        ("bs", "haive.games.cards.standard.bs.agent"),
        ("hold_em", "haive.games.hold_em.agent"),
        ("poker", "haive.games.poker.agent"),
        # Strategy
        ("battleship", "haive.games.battleship.agent"),
        ("risk", "haive.games.risk.agent"),
        ("monopoly", "haive.games.monopoly.agent"),
        ("mastermind", "haive.games.mastermind.agent"),
        ("clue", "haive.games.clue.agent"),
        # Social deduction
        ("among_us", "haive.games.among_us.agent"),
        ("mafia", "haive.games.mafia.agent"),
        ("debate", "haive.games.debate.agent"),
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

    print(f"\n  Card & strategy games: {ok}/{ok+broken} OK")
    print("\n[OK] Card & strategy game agents demo complete")


if __name__ == "__main__":
    asyncio.run(main())
