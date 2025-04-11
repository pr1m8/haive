"""
Configuration for the Mancala game agent.

This module defines the configuration for the Mancala game agent,
which includes the game name, state schema, AugLLM configurations,
enable_analysis, visualize, and stones_per_pit.
"""
from src.haive.games.framework.base.config import GameConfig
from src.haive.games.mancala.state import MancalaState
from src.haive.games.mancala.engines import mancala_engines
from typing import Dict, Type
from pydantic import Field
from src.haive.core.engine.aug_llm import AugLLMConfig

class MancalaConfig(GameConfig):
    """Configuration for the Mancala game agent.

    This class defines the configuration for the Mancala game agent,
    which includes the game name, state schema, AugLLM configurations,
    enable_analysis, visualize, and stones_per_pit.
    """
    name: str = Field(default="mancala", description="Name of the game")
    state_schema: Type[MancalaState] = Field(default=MancalaState)
    aug_llm_configs: Dict[str, AugLLMConfig] = Field(
        default=mancala_engines, 
        description="Configs for the Mancala engines"
    )
    enable_analysis: bool = Field(
        default=True, 
        description="Whether to enable position analysis"
    )
    visualize: bool = Field(
        default=True, 
        description="Whether to visualize the game"
    )
    stones_per_pit: int = Field(
        default=4, 
        description="Initial number of stones per pit"
    )
    
    @classmethod
    def default_config(cls):
        """Create a default configuration.

        Returns:
            MancalaConfig: Default configuration for the Mancala game.
        """
        return cls(
            name="mancala",
            state_schema=MancalaState,
            aug_llm_configs=mancala_engines,
            enable_analysis=True,
            visualize=True,
            stones_per_pit=4
        )