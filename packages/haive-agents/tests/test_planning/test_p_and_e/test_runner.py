#!/usr/bin/env python
"""Quick test runner to verify tests work."""

import subprocess
import sys


def run_tests():
    """Run all plan and execute tests."""
    test_files = [
        "tests/test_planning/test_p_and_e/test_models.py",
        "tests/test_planning/test_p_and_e/test_state.py",
        "tests/test_planning/test_p_and_e/test_agent.py",
        "tests/test_planning/test_p_and_e/test_integration.py",
    ]

    for test_file in test_files:

        result = subprocess.run(
            ["poetry", "run", "pytest", test_file, "-v"],
            check=False,
            capture_output=True,
            text=True,
        )

        if result.stderr:
            pass

        if result.returncode != 0:
            return False

    return True


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
