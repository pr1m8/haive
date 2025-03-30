from src.haive.games.framework.base import GameConfig
from .models import WordConnectionsState, WordConnectionsPlayerDecision, WordConnectionsAnalysis
from src.haive.core.engine.aug_llm import AugLLMConfig
from src.haive.core.models.llm.base import AzureLLMConfig
from langchain_core.prompts import ChatPromptTemplate
from pydantic import Field
from typing import Dict, Any, List

# Define the prompts for the agent

def generate_move_prompt() -> ChatPromptTemplate:
    """Generate a prompt for making a move in Word Connections."""
    return ChatPromptTemplate.from_messages([
        ('system', 
            """You are an expert at the Word Connections puzzle game. In this game, you must identify groups of four words that share a common theme or category.

            The game presents a 4x4 grid containing 16 words. Your objective is to correctly group these into four distinct categories of four words each.
            
            Each category has a specific difficulty level:
            - 🟨 Yellow: Easiest to identify (straightforward connections)
            - 🟩 Green: Moderate difficulty (requires some thought)
            - 🟦 Blue: Challenging (connections may be less obvious)
            - 🟪 Purple: Most difficult (connections may involve wordplay, obscure knowledge, or subtle relationships)
            
            You have a limited number of incorrect guesses (4) before the game ends.
            
            RULES:
            1. Each group MUST contain exactly 4 words
            2. Each word belongs to exactly one group
            3. All words in a group must share a SPECIFIC connection (not just a loose association)
            4. Be precise with your reasoning - explain the exact relationship between words
            5. Consider multiple possible connections before finalizing your answer
            
            STRATEGY TIPS:
            - Start with the most obvious connections (look for colors, numbers, categories, etc.)
            - Watch for words that could fit in multiple categories - these are designed to misdirect you
            - Consider wordplay, double meanings, and obscure connections for harder groups
            - Learn from incorrect attempts - they provide valuable clues
            
            The player will see your reasoning, so explain your thought process clearly and comprehensively.
            """
        ),
        ('human', 
            "Current Game State:\n"
            "{board}\n\n"
            "Choose the best group of 4 words that you believe form a category. Think step by step about all possible connections. Be thorough in your analysis and don't rush to conclusions."
        )
    ])


def generate_analysis_prompt() -> ChatPromptTemplate:
    """Generate a prompt for analyzing a Word Connections position."""
    return ChatPromptTemplate.from_messages([
        ('system', 
            """You are a Word Connections puzzle expert and analyst. Your job is to carefully analyze the current board state and provide strategic insights.
            
            For this analysis, think more deeply than just finding the immediate connections. Consider:
            
            1. PATTERN RECOGNITION: Identify all potential categories and connections among the remaining words
            2. CRITICAL EVALUATION: Assess the strength of each potential grouping hypothesis
            3. ERROR ANALYSIS: If there were incorrect attempts, explain why they failed
            4. AMBIGUITY MAPPING: Identify words that could belong to multiple categories
            5. STRATEGIC PLANNING: Suggest the most promising group to try next
            
            Be methodical and thorough. Consider wordplay, double meanings, and less obvious relationships.
            For difficult puzzles, consider categories related to:
            - Phrases, idioms, or sayings
            - Pop culture references
            - Words that can be combined with a common word
            - Words that can be preceded or followed by the same word
            - Words that belong to specialized categories
            
            Your analysis should help the player make better decisions by understanding the puzzle more deeply.
            """
        ),
        ('human', 
            "Current Game State:\n"
            "{board}\n\n"
            "Recent Moves:\n{move_history}\n\n"
            "Provide a detailed analysis including:\n"
            "1. Potential groups of words that might form categories\n"
            "2. Words that seem ambiguous or difficult to categorize\n"
            "3. Patterns you observe in the remaining words\n"
            "4. Analysis of why previous attempts may have failed\n"
            "5. Strategic recommendations for the next move"
        )
    ])


# Define the AugLLM configurations
aug_llm_configs = {
    "player_move": AugLLMConfig(
        name="player_move",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        prompt_template=generate_move_prompt(),
        structured_output_model=WordConnectionsPlayerDecision
    ),
    "game_analyzer": AugLLMConfig(
        name="game_analyzer",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        prompt_template=generate_analysis_prompt(),
        structured_output_model=WordConnectionsAnalysis
    )
}

class WordConnectionsAgentConfig(GameConfig):
    """Configuration for the Word Connections agent."""
    state_schema: type = Field(default=WordConnectionsState)
    aug_llm_configs: Dict[str, AugLLMConfig] = Field(
        default=aug_llm_configs, description="Config for the Word Connections agent."
    )
    enable_analysis: bool = Field(
        default=True, description="Whether to enable analysis."
    )
    visualize: bool = Field(
        default=True, description="Whether to visualize the game."
    )
    auto_submit: bool = Field(
        default=False, description="Whether to automatically submit selections."
    )
    source: str = Field(
        default="internal", description="Source of the game data ('internal' or 'nyt')."
    )
    categories: List[str] = Field(
        default_factory=list, description="Specific categories to use (if empty, use random)."
    )
    
    # Examples of real connections puzzles
    few_shot_examples: List[Dict[str, Any]] = Field(
        default=[
            {
                "categories": {
                    "Units of weight": ["OUNCE", "POUND", "TON", "GRAM"],
                    "High winds": ["GALE", "TORNADO", "CYCLONE", "HURRICANE"],
                    "Financial indicators": ["DOW", "S&P", "NASDAQ", "NYSE"],
                    "Parts of a play": ["ACT", "SCENE", "SCRIPT", "INTERMISSION"]
                },
                "difficulties": {
                    "Units of weight": "yellow",
                    "High winds": "green",
                    "Financial indicators": "blue",
                    "Parts of a play": "purple"
                }
            },
            {
                "categories": {
                    "Card games": ["POKER", "BLACKJACK", "HEARTS", "BRIDGE"],
                    "Hair products": ["GEL", "SPRAY", "MOUSSE", "SHAMPOO"],
                    "Words meaning 'talk'": ["CHAT", "SPEAK", "CONVERSE", "ADDRESS"],
                    "Things with shells": ["TURTLE", "NUT", "EGG", "TACO"]
                },
                "difficulties": {
                    "Card games": "yellow",
                    "Hair products": "green",
                    "Words meaning 'talk'": "blue", 
                    "Things with shells": "purple"
                }
            }
        ],
        description="Examples of real Connections puzzles for reference."
    )

    @classmethod
    def default_config(cls):
        """Create a default configuration."""
        return cls(
            state_schema=WordConnectionsState,
            aug_llm_configs=aug_llm_configs,
            enable_analysis=True,
            visualize=True,
            auto_submit=False,
            source="internal"
        )
        
    @classmethod
    def create_nyt_config(cls):
        """Create a configuration for playing the NYT version."""
        return cls(
            state_schema=WordConnectionsState,
            aug_llm_configs=aug_llm_configs,
            enable_analysis=True,
            visualize=True,
            auto_submit=False,
            source="nyt"
        )