"""Demo 29: Strategy Games.

Tests: TicTacToe, Connect4, Checkers, Nim, Battleship, Reversi, Mancala, Mastermind
"""

import asyncio
import sys

sys.path.insert(0, ".")

from dotenv import load_dotenv

load_dotenv()


GAMES = [
    (
        "TicTacToe",
        "haive.games.tic_tac_toe.agent",
        "TicTacToeAgent",
        "haive.games.tic_tac_toe.config",
        "TicTacToeConfig",
    ),
    (
        "Connect4",
        "haive.games.connect4.agent",
        "Connect4Agent",
        "haive.games.connect4.config",
        "Connect4AgentConfig",
    ),
    (
        "Checkers",
        "haive.games.checkers.agent",
        "CheckersAgent",
        "haive.games.checkers.config",
        "CheckersAgentConfig",
    ),
    ("Nim", "haive.games.nim.agent", "NimAgent", "haive.games.nim.config", "NimConfig"),
    (
        "Battleship",
        "haive.games.battleship.agent",
        "BattleshipAgent",
        "haive.games.battleship.config",
        "BattleshipAgentConfig",
    ),
    (
        "Reversi",
        "haive.games.reversi.agent",
        "ReversiAgent",
        "haive.games.reversi.config",
        "ReversiConfig",
    ),
    (
        "Mancala",
        "haive.games.mancala.agent",
        "MancalaAgent",
        "haive.games.mancala.config",
        "MancalaConfig",
    ),
    (
        "Mastermind",
        "haive.games.mastermind.agent",
        "MastermindAgent",
        "haive.games.mastermind.config",
        "MastermindConfig",
    ),
    (
        "Dominoes",
        "haive.games.dominoes.agent",
        "DominoesAgent",
        "haive.games.dominoes.config",
        "DominoesAgentConfig",
    ),
    (
        "Fox & Geese",
        "haive.games.fox_and_geese.agent",
        "FoxAndGeeseAgent",
        "haive.games.fox_and_geese.config",
        "FoxAndGeeseConfig",
    ),
]


async def main():
    print("=" * 60)
    print("Demo 29: Strategy Games")
    print("=" * 60)

    import importlib

    for name, agent_mod, agent_cls, config_mod, config_cls in GAMES:
        try:
            a_mod = importlib.import_module(agent_mod)
            c_mod = importlib.import_module(config_mod)
            AgentClass = getattr(a_mod, agent_cls)
            ConfigClass = getattr(c_mod, config_cls)

            config = ConfigClass(enable_analysis=False, visualize=False)
            agent = AgentClass(config)
            print(f"[OK] {name}: {agent_cls} created, app={agent.app is not None}")
        except Exception as e:
            print(f"[FAIL] {name}: {type(e).__name__}: {str(e)[:80]}")

    print(f"\n[OK] Strategy games demo complete ({len(GAMES)} games)")


if __name__ == "__main__":
    asyncio.run(main())
