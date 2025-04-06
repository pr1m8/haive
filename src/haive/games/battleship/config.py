"""
Battleship agent configuration module.

This module provides configuration classes for the Battleship game agent, including:
    - Base configuration
    - Game settings
    - Visualization options
"""

from typing import Dict
from pydantic import BaseModel, Field

from src.haive.core.engine.agent.agent import AgentConfig
from src.haive.core.aug_llm.base import AugLLMConfig

from .state import BattleshipState
from .engines import build_battleship_engines

class BattleshipAgentConfig(AgentConfig):
    """
    Configuration class for Battleship game agents.
    
    This class defines the configuration parameters for Battleship agents, including:
        - Game settings
        - Analysis options
        - Visualization settings
        - Engine configurations
    
    Attributes:
        state_schema (type): The state schema for the game
        player1_name (str): Name of player 1
        player2_name (str): Name of player 2
        enable_analysis (bool): Whether to enable strategic analysis
        visualize_board (bool): Whether to visualize the game boards
        engines (Dict[str, AugLLMConfig]): Engine configurations
    """
    
    name: str = Field(
        default="battleship_agent",
        description="Name of the agent"
    )
    
    state_schema: type = Field(
        default=BattleshipState,
        description="State schema for the game"
    )
    
    player1_name: str = Field(
        default="Player 1",
        description="Name of player 1"
    )
    
    player2_name: str = Field(
        default="Player 2",
        description="Name of player 2"
    )
    
    enable_analysis: bool = Field(
        default=True,
        description="Whether to enable strategic analysis"
    )
    
    visualize_board: bool = Field(
        default=True,
        description="Whether to visualize the game boards"
    )
    
    engines: Dict[str, AugLLMConfig] = Field(
        default_factory=build_battleship_engines,
        description="Engine configurations for players and analyzers"
    )
    
    class Config:
        """Pydantic configuration."""
        arbitrary_types_allowed = True