"""Comprehensive demonstration of the generic player agent system.

This demo shows how the generic system solves the configurable agents problem
across ALL games using Python generics for full type safety and reusability.

KEY BENEFITS:
✅ Type-safe player identifiers (compile-time checking)
✅ Generic pattern works across all two-player games
✅ No hardcoded LLM configurations anywhere
✅ Easy LLM swapping per role
✅ Consistent API across all games
✅ Full integration with LLM factory system
"""

import time

# Import for actual game execution
from haive.games.chess.agent import ChessAgent
from haive.games.chess.configurable_config import ConfigurableChessConfig

# Import game-specific implementations
from haive.games.chess.generic_engines import (
    create_generic_chess_config_from_example,
    create_generic_chess_engines_simple,
)

# Import the generic system
from haive.games.core.agent.generic_player_agent import (
    CheckersPlayerIdentifiers,
    ChessPlayerIdentifiers,
    Connect4PlayerIdentifiers,
    TicTacToePlayerIdentifiers,
)
from haive.games.tic_tac_toe.generic_engines import (
    create_generic_ttt_config_from_example,
    create_generic_ttt_engines_simple,
)


def demonstrate_type_safety():
    """Demonstrate compile-time type safety with the generic system."""
    print("🔒 TYPE SAFETY DEMONSTRATION")
    print("=" * 40)

    print("✅ Type-safe player identifiers prevent configuration errors:")
    print()

    # Correct type-safe configurations
    chess_players = ChessPlayerIdentifiers()  # player1="white", player2="black"
    ttt_players = TicTacToePlayerIdentifiers()  # player1="X", player2="O"
    checkers_players = CheckersPlayerIdentifiers()  # player1="red", player2="black"
    connect4_players = Connect4PlayerIdentifiers()  # player1="red", player2="yellow"

    print("🎯 Valid player configurations:")
    print(f"   Chess: {chess_players.player1} vs {chess_players.player2}")
    print(f"   Tic Tac Toe: {ttt_players.player1} vs {ttt_players.player2}")
    print(f"   Checkers: {checkers_players.player1} vs {checkers_players.player2}")
    print(f"   Connect4: {connect4_players.player1} vs {connect4_players.player2}")

    print()
    print("❌ These would cause type errors at development time:")
    print(
        "   ChessPlayerIdentifiers(player1='red', player2='yellow')  # Wrong for chess!"
    )
    print(
        "   TicTacToePlayerIdentifiers(player1='white', player2='black')  # Wrong for TTT!"
    )

    print()
    print("🚀 Benefits:")
    print("   ✅ Catch configuration errors before runtime")
    print("   ✅ IDE autocomplete and type hints")
    print("   ✅ Self-documenting code")
    print("   ✅ Consistent naming across games")


def demonstrate_cross_game_compatibility():
    """Demonstrate how the same pattern works across all games."""
    print("\n🎮 CROSS-GAME COMPATIBILITY")
    print("=" * 35)

    # Same configuration approach for all games
    model1 = "openai:gpt-4o"
    model2 = "anthropic:claude-3-5-sonnet-20240620"

    print(f"🔧 Using consistent models: {model1} vs {model2}")
    print()

    # Create engines for different games using the SAME API
    games_configs = {
        "Chess": create_generic_chess_engines_simple(model1, model2),
        "Tic Tac Toe": create_generic_ttt_engines_simple(model1, model2),
    }

    for game_name, engines in games_configs.items():
        print(f"🎯 {game_name} roles:")
        for role in sorted(engines.keys()):
            engine = engines[role]
            provider = getattr(engine.llm_config, "provider", "unknown")
            model = getattr(engine.llm_config, "model", "unknown")
            print(f"   {role}: {provider} - {model}")
        print()

    print("✨ Same Generic Pattern for ALL Games:")
    print("   create_generic_{game}_engines_simple(model1, model2)")
    print(
        "   → {player1}_player, {player2}_player, {player1}_analyzer, {player2}_analyzer"
    )


def demonstrate_no_hardcoded_llms():
    """Demonstrate elimination of hardcoded LLM configurations."""
    print("🚫 NO MORE HARDCODED LLMs")
    print("=" * 30)

    print("❌ BEFORE (hardcoded in engines.py files):")
    print("   AzureLLMConfig(model='gpt-4o')")
    print("   AnthropicLLMConfig(model='claude-3-5-sonnet-20240620')")
    print("   → Hard to change, not configurable")
    print()

    print("✅ AFTER (fully configurable with generics):")

    # Show different configuration methods
    configs = [
        ("Simple strings", "gpt-4", "claude-3-opus"),
        ("Canonical format", "openai:gpt-4o", "anthropic:claude-3-5-sonnet-20240620"),
        ("Mixed providers", "google:gemini-1.5-pro", "groq:llama-3.1-70b-versatile"),
    ]

    for desc, model1, model2 in configs:
        print(f"   {desc}: {model1} vs {model2}")
        engines = create_generic_chess_engines_simple(model1, model2)
        white_engine = engines["white_player"]
        black_engine = engines["black_player"]
        print(
            f"      → White: {getattr(white_engine.llm_config, 'provider', 'unknown')}"
        )
        print(
            f"      → Black: {getattr(black_engine.llm_config, 'provider', 'unknown')}"
        )
        print()


