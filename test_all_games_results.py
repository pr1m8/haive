#!/usr/bin/env python3
"""
Test all games and save detailed outputs.
Run each game with different AI models and save results to files.
"""

import json
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List
import traceback

# Create results directory
RESULTS_DIR = Path("game_results")
RESULTS_DIR.mkdir(exist_ok=True)

def save_result(game_name: str, result: Dict[str, Any], error: str = None):
    """Save game result to JSON file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{game_name}_{timestamp}.json"
    filepath = RESULTS_DIR / filename
    
    output = {
        "game": game_name,
        "timestamp": timestamp,
        "success": error is None,
        "error": error,
        "result": result
    }
    
    with open(filepath, 'w') as f:
        json.dump(output, f, indent=2, default=str)
    
    print(f"✅ Saved {game_name} result to {filepath}")

async def test_game_sync(game_name: str, config_class, agent_class):
    """Test a game synchronously."""
    try:
        print(f"\n🎮 Testing {game_name} (sync)...")
        
        # Create config and agent
        config = config_class()
        agent = agent_class(config=config)
        
        # Get the state class and create initial state
        state_class = config.state_schema
        initial_state = state_class()
        
        print(f"   Created initial state: {type(initial_state).__name__}")
        
        # Run the game synchronously with initial state
        result = agent.run(initial_state)
        
        # Extract key info
        game_result = {
            "method": "sync",
            "final_state": str(result) if result else None,
            "winner": getattr(result, 'winner', None) if hasattr(result, 'winner') else None,
            "game_status": getattr(result, 'game_status', None) if hasattr(result, 'game_status') else None,
            "turn": getattr(result, 'turn', None) if hasattr(result, 'turn') else None,
            "move_count": len(getattr(result, 'move_history', [])) if hasattr(result, 'move_history') else 0,
        }
        
        print(f"✅ {game_name} completed successfully!")
        if game_result.get('winner'):
            print(f"   Winner: {game_result['winner']}")
        if game_result.get('game_status'):
            print(f"   Status: {game_result['game_status']}")
        if game_result.get('move_count'):
            print(f"   Moves: {game_result['move_count']}")
        
        save_result(game_name, game_result)
        return game_result
        
    except Exception as e:
        error_msg = f"Error in {game_name}: {str(e)}"
        print(f"❌ {error_msg}")
        save_result(game_name, {}, error_msg)
        return {"error": error_msg}

def test_game_config_only(game_name: str, config_class):
    """Test just creating the config for a game."""
    try:
        print(f"\n🔧 Testing {game_name} config...")
        
        config = config_class()
        
        result = {
            "method": "config_only",
            "config_created": True,
            "has_engines": hasattr(config, 'engines'),
            "engines_count": len(config.engines) if hasattr(config, 'engines') and config.engines else 0,
            "config_fields": list(config.__dict__.keys()) if hasattr(config, '__dict__') else []
        }
        
        print(f"✅ {game_name} config created successfully!")
        print(f"   Engines: {result['engines_count']}")
        
        save_result(f"{game_name}_config", result)
        return result
        
    except Exception as e:
        error_msg = f"Config error in {game_name}: {str(e)}"
        print(f"❌ {error_msg}")
        save_result(f"{game_name}_config", {}, error_msg)
        return {"error": error_msg}

def main():
    """Run all game tests."""
    print("🚀 Starting comprehensive game testing...")
    print(f"Results will be saved to: {RESULTS_DIR.absolute()}")
    
    # Import games and test configs first
    games_to_test = [
        ("tic_tac_toe", "haive.games.tic_tac_toe.config", "TicTacToeConfig", "haive.games.tic_tac_toe.agent", "TicTacToeAgent"),
        ("chess", "haive.games.chess.config", "ChessConfig", "haive.games.chess.agent", "ChessAgent"),
        ("mancala", "haive.games.mancala.config", "MancalaConfig", "haive.games.mancala.agent", "MancalaAgent"),
        ("nim", "haive.games.nim.config", "NimConfig", "haive.games.nim.agent", "NimAgent"),
        ("mastermind", "haive.games.mastermind.config", "MastermindConfig", "haive.games.mastermind.agent", "MastermindAgent"),
        ("connect4", "haive.games.connect4.config", "Connect4AgentConfig", "haive.games.connect4.agent", "Connect4Agent"),
        ("reversi", "haive.games.reversi.config", "ReversiConfig", "haive.games.reversi.agent", "ReversiAgent"),
    ]
    
    successful_configs = []
    failed_configs = []
    
    # Test configs first
    print("\n" + "="*50)
    print("PHASE 1: Testing Config Creation")
    print("="*50)
    
    for game_name, config_module, config_class_name, agent_module, agent_class_name in games_to_test:
        try:
            # Import config
            import importlib
            config_mod = importlib.import_module(config_module)
            config_class = getattr(config_mod, config_class_name)
            
            result = test_game_config_only(game_name, config_class)
            if "error" not in result:
                successful_configs.append((game_name, config_class, agent_module, agent_class_name))
            else:
                failed_configs.append((game_name, result["error"]))
                
        except Exception as e:
            error_msg = f"Import error for {game_name}: {str(e)}"
            print(f"❌ {error_msg}")
            failed_configs.append((game_name, error_msg))
    
    # Test actual game runs for successful configs
    print("\n" + "="*50)
    print("PHASE 2: Testing Game Execution")
    print("="*50)
    
    successful_games = []
    failed_games = []
    
    for game_name, config_class, agent_module, agent_class_name in successful_configs:
        try:
            # Import agent
            import importlib
            agent_mod = importlib.import_module(agent_module)
            agent_class = getattr(agent_mod, agent_class_name)
            
            # Test sync run
            result = asyncio.run(test_game_sync(game_name, config_class, agent_class))
            if "error" not in result:
                successful_games.append(game_name)
            else:
                failed_games.append((game_name, result["error"]))
                
        except Exception as e:
            error_msg = f"Execution error for {game_name}: {str(e)}"
            print(f"❌ {error_msg}")
            traceback.print_exc()
            failed_games.append((game_name, error_msg))
    
    # Summary
    print("\n" + "="*50)
    print("FINAL SUMMARY")
    print("="*50)
    
    print(f"\n✅ Successful config creation: {len(successful_configs)}")
    for game_name, _, _, _ in successful_configs:
        print(f"   - {game_name}")
    
    print(f"\n❌ Failed config creation: {len(failed_configs)}")
    for game_name, error in failed_configs:
        print(f"   - {game_name}: {error}")
    
    print(f"\n🎮 Successful game execution: {len(successful_games)}")
    for game_name in successful_games:
        print(f"   - {game_name}")
    
    print(f"\n💥 Failed game execution: {len(failed_games)}")
    for game_name, error in failed_games:
        print(f"   - {game_name}: {error}")
    
    print(f"\n📁 All results saved to: {RESULTS_DIR.absolute()}")
    print(f"   Total files: {len(list(RESULTS_DIR.glob('*.json')))}")

if __name__ == "__main__":
    main()