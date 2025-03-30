from src.haive.games.nim.state import NimState
from src.haive.core.engine.aug_llm import AugLLMConfig
from src.haive.games.framework.base.config import GameConfig
from typing import Dict, List, Type
from pydantic import Field  

class NimConfig(GameConfig):
    """Configuration for the Nim agent."""
    state_schema: Type[NimState] = Field(default=NimState)
    aug_llm_configs: Dict[str, AugLLMConfig] = Field(
        default=aug_llm_configs, description="Config for the Nim agent."
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
        """Create a default configuration."""
        return cls(
            state_schema=NimState,
            aug_llm_configs=aug_llm_configs,
            enable_analysis=True,
            visualize=True,
            pile_sizes=[3, 5, 7],
            misere_mode=False
        )