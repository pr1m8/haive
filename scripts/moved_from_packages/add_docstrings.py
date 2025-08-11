#!/usr/bin/env python
"""Script to add Google-style docstrings to haive-games package.

This script identifies modules, classes, and functions in the haive-games
package that are missing docstrings and adds them automatically based on
naming conventions and context.

Usage:
    python add_docstrings.py [--path PATH] [--dry-run]

Example:
    python add_docstrings.py --path ../src/haive/games/chess
"""

import argparse
import ast
import os
import re
import sys


class DocstringVisitor(ast.NodeVisitor):
    """AST visitor to find nodes that need docstrings."""

    def __init__(self, module_name: str):
        self.module_name = module_name
        self.needs_docstrings = []
        self.has_docstrings = []
        self.current_class = None

    def visit_Module(self, node):
        """Visit a module node to check for module-level docstring."""
        if not ast.get_docstring(node):
            self.needs_docstrings.append(("module", None, node))
        else:
            self.has_docstrings.append(("module", None, node))
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        """Visit a class definition to check for class-level docstring."""
        old_class = self.current_class
        self.current_class = node.name

        if not ast.get_docstring(node):
            self.needs_docstrings.append(("class", node.name, node))
        else:
            self.has_docstrings.append(("class", node.name, node))

        self.generic_visit(node)
        self.current_class = old_class

    def visit_FunctionDef(self, node):
        """Visit a function definition to check for function-level docstring."""
        # Skip special methods
        if node.name.startswith("__") and node.name.endswith("__"):
            self.generic_visit(node)
            return

        if not ast.get_docstring(node):
            self.needs_docstrings.append(("function", node.name, node))
        else:
            self.has_docstrings.append(("function", node.name, node))

        self.generic_visit(node)


