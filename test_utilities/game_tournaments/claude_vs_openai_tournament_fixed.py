#!/usr/bin/env python3
"""Claude vs OpenAI Tournament - FIXED VERSION
Run all working games with consistent LLM configurations.
Properly handles state initialization for each game type.
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

# Create tournament results directory
TOURNAMENT_DIR = Path("claude_vs_openai_tournament_fixed")
TOURNAMENT_DIR.mkdir(exist_ok=True)


def save_tournament_result(game_name: str, winner: str, details: dict, matchup: str):
    """Save tournament result with consistent format."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    result = {
        "game": game_name,
        "matchup": matchup,
        "timestamp": timestamp,
        "winner": winner,
        "claude_player": details.get("claude_player", "Unknown"),
        "openai_player": details.get("openai_player", "Unknown"),
        "final_status": details.get("final_status", "Unknown"),
        "moves_played": details.get("moves", 0),
        "game_details": details,
    }

    filename = f"{game_name}_{matchup}_{timestamp}.json"
    with open(TOURNAMENT_DIR / filename, "w") as f:
        json.dump(result, f, indent=2, default=str)



def create_initial_state(game_name: str, state_class):
    """Create proper initial state for each game type."""
    if game_name == "mastermind":
        # Mastermind requires initialize() method
        return state_class.initialize(codemaker="player1")
    if game_name == "connect4":
        # Connect4 requires initialize() method
        return state_class.initialize()
    elif game_name == "reversi":
        # Check if Reversi has initialize method
        if hasattr(state_class, "initialize"):
            return state_class.initialize()
        # Try with required fields
        return state_class(turn="B", board=[[None] * 8 for _ in range(8)])
    else:
        # Tic Tac Toe, Mancala, Nim work with default constructor
        return state_class()


def create_claude_openai_config(
    game_config_class, claude_player: str, openai_player: str
):
    """Create game config with Claude vs OpenAI setup."""
    config = game_config_class()

    # Disable analysis to avoid loops
    if hasattr(config, "enable_analysis"):
        config.enable_analysis = False

    # Set recursion limit
    if hasattr(config, "runnable_config"):
        config.runnable_config = {"configurable": {"recursion_limit": 20}}

    # Game-specific configurations
    if hasattr(config, "max_turns"):
        config.max_turns = 10  # Limit turns for faster games

    if hasattr(config, "max_moves"):
        config.max_moves = min(getattr(config, "max_moves", 50), 50)  # Limit moves

    # Create engines dict with Claude vs OpenAI
    if hasattr(config, "engines") and isinstance(config.engines, dict):
        engines = config.engines.copy()

        # Map players to models
        for engine_name, engine_config in engines.items():
            if (
                claude_player in engine_name.lower()
                or "player1" in engine_name.lower()
                or "x" in engine_name.lower()
                or "white" in engine_name.lower()
                or "red" in engine_name.lower()
            ):
                # Assign Claude
                if hasattr(engine_config, "llm_config") and hasattr(
                    engine_config.llm_config, "model"
                ):
                    engine_config.llm_config.model = "claude-3-5-sonnet-20240620"
                if hasattr(engine_config, "llm_config") and hasattr(
                    engine_config.llm_config, "provider"
                ):
                    engine_config.llm_config.provider = "anthropic"
            elif (
                openai_player in engine_name.lower()
                or "player2" in engine_name.lower()
                or "o" in engine_name.lower()
                or "black" in engine_name.lower()
                or "yellow" in engine_name.lower()
            ):
                # Assign OpenAI
                if hasattr(engine_config, "llm_config") and hasattr(
                    engine_config.llm_config, "model"
                ):
                    engine_config.llm_config.model = "gpt-4o"
                if hasattr(engine_config, "llm_config") and hasattr(
                    engine_config.llm_config, "provider"
                ):
                    engine_config.llm_config.provider = "openai"

        config.engines = engines

    return config


