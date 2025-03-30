"""Chess game implementation module.

This package provides a complete implementation of the Chess game, including:
    - Game agent with LLM-powered players
    - State management with FEN support
    - Position analysis and evaluation
    - Move validation and piece movement
    - Game visualization

Example:
    >>> from src.haive.games.chess import ChessAgent, ChessAgentConfig
    >>> 
    >>> # Create and configure a Chess agent
    >>> config = ChessAgentConfig(enable_analysis=True)
    >>> agent = ChessAgent(config)
"""

from .agent import ChessAgent
from .config import ChessAgentConfig
from .models import (
    ChessMoveModel,
    ChessPlayerDecision,        
    ChessAnalysis,
)
from .state import ChessGameState
from .state_manager import ChessGameStateManager

__all__ = [
    "ChessAgent",
    "ChessAgentConfig",
    "ChessMoveModel",
    "ChessPlayerDecision",
    "ChessAnalysis",
    "ChessGameState",
    "ChessGameStateManager",
]