def generate_module_docstring(module_name: str, module_path: str) -> str:
    """Generate a comprehensive module-level docstring.

    Args:
        module_name: The name of the module (e.g., "chess", "poker").
        module_path: Path to the module file.

    Returns:
        A formatted docstring for the module.
    """
    # Determine module type (board game, card game, etc.)
    game_types = {
        "chess": "board game",
        "checkers": "board game",
        "go": "board game",
        "reversi": "board game",
        "connect4": "board game",
        "tic_tac_toe": "board game",
        "monopoly": "board game",
        "battleship": "board game",
        "mancala": "board game",
        "nim": "board game",
        "fox_and_geese": "board game",
        "poker": "card game",
        "blackjack": "card game",
        "uno": "card game",
        "mafia": "social deduction game",
        "among_us": "social deduction game",
        "clue": "social deduction game",
        "debate": "competitive game",
        "wordle": "single-player puzzle",
        "twenty_fourty_eight": "single-player puzzle",
        "word_search": "single-player puzzle",
        "base": "framework component",
        "base_v2": "framework component",
        "framework": "framework component",
        "core": "framework component",
        "multi_player": "framework component",
        "single_player": "framework component",
    }

    # Get module type
    module_path_parts = module_path.split("/")
    actual_module_name = (
        module_path_parts[-2]
        if module_path_parts[-1] == "__init__.py"
        else module_path_parts[-1].replace(".py", "")
    )

    game_type = game_types.get(actual_module_name, "game")

    # Create a title-case version of the module name for readable display
    display_name = " ".join(
        word.capitalize() for word in actual_module_name.replace("_", " ").split()
    )

    # Handle special cases
    if actual_module_name == "twenty_fourty_eight":
        display_name = "2048"
    elif actual_module_name == "tic_tac_toe":
        display_name = "Tic Tac Toe"

    # Determine file type and generate appropriate docstring
    if module_path.endswith("__init__.py"):
        if module_path_parts[-2] in game_types:
            docstring = f"""{display_name} {game_type} implementation.

This module provides a complete implementation of {display_name} for the Haive
games framework, including game state management, rules enforcement, move validation,
and agent integration.

Example:
    >>> from haive.games.{actual_module_name} import {display_name.replace(" ", "")}Agent
    >>> agent = {display_name.replace(" ", "")}Agent()
    >>> final_state = agent.run_game(visualize=True)

Typical usage:
    - Create a game agent
    - Configure game parameters
    - Run a full game or analyze specific positions
    - Inspect game state and results
"""
        else:
            docstring = f"""Module for {module_name} functionality.

This module contains implementations for {module_name} in the Haive games framework.

Example:
    >>> from haive.games.{module_name} import SomeClass
    >>> instance = SomeClass()
"""
    elif module_path.endswith("models.py"):
        docstring = f"""Models for {display_name} gameplay and analysis.

This module provides data models for representing {display_name} game elements,
including board state, pieces, players, moves, and analysis results.

Example:
    >>> from haive.games.{actual_module_name}.models import {display_name.replace(" ", "")}Move
    >>> move = {display_name.replace(" ", "")}Move(position=(0, 0), player="X")
"""
    elif module_path.endswith("state.py"):
        docstring = f"""State representation for {display_name} game.

This module defines the core state model for {display_name}, tracking the
complete game state including board position, player information, turn tracking,
and game status.

Example:
    >>> from haive.games.{actual_module_name}.state import {display_name.replace(" ", "")}State
    >>> state = {display_name.replace(" ", "")}State.initialize()
"""
    elif module_path.endswith("state_manager.py"):
        docstring = f"""State manager for {display_name} game logic and mechanics.

This module handles core operations like initializing the board, validating and applying
moves, evaluating win conditions, and updating the state with engine analyses.

Example:
    >>> from haive.games.{actual_module_name}.state_manager import {display_name.replace(" ", "")}StateManager
    >>> manager = {display_name.replace(" ", "")}StateManager()
    >>> new_state = manager.apply_move(state, move)
"""
    elif module_path.endswith("agent.py"):
        docstring = f"""{display_name} agent implementation.

This module provides an agent for playing {display_name}, handling strategic decision
making, move generation, and game management.

Example:
    >>> from haive.games.{actual_module_name}.agent import {display_name.replace(" ", "")}Agent
    >>> agent = {display_name.replace(" ", "")}Agent()
    >>> result = agent.run_game()
"""
    elif module_path.endswith("config.py"):
        docstring = f"""Configuration for {display_name} game.

This module defines the configuration options for {display_name} games,
including game parameters, player settings, and engine configurations.

Example:
    >>> from haive.games.{actual_module_name}.config import {display_name.replace(" ", "")}Config
    >>> config = {display_name.replace(" ", "")}Config(first_player="X")
"""
    elif module_path.endswith("engines.py"):
        docstring = f"""Engine configurations for {display_name} game.

This module provides engine definitions for {display_name}, including
strategic analysis, move generation, and position evaluation.

Example:
    >>> from haive.games.{actual_module_name}.engines import analysis_engine
    >>> analysis = analysis_engine.invoke(state=game_state)
"""
    elif module_path.endswith("prompts.py"):
        docstring = f"""Prompt templates for {display_name} agents.

This module contains prompt templates used by LLM-based {display_name} agents
for various tasks like move generation, position analysis, and game state description.

Example:
    >>> from haive.games.{actual_module_name}.prompts import MOVE_PROMPT
    >>> filled_prompt = MOVE_PROMPT.format(board=state.board)
"""
    elif module_path.endswith("ui.py"):
        docstring = f"""User interface for {display_name} game.

This module provides UI components for visualizing and interacting with
{display_name} games, including console-based and rich terminal interfaces.

Example:
    >>> from haive.games.{actual_module_name}.ui import {display_name.replace(" ", "")}UI
    >>> ui = {display_name.replace(" ", "")}UI()
    >>> ui.display(game_state)
"""
    else:
        # Default docstring for other file types
        docstring = f"""Utilities for {display_name} game.

This module provides supporting functionality for {display_name} games.

Example:
    >>> from haive.games.{actual_module_name}.{module_path_parts[-1].replace(".py", "")} import some_function
    >>> result = some_function()
"""

    return docstring


