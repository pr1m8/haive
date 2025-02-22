from src.haive.core.aug_llm.base import AugLLMConfig
from langchain_core.prompts import ChatPromptTemplate
from src.haive.agents.agent_games.go.models import GoPlayerDecision, GoAnalysis

# 🔄 **Reusable Prompt Structure**
def generate_go_move_prompt(color: str) -> ChatPromptTemplate:
    """Generates a move prompt for a given color (black or white)."""
    return ChatPromptTemplate.from_messages([
        ('system', 
            f"You are the {color} player in a game of Go. Your goal is to play the best possible move according to strategy.\n"
            "Ensure your move is legal and follows Go rules, provided as **(row, col)** coordinates."
        ),
        ('human', 
            "📌 **Game Context for {color}:**\n"
            "🔲 **Board Size:** {board_size}x{board_size}\n"
            "📝 **Move History (Last 5 Moves):** {recent_moves}\n"
            "🎯 **Captured Stones:** {captured_stones}\n\n"
            "🔍 **Your Last {color} Analysis:** {player_analysis}\n"
            "⚠️ **Opponent's Plans Are Hidden** (You only see your perspective)\n\n"
            f"💡 **Your Turn! Choose the best move for {color}** as **(row, col)** coordinates."
        )
    ])


def generate_go_analysis_prompt(color: str) -> ChatPromptTemplate:
    """Generates an analysis prompt for a given color (black or white)."""
    return ChatPromptTemplate.from_messages([
        ('system', 
            f"You are analyzing {color}'s position in a game of Go. Your task is to evaluate the strategic outlook."
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
