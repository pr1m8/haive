"""
Configuration for the Fox and Geese game agent.

This module defines the configuration for the Fox and Geese game agent,
which includes the game name, state schema, AugLLM configurations,
enable_analysis, visualize, and max_turns.
"""
from src.haive.games.framework.base.config import GameConfig
from src.haive.games.fox_and_geese.state import FoxAndGeeseState
from src.haive.games.fox_and_geese.engines import fox_and_geese_engines
from typing import Dict, Type
from pydantic import Field
from src.haive.core.engine.agent.agent import AugLLMConfig

class FoxAndGeeseConfig(GameConfig):
    """Configuration for the Fox and Geese game agent.

    This class defines the configuration for the Fox and Geese game agent,
    which includes the game name, state schema, AugLLM configurations,
    enable_analysis, visualize, and max_turns.
    """
    name: str = Field(default="fox_and_geese", description="Name of the game")
    state_schema: Type[FoxAndGeeseState] = Field(default=FoxAndGeeseState)
    engines: Dict[str, AugLLMConfig] = Field(
        default=fox_and_geese_engines, 
        description="Configs for the Fox and Geese engines"
    )
    enable_analysis: bool = Field(
        default=True, 
        description="Whether to enable position analysis"
    )
    visualize: bool = Field(
        default=True, 
        description="Whether to visualize the game"
    )
    max_turns: int = Field(
        default=100, 
        description="Maximum number of turns before declaring a draw"
    )
    
    @classmethod
    def default_config(cls):
        """Create a default configuration."""
        return cls(
            name="fox_and_geese",
            state_schema=FoxAndGeeseState,
            engines=fox_and_geese_engines,
            enable_analysis=True,
            visualize=True,
            max_turns=100
        )