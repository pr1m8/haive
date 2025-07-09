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
        print(f"\n{'='*60}")
        print(f"Running {test_file}")
        print("=" * 60)

        result = subprocess.run(
            ["poetry", "run", "pytest", test_file, "-v"], capture_output=True, text=True
        )

        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)

        if result.returncode != 0:
            print(f"FAILED: {test_file}")
            return False

    print("\n" + "=" * 60)
    print("All tests completed!")
    return True


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
