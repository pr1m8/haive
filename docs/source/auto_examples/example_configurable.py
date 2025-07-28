"""Example of running chess with configurable LLMs.

This example demonstrates how to run chess games with different LLM
providers and models, showing the flexibility of the new configuration
system.
"""

import uuid

# from haive.games.chess.agent import ChessAgent  # TODO: ChessAgent not implemented
from haive.games.chess.config import ChessConfig
from haive.games.chess.llm_utils import (
    create_chess_engines_from_config,
    create_chess_engines_simple,
    get_available_chess_providers,
    get_recommended_chess_models,
)
from haive.games.chess.state import ChessState


def run_chess_with_custom_llms(
    white_provider: str = "anthropic",
    white_model: str = None,
    black_provider: str = "anthropic",
    black_model: str = None,
    max_moves: int = 50,
    enable_analysis: bool = True,
):
    """Run a chess game with custom LLM configurations.

    Args:
        white_provider: LLM provider for white (e.g., "anthropic", "openai")
        white_model: Model for white (uses default if None)
        black_provider: LLM provider for black
        black_model: Model for black (uses default if None)
        max_moves: Maximum moves before draw
        enable_analysis: Whether to enable position analysis
    """
    thread_id = f"chess_{uuid.uuid4().hex[:8]}"
    print(f"🎮 Starting chess game with thread_id: {thread_id}")
    print(f"⚪ White: {white_provider} ({white_model or 'default'})")
    print(f"⚫ Black: {black_provider} ({black_model or 'default'})")
    print("-" * 50)

    # Create engines with custom LLMs
    engines = create_chess_engines_simple(
        white_provider=white_provider,
        white_model=white_model,
        black_provider=black_provider,
        black_model=black_model,
        enable_analysis=enable_analysis,
    )

    # Create configuration
    config = ChessConfig(
        name="Configurable Chess Game",
        engines=engines,
        enable_analysis=enable_analysis,
        max_moves=max_moves,
        # Ensure high recursion limit
        runnable_config={
            "configurable": {
                "thread_id": thread_id,
                "recursion_limit": 600,  # Extra buffer
            }
        },
    )

    # Create agent and initial state
    agent = ChessAgent(config)
    initial_state = ChessState()

    # Run the game
    try:
        app = agent.app
        move_count = 0

        for step in app.stream(
            initial_state.model_dump(),
            config=config.runnable_config,
            stream_mode="values",
        ):
            # Track moves
            if "move_history" in step:
                current_moves = len(step["move_history"])
                if current_moves > move_count:
                    move_count = current_moves
                    last_move = step["move_history"][-1]
                    print(f"Move {move_count}: {last_move[0]} played {last_move[1]}")

            # Check game status
            if step.get("game_result"):
                print("\n" + "=" * 50)
                print(f"🏁 Game ended: {step['game_result']}")
                print(f"📊 Total moves: {move_count}")
                break

    except Exception as e:
        print(f"\n❌ Error during game: {e}")
        import traceback

        traceback.print_exc()


def run_advanced_chess_example():
    """Run an example with advanced configuration."""
    print("🔧 Advanced Chess Configuration Example")
    print("=" * 60)

    # Create custom engine configurations
    engines = create_chess_engines_from_config(
        white_config={
            "provider": "anthropic",
            "model": "claude-3-5-sonnet-20240620",
            "temperature": 0.7,
        },
        black_config={
            "provider": "openai",
            "model": "gpt-4o",
            "temperature": 0.7,
        },
        # Use different models for analysis
        analyzer_configs={
            "white": {
                "provider": "azure",
                "model": "gpt-4o",
                "temperature": 0.5,  # Lower for analysis
            },
            "black": {
                "provider": "azure",
                "model": "gpt-4o",
                "temperature": 0.5,
            },
        },
    )

    # Create configuration with custom engines
    config = ChessConfig(
        name="Advanced Chess Game",
        engines=engines,
        enable_analysis=True,
        max_moves=100,
    )

    # Run the game
    ChessAgent(config)
    ChessState()

    print("\n🎯 Running advanced game with custom analyzers...")
    # ... (game execution code similar to above)


def list_available_providers():
    """List all available LLM providers for chess."""
    print("\n📋 Available LLM Providers for Chess:")
    print("=" * 40)

    providers = get_available_chess_providers()
    recommendations = get_recommended_chess_models()

    for provider in providers:
        recommended = recommendations.get(provider, "default")
        print(f"  • {provider:<12} (recommended: {recommended})")

    print("\n💡 Usage example:")
    print(
        '  run_chess_with_custom_llms(white_provider="anthropic", black_provider="openai")'
    )


if __name__ == "__main__":
    # Example 1: List available providers
    list_available_providers()

    print("\n" + "=" * 60 + "\n")

    # Example 2: Run a simple game with different providers
    print("🎮 Example Game: Anthropic vs OpenAI")
    print("=" * 40)
    run_chess_with_custom_llms(
        white_provider="anthropic",
        black_provider="openai",
        max_moves=20,  # Quick game for demo
        enable_analysis=False,  # Faster without analysis
    )

    # Uncomment to run more examples:
    #
    # # Example 3: Same provider, different models
    # run_chess_with_custom_llms(
    #     white_provider="anthropic",
    #     white_model="claude-3-opus-20240229",
    #     black_provider="anthropic",
    #     black_model="claude-3-sonnet-20240229",
    # )
    #
    # # Example 4: Advanced configuration
    # run_advanced_chess_example()
