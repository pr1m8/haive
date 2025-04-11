"""
Engines for the Mastermind game.

This module contains the engines for the Mastermind game,
including the codemaker engine, guess engines, and analyzer engines.
"""
from src.haive.core.engine.aug_llm import AugLLMConfig
from src.haive.core.models.llm.base import AzureLLMConfig
from langchain_core.prompts import ChatPromptTemplate
from src.haive.games.mastermind.models import MastermindGuess, MastermindAnalysis, ColorCode
from typing import List
def generate_codemaker_prompt() -> ChatPromptTemplate:
    """Generate a prompt for creating a secret code in Mastermind.

    This function constructs a prompt template for the codemaker engine,
    which generates a secret code for the Mastermind game.
    """
    return ChatPromptTemplate.from_messages([
        ('system', 
            "You are the codemaker in a game of Mastermind. Your task is to create a secret code "
            "that will be challenging for the codebreaker to guess.\n\n"
            "The code consists of 4 colors chosen from: red, blue, green, yellow, purple, and orange. "
            "Colors can be repeated."
        ),
        ('human', 
            "Create a secret code of 4 colors for a Mastermind game. "
            "Think about how to make this code challenging. "
            "Return your answer as a list of 4 colors (from red, blue, green, yellow, purple, orange)."
        )
    ])

def generate_guess_prompt(player: str) -> ChatPromptTemplate:
    """Generate a prompt for making a guess in Mastermind.

    This function constructs a prompt template for the guess engine,
    which generates a guess for the Mastermind game.
    """
    return ChatPromptTemplate.from_messages([
        ('system', 
            f"You are playing as {player} (the codebreaker) in a game of Mastermind. "
            f"Your goal is to guess the secret code in as few turns as possible.\n\n"
            f"Rules:\n"
            f"1. The secret code consists of 4 colors chosen from: red, blue, green, yellow, purple, and orange.\n"
            f"2. Colors can be repeated in the code.\n"
            f"3. After each guess, you receive feedback on the number of pegs that are:\n"
            f"   - The correct color in the correct position (🎯)\n"
            f"   - The correct color but in the wrong position (🔄)\n"
            f"4. You have a maximum of {'{max_turns}'} turns to guess the code."
        ),
        ('human', 
            "Current Game State:\n"
            "{board_string}\n\n"
            "Turn: {current_turn_number}/{max_turns}\n"
            "Previous guesses and feedback:\n{guess_history}\n\n"
            "Previous analysis (if any):\n{player_analysis}\n\n"
            "Make your guess by selecting 4 colors from: red, blue, green, yellow, purple, orange.\n"
            "Explain your reasoning and return a MastermindGuess object with your colors and player."
        )
    ])

def generate_analysis_prompt(player: str) -> ChatPromptTemplate:
    """Generate a prompt for analyzing a Mastermind position.

    This function constructs a prompt template for the analyzer engine,
    which analyzes the current game state from the perspective of the specified player.
    """
    return ChatPromptTemplate.from_messages([
        ('system', 
            f"You are a Mastermind strategy expert. Analyze the game state from {player}'s perspective.\n\n"
            f"Key Mastermind concepts:\n"
            f"- Process of elimination: Use feedback to eliminate impossible combinations\n"
            f"- Information theory: Make guesses that will yield maximum information\n"
            f"- Pattern recognition: Look for patterns in feedback across multiple guesses\n"
            f"- Swaszek strategy: Start with guesses that contain repeated colors"
        ),
        ('human', 
            "Current Game State:\n"
            "Turn: {current_turn_number}/{max_turns}\n"
            "Previous guesses and feedback:\n{guess_history}\n\n"
            "Based on the current game state, analyze:\n"
            "1. What possible color combinations remain?\n"
            "2. Which colors are most likely part of the solution?\n"
            "3. Which positions are you confident about?\n"
            "4. What strategy would be most effective now?\n"
            "5. What should the next guess be?\n\n"
            "Provide a detailed analysis that will help make an optimal next guess."
        )
    ])

# Define the AugLLM configurations
mastermind_engines = {
    "codemaker": AugLLMConfig(
        name="codemaker",
        llm_config=AzureLLMConfig(model="gpt-4o", parameters={"temperature": 0.7}),
        prompt_template=generate_codemaker_prompt(),
        structured_output_model=ColorCode
    ),
    "player1_guesser": AugLLMConfig(
        name="player1_guesser",
        llm_config=AzureLLMConfig(model="gpt-4o", parameters={"temperature": 0.3}),
        prompt_template=generate_guess_prompt("player1"),
        structured_output_model=MastermindGuess
    ),
    "player2_guesser": AugLLMConfig(
        name="player2_guesser",
        llm_config=AzureLLMConfig(model="gpt-4o", parameters={"temperature": 0.3}),
        prompt_template=generate_guess_prompt("player2"),
        structured_output_model=MastermindGuess
    ),
    "player1_analyzer": AugLLMConfig(
        name="player1_analyzer",
        llm_config=AzureLLMConfig(model="gpt-4o", parameters={"temperature": 0.2}),
        prompt_template=generate_analysis_prompt("player1"),
        structured_output_model=MastermindAnalysis
    ),
    "player2_analyzer": AugLLMConfig(
        name="player2_analyzer",
        llm_config=AzureLLMConfig(model="gpt-4o", parameters={"temperature": 0.2}),
        prompt_template=generate_analysis_prompt("player2"),
        structured_output_model=MastermindAnalysis
    )
}