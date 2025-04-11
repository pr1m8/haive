"""
Battleship game engine configurations.

This module provides engine configurations for the Battleship game, including:
    - Player decision engines
    - Ship placement engines
    - Analysis engines
"""

from typing import Dict, List
from src.haive.core.aug_llm.base import AugLLMConfig
from src.haive.core.models.llm.base import AzureLLMConfig

from .models import (
    MoveCommand,
    Analysis,
    ShipPlacementWrapper
)
from .prompts import (
    generate_ship_placement_prompt,
    generate_move_prompt,
    generate_analysis_prompt
)

def build_battleship_engines() -> Dict[str, AugLLMConfig]:
    """
    Build engine configurations for the Battleship game.
    
    This function creates AugLLMConfig objects for:
        - Player 1 ship placement
        - Player 2 ship placement
        - Player 1 move selection
        - Player 2 move selection
        - Player 1 analysis
        - Player 2 analysis
    
    Returns:
        Dict[str, AugLLMConfig]: Dictionary of engine configurations
    """
    # Default LLM configuration
    default_llm_config = AzureLLMConfig(
        model="gpt-4o",
        parameters={"temperature": 0.7}
    )
    
    engines = {
        "player1_ship_placement": AugLLMConfig(
            name="player1_ship_placement",
            llm_config=default_llm_config,
            prompt_template=generate_ship_placement_prompt("Player 1"),
            structured_output_model=ShipPlacementWrapper,
            description="Player 1 ship placement"
        ),
        "player2_ship_placement": AugLLMConfig(
            name="player2_ship_placement",
            llm_config=default_llm_config,
            prompt_template=generate_ship_placement_prompt("Player 2"),
            structured_output_model=ShipPlacementWrapper,
            description="Player 2 ship placement"
        ),
        "player1_move": AugLLMConfig(
            name="player1_move",
            llm_config=default_llm_config,
            prompt_template=generate_move_prompt("Player 1"),
            structured_output_model=MoveCommand,
            description="Player 1 move selection"
        ),
        "player2_move": AugLLMConfig(
            name="player2_move",
            llm_config=default_llm_config,
            prompt_template=generate_move_prompt("Player 2"),
            structured_output_model=MoveCommand,
            description="Player 2 move selection"
        ),
        "player1_analyzer": AugLLMConfig(
            name="player1_analyzer",
            llm_config=default_llm_config,
            prompt_template=generate_analysis_prompt("Player 1"),
            structured_output_model=Analysis,
            description="Player 1 analysis"
        ),
        "player2_analyzer": AugLLMConfig(
            name="player2_analyzer",
            llm_config=default_llm_config,
            prompt_template=generate_analysis_prompt("Player 2"),
            structured_output_model=Analysis,
            description="Player 2 analysis"
        )
    }
    
    return engines