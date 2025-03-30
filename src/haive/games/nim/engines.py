
from src.haive.core.engine.aug_llm import AugLLMConfig
from src.haive.core.aug_llm.azure import AzureLLMConfig
from langchain_core.prompts import ChatPromptTemplate
from src.haive.games.framework.base.config import GameConfig
from src.haive.games.framework.base.agent import GameAgent
from src.haive.games.nim.models import NimMove, NimAnalysis, NimState


    
def generate_move_prompt(player: str) -> ChatPromptTemplate:
    """Generate a prompt for making a move in Nim."""
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
            "Choose one of the available legal moves. Provide your reasoning and return a move object."
        )
    ])

def generate_analysis_prompt(player: str) -> ChatPromptTemplate:
    """Generate a prompt for analyzing a Nim position."""
    return ChatPromptTemplate.from_messages([
        ('system', 
            f"You are a Nim strategy expert. Analyze the position from {player}'s perspective.\n\n"
            f"In standard Nim, the optimal strategy involves the nim-sum (XOR sum of pile sizes). A position is winning if the nim-sum is non-zero."
            f"In misere Nim (last player loses), the same applies except in the endgame with small piles."
        ),
        ('human', 
            "Current Game State:\n"
            "{board_string}\n\n"
            f"Analyze the position for {player}.\n\n"
            "Recent Moves:\n{move_history}\n\n"
            "Provide a detailed analysis including:\n"
            "1. The nim-sum of the position\n"
            "2. Whether this is a winning or losing position\n"
            "3. The optimal move if available\n"
            "4. Strategic explanation"
        )
    ])

# Define the AugLLM configurations
aug_llm_configs = {
    "player1_player": AugLLMConfig(
        name="player1_player",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        prompt_template=generate_move_prompt("player1"),
        structured_output_model=NimMove
    ),
    "player2_player": AugLLMConfig(
        name="player2_player",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        prompt_template=generate_move_prompt("player2"),
        structured_output_model=NimMove
    ),
    "player1_analyzer": AugLLMConfig(
        name="player1_analyzer",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        prompt_template=generate_analysis_prompt("player1"),
        structured_output_model=NimAnalysis
    ),
    "player2_analyzer": AugLLMConfig(
        name="player2_analyzer",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        prompt_template=generate_analysis_prompt("player2"),
        structured_output_model=NimAnalysis
    ),
}
