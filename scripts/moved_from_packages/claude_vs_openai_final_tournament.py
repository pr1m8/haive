#!/usr/bin/env python3
"""Final comprehensive tournament between Claude and OpenAI with all working games.

This script runs a tournament across all 21 working games in the Haive games library.
"""

import asyncio
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any

# Add the parent directories to the path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from haive.core.models.llm import LLMConfig, LLMProvider

# Import all working game agents
from haive.games.among_us import AmongUsAgent, AmongUsAgentConfig
from haive.games.battleship import BattleshipAgent, BattleshipAgentConfig
from haive.games.checkers import CheckersAgent, CheckersAgentConfig
from haive.games.chess import ChessAgent, ChessConfig
from haive.games.clue import ClueAgent, ClueConfig
from haive.games.connect4 import Connect4Agent, Connect4AgentConfig
from haive.games.debate import DebateAgent, DebateAgentConfig
from haive.games.dominoes import DominoesAgent, DominoesAgentConfig
from haive.games.fox_and_geese import FoxAndGeeseAgent, FoxAndGeeseConfig
from haive.games.hold_em import HoldemGameAgent, HoldemGameAgentConfig
from haive.games.mafia import MafiaAgent, MafiaAgentConfig
from haive.games.mancala import MancalaAgent, MancalaConfig
from haive.games.mastermind import MastermindAgent, MastermindConfig
from haive.games.monopoly import MonopolyAgent, MonopolyAgentConfig
from haive.games.nim import NimAgent, NimConfig
from haive.games.poker import PokerAgent, PokerAgentConfig
from haive.games.reversi import ReversiAgent, ReversiConfig
from haive.games.risk import RiskAgent, RiskConfig
from haive.games.tic_tac_toe import TicTacToeAgent, TicTacToeConfig

# Configure LLMs
claude_config = LLMConfig(
    provider=LLMProvider.AZURE,
    model="claude-3-5-sonnet-20241022",
    api_key=os.getenv("AZURE_ANTHROPIC_API_KEY", ""),
    api_base="https://anthropic-aws-virginia.openai.azure.com/",
    api_version="2023-05-15",
)

openai_config = LLMConfig(
    provider=LLMProvider.AZURE,
    model="gpt-4o",
    api_key=os.getenv("AZURE_OPENAI_API_KEY", ""),
    api_base="https://awt-gpt.openai.azure.com/",
    api_version="2024-08-01-preview",
)


