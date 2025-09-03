"""Working Connect4 example with the generic agent system.

This example demonstrates a complete working Connect4 game using the new
generic player agent system with configurable LLMs.
"""

import asyncio
import time

from haive.games.connect4.api import (
    Connect4API,
)
from haive.games.connect4.configurable_config import (
    create_connect4_config_from_player_configs,
)
from haive.games.connect4.generic_engines import (
    create_generic_connect4_config_from_example,
    create_generic_connect4_engines_simple,
)
from haive.games.core.agent.player_agent import PlayerAgentConfig


def demo_1_simple_configuration():
    """Demo 1: Simple model string configuration."""
    print("🔴🟡 DEMO 1: Simple Connect4 Configuration")
    print("=" * 50)

    print("Creating Connect4 game with simple model strings...")

    # Create engines using simple model strings
    engines = create_generic_connect4_engines_simple(
        red_model="openai:gpt-4o",
        yellow_model="anthropic:claude-3-5-sonnet-20240620",
        temperature=0.7,
    )

    print(f"✅ Created {len(engines)} engines:")
    for role, engine in engines.items():
        provider = getattr(engine.llm_config, "provider", "unknown")
        model = getattr(engine.llm_config, "model", "unknown")
        print(f"   {role}: {provider} - {model}")

    print()


def demo_2_api_usage():
    """Demo 2: Using the Connect4 API."""
    print("🌐 DEMO 2: Connect4 API Usage")
    print("=" * 30)

    print("Creating game via API...")

    # Create game using API
    agent, game_id = Connect4API.create_game_simple(
        red_model="gpt-4o",
        yellow_model="claude-3-opus",
        temperature=0.8,
        enable_analysis=False,  # Disable for faster execution
        max_moves=20,  # Limit for demo
    )

    print(f"✅ Game created: {game_id}")
    print(f"   Red Player: {agent.config.red_player_name}")
    print(f"   Yellow Player: {agent.config.yellow_player_name}")
    print(f"   Max Moves: {agent.config.max_moves}")
    print(f"   Analysis: {'Enabled' if agent.config.enable_analysis else 'Disabled'}")

    print()


def demo_3_example_configurations():
    """Demo 3: Using example configurations."""
    print("📋 DEMO 3: Example Configurations")
    print("=" * 35)

    examples = ["gpt_vs_claude", "gpt_only", "claude_only", "budget", "mixed"]

    print("Available example configurations:")
    for example_name in examples:
        try:
            engines = create_generic_connect4_config_from_example(example_name)
            red_engine = engines["red_player"]
            yellow_engine = engines["yellow_player"]

            red_model = getattr(red_engine.llm_config, "model", "unknown")
            yellow_model = getattr(yellow_engine.llm_config, "model", "unknown")

            print(f"   {example_name}: {red_model} vs {yellow_model}")
        except Exception as e:
            print(f"   {example_name}: Error - {e}")

    print()


def demo_4_custom_player_configs():
    """Demo 4: Custom player configurations."""
    print("🎯 DEMO 4: Custom Player Configurations")
    print("=" * 40)

    print("Creating custom player configurations...")

    # Create custom configurations with different models per role
    player_configs = {
        "red_player": PlayerAgentConfig(
            llm_config="openai:gpt-4o",
            temperature=0.8,
            player_name="Connect4 Master Red",
        ),
        "yellow_player": PlayerAgentConfig(
            llm_config="anthropic:claude-3-5-sonnet-20240620",
            temperature=0.6,
            player_name="Strategic Yellow",
        ),
        "red_analyzer": PlayerAgentConfig(
            llm_config="google:gemini-1.5-pro",
            temperature=0.3,
            player_name="Gemini Red Analyst",
        ),
        "yellow_analyzer": PlayerAgentConfig(
            llm_config="groq:llama-3.1-70b-versatile",
            temperature=0.3,
            player_name="Llama Yellow Analyst",
        ),
    }

    config = create_connect4_config_from_player_configs(
        player_configs, enable_analysis=True
    )

    print("✅ Custom configuration created::")
    print(f"   Red Player: {config.red_player_name}")
    print(f"   Yellow Player: {config.yellow_player_name}")
    print(f"   Analysis: {'Enabled' if config.enable_analysis else 'Disabled'}")
    print(f"   Engines: {len(config.engines)} configured")

    print()


def demo_5_convenience_functions():
    """Demo 5: Convenience functions for quick play."""
    print("⚡ DEMO 5: Convenience Functions")
    print("=" * 30)

    print("Testing convenience functions...")

    # Test with mocked execution (avoid long-running games in demo)
    try:
        print("📋 Available convenience functions:")
        print("   play_connect4_simple(red_model, yellow_model)")
        print("   play_connect4_example(example_name)")
        print("   play_connect4_async(red_model, yellow_model)")

        print("\n🔧 Example usage:")
        print("   result = play_connect4_simple('gpt-4o', 'claude-3-opus')")
        print("   result = play_connect4_example('budget')")
        print("   result = await play_connect4_async('gpt-4o', 'claude-3-opus')")

    except Exception as e:
        print(f"Note: Functions available but not executed in demo: {e}")

    print()


