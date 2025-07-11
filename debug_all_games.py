#!/usr/bin/env python3
"""Comprehensive diagnostic script for all haive.games imports.

This script will:
1. Test importing each game individually
2. Capture full traceback for failures
3. Analyze the errors and suggest fixes
4. Test which games can be added to __all__
"""

import ast
import importlib
import sys
import traceback
from pathlib import Path
from typing import Any, Dict, List, Tuple

# Add package paths
project_root = Path(__file__).parent
packages_dir = project_root / "packages"

for package_dir in packages_dir.glob("haive-*"):
    src_dir = package_dir / "src"
    if src_dir.exists():
        sys.path.insert(0, str(src_dir))

# Common import error patterns and their fixes
ERROR_PATTERNS = {
    "cannot import name 'create_llm_config'": {
        "description": "Missing function that doesn't exist in haive.core.models.llm",
        "fix": "Remove the import or implement the function locally",
    },
    "cannot import name 'computed_field'": {
        "description": "Missing Pydantic v2 import",
        "fix": "Add 'computed_field' to pydantic imports",
    },
    "name '.*' is not defined": {
        "description": "Missing type import",
        "fix": "Add the missing type to imports (e.g., Dict, Optional, List)",
    },
    "Unable to serialize unknown type": {
        "description": "Pydantic serialization error with class objects",
        "fix": "Use default_factory and exclude=True for complex fields",
    },
    "No module named": {
        "description": "Missing module or incorrect import path",
        "fix": "Check if module exists and fix import path",
    },
}


def analyze_error(error_str: str, tb_str: str) -> dict[str, str]:
    """Analyze error and provide specific fix suggestions."""
    import re

    analysis = {
        "error_type": (
            type(error_str).__name__ if hasattr(error_str, "__class__") else "Unknown"
        ),
        "error_message": str(error_str),
        "suggested_fix": "Unknown error pattern",
        "specific_action": "",
    }

    # Check each pattern
    for pattern, info in ERROR_PATTERNS.items():
        if re.search(pattern, str(error_str)):
            analysis["suggested_fix"] = info["description"]
            analysis["specific_action"] = info["fix"]

            # Extract specific details
            if "cannot import name" in str(error_str):
                match = re.search(r"cannot import name '(\w+)'", str(error_str))
                if match:
                    missing_import = match.group(1)
                    analysis["specific_action"] = (
                        f"Remove or fix import of '{missing_import}'"
                    )

                    # Find the file causing the issue
                    import_match = re.search(r"from ([\w\.]+) import", tb_str)
                    if import_match:
                        module = import_match.group(1)
                        analysis["specific_action"] += f" from module '{module}'"

            elif "name '.*' is not defined" in pattern:
                match = re.search(r"name '(\w+)' is not defined", str(error_str))
                if match:
                    missing_name = match.group(1)
                    analysis["specific_action"] = f"Add '{missing_name}' to imports"

                    # Common type imports
                    if missing_name in [
                        "Dict",
                        "List",
                        "Optional",
                        "Union",
                        "Any",
                        "Tuple",
                    ]:
                        analysis[
                            "specific_action"
                        ] += f" - Add to typing imports: from typing import {missing_name}"

            break

    # Extract file location from traceback
    file_match = re.search(r'File "([^"]+)", line (\d+)', tb_str)
    if file_match:
        analysis["error_file"] = file_match.group(1)
        analysis["error_line"] = file_match.group(2)

    return analysis


def find_import_chain(tb_str: str) -> list[str]:
    """Extract the import chain from traceback."""
    import re

    chain = []

    # Find all file references in traceback
    for match in re.finditer(
        r'File "([^"]+)", line \d+, in (.+)\n.*\n.*?(from .+ import .+|import .+)',
        tb_str,
        re.MULTILINE,
    ):
        file_path = match.group(1)
        if "haive/games" in file_path:
            chain.append(file_path)

    return chain


