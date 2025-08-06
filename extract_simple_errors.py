#!/usr/bin/env python3
"""Simple extraction of import errors from log."""

import re
from collections import defaultdict


def extract_errors():
    """Extract errors using the text you provided."""

    # Based on your message, here are the main error categories
    errors = {
        "missing_core_modules": [
            "haive.core.schema.example",
            "haive.core.schema.prebuilt.messages.examples",
            "haive.core.types.tree_leaf",
            "haive.core.utils.debugkit.benchmarking.core",
            "haive.core.utils.debugkit.debugging",
            "haive.core.utils.parser_utils",
            "haive.core.utils.tool_list",
            "haive.core.utils.dev",
            "haive_agents_dep",
            "haive.core.utils.collections",
        ],
        "missing_dataflow_modules": [
            "haive.dataflow.registry.registry",
            "haive.dataflow.api.api",
            "haive.dataflow.api.models",
            "haive.api",
            "haive.dataflow.api.engine",
            "haive.dataflow.api.utils",
            "haive.dataflow.api.llms.api.llms",
            "haive.dataflow.api.middleware.auth.supabase",
            "haive.dataflow.api.middleware.config",
            "haive.dataflow.api.routes.utils",
            "haive.dataflow.api.routes.auth",
            "haive.dataflow.auth.config",
            "haive.dataflow.auth.auth",
            "haive.dataflow.db.db",
            "haive.dataflow.engine",
            "haive.dataflow.internal_websockets.auth",
            "haive.dataflow.persistence.config",
            "haive.dataflow.persistence.persistence",
            "haive.dataflow.providers.providers",
            "haive.dataflow.providers.utils",
            "haive.dataflow.registries.db",
            "haive.dataflow.registry.db.supabase",
            "game_router",
            "game_api",
            "haive_games",
        ],
        "missing_games_modules": [
            "haive.games.cards.blackjack",
            "haive.games.cards.bs",
            "haive.games.cards.card",
            "haive.games.models",
            "haive.games.simple",
            "game",  # This seems to be a circular/missing import
        ],
        "import_errors": [
            "cannot import name 'create_age' from 'haive.core.schema'",
            "cannot import name 'AgentRegistry' from 'haive.core.registry'",
            "cannot import name 'GameInfo' from 'haive.games.api'",
            "cannot import name 'update_availability_status' from 'haive.dataflow.registry.importers.litellm_importer'",
            "cannot import name 'SupabaseServerConfig' from 'haive.dataflow.config'",
            "cannot import name 'AmongUsConfig' from 'haive.games.among_us.config'",
            "cannot import name 'MonopolyPlayerAgent' from 'haive.games.monopoly.player_agent'",
            "cannot import name 'ChessAgentConfig' from 'haive.games.chess.config'",
            "cannot import name 'AugLLMEngine' from 'haive.core.engine.aug_llm'",
            "cannot import name 'GameState' from 'haive.games.core.base.state'",
            "cannot import name 'CardAction' from 'haive.games.core.components.cards.actions'",
            "cannot import name 'TCard' from 'haive.games.core.components.cards.base'",
            "cannot import name 'GameConfig' from 'haive.games.core.agent.game_config'",
        ],
        "type_errors": [
            "TypeError - All parameters must be present on typing.Generic",
            "TypeError - Cannot create a consistent method resolution order (MRO)",
            "TypeError - Can't instantiate abstract class AmongUsPromptGenerator",
            "TypeError - Can't instantiate abstract class BattleshipPromptGenerator",
            "TypeError - Can't instantiate abstract class CluePromptGenerator",
            "TypeError - Can't instantiate abstract class DebatePromptGenerator",
        ],
        "name_errors": [
            "NameError - name 'Any' is not defined",
            "NameError - name 'GamePiece' is not defined",
        ],
    }

    return errors


def create_fix_plan():
    """Create comprehensive fix plan."""

    errors = extract_errors()

    print("# Comprehensive Import Error Fix Plan")
    print()
    print("Based on documentation build errors, here are the fixes needed:")
    print()

    # 1. Mock imports for missing modules
    print("## 1. Add to autodoc_mock_imports")
    print()
    print("```python")
    print("autodoc_mock_imports.extend([")

    all_missing = (
        errors["missing_core_modules"]
        + errors["missing_dataflow_modules"]
        + errors["missing_games_modules"]
    )

    for module in sorted(set(all_missing)):
        print(f'    "{module}",')

    # Add individual missing names
    missing_names = set()
    for error in errors["import_errors"]:
        if "cannot import name" in error:
            # Extract the name
            import re

            match = re.search(r"cannot import name '([^']+)'", error)
            if match:
                missing_names.add(match.group(1))

    for name in sorted(missing_names):
        print(f'    "{name}",')

    # Add undefined names
    for error in errors["name_errors"]:
        if "name '" in error and "' is not defined" in error:
            match = re.search(r"name '([^']+)' is not defined", error)
            if match:
                missing_names.add(match.group(1))

    for name in sorted(missing_names):
        print(f'    "{name}",')

    print("])")
    print("```")
    print()

    # 2. Ignore patterns for problematic modules
    print("## 2. Add to autoapi_ignore")
    print()
    print("```python")
    print("autoapi_ignore.extend([")

    ignore_patterns = [
        # Dataflow is experimental
        '"**/dataflow/**/*.py"',
        # Abstract class instantiation errors
        '"**/configurable_config.py"',
        '"**/generic_engines.py"',
        # Card games with missing dependencies
        '"**/cards/standard/blackjack/**/*.py"',
        '"**/cards/standard/bs/**/*.py"',
        '"**/cards/standard/poker/**/*.py"',
        # Core game modules with circular imports
        '"**/core/game/**/*.py"',
        # Memory modules with metaclass conflicts
        '"**/memory/models_dir/**/*.py"',
        '"**/memory/search/**/*.py"',
        # Experimental modules
        '"**/api_example.py"',
        '"**/example_configurable.py"',
    ]

    for pattern in ignore_patterns:
        print(f"    {pattern},")

    print("])")
    print("```")
    print()

    # 3. Specific fixes needed
    print("## 3. Specific Module Fixes")
    print()

    specific_fixes = [
        ("haive.core.schema.__init__.py", "Add missing 'create_age' export"),
        ("haive.core.registry.__init__.py", "Add missing 'AgentRegistry' export"),
        ("haive.games.api.__init__.py", "Add missing 'GameInfo' export"),
        ("haive.games.among_us.config.py", "Add missing 'AmongUsConfig' export"),
        ("haive.games.chess.config.py", "Add missing 'ChessAgentConfig' export"),
        ("haive.core.engine.aug_llm.__init__.py", "Add missing 'AugLLMEngine' export"),
        ("haive.games.core.base.state.py", "Add missing 'GameState' export"),
    ]

    for file_path, description in specific_fixes:
        print(f"- **{file_path}**: {description}")

    print()

    # 4. Summary
    print("## 4. Summary")
    print()
    total_issues = sum(len(errors[category]) for category in errors)
    print(f"- **Total issues identified**: {total_issues}")
    print(
        f"- **Missing modules**: {len(errors['missing_core_modules']) + len(errors['missing_dataflow_modules']) + len(errors['missing_games_modules'])}"
    )
    print(f"- **Import errors**: {len(errors['import_errors'])}")
    print(f"- **Type errors**: {len(errors['type_errors'])}")
    print(f"- **Name errors**: {len(errors['name_errors'])}")
    print()

    print(
        "**Strategy**: Focus on mock imports and ignore patterns first, then address specific missing exports."
    )


if __name__ == "__main__":
    create_fix_plan()
