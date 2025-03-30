"""Framework for building game agents.

This package provides a comprehensive framework for building game agents
that can play various types of games using LLMs. It includes base classes,
utilities, and patterns for implementing game-specific agents.

The framework is organized into:
- base: Core classes and interfaces for game agents
- multi_player: Extensions for multi-player games
- templates: Templates and generators for new games

Example:
    >>> from src.haive.games.framework import GameAgent, GameConfig
    >>> from src.haive.games.framework.base import GameState
    >>> 
    >>> # Create a game-specific agent
    >>> class MyGameAgent(GameAgent[MyGameConfig]):
    ...     def __init__(self, config: MyGameConfig):
    ...         super().__init__(config)

Typical usage:
    - Import base classes from framework.base
    - Use multi_player for games with more than two players
    - Use templates to generate new game implementations
"""

from src.haive.games.framework.base import (
    GameAgent,
    GameConfig,
    GameState,
    GameStateManager,
    GameAgentFactory,
    run_game,
)

__all__ = [
    'GameAgent',
    'GameConfig',
    'GameState',
    'GameStateManager',
    'GameAgentFactory',
    'run_game',
]
