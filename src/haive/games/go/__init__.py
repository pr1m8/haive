"""Go game implementation module.

This package provides a complete implementation of the Go game, including:
    - Game agent with LLM-powered players
    - State management with SGF support
    - Position analysis and territory evaluation
    - Move validation and scoring
    - Game visualization

Example:
    >>> from src.haive.games.go import GoAgent, GoAgentConfig
    >>> 
    >>> # Create and configure a Go agent
    >>> config = GoAgentConfig(board_size=19, enable_analysis=True)
    >>> agent = GoAgent(config)
"""

from .agent import GoAgent
from .config import GoAgentConfig
from .models import (
    GoMove,
    GoPlayerDecision,
    GoAnalysis,
)
from .state import GoGameState
from .state_manager import GoGameStateManager

__all__ = [
    "GoAgent",
    "GoAgentConfig",
    "GoMove",
    "GoPlayerDecision",
    "GoAnalysis",
    "GoGameState",
    "GoGameStateManager",
]
