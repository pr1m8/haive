#!/usr/bin/env python3
"""Run Tic Tac Toe model tests directly without pytest framework.

This bypasses the conftest.py dependency issues and runs the tests directly.
"""

import sys
from pathlib import Path

# Add haive-games source to path
haive_games_src = Path(__file__).parent / "packages" / "haive-games" / "src"
sys.path.insert(0, str(haive_games_src))

# Import models directly (bypass __init__.py issues)
import importlib.util

models_path = haive_games_src / "haive" / "games" / "tic_tac_toe" / "models.py"
spec = importlib.util.spec_from_file_location("models", models_path)
models_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(models_module)

TicTacToeMove = models_module.TicTacToeMove
TicTacToeAnalysis = models_module.TicTacToeAnalysis


def test_tic_tac_toe_move():
    """Test TicTacToeMove model creation and string representation."""

    # X move
    move_x = TicTacToeMove(row=0, col=1, player="X")
    assert move_x.row == 0
    assert move_x.col == 1
    assert move_x.player == "X"
    assert "X places at (0, 1)" in str(move_x)

    # O move
    move_o = TicTacToeMove(row=2, col=2, player="O")
    assert move_o.row == 2
    assert move_o.col == 2
    assert move_o.player == "O"
    assert "O places at (2, 2)" in str(move_o)

    # Invalid row (too high)
    try:
        TicTacToeMove(row=3, col=1, player="X")
        raise AssertionError("Should have raised ValueError")
    except ValueError:
        pass")

    # Invalid column (too high)
    try:
        TicTacToeMove(row=1, col=3, player="X")
        raise AssertionError("Should have raised ValueError")
    except ValueError:
        pass")

    # Invalid player
    try:
        TicTacToeMove(row=1, col=1, player="Z")
        raise AssertionError("Should have raised ValueError")
    except ValueError:
        pass")


def test_tic_tac_toe_analysis():
    """Test TicTacToeAnalysis model creation and validation."""

    # Create basic analysis
    analysis = TicTacToeAnalysis(
        winning_moves=[{"row": 0, "col": 0}],
        blocking_moves=[{"row": 2, "col": 0}],
        fork_opportunities=[{"row": 1, "col": 1}],
        center_available=True,
        corner_available=True,
        position_evaluation="winning",
        recommended_move={"row": 0, "col": 0},
        strategy="Go for the win by playing at (0, 0)",
    )

    # Check fields
    assert len(analysis.winning_moves) == 1
    assert analysis.winning_moves[0]["row"] == 0
    assert analysis.winning_moves[0]["col"] == 0

    assert len(analysis.blocking_moves) == 1
    assert analysis.blocking_moves[0]["row"] == 2
    assert analysis.blocking_moves[0]["col"] == 0

    assert len(analysis.fork_opportunities) == 1
    assert analysis.fork_opportunities[0]["row"] == 1
    assert analysis.fork_opportunities[0]["col"] == 1

    assert analysis.center_available is True
    assert analysis.corner_available is True
    assert analysis.position_evaluation == "winning"
    assert analysis.recommended_move["row"] == 0
    assert analysis.recommended_move["col"] == 0
    assert "Go for the win" in analysis.strategy

    # Test with empty lists
    analysis = TicTacToeAnalysis(
        winning_moves=[],
        blocking_moves=[],
        fork_opportunities=[],
        center_available=False,
        corner_available=False,
        position_evaluation="drawing",
        recommended_move=None,
        strategy="Game is heading for a draw",
    )

    assert len(analysis.winning_moves) == 0
    assert len(analysis.blocking_moves) == 0
    assert len(analysis.fork_opportunities) == 0
    assert analysis.center_available is False
    assert analysis.corner_available is False
    assert analysis.position_evaluation == "drawing"
    assert analysis.recommended_move is None
    assert "draw" in analysis.strategy

    # Invalid position evaluation
    try:
        TicTacToeAnalysis(
            winning_moves=[],
            blocking_moves=[],
            fork_opportunities=[],
            center_available=False,
            corner_available=False,
            position_evaluation="maybe",  # Invalid value
            recommended_move=None,
            strategy="Game is uncertain",
        )
        raise AssertionError("Should have raised ValueError")
    except ValueError:
        pass")


def run_all_tests():
    """Run all tic tac toe model tests."""

    tests = [
        ("TicTacToeMove", test_tic_tac_toe_move),
        ("TicTacToeAnalysis", test_tic_tac_toe_analysis),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        try:
            test_func()
            passed += 1
        except Exception as e:
            import traceback

            traceback.print_exc()


    if passed == total:
        return True
    print("❌ Some tests failed")
    return False


if __name__ == "__main__":
    success = run_all_tests()

    if success:

        # Mark task as completed
    else:
        pass")

    sys.exit(0 if success else 1)
