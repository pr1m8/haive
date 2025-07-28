"""Example of using configurable chess players.

This example demonstrates how to create chess games with different LLM
configurations for players without hardcoding them.
"""

import asyncio

from haive.games.chess.agent import ChessAgent
from haive.games.chess.configurable_config import (
    ConfigurableChessConfig,
    create_chess_config,
    create_chess_config_from_example,
    create_chess_config_from_player_configs,
)
from haive.games.core.agent.player_agent import (
    create_player_config,
)


def example_1_simple_models():
    """Example 1: Simple model strings."""
    print("=== Example 1: Simple Model Strings ===")

    # Create a chess game with different models for each player
    config = create_chess_config(
        white_model="gpt-4o", black_model="claude-3-5-sonnet-20240620", temperature=0.7
    )

    print(f"White Player: {config.white_player_name}")
    print(f"Black Player: {config.black_player_name}")
    print(f"Engines: {list(config.engines.keys())}")

    return config


def example_2_canonical_strings():
    """Example 2: Canonical model strings with providers."""
    print("\n=== Example 2: Canonical Model Strings ===")

    config = create_chess_config(
        white_model="anthropic:claude-3-opus-20240229",
        black_model="openai:gpt-4-turbo",
        temperature=0.8,
    )

    print(f"White Player: {config.white_player_name}")
    print(f"Black Player: {config.black_player_name}")

    return config


def example_3_example_configs():
    """Example 3: Using predefined example configurations."""
    print("\n=== Example 3: Example Configurations ===")

    # Available: anthropic_vs_openai, gpt4_only, claude_only, mixed_providers, budget_friendly
    config = create_chess_config_from_example("mixed_providers")

    print(f"White Player: {config.white_player_name}")
    print(f"Black Player: {config.black_player_name}")
    print("Engine providers:")
    for role, engine in config.engines.items():
        provider = getattr(engine.llm_config, "provider", "unknown")
        model = getattr(engine.llm_config, "model", "unknown")
        print(f"  {role}: {provider} - {model}")

    return config


def example_4_custom_player_configs():
    """Example 4: Custom player agent configurations."""
    print("\n=== Example 4: Custom Player Configurations ===")

    # Create custom player configurations with names
    player_configs = {
        "white_player": create_player_config(
            "gpt-4o", temperature=0.6, player_name="Deep Blue 2024"
        ),
        "black_player": create_player_config(
            "claude-3-5-sonnet-20240620",
            temperature=0.8,
            player_name="AlphaZero Claude",
        ),
        "white_analyzer": create_player_config(
            "gemini-1.5-pro", temperature=0.3, player_name="Gemini Analyst"
        ),
        "black_analyzer": create_player_config(
            "groq:llama-3.1-70b-versatile", temperature=0.3, player_name="Llama Analyst"
        ),
    }

    config = create_chess_config_from_player_configs(player_configs)

    print(f"White Player: {config.white_player_name}")
    print(f"Black Player: {config.black_player_name}")

    return config


def example_5_budget_friendly():
    """Example 5: Budget-friendly configuration."""
    print("\n=== Example 5: Budget-Friendly Configuration ===")

    config = create_chess_config_from_example("budget_friendly")

    print(f"White Player: {config.white_player_name}")
    print(f"Black Player: {config.black_player_name}")
    print("Using cost-effective models:")
    for role, engine in config.engines.items():
        provider = getattr(engine.llm_config, "provider", "unknown")
        model = getattr(engine.llm_config, "model", "unknown")
        print(f"  {role}: {provider} - {model}")

    return config


def example_6_same_model():
    """Example 6: Using the same model for all roles."""
    print("\n=== Example 6: Same Model for All Roles ===")

    config = create_chess_config_from_example("claude_only")

    print(f"White Player: {config.white_player_name}")
    print(f"Black Player: {config.black_player_name}")
    print("All roles using Claude:")
    for role, engine in config.engines.items():
        model = getattr(engine.llm_config, "model", "unknown")
        print(f"  {role}: {model}")

    return config


async def run_short_game(config: ConfigurableChessConfig, max_moves: int = 10):
    """Run a short chess game to test the configuration."""
    print(f"\n🎮 Running short game ({max_moves} moves max)...")

    # Limit moves for quick testing
    config.max_moves = max_moves
    config.should_visualize_graph = (
        False  # Disable graph visualization for cleaner output
    )

    try:
        agent = ChessAgent(config)

        # Run the game
        result = agent.run({})

        if result:
            print("✅ Game completed successfully!")
            print(f"Game status: {result.get('game_status', 'unknown')}")
            print(f"Total moves: {len(result.get('move_history', []))}")

            # Show last few moves
            move_history = result.get("move_history", [])
            if move_history:
                print("Last few moves:")
                for i, (player, move) in enumerate(move_history[-5:], 1):
                    print(f"  {len(move_history) - 5 + i}. {player}: {move}")
        else:
            print("❌ Game failed to complete")

    except Exception as e:
        print(f"❌ Error running game: {e}")


def main():
    """Run all examples."""
    print("Configurable Chess Players Examples")
    print("=" * 50)

    # Run configuration examples
    configs = [
        example_1_simple_models(),
        example_2_canonical_strings(),
        example_3_example_configs(),
        example_4_custom_player_configs(),
        example_5_budget_friendly(),
        example_6_same_model(),
    ]

    # Pick one config to run a short game
    print("\n" + "=" * 50)
    print("Testing with Example 1 configuration...")

    # Run async game
    asyncio.run(run_short_game(configs[0], max_moves=6))


if __name__ == "__main__":
    main()
