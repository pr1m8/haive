"""Models for multi-player game framework.

This module provides common enumerations and base models used across
multi-player games. These models serve as building blocks for creating
game-specific implementations.

Example:
    >>> from haive.agents.agent_games.framework.multi_player.models import GamePhase
    >>> 
    >>> # Use game phases in your game state
    >>> current_phase = GamePhase.SETUP
    >>> if current_phase == GamePhase.MAIN:
    ...     # Handle main game phase
    ...     pass
"""

from enum import Enum

class GamePhase(str, Enum):
    """Common game phases that many games share.
    
    This enumeration defines standard game phases that are common across
    different types of games. Games can extend or modify these phases
    based on their specific needs.
    
    Attributes:
        SETUP (str): Initial game setup phase for player assignments, etc.
        MAIN (str): Main gameplay phase where core game actions occur.
        SCORING (str): Phase for calculating and updating scores.
        END (str): Game conclusion phase for final state updates.
    
    Example:
        >>> phase = GamePhase.SETUP
        >>> if phase == GamePhase.MAIN:
        ...     # Handle main game phase
        ...     pass
        >>> # Check if game is over
        >>> is_game_over = phase == GamePhase.END
    """
    SETUP = "setup"
    MAIN = "main"
    SCORING = "scoring"
    END = "end" 