def demonstrate_easy_llm_swapping():
    """Demonstrate how easy it is to swap LLMs per role."""
    print("🔄 EASY LLM SWAPPING PER ROLE")
    print("=" * 35)

    print("🎯 Different models for different roles:")

    # Example: Use fast models for players, smart models for analyzers
    from haive.games.chess.generic_engines import create_generic_chess_engines
    from haive.games.core.agent.player_agent import PlayerAgentConfig

    role_specific_configs = {
        "white_player": PlayerAgentConfig(
            llm_config="groq:llama-3.1-8b-instant",  # Fast for real-time play
            temperature=0.7,
            player_name="Speed White",
        ),
        "black_player": PlayerAgentConfig(
            llm_config="groq:llama-3.1-8b-instant",  # Fast for real-time play
            temperature=0.7,
            player_name="Speed Black",
        ),
        "white_analyzer": PlayerAgentConfig(
            llm_config="openai:gpt-4o",  # Smart for deep analysis
            temperature=0.3,
            player_name="Deep White Analyzer",
        ),
        "black_analyzer": PlayerAgentConfig(
            llm_config="anthropic:claude-3-5-sonnet-20240620",  # Smart for deep analysis
            temperature=0.3,
            player_name="Deep Black Analyzer",
        ),
    }

    engines = create_generic_chess_engines(role_specific_configs)

    print("⚡ Fast models for real-time play:")
    for role in ["white_player", "black_player"]:
        engine = engines[role]
        model = getattr(engine.llm_config, "model", "unknown")
        print(f"   {role}: {model}")

    print("\n🧠 Smart models for deep analysis:")
    for role in ["white_analyzer", "black_analyzer"]:
        engine = engines[role]
        model = getattr(engine.llm_config, "model", "unknown")
        print(f"   {role}: {model}")

    print("\n✨ Benefits:")
    print("   ✅ Optimize cost vs performance per role")
    print("   ✅ Use fast models for real-time decisions")
    print("   ✅ Use smart models for complex analysis")
    print("   ✅ Easy to experiment with different combinations")


def demonstrate_api_integration():
    """Demonstrate API-friendly configuration."""
    print("\n🌐 API-FRIENDLY CONFIGURATION")
    print("=" * 35)

    print("🔧 Easy to expose in APIs:")
    print()

    # Simulate API endpoints
    def create_chess_game_api(
        white_model: str, black_model: str, temperature: float = 0.7
    ):
        """Simulated API endpoint for creating chess games."""
        engines = create_generic_chess_engines_simple(
            white_model, black_model, temperature
        )
        return {
            "game_id": "chess_123",
            "white_model": white_model,
            "black_model": black_model,
            "engines_created": len(engines),
            "roles": list(engines.keys()),
        }

    def create_ttt_game_api(x_model: str, o_model: str, temperature: float = 0.3):
        """Simulated API endpoint for creating tic-tac-toe games."""
        engines = create_generic_ttt_engines_simple(x_model, o_model, temperature)
        return {
            "game_id": "ttt_456",
            "x_model": x_model,
            "o_model": o_model,
            "engines_created": len(engines),
            "roles": list(engines.keys()),
        }

    # Example API calls
    api_calls = [
        ("Chess Game", create_chess_game_api("gpt-4", "claude-3-opus")),
        ("TTT Game", create_ttt_game_api("gpt-3.5-turbo", "llama-3.1-8b-instant")),
    ]

    for call_name, result in api_calls:
        print(f"📡 {call_name} API Response:")
        for key, value in result.items():
            print(f"   {key}: {value}")
        print()

    print("✅ API Benefits:")
    print("   ✅ Simple model string parameters")
    print("   ✅ Consistent API across all games")
    print("   ✅ Easy for frontend integration")
    print("   ✅ No backend code changes needed")


