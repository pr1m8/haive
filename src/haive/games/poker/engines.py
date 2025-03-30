"""Poker agent LLM configurations and prompts.

This module defines the language model configurations and prompt templates
for different poker playing styles and roles. It includes:
    - Player prompt generation for different styles
    - Hand analysis prompt generation
    - LLM provider selection and configuration
    - Agent configuration creation

The module supports multiple LLM providers (Azure, DeepSeek, Anthropic, Gemini, Mistral) and
configures them with appropriate models and prompts for poker gameplay.
"""

import os
from typing import Dict, List, Optional, Union
from langchain_core.prompts import ChatPromptTemplate

from src.haive.core.engine.aug_llm import AugLLMConfig
from src.haive.core.models.llm.base import (
    AzureLLMConfig, LLMProvider, DeepSeekLLMConfig, 
    AnthropicLLMConfig, GeminiLLMConfig, MistralLLMConfig
)
from src.haive.games.poker.models import AgentDecisionSchema

# === Poker Player Prompts ===
def generate_poker_prompt(player_style: str) -> ChatPromptTemplate:
    """Generate a structured prompt for a poker player."""
    return ChatPromptTemplate.from_messages([
        ('system', 
            f"You are a {player_style} poker player in a game of Texas Hold'em. "
            "Your goal is to make strategic decisions based on your hand, the game state, "
            "opponent actions, and pot size. Your playing style should align with your description."
        ),
        ('human', 
            "Game State:\n"
            "- Player Name: {player_id}\n"
            "- Position: {position_name}\n"
            "- Phase: {phase}\n"
            "- Hand: {hand}\n"
            "- Community Cards: {community_cards}\n"
            "- Chips: {chips}\n"
            "- Current Bet: {current_bet}\n"
            "- Pot Size: {pot_size}\n\n"
            "Recent Actions:\n{recent_actions}\n\n"
            "Players Summary:\n{player_states}\n\n"
            "Legal Moves: {legal_moves}\n\n"
            "Make your move and provide reasoning."
        )
    ])

def generate_hand_analysis_prompt() -> ChatPromptTemplate:
    """Generate a structured prompt for poker hand analysis."""
    return ChatPromptTemplate.from_messages([
        ('system', 
            "You are an expert poker hand analyzer. Your task is to evaluate the strength of hands, "
            "potential draws, and probabilities of winning given the board state."
        ),
        ('human', 
            "Game State:\n"
            "- Player Hand: {hand}\n"
            "- Community Cards: {community_cards}\n"
            "- Opponent Actions: {recent_actions}\n\n"
            "Analyze the situation and determine the best move."
        )
    ])
def get_available_providers() -> List[LLMProvider]:
    """Determine all available LLM providers based on environment variables."""
    available_providers = []
    
    # Check each provider individually to avoid using LLMProvider as dict key
    if os.getenv("DEEPSEEK_API_KEY"):
        available_providers.append(LLMProvider.DEEPSEEK)
    
    if os.getenv("ANTHROPIC_API_KEY"):
        available_providers.append(LLMProvider.ANTHROPIC)
    
    if os.getenv("AZURE_OPENAI_API_KEY"):
        available_providers.append(LLMProvider.AZURE)
    
    if os.getenv("GOOGLE_API_KEY"):
        available_providers.append(LLMProvider.GEMINI)
    
    if os.getenv("MISTRAL_API_KEY"):
        available_providers.append(LLMProvider.MISTRALAI)
    
    # If no providers are available, default to Azure
    if not available_providers:
        available_providers.append(LLMProvider.AZURE)
    
    return available_providers

def get_poker_llm_provider() -> LLMProvider:
    """Determine the best available LLM provider."""
    providers = get_available_providers()
    
    # Define priority order
    priority_order = [
        LLMProvider.DEEPSEEK,
        LLMProvider.ANTHROPIC,
        LLMProvider.GEMINI,
        LLMProvider.MISTRALAI,
        LLMProvider.AZURE
    ]
    
    # Return the highest priority available provider
    for provider in priority_order:
        if provider in providers:
            return provider
    
    # Default fallback
    return LLMProvider.AZURE
