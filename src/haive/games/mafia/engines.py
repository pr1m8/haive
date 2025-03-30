"""LLM engine configurations for the Mafia game.

This module defines the LLM configurations and prompts for each role in the
Mafia game. It provides:
    - Role-specific prompt templates
    - LLM configurations for each role
    - Structured output schemas for decisions
    - Example prompts and responses

The module uses Azure OpenAI's GPT-4 model for all roles, with custom
prompts designed to elicit appropriate role-playing behavior.

Example:
    >>> from mafia.engines import aug_llm_configs
    >>> 
    >>> # Get the villager player engine config
    >>> villager_config = aug_llm_configs["villager"]["player"]
    >>> print(villager_config.name)  # Shows "villager_player"
"""

from src.haive.core.engine.aug_llm import AugLLMConfig
from src.haive.core.models.llm.base import AzureLLMConfig
from langchain_core.prompts import ChatPromptTemplate
from pydantic import Field
from .models import (
    PlayerRole, MafiaPlayerDecision, NarratorDecision, MafiaPlayerDecisionSchema, NarratorDecisionSchema
)

def generate_villager_prompt() -> ChatPromptTemplate:
    """Generate a prompt template for a villager in Mafia.
    
    This function creates a prompt that guides villager behavior, focusing on:
        - Analyzing other players' behavior
        - Making strategic decisions during discussions
        - Voting based on observed patterns
    
    Returns:
        ChatPromptTemplate: Configured prompt template for villager role

    Example:
        >>> prompt = generate_villager_prompt()
        >>> messages = prompt.format_messages(
        ...     player_id="Player_1",
        ...     phase="day_discussion",
        ...     day_number=1,
        ...     alive_players=["Player_1", "Player_2"],
        ...     public_info=["Night falls..."]
        ... )
    """
    return ChatPromptTemplate.from_messages([
        ('system', 
            "You are a villager in a game of Mafia. Your goal is to identify and eliminate the mafia members. "
            "Act realistically given your knowledge and analyze the behavior of other players. "
            "Be strategic in your discussions and voting."
        ),
        ('human', 
            "Game State:\n"
            "- You are: {player_id} (Villager)\n"
            "- Current Phase: {phase}\n"
            "- Day Number: {day_number}\n"
            "- Round Number: {round_number}\n\n"
            "Players:\n"
            "- Alive: {alive_players}\n"
            "- Dead: {dead_players}\n\n"
            "Recent Public Information:\n{public_info}\n\n"
            "Information Only You Know:\n{private_info}\n\n"
            "Recent Actions:\n{recent_actions}\n\n"
            "Current Task: {phase_context_task}\n\n"
            "Legal Actions Available:\n{legal_moves}\n\n"
            "Choose your action wisely. Provide your reasoning."
        )
    ])


def generate_mafia_prompt() -> ChatPromptTemplate:
    """Generate a prompt template for a mafia member in Mafia.
    
    This function creates a prompt that guides mafia behavior, focusing on:
        - Coordinating with other mafia members
        - Maintaining cover during discussions
        - Strategic target selection at night
    
    Returns:
        ChatPromptTemplate: Configured prompt template for mafia role

    Example:
        >>> prompt = generate_mafia_prompt()
        >>> messages = prompt.format_messages(
        ...     player_id="Player_1",
        ...     phase="night",
        ...     day_number=1,
        ...     alive_players=["Player_1", "Player_2"],
        ...     private_info=["Other mafia: Player_3"]
        ... )
    """
    return ChatPromptTemplate.from_messages([
        ('system', 
            "You are a mafia member in a game of Mafia. Your goal is to eliminate the villagers while "
            "avoiding detection. Work with other mafia members (if any) and maintain your cover. "
            "Act like an innocent villager during the day, but strategically eliminate villagers at night."
        ),
        ('human', 
            "Game State:\n"
            "- You are: {player_id} (Mafia)\n"
            "- Current Phase: {phase}\n"
            "- Day Number: {day_number}\n"
            "- Round Number: {round_number}\n\n"
            "Players:\n"
            "- Alive: {alive_players}\n"
            "- Dead: {dead_players}\n\n"
            "Recent Public Information:\n{public_info}\n\n"
            "Information Only You Know:\n{private_info}\n\n"
            "Recent Actions:\n{recent_actions}\n\n"
            "Current Task: {phase_context_task}\n\n"
            "Legal Actions Available:\n{legal_moves}\n\n"
            "Choose your action wisely. Provide your reasoning."
        )
    ])

def generate_detective_prompt() -> ChatPromptTemplate:
    """Generate a prompt template for a detective in Mafia.
    
    This function creates a prompt that guides detective behavior, focusing on:
        - Strategic investigation target selection
        - Using investigation results effectively
        - Contributing to discussions without revealing role
    
    Returns:
        ChatPromptTemplate: Configured prompt template for detective role

    Example:
        >>> prompt = generate_detective_prompt()
        >>> messages = prompt.format_messages(
        ...     player_id="Player_1",
        ...     phase="night",
        ...     day_number=1,
        ...     alive_players=["Player_1", "Player_2"],
        ...     private_info=["Player_2 is not mafia"]
        ... )
    """
    return ChatPromptTemplate.from_messages([
        ('system', 
            "You are a detective in a game of Mafia. Your goal is to identify the mafia members. "
            "You can investigate one player each night to determine if they are mafia or not. "
            "Use your investigation results wisely without revealing your role."
        ),
        ('human', 
            "Game State:\n"
            "- You are: {player_id} (Detective)\n"
            "- Current Phase: {phase}\n"
            "- Day Number: {day_number}\n"
            "- Round Number: {round_number}\n\n"
            "Players:\n"
            "- Alive: {alive_players}\n"
            "- Dead: {dead_players}\n\n"
            "Recent Public Information:\n{public_info}\n\n"
            "Information Only You Know:\n{private_info}\n\n"
            "Recent Actions:\n{recent_actions}\n\n"
            "Current Task: {phase_context_task}\n\n"
            "Legal Actions Available:\n{legal_moves}\n\n"
            "Choose your action wisely. Provide your reasoning."
        )
    ])

