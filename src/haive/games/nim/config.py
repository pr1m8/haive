"""
Configuration for the Nim game.

This module defines the configuration for the Nim game,
which includes the state schema, engines, enable_analysis,
visualize, and pile_sizes.
"""
from src.haive.games.nim.state import NimState
from src.haive.core.engine.aug_llm import AugLLMConfig
from src.haive.games.framework.base.config import GameConfig
from typing import Dict, List, Type
from pydantic import Field  
from src.haive.games.nim.engines import default_nim_engines
class NimConfig(GameConfig):
    """Configuration for the Nim agent.

    Attributes:
        state_schema (Type[NimState]): The state schema for the Nim game.
        engines (Dict[str, AugLLMConfig]): The engines for the Nim game.
        enable_analysis (bool): Whether to enable analysis.
        visualize (bool): Whether to visualize the game.
    """
    state_schema: Type[NimState] = Field(default=NimState)
    engines: Dict[str, AugLLMConfig] = Field(
        default=default_nim_engines, description="Config for the Nim agent."
    )
    enable_analysis: bool = Field(
        default=True, description="Whether to enable analysis."
    )
    visualize: bool = Field(
        default=True, description="Whether to visualize the game."
    )
    pile_sizes: List[int] = Field(
        default=[3, 5, 7], description="Initial pile sizes."
    )
    misere_mode: bool = Field(
        default=False, description="If True, player taking last stone loses."
    )

    @classmethod
    def default_config(cls):
        """Create a default configuration.

        Returns:
            NimConfig: The default configuration.
        """
        return cls(
            state_schema=NimState,
            engines=default_nim_engines,
            enable_analysis=True,
            visualize=True,
            pile_sizes=[3, 5, 7],
            misere_mode=False
        )