def get_model_for_provider(provider: LLMProvider) -> str:
    """Get the best model for a given provider."""
    # Avoid using dict with LLMProvider as key
    if provider == LLMProvider.DEEPSEEK:
        return "deepseek-chat"
    elif provider == LLMProvider.ANTHROPIC:
        return "claude-3-opus-20240229"
    elif provider == LLMProvider.GEMINI:
        return "gemini-1.5-pro"
    elif provider == LLMProvider.MISTRALAI:
        return "mistral-large-latest"
    else:
        # Default to Azure model
        return "gpt-4o"
def create_llm_config_for_provider(provider: LLMProvider, **kwargs):
    """Create an LLM configuration for a specific provider."""
    # Get the model name for this provider
    model = get_model_for_provider(provider)
    
    # Create the appropriate config class based on provider
    # Avoid using dict with LLMProvider as key
    if provider == LLMProvider.DEEPSEEK:
        config_class = DeepSeekLLMConfig
    elif provider == LLMProvider.ANTHROPIC:
        config_class = AnthropicLLMConfig
    elif provider == LLMProvider.GEMINI:
        config_class = GeminiLLMConfig
    elif provider == LLMProvider.MISTRALAI:
        config_class = MistralLLMConfig
    else:
        # Default to Azure
        config_class = AzureLLMConfig
    
    # Create base configuration with default values
    base_config = {
        "model": model,
        "temperature": 0.6,
        #"max_tokens": 150
    }
    
    # Override defaults with any provided kwargs
    base_config.update(kwargs)
    
    return config_class(**base_config)
# === Poker Agent Configurations ===
def create_poker_agent_configs() -> Dict[str, AugLLMConfig]:
    """Create structured configurations for poker agents."""
    # Get primary provider with fallbacks
    provider = get_poker_llm_provider()
    llm_config = create_llm_config_for_provider(provider)
    
    return {
        "conservative_agent": AugLLMConfig(
            name="conservative_player",
            llm_config=llm_config,
            prompt_template=generate_poker_prompt("tight and risk-averse"),
            structured_output_model=AgentDecisionSchema
        ),
        "aggressive_agent": AugLLMConfig(
            name="aggressive_player",
            llm_config=llm_config,
            prompt_template=generate_poker_prompt("aggressive and bluffs often"),
            structured_output_model=AgentDecisionSchema
        ),
        "balanced_agent": AugLLMConfig(
            name="balanced_player",
            llm_config=llm_config,
            prompt_template=generate_poker_prompt("balanced and adaptive"),
            structured_output_model=AgentDecisionSchema
        ),
        "loose_agent": AugLLMConfig(
            name="loose_player",
            llm_config=llm_config,
            prompt_template=generate_poker_prompt("loose and plays many hands"),
            structured_output_model=AgentDecisionSchema
        ),
        "hand_analyzer": AugLLMConfig(
            name="hand_analyzer",
            llm_config=llm_config, 
            prompt_template=generate_hand_analysis_prompt(),
            structured_output_model=AgentDecisionSchema
        )
    }

# Updated version of create_default_agent_configs to work with various providers
def create_default_agent_configs(config):
    """Create default configurations for poker agents based on config."""
    # The issue is here - we need to properly handle LLMProvider instances
    providers = get_available_providers()
    
    # Create configurations for poker playing styles
    poker_configs = create_poker_agent_configs()
    
    # Add these to the config engines
    if not hasattr(config, 'engines') or config.engines is None:
        config.engines = {}
    
    config.engines.update(poker_configs)
    
    return config
# === Exposed Agent Configuration ===
poker_agent_configs = create_poker_agent_configs()