def generate_class_docstring(class_name: str, module_name: str, file_path: str) -> str:
    """Generate a docstring for a class based on its name and module context.

    Args:
        class_name: Name of the class.
        module_name: Name of the module.
        file_path: Path to the file containing the class.

    Returns:
        A formatted docstring for the class.
    """
    # Get module name from path
    path_parts = file_path.split("/")
    actual_module_name = (
        path_parts[-2]
        if path_parts[-1] == "__init__.py"
        else path_parts[-1].replace(".py", "")
    )

    # Create a title-case version of the module name for readable display
    display_name = " ".join(
        word.capitalize() for word in actual_module_name.replace("_", " ").split()
    )

    # Handle special cases
    if actual_module_name == "twenty_fourty_eight":
        display_name = "2048"
    elif actual_module_name == "tic_tac_toe":
        display_name = "Tic Tac Toe"

    # Determine the type of class based on naming patterns
    if class_name.endswith("Config"):
        return f"""Configuration for the {display_name} game.

This class defines the configurable parameters for {display_name} games,
including player settings, game rules variations, and engine configurations.

Attributes:
    [Automatically detected from class fields]

Example:
    >>> config = {class_name}(
    ...     first_player="player1",
    ...     enable_analysis=True
    ... )
    >>> agent = {display_name.replace(" ", "")}Agent(config)
"""

    if class_name.endswith("State"):
        return f"""Represents the complete state of a {display_name} game.

This class manages the game state including board position, player information,
turn tracking, move history, and game status.

Attributes:
    [Automatically detected from class fields]

Example:
    >>> state = {class_name}.initialize(players=["player1", "player2"])
    >>> print(state.board)
"""

    if class_name.endswith("StateManager"):
        return f"""Manages game logic and state transitions for {display_name}.

This class handles core game mechanics including move validation, state updates,
win condition checking, and game progression.

Attributes:
    [Automatically detected from class fields]

Example:
    >>> manager = {class_name}()
    >>> valid_move = manager.is_valid_move(state, move)
    >>> new_state = manager.apply_move(state, move)
"""

    if class_name.endswith("Agent"):
        return f"""{display_name} playing agent with strategic reasoning capabilities.

This agent can play {display_name} using LLM-based reasoning, analyzing positions,
generating moves, and responding to opponents.

Attributes:
    [Automatically detected from class fields]

Example:
    >>> agent = {class_name}()
    >>> final_state = agent.run_game()
"""

    if class_name.endswith("Move"):
        return f"""Represents a single move in {display_name}.

This class defines the structure and validation for game moves, capturing
all necessary information for state transitions.

Attributes:
    [Automatically detected from class fields]

Example:
    >>> move = {class_name}(player="player1", position=(0, 0))
"""

    if class_name.endswith("Analysis"):
        return f"""Strategic analysis for {display_name} positions.

This class provides structured analysis of game positions, including
evaluation, possible moves, threats, and strategic recommendations.

Attributes:
    [Automatically detected from class fields]

Example:
    >>> analysis = {class_name}(
    ...     position_evaluation="advantage",
    ...     recommended_move={"row": 0, "col": 0}
    ... )
"""

    if class_name.endswith("Board"):
        return f"""Represents the game board for {display_name}.

This class provides the structure and operations for the {display_name} board,
including initialization, access, and state representation.

Attributes:
    [Automatically detected from class fields]

Example:
    >>> board = {class_name}(size=(8, 8))
    >>> board.place_piece(position=(0, 0), piece="X")
"""

    if class_name.endswith("Player"):
        return f"""Represents a player in {display_name}.

This class holds player information for {display_name} games, including
identification, score, and game-specific player state.

Attributes:
    [Automatically detected from class fields]

Example:
    >>> player = {class_name}(id="p1", name="Player 1")
"""

    if class_name.endswith("UI") or class_name.endswith("Renderer"):
        return f"""User interface component for {display_name}.

This class provides visualization and interaction capabilities for
{display_name} games.

Attributes:
    [Automatically detected from class fields]

Example:
    >>> ui = {class_name}()
    >>> ui.render(game_state)
"""

    if class_name.endswith("Runner"):
        return f"""Game runner for {display_name}.

This class manages the execution of {display_name} games, coordinating
between players, state updates, and visualization.

Attributes:
    [Automatically detected from class fields]

Example:
    >>> runner = {class_name}()
    >>> result = runner.run_game(players=[player1, player2])
"""

    # Generic class docstring for other types
    return f"""{class_name} for {display_name} game implementation.

This class provides functionality for the {display_name} game module.

Attributes:
    [Automatically detected from class fields]

Example:
    >>> obj = {class_name}()
"""


