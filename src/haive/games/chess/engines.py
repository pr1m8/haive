"""
Chess game augmented LLM configurations module.

This module provides LLM configurations for the chess game, including:
    - Move generation prompts for players
    - Position analysis prompts
    - Structured output models
"""

from typing import Dict, Optional
from langchain_core.prompts import ChatPromptTemplate
from src.haive.core.aug_llm.base import AugLLMConfig
from src.haive.core.models.llm.base import AzureLLMConfig

from .models import ChessPlayerDecision, ChessAnalysis, SegmentedAnalysis

def generate_move_prompt(color: str) -> ChatPromptTemplate:
    """
    Generate a prompt for move selection.
    
    Args:
        color: Player color ("white" or "black")
        
    Returns:
        ChatPromptTemplate: Template for move selection
    """
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
            "🔍 **Your Last Analysis:** {player_analysis}\n"
            "⚠️ **Opponent's Plans Are Hidden** (You only see your perspective)\n\n"
            f"💡 **Your Turn! Choose the best move for {color}** in **UCI format** (e.g., e2e4, d2d4, etc.)."
        )
    ])

def generate_analysis_prompt(color: str) -> ChatPromptTemplate:
    """
    Generate a prompt for position analysis.
    
    Args:
        color: Player color ("white" or "black")
        
    Returns:
        ChatPromptTemplate: Template for position analysis
    """
    return ChatPromptTemplate.from_messages([
        ('system', 
            f"You are analyzing {color}'s position in a chess game. Your task is to evaluate the strategic outlook."
        ),
        ('human', 
            "📌 **Game Analysis for {color}:**\n"
            "♟️ **Current Board Position (FEN):** {current_board_fen}\n"
            "🕰️ **Previous Board Position (FEN):** {previous_board_fen}\n"
            "📜 **Recent Moves:** {recent_moves}\n"
            "🎯 **Captured Pieces:** {captured_pieces}\n\n"
            "📝 **Your Task:**\n"
            "1️⃣ Assess {color}'s overall **position strength**.\n"
            "2️⃣ Identify key **strategic themes** for {color}.\n"
            "3️⃣ Suggest optimal **next moves** and long-term plans."
        )
    ])

def build_chess_aug_llms() -> Dict[str, AugLLMConfig]:
    """
    Build LLM configs for chess players and analyzers.
    
    This function creates AugLLMConfig objects for:
        - White player move generation
        - Black player move generation
        - White position analysis
        - Black position analysis
    
    Returns:
        Dict[str, AugLLMConfig]: Dictionary of LLM configurations
    """
    # Default LLM configuration
    default_llm_config = AzureLLMConfig(
        model="gpt-4o",
        parameters={"temperature": 0.7}
    )
    
    return {
        "white_player": AugLLMConfig(
            name="white_player",
            llm_config=default_llm_config,
            prompt_template=generate_move_prompt("white"),
            structured_output_model=ChessPlayerDecision,
            description="White player move generation"
        ),
        "black_player": AugLLMConfig(
            name="black_player",
            llm_config=default_llm_config,
            prompt_template=generate_move_prompt("black"),
            structured_output_model=ChessPlayerDecision,
            description="Black player move generation"
        ),
        "white_analyzer": AugLLMConfig(
            name="white_analyzer",
            llm_config=default_llm_config,
            prompt_template=generate_analysis_prompt("white"),
            structured_output_model=SegmentedAnalysis,
            description="White position analysis"
        ),
        "black_analyzer": AugLLMConfig(
            name="black_analyzer",
            llm_config=default_llm_config,
            prompt_template=generate_analysis_prompt("black"),
            structured_output_model=SegmentedAnalysis,
            description="Black position analysis"
        )
    }