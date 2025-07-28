"""Configurable chess engines using the new player agent system.

This module provides chess engine configurations that use configurable
player agents instead of hardcoded LLM configurations, making it easy to
switch LLMs for different players.
"""

from typing import Dict

from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.prompts import ChatPromptTemplate

from haive.games.chess.models import ChessPlayerDecision, SegmentedAnalysis
from haive.games.core.agent.player_agent import (
    GamePlayerRole,
    PlayerAgentConfig,
    PlayerAgentFactory,
    create_simple_player_configs,
)


def create_chess_move_prompt(color: str) -> ChatPromptTemplate:
    """Create a chess move prompt for the specified color.

    Args:
        color: Player color ("white" or "black")

    Returns:
        ChatPromptTemplate: Prompt template for move generation
    """
    return ChatPromptTemplate.from_messages(
        [
            (
                "system",
                f"""You are playing chess as {color.upper()}. You are an expert chess player.

CRITICAL MOVE FORMAT RULES:
- You MUST provide moves in UCI format: start square + end square (e.g., 'e2e4', 'g1f3')
- Castling: {'e1g1' if color == 'white' else 'e8g8'} (kingside), {'e1c1' if color == 'white' else 'e8c8'} (queenside)
- Promotion: add piece letter at end (e.g., 'a7a8q' for queen promotion)
- Do NOT use algebraic notation (e.g., 'Nf3', 'Bxe5')
- Do NOT include piece symbols or capture notation

EXAMPLES OF CORRECT MOVES:
- Pawn move: {'e2e4' if color == 'white' else 'e7e5'} ({'e2' if color == 'white' else 'e7'} to {'e4' if color == 'white' else 'e5'})
- Knight move: {'g1f3' if color == 'white' else 'g8f6'} (knight from {'g1' if color == 'white' else 'g8'} to {'f3' if color == 'white' else 'f6'})
- Capture: 'd4e5' (piece on d4 captures on e5)
- Castle kingside: {'e1g1' if color == 'white' else 'e8g8'}
- Promotion: {'h7h8q' if color == 'white' else 'b2b1n'} (pawn promotes to {'queen' if color == 'white' else 'knight'})

{{error_context}}

Evaluate the position carefully and select the best strategic move from the legal moves provided.""",
            ),
            (
                "human",
                """Current position (FEN): {current_board_fen}

Recent moves: {recent_moves}

Captured pieces: {captured_pieces}

LEGAL MOVES AVAILABLE:
{legal_moves}

You MUST select one of the legal moves listed above. Analyze the position and choose your move.""",
            ),
        ]
    )


def create_chess_analysis_prompt(color: str) -> ChatPromptTemplate:
    """Create a chess analysis prompt for the specified color.

    Args:
        color: Player color ("white" or "black")

    Returns:
        ChatPromptTemplate: Prompt template for position analysis
    """
    return ChatPromptTemplate.from_messages(
        [
            (
                "system",
                f"""You are analyzing the chess position from {color.upper()}'s perspective.

Provide strategic insights including:
1. Position score from -10 to +10 (positive favors White, negative favors Black)
2. Attacking chances: describe {color.title()}'s offensive opportunities
3. Defensive needs: identify threats and weaknesses
4. Suggested plans: provide 2-3 concrete strategic plans

Be specific and focus on the current position's tactical and strategic elements.""",
            ),
            (
                "human",
                """Position (FEN): {current_board_fen}

Recent moves: {recent_moves}

Captured pieces: {captured_pieces}

Analyze this position strategically from {color.title()}'s perspective.""",
            ),
        ]
    )


def get_chess_role_definitions() -> Dict[str, GamePlayerRole]:
    """Get role definitions for chess players and analyzers.

    Returns:
        Dict[str, GamePlayerRole]: Dictionary of role definitions
    """
    return {
        "white_player": GamePlayerRole(
            role_name="white_player",
            prompt_template=create_chess_move_prompt("white"),
            structured_output_model=ChessPlayerDecision,
            temperature=0.7,
            description="White player move generation",
        ),
        "black_player": GamePlayerRole(
            role_name="black_player",
            prompt_template=create_chess_move_prompt("black"),
            structured_output_model=ChessPlayerDecision,
            temperature=0.7,
            description="Black player move generation",
        ),
        "white_analyzer": GamePlayerRole(
            role_name="white_analyzer",
            prompt_template=create_chess_analysis_prompt("white"),
            structured_output_model=SegmentedAnalysis,
            temperature=0.7,
            description="White position analysis",
        ),
        "black_analyzer": GamePlayerRole(
            role_name="black_analyzer",
            prompt_template=create_chess_analysis_prompt("black"),
            structured_output_model=SegmentedAnalysis,
            temperature=0.7,
            description="Black position analysis",
        ),
    }