def test_game_import(game_name: str) -> tuple[bool, Any, str, dict[str, str]]:
    """Test importing a specific game module.

    Returns:
        Tuple of (success, module_or_error, full_traceback, analysis)
    """
    try:
        module = importlib.import_module(f"haive.games.{game_name}")
        return True, module, "", {}
    except Exception as e:
        tb = traceback.format_exc()
        analysis = analyze_error(e, tb)
        return False, e, tb, analysis


def get_game_directories() -> list[str]:
    """Get all game directories in haive.games."""
    games_dir = packages_dir / "haive-games" / "src" / "haive" / "games"
    game_dirs = []

    if games_dir.exists():
        for item in sorted(games_dir.iterdir()):
            if item.is_dir() and not item.name.startswith("_"):
                # Skip non-game directories
                if item.name not in [
                    "api",
                    "base",
                    "base_v2",
                    "board",
                    "cards",
                    "core",
                    "framework",
                    "logs",
                    "multi_player",
                    "resources",
                    "single_player",
                    "utils",
                ]:
                    game_dirs.append(item.name)

    return game_dirs


def check_game_exports(game_name: str, module: Any) -> dict[str, Any]:
    """Check what a successfully imported game module exports."""
    exports = {
        "has_all": hasattr(module, "__all__"),
        "all_contents": getattr(module, "__all__", []),
        "classes": [],
        "functions": [],
        "other": [],
    }

    # Analyze module contents
    for name in dir(module):
        if not name.startswith("_"):
            obj = getattr(module, name)
            if isinstance(obj, type):
                exports["classes"].append(name)
            elif callable(obj):
                exports["functions"].append(name)
            else:
                exports["other"].append(name)

    # Look for common game components
    common_components = ["Agent", "Config", "State", "Game"]
    exports["game_components"] = [
        name
        for name in exports["classes"]
        if any(comp in name for comp in common_components)
    ]

    return exports


def main():
    """Run comprehensive game import diagnostics."""

    # Get all game directories
    games = get_game_directories()
    for game in games:
        pass


    results = {}
    successful_games = []
    failed_games = []

    for game in games:

        success, result, tb, analysis = test_game_import(game)

        if success:
            successful_games.append(game)

            # Check exports
            exports = check_game_exports(game, result)
            if exports["has_all"]:
                pass

            results[game] = {"status": "success", "module": result, "exports": exports}
        else:
            failed_games.append(game)


            if "error_file" in analysis:

            # Show import chain
            chain = find_import_chain(tb)
            if chain:
                for i, file in enumerate(chain):
                    pass

            # Show relevant traceback section
            tb_lines = tb.split("\n")
            for i, line in enumerate(tb_lines):
                if "haive/games" in line and i < len(tb_lines) - 5:
                    for j in range(max(0, i - 1), min(len(tb_lines), i + 5)):
                        pass
                    break

            results[game] = {
                "status": "failed",
                "error": str(result),
                "analysis": analysis,
                "traceback": tb,
            }


    for game in successful_games:
        pass")

    for game in failed_games:
        pass")



    # Add successful game exports
    for game in successful_games:
        if game in results and results[game]["exports"]["game_components"]:
            for component in results[game]["exports"]["game_components"]:
                pass



    fix_priority = {}
    for game, result in results.items():
        if result["status"] == "failed":
            error_type = result["analysis"]["suggested_fix"]
            if error_type not in fix_priority:
                fix_priority[error_type] = []
            fix_priority[error_type].append(
                {
                    "game": game,
                    "action": result["analysis"]["specific_action"],
                    "file": result["analysis"].get("error_file", "Unknown"),
                }
            )

    for error_type, fixes in fix_priority.items():
        for fix in fixes:
            if fix["file"] != "Unknown":
                pass

    # Save detailed results
    import json

    output_file = project_root / "game_import_diagnostics.json"

    # Convert results to JSON-serializable format
    json_results = {}
    for game, result in results.items():
        json_results[game] = {
            "status": result["status"],
            "error": result.get("error", ""),
            "analysis": result.get("analysis", {}),
            "exports": result.get("exports", {}),
        }

    with open(output_file, "w") as f:
        json.dump(json_results, f, indent=2)



if __name__ == "__main__":
    main()
