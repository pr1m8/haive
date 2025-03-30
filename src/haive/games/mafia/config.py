"""Configuration for the Mafia game agent.

This module provides configuration classes and utilities for the Mafia game
agent, including:
    - Game settings (max days, discussion rounds)
    - LLM engine configurations
    - Role mappings and assignments
    - Debug settings

Example:
    >>> from mafia.config import MafiaAgentConfig
    >>> 
    >>> # Create a default configuration for 7 players
    >>> config = MafiaAgentConfig.default_config(
    ...     player_count=7,
    ...     max_days=3
    ... )
    >>> print(config.max_days)  # Shows 3
"""

from pydantic import Field, BaseModel
from typing import Dict, Any, Optional, List, Type
from src.haive.games.framework.multi_player.config import MultiPlayerGameConfig
from .state import MafiaGameState
from .models import PlayerRole
from src.haive.core.engine.aug_llm import AugLLMConfig
from .engines import aug_llm_configs

class MafiaAgentConfig(MultiPlayerGameConfig):
    """Configuration for the Mafia game agent.
    
    This class extends MultiPlayerGameConfig to provide Mafia-specific
    configuration options and defaults.

    Attributes:
        max_days (int): Maximum number of days before forcing game end
        day_discussion_rounds (int): Number of discussion rounds per day
        engines (Dict[str, Dict[str, AugLLMConfig]]): LLM configs by role
        state_schema (Type[MafiaGameState]): State schema for the game
        role_mapping (Dict[str, PlayerRole]): Engine key to role mapping
        debug (bool): Enable debug mode for detailed logging

    Example:
        >>> config = MafiaAgentConfig(
        ...     name="mafia_game",
        ...     max_days=3,
        ...     engines=aug_llm_configs,
        ...     initial_player_count=7
        ... )
        >>> print(config.max_days)  # Shows 3
    """

    max_days: int = Field(default=3, description="Maximum number of days before forcing game end")
    day_discussion_rounds: int = Field(default=1, description="Number of discussion rounds per day")
    engines: Dict[str, Dict[str, AugLLMConfig]] = Field(
        default_factory=dict, description="Configurations for game LLMs by role and function"
    )
    state_schema: Type[MafiaGameState] = Field(
        default=MafiaGameState, description="State schema for the game"
    )
    role_mapping: Dict[str, PlayerRole] = Field(
        default_factory=dict, description="Mapping from engine keys to player roles"
    )
    debug: bool = Field(default=False, description="Enable debug mode")
    
    @classmethod
    def default_config(cls, player_count: int = 7, max_days: int = 3) -> 'MafiaAgentConfig':
        """Create a default configuration for a Mafia game.
        
        This method creates a standard configuration with appropriate role
        mappings and engine configurations for the specified number of players.

        Args:
            player_count (int, optional): Number of players including narrator.
                Defaults to 7.
            max_days (int, optional): Maximum number of days before forcing
                game end. Defaults to 3.

        Returns:
            MafiaAgentConfig: Configured agent ready for game initialization

        Example:
            >>> config = MafiaAgentConfig.default_config(
            ...     player_count=9,
            ...     max_days=4
            ... )
            >>> print(len(config.role_mapping))  # Shows 5 (all roles)
        """
        # Create standard role mapping
        role_mapping = {
            "villager": PlayerRole.VILLAGER,
            "mafia": PlayerRole.MAFIA,
            "detective": PlayerRole.DETECTIVE,
            "doctor": PlayerRole.DOCTOR,
            "narrator": PlayerRole.NARRATOR
        }
        
        # Return config with engines and role mapping
        return cls(
            name="mafia_game",
            max_days=max_days,
            engines=aug_llm_configs,
            role_mapping=role_mapping,
            initial_player_count=player_count,
            state_schema=MafiaGameState,
            debug=False
        )