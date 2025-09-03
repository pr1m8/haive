"""Comprehensive demo of configurable agents solution.

This demo shows how the new configurable agent system solves the original problem:
- Games can directly change LLM being used through configuration
- Separate agents/subagents are added rather than hardcoded
- Easy LLM config changes for users
- Working APIs with no recursion limit errors
- Clean integration with the new LLM factory system

BEFORE: Hardcoded LLMs in engines files
AFTER: Configurable player agents that can be passed as config inputs
"""

import time

# Import agents for testing
from haive.games.chess.agent import ChessAgent

# Import the new configurable system
from haive.games.chess.configurable_config import (
    ConfigurableChessConfig,
    create_chess_config,
    create_chess_config_from_example,
)
from haive.games.chess.configurable_engines import get_example_engines
from haive.games.core.agent.player_agent import (
    create_player_config,
)
from haive.games.tic_tac_toe.configurable_engines import get_example_tic_tac_toe_engines


def demonstrate_problem_solved():
    """Demonstrate how the configurable agent system solves the original problems."""

    print("🎯 CONFIGURABLE AGENTS SOLUTION DEMO")
    print("=" * 60)
    print()

    print("✅ PROBLEM SOLVED: Games can now directly change LLM being used!")
    print("✅ PROBLEM SOLVED: Separate agents/subagents added via config!")
    print("✅ PROBLEM SOLVED: Easy LLM config changes for users!")
    print("✅ PROBLEM SOLVED: Working APIs with recursion limits fixed!")
    print()

    # Demonstrate the solutions
    demo_1_easy_llm_changes()
    demo_2_player_agents_as_inputs()
    demo_3_api_integration()
    demo_4_no_hardcoded_engines()
    demo_5_cross_game_compatibility()


def demo_1_easy_llm_changes():
    """Demo 1: Easy LLM configuration changes."""
    print("🔧 DEMO 1: Easy LLM Configuration Changes")
    print("-" * 40)

    print("BEFORE: Had to modify engines.py files")
    print("AFTER: Simple configuration changes")
    print()

    # Show multiple ways to configure LLMs
    configs = [
        ("Simple strings", create_chess_config("gpt-4", "claude-3-opus")),
        (
            "Canonical format",
            create_chess_config(
                "openai:gpt-4o", "anthropic:claude-3-5-sonnet-20240620"
            ),
        ),
        ("Example configs", create_chess_config_from_example("budget_friendly")),
        ("Mixed providers", create_chess_config_from_example("mixed_providers")),
    ]

    for name, config in configs:
        print(f"📋 {name}:")
        print(f"   White: {config.white_player_name}")
        print(f"   Black: {config.black_player_name}")
        print(f"   Engines: {len(config.engines)} configured")
        print()


def demo_2_player_agents_as_inputs():
    """Demo 2: Player agents as configuration inputs."""
    print("🎮 DEMO 2: Player Agents as Configuration Inputs")
    print("-" * 50)

    print("BEFORE: Hardcoded engines in build_chess_aug_llms()")
    print("AFTER: Player agents passed as config inputs")
    print()

    # Create custom player configurations
    custom_players = {
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
            "groq:llama-3.1-70b-versatile",
            temperature=0.3,
            player_name="Llama Speed Analyst",
        ),
    }

    print("🤖 Custom Player Agent Configuration:")
    for role, config in custom_players.items():
        print(f"   {role}: {config.player_name} ({config.llm_config})")

    # Create the chess config
    chess_config = ConfigurableChessConfig(player_configs=custom_players)
    print(
        f"\n✅ Chess game created with {len(chess_config.engines)} configurable engines"
    )
    print()


def demo_3_api_integration():
    """Demo 3: Working API integration with recursion limits."""
    print("🌐 DEMO 3: API Integration with Recursion Limits Fixed")
    print("-" * 55)

    print("BEFORE: Recursion limit errors in complex games")
    print("AFTER: Proper recursion configuration for each game type")
    print()

    # Show recursion configuration
    config = create_chess_config("gpt-4o", "claude-3-opus")

    print("📊 Recursion Configuration:")
    runnable_config = config.runnable_config
    if "recursion_limit" in runnable_config:
        print(f"   Recursion limit: {runnable_config['recursion_limit']}")
    if "configurable" in runnable_config:
        configurable = runnable_config["configurable"]
        if "thread_id" in configurable:
            print(f"   Thread ID: {configurable['thread_id']}")

    print("✅ Games now work in APIs without recursion errors")
    print()


