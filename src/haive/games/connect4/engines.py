
# src/haive/agents/agent_games/connect4/config.py

from src.haive.games.framework.base.config import GameConfig
from src.haive.games.connect4.models import Connect4Move, Connect4PlayerDecision, Connect4Analysis
from src.haive.core.engine.aug_llm import AugLLMConfig
from src.haive.core.models.llm.base import AzureLLMConfig
from langchain_core.prompts import ChatPromptTemplate
from pydantic import Field
from typing import Dict
import copy

# Define the prompts for each agent

def generate_move_prompt(color: str) -> ChatPromptTemplate:
    """Generate a prompt for making a move in Connect 4."""
    return ChatPromptTemplate.from_messages([
        ('system', 
            f"You are the {color} player in a game of Connect 4. Your goal is to connect four of your pieces in a row, column, or diagonal. "
            "Choose the best column to drop your piece."
        ),
        ('human', 
            "Game Board:\n{board}\n\n"
            f"You are playing as {color}. It's {'your' if '{{turn}}' == '{color}' else 'not your'} turn.\n\n"
            "Legal Moves Available:\n{legal_moves}\n\n"
            "Threats:\n- Winning moves: {threats_winning_moves}\n- Blocking needed: {threats_blocking_moves}\n\n"
            "Recent Moves:\n{move_history}\n\n"
            "Your Analysis: {player_analysis}\n\n"
            f"Select the best column (0-6) for {color}. Provide your reasoning."
        )
    ])

def generate_analysis_prompt(color: str) -> ChatPromptTemplate:
    """Generate a structured and detailed prompt for analyzing a Connect 4 position."""
    return ChatPromptTemplate.from_messages([
        ('system', 
            f"You are a Connect 4 strategy expert, analyzing the board from {color}'s perspective. "
            "Your objective is to provide a structured evaluation of the current position, including scoring, threats, and strategy recommendations."
        ),
        ('human', 
            "🔷 **Game Board State:**\n{board}\n\n"
            f"🎮 **You are playing as {color}.** It's {'your' if '{{turn}}' == '{color}' else 'not your'} turn.\n\n"
            
            "📊 **Threats Analysis:**\n"
            "- **Winning Moves:** {threats_winning_moves}\n"
            "- **Blocking Moves:** {threats_blocking_moves}\n\n"
            
            "🛠 **Board Control Insights:**\n"
            "- **Column Usage:** {columns_usage} (Number of pieces in each column)\n\n"
            
            "🔄 **Recent Move History:**\n{move_history}\n\n"
            
            "📈 **Provide a structured analysis including:**\n"
            "1️⃣ **Position Score:** Evaluate the position from -10 (very bad) to +10 (very strong).\n"
            "2️⃣ **Threat Assessment:** Identify immediate threats, three-in-a-row opportunities, and opponent weaknesses.\n"
            "3️⃣ **Center Control:** Rate control of central columns (0-10, where 10 is perfect control of columns 3 and 4).\n"
            "4️⃣ **Suggested Columns:** List columns in priority order for the best move.\n"
            "5️⃣ **Defensive Recommendations:** Highlight if defensive play is necessary and where.\n"
            "6️⃣ **Winning Probability:** Estimate the likelihood of winning (0-100%).\n\n"
            
            "📝 **Output structured response following this format:**\n"
            "{{ \n"
            '  "position_score": <int>,\n'
            '  "center_control": <int>,\n'
            '  "suggested_columns": [<list of column indices>],\n'
            '  "winning_chances": <int>,\n'
            '  "threats": {{ \n'
            '    "winning_moves": [<list of columns>],\n'
            '    "blocking_moves": [<list of columns>]\n'
            '  }},\n'
            "}}"
        )
    ])



# Define the AugLLM configurations

aug_llm_configs = {
    "red_player": AugLLMConfig(
        name="red_player",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        prompt_template=generate_move_prompt("red"),
        structured_output_model=Connect4PlayerDecision
    ),
    "yellow_player": AugLLMConfig(
        name="yellow_player",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        prompt_template=generate_move_prompt("yellow"),
        structured_output_model=Connect4PlayerDecision
    ),
    "red_analyzer": AugLLMConfig(
        name="red_analyzer",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        prompt_template=generate_analysis_prompt("red"),
        structured_output_model=Connect4Analysis
    ),
    "yellow_analyzer": AugLLMConfig(
        name="yellow_analyzer",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        prompt_template=generate_analysis_prompt("yellow"),
        structured_output_model=Connect4Analysis
    )
}