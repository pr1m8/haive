# src/haive/agents/agent_games/dominoes/config.py

from src.haive.games.framework.base.config import GameConfig
from src.haive.games.dominoes.state import DominoesState
from src.haive.core.engine.aug_llm import AugLLMConfig
from src.haive.games.dominoes.engines import aug_llm_configs
from pydantic import Field
from typing import Dict

class DominoesAgentConfig(GameConfig):
    """Configuration for the dominoes agent."""
    state_schema: type = Field(default=DominoesState)
    engines: Dict[str, AugLLMConfig] = Field(
        default=aug_llm_configs, description="Config for the dominoes agent."
    )
    enable_analysis: bool = Field(
        default=True, description="Whether to enable analysis."
    )
    visualize: bool = Field(
        default=True, description="Whether to visualize the game."
    )
    hand_size: int = Field(
        default=7, description="Number of tiles per player at start."
    )

    @classmethod
    def default_config(cls):
        """Create a default configuration."""
        return cls(
            state_schema=DominoesState,
            engines=aug_llm_configs,
            enable_analysis=True,
            visualize=True,
            hand_size=7
        )