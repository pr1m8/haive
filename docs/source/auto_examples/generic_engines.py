"""Generic chess engines using the new generic player agent system.

This module demonstrates how to use the generic player agent system for
chess, providing a clean, type-safe implementation that eliminates
hardcoded LLM configurations.
"""

from typing import Type, Union

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm import LLMConfig
from langchain_core.prompts import ChatPromptTemplate

from haive.games.chess.models import ChessPlayerDecision, SegmentedAnalysis
from haive.games.core.agent.generic_player_agent import (
    ChessPlayerIdentifiers,
    GenericGameEngineFactory,
    GenericPromptGenerator,
)
from haive.games.core.agent.player_agent import PlayerAgentConfig


class ChessPromptGenerator(GenericPromptGenerator[str, str]):
    """Chess-specific prompt generator using the generic system."""

    def create_move_prompt(self, player: str) -> ChatPromptTemplate:
        """Create a chess move prompt for the specified player.

        Args:
            player: Player color ("white" or "black")

        Returns:
            ChatPromptTemplate: Prompt template for move generation
        """
        return ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    f"""You are playing chess as {player.upper()}. You are an expert chess player.

CRITICAL MOVE FORMAT RULES:
- You MUST provide moves in UCI format: start square + end square (e.g., 'e2e4', 'g1f3')
- Castling: {'e1g1' if player == 'white' else 'e8g8'} (kingside), {'e1c1' if player == 'white' else 'e8c8'} (queenside)
- Promotion: add piece letter at end (e.g., 'a7a8q' for queen promotion)
- Do NOT use algebraic notation (e.g., 'Nf3', 'Bxe5')
- Do NOT include piece symbols or capture notation

EXAMPLES OF CORRECT MOVES:
- Pawn move: {'e2e4' if player == 'white' else 'e7e5'} ({'e2' if player == 'white' else 'e7'} to {'e4' if player == 'white' else 'e5'})
- Knight move: {'g1f3' if player == 'white' else 'g8f6'} (knight from {'g1' if player == 'white' else 'g8'} to {'f3' if player == 'white' else 'f6'})
- Capture: 'd4e5' (piece on d4 captures on e5)
- Castle kingside: {'e1g1' if player == 'white' else 'e8g8'}
- Promotion: {'h7h8q' if player == 'white' else 'b2b1n'} (pawn promotes to {'queen' if player == 'white' else 'knight'})

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

    def create_analysis_prompt(self, player: str) -> ChatPromptTemplate:
        """Create a chess analysis prompt for the specified player.

        Args:
            player: Player color ("white" or "black")

        Returns:
            ChatPromptTemplate: Prompt template for position analysis
        """
        return ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    f"""You are analyzing the chess position from {player.upper()}'s perspective.

Provide strategic insights including:
1. Position score from -10 to +10 (positive favors White, negative favors Black)
2. Attacking chances: describe {player.upper()}'s offensive opportunities
3. Defensive needs: identify threats and weaknesses
4. Suggested plans: provide 2-3 concrete strategic plans

Be specific and focus on the current position's tactical and strategic elements.""",
                ),
                (
                    "human",
                    f"""Position (FEN): {{current_board_fen}}

Recent moves: {{recent_moves}}

Captured pieces: {{captured_pieces}}

Analyze this position strategically from {player.upper()}'s perspective.""",
                ),
            ]
        )

    def get_move_output_model(self) -> Type:
        """Get the structured output model for chess moves."""
        return ChessPlayerDecision

    def get_analysis_output_model(self) -> Type:
        """Get the structured output model for chess analysis."""
        return SegmentedAnalysis


# Create the global chess factory instance
chess_players = ChessPlayerIdentifiers()
chess_prompt_generator = ChessPromptGenerator(chess_players)
chess_engine_factory = GenericGameEngineFactory(
    chess_players,
    chess_prompt_generator,
    default_temperature=0.7,
    analyzer_temperature=0.3,
)


# Convenience functions for chess using the generic system


def create_generic_chess_engines(
    player_configs: dict[str, PlayerAgentConfig],
) -> dict[str, AugLLMConfig]:
    """Create chess engines using the generic system.

    Args:
        player_configs: Dictionary of role name to player configuration

    Returns:
        dict[str, AugLLMConfig]: Dictionary of configured engines

    Example:
        >>> configs = {
        ...     "white_player": PlayerAgentConfig(llm_config="gpt-4"),
        ...     "black_player": PlayerAgentConfig(llm_config="claude-3-opus"),
        ...     "white_analyzer": PlayerAgentConfig(llm_config="gpt-4"),
        ...     "black_analyzer": PlayerAgentConfig(llm_config="claude-3-opus"),
        ... }
        >>> engines = create_generic_chess_engines(configs)
    """
    return chess_engine_factory.create_engines_from_player_configs(player_configs)


