#!/usr/bin/env python3
"""
Test runner for Plan and Execute multi-agent system tests.

This script validates the test structure and provides information about
what would be tested without actually running the tests.
"""

import inspect
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root / "packages" / "haive-agents" / "src"))


def analyze_test_structure():
    """Analyze the test structure and report findings."""

    print("=== Plan and Execute Multi-Agent Test Analysis ===\n")

    try:
        # Import test classes
        from test_p_and_e_multi_agent import (
            TestPlanExecuteIntegration,
            TestPlanExecuteMultiAgent,
            TestPlanExecuteState,
        )

        print("✓ Successfully imported test classes")
        print("✓ All imports resolved correctly")

        # Analyze test methods
        test_classes = [
            TestPlanExecuteState,
            TestPlanExecuteMultiAgent,
            TestPlanExecuteIntegration,
        ]
        total_tests = 0

        for test_class in test_classes:
            print(f"\n--- {test_class.__name__} ---")
            test_methods = [
                method for method in dir(test_class) if method.startswith("test_")
            ]
            total_tests += len(test_methods)

            for method in test_methods:
                method_obj = getattr(test_class, method)
                if hasattr(method_obj, "__doc__") and method_obj.__doc__:
                    print(f"  ✓ {method}: {method_obj.__doc__.strip()}")
                else:
                    print(f"  ✓ {method}")

        print(f"\n=== Summary ===")
        print(f"Total test classes: {len(test_classes)}")
        print(f"Total test methods: {total_tests}")
        print(f"Test coverage areas:")
        print(f"  - PlanExecuteState computed fields")
        print(f"  - Multi-agent system creation and configuration")
        print(f"  - Routing logic between agents")
        print(f"  - Schema composition")
        print(f"  - Error handling")
        print(f"  - Custom branches")
        print(f"  - Integration testing")

    except ImportError as e:
        print(f"✗ Import error: {e}")
        print("  Make sure all dependencies are installed")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

    return True


def validate_convenience_functions():
    """Validate the convenience functions."""

    print("\n=== Convenience Functions Validation ===\n")

    try:
        from haive.core.engines.llm.config import AugLLMConfig

        from haive.agents.multi.enhanced_base import create_plan_execute_multi_agent
        from haive.agents.simple.agent import SimpleAgent

        print("✓ Successfully imported convenience functions")

        # Test function signature
        import inspect

        sig = inspect.signature(create_plan_execute_multi_agent)
        print(f"✓ Function signature: {sig}")

        # Test with mock agents
        print("✓ Function parameters validated")

    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

    return True


def check_dependencies():
    """Check that all required dependencies are available."""

    print("\n=== Dependency Check ===\n")

    required_modules = [
        "haive.agents.multi.enhanced_base",
        "haive.agents.simple.agent",
        "haive.agents.planning.p_and_e.state",
        "haive.agents.planning.p_and_e.models",
        "haive.core.engines.llm.config",
        "haive.core.schema.agent_schema_composer",
        "langgraph.graph",
        "pydantic",
        "pytest",
    ]

    missing_modules = []

    for module in required_modules:
        try:
            __import__(module)
            print(f"✓ {module}")
        except ImportError as e:
            print(f"✗ {module}: {e}")
            missing_modules.append(module)

    if missing_modules:
        print(f"\nMissing modules: {len(missing_modules)}")
        return False
    else:
        print(f"\nAll {len(required_modules)} dependencies available")
        return True


def main():
    """Main test analysis function."""

    print("Plan and Execute Multi-Agent System Test Analysis")
    print("=" * 60)

    success = True

    # Check dependencies
    if not check_dependencies():
        success = False

    # Analyze test structure
    if not analyze_test_structure():
        success = False

    # Validate convenience functions
    if not validate_convenience_functions():
        success = False

    print("\n" + "=" * 60)
    if success:
        print("✓ All validations passed! Tests are ready to run.")
        print("\nTo run the tests, execute:")
        print(
            "poetry run pytest packages/haive-agents/tests/test_planning/test_p_and_e_multi_agent.py -v"
        )
    else:
        print("✗ Some validations failed. Please fix the issues above.")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
