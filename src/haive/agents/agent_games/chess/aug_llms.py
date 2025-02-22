from src.haive.core.aug_llm.base import AugLLMConfig
from langchain_core.prompts import ChatPromptTemplate
from src.haive.agents.agent_games.chess.models import ChessPlayerDecision, SegmentedAnalysis

# 🔄 **Reusable Prompt Structure**
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


# ✅ **Final Augmented LLM Configurations**
aug_llm_configs = {
    "white_player": AugLLMConfig(
        name="white_player",
        prompt_template=generate_move_prompt("white"),
        structured_output_model=ChessPlayerDecision
    ),
    "black_player": AugLLMConfig(
        name="black_player",
        prompt_template=generate_move_prompt("black"),
        structured_output_model=ChessPlayerDecision
    ),
    "white_analyzer": AugLLMConfig(
        name="white_analyzer",
        prompt_template=generate_analysis_prompt("white"),
        structured_output_model=SegmentedAnalysis
    ),
    "black_analyzer": AugLLMConfig(
        name="black_analyzer",
        prompt_template=generate_analysis_prompt("black"),
        structured_output_model=SegmentedAnalysis
    )
}
