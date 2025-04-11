"""Base framework for game agents.

This package provides the foundational classes and utilities for building game agents,
including experimental features for game development.

Core Components:
    - GameAgent: Base class for implementing game-specific agents
    - GameConfig: Configuration class for game agents
    - GameState: Base state representation for games
    - GameStateManager: Interface for managing game state transitions
    - GameAgentFactory: Factory for creating game agents

Experimental Components:
    - GameTemplateGenerator: Template generator for creating new game implementations
      Warning: This component is experimental and its API may change.

Example:
    >>> from src.haive.agents.agent_games.framework.base import GameAgent, GameConfig
    >>> from src.haive.agents.agent_games.framework.base import GameTemplateGenerator  # Experimental
"""

from .agent import GameAgent,run_game           
from .config import GameConfig
from .state import GameState
from .state_manager import GameStateManager
from .factory import GameAgentFactory
from .template_generator import GameTemplateGenerator
#from .utils import run_game
__all__ = [
    'GameAgent',
    'GameConfig',
    'GameState',
    'GameStateManager',
    'GameAgentFactory',
    'GameTemplateGenerator',  # Experimental
    #'run_game',
    'run_game',
]
