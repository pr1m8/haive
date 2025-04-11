"""
Fox and Geese game module.

This module provides logic, configuration, state management, engine interfaces,
and an LLM-based agent for playing and analyzing Fox and Geese games.
"""

from .config import FoxAndGeeseConfig
from .models import FoxAndGeeseMove, FoxAndGeesePosition, FoxAndGeeseAnalysis
from .state import FoxAndGeeseState
from .state_manager import FoxAndGeeseStateManager
from .agent import FoxAndGeeseAgent 

__all__ = [
    "FoxAndGeeseConfig",
    "FoxAndGeeseMove",
    "FoxAndGeesePosition",
    "FoxAndGeeseAnalysis",  
    "FoxAndGeeseState",
    "FoxAndGeeseStateManager",
    "FoxAndGeeseAgent"
]