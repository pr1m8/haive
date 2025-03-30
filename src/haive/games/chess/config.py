"""Chess agent configuration module.

This module provides configuration classes for the chess game agent, including:
    - Base configuration for chess agents
    - LLM configuration for players and analyzers
    - Game settings and visualization options

Example:
    >>> from src.haive.games.chess import ChessAgentConfig
    >>> 
    >>> # Create a config with analysis enabled
    >>> config = ChessAgentConfig(
    ...     enable_analysis=True,
    ...     should_visualize_graph=True,
    ...     max_moves=100
    ... )
"""

from typing import Dict, Optional, List
from pydantic import BaseModel, Field

from src.haive.core.engine.agent.agent import AgentConfig
from src.haive.core.engine.aug_llm import AugLLMConfig
from src.haive.core.models.llm.base import AzureLLMConfig

from .aug_llms import build_chess_aug_llms_per_color
from .state import ChessState

class ChessAgentConfig(AgentConfig):
    """Configuration class for chess game agents.
    
    This class defines the configuration parameters for chess agents, including:
        - Game settings (max moves, analysis options)
        - LLM configurations for players and analyzers
        - Visualization settings
    
    Attributes:
        enable_analysis (bool): Whether to enable position analysis.
        should_visualize_graph (bool): Whether to visualize the game workflow graph.
        max_moves (int): Maximum number of moves before forcing a draw.
        aug_llm_configs (Dict[str, AugLLMConfig]): LLM configurations for players and analyzers.
    
    Example:
        >>> config = ChessAgentConfig(
        ...     enable_analysis=True,
        ...     should_visualize_graph=True,
        ...     max_moves=100,
        ...     aug_llm_configs={
        ...         "white_player": white_player_config,
        ...         "black_player": black_player_config,
        ...         "white_analyzer": white_analyzer_config,
        ...         "black_analyzer": black_analyzer_config,
        ...     }
        ... )
    """
    state_schema: BaseModel = Field(
        default=ChessState,
        description="The state schema for the game."
    )
    enable_analysis: bool = Field(
        default=False,
        description="Whether to enable position analysis during gameplay."
    )
    
    should_visualize_graph: bool = Field(
        default=False,
        description="Whether to visualize the game workflow graph."
    )
    
    max_moves: int = Field(
        default=200,
        description="Maximum number of moves before forcing a draw."
    )
    
    engines: Dict[str, AugLLMConfig] = Field(
        default_factory=build_chess_aug_llms_per_color,
        description="LLM configurations for players and analyzers."
    )
    
    class Config:
        """Pydantic configuration class.
        
        This inner class configures Pydantic behavior for the ChessAgentConfig.
        """
        arbitrary_types_allowed = True