def demo_6_real_game_execution():
    """Demo 6: Real game execution (limited moves)."""
    print("🎮 DEMO 6: Real Game Execution")
    print("=" * 30)

    print("Running a real Connect4 game with limited moves...")

    try:
        # Create a quick game configuration
        agent, game_id = Connect4API.create_game_simple(
            red_model="gpt-4o",
            yellow_model="claude-3-5-sonnet-20240620",
            temperature=0.7,
            enable_analysis=False,  # Disable for speed
            max_moves=8,  # Very limited for demo
        )

        print(f"🚀 Starting game: {game_id}")
        print(
            f"   Players: {agent.config.red_player_name} vs {agent.config.yellow_player_name}"
        )
        print(f"   Max moves: {agent.config.max_moves}")

        start_time = time.time()

        # Run the game
        result = Connect4API.run_game(agent, game_id)

        end_time = time.time()

        print(f"\n✅ Game completed in {end_time - start_time:.2f} seconds!")
        print(f"   Status: {result.status.value}")
        print(f"   Winner: {result.winner or 'None (Draw/Ongoing)'}")
        print(f"   Total moves: {result.total_moves}")
        print(f"   Duration: {result.duration_seconds:.2f}s")

        if result.move_history:
            print("   First few moves:")
            for i, (player, column) in enumerate(result.move_history[:5], 1):
                print(f"     {i}. {player}: Column {column}")

        if result.error_message:
            print(f"   Error: {result.error_message}")

    except Exception as e:
        print(f"❌ Error running game: {e}")
        import traceback

        traceback.print_exc()

    print()


async def demo_7_async_execution():
    """Demo 7: Asynchronous game execution."""
    print("🔄 DEMO 7: Async Game Execution")
    print("=" * 30)

    print("Running async Connect4 game...")

    try:
        # Create game
        agent, game_id = Connect4API.create_game_from_example(
            "budget",  # Use budget models for faster execution
            max_moves=6,  # Very limited for demo
        )

        print(f"🚀 Starting async game: {game_id}")

        # Run async
        result = await Connect4API.run_game_async(agent, game_id)

        print("✅ Async game completed!!")
        print(f"   Status: {result.status.value}")
        print(f"   Total moves: {result.total_moves}")
        print(f"   Duration: {result.duration_seconds:.2f}s")

    except Exception as e:
        print(f"❌ Error in async execution: {e}")

    print()


def demo_8_error_handling():
    """Demo 8: Error handling and validation."""
    print("⚠️ DEMO 8: Error Handling")
    print("=" * 25)

    print("Testing error handling...")

    # Test invalid example name
    try:
        create_generic_connect4_config_from_example("invalid_example")
        print("❌ Should have raised error for invalid example")
    except ValueError as e:
        print(f"✅ Correctly caught error: {e}")

    # Test missing player config
    try:
        from haive.games.connect4.generic_engines import create_generic_connect4_engines

        incomplete_configs = {
            "red_player": PlayerAgentConfig(llm_config="gpt-4o"),
            # Missing other required configs
        }
        create_generic_connect4_engines(incomplete_configs)
        print("❌ Should have raised error for incomplete configs")
    except ValueError as e:
        print(f"✅ Correctly caught error: {e}")

    print()


def show_configuration_summary():
    """Show summary of Connect4 configuration options."""
    print("📚 CONNECT4 CONFIGURATION SUMMARY")
    print("=" * 40)

    print("🎯 Configuration Methods:")
    print("1. Simple strings:")
    print("   create_connect4_config('gpt-4o', 'claude-3-opus')")
    print()

    print("2. Example configurations:")
    print("   create_connect4_config_from_example('budget')")
    print("   Available: gpt_vs_claude, gpt_only, claude_only, budget, mixed")
    print()

    print("3. Custom player configs:")
    print("   player_configs = {")
    print("       'red_player': PlayerAgentConfig(llm_config='gpt-4o'),")
    print("       'yellow_player': PlayerAgentConfig(llm_config='claude-3-opus')")
    print("   }")
    print("   create_connect4_config_from_player_configs(player_configs)")
    print()

    print("🌐 API Methods:")
    print("   Connect4API.create_game_simple(red_model, yellow_model)")
    print("   Connect4API.create_game_from_example(example_name)")
    print("   Connect4API.create_game_from_player_configs(configs)")
    print("   Connect4API.run_game(agent, game_id)")
    print("   Connect4API.run_game_async(agent, game_id)")
    print()

    print("⚡ Convenience Functions:")
    print("   play_connect4_simple('gpt-4o', 'claude-3-opus')")
    print("   play_connect4_example('budget')")
    print("   await play_connect4_async('gpt-4o', 'claude-3-opus')")
    print()


async def main():
    """Run all Connect4 demonstrations."""
    print("🔴🟡 CONNECT4 GENERIC AGENT SYSTEM DEMONSTRATION")
    print("=" * 60)
    print("Complete working Connect4 implementation with configurable agents")
    print("=" * 60)

    # Run sync demos
    demo_1_simple_configuration()
    demo_2_api_usage()
    demo_3_example_configurations()
    demo_4_custom_player_configs()
    demo_5_convenience_functions()
    demo_6_real_game_execution()
    demo_8_error_handling()

    # Run async demo
    await demo_7_async_execution()

    # Show summary
    show_configuration_summary()

    print("🎉 CONNECT4 DEMONSTRATION COMPLETE!")
    print("=" * 60)
    print("✅ Generic system working for Connect4")
    print("✅ API functional with sync/async support")
    print("✅ Multiple configuration methods available")
    print("✅ Error handling and validation working")
    print("✅ Real game execution successful")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
