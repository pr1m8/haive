"""Texas Hold'em Poker game implementation for AI agents.

This package provides a complete implementation of a multi-agent Texas Hold'em
poker game, including:
    - Game state management and progression
    - LLM-based player decision making
    - Hand evaluation and showdown logic
    - Configurable game parameters
    - Detailed game history and statistics

The implementation uses LangGraph for workflow management and supports
multiple LLM providers (Azure, OpenAI, Anthropic) for agent decisions.

Key Components:
    - PokerAgent: Main agent class managing the game
    - PokerState: Game state tracking and management
    - PokerAgentConfig: Configuration for game setup
    - Models: Data models for cards, players, and decisions
    - Engines: LLM configurations and prompts

Example:
    >>> from src.haive.agents.agent_games.poker import PokerAgent, PokerAgentConfig
    >>> 
    >>> # Create a game with 4 players
    >>> config = PokerAgentConfig(
    ...     player_names=["Alice", "Bob", "Charlie", "Dave"],
    ...     starting_chips=1000,
    ...     small_blind=5,
    ...     big_blind=10
    ... )
    >>> 
    >>> agent = PokerAgent(config)
    >>> result = agent.run()
"""

from src.haive.games.poker.agent import PokerAgent
from src.haive.games.poker.config import PokerAgentConfig
from src.haive.games.poker.state import PokerState
from src.haive.games.poker.state_manager import PokerStateManager
from src.haive.games.poker.models import (
    Card, Hand, Player, PlayerAction, GamePhase,
    AgentDecision, PlayerObservation, GameResult
)
from src.haive.games.poker.engines import poker_agent_configs

__all__ = [
    'PokerAgent',
    'PokerAgentConfig',
    'PokerState',
    'PokerStateManager',
    'Card',
    'Hand',
    'Player',
    'PlayerAction',
    'GamePhase',
    'AgentDecision',
    'PlayerObservation',
    'GameResult',
    'poker_agent_configs'
]

# Version of the poker game implementation
__version__ = '1.0.0'