def generate_function_docstring(
    func_name: str, func_def: ast.FunctionDef, module_name: str, file_path: str
) -> str:
    """Generate a docstring for a function based on its name and signature.

    Args:
        func_name: Name of the function.
        func_def: AST FunctionDef node for the function.
        module_name: Name of the module.
        file_path: Path to the file containing the function.

    Returns:
        A formatted docstring for the function.
    """
    # Get module name from path
    path_parts = file_path.split("/")
    actual_module_name = (
        path_parts[-2]
        if path_parts[-1] == "__init__.py"
        else path_parts[-1].replace(".py", "")
    )

    # Create a title-case version of the module name for readable display
    display_name = " ".join(
        word.capitalize() for word in actual_module_name.replace("_", " ").split()
    )

    # Handle special cases
    if actual_module_name == "twenty_fourty_eight":
        display_name = "2048"
    elif actual_module_name == "tic_tac_toe":
        display_name = "Tic Tac Toe"

    # Extract parameters from the function definition
    params = []
    for arg in func_def.args.args:
        if arg.arg != "self" and arg.arg != "cls":
            params.append(arg.arg)

    # Generate function description based on common naming patterns
    if func_name.startswith("get_"):
        desc = f"Retrieve {func_name[4:]} from the {display_name} game."
    elif func_name.startswith("set_"):
        desc = f"Set {func_name[4:]} in the {display_name} game."
    elif func_name.startswith("is_"):
        desc = f"Check if {func_name[3:]} in the {display_name} game."
    elif func_name.startswith("has_"):
        desc = f"Check if {display_name} game has {func_name[4:]}."
    elif func_name.startswith("apply_"):
        desc = f"Apply {func_name[6:]} to the {display_name} game state."
    elif func_name.startswith("validate_"):
        desc = f"Validate {func_name[9:]} in the {display_name} game."
    elif func_name == "initialize":
        desc = f"Initialize a new {display_name} game state."
    elif func_name == "reset":
        desc = f"Reset the {display_name} game to its initial state."
    elif func_name == "step":
        desc = f"Execute a single step/move in the {display_name} game."
    elif func_name == "run_game":
        desc = f"Run a complete {display_name} game from start to finish."
    elif func_name == "is_valid_move":
        desc = f"Check if a move is valid in the current {display_name} game state."
    elif func_name == "apply_move":
        desc = f"Apply a move to the current {display_name} game state."
    elif func_name == "get_legal_moves":
        desc = f"Get all legal moves for the current {display_name} game state."
    elif func_name == "check_win_condition":
        desc = "Check if the game has reached a win condition."
    elif func_name == "evaluate_position":
        desc = "Evaluate the current game position strategically."
    elif func_name == "update_state":
        desc = "Update the game state based on the latest move or changes."
    else:
        desc = f"{func_name} operation for {display_name} game."

    # Generate parameter descriptions
    param_docs = []
    for param in params:
        param_desc = generate_param_description(param, func_name, actual_module_name)
        param_docs.append(f"        {param}: {param_desc}")

    param_section = "\n".join(param_docs) if param_docs else "        None"

    # Determine return type based on function annotation if available
    return_desc = "The result of the operation."
    if func_def.returns:
        if isinstance(func_def.returns, ast.Name):
            return_type = func_def.returns.id
            if return_type == "bool":
                return_desc = "True if successful, False otherwise."
            elif return_type == "str":
                return_desc = "A string representation or result."
            elif return_type == "int":
                return_desc = "A numeric result or status code."
            elif return_type == "float":
                return_desc = "A numeric value or score."
            elif return_type == "list":
                return_desc = "A list of results."
            elif return_type == "dict":
                return_desc = "A dictionary containing result data."
            elif return_type == "None":
                return_desc = "None"
            elif "State" in return_type:
                return_desc = f"Updated {display_name} game state."
            elif "Move" in return_type:
                return_desc = f"Generated {display_name} move."
            elif "Analysis" in return_type:
                return_desc = f"Analysis result for the {display_name} position."

    return f"""{desc}

Args:
{param_section}

Returns:
        {return_desc}
"""