def create_generic_chess_engines_simple(
    white_model: Union[str, LLMConfig] = "gpt-4o",
    black_model: Union[str, LLMConfig] = "claude-3-5-sonnet-20240620",
    temperature: float = 0.7,
    **kwargs,
) -> dict[str, AugLLMConfig]:
    """Create chess engines with simple model configurations using generics.

    Args:
        white_model: Model for white player and analyzer
        black_model: Model for black player and analyzer
        temperature: Temperature for player engines
        **kwargs: Additional configuration parameters

    Returns:
        dict[str, AugLLMConfig]: Dictionary of engines

    Example:
        >>> engines = create_generic_chess_engines_simple("gpt-4", "claude-3-opus")
        >>> engines = create_generic_chess_engines_simple(
        ...     "anthropic:claude-3-5-sonnet-20240620",
        ...     "openai:gpt-4o",
        ...     temperature=0.8
        ... )
    """
    return chess_engine_factory.create_engines_from_simple_configs(
        white_model, black_model, temperature=temperature, **kwargs
    )


def create_generic_chess_config_from_example(
    example_name: str, temperature: float = 0.7
) -> dict[str, AugLLMConfig]:
    """Create chess engines from predefined examples using generics.

    Args:
        example_name: Name of the example configuration
        temperature: Temperature for all engines

    Returns:
        dict[str, AugLLMConfig]: Dictionary of engines

    Available examples:
        - "anthropic_vs_openai": Claude vs GPT-4
        - "gpt4_only": GPT-4 for all roles
        - "claude_only": Claude for all roles
        - "mixed_providers": Different provider per role
        - "budget_friendly": Cost-effective models
    """
    example_configs = {
        "anthropic_vs_openai": {
            "white": "anthropic:claude-3-5-sonnet-20240620",
            "black": "openai:gpt-4o",
        },
        "gpt4_only": {"white": "openai:gpt-4o", "black": "openai:gpt-4o"},
        "claude_only": {
            "white": "anthropic:claude-3-5-sonnet-20240620",
            "black": "anthropic:claude-3-5-sonnet-20240620",
        },
        "mixed_providers": {
            "white": "anthropic:claude-3-5-sonnet-20240620",
            "black": "openai:gpt-4o",
        },
        "budget_friendly": {
            "white": "openai:gpt-3.5-turbo",
            "black": "groq:llama-3.1-8b-instant",
        },
    }

    if example_name not in example_configs:
        available = ", ".join(example_configs.keys())
        raise ValueError(f"Unknown example '{example_name}'. Available: {available}")

    config = example_configs[example_name]
    return create_generic_chess_engines_simple(
        config["white"], config["black"], temperature=temperature
    )


# Type-safe engine creation with compile-time checking


def create_typed_chess_engines() -> dict[str, AugLLMConfig]:
    """Demonstrate type-safe engine creation using the generic system.

    This function shows how the generic system provides compile-time type checking
    for player identifiers and role names.

    Returns:
        dict[str, AugLLMConfig]: Dictionary of engines
    """
    # The generic system ensures type safety
    players = ChessPlayerIdentifiers()  # player1="white", player2="black"

    # This would cause a type error if we used wrong player names:
    # players = ChessPlayerIdentifiers(player1="red", player2="yellow")  # Type error!

    factory = GenericGameEngineFactory(players, chess_prompt_generator)

    # Create engines with full type safety
    return factory.create_engines_from_simple_configs("gpt-4o", "claude-3-opus")


# Advanced configuration examples


def create_role_specific_chess_engines() -> dict[str, AugLLMConfig]:
    """Create chess engines with different models per role using generics.

    This example shows how to use different LLM models for players vs analyzers,
    demonstrating the flexibility of the generic system.

    Returns:
        dict[str, AugLLMConfig]: Dictionary of engines
    """
    player_configs = {
        "white_player": PlayerAgentConfig(
            llm_config="openai:gpt-4o",
            temperature=0.7,
            player_name="GPT-4 White Player",
        ),
        "black_player": PlayerAgentConfig(
            llm_config="anthropic:claude-3-5-sonnet-20240620",
            temperature=0.7,
            player_name="Claude Black Player",
        ),
        "white_analyzer": PlayerAgentConfig(
            llm_config="google:gemini-1.5-pro",
            temperature=0.3,
            player_name="Gemini White Analyzer",
        ),
        "black_analyzer": PlayerAgentConfig(
            llm_config="groq:llama-3.1-70b-versatile",
            temperature=0.3,
            player_name="Llama Black Analyzer",
        ),
    }

    return create_generic_chess_engines(player_configs)


# Demonstration of cross-game compatibility


def demonstrate_generic_pattern():
    """Demonstrate how the generic pattern works across different games.

    This function shows how the same generic system can be used for any
    two-player game with just different player identifiers and prompts.
    """
    print("🎯 Generic Player Agent System Demonstration")
    print("=" * 50)

    # Chess example
    chess_engines = create_generic_chess_engines_simple("gpt-4", "claude-3-opus")
    print("♟️  Chess engines created:")
    for role in sorted(chess_engines.keys()):
        print(f"   {role}")

    # The same pattern works for any game - just different identifiers
    print("\n🔄 Same pattern works for:")
    print("   - Checkers: red_player, black_player, red_analyzer, black_analyzer")
    print("   - Tic Tac Toe: X_player, O_player, X_analyzer, O_analyzer")
    print("   - Connect4: red_player, yellow_player, red_analyzer, yellow_analyzer")
    print("   - Any two-player game!")

    print("\n✅ Full type safety and compile-time checking")
    print("✅ No hardcoded LLM configurations")
    print("✅ Easy LLM swapping per role")
    print("✅ Cross-game compatibility")


if __name__ == "__main__":
    demonstrate_generic_pattern()
