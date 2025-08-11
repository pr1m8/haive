#!/usr/bin/env python3
"""Script to check which games are currently working."""

import importlib
import sys
from pathlib import Path

# Add the games package to the path
games_path = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(games_path))


def test_game_import(game_name):
    """Test if a game can be imported and has the basic requirements."""
    try:
        # Try to import the game module
        module = importlib.import_module(f"haive.games.{game_name}")

        # Check if it has an agent
        agent_classes = [
            attr
            for attr in dir(module)
            if attr.endswith("Agent") and not attr.startswith("_")
        ]
        config_classes = [
            attr
            for attr in dir(module)
            if attr.endswith("Config") and not attr.startswith("_")
        ]

        if not agent_classes:
            return False, "No agent class found"

        if not config_classes:
            return False, "No config class found"

        return True, f"Agent: {agent_classes[0]}, Config: {config_classes[0]}"

    except Exception as e:
        return False, str(e)


def main():
    """Check all games in the games directory."""
    games_dir = Path(__file__).parent.parent.parent / "src" / "haive" / "games"

    working_games = []
    broken_games = []

    # Get all game directories
    for game_dir in games_dir.iterdir():
        if (
            game_dir.is_dir()
            and not game_dir.name.startswith("_")
            and game_dir.name
            not in [
                "core",
                "api",
                "logs",
                "resources",
                "utils",
                "board",
                "framework",
                "cards",
            ]
        ):
            game_name = game_dir.name

            # Check if the game has an __init__.py file
            init_file = game_dir / "__init__.py"
            if not init_file.exists():
                broken_games.append((game_name, "No __init__.py file"))
                continue

            success, message = test_game_import(game_name)

            if success:
                working_games.append((game_name, message))
            else:
                broken_games.append((game_name, message))

    for _i, (_game, _info) in enumerate(working_games, 1):
        pass

    for _i, (_game, _error) in enumerate(broken_games, 1):
        pass

    # Summary
    total = len(working_games) + len(broken_games)
    len(working_games) / total * 100 if total > 0 else 0


if __name__ == "__main__":
    main()