def generate_param_description(
    param_name: str, func_name: str, module_name: str
) -> str:
    """Generate a description for a function parameter based on its name.

    Args:
        param_name: Name of the parameter.
        func_name: Name of the function containing the parameter.
        module_name: Name of the module.

    Returns:
        A description string for the parameter.
    """
    display_name = " ".join(
        word.capitalize() for word in module_name.replace("_", " ").split()
    )

    # Common parameter names and their descriptions
    param_descriptions = {
        "state": f"Current {display_name} game state.",
        "move": f"The move to apply to the {display_name} game.",
        "player": "The player making the move or taking the action.",
        "player_id": "Identifier for the player.",
        "config": f"Configuration settings for the {display_name} game.",
        "board": f"The {display_name} game board.",
        "position": "Position coordinates on the game board.",
        "game": f"The {display_name} game instance.",
        "visualize": "Whether to display visualization of the game.",
        "verbose": "Whether to output detailed progress information.",
        "timeout": "Maximum time allowed for the operation.",
        "max_steps": "Maximum number of steps or moves allowed.",
        "seed": "Random seed for reproducibility.",
        "engine": "The engine to use for AI operations.",
        "analysis": "Game position analysis data.",
    }

    # Check for common parameter prefixes/suffixes
    if param_name.endswith("_state"):
        return f"State information for {param_name[:-6]}."
    if param_name.endswith("_config"):
        return f"Configuration for {param_name[:-7]}."
    if param_name.endswith("_id"):
        return f"Identifier for {param_name[:-3]}."
    if param_name.endswith("_name"):
        return f"Name of the {param_name[:-5]}."
    if param_name.endswith("_path"):
        return f"Path to the {param_name[:-5]}."
    if param_name.endswith("_file"):
        return f"File containing {param_name[:-5]} data."
    if param_name.endswith("_dir"):
        return f"Directory containing {param_name[:-4]} data."
    if param_name.startswith("max_"):
        return f"Maximum value for {param_name[4:]}."
    if param_name.startswith("min_"):
        return f"Minimum value for {param_name[4:]}."
    if param_name.startswith("num_"):
        return f"Number of {param_name[4:]}."

    # Return from common parameter descriptions or a generic description
    return param_descriptions.get(
        param_name, f"The {param_name.replace('_', ' ')} for the operation."
    )


