# src/haive/agents/agent_games/checkers/config.py

from src.haive.games.framework.base import GameConfig
from src.haive.games.checkers.models import CheckersState, CheckersPlayerDecision, CheckersAnalysis
from src.haive.core.engine.aug_llm import AugLLMConfig
from src.haive.core.models.llm.base import AzureLLMConfig
from langchain_core.prompts import ChatPromptTemplate
from pydantic import Field
from typing import Dict

# Define the prompts for each agent

class CheckersAgentConfig(GameConfig):
    """Configuration for the checkers agent."""
    state_schema: type = Field(default=CheckersState)
    aug_llm_configs: Dict[str, AugLLMConfig] = Field(
        default=aug_llm_configs, description="Config for the checkers agent."
    )
    enable_analysis: bool = Field(
        default=True, description="Whether to enable analysis."
    )
    visualize: bool = Field(
        default=True, description="Whether to visualize the game."
    )

    @classmethod
    def default_config(cls):
        """Create a default configuration."""
        return cls(
            state_schema=CheckersState,
            aug_llm_configs=aug_llm_configs,
            enable_analysis=True,
            visualize=True
        )