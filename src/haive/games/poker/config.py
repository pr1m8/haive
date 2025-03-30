"""Configuration module for the Poker agent.

This module provides configuration classes and utilities for setting up
poker game agents, including:
    - Game settings (blinds, starting chips, max hands)
    - Player configurations and names
    - LLM engine configurations
    - State management settings
    - Game history and analysis options

The module supports multiple LLM providers and allows customization of
game parameters through a Pydantic-based configuration system.

Example:
    >>> from poker.config import PokerAgentConfig
    >>> 
    >>> # Create default config for 6 players
    >>> config = PokerAgentConfig.default_config(
    ...     player_names=["P1", "P2", "P3", "P4", "P5", "P6"],
    ...     starting_chips=2000,
    ...     small_blind=10,
    ...     big_blind=20
    ... )
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Type, Any
from src.haive.core.engine.agent.agent import AgentConfig
from src.haive.core.engine.aug_llm import AugLLMConfig
from src.haive.core.models.llm.base import (
    AzureLLMConfig, LLMProvider, DeepSeekLLMConfig, 
    GeminiLLMConfig, AnthropicLLMConfig, MistralLLMConfig
)
import os
from src.haive.games.poker.state import PokerState
from src.haive.games.poker.state_manager import PokerStateManager
from src.haive.games.poker.engines import (
    create_poker_agent_configs, 
    create_default_agent_configs, 
    get_available_providers
)

class PokerAgentConfig(AgentConfig):
    """Configuration class for the poker agent.

    This class defines all necessary parameters and settings for running
    a poker game, including player setup, game rules, and LLM configurations.
    It inherits from the base AgentConfig class and adds poker-specific
    parameters.

    Attributes:
        engines (Dict[str, AugLLMConfig]): Mapping of agent names to their
            LLM configurations. Default is an empty dict.
        player_names (List[str]): List of player names in the game.
            Default is ["Alice", "Bob", "Charlie", "Dave"].
        state_schema (Type[BaseModel]): Schema class for game state.
            Default is PokerState.
        state_schema_manager (Any): Manager for handling state transitions.
            Default is PokerStateManager().
        starting_chips (int): Initial chip count for each player.
            Default is 1000.
        small_blind (int): Small blind amount. Default is 5.
        big_blind (int): Big blind amount. Default is 10.
        max_hands (int): Maximum number of hands to play.
            Default is 10.
        enable_detailed_analysis (bool): Whether to log detailed hand
            analysis. Default is True.
        save_game_history (bool): Whether to save game history to disk.
            Default is True.

    Example:
        >>> config = PokerAgentConfig(
        ...     name="high_stakes_game",
        ...     starting_chips=5000,
        ...     small_blind=25,
        ...     big_blind=50,
        ...     max_hands=20
        ... )
    """

    engines: Dict[str, AugLLMConfig] = Field(
        default_factory=dict,
        description="Configuration for different poker agents"
    )
    
    player_names: List[str] = Field(
        default=["Alice", "Bob", "Charlie", "Dave"],
        description="List of player names"
    )

    state_schema: Type[BaseModel] = Field(
        default=PokerState,
        description="State schema for the poker game"
    )

    state_schema_manager: Any = Field(
        default=PokerStateManager(),
        description="State schema manager for the poker game"
    )

    starting_chips: int = Field(
        default=1000,
        description="Starting chips for each player"
    )
    
    small_blind: int = Field(
        default=50,
        description="Small blind amount"
    )
    
    big_blind: int = Field(
        default=100,
        description="Big blind amount"
    )
    
    max_hands: int = Field(
        default=10,
        description="Maximum number of hands to play"
    )
    
    enable_detailed_analysis: bool = Field(
        default=True,
        description="Whether to include detailed hand analysis in the log"
    )
    
    save_game_history: bool = Field(
        default=True,
        description="Whether to save game history"
    )

    @classmethod
    def default_config(cls, **kwargs) -> 'PokerAgentConfig':
        """Create a default configuration for poker agents.
        
        This class method generates a default configuration with reasonable
        starting values for all parameters. Any parameter can be overridden
        by passing it as a keyword argument.

        Args:
            **kwargs: Override default configuration parameters. Valid keys
                include all attributes of PokerAgentConfig.

        Returns:
            PokerAgentConfig: A new configuration instance with default
                values and any specified overrides.

        Example:
            >>> config = PokerAgentConfig.default_config(
            ...     player_names=["Player1", "Player2", "Player3"],
            ...     starting_chips=2000,
            ...     max_hands=15
            ... )
        """
        # Get available providers and create engine configurations
        providers = get_available_providers()
        engines = create_default_agent_configs(providers)
        
        # If engines are provided in kwargs, use those instead
        if 'engines' not in kwargs:
            kwargs['engines'] = engines
        
        # Create default poker agent config
        config = cls(
            name="poker_game",
            **kwargs
        )
        
        return config