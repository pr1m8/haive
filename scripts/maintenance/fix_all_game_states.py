#!/usr/bin/env python3
"""
Fix all game state initialization issues.
Test and document proper initialization methods for each game.
"""

def test_game_state_initialization():
    """Test proper state initialization for each game."""
    
    results = {}
    
    # Test Tic Tac Toe
    try:
        from haive.games.tic_tac_toe.state import TicTacToeState
        state = TicTacToeState()  # Should work
        results["tic_tac_toe"] = {"method": "TicTacToeState()", "status": "✅ Works"}
    except Exception as e:
        results["tic_tac_toe"] = {"method": "TicTacToeState()", "status": f"❌ {e}"}
    
    # Test Mastermind
    try:
        from haive.games.mastermind.state import MastermindState
        state = MastermindState()  # This will fail
        results["mastermind_direct"] = {"method": "MastermindState()", "status": "✅ Works"}
    except Exception as e:
        results["mastermind_direct"] = {"method": "MastermindState()", "status": f"❌ {e}"}
    
    try:
        from haive.games.mastermind.state import MastermindState
        state = MastermindState.initialize()  # This should work
        results["mastermind_initialize"] = {"method": "MastermindState.initialize()", "status": "✅ Works"}
    except Exception as e:
        results["mastermind_initialize"] = {"method": "MastermindState.initialize()", "status": f"❌ {e}"}
    
    # Test Connect4
    try:
        from haive.games.connect4.state import Connect4State
        state = Connect4State()  # This will fail
        results["connect4_direct"] = {"method": "Connect4State()", "status": "✅ Works"}
    except Exception as e:
        results["connect4_direct"] = {"method": "Connect4State()", "status": f"❌ {e}"}
    
    try:
        from haive.games.connect4.state import Connect4State
        state = Connect4State.initialize()  # This should work
        results["connect4_initialize"] = {"method": "Connect4State.initialize()", "status": "✅ Works"}
    except Exception as e:
        results["connect4_initialize"] = {"method": "Connect4State.initialize()", "status": f"❌ {e}"}
    
    # Test Mancala
    try:
        from haive.games.mancala.state import MancalaState
        state = MancalaState()
        results["mancala"] = {"method": "MancalaState()", "status": "✅ Works"}
    except Exception as e:
        results["mancala"] = {"method": "MancalaState()", "status": f"❌ {e}"}
    
    # Test Nim
    try:
        from haive.games.nim.state import NimState
        state = NimState()
        results["nim"] = {"method": "NimState()", "status": "✅ Works"}
    except Exception as e:
        results["nim"] = {"method": "NimState()", "status": f"❌ {e}"}
    
    # Test Reversi
    try:
        from haive.games.reversi.state import ReversiState
        state = ReversiState()
        results["reversi"] = {"method": "ReversiState()", "status": "✅ Works"}
    except Exception as e:
        results["reversi"] = {"method": "ReversiState()", "status": f"❌ {e}"}
    
    return results

def main():
    """Test all game state initializations."""
    print("🔧 Testing Game State Initializations")
    print("=" * 50)
    
    results = test_game_state_initialization()
    
    for game, result in results.items():
        print(f"{result['status']:30} {game:15} → {result['method']}")
    
    print("\n📋 Summary:")
    working = [k for k, v in results.items() if "✅" in v['status']]
    failing = [k for k, v in results.items() if "❌" in v['status']]
    
    print(f"✅ Working: {len(working)} games")
    print(f"❌ Failing: {len(failing)} games")
    
    if failing:
        print(f"\n🛠️ Need to fix: {', '.join(failing)}")

if __name__ == "__main__":
    main()