def generate_doctor_prompt() -> ChatPromptTemplate:
    """Generate a prompt template for a doctor in Mafia.
    
    This function creates a prompt that guides doctor behavior, focusing on:
        - Strategic protection target selection
        - Pattern recognition for mafia targets
        - Contributing to discussions without revealing role
    
    Returns:
        ChatPromptTemplate: Configured prompt template for doctor role

    Example:
        >>> prompt = generate_doctor_prompt()
        >>> messages = prompt.format_messages(
        ...     player_id="Player_1",
        ...     phase="night",
        ...     day_number=1,
        ...     alive_players=["Player_1", "Player_2"],
        ...     private_info=["You saved Player_2 last night"]
        ... )
    """
    return ChatPromptTemplate.from_messages([
        ('system', 
            "You are a doctor in a game of Mafia. Your goal is to protect the villagers. "
            "You can save one player each night from being killed by the mafia. "
            "Use your healing ability wisely without revealing your role."
        ),
        ('human', 
            "Game State:\n"
            "- You are: {player_id} (Doctor)\n"
            "- Current Phase: {phase}\n"
            "- Day Number: {day_number}\n"
            "- Round Number: {round_number}\n\n"
            "Players:\n"
            "- Alive: {alive_players}\n"
            "- Dead: {dead_players}\n\n"
            "Recent Public Information:\n{public_info}\n\n"
            "Information Only You Know:\n{private_info}\n\n"
            "Recent Actions:\n{recent_actions}\n\n"
            "Current Task: {phase_context_task}\n\n"
            "Legal Actions Available:\n{legal_moves}\n\n"
            "Choose your action wisely. Provide your reasoning."
        )
    ])

def generate_narrator_prompt() -> ChatPromptTemplate:
    """Generate a prompt template for the narrator in Mafia.
    
    This function creates a prompt that guides narrator behavior, focusing on:
        - Creating engaging narrative descriptions
        - Managing game flow and phase transitions
        - Providing appropriate information to players
    
    Returns:
        ChatPromptTemplate: Configured prompt template for narrator role

    Example:
        >>> prompt = generate_narrator_prompt()
        >>> messages = prompt.format_messages(
        ...     phase="night",
        ...     day_number=1,
        ...     player_summary="5 alive, 2 dead",
        ...     alive_mafia_count=2,
        ...     alive_village_count=3
        ... )
    """
    return ChatPromptTemplate.from_messages([
        ('system', 
            "You are the narrator in a game of Mafia. Your role is to guide the game, "
            "announce events, and manage phase transitions. You know all player roles "
            "and see all actions. Maintain suspense and create an engaging narrative."
        ),
        ('human', 
            "Game State:\n"
            "- Current Phase: {phase}\n"
            "- Day Number: {day_number}\n"
            "- Round Number: {round_number}\n\n"
            "Player Summary:\n{player_summary}\n\n"
            "Game Statistics:\n"
            "- Alive Mafia: {alive_mafia_count}\n"
            "- Alive Villagers: {alive_village_count}\n\n"
            "Phase-Specific Information:\n{phase_info}\n\n"
            "Recent Announcements:\n{public_announcements}\n\n"
            "Recent Actions:\n{action_history}\n\n"
            "Current Task: {phase_context_task}\n\n"
            "Your task is to manage the game flow and create engaging narration.\n"
            "You can make announcements and transition to the next phase when appropriate.\n\n"
            "Consider the following options:\n"
            "1. Make an announcement about the current situation\n"
            "2. Transition to the next phase if all required actions are complete\n"
            "3. Provide information about player deaths or other key events\n\n"
            "Decide on your next action as narrator."
        )
    ])

# Define the AugLLM configurations for each role
aug_llm_configs = {
    "villager": {
        "player": AugLLMConfig(
            name="villager_player",
            llm_config=AzureLLMConfig(model="gpt-4o"),
            prompt_template=generate_villager_prompt(),
            structured_output_model=MafiaPlayerDecisionSchema
        )
    },
    "mafia": {
        "player": AugLLMConfig(
            name="mafia_player",
            llm_config=AzureLLMConfig(model="gpt-4o"),
            prompt_template=generate_mafia_prompt(),
            structured_output_model=MafiaPlayerDecisionSchema
        )
    },
    "detective": {
        "player": AugLLMConfig(
            name="detective_player",
            llm_config=AzureLLMConfig(model="gpt-4o"),
            prompt_template=generate_detective_prompt(),
            structured_output_model=MafiaPlayerDecisionSchema
        )
    },
    "doctor": {
        "player": AugLLMConfig(
            name="doctor_player",
            llm_config=AzureLLMConfig(model="gpt-4o"),
            prompt_template=generate_doctor_prompt(),
            structured_output_model=MafiaPlayerDecisionSchema
        )
    },
    "narrator": {
        "player": AugLLMConfig(
            name="narrator_player",
            llm_config=AzureLLMConfig(model="gpt-4o"),
            prompt_template=generate_narrator_prompt(),
            structured_output_model=NarratorDecisionSchema
        )
    }
}