def run_tournament_game(
    game_name: str, config_class, agent_class, claude_player: str, openai_player: str
):
    """Run a single tournament game."""
    matchup = "claude_vs_openai"

    try:

        # Create config with consistent LLM setup
        config = create_claude_openai_config(config_class, claude_player, openai_player)

        # Create agent
        agent = agent_class(config=config)

        # Get initial state using proper method
        state_class = config.state_schema
        initial_state = create_initial_state(game_name, state_class)


        try:
            # Run game with limited recursion
            result = agent.run(initial_state)

            # Extract winner
            winner = "Unknown"
            final_status = getattr(result, "game_status", "Unknown")
            moves = len(getattr(result, "move_history", []))

            # Determine winner based on game result
            if hasattr(result, "winner") and result.winner:
                raw_winner = str(result.winner)
                if (
                    "X" in raw_winner
                    or "player1" in raw_winner
                    or "white" in raw_winner.lower()
                    or "red" in raw_winner.lower()
                ):
                    winner = "Claude"
                elif (
                    "O" in raw_winner
                    or "player2" in raw_winner
                    or "black" in raw_winner.lower()
                    or "yellow" in raw_winner.lower()
                ):
                    winner = "OpenAI"
                else:
                    winner = f"Player: {raw_winner}"
            elif "win" in final_status.lower():
                if (
                    "player1" in final_status.lower()
                    or "X" in final_status
                    or "red" in final_status.lower()
                ):
                    winner = "Claude"
                elif (
                    "player2" in final_status.lower()
                    or "O" in final_status
                    or "yellow" in final_status.lower()
                ):
                    winner = "OpenAI"
                else:
                    winner = f"Status: {final_status}"
            elif final_status == "draw":
                winner = "Draw"
            else:
                winner = "Game Completed"

            details = {
                "claude_player": claude_player,
                "openai_player": openai_player,
                "final_status": final_status,
                "moves": moves,
                "board": getattr(result, "board", None),
                "turn": getattr(result, "turn", None),
            }

            save_tournament_result(game_name, winner, details, matchup)
            return winner

        except Exception as e:
            if "recursion_limit" in str(e):
                # Try to extract winner from error context
                error_text = str(e)
                if "X_win" in error_text:
                    winner = "Claude"
                elif "O_win" in error_text:
                    winner = "OpenAI"
                elif "_win" in error_text:
                    winner = "Game Completed (Hit Limit)"
                else:
                    winner = "Completed with Limit"

                details = {
                    "claude_player": claude_player,
                    "openai_player": openai_player,
                    "final_status": "recursion_limit",
                    "moves": 0,
                    "error": str(e),
                }

                save_tournament_result(game_name, winner, details, matchup)
                return winner
            raise e

    except Exception as e:
        details = {
            "claude_player": claude_player,
            "openai_player": openai_player,
            "final_status": "error",
            "error": str(e),
        }
        save_tournament_result(game_name, "Failed", details, matchup)
        return None


def main():
    """Run the complete Claude vs OpenAI tournament."""

    # Define games to test with their player mappings (only working ones)
    tournament_games = [
        {
            "name": "tic_tac_toe",
            "config_module": "haive.games.tic_tac_toe.config",
            "config_class": "TicTacToeConfig",
            "agent_module": "haive.games.tic_tac_toe.agent",
            "agent_class": "TicTacToeAgent",
            "claude_player": "X_player",
            "openai_player": "O_player",
        },
        {
            "name": "nim",
            "config_module": "haive.games.nim.config",
            "config_class": "NimConfig",
            "agent_module": "haive.games.nim.agent",
            "agent_class": "NimAgent",
            "claude_player": "player1",
            "openai_player": "player2",
        },
        {
            "name": "mastermind",
            "config_module": "haive.games.mastermind.config",
            "config_class": "MastermindConfig",
            "agent_module": "haive.games.mastermind.agent",
            "agent_class": "MastermindAgent",
            "claude_player": "player1",
            "openai_player": "player2",
        },
        {
            "name": "mancala",
            "config_module": "haive.games.mancala.config",
            "config_class": "MancalaConfig",
            "agent_module": "haive.games.mancala.agent",
            "agent_class": "MancalaAgent",
            "claude_player": "player1",
            "openai_player": "player2",
        },
        {
            "name": "connect4",
            "config_module": "haive.games.connect4.config",
            "config_class": "Connect4AgentConfig",
            "agent_module": "haive.games.connect4.agent",
            "agent_class": "Connect4Agent",
            "claude_player": "red_player",
            "openai_player": "yellow_player",
        },
        {
            "name": "reversi",
            "config_module": "haive.games.reversi.config",
            "config_class": "ReversiConfig",
            "agent_module": "haive.games.reversi.agent",
            "agent_class": "ReversiAgent",
            "claude_player": "player1",
            "openai_player": "player2",
        },
    ]

    tournament_results = {}

    # Run each game
    for game in tournament_games:
        try:
            # Import modules
            import importlib

            config_mod = importlib.import_module(game["config_module"])
            config_class = getattr(config_mod, game["config_class"])

            agent_mod = importlib.import_module(game["agent_module"])
            agent_class = getattr(agent_mod, game["agent_class"])

            # Run tournament game
            winner = run_tournament_game(
                game["name"],
                config_class,
                agent_class,
                game["claude_player"],
                game["openai_player"],
            )

            tournament_results[game["name"]] = winner

        except Exception as e:
            tournament_results[game["name"]] = "Failed"

    # Final tournament summary

    claude_wins = 0
    openai_wins = 0
    other_results = 0

    for game, winner in tournament_results.items():
        status_icon = "🎯" if winner else "❌"

        if winner == "Claude":
            claude_wins += 1
        elif winner == "OpenAI":
            openai_wins += 1
        elif winner and winner != "Failed":
            other_results += 1


    if claude_wins > openai_wins:
        pass)")
    elif openai_wins > claude_wins:
        pass)")
    else:
        pass)")



if __name__ == "__main__":
    main()
