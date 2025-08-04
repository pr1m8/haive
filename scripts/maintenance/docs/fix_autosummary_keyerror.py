#!/usr/bin/env python3
"""Fix autosummary KeyError by removing problematic files and fixing imports."""
from __future__ import annotations

from pathlib import Path


def main():
    """Main function to fix documentation build errors."""
    project_root = Path(__file__).parent

    # 1. Remove problematic file with spaces and parentheses
    problematic_file = (
        project_root
        / "packages/haive-games/src/haive/games/core/game/containers/containers_tilebag (1).py"
    )
    if problematic_file.exists():
        problematic_file.unlink()
    else:
        passed")

    # 2. Fix imports in container.py
    container_file = (
        project_root
        / "packages/haive-games/src/haive/games/core/game/containers/container.py"
    )
    if container_file.exists():

        with open(container_file) as f:
            content = f.read()

        # Check if imports are already fixed
        if "import uuid" not in content:
            # Add missing imports at the top
            imports_to_add = """import uuid
import random
from typing import Callable, Generic, TypeVar

"""

            # Find the first import or class definition
            lines = content.split("\n")
            insert_pos = 0

            for i, line in enumerate(lines):
                if line.startswith(("from typing import", "from pydantic")):
                    insert_pos = i
                    break

            # Insert the new imports
            new_lines = (
                lines[:insert_pos]
                + imports_to_add.strip().split("\n")
                + [""]
                + lines[insert_pos:]
            )

            # Also need to define T before using it
            # Find where Generic[T] is first used
            for i, line in enumerate(new_lines):
                if "Generic[T]" in line and "T = TypeVar" not in "\n".join(
                    new_lines[:i]
                ):
                    # Insert T definition before this line
                    new_lines.insert(i, "T = TypeVar('T')")
                    new_lines.insert(i + 1, "")
                    break

            # Write back the fixed content
            with open(container_file, "w") as f:
                f.write("\n".join(new_lines))

        else:
            passpy")

    # 3. Search for any other files with problematic names
    games_path = project_root / "packages/haive-games/src/haive/games"

    problematic_count = 0
    for path in games_path.rglob("*.py"):
        filename = path.name
        # Check for spaces, parentheses, or other problematic characters
        if " " in filename or "(" in filename or ")" in filename:
            problematic_count += 1

    if problematic_count == 0:
        pass")

    # 4. Create/update __init__.py files to ensure proper imports
    containers_dir = (
        project_root / "packages/haive-games/src/haive/games/core/game/containers"
    )
    init_file = containers_dir / "__init__.py"

    if not init_file.exists():
        init_content = '''"""Container classes for game pieces."""

from .base import GamePieceContainer
from .container import Deck, TileBag, PlayerHand
from .deck import StandardDeck

__all__ = [
    "GamePieceContainer",
    "Deck",
    "TileBag",
    "PlayerHand",
    "StandardDeck",
]
'''
        with open(init_file, "w") as f:
            f.write(init_content)



if __name__ == "__main__":
    main()
