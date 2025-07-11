#!/usr/bin/env python3
"""Diagnose haive.games import issues."""

import importlib
import sys
import traceback
from pathlib import Path

# Add package paths
project_root = Path(__file__).parent
packages_dir = project_root / "packages"

for package_dir in packages_dir.glob("haive-*"):
    src_dir = package_dir / "src"
    if src_dir.exists():
        sys.path.insert(0, str(src_dir))


# Test basic import
try:
    import haive.games

except Exception as e:
    traceback.print_exc()

# Test submodules

games_to_test = [
    "haive.games.chess",
    "haive.games.tic_tac_toe",
    "haive.games.connect4",
    "haive.games.among_us",
    "haive.games.checkers",
]

for game in games_to_test:
    try:
        mod = importlib.import_module(game)
    except Exception as e:
        pass")

# Check what's in __all__

try:
    if hasattr(haive.games, "__all__"):
        pass
    else:
        pass
except:
    pass

# List actual game directories

games_dir = packages_dir / "haive-games" / "src" / "haive" / "games"
if games_dir.exists():
    for item in sorted(games_dir.iterdir()):
        if item.is_dir() and not item.name.startswith("_"):
            pass
