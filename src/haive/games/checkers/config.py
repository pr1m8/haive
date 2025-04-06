# src/haive/games/checkers/config.py

from typing import Dict, List, Optional, Union, Type
from pydantic import BaseModel, Field
from src.haive.core.engine.agent.agent import AgentConfig
from src.haive.games.checkers.state import CheckersState
from src.haive.core.aug_llm.base import AugLLMConfig
from src.haive.games.checkers.engines import build_checkers_aug_llms

class CheckersAgentConfig(AgentConfig):
    """
    Configuration for checkers game agent.
    
    Attributes:
        board_size: Size of the checkers board (typically 8x8)
        max_turns: Maximum number of turns before the game is declared a draw
        allow_flying_kings: Whether kings can move any distance along diagonals
        mandatory_jumps: Whether jumps are mandatory when available
        state_schema: State schema for the checkers game
    """
    board_size: int = Field(default=8, description="Size of the checkers board")
    max_turns: int = Field(default=100, description="Maximum number of turns before declaring a draw")
    allow_flying_kings: bool = Field(default=False, description="Whether kings can move any distance along diagonals")
    mandatory_jumps: bool = Field(default=True, description="Whether jumps are mandatory when available")
    state_schema: Type[BaseModel] = Field(default=CheckersState, description="State schema for the checkers game")
    engines: Dict[str, AugLLMConfig] = Field(default_factory=build_checkers_aug_llms, description="Engines for the checkers game")
    @classmethod
    def default(cls):
        """Create a default configuration for checkers."""
        return cls(
            name="checkers_agent",
            max_turns=100,
            board_size=8,
            mandatory_jumps=True,
            allow_flying_kings=False
        )
    
    class Config:
        """Pydantic configuration."""
        arbitrary_types_allowed = True