def create_game_config(game_name: str) -> tuple[Any, Any]:
    """Create agent and config for a specific game."""
    if game_name == "tic_tac_toe":
        config = TicTacToeConfig(
            aug_llm_configs={"player_1": claude_config, "player_2": openai_config},
            max_rounds=9,
        )
        return TicTacToeAgent, config

    if game_name == "nim":
        config = NimConfig(
            aug_llm_configs={"player_1": claude_config, "player_2": openai_config},
            max_rounds=20,
        )
        return NimAgent, config

    if game_name == "mancala":
        config = MancalaConfig(
            aug_llm_configs={"player_1": claude_config, "player_2": openai_config},
            max_rounds=100,
        )
        return MancalaAgent, config

    if game_name == "mastermind":
        config = MastermindConfig(
            aug_llm_configs={"codebreaker": claude_config, "codemaker": openai_config},
            max_rounds=10,
        )
        return MastermindAgent, config

    if game_name == "connect4":
        config = Connect4AgentConfig(
            aug_llm_configs={"player_1": claude_config, "player_2": openai_config},
            max_rounds=42,
        )
        return Connect4Agent, config

    if game_name == "reversi":
        config = ReversiConfig(
            aug_llm_configs={"player_1": claude_config, "player_2": openai_config},
            max_rounds=64,
        )
        return ReversiAgent, config

    if game_name == "chess":
        config = ChessConfig(
            aug_llm_configs={"white": claude_config, "black": openai_config},
            max_moves=200,
        )
        return ChessAgent, config

    if game_name == "checkers":
        config = CheckersAgentConfig(
            aug_llm_configs={"red": claude_config, "black": openai_config},
            max_moves=200,
        )
        return CheckersAgent, config

    if game_name == "battleship":
        config = BattleshipAgentConfig(
            aug_llm_configs={"player_1": claude_config, "player_2": openai_config},
            max_rounds=100,
        )
        return BattleshipAgent, config

    if game_name == "clue":
        config = ClueConfig(
            aug_llm_configs={
                "player_1": claude_config,
                "player_2": openai_config,
                "player_3": claude_config,
            },
            max_rounds=50,
        )
        return ClueAgent, config

    if game_name == "debate":
        config = DebateAgentConfig(
            aug_llm_configs={"debater_1": claude_config, "debater_2": openai_config},
            max_rounds=5,
            topic="Should AI be regulated by governments?",
        )
        return DebateAgent, config

    if game_name == "dominoes":
        config = DominoesAgentConfig(
            aug_llm_configs={
                "player_1": claude_config,
                "player_2": openai_config,
            },
            max_rounds=50,
        )
        return DominoesAgent, config

    if game_name == "fox_and_geese":
        config = FoxAndGeeseConfig(
            aug_llm_configs={"fox": claude_config, "geese": openai_config},
            max_rounds=100,
        )
        return FoxAndGeeseAgent, config

    if game_name == "mafia":
        config = MafiaAgentConfig(
            aug_llm_configs={
                "narrator": claude_config,
                "villager": openai_config,
                "mafia": claude_config,
                "detective": openai_config,
                "doctor": claude_config,
            },
            player_count=7,
            max_days=5,
        )
        return MafiaAgent, config

    if game_name == "poker":
        config = PokerAgentConfig(
            aug_llm_configs={
                "player_1": claude_config,
                "player_2": openai_config,
            },
            max_rounds=20,
            starting_chips=1000,
        )
        return PokerAgent, config

    if game_name == "risk":
        config = RiskConfig(
            aug_llm_configs={
                "player_1": claude_config,
                "player_2": openai_config,
            },
            max_rounds=100,
        )
        return RiskAgent, config

    if game_name == "among_us":
        config = AmongUsAgentConfig(
            aug_llm_configs={
                "player_1": claude_config,
                "player_2": openai_config,
                "player_3": claude_config,
                "player_4": openai_config,
            },
            impostor_count=1,
            max_rounds=10,
        )
        return AmongUsAgent, config

    if game_name == "monopoly":
        config = MonopolyAgentConfig(
            aug_llm_configs={
                "player_1": claude_config,
                "player_2": openai_config,
            },
            max_turns=100,
        )
        return MonopolyAgent, config

    if game_name == "hold_em":
        config = HoldemGameAgentConfig(
            aug_llm_configs={
                "player_1": claude_config,
                "player_2": openai_config,
            },
            max_hands=10,
            starting_chips=1000,
        )
        return HoldemGameAgent, config

    raise ValueError(f"Unknown game: {game_name}")


