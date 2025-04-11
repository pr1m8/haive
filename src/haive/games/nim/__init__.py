"""
Nim game module.

This package provides components for simulating and managing the Nim game,
including state management, LLM-based agents, configuration, and strategic analysis.
"""

from .config import NimConfig
from .state import NimState
from .models import NimMove, NimAnalysis
from .engines import nim_engines
from .state_manager import NimStateManager
from .agent import NimAgent

__all__ = [
    "NimConfig",
    "NimState",
    "NimMove",
    "NimAnalysis",
    "nim_engines",
    "NimStateManager",
    "NimAgent"
]