def add_docstrings_to_file(file_path: str, dry_run: bool = False) -> dict[str, int]:
    """Add docstrings to a Python file where needed.

    Args:
        file_path: Path to the Python file to process.
        dry_run: If True, don't actually modify the file.

    Returns:
        Dictionary with stats about added docstrings.
    """
    stats = {
        "module_added": 0,
        "class_added": 0,
        "function_added": 0,
        "module_skipped": 0,
        "class_skipped": 0,
        "function_skipped": 0,
    }

    try:
        with open(file_path) as f:
            file_content = f.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return stats

    # Extract module name from path
    path_parts = file_path.split("/")
    module_parts = []
    for i, part in enumerate(path_parts):
        if part == "src":
            module_parts = path_parts[i + 1 :]
            break

    if not module_parts:
        module_parts = path_parts[-3:]

    # Module name without '.py' extension
    module_name = ".".join(module_parts)
    if module_name.endswith(".py"):
        module_name = module_name[:-3]

    # Parse the file
    try:
        tree = ast.parse(file_content)
    except SyntaxError as e:
        print(f"Syntax error in {file_path}: {e}")
        return stats

    # Find nodes that need docstrings
    visitor = DocstringVisitor(module_name)
    visitor.visit(tree)

    # Generate and add docstrings
    modifications = []

    for node_type, node_name, node in visitor.needs_docstrings:
        if node_type == "module":
            docstring = generate_module_docstring(module_name, file_path)
            # Add to start of file (handling shebang if present)
            if file_content.startswith("#!"):
                shebang_end = file_content.find("\n") + 1
                modifications.append(
                    (shebang_end, shebang_end, f'"""{docstring}"""\n\n')
                )
            else:
                modifications.append((0, 0, f'"""{docstring}"""\n\n'))
            stats["module_added"] += 1

        elif node_type == "class":
            docstring = generate_class_docstring(node_name, module_name, file_path)
            # Find position after class definition to insert docstring
            class_line = file_content.count("\n", 0, node.lineno - 1)
            class_def_end = file_content.find(":", node.col_offset + class_line) + 1
            indentation = " " * (
                node.col_offset + 4
            )  # 4 spaces after class indentation
            modifications.append(
                (class_def_end, class_def_end, f'\n{indentation}"""{docstring}"""')
            )
            stats["class_added"] += 1

        elif node_type == "function":
            docstring = generate_function_docstring(
                node_name, node, module_name, file_path
            )
            # Find position after function definition to insert docstring
            func_line = file_content.count("\n", 0, node.lineno - 1)
            func_def_end = file_content.find(":", node.col_offset + func_line) + 1
            indentation = " " * (
                node.col_offset + 4
            )  # 4 spaces after function indentation
            modifications.append(
                (func_def_end, func_def_end, f'\n{indentation}"""{docstring}"""')
            )
            stats["function_added"] += 1

    # Update file content with docstrings
    # Sort modifications in reverse order to avoid position shifts
    modifications.sort(key=lambda x: x[0], reverse=True)

    new_content = file_content
    for start, end, text in modifications:
        new_content = new_content[:start] + text + new_content[end:]

    # Write updated content back to the file
    if not dry_run and modifications:
        try:
            with open(file_path, "w") as f:
                f.write(new_content)
            print(f"Updated {file_path} with {len(modifications)} docstrings")
        except Exception as e:
            print(f"Error writing to file {file_path}: {e}")

    # Add skipped stats
    stats["module_skipped"] = len(
        [n for n in visitor.has_docstrings if n[0] == "module"]
    )
    stats["class_skipped"] = len([n for n in visitor.has_docstrings if n[0] == "class"])
    stats["function_skipped"] = len(
        [n for n in visitor.has_docstrings if n[0] == "function"]
    )

    return stats


