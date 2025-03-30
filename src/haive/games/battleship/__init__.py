"""Battleship game implementation for AI agents.

This package provides a complete implementation of a two-player Battleship
game with LLM-powered agents, including:
    - Game state management and ship placement
    - LLM-based targeting strategies
    - Turn-based gameplay mechanics
    - Configurable board sizes and ship layouts
    - Detailed game history and move tracking

The implementation uses LangGraph for workflow management and supports
multiple LLM providers (Azure, OpenAI, Anthropic) for agent decisions.

Components:
    BattleshipAgent:
        Main agent class managing the game flow, player interactions,
        and game state transitions.

    BattleshipState:
        Tracks the current game state including board positions,
        ship placements, and game phase.

    BattleshipAgentConfig:
        Configuration class for customizing game parameters like
        board size, fleet composition, and player settings.

    Models:
        Ship: Represents a battleship with size, position, and health.
        Board: 2D grid tracking shots and ship positions.
        Coordinate: (x,y) position on the game board.
        Move: Player action including target coordinate and result.
        GamePhase: Enum for game stages (setup, playing, ended).
        PlayerState: Player's current game state and statistics.
        GameResult: Final game outcome and statistics.
        ShipPlacement: Ship position and orientation on board.

    Prompts:
        generate_ship_placement_prompt:
            Creates LLM prompt for strategic ship placement.
        generate_targeting_prompt:
            Creates LLM prompt for target selection.

    AugLLMs:
        battleship_agent_configs:
            LLM configurations for different player roles.

Example:
    >>> from haive.agents.agent_games.battleship import BattleshipAgent, BattleshipAgentConfig
    >>> 
    >>> # Create a standard 10x10 Battleship game
    >>> config = BattleshipAgentConfig(
    ...     player_names=["Player 1", "Player 2"],
    ...     board_size=10,
    ...     use_standard_fleet=True
    ... )
    >>> 
    >>> agent = BattleshipAgent(config)
    >>> result = agent.run()
"""

from .agent import BattleshipAgent
from .config import BattleshipAgentConfig
from .state import BattleshipGameState,PlayerPrivateState
from .state_manager import BattleshipGameStateManager
from .models import (
    BattleshipPlacement,
    BattleshipAnalysis,
    BattleshipBoardPlacement,
    BattleshipMoveModel,
    BattleshipMoveResult,
    Board,
    Coordinates,
    Ship,
    #ShipPlacement  # Ship position and orientation
)
from .prompts import (
    generate_ship_placement_prompt,  # Strategic ship placement prompt
    #generate_targeting_prompt,  # Target selection prompt
    generate_move_prompt,
    generate_analysis_prompt
)
from .aug_llms import aug_llm_configs  # LLM role configurations

__all__ = [
    # Core game components
    'BattleshipAgent',  # Main game orchestrator
    'BattleshipAgentConfig',  # Game configuration
    'BattleshipGameState',  # Game state tracker
    'BattleshipGameStateManager',  # State management utilities
    
    # Game models
    'Ship',  # Ship representation
    'Board',  # Game board
    'Coordinates',  # Board position
    'BattleshipMoveModel',  # Player action
    #'GamePhase',  # Game stages
    'PlayerState',  # Player state
    #'GameResult',  # Game outcome
    'BattleshipPlacement',  # Ship positioning
    'BattleshipAnalysis',  # Player analysis
    'BattleshipBoardPlacement',  # Board placement
    'BattleshipMoveResult',  # Move result
    'BattleshipMoveModel',  # Player action
    'BattleshipPlacement',  # Ship positioning
    'BattleshipAnalysis',  # Player analysis
    'BattleshipBoardPlacement',  # Board placement
    # LLM components
    'generate_ship_placement_prompt',  # Ship placement strategy
    #'generate_targeting_prompt',  # Targeting strategy
    'generate_move_prompt',
    'generate_analysis_prompt',
    'aug_llm_configs'  # LLM configurations
]

# Version of the battleship game implementation
__version__ = '1.0.0'
