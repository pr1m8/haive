from langchain_core.prompts import ChatPromptTemplate
from src.haive.core.engine.aug_llm import AugLLMConfig
from src.haive.core.models.llm.base import AzureLLMConfig
from src.haive.games.checkers.models import CheckersPlayerDecision, CheckersAnalysis
from typing import Dict
# ------------------------------
# 📊 Move Prompt
# ------------------------------
def generate_move_prompt(color: str) -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages([
        ('system', 
            f"You are the {color} player in a game of checkers. Your goal is to play the best possible move according to strategy. "
            "Ensure your move is legal and follows checkers rules."
        ),
        ('human', 
            "Game Board:\n{board}\n\n"
            f"You are playing as {color}. It's {{turn}}'s turn.\n\n"
            "Legal Moves Available:\n{legal_moves}\n\n"
            "Captured Pieces:\n- Red: {captured_red}\n- Black: {captured_black}\n\n"
            "Recent Moves:\n{move_history}\n\n"
            "Your Analysis: {player_analysis}\n\n"
            f"Select the best move for {color}. Provide your reasoning."
        )
    ])


# ------------------------------
# 📊 Analysis Prompt
# ------------------------------
def generate_analysis_prompt(color: str) -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages([
        ('system', f"You are a checkers analysis expert. Analyze the position from {color}'s perspective."),
        ('human',
            "Game Board:\n{board}\n\n"
            f"Analyze the position for {color}. It's {{turn}}'s turn.\n\n"
            "Captured Pieces:\n- Red: {captured_red}\n- Black: {captured_black}\n\n"
            "Recent Moves:\n{move_history}\n\n"
            "Provide a detailed analysis including:\n"
            "1. Material advantage\n"
            "2. Control of center\n"
            "3. King count\n"
            "4. Mobility assessment\n"
            "5. Threatened pieces\n"
            "6. Strategic recommendations"
        )
    ])

# ------------------------------
# 📊 AugLLM Configurations
# ------------------------------
def build_checkers_aug_llms() -> Dict[str, AugLLMConfig]:
    return {
        "red_player": AugLLMConfig(
            name="red_player",
            llm_config=AzureLLMConfig(model="gpt-4o"),
        prompt_template=generate_move_prompt("red"),
        structured_output_model=CheckersPlayerDecision
        ),
        "black_player": AugLLMConfig(
            name="black_player",
            llm_config=AzureLLMConfig(model="gpt-4o"),
            prompt_template=generate_move_prompt("black"),
            structured_output_model=CheckersPlayerDecision
        ),
        "red_analyzer": AugLLMConfig(
            name="red_analyzer",
            llm_config=AzureLLMConfig(model="gpt-4o"),
            prompt_template=generate_analysis_prompt("red"),
            structured_output_model=CheckersAnalysis
        ),
        "black_analyzer": AugLLMConfig(
            name="black_analyzer",
            llm_config=AzureLLMConfig(model="gpt-4o"),
            prompt_template=generate_analysis_prompt("black"),
            structured_output_model=CheckersAnalysis
        )
    }