def create_module_readme(module_path: str, dry_run: bool = False) -> bool:
    """Create a README.md file for a module if it doesn't exist.

    Args:
        module_path: Path to the module directory.
        dry_run: If True, don't actually create the file.

    Returns:
        True if README was created, False otherwise.
    """
    readme_path = os.path.join(module_path, "README.md")
    if os.path.exists(readme_path):
        print(f"README already exists at {readme_path}")
        return False

    # Extract module name from path
    module_name = os.path.basename(module_path)

    # Determine game category
    game_categories = {
        "chess": "Board Game",
        "checkers": "Board Game",
        "go": "Board Game",
        "reversi": "Board Game",
        "connect4": "Board Game",
        "tic_tac_toe": "Board Game",
        "monopoly": "Board Game",
        "battleship": "Board Game",
        "mancala": "Board Game",
        "nim": "Board Game",
        "fox_and_geese": "Board Game",
        "poker": "Card Game",
        "blackjack": "Card Game",
        "uno": "Card Game",
        "mafia": "Social Deduction Game",
        "among_us": "Social Deduction Game",
        "clue": "Social Deduction Game",
        "debate": "Competitive Game",
        "wordle": "Single-Player Puzzle",
        "twenty_fourty_eight": "Single-Player Puzzle",
        "word_search": "Single-Player Puzzle",
    }

    category = game_categories.get(module_name, "Game")

    # Create a title-case version of the module name for readable display
    display_name = " ".join(
        word.capitalize() for word in module_name.replace("_", " ").split()
    )

    # Handle special cases
    if module_name == "twenty_fourty_eight":
        display_name = "2048"
    elif module_name == "tic_tac_toe":
        display_name = "Tic Tac Toe"

    # Analyze directory to find components
    components = []
    for filename in os.listdir(module_path):
        if filename.endswith(".py") and filename != "__init__.py":
            base_name = filename[:-3]
            if base_name in [
                "agent",
                "config",
                "state",
                "state_manager",
                "models",
                "engines",
                "ui",
                "prompts",
            ]:
                component_name = f"{display_name}{base_name.capitalize()}"
                if base_name == "models":
                    # Try to identify model classes in the file
                    try:
                        with open(os.path.join(module_path, filename)) as f:
                            content = f.read()
                            model_classes = re.findall(r"class ()\(BaseModel", content)
                            for model_class in model_classes:
                                components.append(model_class)
                    except Exception:
                        components.append(f"{display_name} Models")
                else:
                    components.append(component_name)

    # Generate feature list based on module and known game types
    features = []
    if category == "Board Game":
        features = [
            f"Complete implementation of {display_name} rules",
            "Board state management and visualization",
            "Move validation and legal move generation",
            "Win condition detection",
            "LLM-based strategic reasoning",
            "Game history tracking",
        ]
    elif category == "Card Game":
        features = [
            f"Complete implementation of {display_name} rules",
            "Card deck management and game state tracking",
            "Betting/bidding mechanics",
            "Hand evaluation and scoring",
            "LLM-based strategic reasoning",
            "Player information management with visibility controls",
        ]
    elif category == "Social Deduction Game":
        features = [
            f"Complete implementation of {display_name} rules",
            "Role assignment and management",
            "Information hiding and revelation mechanics",
            "Voting and elimination systems",
            "LLM-based strategic reasoning and deception",
            "Complex social interaction modeling",
        ]
    elif category == "Single-Player Puzzle":
        features = [
            f"Complete implementation of {display_name} rules",
            "Puzzle state representation and visualization",
            "Move validation and solution checking",
            "Difficulty scaling",
            "LLM-based solving strategies",
            "Performance metrics and scoring",
        ]
    else:
        features = [
            f"Complete implementation of {display_name} rules",
            "Game state management",
            "Move validation and processing",
            "Win condition detection",
            "LLM-based strategic reasoning",
        ]

    # Basic usage example
    usage_example = f"""```python
from haive.games.{module_name} import {display_name.replace(" ", "")}Agent
from haive.games.{module_name} import {display_name.replace(" ", "")}Config

# Create a game agent with custom configuration
config = {display_name.replace(" ", "")}Config(
    enable_analysis=True,
    visualize=True
)
agent = {display_name.replace(" ", "")}Agent(config)

# Run a complete game
final_state = agent.run_game()

# Check game outcome
print(f"Game status: {final_state}")
```"""

    # Create README content
    readme_content = f"""# {display_name} {category} Module

The {display_name} module provides a comprehensive implementation of the {display_name} {category.lower()} for use with the Haive framework. This module enables agents to play {display_name} using LLM-based strategic reasoning, with support for game state management, move validation, analysis, and interactive gameplay.

## Features

{chr(10).join([f"- {feature}" for feature in features])}

## Components

{chr(10).join([f"- `{component}` - {component} for {display_name} implementation" for component in components])}

## Usage Example

{usage_example}

## Integration with Haive Framework

This module is designed to work seamlessly with the Haive agent framework, providing:

- Standardized state representation
- Engine configurations for agent deployment
- Strategic analysis capabilities
- Full compatibility with LLM-based reasoning
- Langgraph-based workflow management
"""

    if not dry_run:
        try:
            with open(readme_path, "w") as f:
                f.write(readme_content)
            print(f"Created README at {readme_path}")
            return True
        except Exception as e:
            print(f"Error creating README at {readme_path}: {e}")
            return False
    else:
        print(f"Would create README at {readme_path}")
        return True


