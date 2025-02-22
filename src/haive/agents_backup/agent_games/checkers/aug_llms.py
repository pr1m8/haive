from src.haive.core.aug_llm.base import AugLLMConfig
from langchain_core.prompts import ChatPromptTemplate
from src.haive.agents.agent_games.checkers.models import CheckersMove, CheckersPlayerAnalysis

# 🔄 **Reusable Prompt Structure**
def generate_move_prompt(color: str) -> ChatPromptTemplate:
    """Generates a move prompt for a given color (red or black)."""
    return ChatPromptTemplate.from_messages([
        ('system', 
            f"You are the {color} player in a game of Checkers. Your goal is to make the best possible move according to Checkers strategy.\n"
            "Provide your move as starting and ending coordinates in the format (start_row, start_col) -> (end_row, end_col)."
        ),
        ('human', 
            "📌 **Game Context for {color}:**\n"
            "🔲 **Current Board State:**\n{board_visual}\n"
            "📝 **Move History (Last 5 Moves):** {recent_moves}\n"
            "🎯 **Captured Pieces:** {captured_pieces}\n\n"
            "🔍 **Your Last {color} Analysis:** {player_analysis}\n"
            "⚠️ **Opponent's Plans Are Hidden** (You only see your perspective)\n\n"
            f"💡 **Your Turn! Choose the best move for {color}** in the format (start_row, start_col) -> (end_row, end_col)."
        )
    ])
def generate_analysis_prompt(color: str) -> ChatPromptTemplate:
    """Generates an analysis prompt for a given color (red or black)."""
    return ChatPromptTemplate.from_messages([
        ('system', 
            f"You are analyzing the position for the {color} player in a Checkers game. Your task is to evaluate the strategic outlook."
        ),
        ('human', 
            f"📌 **Game Analysis for {color}:**\n"
            "🔲 **Current Board State:**\n{board_visual}\n"
            "📝 **Move History (Last 5 Moves):** {recent_moves}\n"
            "🎯 **Captured Pieces:** {captured_pieces}\n\n"
            "📝 **Your Task:**\n"
            f"1️⃣ Assess {color}'s overall **position strength**.\n"
            f"2️⃣ Identify key **strategic themes** for {color}.\n"
            "3️⃣ Suggest optimal **next moves** and long-term plans."
        )
    ])

# ✅ **Final Augmented LLM Configurations**
aug_llm_configs = {
    "red_player": AugLLMConfig(
        name="red_player",
        prompt_template=generate_move_prompt("red"),
        structured_output_model=CheckersMove
    ),
    "black_player": AugLLMConfig(
        name="black_player",
        prompt_template=generate_move_prompt("black"),
        structured_output_model=CheckersMove
    ),
    "red_analyzer": AugLLMConfig(
        name="red_analyzer",
        prompt_template=generate_analysis_prompt("red"),
        structured_output_model=CheckersPlayerAnalysis
    ),
    "black_analyzer": AugLLMConfig(
        name="black_analyzer",
        prompt_template=generate_analysis_prompt("black"),
        structured_output_model=CheckersPlayerAnalysis
    )
}
