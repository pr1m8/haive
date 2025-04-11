from typing import Dict, List, Optional, Union, Type
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate

from src.haive.core.engine.agent.agent import AgentConfig
from src.haive.core.engine.aug_llm import AugLLMConfig
from src.haive.core.models.llm.base import AzureLLMConfig
from src.haive.games.cards.bs.models import (
    #BullshitGameState, 
    PlayerClaimAction, 
    ChallengeAction,
    Card
)
from src.haive.games.cards.bs.state import BullshitGameState

def generate_claim_prompt() -> ChatPromptTemplate:
    """
    Create a prompt for players to make a claim during their turn.
    """
    return ChatPromptTemplate.from_messages([
        ('system', 
            "You are playing Bullshit (BS), a game of strategic bluffing. "
            "You must decide whether to tell the truth or bluff when playing cards."
        ),
        ('human', 
            "Current Game State:\n"
            "Your Hand: {hand_details}\n"
            "Current Pile Value: {current_pile_value}\n"
            "Number of Cards in Pile: {pile_size}\n"
            "Players' Hand Sizes:\n{player_hand_sizes}\n\n"
            "Decide what value of cards to play and how many. "
            "Choose whether to tell the truth or bluff strategically."
        )
    ])

def generate_challenge_prompt() -> ChatPromptTemplate:
    """
    Create a prompt for players to decide whether to challenge another player.
    """
    return ChatPromptTemplate.from_messages([
        ('system', 
            "You are playing Bullshit (BS). You must decide whether to challenge "
            "another player's claim based on the game state and your observations."
        ),
        ('human', 
            "Current Game State:\n"
            "Your Hand: {hand_details}\n"
            "Last Played Cards Value: {last_played_value}\n"
            "Number of Cards Played: {last_played_cards_count}\n"
            "Players' Hand Sizes:\n{player_hand_sizes}\n\n"
            "Challenge Options:\n"
            "1. Do not challenge\n"
            "2. Challenge the last player's claim\n\n"
            "Decide whether to challenge and explain your reasoning."
        )
    ])

class BullshitAgentConfig(AgentConfig):
    """
    Configuration for a Bullshit (BS) card game agent.
    
    Attributes:
        num_players: Number of players in the game
        max_rounds: Maximum number of rounds to play
        state_schema: State schema for the Bullshit game
    """
    num_players: int = Field(default=4, description="Number of players in the game")
    max_rounds: int = Field(default=20, description="Maximum number of rounds to play")
    state_schema: Type[BaseModel] = Field(default=BullshitGameState, description="State schema for the Bullshit game")
    
    @classmethod
    def build_bullshit_aug_llms(cls) -> Dict[str, AugLLMConfig]:
        """
        Build AugLLM configurations for different game stages.
        """
        return {
            "claim_engine": AugLLMConfig(
                name="claim_engine",
                llm_config=AzureLLMConfig(model="gpt-4o"),
                prompt_template=generate_claim_prompt(),
                structured_output_model=PlayerClaimAction
            ),
            "challenge_engine": AugLLMConfig(
                name="challenge_engine",
                llm_config=AzureLLMConfig(model="gpt-4o"),
                prompt_template=generate_challenge_prompt(),
                structured_output_model=ChallengeAction
            )
        }
    
    @classmethod
    def default(cls):
        """Create a default configuration for Bullshit."""
        return cls(
            name="bullshit_multi_agent",
            num_players=4,
            max_rounds=20,
            engines=cls.build_bullshit_aug_llms()
        )
    
    class Config:
        """Pydantic configuration."""
        arbitrary_types_allowed = True

# Helper function to build engines
def build_bullshit_aug_llms() -> Dict[str, AugLLMConfig]:
    """
    Build AugLLM configurations for the Bullshit game.
    """
    return BullshitAgentConfig.build_bullshit_aug_llms()