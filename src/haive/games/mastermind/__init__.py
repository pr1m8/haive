"""
Mastermind game module.

This package provides logic, configuration, state management, engine interfaces,
and an LLM-based agent for playing and analyzing Mastermind (codebreaking) games.
"""

from .config import MastermindConfig
from .state import MastermindState
from .models import ColorCode, MastermindGuess, MastermindAnalysis
from .engines import mastermind_engines
from .state_manager import MastermindStateManager
from .agent import MastermindAgent

__all__ = [
    "MastermindConfig",
    "MastermindState",
    "ColorCode",
    "MastermindGuess",
    "MastermindAnalysis",
    "mastermind_engines",
    "MastermindStateManager",
    "MastermindAgent"
]
