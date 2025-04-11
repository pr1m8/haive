"""
Mancala game module.

This package provides logic, configuration, state management, engine interfaces,
and an LLM-based agent for playing and analyzing Mancala games.
"""

from .config import MancalaConfig
from .state import MancalaState
from .models import MancalaMove, MancalaAnalysis
from .engines import mancala_engines
from .state_manager import MancalaStateManager
from .agent import MancalaAgent 

__all__ = [
    "MancalaConfig",
    "MancalaState",
    "MancalaMove",
    "MancalaAnalysis",
    "mancala_engines",
    "MancalaStateManager",
    "MancalaAgent"
]
