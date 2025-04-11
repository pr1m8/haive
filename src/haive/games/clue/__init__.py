"""
Clue game module.

This module provides a Clue (Cluedo) game implementation for the Haive platform.
Players must deduce who committed a murder, with what weapon, and in which room.
"""

from .state import ClueState
from .state_manager import ClueStateManager
from .models import ClueSolution, ClueGuess, ClueResponse
from .config import ClueConfig
from .agent import ClueAgent

__all__ = [
    "ClueState",
    "ClueStateManager",
    "ClueSolution",
    "ClueGuess",
    "ClueResponse",
    "ClueConfig",
    "ClueAgent"
]
