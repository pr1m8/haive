from typing import Dict, List, Optional, Union, Type
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate

from src.haive.core.engine.agent.agent import AgentConfig
from src.haive.core.engine.aug_llm import AugLLMConfig
from src.haive.core.models.llm.base import AzureLLMConfig
from src.haive.games.cards.blackjack.models import (
    BlackjackGameState, 
    PlayerAction, 
    PlayerState
)

# Prompts for Betting
def generate_betting_prompt() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages([
        ('system', 
            "You are a strategic Blackjack player managing your chips. "
            "Your goal is to place a smart bet based on your current chip stack "
            "and the game context."
        ),
        ('human', 
            "Current Chip Stack: ${total_chips}\n"
            "Previous Round Summary: {previous_round_summary}\n"
            "Game Context: {game_context}\n\n"
            "Determine a strategic bet amount. Consider your chip stack, "
            "recent performance, and risk tolerance. Provide your reasoning."
        )
    ])

# Prompts for Player Actions
def generate_player_action_prompt() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages([
        ('system', 
            "You are a strategic Blackjack player making decisions to maximize your chances of winning. "
            "Analyze the current hand carefully and choose the most appropriate action."
        ),
        ('human', 
            "Your Hand: {hand_details}\n"
            "Dealer's Visible Card: {dealer_card}\n"
            "Current Bet: ${current_bet}\n"
            "Chip Stack: ${total_chips}\n"
            "Possible Actions: hit, stand, double_down, split, surrender\n\n"
            "Decide your next move and explain your reasoning."
        )
    ])

# Blackjack Agent Configuration
class BlackjackAgentConfig(AgentConfig):
    """
    Configuration for a multi-player Blackjack game agent.
    
    Attributes:
        num_players: Number of players in the game
        max_rounds: Maximum number of rounds to play
        initial_chips: Starting chip amount for each player
        state_schema: State schema for the Blackjack game
    """
    num_players: int = Field(default=2, description="Number of players in the game")
    max_rounds: int = Field(default=10, description="Maximum number of rounds to play")
    initial_chips: float = Field(default=1000.0, description="Starting chip amount for each player")
    state_schema: Type[BaseModel] = Field(default=BlackjackGameState, description="State schema for the Blackjack game")
    
    # Define engines for different game stages
    @classmethod
    def build_blackjack_aug_llms(cls) -> Dict[str, AugLLMConfig]:
        """
        Build AugLLM configurations for different game stages.
        """
        return {
            "betting_engine": AugLLMConfig(
                name="betting_engine",
                llm_config=AzureLLMConfig(model="gpt-4o"),
                prompt_template=generate_betting_prompt(),
                structured_output_model=float  # Bet amount
            ),
            "player_action_engine": AugLLMConfig(
                name="player_action_engine",
                llm_config=AzureLLMConfig(model="gpt-4o"),
                prompt_template=generate_player_action_prompt(),
                structured_output_model=PlayerAction
            )
        }
    
    # Default configuration method
    @classmethod
    def default(cls):
        """Create a default configuration for Blackjack."""
        return cls(
            name="blackjack_multi_agent",
            num_players=2,
            max_rounds=10,
            initial_chips=1000.0,
            engines=cls.build_blackjack_aug_llms()
        )
    
    class Config:
        """Pydantic configuration."""
        arbitrary_types_allowed = True

# Helper function to build engines
def build_blackjack_aug_llms() -> Dict[str, AugLLMConfig]:
    """
    Build AugLLM configurations for the Blackjack game.
    """
    return BlackjackAgentConfig.build_blackjack_aug_llms()