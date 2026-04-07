"""Demo 30: Social Deduction & Multi-Player Games.

Tests: Mafia, Debate, Clue
"""

import asyncio
import sys

sys.path.insert(0, ".")

from dotenv import load_dotenv

load_dotenv()


GAMES = [
    (
        "Mafia",
        "haive.games.mafia.agent",
        "MafiaAgent",
        "haive.games.mafia.config",
        "MafiaAgentConfig",
    ),
    (
        "Debate",
        "haive.games.debate.agent",
        "DebateAgent",
        "haive.games.debate.config",
        "DebateAgentConfig",
    ),
    (
        "Clue",
        "haive.games.clue.agent",
        "ClueAgent",
        "haive.games.clue.config",
        "ClueConfig",
    ),
    (
        "Hold'em",
        "haive.games.hold_em.game_agent",
        "HoldemGameAgent",
        "haive.games.hold_em.config",
        "HoldemGameAgentConfig",
    ),
]


async def main():
    print("=" * 60)
    print("Demo 30: Social Deduction & Multi-Player Games")
    print("=" * 60)

    import importlib

    for name, agent_mod, agent_cls, config_mod, config_cls in GAMES:
        try:
            a_mod = importlib.import_module(agent_mod)
            c_mod = importlib.import_module(config_mod)
            AgentClass = getattr(a_mod, agent_cls)
            ConfigClass = getattr(c_mod, config_cls)

            try:
                config = ConfigClass(enable_analysis=False, visualize=False)
            except Exception:
                config = ConfigClass()
            agent = AgentClass(config)
            print(f"[OK] {name}: {agent_cls} created, app={agent.app is not None}")
        except Exception as e:
            print(f"[FAIL] {name}: {type(e).__name__}: {str(e)[:80]}")

    print(f"\n[OK] Social deduction demo complete ({len(GAMES)} games)")


if __name__ == "__main__":
    asyncio.run(main())
