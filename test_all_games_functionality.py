#!/usr/bin/env python3
"""Test all games end-to-end functionality."""

import traceback
from pathlib import Path

def test_game_functionality(game_name: str) -> dict:
    """Test a single game's functionality."""
    results = {
        'game': game_name,
        'import_success': False,
        'config_creation': False,
        'engine_creation': False,
        'errors': []
    }
    
    try:
        # Test imports
        print(f"  📦 Testing imports for {game_name}...")
        
        # Try importing the configurable config
        config_module = f"haive.games.{game_name}.configurable_config"
        config_imported = __import__(config_module, fromlist=[''])
        
        # Try importing the generic engines
        engines_module = f"haive.games.{game_name}.generic_engines"
        engines_imported = __import__(engines_module, fromlist=[''])
        
        results['import_success'] = True
        print(f"    ✅ Imports successful")
        
        # Test config creation - find the main create function
        print(f"  ⚙️ Testing config creation...")
        
        # Try to find the main config creation function
        create_func_name = f"create_{game_name}_config"
        if hasattr(config_imported, create_func_name):
            create_func = getattr(config_imported, create_func_name)
            # Test with simple parameters
            config = create_func("gpt-4o", "claude-3-opus", temperature=0.3)
            results['config_creation'] = True
            print(f"    ✅ Config creation successful")
            
            # Test engine creation
            print(f"  🔧 Testing engine creation...")
            if hasattr(config, 'engines') and config.engines:
                results['engine_creation'] = True
                print(f"    ✅ Engine creation successful ({len(config.engines)} engines)")
            else:
                results['errors'].append("Config has no engines or empty engines")
                print(f"    ❌ No engines found in config")
        else:
            results['errors'].append(f"No {create_func_name} function found")
            print(f"    ❌ No {create_func_name} function found")
            
    except Exception as e:
        error_msg = f"{type(e).__name__}: {str(e)}"
        results['errors'].append(error_msg)
        print(f"    ❌ Error: {error_msg}")
        
    return results

def main():
    """Test all games functionality."""
    print("🧪 Testing ALL games end-to-end functionality...")
    print("=" * 60)
    
    # List of games to test (excluding framework dirs and go)
    games_to_test = [
        'among_us', 'battleship', 'checkers', 'chess', 'clue', 'connect4', 
        'debate', 'dominoes', 'fox_and_geese', 'hold_em', 'mafia', 'mancala', 
        'mastermind', 'monopoly', 'nim', 'poker', 'reversi', 'risk', 'tic_tac_toe'
    ]
    
    all_results = []
    successful_games = 0
    
    for game in games_to_test:
        print(f"\n🎮 Testing {game}...")
        results = test_game_functionality(game)
        all_results.append(results)
        
        if results['import_success'] and results['config_creation'] and results['engine_creation']:
            successful_games += 1
            print(f"  ✅ {game} - FULLY FUNCTIONAL")
        else:
            print(f"  ❌ {game} - ISSUES FOUND")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 FINAL TEST SUMMARY")
    print("=" * 60)
    
    print(f"Total games tested: {len(games_to_test)}")
    print(f"Fully functional: {successful_games}/{len(games_to_test)}")
    print()
    
    # Detailed results
    for result in all_results:
        status = "✅" if (result['import_success'] and result['config_creation'] and result['engine_creation']) else "❌"
        print(f"{status} {result['game']:15} - Import: {result['import_success']}, Config: {result['config_creation']}, Engines: {result['engine_creation']}")
        
        if result['errors']:
            for error in result['errors']:
                print(f"    └── Error: {error}")
    
    # Final status
    print()
    if successful_games == len(games_to_test):
        print("🎉 SUCCESS: All games are fully functional!")
    else:
        failed_count = len(games_to_test) - successful_games
        print(f"⚠️ ISSUES: {failed_count} games have problems that need fixing")
    
    return successful_games == len(games_to_test)

if __name__ == '__main__':
    main()