def create_configurable_chess_engines(
    player_configs: Dict[str, PlayerAgentConfig],
) -> Dict[str, AugLLMConfig]:
    """Create chess engines from configurable player agents.

    Args:
        player_configs: Dictionary of role name to player configuration

    Returns:
        Dict[str, AugLLMConfig]: Dictionary of configured engines

    Example:
        >>> configs = {
        ...     "white_player": PlayerAgentConfig(llm_config="gpt-4"),
        ...     "black_player": PlayerAgentConfig(llm_config="claude-3-opus"),
        ...     "white_analyzer": PlayerAgentConfig(llm_config="gpt-4"),
        ...     "black_analyzer": PlayerAgentConfig(llm_config="claude-3-opus"),
        ... }
        >>> engines = create_configurable_chess_engines(configs)
    """
    roles = get_chess_role_definitions()
    return PlayerAgentFactory.create_engines_from_player_configs(roles, player_configs)


# Convenience functions for common chess configurations


def create_anthropic_vs_openai_engines(
    white_model: str = "claude-3-5-sonnet-20240620",
    black_model: str = "gpt-4o",
    temperature: float = 0.7,
) -> Dict[str, AugLLMConfig]:
    """Create chess engines with Anthropic vs OpenAI models.

    Args:
        white_model: Anthropic model for white player
        black_model: OpenAI model for black player
        temperature: Temperature for all engines

    Returns:
        Dict[str, AugLLMConfig]: Dictionary of engines
    """
    configs = create_simple_player_configs(
        white_model=f"anthropic:{white_model}",
        black_model=f"openai:{black_model}",
        temperature=temperature,
    )
    return create_configurable_chess_engines(configs)


def create_same_model_engines(
    model: str = "gpt-4o", temperature: float = 0.7
) -> Dict[str, AugLLMConfig]:
    """Create chess engines using the same model for all roles.

    Args:
        model: Model string to use for all roles
        temperature: Temperature for all engines

    Returns:
        Dict[str, AugLLMConfig]: Dictionary of engines
    """
    configs = create_simple_player_configs(
        white_model=model, black_model=model, temperature=temperature
    )
    return create_configurable_chess_engines(configs)


def create_mixed_provider_engines(
    providers: Dict[str, str] = None, temperature: float = 0.7
) -> Dict[str, AugLLMConfig]:
    """Create chess engines with different providers for each role.

    Args:
        providers: Dictionary of role to model string
        temperature: Temperature for all engines

    Returns:
        Dict[str, AugLLMConfig]: Dictionary of engines
    """
    if providers is None:
        providers = {
            "white_player": "anthropic:claude-3-5-sonnet-20240620",
            "black_player": "openai:gpt-4o",
            "white_analyzer": "google:gemini-1.5-pro",
            "black_analyzer": "groq:llama-3.1-70b-versatile",
        }

    configs = {}
    for role, model in providers.items():
        configs[role] = PlayerAgentConfig(
            llm_config=model,
            temperature=temperature,
            player_name=role.replace("_", " ").title(),
        )

    return create_configurable_chess_engines(configs)


# Example configurations for easy testing

EXAMPLE_CONFIGS = {
    "anthropic_vs_openai": lambda: create_anthropic_vs_openai_engines(),
    "gpt4_only": lambda: create_same_model_engines("gpt-4o"),
    "claude_only": lambda: create_same_model_engines("claude-3-5-sonnet-20240620"),
    "mixed_providers": lambda: create_mixed_provider_engines(),
    "budget_friendly": lambda: create_mixed_provider_engines(
        {
            "white_player": "openai:gpt-3.5-turbo",
            "black_player": "groq:llama-3.1-8b-instant",
            "white_analyzer": "openai:gpt-3.5-turbo",
            "black_analyzer": "groq:llama-3.1-8b-instant",
        }
    ),
}


def get_example_engines(config_name: str) -> Dict[str, AugLLMConfig]:
    """Get example engine configuration by name.

    Args:
        config_name: Name of the configuration from EXAMPLE_CONFIGS

    Returns:
        Dict[str, AugLLMConfig]: Dictionary of engines

    Available configs: anthropic_vs_openai, gpt4_only, claude_only,
                      mixed_providers, budget_friendly
    """
    if config_name not in EXAMPLE_CONFIGS:
        available = ", ".join(EXAMPLE_CONFIGS.keys())
        raise ValueError(f"Unknown config '{config_name}'. Available: {available}")

    return EXAMPLE_CONFIGS[config_name]()
