#!/usr/bin/env python3
"""
Claude vs OpenAI Tournament via API
Uses the existing working API system to run all games.
"""

import json
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

# Tournament results directory
TOURNAMENT_DIR = Path("claude_vs_openai_api_results")
TOURNAMENT_DIR.mkdir(exist_ok=True)

def save_api_result(game_name: str, result: Dict[str, Any]):
    """Save API tournament result."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{game_name}_api_{timestamp}.json"
    filepath = TOURNAMENT_DIR / filename
    
    output = {
        "game": game_name,
        "timestamp": timestamp,
        "api_result": result
    }
    
    with open(filepath, 'w') as f:
        json.dump(output, f, indent=2, default=str)
    
    # Extract winner info
    winner = "Unknown"
    if isinstance(result, dict):
        if 'winner' in result:
            winner = result['winner']
        elif 'final_state' in result and 'winner' in result['final_state']:
            winner = result['final_state']['winner']
        elif 'game_status' in result:
            status = result['game_status']
            if 'win' in str(status):
                winner = status
    
    print(f"🏆 {game_name}: {winner}")
    return winner

def test_general_api():
    """Test the General Games API to discover available games."""
    try:
        from fastapi import FastAPI
        from haive.dataflow.api.general_games_api import GeneralGameAPI
        
        print("🔍 Discovering games via API...")
        app = FastAPI()
        api = GeneralGameAPI(app)
        
        print(f"✅ Found {len(api.discovered_games)} games")
        
        working_games = []
        for game_name, game_info in api.discovered_games.items():
            if game_info.get('config_class'):
                working_games.append(game_name)
                print(f"   ✅ {game_name}")
            else:
                print(f"   ❌ {game_name} - no config")
        
        return working_games, api
        
    except Exception as e:
        print(f"❌ API discovery failed: {e}")
        return [], None

def run_api_game(game_name: str, api):
    """Run a game via the API system."""
    try:
        print(f"\n🎮 Running {game_name} via API...")
        
        # Try to get the game info
        if game_name not in api.discovered_games:
            print(f"❌ {game_name} not found in discovered games")
            return "Not Found"
        
        game_info = api.discovered_games[game_name]
        config_class = game_info.get('config_class')
        
        if not config_class:
            print(f"❌ {game_name} has no config class")
            return "No Config"
        
        # Create config and run
        try:
            config = config_class()
            print(f"   Config: {type(config).__name__}")
            
            # Get agent class
            agent_class = game_info.get('agent_class')
            if not agent_class:
                print(f"❌ {game_name} has no agent class")
                return "No Agent"
            
            # Create agent
            agent = agent_class(config=config)
            print(f"   Agent: {type(agent).__name__}")
            
            # Create initial state using our fixed method
            state_class = config.state_schema
            
            if game_name == "mastermind":
                initial_state = state_class.initialize(codemaker="player1")
            elif game_name == "connect4":
                initial_state = state_class.initialize()
            elif hasattr(state_class, 'initialize'):
                initial_state = state_class.initialize()
            else:
                initial_state = state_class()
            
            print(f"   State: {type(initial_state).__name__}")
            
            # Run with limited recursion
            config.runnable_config = {"configurable": {"recursion_limit": 15}}
            if hasattr(config, 'enable_analysis'):
                config.enable_analysis = False
            
            result = agent.run(initial_state)
            print(f"   Result: {type(result).__name__}")
            
            # Extract result info
            game_result = {
                "success": True,
                "winner": getattr(result, 'winner', 'Unknown'),
                "game_status": getattr(result, 'game_status', 'Unknown'),
                "moves": len(getattr(result, 'move_history', [])),
                "board": str(getattr(result, 'board', None))[:100] if hasattr(result, 'board') else None
            }
            
            return save_api_result(game_name, game_result)
            
        except Exception as e:
            error_result = {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
            
            if "recursion_limit" in str(e):
                # Game may have completed but hit limit
                if "X_win" in str(e):
                    error_result["likely_winner"] = "X/Player1"
                elif "O_win" in str(e):
                    error_result["likely_winner"] = "O/Player2"
                elif "_win" in str(e):
                    error_result["likely_winner"] = "Completed"
                error_result["status"] = "hit_recursion_limit"
            
            return save_api_result(game_name, error_result)
            
    except Exception as e:
        print(f"❌ {game_name} failed completely: {e}")
        return "Failed"

def main():
    """Run the API-based tournament."""
    print("🏟️ CLAUDE vs OPENAI API TOURNAMENT")
    print("====================================")
    print(f"Results saved to: {TOURNAMENT_DIR.absolute()}")
    
    # Discover games
    working_games, api = test_general_api()
    
    if not api:
        print("❌ Could not initialize API")
        return
    
    # Focus on games we know work
    priority_games = ["tic_tac_toe", "nim", "mancala", "mastermind", "connect4", "reversi"]
    
    tournament_results = {}
    
    print(f"\n🎯 Testing {len(priority_games)} priority games...")
    
    for game_name in priority_games:
        if game_name in working_games:
            winner = run_api_game(game_name, api)
            tournament_results[game_name] = winner
        else:
            print(f"⚠️ {game_name} not in working games list")
            tournament_results[game_name] = "Not Available"
    
    # Summary
    print("\n" + "="*60)
    print("🏆 API TOURNAMENT RESULTS")
    print("="*60)
    
    for game, result in tournament_results.items():
        status_icon = "✅" if result not in ["Failed", "Not Available", "No Config", "No Agent"] else "❌"
        print(f"{status_icon} {game.replace('_', ' ').title()}: {result}")
    
    successful = len([r for r in tournament_results.values() if r not in ["Failed", "Not Available", "No Config", "No Agent"]])
    total = len(tournament_results)
    
    print(f"\n📊 Success Rate: {successful}/{total} games completed")
    print(f"📁 Detailed results: {TOURNAMENT_DIR.absolute()}")
    
    # Show individual game files
    print(f"\n📄 Result Files:")
    for file in sorted(TOURNAMENT_DIR.glob("*.json")):
        print(f"   {file.name}")

if __name__ == "__main__":
    main()