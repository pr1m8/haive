"""Connect4 agent configuration module.

This module provides configuration classes for the Connect4 game agent, including:
    - Base configuration for Connect4 agents
    - LLM configuration for players and analyzers
    - Game settings and visualization options

Example:
    >>> from src.haive.games.connect4 import Connect4AgentConfig
    >>> 
    >>> # Create a config with analysis enabled
    >>> config = Connect4AgentConfig(
    ...     enable_analysis=True,
    ...     should_visualize_graph=True,
    ...     max_moves=42  # Maximum possible moves in Connect4
    ... )
"""

from typing import Dict, Optional
from pydantic import BaseModel, Field
from src.haive.core.engine.aug_llm import AugLLMConfig
from src.haive.core.engine.agent.agent import AgentConfig
from src.haive.games.connect4.state import Connect4State
from src.haive.games.connect4.engines import aug_llm_configs
class Connect4AgentConfig(AgentConfig):
    """Configuration class for Connect4 game agents.
    
    This class defines the configuration parameters for Connect4 agents, including:
        - Game settings (max moves, analysis options)
        - LLM configurations for players and analyzers
        - Visualization settings
    
    Attributes:
        enable_analysis (bool): Whether to enable position analysis.
        should_visualize_graph (bool): Whether to visualize the game workflow graph.
        max_moves (int): Maximum number of moves before forcing a draw.
        aug_llm_configs (Dict[str, AugLLMConfig]): LLM configurations for players and analyzers.
    
    Example:
        >>> config = Connect4AgentConfig(
        ...     enable_analysis=True,
        ...     should_visualize_graph=True,
        ...     max_moves=42,
        ...     aug_llm_configs={
        ...         "red_player": red_player_config,
        ...         "yellow_player": yellow_player_config,
        ...         "red_analyzer": red_analyzer_config,
        ...         "yellow_analyzer": yellow_analyzer_config,
        ...     }
        ... )
    """
    state_schema: type[BaseModel] = Field(default=Connect4State)
    enable_analysis: bool = Field(
        default=False,
        description="Whether to enable position analysis during gameplay."
    )
    
    should_visualize_graph: bool = Field(
        default=False,
        description="Whether to visualize the game workflow graph."
    )
    
    max_moves: int = Field(
        default=42,  # 7 columns * 6 rows
        description="Maximum number of moves before forcing a draw."
    )
    
    engines: Dict[str, AugLLMConfig] = Field(
        default=aug_llm_configs,
        description="LLM configurations for players and analyzers."
    )
    
    class Config:
        """Pydantic configuration class.
        
        This inner class configures Pydantic behavior for the Connect4AgentConfig.
        """
        arbitrary_types_allowed = True