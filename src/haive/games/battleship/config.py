# ================================================
# 1. Configuration
# ================================================

from pydantic import BaseModel, Field
from src.haive.core.engine.aug_llm import AugLLMConfig

class BattleshipAgentConfig(BaseModel):
    """Configuration for the Battleship agent."""
    player1_name: str = Field(default="Player 1", description="Name of player 1")
    player2_name: str = Field(default="Player 2", description="Name of player 2")
    model_name: str = Field(default="gpt-4-turbo", description="LLM model to use")
    temperature: float = Field(default=0.5, description="Temperature for LLM")
    visualize: bool = Field(default=True, description="Whether to visualize the game state")
    save_history: bool = Field(default=True, description="Whether to save game history")
    output_dir: str = Field(default="./game_history", description="Directory for output files")
    enable_analysis: bool = Field(default=True, description="Whether to enable game analysis")
