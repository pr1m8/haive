"""
Chess agent configuration module.

This module provides configuration classes for the chess game agent, including:
    - Base configuration
    - LLM configuration for players and analyzers
    - Game settings and visualization options
"""

from typing import Dict, Optional
from pydantic import BaseModel, Field

from src.haive.core.engine.agent.agent import AgentConfig
from src.haive.core.aug_llm.base import AugLLMConfig

from .state import ChessState
from .engines import build_chess_aug_llms

class ChessAgentConfig(AgentConfig):
    """
    Configuration class for chess game agents.
    
    This class defines the configuration parameters for chess agents, including:
        - Game settings (max moves, analysis options)
        - LLM configurations for players and analyzers
        - Visualization settings
    
    Attributes:
        state_schema (BaseModel): The state schema for the game
        enable_analysis (bool): Whether to enable position analysis
        should_visualize_graph (bool): Whether to visualize the workflow graph
        max_moves (int): Maximum number of moves before forcing a draw
        engines (Dict[str, AugLLMConfig]): LLM configurations for players and analyzers
    """
    
    # State schema
    state_schema: type = Field(
        default=ChessState,
        description="The state schema for the game"
    )
    
    # Analysis settings
    enable_analysis: bool = Field(
        default=True,
        description="Whether to enable position analysis during gameplay"
    )
    
    # Visualization settings
    should_visualize_graph: bool = Field(
        default=True,
        description="Whether to visualize the game workflow graph"
    )
    
    # Game settings
    max_moves: int = Field(
        default=200,
        description="Maximum number of moves before forcing a draw"
    )
    
    # LLM engines
    engines: Dict[str, AugLLMConfig] = Field(
        default_factory=build_chess_aug_llms,
        description="LLM configurations for players and analyzers"
    )
    #runnable_config: Dict['configurable]
    class Config:
        """Pydantic configuration class."""
        arbitrary_types_allowed = True