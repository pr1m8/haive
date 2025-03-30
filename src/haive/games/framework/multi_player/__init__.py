"""Multi-player game framework for building complex game agents.

This package provides a framework for creating multi-player game agents with support for:
    - Variable number of players
    - Role-based player configurations
    - Phase-based game flow
    - Information hiding between players
    - Concurrent or sequential player actions

Core Components:
    - MultiPlayerGameAgent: Base agent for multi-player games
    - MultiPlayerGameConfig: Configuration for multi-player agents
    - MultiPlayerGameState: Base state for multi-player games
    - MultiPlayerGameStateManager: State management for multi-player games
    - MultiPlayerGameFactory: Factory for creating multi-player agents
    - GamePhase: Common game phase enumerations

Example:
    >>> from haive.agents.agent_games.framework.multi_player import MultiPlayerGameAgent
    >>> from haive.agents.agent_games.framework.multi_player import MultiPlayerGameConfig
    >>> 
    >>> # Create a custom multi-player game agent
    >>> class MyGameAgent(MultiPlayerGameAgent):
    ...     def __init__(self, config: MultiPlayerGameConfig):
    ...         super().__init__(config)
    ...         self.state_manager = MyGameStateManager

Typical usage:
    - Import base classes to create game-specific implementations
    - Use the factory to create standard game agents
    - Customize game flow with phase-based logic
    - Implement role-specific behaviors
"""

from .agent import MultiPlayerGameAgent
from .config import MultiPlayerGameConfig
from .state import MultiPlayerGameState
from .state_manager import MultiPlayerGameStateManager
from .factory import MultiPlayerGameFactory
from .models import GamePhase

__all__ = [
    'MultiPlayerGameAgent',
    'MultiPlayerGameConfig',
    'MultiPlayerGameState',
    'MultiPlayerGameStateManager',
    'MultiPlayerGameFactory',
    'GamePhase',
]
