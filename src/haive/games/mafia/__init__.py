"""Mafia game implementation module.

This package provides a complete implementation of the Mafia party game, including:
    - Multi-player game agent with role-based gameplay
    - Day/Night phase management
    - Role-specific actions and abilities
    - Hidden information and voting mechanics
    - Game state tracking and validation

Example:
    >>> from src.haive.games.mafia import MafiaAgent, MafiaAgentConfig
    >>> 
    >>> # Create and configure a Mafia game agent
    >>> config = MafiaAgentConfig(
    ...     num_players=6,
    ...     num_mafia=2
    ... )
    >>> agent = MafiaAgent(config)


from .agent import MafiaAgent
from .config import MafiaAgentConfig
from .models import (
    MafiaGameState,
    MafiaPlayerState,
    MafiaAction,
    MafiaVote,
    MafiaAnalysis,
)
from .state import MafiaState
from .state_manager import MafiaStateManager
from .engines import (
    generate_mafia_action_prompt,
    generate_mafia_vote_prompt,
    generate_mafia_analysis_prompt,
)

__all__ = [
    "MafiaAgent",
    "MafiaAgentConfig",
    "MafiaGameState",
    "MafiaPlayerState",
    "MafiaAction",
    "MafiaVote",
    "MafiaAnalysis",
    "MafiaState",
    "MafiaStateManager",
    "generate_mafia_action_prompt",
    "generate_mafia_vote_prompt",
    "generate_mafia_analysis_prompt",
]
"""