def demonstrate_example_configurations():
    """Demonstrate predefined example configurations."""
    print("📋 EXAMPLE CONFIGURATIONS")
    print("=" * 30)

    print("🎯 Predefined examples for quick setup:")
    print()

    # Chess examples
    chess_examples = [
        "anthropic_vs_openai",
        "gpt4_only",
        "claude_only",
        "budget_friendly",
    ]

    print("♟️  Chess Examples:")
    for example in chess_examples:
        try:
            engines = create_generic_chess_config_from_example(example)
            white_model = getattr(
                engines["white_player"].llm_config, "model", "unknown"
            )
            black_model = getattr(
                engines["black_player"].llm_config, "model", "unknown"
            )
            print(f"   {example}: {white_model} vs {black_model}")
        except Exception as e:
            print(f"   {example}: Error - {e}")

    print()

    # Tic Tac Toe examples
    ttt_examples = ["gpt_vs_claude", "gpt_only", "claude_only", "budget"]

    print("⭕ Tic Tac Toe Examples:")
    for example in ttt_examples:
        try:
            engines = create_generic_ttt_config_from_example(example)
            x_model = getattr(engines["X_player"].llm_config, "model", "unknown")
            o_model = getattr(engines["O_player"].llm_config, "model", "unknown")
            print(f"   {example}: {x_model} vs {o_model}")
        except Exception as e:
            print(f"   {example}: Error - {e}")

    print()
    print("🚀 Usage:")
    print("   engines = create_generic_chess_config_from_example('budget_friendly')")
    print("   engines = create_generic_ttt_config_from_example('gpt_vs_claude')")


def demonstrate_real_game_execution():
    """Demonstrate real game execution with the generic system."""
    print("\n🎮 REAL GAME EXECUTION")
    print("=" * 25)

    print("🏁 Creating and running a chess game with generic engines...")

    try:
        # Create engines using the generic system
        engines = create_generic_chess_engines_simple(
            "openai:gpt-4o", "anthropic:claude-3-5-sonnet-20240620", temperature=0.7
        )

        # Create a chess config using the engines
        config = ConfigurableChessConfig(
            engines=engines,
            max_moves=8,  # Limit for demo
            enable_analysis=False,  # Disable for speed
            should_visualize_graph=False,
        )

        print(f"✅ Engines created: {len(engines)} roles")
        print(f"🎯 White: {config.white_player_name}")
        print(f"🎯 Black: {config.black_player_name}")
        print()

        # Run the game
        print("🚀 Starting game...")
        start_time = time.time()

        agent = ChessAgent(config)
        result = agent.run({})

        end_time = time.time()
        duration = end_time - start_time

        if result:
            print(f"✅ Game completed in {duration:.2f} seconds!")
            print(f"📊 Status: {result.get('game_status', 'unknown')}")
            print(f"🔢 Moves: {len(result.get('move_history', []))}")

            # Show some moves
            move_history = result.get("move_history", [])
            if move_history:
                print("\n📝 Move History:")
                for i, (player, move) in enumerate(move_history[:6], 1):
                    print(f"   {i}. {player}: {move}")
        else:
            print("❌ Game failed to complete")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        traceback.print_exc()


def demonstrate_generic_benefits():
    """Summarize all benefits of the generic system."""
    print("\n🎉 GENERIC SYSTEM BENEFITS SUMMARY")
    print("=" * 45)

    benefits = [
        ("🔒 Type Safety", "Compile-time checking prevents configuration errors"),
        (
            "🎮 Cross-Game",
            "Same pattern works for chess, checkers, tic-tac-toe, connect4, etc.",
        ),
        ("🚫 No Hardcoding", "Zero hardcoded LLM configurations anywhere"),
        ("🔄 Easy Swapping", "Change models with simple string parameters"),
        ("⚡ Role-Specific", "Different models for players vs analyzers"),
        ("🌐 API-Friendly", "Perfect for web APIs and microservices"),
        ("📋 Examples", "Predefined configurations for common use cases"),
        ("🧩 Extensible", "Easy to add new games following the pattern"),
        ("🔗 LLM Factory", "Full integration with the new LLM factory system"),
        ("📝 Self-Documenting", "Clear, readable configuration code"),
    ]

    for emoji_title, description in benefits:
        print(f"{emoji_title}: {description}")

    print()
    print("🚀 PROBLEM SOLVED: Player agents as config inputs!")
    print("🚀 PROBLEM SOLVED: Easy LLM configuration changes!")
    print("🚀 PROBLEM SOLVED: No hardcoded engines!")
    print("🚀 PROBLEM SOLVED: Type-safe, generic, extensible!")


def main():
    """Run the comprehensive generic agents demonstration."""
    print("🎯 GENERIC PLAYER AGENT SYSTEM DEMONSTRATION")
    print("=" * 60)
    print("Solving the configurable agents problem with Python generics")
    print("=" * 60)

    demonstrate_type_safety()
    demonstrate_cross_game_compatibility()
    demonstrate_no_hardcoded_llms()
    demonstrate_easy_llm_swapping()
    demonstrate_api_integration()
    demonstrate_example_configurations()
    demonstrate_real_game_execution()
    demonstrate_generic_benefits()

    print("\n" + "=" * 60)
    print("🎉 GENERIC SOLUTION COMPLETE!")
    print("✅ Type-safe player agents as config inputs")
    print("✅ Works across ALL two-player games")
    print("✅ Zero hardcoded LLM configurations")
    print("✅ Production-ready and extensible")
    print("=" * 60)


if __name__ == "__main__":
    main()
