"""Demo 28: Among Us.

Tests: AmongUsAgent - multi-player social deduction game
"""

import asyncio
import sys

sys.path.insert(0, ".")

from dotenv import load_dotenv

load_dotenv()


async def main():
    print("=" * 60)
    print("Demo 28: Among Us - Social Deduction Game")
    print("=" * 60)

    from haive.games.among_us.factory import create_among_us_game

    players = ["Alice", "Bob", "Charlie", "Dave", "Eve"]
    agent = create_among_us_game(player_names=players)
    print(f"[OK] Agent created: {type(agent).__name__}")
    print(f"[OK] App compiled: {type(agent.app).__name__}")

    # Initialize game
    state = agent.state_manager.initialize(player_names=players)
    roles = {p: s.role.value for p, s in state.player_states.items()}
    print(f"[OK] Game initialized: {len(players)} players")
    print(f"     Roles: {roles}")
    print(f"     Map: {state.map_name}")

    impostor = [p for p, r in roles.items() if r == "impostor"]
    print(f"     Impostor(s): {impostor}")

    # Show task assignments
    for p, s in state.player_states.items():
        tasks = [t.description for t in s.tasks[:2]]
        print(f"     {p}: {tasks}")

    print("\n[OK] Among Us demo complete")


if __name__ == "__main__":
    asyncio.run(main())
