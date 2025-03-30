"""Connect4 game implementation module.

This package provides a complete implementation of the Connect4 game, including:
    - Game agent with LLM-powered players
    - State management and move validation
    - Position analysis and evaluation
    - Game visualization
    - Configuration and model definitions

Example:
    >>> from src.haive.games.connect4 import Connect4Agent, Connect4AgentConfig
    >>> 
    >>> # Create and configure a Connect4 agent
    >>> config = Connect4AgentConfig(enable_analysis=True)
    >>> agent = Connect4Agent(config)
"""

from .agent import Connect4Agent
from .config import Connect4AgentConfig
from .models import (
    Connect4Move,
    Connect4PlayerDecision,
    Connect4Analysis,
)
from .state import Connect4State
from .state_manager import Connect4StateManager

__all__ = [
    "Connect4Agent",
    "Connect4AgentConfig",
    "Connect4Move",
    "Connect4PlayerDecision",
    "Connect4Analysis",
    "Connect4State",
    "Connect4StateManager",
]
