#!/usr/bin/env python3
"""Run tests for enhanced agents with debug output."""

import subprocess
import sys


def run_test(test_path: str):
    """Run a specific test with poetry."""
    cmd = [
        "poetry",
        "run",
        "pytest",
        test_path,
        "-xvs",  # Stop on first failure, verbose, no capture
        "--tb=short",  # Shorter traceback
    ]

    result = subprocess.run(cmd, check=False, capture_output=False)
    return result.returncode == 0


def main():
    """Run all enhanced agent tests."""
    tests = [
        # Multi-agent tests
        "packages/haive-agents/tests/multi/test_enhanced_multi_agents.py::TestSupervisorAgent::test_supervisor_creation",
        "packages/haive-agents/tests/multi/test_enhanced_multi_agents.py::TestSequentialAgent::test_sequential_pipeline",
        "packages/haive-agents/tests/multi/test_enhanced_multi_agents.py::TestEnhancedMultiAgent::test_multi_agent_creation",
        # RAG tests
        "packages/haive-agents/tests/rag/test_enhanced_rag_agents.py::TestBaseRAGAgent::test_base_rag_creation",
        "packages/haive-agents/tests/rag/test_enhanced_rag_agents.py::TestSimpleRAGAgent::test_simple_rag_creation",
    ]

    passed = 0
    failed = 0

    for test in tests:
        if run_test(test):
            passed += 1
        else:
            failed += 1

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
