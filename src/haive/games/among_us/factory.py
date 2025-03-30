# among_us_factory.py

from typing import List, Dict, Any, Optional
#from src.haive.games.framework.multi_player.factory import MultiPlayerGameFactory
from src.haive.core.engine.aug_llm import AugLLMConfig
from src.haive.core.models.llm.base import AzureLLMConfig
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage

from src.haive.games.among_us.agent import AmongUsAgent
from src.haive.games.among_us.state import AmongUsState
from src.haive.games.among_us.models import PlayerRole, AmongUsGamePhase
from src.haive.games.among_us.prompts import CREWMATE_PROMPT, IMPOSTOR_PROMPT, MEETING_PROMPT, VOTING_PROMPT

def create_among_us_game(
    player_names: List[str],
    llm_config: Optional[Dict[str, Any]] = None,
    game_config: Optional[Dict[str, Any]] = None
) -> AmongUsAgent:
    """
    Create an Among Us game with customizable configuration.
    
    Args:
        player_names: List of player names/IDs
        llm_config: Configuration for the language model
        game_config: Game-specific configuration
        
    Returns:
        An initialized AmongUsAgent
    """
    # Default configurations
    default_llm_config = {
        "model": "gpt-4o",
        "parameters": {
            "temperature": 0.8,
            "top_p": 0.9
        }
    }
    
    default_game_config = {
        "map_name": "skeld",
        "num_impostors": max(1, len(player_names) // 5),
        "emergency_meetings_per_player": 1,
        "discussion_time": 45,  # seconds
        "voting_time": 30,  # seconds
        "kill_cooldown": 45,  # seconds
        "visual_tasks_enabled": True,
        "task_bar_updates": "always",  # "always", "meetings", "never"
        "map_locations": [
            "cafeteria", "admin", "electrical", "storage", "medbay", 
            "navigation", "shields", "weapons", "o2", "security"
        ]
    }
    
    # Merge with provided configs, prioritizing provided values
    final_llm_config = {**default_llm_config, **(llm_config or {})}
    final_game_config = {**default_game_config, **(game_config or {})}
    
    # Create LLM configuration
    azure_llm_config = AzureLLMConfig(**final_llm_config)
    
    # Create prompt templates with placeholders instead of formatting them now
    # This prevents the KeyError because we're not attempting to format the prompts yet
    crewmate_template = ChatPromptTemplate.from_messages([
        SystemMessage(content=CREWMATE_PROMPT),
        MessagesPlaceholder(variable_name="messages")
    ])
    
    impostor_template = ChatPromptTemplate.from_messages([
        SystemMessage(content=IMPOSTOR_PROMPT),
        MessagesPlaceholder(variable_name="messages")
    ])
    
    meeting_template = ChatPromptTemplate.from_messages([
        SystemMessage(content=MEETING_PROMPT),
        MessagesPlaceholder(variable_name="messages")
    ])
    
    voting_template = ChatPromptTemplate.from_messages([
        SystemMessage(content=VOTING_PROMPT),
        MessagesPlaceholder(variable_name="messages")
    ])
    
    # Create AugLLM configs for different roles and game phases
    crewmate_config = AugLLMConfig(
        name="crewmate_player",
        llm_config=azure_llm_config,
        prompt_template=crewmate_template
    )
    
    impostor_config = AugLLMConfig(
        name="impostor_player",
        llm_config=azure_llm_config,
        prompt_template=impostor_template
    )
    
    meeting_config = AugLLMConfig(
        name="meeting_discussion",
        llm_config=azure_llm_config,
        prompt_template=meeting_template
    )
    
    voting_config = AugLLMConfig(
        name="voting_decision",
        llm_config=azure_llm_config,
        prompt_template=voting_template
    )
    
    # Corrected factory.py engines setup

    # Set up engines dictionary for MultiPlayerGameConfig
    engines = {
        "CREWMATE": {
            "player": crewmate_config,
            "meeting": meeting_config,
            "voting": voting_config
        },
        "IMPOSTOR": {
            "player": impostor_config,
            "meeting": meeting_config,
            "voting": voting_config
        }
    }

    # Create config for the agent
    from src.haive.games.among_us.config import AmongUsAgentConfig

    agent_config = AmongUsAgentConfig(
    state_schema=AmongUsState,
    engines=engines,
    player_names=player_names,
    map_name=final_game_config["map_name"],
    num_impostors=final_game_config["num_impostors"],
    emergency_meetings_per_player=final_game_config["emergency_meetings_per_player"],
    discussion_time=final_game_config["discussion_time"],
    voting_time=final_game_config["voting_time"],
    kill_cooldown=final_game_config["kill_cooldown"]
    )
    
    
    # Create and return agent instance
    return AmongUsAgent(agent_config)