"""
Engines for the Clue game.

This module contains the engines for the Clue game,
including the player engines, guess engines, and analysis engines.
"""
from src.haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.prompts import ChatPromptTemplate
from typing import Dict
from src.haive.games.clue.models import ClueGuess, ClueResponse, ClueHypothesis

def generate_player_prompt() -> ChatPromptTemplate:
    """Generate a prompt for playing Clue.

    This function constructs a prompt template for the player engine,
    which makes guesses in the Clue game.
    """
    return ChatPromptTemplate.from_messages([
        ('system', 
            "You are playing the Clue (Cluedo) board game. Your goal is to figure out who committed "
            "the murder, with what weapon, and in which room.\n\n"
            "The game is played by making guesses and analyzing the responses from other players. "
            "Through process of elimination, you can narrow down the possible solutions.\n\n"
            "You will respond with a ClueGuess object. Make sure to use the exact enum values from "
            "ValidSuspect, ValidWeapon, and ValidRoom classes."
        ),
        ('human', 
            "Current Game State:\n"
            "{board_string}\n\n"
            "Turn: {current_turn_number}/{max_turns}\n"
            "Your cards: {player_cards}\n"
            "Previous guesses and responses: {guess_history}\n\n"
            "Based on the information available, make a guess about who committed the murder, "
            "with what weapon, and in which room.\n\n"
            "Return your guess as a ClueGuess object with the suspect, weapon, room, and your player name."
        )
    ])

def generate_analysis_prompt() -> ChatPromptTemplate:
    """Generate a prompt for analyzing Clue game state.

    This function constructs a prompt template for the analysis engine,
    which analyzes the current game state and provides insights.
    """
    return ChatPromptTemplate.from_messages([
        ('system', 
            "You are a Clue (Cluedo) game expert. Analyze the current game state and "
            "determine the most likely solution based on the available information.\n\n"
            "Use logical deduction and process of elimination to narrow down the possibilities.\n\n"
            "You will respond with a ClueHypothesis object containing your analysis of possible solutions."
        ),
        ('human', 
            "Current Game State:\n"
            "Turn: {current_turn_number}/{max_turns}\n"
            "Your cards: {player_cards}\n"
            "Previous guesses and responses: {guess_history}\n\n"
            "Based on the current game state, analyze:\n"
            "1. Which suspects, weapons, and rooms can be eliminated?\n"
            "2. What is the most likely solution based on the evidence?\n"
            "3. What should be the next guess?\n\n"
            "Provide your analysis as a ClueHypothesis object with possible suspects, weapons, rooms, "
            "confidence level (0.0-1.0), and detailed reasoning."
        )
    ])

# Define engine configs
clue_engines: Dict[str, AugLLMConfig] = {
    "player1_player": AugLLMConfig(
        name="player1_player",
        prompt_template=generate_player_prompt(),
        output_key="guess"
    ),
    "player2_player": AugLLMConfig(
        name="player2_player",
        prompt_template=generate_player_prompt(),
        output_key="guess"
    ),
    "player1_analyzer": AugLLMConfig(
        name="player1_analyzer",
        prompt_template=generate_analysis_prompt(),
        output_key="analysis"
    ),
    "player2_analyzer": AugLLMConfig(
        name="player2_analyzer",
        prompt_template=generate_analysis_prompt(),
        output_key="analysis"
    )
} 