def process_directory(dir_path: str, dry_run: bool = False) -> dict[str, int]:
    """Process all Python files in a directory to add documentation.

    Args:
        dir_path: Path to the directory to process.
        dry_run: If True, don't modify any files.

    Returns:
        Dictionary with statistics about the processed files.
    """
    stats = {
        "files_processed": 0,
        "module_docstrings_added": 0,
        "class_docstrings_added": 0,
        "function_docstrings_added": 0,
        "module_docstrings_skipped": 0,
        "class_docstrings_skipped": 0,
        "function_docstrings_skipped": 0,
        "readmes_added": 0,
        "readmes_skipped": 0,
        "errors": 0,
    }

    # Process Python files for docstrings
    for root, dirs, files in os.walk(dir_path):
        for filename in files:
            if filename.endswith(".py"):
                file_path = os.path.join(root, filename)
                try:
                    file_stats = add_docstrings_to_file(file_path, dry_run)
                    stats["files_processed"] += 1
                    stats["module_docstrings_added"] += file_stats["module_added"]
                    stats["class_docstrings_added"] += file_stats["class_added"]
                    stats["function_docstrings_added"] += file_stats["function_added"]
                    stats["module_docstrings_skipped"] += file_stats["module_skipped"]
                    stats["class_docstrings_skipped"] += file_stats["class_skipped"]
                    stats["function_docstrings_skipped"] += file_stats[
                        "function_skipped"
                    ]
                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")
                    stats["errors"] += 1

    # Generate README files for modules
    for root, dirs, files in os.walk(dir_path):
        # Skip __pycache__ and other hidden directories
        dirs[:] = [d for d in dirs if not d.startswith("__") and not d.startswith(".")]

        # Check if this is a module directory (has __init__.py)
        if "__init__.py" in files:
            try:
                if create_module_readme(root, dry_run):
                    stats["readmes_added"] += 1
                else:
                    stats["readmes_skipped"] += 1
            except Exception as e:
                print(f"Error creating README for {root}: {e}")
                stats["errors"] += 1

    return stats


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Add Google-style docstrings to haive-games package."
    )
    parser.add_argument(
        "--path",
        type=str,
        default="../src/haive/games",
        help="Path to the games directory to process (default: ../src/haive/games)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Don't modify files, just show what would be changed",
    )

    args = parser.parse_args()

    if not os.path.exists(args.path) or not os.path.isdir(args.path):
        print(f"Error: Path {args.path} does not exist or is not a directory.")
        sys.exit(1)

    print(f"Processing {args.path} {'(dry run)' if args.dry_run else ''}...")
    stats = process_directory(args.path, args.dry_run)

    print("\nDocumentation generation complete!")
    print(f"Files processed: {stats['files_processed']}")
    print(f"Module docstrings added: {stats['module_docstrings_added']}")
    print(f"Class docstrings added: {stats['class_docstrings_added']}")
    print(f"Function docstrings added: {stats['function_docstrings_added']}")
    print(f"Module docstrings skipped: {stats['module_docstrings_skipped']}")
    print(f"Class docstrings skipped: {stats['class_docstrings_skipped']}")
    print(f"Function docstrings skipped: {stats['function_docstrings_skipped']}")
    print(f"READMEs added: {stats['readmes_added']}")
    print(f"READMEs skipped: {stats['readmes_skipped']}")
    print(f"Errors: {stats['errors']}")


if __name__ == "__main__":
    main()
