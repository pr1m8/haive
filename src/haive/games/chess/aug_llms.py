"""Chess game augmented LLM configurations module.

This module provides augmented LLM configurations for the chess game, including:
    - Move generation prompts for white and black players
    - Position analysis prompts for both sides
    - Structured output models for moves and analysis
    - Pre-configured LLM configurations for easy agent setup

Example:
    >>> from src.haive.games.chess.aug_llms import aug_llm_configs
    >>> 
    >>> # Access white player's move generation configuration
    >>> white_config = aug_llm_configs["white_player"]
    >>> white_prompt = white_config.prompt_template
"""

from typing import Dict, Any, List, Optional
from langchain.prompts import ChatPromptTemplate
from pydantic import BaseModel

from src.haive.core.engine.aug_llm import AugLLMConfig
from src.haive.core.models.llm.base import AzureLLMConfig, DeepSeekLLMConfig, LLMConfig

from .models import (
    ChessPlayerDecision,
    ChessAnalysis,
    ChessMoveModel,
    ChessMoveValidation,
    SegmentedAnalysis
)



def generate_move_prompt(color: str) -> ChatPromptTemplate:
    """Generates a move prompt for a given color (white or black)."""
    return ChatPromptTemplate.from_messages([
        ('system', 
            f"You are the {color} chess player. Your goal is to play the best possible move according to chess strategy.\n"
            "Ensure your move is legal and follows chess rules, provided in **UCI format** (e.g., e2e4, g8f6)."
        ),
        ('human', 
            "📌 **Game Context for {color}:**\n"
            "♟️ **Current Board Position (FEN):** {current_board_fen}\n"
            "🕰️ **Previous Board Position (FEN):** {previous_board_fen}\n"
            "📜 **Move History (Last 5 Moves):** {recent_moves}\n"
            "🎯 **Captured Pieces:** {captured_pieces}\n\n"
            "🔍 **Your Last {color} Analysis:** {player_analysis}\n"
            "⚠️ **Opponent's Plans Are Hidden** (You only see your perspective)\n\n"
            f"💡 **Your Turn! Choose the best move for {color}** in **UCI format** (e.g., e2e4, d2d4, etc.)."
        )
    ])
def generate_analysis_prompt(color: str) -> ChatPromptTemplate:
    """Generates an analysis prompt for a given color (white or black)."""
    return ChatPromptTemplate.from_messages([
        ('system', 
            f"You are analyzing {color}'s position in a chess game. Your task is to evaluate the strategic outlook."
        ),
        ('human', 
            "📌 **Game Analysis for {color}:**\n"
            "♟️ **Current Board Position (FEN):** {current_board_fen}\n"
            "🕰️ **Previous Board Position (FEN):** {previous_board_fen}\n"
            "📜 **Move History (Last 5 Moves):** {recent_moves}\n"
            "🎯 **Captured Pieces:** {captured_pieces}\n\n"
            "📝 **Your Task:**\n"
            "1️⃣ Assess {color}'s overall **position strength**.\n"
            "2️⃣ Identify key **strategic themes** for {color}.\n"
            "3️⃣ Suggest optimal **next moves** and long-term plans."
        )
    ])

def build_chess_aug_llms_per_color(
    *,
    white_llm: Optional[LLMConfig] = AzureLLMConfig(),
    black_llm: Optional[LLMConfig] = DeepSeekLLMConfig(),
) -> Dict[str, AugLLMConfig]:
    print(white_llm)
    print(black_llm)
    """Build LLM configs for both players and analyzers, from per-color LLMs."""
    return {
        "white_player": AugLLMConfig(
            llm_config=white_llm,
            prompt_template=generate_move_prompt("white"),
            structured_output_model=ChessPlayerDecision,
            description="White player move generation"
        ),
        "white_analyzer": AugLLMConfig(
            llm_config=white_llm,
            prompt_template=generate_analysis_prompt("white"),
            structured_output_model=ChessAnalysis,
            description="White position analysis"
        ),
        "black_player": AugLLMConfig(
            llm_config=black_llm,
            prompt_template=generate_move_prompt("black"),
            structured_output_model=ChessPlayerDecision,
            description="Black player move generation"
        ),
        "black_analyzer": AugLLMConfig(
            llm_config=black_llm,
            prompt_template=generate_analysis_prompt("black"),
            structured_output_model=ChessAnalysis,
            description="Black position analysis"
        ),
    }


# Default LLMs fallback
aug_llm_configs: Dict[str, AugLLMConfig] = build_chess_aug_llms_per_color()