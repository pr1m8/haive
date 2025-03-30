"""Configuration for multi-player game agents.

This module provides the configuration class for multi-player game agents,
supporting features like:
    - Role-based player configurations
    - LLM engine configurations per role
    - Game state schema definitions
    - Visualization settings
    - Game flow control

Example:
    >>> from haive.agents.agent_games.framework.multi_player.config import MultiPlayerGameConfig
    >>> from haive.core.aug_llm.base import AugLLMConfig
    >>> 
    >>> # Create a game configuration
    >>> config = MultiPlayerGameConfig(
    ...     state_schema=MyGameState,
    ...     engines={
    ...         "player": {"move": player_llm_config},
    ...         "narrator": {"narrate": narrator_llm_config}
    ...     }
    ... )
"""

from typing import Type, Dict, Optional
from pydantic import BaseModel, Field
from src.haive.core.engine.agent.agent import AgentConfig
from src.haive.games.framework.multi_player.state import MultiPlayerGameState
from src.haive.core.engine.aug_llm import AugLLMConfig

class MultiPlayerGameConfig(AgentConfig):
    """Configuration for multi-player game agents.
    
    This class defines the configuration for multi-player game agents,
    including state management, player roles, and LLM configurations.
    
    Attributes:
        state_schema (Type[MultiPlayerGameState]): State schema for the game.
        player_schemas (Dict[str, Type[BaseModel]]): Role-specific schemas.
        engines (Dict[str, Dict[str, AugLLMConfig]]): LLM configs by role.
        initial_player_count (int): Default number of players.
        visualize (bool): Whether to visualize the game.
        max_rounds (Optional[int]): Maximum number of rounds.
        async_mode (bool): Whether to run players asynchronously.
    
    Example:
        >>> config = MultiPlayerGameConfig(
        ...     state_schema=MyGameState,
        ...     engines={
        ...         "player": {
        ...             "move": AugLLMConfig(
        ...                 name="player_move",
        ...                 llm_config=my_llm_config,
        ...                 prompt_template=move_prompt
        ...             )
        ...         }
        ...     },
        ...     initial_player_count=4
        ... )
    """
    
    state_schema: Type[MultiPlayerGameState] = Field(
        ..., description="State schema for the game"
    )
    player_schemas: Dict[str, Type[BaseModel]] = Field(
        default_factory=dict,
        description="Role-specific schemas for players"
    )
    engines: Dict[str, Dict[str, AugLLMConfig]] = Field(
        ...,
        description="Configurations for game LLMs by role and function"
    )
    initial_player_count: int = Field(
        default=2,
        description="Default number of players"
    )
    visualize: bool = Field(
        default=True,
        description="Whether to visualize the game"
    )
    max_rounds: Optional[int] = Field(
        default=None,
        description="Maximum number of rounds"
    )
    async_mode: bool = Field(
        default=False,
        description="Whether to run players asynchronously"
    )
    
    class Config:
        """Pydantic configuration."""
        arbitrary_types_allowed = True