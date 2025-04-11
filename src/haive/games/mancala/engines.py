"""
Engines for the Mancala game.

This module defines the engines for the Mancala game,
including the move and analysis prompts.
"""
from src.haive.core.engine.aug_llm import AugLLMConfig
from src.haive.core.models.llm.base import AzureLLMConfig
from langchain_core.prompts import ChatPromptTemplate
from src.haive.games.mancala.models import MancalaMove, MancalaAnalysis

def generate_move_prompt(player: str) -> ChatPromptTemplate:
    """Generate a prompt for making a move in Mancala.

    This function constructs a prompt template for the move engine,
    which generates a move for the Mancala game.
    """
    return ChatPromptTemplate.from_messages([
        ('system', 
            f"You are playing as {player} in a game of Mancala (also known as Kalah). Your goal is to collect more stones than your opponent.\n\n"
            f"Rules:\n"
            f"1. On your turn, you select one of your pits and distribute the stones one by one counterclockwise, including your store but skipping your opponent's store.\n"
            f"2. If your last stone lands in your store, you get a free turn.\n"
            f"3. If your last stone lands in an empty pit on your side, you capture that stone and all stones in the opposite pit.\n"
            f"4. The game ends when all pits on one side are empty. The player with stones remaining adds them to their store.\n"
            f"5. The player with the most stones in their store wins."
        ),
        ('human', 
            "Current Game State:\n"
            "{board_string}\n\n"
            "Turn: {turn}\n"
            "Legal Moves Available:\n{legal_moves}\n\n"
            "Recent Moves:\n{move_history}\n\n"
            "Previous Analysis (if available):\n{player_analysis}\n\n"
            "Choose one of the available legal moves. Provide your reasoning and return a MancalaMove object with the correct pit_index and player."
        )
    ])

def generate_analysis_prompt(player: str) -> ChatPromptTemplate:
    """Generate a prompt for analyzing a Mancala position.

    This function constructs a prompt template for the analysis engine,
    which analyzes the current game state from the perspective of the specified player.
    """
    return ChatPromptTemplate.from_messages([
        ('system', 
            f"You are a Mancala strategy expert. Analyze the position from {player}'s perspective.\n\n"
            f"Key Mancala strategic concepts:\n"
            f"- Stone distribution: Having stones spread among multiple pits is often better than many in one pit\n"
            f"- Free turns: Landing in your store gives an extra turn, creating powerful sequences\n"
            f"- Capture potential: Setting up captures by moving into empty pits on your side\n"
            f"- Endgame: When pits start emptying, careful planning becomes crucial\n"
            f"- Keeping your rightmost pits empty in endgame can force opponent to give you stones"
        ),
        ('human', 
            "Current Game State:\n"
            "{board_string}\n\n"
            "Player: {player}\n"
            "Current scores: Player 1: {player1_score}, Player 2: {player2_score}\n\n"
            "Pit stones (Player 1): {player1_pits}\n"
            "Pit stones (Player 2): {player2_pits}\n\n"
            "Recent Moves:\n{move_history}\n\n"
            "Analyze this position. Consider:\n"
            "1. Overall position evaluation\n"
            "2. Stone distribution analysis\n"
            "3. Capture opportunities\n"
            "4. Free turn possibilities\n"
            "5. Strategic recommendations\n"
            "6. Key tactical considerations"
        )
    ])

# Define the AugLLM configurations
mancala_engines = {
    "player1_player": AugLLMConfig(
        name="player1_player",
        llm_config=AzureLLMConfig(model="gpt-4o", parameters={"temperature": 0.7}),
        prompt_template=generate_move_prompt("player1"),
        structured_output_model=MancalaMove
    ),
    "player2_player": AugLLMConfig(
        name="player2_player",
        llm_config=AzureLLMConfig(model="gpt-4o", parameters={"temperature": 0.7}),
        prompt_template=generate_move_prompt("player2"),
        structured_output_model=MancalaMove
    ),
    "player1_analyzer": AugLLMConfig(
        name="player1_analyzer",
        llm_config=AzureLLMConfig(model="gpt-4o", parameters={"temperature": 0.2}),
        prompt_template=generate_analysis_prompt("player1"),
        structured_output_model=MancalaAnalysis
    ),
    "player2_analyzer": AugLLMConfig(
        name="player2_analyzer",
        llm_config=AzureLLMConfig(model="gpt-4o", parameters={"temperature": 0.2}),
        prompt_template=generate_analysis_prompt("player2"),
        structured_output_model=MancalaAnalysis
    )
}