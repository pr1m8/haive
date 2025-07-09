"""Simple test script for the modular BaseGraph architecture.

This script tests the basic functionality of the new modular components
to ensure they work correctly before integrating with existing agents.
"""

import logging
from typing import Any, Dict

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def test_node_functions():
    """Test functions to use as nodes."""

    def start_function(state: Dict[str, Any]) -> Dict[str, Any]:
        """Start node function."""
        logger.info("Start function called")
        return {"status": "started", "count": 0}

    def process_function(state: Dict[str, Any]) -> Dict[str, Any]:
        """Process node function."""
        logger.info("Process function called")
        count = state.get("count", 0)
        return {"status": "processing", "count": count + 1}

    def router_function(state: Dict[str, Any]) -> str:
        """Router function for conditional edges."""
        count = state.get("count", 0)
        if count >= 3:
            return "finish"
        else:
            return "continue"

    return start_function, process_function, router_function


def test_basic_modular_graph():
    """Test basic ModularBaseGraph functionality."""
    try:
        from haive.core.graph.state_graph.components import ModularBaseGraph

        logger.info("Testing basic ModularBaseGraph functionality...")

        # Create graph
        graph = ModularBaseGraph(name="test_workflow", description="Test workflow")

        # Test initial state
        assert graph.name == "test_workflow"
        assert graph.get_node_count() == 0
        assert graph.get_edge_count() == 0
        assert graph.get_branch_count() == 0

        # Get test functions
        start_func, process_func, router_func = test_node_functions()

        # Add nodes
        graph.add_node("start", start_func)
        graph.add_node("process", process_func)
        graph.add_node("finish", lambda state: {"status": "finished"})

        # Test node operations
        assert graph.get_node_count() == 3
        assert graph.get_node("start") is not None
        assert graph.get_node("nonexistent") is None

        # Add edges
        graph.add_edge("start", "process")

        # Test edge operations
        assert graph.get_edge_count() == 1
        assert graph.has_edge("start", "process")
        assert not graph.has_edge("process", "start")

        # Set entry and finish points
        graph.set_entry_point("start")
        graph.set_finish_point("finish")

        assert graph.entry_point == "start"
        assert graph.finish_point == "finish"
        assert graph.has_entry_point()

        # Add conditional routing
        graph.add_conditional_edges(
            "process", router_func, {"continue": "process", "finish": "finish"}
        )

        # Test branch operations
        assert graph.get_branch_count() > 0
        branches = graph.get_branches_for_node("process")
        assert len(branches) > 0

        # Test validation
        errors = graph.validate_graph()
        logger.info(f"Validation errors: {errors}")

        # Test graph summary
        summary = graph.get_graph_summary()
        logger.info(f"Graph summary: {summary}")

        # Test compilation (placeholder)
        compiled_graph = graph.compile()
        assert compiled_graph is not None

        logger.info("✅ Basic ModularBaseGraph test passed!")
        return True

    except Exception as e:
        logger.error(f"❌ Basic test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_component_isolation():
    """Test that components work in isolation."""
    try:
        from haive.core.graph.state_graph.components import (
            BranchManager,
            EdgeManager,
            ModularBaseGraph,
            NodeManager,
        )

        logger.info("Testing component isolation...")

        # Create a minimal graph for testing
        graph = ModularBaseGraph(name="isolation_test")

        # Test NodeManager isolation
        node_manager = graph._node_manager
        assert node_manager.component_name == "node_manager"
        assert node_manager.is_initialized

        # Test EdgeManager isolation
        edge_manager = graph._edge_manager
        assert edge_manager.component_name == "edge_manager"
        assert edge_manager.is_initialized

        # Test BranchManager isolation
        branch_manager = graph._branch_manager
        assert branch_manager.component_name == "branch_manager"
        assert branch_manager.is_initialized

        # Test component info
        node_info = node_manager.get_component_info()
        edge_info = edge_manager.get_component_info()
        branch_info = branch_manager.get_component_info()

        assert node_info["component_name"] == "node_manager"
        assert edge_info["component_name"] == "edge_manager"
        assert branch_info["component_name"] == "branch_manager"

        logger.info("✅ Component isolation test passed!")
        return True

    except Exception as e:
        logger.error(f"❌ Component isolation test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_error_handling():
    """Test error handling in modular components."""
    try:
        from haive.core.graph.state_graph.components import ModularBaseGraph

        logger.info("Testing error handling...")

        graph = ModularBaseGraph(name="error_test")

        # Test node errors
        try:
            graph.remove_node("nonexistent")
            assert False, "Should have raised ValueError"
        except ValueError:
            pass  # Expected

        try:
            graph.set_entry_point("nonexistent")
            assert False, "Should have raised ValueError"
        except ValueError:
            pass  # Expected

        # Test edge errors
        try:
            graph.add_edge("nonexistent1", "nonexistent2")
            assert False, "Should have raised ValueError"
        except ValueError:
            pass  # Expected

        # Test branch errors
        try:
            graph.add_conditional_edges(
                "nonexistent", lambda x: "test", {"test": "target"}
            )
            assert False, "Should have raised ValueError"
        except ValueError:
            pass  # Expected

        logger.info("✅ Error handling test passed!")
        return True

    except Exception as e:
        logger.error(f"❌ Error handling test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    logger.info("🚀 Starting ModularBaseGraph tests...")

    tests = [
        test_basic_modular_graph,
        test_component_isolation,
        test_error_handling,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1
        else:
            logger.error(f"Test {test.__name__} failed!")

    logger.info(f"📊 Test Results: {passed}/{total} tests passed")

    if passed == total:
        logger.info("🎉 All tests passed! Modular architecture is working correctly.")
        return True
    else:
        logger.error("💥 Some tests failed. Please check the implementation.")
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
