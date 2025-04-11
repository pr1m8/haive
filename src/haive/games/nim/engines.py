"""
Engines for the Nim game.
"""
from src.haive.core.engine.aug_llm import AugLLMConfig
from src.haive.core.models.llm.base import AzureLLMConfig
from langchain_core.prompts import ChatPromptTemplate
from src.haive.games.nim.models import NimMove, NimAnalysis

def generate_move_prompt(player: str, misere_mode: bool) -> ChatPromptTemplate:
    """Generate a prompt for making a move in Nim.

    Args:
        player (str): The player to generate the prompt for.
        misere_mode (bool): Whether to use misere mode.
    """
    return ChatPromptTemplate.from_messages([
        ('system', 
             f"You are the {player} in a game of Nim. Your goal is to take the last stone {'(Standard Nim)' if not '{misere_mode}' else '(Misere Nim, avoid taking the last stone)'}.\n\n"
             f"Rules:\n"
             f"1. Players take turns removing stones from piles.\n"
             f"2. On your turn, you must take at least one stone, and you can take any number of stones from a single pile.\n"
             f"3. The player who takes the last stone {'wins (Standard Nim)' if not '{misere_mode}' else 'loses (Misere Nim)'}."
        ),
        ('human', 
             "Current Game State:\n"
             "{board_string}\n\n"
             f"You are playing as {player}. It's your turn.\n\n"
             "Legal Moves Available:\n{legal_moves}\n\n"
             "Recent Moves:\n{move_history}\n\n"
             "Choose one of the available legal moves. Provide your reasoning and return a move object. "
             "Consider the nim-sum strategy if you are familiar with it."
        )
    ])

from langchain_core.prompts import ChatPromptTemplate

def generate_analysis_prompt(player_symbol: str) -> ChatPromptTemplate:
    """Generate a prompt for analyzing a Reversi/Othello position with structured output."""
    player_color = "Black" if player_symbol == "B" else "White"
    opponent_symbol = "W" if player_symbol == "B" else "B"
    opponent_color = "White" if player_symbol == "B" else "Black"

    return ChatPromptTemplate.from_messages([
        ('system',
            f"You are a Reversi/Othello strategy expert analyzing the board from the perspective of player '{player_symbol}' ({player_color}). "
            f"Your goal is to evaluate the current position and provide a structured analysis using all key strategic metrics."
        ),
        ('human',
            "Current Board:\n{board_string}\n\n"
            "Player: {player_symbol} ({player_color})\n"
            "Opponent: {opponent_symbol} ({opponent_color})\n\n"
            "Legal moves (row, col): {legal_moves}\n"
            "Disc count: Black: {black_count}, White: {white_count}\n\n"
            "Please analyze the position and return a JSON object with the following fields:\n"
            "- mobility (int): number of legal moves for the player\n"
            "- frontier_discs (int): number of discs adjacent to empty squares\n"
            "- corner_discs (int): number of corner positions held by the player\n"
            "- stable_discs (int): number of discs that cannot be flipped\n"
            "- positional_score (int): heuristic score based on board control\n"
            "- position_evaluation (str): one of ['winning', 'losing', 'equal', 'unclear']\n"
            "- recommended_moves (list of {{'row': int, 'col': int}}): best next moves\n"
            "- danger_zones (list of {{'row': int, 'col': int}}): positions to avoid\n"
            "- strategy (str): concise summary of your strategic plan\n"
            "- reasoning (str): detailed explanation justifying your evaluation and suggestions\n\n"
            "Respond only with the JSON object matching this structure."
        )
    ])

# Define the AugLLM configurations
default_nim_engines = {
    "player1_player": AugLLMConfig(
        name="player1_player",
        llm_config=AzureLLMConfig(model="gpt-4o", parameters={"temperature": 0.7}),
        prompt_template=generate_move_prompt("player1"),
        structured_output_model=NimMove
    ),
    "player2_player": AugLLMConfig(
        name="player2_player",
        llm_config=AzureLLMConfig(model="gpt-4o", parameters={"temperature": 0.7}),
        prompt_template=generate_move_prompt("player2"),
        structured_output_model=NimMove
    ),
    "player1_analyzer": AugLLMConfig(
        name="player1_analyzer",
        llm_config=AzureLLMConfig(model="gpt-4o", parameters={"temperature": 0.2}),
        prompt_template=generate_analysis_prompt("player1"),
        structured_output_model=NimAnalysis
    ),
    "player2_analyzer": AugLLMConfig(
        name="player2_analyzer",
        llm_config=AzureLLMConfig(model="gpt-4o", parameters={"temperature": 0.2}),
        prompt_template=generate_analysis_prompt("player2"),
        structured_output_model=NimAnalysis
    )
}