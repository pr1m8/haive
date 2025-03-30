
# Define the prompts for each agent
from langchain_core.prompts import ChatPromptTemplate
from src.haive.core.engine.aug_llm import AugLLMConfig
from src.haive.core.models.llm.base import AzureLLMConfig
from src.haive.games.dominoes.models import DominoesPlayerDecision, DominoesAnalysis

# ------------------------------
# 📊 Move Prompt
# ------------------------------
def generate_move_prompt(player: str) -> ChatPromptTemplate:
    """Generate a prompt for making a move in dominoes."""
    return ChatPromptTemplate.from_messages([
        ('system', 
            f"You are playing as {player} in a game of dominoes. Your goal is to play strategically to empty your hand first. "
            "Dominoes rules: Match one end of your tile to an open end on the board."
        ),
        ('human', 
            "Game State:\n"
            "- You are {player}\n"
            "- Your Hand: {hand}\n"
            "- Your Pip Count: {pip_count}\n"
            "- Board: {board}\n"
            "- Open Ends: {open_ends}\n"
            "- Boneyard: {boneyard_count} tiles remaining\n"
            "- Opponent Tiles: {opponent_count}\n\n"
            "Legal Moves Available:\n{legal_moves}\n\n"
            "Recent Moves:\n{move_history}\n\n"
            "Your Analysis: {player_analysis}\n\n"
            "Choose the best move. If you need to pass, set pass_turn to true. Explain your reasoning."
        )
    ])

def generate_analysis_prompt(player: str) -> ChatPromptTemplate:
    """Generate a prompt for analyzing a dominoes position."""
    return ChatPromptTemplate.from_messages([
        ('system', 
            f"You are a dominoes strategy expert. Analyze the position for {player}."
        ),
        ('human', 
            "Game State to Analyze:\n"
            "- Player: {player}\n"
            "- Hand: {hand}\n"
            "- Pip Count: {pip_count}\n"
            "- Value Counts: {value_counts}\n"
            "- Board: {board}\n"
            "- Open Ends: {open_ends}\n"
            "- Boneyard: {boneyard_count} tiles remaining\n"
            "- Opponent Tiles: {opponent_count}\n\n"
            "Recent Moves:\n{move_history}\n\n"
            "Provide a detailed analysis including:\n"
            "1. Hand strength (1-10)\n"
            "2. Pip count assessment\n"
            "3. Open end values\n"
            "4. Values you don't have\n"
            "5. Strategic recommendations\n"
            "6. Blocking potential against opponent"
        )
    ])

# Define the AugLLM configurations

aug_llm_configs = {
    "player1_player": AugLLMConfig(
        name="player1_player",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        prompt_template=generate_move_prompt("player1"),
        structured_output_model=DominoesPlayerDecision
    ),
    "player2_player": AugLLMConfig(
        name="player2_player",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        prompt_template=generate_move_prompt("player2"),
        structured_output_model=DominoesPlayerDecision
    ),
    "player1_analyzer": AugLLMConfig(
        name="player1_analyzer",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        prompt_template=generate_analysis_prompt("player1"),
        structured_output_model=DominoesAnalysis
    ),
    "player2_analyzer": AugLLMConfig(
        name="player2_analyzer",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        prompt_template=generate_analysis_prompt("player2"),
        structured_output_model=DominoesAnalysis
    )
}
