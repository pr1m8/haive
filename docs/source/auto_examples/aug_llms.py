"""Chess game augmented LLM configurations module.

This module provides augmented LLM configurations for the chess game, including:
    - Move generation prompts for white and black players
    - Position analysis prompts for both sides
    - Structured output models for moves and analysis
    - Pre-configured LLM configurations for easy agent setup

The module provides an alternative to the engines.py approach, with a focus
on customizability and different prompt styles for chess gameplay.

Example:
    >>> from haive.games.chess.aug_llms import aug_llm_configs
    >>>
    >>> # Access white player's move generation configuration
    >>> white_config = aug_llm_configs["white_player"]
    >>> white_prompt = white_config.prompt_template
"""

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig, DeepSeekLLMConfig, LLMConfig
from langchain.prompts import ChatPromptTemplate

from haive.games.chess.models import ChessAnalysis, ChessPlayerDecision


def generate_move_prompt(color: str) -> ChatPromptTemplate:
    """Generate a move prompt for a given player color.

    Creates a ChatPromptTemplate with system and human messages designed
    to elicit high-quality chess moves from an LLM.

    Args:
        color (str): Player color ("white" or "black")

    Returns:
        ChatPromptTemplate: A prompt template for generating chess moves

    Examples:
        >>> white_prompt = generate_move_prompt("white")
        >>> isinstance(white_prompt, ChatPromptTemplate)
        True
        >>> "UCI format" in white_prompt.messages[0][1]
        True
    """
    return ChatPromptTemplate.from_messages(
        [
            (
                "system",
                f"You are the {color} chess player. Your goal is to play the best possible move according to chess strategy.\n"
                "Ensure your move is legal and follows chess rules, provided in **UCI format** (e.g., e2e4, g8f6).",
            ),
            (
                "human",
                "📌 **Game Context for {color}:**\n"
                "♟️ **Current Board Position (FEN):** {current_board_fen}\n"
                "🕰️ **Previous Board Position (FEN):** {previous_board_fen}\n"
                "📜 **Move History (Last 5 Moves):** {recent_moves}\n"
                "🎯 **Captured Pieces:** {captured_pieces}\n\n"
                "🔍 **Your Last {color} Analysis:** {player_analysis}\n"
                "⚠️ **Opponent's Plans Are Hidden** (You only see your perspective)\n\n"
                f"💡 **Your Turn! Choose the best move for {color}** in **UCI format** (e.g., e2e4, d2d4, etc.).",
            ),
        ]
    )


def generate_analysis_prompt(color: str) -> ChatPromptTemplate:
    """Generate an analysis prompt for a given player color.

    Creates a ChatPromptTemplate with system and human messages designed
    to elicit detailed position analysis from an LLM.

    Args:
        color (str): Player color ("white" or "black")

    Returns:
        ChatPromptTemplate: A prompt template for generating chess position analysis

    Examples:
        >>> black_prompt = generate_analysis_prompt("black")
        >>> isinstance(black_prompt, ChatPromptTemplate)
        True
        >>> "strategic themes" in black_prompt.messages[1][1]
        True
    """
    return ChatPromptTemplate.from_messages(
        [
            (
                "system",
                f"You are analyzing {color}'s position in a chess game. Your task is to evaluate the strategic outlook.",
            ),
            (
                "human",
                "📌 **Game Analysis for {color}:**\n"
                "♟️ **Current Board Position (FEN):** {current_board_fen}\n"
                "🕰️ **Previous Board Position (FEN):** {previous_board_fen}\n"
                "📜 **Move History (Last 5 Moves):** {recent_moves}\n"
                "🎯 **Captured Pieces:** {captured_pieces}\n\n"
                "📝 **Your Task:**\n"
                "1️⃣ Assess {color}'s overall **position strength**.\n"
                "2️⃣ Identify key **strategic themes** for {color}.\n"
                "3️⃣ Suggest optimal **next moves** and long-term plans.",
            ),
        ]
    )


def build_chess_aug_llms_per_color(
    *,
    white_llm: LLMConfig | None = AzureLLMConfig(),
    black_llm: LLMConfig | None = DeepSeekLLMConfig(),
) -> dict[str, AugLLMConfig]:
    """Build LLM configs for both players and analyzers using per-color LLMs.

    Creates a comprehensive set of AugLLMConfig objects for chess gameplay,
    allowing different LLM providers for white and black players.

    Args:
        white_llm (LLMConfig | None): LLM configuration for white player and analyzer
        black_llm (LLMConfig | None): LLM configuration for black player and analyzer

    Returns:
        dict[str, AugLLMConfig]: Dictionary with configurations for all chess roles

    Examples:
        >>> # Using default LLMs
        >>> configs = build_chess_aug_llms_per_color()
        >>> len(configs)
        4
        >>> sorted(list(configs.keys()))
        ['black_analyzer', 'black_player', 'white_analyzer', 'white_player']

        >>> # Using custom LLMs
        >>> from haive.core.models.llm.base import AnthropicLLMConfig
        >>> configs = build_chess_aug_llms_per_color(
        ...     white_llm=AnthropicLLMConfig(model="claude-3-opus-20240229"),
        ...     black_llm=AnthropicLLMConfig(model="claude-3-sonnet-20240229"),
        ... )
        >>> configs["white_player"].llm_config.model
        'claude-3-opus-20240229'
    """
    print(white_llm)
    print(black_llm)

    return {
        "white_player": AugLLMConfig(
            llm_config=white_llm,
            prompt_template=generate_move_prompt("white"),
            structured_output_model=ChessPlayerDecision,
            description="White player move generation",
        ),
        "white_analyzer": AugLLMConfig(
            llm_config=white_llm,
            prompt_template=generate_analysis_prompt("white"),
            structured_output_model=ChessAnalysis,
            description="White position analysis",
        ),
        "black_player": AugLLMConfig(
            llm_config=black_llm,
            prompt_template=generate_move_prompt("black"),
            structured_output_model=ChessPlayerDecision,
            description="Black player move generation",
        ),
        "black_analyzer": AugLLMConfig(
            llm_config=black_llm,
            prompt_template=generate_analysis_prompt("black"),
            structured_output_model=ChessAnalysis,
            description="Black position analysis",
        ),
    }


# Default LLMs fallback
aug_llm_configs: dict[str, AugLLMConfig] = build_chess_aug_llms_per_color()
