"""
Engines for the Fox and Geese game.

This module defines the engines for the Fox and Geese game,
which includes the move and analysis prompts.
"""
from src.haive.core.engine.aug_llm import AugLLMConfig
from src.haive.core.models.llm.base import AzureLLMConfig
from langchain_core.prompts import ChatPromptTemplate
from src.haive.games.fox_and_geese.models import FoxAndGeeseMove, FoxAndGeesePosition,  FoxAndGeeseAnalysis

def generate_fox_move_prompt() -> ChatPromptTemplate:
    """Generate a prompt for the fox to make a move.

    This function constructs a prompt template for the fox move engine,
    which generates a move for the Fox and Geese game.
    """
    return ChatPromptTemplate.from_messages([
        ('system', 
            "You are the fox in a game of Fox and Geese. Your goal is to capture geese until fewer than 4 remain.\n\n"
            "Rules:\n"
            "1. You can move diagonally in any direction to an empty square.\n"
            "2. You can also capture a goose by jumping over it diagonally, landing on an empty square.\n"
            "3. You win if you reduce the number of geese to fewer than 4.\n"
            "4. The geese win if they trap you with no legal moves."
        ),
        ('human', 
            "Current Board:\n{board_string}\n\n"
            "It's your turn to move the fox.\n\n"
            "Legal Moves:\n{legal_moves}\n\n"
            "Recent Move History:\n{move_history}\n\n"
            "Choose a move for the fox. Analyze the position and explain your strategic thinking. "
            "Return a FoxAndGeeseMove object in the correct format."
        )
    ])

def generate_geese_move_prompt() -> ChatPromptTemplate:
    """Generate a prompt for the geese to make a move.

    This function constructs a prompt template for the geese move engine,
    which generates a move for the Fox and Geese game.
    """
    return ChatPromptTemplate.from_messages([
        ('system', 
            "You are controlling the geese in a game of Fox and Geese. Your goal is to trap the fox so it has no legal moves.\n\n"
            "Rules:\n"
            "1. Geese can only move diagonally forward (downward).\n"
            "2. Geese cannot move backward.\n"
            "3. The fox can jump over and capture geese.\n"
            "4. You win if you trap the fox with no legal moves.\n"
            "5. The fox wins if it reduces the number of geese to fewer than 4."
        ),
        ('human', 
            "Current Board:\n{board_string}\n\n"
            "It's your turn to move one of your geese.\n\n"
            "Legal Moves:\n{legal_moves}\n\n"
            "Recent Move History:\n{move_history}\n\n"
            "Choose a move for one of your geese. Analyze the position and explain your strategic thinking. "
            "Return a FoxAndGeeseMove object in the correct format."
        )
    ])

def generate_fox_analysis_prompt() -> ChatPromptTemplate:
    """Generate a prompt for analyzing the Fox's position.

    This function constructs a prompt template for the fox analysis engine,
    which analyzes the current game state from the perspective of the fox player.
    """
    return ChatPromptTemplate.from_messages([
        ('system', 
            "You are a Fox expert in Fox and Geese. Analyze the current position from the perspective of the fox player.\n\n"
            "In Fox and Geese:\n"
            "- The fox wins by capturing geese until fewer than 4 remain\n"
            "- The geese win by trapping the fox with no legal moves\n"
            "- The fox can move diagonally in any direction and can capture by jumping\n"
            "- Geese can only move diagonally forward (downward)\n"
        ),
        ('human', 
            "Current Board:\n{board_string}\n\n"
            "Current Turn: {turn}\n\n"
            "Recent Move History:\n{move_history}\n\n"
            "Analyze this position from the fox's perspective. Consider:\n"
            "1. What is the fox's advantage level?\n"
            "2. What are the critical squares or formations for the fox?\n"
            "3. What is the recommended strategy for the fox?\n"
            "4. Any potential threats from the geese?\n"
            "Provide your analysis and strategy for the fox."
        )
    ])

def generate_geese_analysis_prompt() -> ChatPromptTemplate:
    """Generate a prompt for analyzing the Geese's position.

    This function constructs a prompt template for the geese analysis engine,
    which analyzes the current game state from the perspective of the geese player.
    """
    return ChatPromptTemplate.from_messages([
        ('system', 
            "You are an expert controlling the geese in Fox and Geese. Analyze the current position from the perspective of the geese player.\n\n"
            "In Fox and Geese:\n"
            "- The fox wins by capturing geese until fewer than 4 remain\n"
            "- The geese win by trapping the fox with no legal moves\n"
            "- The fox can move diagonally in any direction and can capture by jumping\n"
            "- Geese can only move diagonally forward (downward)\n"
        ),
        ('human', 
            "Current Board:\n{board_string}\n\n"
            "Current Turn: {turn}\n\n"
            "Recent Move History:\n{move_history}\n\n"
            "Analyze this position from the geese's perspective. Consider:\n"
            "1. What is the geese's advantage level?\n"
            "2. What are the key strategic features for the geese?\n"
            "3. What is the recommended strategy for the geese?\n"
            "4. Any potential threats from the fox?\n"
            "Provide your analysis and strategy for the geese."
        )
    ])
fox_and_geese_engines = {
    "fox_player": AugLLMConfig(
        name="fox_player",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        prompt_template=generate_fox_move_prompt(),
        structured_output_model=FoxAndGeeseMove
    ),
    "geese_player": AugLLMConfig(
        name="geese_player",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        prompt_template=generate_geese_move_prompt(),
        structured_output_model=FoxAndGeeseMove
    ),
    "fox_analysis": AugLLMConfig(
        name="fox_analysis",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        prompt_template=generate_fox_analysis_prompt(),
        structured_output_model=FoxAndGeeseAnalysis
    ),
    "geese_analysis": AugLLMConfig(
        name="geese_analysis",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        prompt_template=generate_geese_analysis_prompt(),
        structured_output_model=FoxAndGeeseAnalysis
    )
}
