"""
Prompt generation and engine configuration for Tic Tac Toe agents.

This module defines prompt templates and model configurations for both move generation and board analysis.
These are used by agents to communicate with LLMs in a structured and strategic way.
"""

from src.haive.core.engine.aug_llm import AugLLMConfig
from src.haive.core.models.llm.base import AzureLLMConfig
from langchain_core.prompts import ChatPromptTemplate
from src.haive.games.tic_tac_toe.models import TicTacToeMove, TicTacToeAnalysis

def generate_move_prompt(player_symbol: str) -> ChatPromptTemplate:
    """
    Generate a prompt template for making a move in Tic Tac Toe.

    Args:
        player_symbol (str): The symbol ('X' or 'O') for which to generate the prompt.

    Returns:
        ChatPromptTemplate: A structured prompt for move generation.
    """
    return ChatPromptTemplate.from_messages([
        ('system',
            f"You are playing as {player_symbol} in a game of Tic Tac Toe. "
            f"Your goal is to get three of your symbols in a row (horizontally, vertically, or diagonally).\n\n"
            f"Rules:\n"
            f"1. Players take turns placing their symbol (X or O) on the board.\n"
            f"2. The first player to get three of their symbols in a row wins.\n"
            f"3. If the board fills up with neither player getting three in a row, the game is a draw."
        ),
        ('human',
            "Current Board:\n"
            "{board_string}\n\n"
            "It's your turn ({current_player}).\n\n"
            "Legal moves (row, col):\n{legal_moves}\n\n"
            "Previous analysis (if available):\n{player_analysis}\n\n"
            "Choose one of the legal moves. Explain your reasoning and return a TicTacToeMove object with your row, col, and player."
        )
    ])

def generate_analysis_prompt(player_symbol: str) -> ChatPromptTemplate:
    """
    Generate a prompt template for analyzing a board position in Tic Tac Toe.

    Args:
        player_symbol (str): The symbol ('X' or 'O') for the analyzing player.

    Returns:
        ChatPromptTemplate: A structured prompt for board analysis.
    """
    return ChatPromptTemplate.from_messages([
        ('system',
            f"You are a Tic Tac Toe strategy expert. Analyze the position from the perspective of player {player_symbol}.\n\n"
            f"Key Tic Tac Toe concepts:\n"
            f"- Win: Complete a line of three of your symbols\n"
            f"- Block: Prevent your opponent from completing a line\n"
            f"- Fork: Create two winning threats simultaneously\n"
            f"- Center control: The center position (1,1) is strategically valuable\n"
            f"- Corner play: Corner positions are more valuable than edge positions\n"
            f"- Evaluate the position: Is it winning, losing, or drawing?\n"
        ),
        ('human',
            "Current Board:\n"
            "{board_string}\n\n"
            "Player: {player_symbol}\n"
            "Opponent: {opponent_symbol}\n\n"
            "Analyze this position. Consider the following:\n"
            "1. Are there any immediate winning moves?\n"
            "2. Are there any moves you need to make to block your opponent's win?\n"
            "3. Can you create a fork (two simultaneous winning ways)?\n"
            "4. What is the best strategic move?\n"
            "5. Provide an overall evaluation of the position\n\n"
            "Provide a detailed analysis including specific moves by coordinates (row, col) and your reasoning behind each one."
        )
    ])

# Define the AugLLM configurations for all game agents

#: Dictionary of LLM engine configurations for move generation and analysis.
tictactoe_engines = {
    "X_player": AugLLMConfig(
        name="X_player",
        llm_config=AzureLLMConfig(model="gpt-4o", parameters={"temperature": 0.3}),
        prompt_template=generate_move_prompt("X"),
        structured_output_model=TicTacToeMove
    ),
    "O_player": AugLLMConfig(
        name="O_player",
        llm_config=AzureLLMConfig(model="gpt-4o", parameters={"temperature": 0.3}),
        prompt_template=generate_move_prompt("O"),
        structured_output_model=TicTacToeMove
    ),
    "X_analyzer": AugLLMConfig(
        name="X_analyzer",
        llm_config=AzureLLMConfig(model="gpt-4o", parameters={"temperature": 0.2}),
        prompt_template=generate_analysis_prompt("X"),
        structured_output_model=TicTacToeAnalysis
    ),
    "O_analyzer": AugLLMConfig(
        name="O_analyzer",
        llm_config=AzureLLMConfig(model="gpt-4o", parameters={"temperature": 0.2}),
        prompt_template=generate_analysis_prompt("O"),
        structured_output_model=TicTacToeAnalysis
    )
}