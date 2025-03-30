"""Go game LLM augmentations.

This module provides augmented LLM configurations for Go game agents, including:
    - Move generation prompts for black and white players
    - Position analysis prompts for both sides
    - Structured output models for moves and analysis
    - Pre-configured LLM configurations for easy agent setup

Example:
    >>> from src.haive.games.go.aug_llms import aug_llm_configs
    >>> 
    >>> # Get black player's move generation config
    >>> black_config = aug_llm_configs["black_player"]
    >>> 
    >>> # Generate a prompt
    >>> prompt = black_config.prompt_template.format(
    ...     board_size=19,
    ...     recent_moves=[(0, "black", (3, 4))],
    ...     captured_stones={"black": 0, "white": 0},
    ...     player_analysis="Territory is balanced"
    ... )
"""

from typing import Dict, Any, List, Optional
from langchain.prompts import ChatPromptTemplate
from pydantic import BaseModel

from src.haive.core.engine.aug_llm import AugLLMConfig
from src.haive.core.models.llm.base import AzureLLMConfig

from .models import GoPlayerDecision, GoAnalysis

# 🔄 **Reusable Prompt Structure**
def generate_go_move_prompt(color: str) -> ChatPromptTemplate:
    """Generate a move prompt for a Go player.
    
    This function creates a ChatPromptTemplate that guides an LLM to:
        - Play as a specific color in Go
        - Consider the current game context
        - Make legal moves in coordinate format
        - Follow Go strategy and rules
    
    Args:
        color (str): The player color ("black" or "white").
    
    Returns:
        ChatPromptTemplate: A prompt template for move generation.
    
    Example:
        >>> prompt = generate_go_move_prompt("black")
        >>> formatted = prompt.format(
        ...     board_size=19,
        ...     recent_moves=[(0, "black", (3, 4))],
        ...     captured_stones={"black": 0, "white": 0},
        ...     player_analysis="Territory is balanced"
        ... )
    
    Notes:
        The prompt includes:
        - System role definition as the specified color
        - Game context (board size, move history)
        - Captured stones count
        - Previous position analysis
        - Clear instruction for move format
    """
    return ChatPromptTemplate.from_messages([
        ('system', 
            f"You are the {color} player in a game of Go. Your goal is to play "
            "the best possible move according to strategy.\n"
            "Ensure your move is legal and follows Go rules, provided as "
            "**(row, col)** coordinates."
        ),
        ('human', 
            "📌 **Game Context for {color}:**\n"
            "🔲 **Board Size:** {board_size}x{board_size}\n"
            "📝 **Move History (Last 5 Moves):** {recent_moves}\n"
            "🎯 **Captured Stones:** {captured_stones}\n\n"
            "🔍 **Your Last {color} Analysis:** {player_analysis}\n"
            "⚠️ **Opponent's Plans Are Hidden** (You only see your perspective)\n\n"
            f"💡 **Your Turn! Choose the best move for {color}** as **(row, col)** "
            "coordinates."
        )
    ])


def generate_go_analysis_prompt(color: str) -> ChatPromptTemplate:
    """Generate a position analysis prompt for a Go player.
    
    This function creates a ChatPromptTemplate that guides an LLM to:
        - Analyze the position from a specific color's perspective
        - Evaluate territory and influence
        - Identify key positions
        - Suggest strategic plans
    
    Args:
        color (str): The player color ("black" or "white") to analyze for.
    
    Returns:
        ChatPromptTemplate: A prompt template for position analysis.
    
    Example:
        >>> prompt = generate_go_analysis_prompt("black")
        >>> formatted = prompt.format(
        ...     board_size=19,
        ...     recent_moves=[(0, "black", (3, 4))],
        ...     captured_stones={"black": 0, "white": 0}
        ... )
    
    Notes:
        The prompt includes:
        - System role definition as an analyst
        - Game context (board size, move history)
        - Captured stones count
        - Structured analysis tasks:
            1. Territory assessment
            2. Key position identification
            3. Strategic planning
    """
    return ChatPromptTemplate.from_messages([
        ('system', 
            f"You are analyzing {color}'s position in a game of Go. Your task is "
            "to evaluate the strategic outlook."
        ),
        ('human', 
            "📌 **Game Analysis for {color}:**\n"
            "🔲 **Board Size:** {board_size}x{board_size}\n"
            "📝 **Move History (Last 5 Moves):** {recent_moves}\n"
            "🎯 **Captured Stones:** {captured_stones}\n\n"
            "📝 **Your Task:**\n"
            "1️⃣ Assess {color}'s **territory control and influence**.\n"
            "2️⃣ Identify key **strong and weak positions**.\n"
            "3️⃣ Suggest optimal **next moves and strategic plans**."
        )
    ])


# ✅ **Final Augmented LLM Configurations**
aug_llm_configs = {
    "black_player": AugLLMConfig(
        name="black_player",
        prompt_template=generate_go_move_prompt("black"),
        structured_output_model=GoPlayerDecision
    ),
    "white_player": AugLLMConfig(
        name="white_player",
        prompt_template=generate_go_move_prompt("white"),
        structured_output_model=GoPlayerDecision
    ),
    "black_analyzer": AugLLMConfig(
        name="black_analyzer",
        prompt_template=generate_go_analysis_prompt("black"),
        structured_output_model=GoAnalysis
    ),
    "white_analyzer": AugLLMConfig(
        name="white_analyzer",
        prompt_template=generate_go_analysis_prompt("white"),
        structured_output_model=GoAnalysis
    )
}
