"""
Configuration for the Mastermind game agent.

This module defines the configuration for the Mastermind game agent,
including game state schema, engines, analysis settings, visualization,
and game parameters.
"""
from src.haive.games.framework.base.config import GameConfig
from src.haive.games.mastermind.state import MastermindState
from src.haive.games.mastermind.engines import mastermind_engines
from typing import Dict, Type, List, Optional
from pydantic import Field
from src.haive.core.engine.aug_llm import AugLLMConfig

# Version information for tracking changes
VERSION = "1.1.0"

class MastermindConfig(GameConfig):
    """Configuration for the Mastermind game agent.

    This class defines the configuration for the Mastermind game agent,
    including game state schema, engines, analysis settings, visualization,
    and game parameters.
    """
    name: str = Field(default="mastermind", description="Name of the game")
    version: str = Field(default=VERSION, description="Version of the game implementation")
    state_schema: Type[MastermindState] = Field(default=MastermindState)
    engines: Dict[str, AugLLMConfig] = Field(
        default=mastermind_engines, 
        description="Configs for the Mastermind engines"
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
        default=10, 
        description="Maximum number of turns"
    )
    codemaker: str = Field(
        default="player1",
        description="Player who creates the code (player1 or player2)"
    )
    colors: List[str] = Field(
        default=["red", "blue", "green", "yellow", "purple", "orange"],
        description="List of available colors"
    )
    code_length: int = Field(
        default=4,
        description="Length of the secret code"
    )
    secret_code: Optional[List[str]] = Field(
        default=None,
        description="Predetermined secret code (if None, will be generated)"
    )
    
    @classmethod
    def default_config(cls):
        """Create a default configuration.

        Returns:
            MastermindConfig: Default configuration for Mastermind game.
        """
        return cls(
            name="mastermind",
            state_schema=MastermindState,
            aug_llm_configs=mastermind_engines,
            enable_analysis=True,
            visualize=True,
            max_turns=10,
            codemaker="player1",
            colors=["red", "blue", "green", "yellow", "purple", "orange"],
            code_length=4,
            secret_code=None
        )