async def run_single_game(game_name: str) -> dict[str, Any]:
    """Run a single game and return results."""
    start_time = time.time()

    try:
        # Create game config
        agent_class, config = create_game_config(game_name)

        # Create agent
        agent = agent_class(config)

        # Get initial state
        if hasattr(agent, "initialize"):
            initial_state = agent.initialize()
        elif hasattr(agent, "get_initial_state"):
            initial_state = agent.get_initial_state()
        # Try to create initial state from config
        elif game_name == "mafia":
            from haive.games.mafia.state_manager import MafiaStateManager

            player_names = [
                "Player_1",
                "Player_2",
                "Player_3",
                "Player_4",
                "Player_5",
                "Player_6",
                "Narrator",
            ]
            initial_state = MafiaStateManager.initialize(player_names)
        else:
            initial_state = {}

        # Run the game
        final_state = None
        step_count = 0

        for state in agent.app.stream(initial_state):
            final_state = state
            step_count += 1

            # Check for game over
            if isinstance(state, dict):
                if state.get("game_over") or state.get("winner"):
                    break
            elif (hasattr(state, "game_over") and state.game_over) or (
                hasattr(state, "winner") and state.winner
            ):
                break

        # Determine winner
        winner = None
        if isinstance(final_state, dict):
            winner = final_state.get("winner", "unknown")
        elif hasattr(final_state, "winner"):
            winner = final_state.winner

        # Map winner to Claude/OpenAI
        if winner:
            if (
                "1" in str(winner).lower()
                or "white" in str(winner).lower()
                or "red" in str(winner).lower()
                or "fox" in str(winner).lower()
                or "codebreaker" in str(winner).lower()
                or "debater_1" in str(winner).lower()
            ):
                winner_ai = "Claude"
            elif (
                "2" in str(winner).lower()
                or "black" in str(winner).lower()
                or "geese" in str(winner).lower()
                or "codemaker" in str(winner).lower()
                or "debater_2" in str(winner).lower()
            ):
                winner_ai = "OpenAI"
            elif winner.lower() == "draw" or winner.lower() == "tie":
                winner_ai = "Draw"
            else:
                winner_ai = winner
        else:
            winner_ai = "Unknown"

        duration = time.time() - start_time

        result = {
            "game": game_name,
            "status": "completed",
            "winner": winner_ai,
            "raw_winner": str(winner),
            "steps": step_count,
            "duration": duration,
            "timestamp": datetime.now().isoformat(),
        }

        return result

    except Exception as e:
        import traceback

        traceback.print_exc()

        return {
            "game": game_name,
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat(),
        }


async def run_tournament():
    """Run the complete tournament."""
    # List of all working games
    games = [
        "tic_tac_toe",
        "nim",
        "mancala",
        "mastermind",
        "connect4",
        "reversi",
        "chess",
        "checkers",
        "battleship",
        "clue",
        "debate",
        "dominoes",
        "fox_and_geese",
        "mafia",
        "poker",
        "risk",
        "among_us",
        "monopoly",
        "hold_em",
    ]

    # Run all games
    results = []
    for game in games:
        result = await run_single_game(game)
        results.append(result)

        # Save intermediate results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = Path("tournament_tools/results/final_tournament")
        output_dir.mkdir(parents=True, exist_ok=True)

        with open(output_dir / f"{game}_final_{timestamp}.json", "w") as f:
            json.dump(result, f, indent=2)

    # Calculate summary statistics
    claude_wins = sum(
        1
        for r in results
        if r.get("status") == "completed" and r.get("winner") == "Claude"
    )
    openai_wins = sum(
        1
        for r in results
        if r.get("status") == "completed" and r.get("winner") == "OpenAI"
    )
    draws = sum(
        1
        for r in results
        if r.get("status") == "completed" and r.get("winner") == "Draw"
    )
    errors = sum(1 for r in results if r.get("status") == "error")

    summary = {
        "tournament": "Final Tournament - All Working Games",
        "timestamp": datetime.now().isoformat(),
        "total_games": len(games),
        "completed_games": len(results) - errors,
        "claude_wins": claude_wins,
        "openai_wins": openai_wins,
        "draws": draws,
        "errors": errors,
        "claude_win_rate": (
            claude_wins / (claude_wins + openai_wins)
            if (claude_wins + openai_wins) > 0
            else 0
        ),
        "results": results,
    }

    # Save summary
    with open(output_dir / f"tournament_summary_final_{timestamp}.json", "w") as f:
        json.dump(summary, f, indent=2)

    # Print summary

    # Print detailed results
    for result in results:
        game = result["game"]
        if result["status"] == "completed":
            result["winner"]
        else:
            pass

    return summary


if __name__ == "__main__":
    asyncio.run(run_tournament())
