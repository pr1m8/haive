# among_us_config.py

from typing import Dict, List, Optional, Union, Literal, Any
from pydantic import BaseModel, Field, root_validator

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage
from langchain_core.output_parsers import PydanticOutputParser

from src.haive.core.engine.aug_llm import AugLLMConfig
from src.haive.core.models.llm.base import AzureLLMConfig
from src.haive.games.framework.base.config import GameConfig
from src.haive.games.among_us.state import AmongUsState
from src.haive.games.among_us.prompts import (
    CREWMATE_PROMPT, IMPOSTOR_PROMPT, MEETING_PROMPT, VOTING_PROMPT
)

class AmongUsAgentConfig(GameConfig):
    """
    Configuration for Among Us game agent.
    """
    # Base game agent fields inherited from GameAgentConfig
    name: str = Field(default="among_us_agent")
    state_schema: type = Field(default=AmongUsState)
    visualize: bool = Field(default=True)
    
    # Among Us specific configuration
    player_names: List[str] = Field(...)
    engines: Optional[Dict[str, Dict[str, AugLLMConfig]]] = Field(default=None)
    llm_config: Optional[Dict[str, Any]] = Field(default=None)
    
    # Game settings
    map_name: str = Field(default="skeld")
    map_locations: Optional[List[str]] = Field(default=None)
    num_impostors: int = Field(default=None)
    emergency_meetings_per_player: int = Field(default=1)
    discussion_time: int = Field(default=45)  # seconds
    voting_time: int = Field(default=30)  # seconds
    player_movement_speed: float = Field(default=1.0)
    kill_cooldown: int = Field(default=45)  # seconds
    task_bar_updates: Literal["always", "meetings", "never"] = Field(default="always")
    
    @root_validator(pre=True)
    def set_defaults(cls, values):
        """Set default values based on provided values."""
        # Set default number of impostors based on player count
        if values.get('num_impostors') is None and 'player_names' in values:
            values['num_impostors'] = max(1, len(values['player_names']) // 5)
        
        # Set default map locations based on map name
        if values.get('map_locations') is None:
            map_name = values.get('map_name', 'skeld')
            if map_name.lower() == 'skeld':
                values['map_locations'] = [
                    "cafeteria", "admin", "electrical", "storage", "medbay", 
                    "navigation", "shields", "weapons", "o2", "security"
                ]
            elif map_name.lower() == 'polus':
                values['map_locations'] = [
                    "dropship", "office", "laboratory", "storage", "communications", 
                    "weapons", "o2", "electrical", "security", "specimen"
                ]
            elif map_name.lower() == 'mira':
                values['map_locations'] = [
                    "launchpad", "medbay", "communications", "locker", "laboratory", 
                    "office", "admin", "cafeteria", "storage", "reactor"
                ]
        
        # Set default engines if not provided
        if values.get('engines') is None:
            values['engines'] = cls._create_default_engines(values)
        
        return values
    
    @classmethod
    def _create_default_engines(cls, values):
        """Create default engines configuration."""
        # Default LLM config
        default_llm_config = {
            "model": "gpt-4o",
            "parameters": {
                "temperature": 0.8,
                "top_p": 0.9
            }
        }
        
        # Merge with provided LLM config if any
        llm_config = {**default_llm_config, **(values.get('llm_config') or {})}
        
        # Create Azure LLM config
        azure_llm_config = AzureLLMConfig(**llm_config)
        
        # Create prompt templates
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
        
        # Create AugLLM configs
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
        
        # Return engines configuration
        return {
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
    
    class Config:
        """Pydantic model config."""
        arbitrary_types_allowed = True