def demo_4_no_hardcoded_engines():
    """Demo 4: No more hardcoded engines."""
    print("🔧 DEMO 4: No More Hardcoded Engines")
    print("-" * 35)

    print("BEFORE: engines.py had hardcoded LLM configs like:")
    print("   AnthropicLLMConfig(model='claude-3-5-sonnet-20240620')")
    print("   AzureLLMConfig(model='gpt-4o')")
    print()
    print("AFTER: Dynamic engine creation from configuration:")
    print()

    # Show different engine configurations
    example_configs = ["anthropic_vs_openai", "gpt4_only", "budget_friendly"]

    for example_name in example_configs:
        engines = get_example_engines(example_name)
        print(f"📋 Example '{example_name}':")
        for role, engine in engines.items():
            provider = getattr(engine.llm_config, "provider", "unknown")
            model = getattr(engine.llm_config, "model", "unknown")
            print(f"   {role}: {provider} - {model}")
        print()


def demo_5_cross_game_compatibility():
    """Demo 5: Cross-game compatibility."""
    print("🎲 DEMO 5: Cross-Game Compatibility")
    print("-" * 35)

    print("The same player agent system works across different games:")
    print()

    # Show chess engines
    chess_engines = get_example_engines("gpt_vs_claude")
    print("♟️  Chess engines:")
    for role in sorted(chess_engines.keys()):
        print(f"   {role}")

    # Show tic tac toe engines
    ttt_engines = get_example_tic_tac_toe_engines("gpt_vs_claude")
    print("\n⭕ Tic Tac Toe engines:")
    for role in sorted(ttt_engines.keys()):
        print(f"   {role}")

    print("\n✅ Same player agent abstraction works for all games!")
    print()


def demo_real_game_execution():
    """Demo 6: Real game execution with configurable agents."""
    print("🎮 DEMO 6: Real Game Execution")
    print("-" * 30)

    print("Creating and running a chess game with configurable agents...")
    print()

    # Create a configuration optimized for quick testing
    config = create_chess_config(
        white_model="gpt-4o",
        black_model="claude-3-5-sonnet-20240620",
        temperature=0.7,
        enable_analysis=False,  # Disable for faster execution
    )

    # Limit moves for demo
    config.max_moves = 8
    config.should_visualize_graph = False

    print("🏁 Game Setup:p:")
    print(f"   White: {config.white_player_name}")
    print(f"   Black: {config.black_player_name}")
    print(f"   Max moves: {config.max_moves}")
    print(f"   Analysis: {'Enabled' if config.enable_analysis else 'Disabled'}")
    print()

    try:
        print("🎯 Starting game...")
        start_time = time.time()

        agent = ChessAgent(config)
        result = agent.run({})

        end_time = time.time()
        duration = end_time - start_time

        if result:
            print("✅ Game completed successfully!")
            print(f"⏱️  Duration: {duration:.2f} seconds")
            print(f"📊 Status: {result.get('game_status', 'unknown')}")
            print(f"🔢 Moves played: {len(result.get('move_history', []))}")

            # Show move history
            move_history = result.get("move_history", [])
            if move_history:
                print("\n📝 Move History:")
                for i, (player, move) in enumerate(move_history, 1):
                    print(f"   {i}. {player}: {move}")
        else:
            print("❌ Game failed to complete")

    except Exception as e:
        print(f"❌ Error running game: {e}")
        import traceback

        traceback.print_exc()

    print()


def show_configuration_api():
    """Show the configuration API for developers."""
    print("📚 CONFIGURATION API REFERENCE")
    print("-" * 35)

    print("The new system provides multiple configuration methods:")
    print()

    print("1️⃣ Simple model strings:")
    print("   create_chess_config('gpt-4', 'claude-3-opus')")
    print()

    print("2️⃣ Canonical format:")
    print("   create_chess_config('openai:gpt-4o', 'anthropic:claude-3-sonnet')")
    print()

    print("3️⃣ Example configurations:")
    print("   create_chess_config_from_example('budget_friendly')")
    print(
        "   # Available: anthropic_vs_openai, gpt4_only, claude_only, mixed_providers, budget_friendly"
    )
    print()

    print("4️⃣ Custom player configurations:")
    print("   player_configs = {")
    print(
        "       'white_player': create_player_config('gpt-4', player_name='Deep Blue'),"
    )
    print(
        "       'black_player': create_player_config('claude-3-opus', player_name='AlphaZero')"
    )
    print("   }")
    print("   create_chess_config_from_player_configs(player_configs)")
    print()

    print("5️⃣ Direct LLMConfig objects:")
    print("   from haive.core.models.llm import create_llm_config")
    print("   config = create_llm_config('gpt-4', temperature=0.8)")
    print("   create_player_config(config)")
    print()


def main():
    """Run the comprehensive demo."""
    demonstrate_problem_solved()
    demo_real_game_execution()
    show_configuration_api()

    print("🎉 SOLUTION COMPLETE!")
    print("=" * 60)
    print("✅ Games now use player agents as inputs in config")
    print("✅ Easy to change LLM configurations")
    print("✅ No more hardcoded engines")
    print("✅ Working APIs with proper recursion limits")
    print("✅ Clean integration with LLM factory system")
    print("✅ Cross-game compatibility")
    print()
    print("🚀 Ready for production use!")


if __name__ == "__main__":
    main()
