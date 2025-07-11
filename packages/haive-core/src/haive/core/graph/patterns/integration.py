"""Integration utilities for the pattern system.

This module provides helper functions for integrating the pattern system with
other components of the Haive framework, particularly with the DynamicGraph
builder and the NodeFactory.
"""

import logging
from typing import Any

from haive.core.graph.patterns.registry import GraphPatternRegistry

logger = logging.getLogger(__name__)


def apply_pattern_to_graph(
    graph: Any, pattern_name: str, verify_compatibility: bool = True, **kwargs
) -> Any:
    """Apply a registered pattern to a graph with enhanced verification."""
    # Get registry using singleton
    registry = GraphPatternRegistry.get_instance()
    pattern = registry.get_pattern(pattern_name)

    if not pattern:
        error_msg = f"Pattern {pattern_name} not found in registry"
        logger.error(error_msg)
        raise ValueError(error_msg)

    # Verify component compatibility if requested
    if verify_compatibility:
        components = getattr(graph, "components", [])
        missing = pattern.metadata.check_required_components(components)
        if missing:
            error_msg = f"Missing required components for pattern: {', '.join(missing)}"
            logger.error(error_msg)
            raise ValueError(error_msg)

    # Apply the pattern
    try:
        result = pattern.apply(graph, **kwargs)

        # Track applied pattern if graph supports it
        if (
            hasattr(graph, "applied_patterns")
            and pattern_name not in graph.applied_patterns
        ):
            graph.applied_patterns.append(pattern_name)

        return result
    except Exception as e:
        logger.exception(f"Error applying pattern {pattern_name}: {e}")
        raise


def apply_branch_to_graph(
    graph: Any, branch_name: str, source_node: str, **kwargs
) -> Any:
    """Apply a registered branch to a graph.

    Args:
        graph: Graph to apply the branch to
        branch_name: Name of branch to apply
        source_node: Source node for the branch
        **kwargs: Branch parameters

    Returns:
        Modified graph
    """
    registry = GraphPatternRegistry.get_instance()
    branch = registry.get_branch(branch_name)

    if not branch:
        error_msg = f"Branch {branch_name} not found in registry"
        logger.error(error_msg)
        raise ValueError(error_msg)

    # Apply the branch
    return branch.apply_to_graph(graph, source_node, **kwargs)


def create_pattern_node_config(
    pattern_name: str, node_name: str, **pattern_params
) -> Any:
    """Create a NodeConfig based on a pattern.

    Note: This requires importing NodeConfig, which is done dynamically
    to avoid circular imports.

    Args:
        pattern_name: Pattern to use as template
        node_name: Name for the node
        **pattern_params: Pattern parameters

    Returns:
        NodeConfig instance
    """
    # Import NodeConfig dynamically to avoid circular imports
    try:
        from haive.core.graph.node.config import NodeConfig
    except ImportError:
        logger.exception(
            "Cannot import NodeConfig, integration with NodeFactory unavailable"
        )
        raise ImportError("NodeConfig not available")

    registry = GraphPatternRegistry.get_instance()
    pattern = registry.get_pattern(pattern_name)

    if not pattern:
        raise ValueError(f"Pattern {pattern_name} not found")

    # Validate pattern parameters
    is_valid, errors = pattern.metadata.validate_parameters(pattern_params)
    if not is_valid:
        error_msg = (
            f"Invalid parameters for pattern {pattern_name}: {', '.join(errors)}"
        )
        logger.error(error_msg)
        raise ValueError(error_msg)

    # Create a function that will apply the pattern when used as a node
    def pattern_node(state, config=None):
        """Node function that applies a pattern."""
        try:
            # This is a placeholder implementation
            # Actual implementation would depend on how patterns work as nodes
            result = {"pattern_applied": pattern_name}
            for key, value in pattern_params.items():
                result[key] = value
            return result
        except Exception as e:
            logger.exception(f"Error in pattern node {node_name}: {e}")
            return {"error": str(e)}

    # Create node config
    node_config = NodeConfig(
        name=node_name,
        engine=pattern_node,
        metadata={
            "pattern": pattern_name,
            "pattern_type": pattern.metadata.pattern_type,
            "pattern_params": pattern_params,
        },
    )

    return node_config


def register_node_factory_integration():
    """Register integration with the NodeFactory.

    This adds a method to NodeFactory to create nodes from patterns.
    """
    try:
        from haive.core.graph.node.factory import NodeFactory

        # Only add if not already present
        if not hasattr(NodeFactory, "create_pattern_node"):

            @classmethod
            def create_pattern_node(cls, pattern_name, node_name, **pattern_params):
                """Create a node function based on a pattern.

                Args:
                    pattern_name: Pattern to use as template
                    node_name: Name for the node
                    **pattern_params: Pattern parameters

                Returns:
                    Node function
                """
                node_config = create_pattern_node_config(
                    pattern_name, node_name, **pattern_params
                )
                return cls.create_node_function(node_config)

            # Add method to NodeFactory
            NodeFactory.create_pattern_node = create_pattern_node
            logger.info("Registered NodeFactory integration")

    except ImportError:
        logger.warning("NodeFactory not available, skipping integration")


def register_dynamic_graph_integration():
    """Register integration with the DynamicGraph.

    This enhances the apply_pattern method in DynamicGraph.
    """
    try:
        from haive.core.graph.dynamic_graph_builder import DynamicGraph

        # Store the original method if it exists
        original_method = getattr(DynamicGraph, "apply_pattern", None)

        # Define enhanced method
        def enhanced_apply_pattern(
            self, pattern_name, verify_compatibility=True, **kwargs
        ):
            """Apply a registered pattern with enhanced verification.

            Args:
                pattern_name: Name of pattern to apply
                verify_compatibility: Whether to verify component compatibility
                **kwargs: Pattern parameters

            Returns:
                Self for chaining
            """
            # If original method exists, try that first
            if original_method is not None:
                try:
                    return original_method(self, pattern_name, **kwargs)
                except Exception as e:
                    logger.debug(
                        f"Original apply_pattern failed: {e}, trying enhanced version"
                    )

            # Use enhanced implementation
            apply_pattern_to_graph(self, pattern_name, verify_compatibility, **kwargs)
            return self

        # Replace or add the method
        DynamicGraph.apply_pattern = enhanced_apply_pattern
        logger.info("Registered DynamicGraph integration")

        # Add branch application method if not present
        if not hasattr(DynamicGraph, "apply_branch"):

            def apply_branch(self, branch_name, source_node, **kwargs):
                """Apply a registered branch to this graph.

                Args:
                    branch_name: Name of branch to apply
                    source_node: Source node for the branch
                    **kwargs: Branch parameters

                Returns:
                    Self for chaining
                """
                apply_branch_to_graph(self, branch_name, source_node, **kwargs)
                return self

            # Add method to DynamicGraph
            DynamicGraph.apply_branch = apply_branch
            logger.info("Added apply_branch method to DynamicGraph")

    except ImportError:
        logger.warning("DynamicGraph not available, skipping integration")


def check_component_compatibility(
    components: list[Any], pattern_name: str
) -> tuple[bool, list[str]]:
    """Check if components are compatible with a pattern.

    Args:
        components: List of components to check
        pattern_name: Name of pattern to check against

    Returns:
        Tuple of (is_compatible, missing_components)
    """
    registry = GraphPatternRegistry.get_instance()
    pattern = registry.get_pattern(pattern_name)

    if not pattern:
        return False, [f"Pattern {pattern_name} not found"]

    missing = pattern.metadata.check_required_components(components)
    return len(missing) == 0, missing


def find_compatible_patterns(components: list[Any]) -> list[str]:
    """Find patterns compatible with the given components.

    Args:
        components: List of components to check

    Returns:
        List of compatible pattern names
    """
    registry = GraphPatternRegistry.get_instance()
    compatible_patterns = []

    for pattern_name, pattern in registry.patterns.items():
        missing = pattern.metadata.check_required_components(components)
        if not missing:
            compatible_patterns.append(pattern_name)

    return compatible_patterns


# Add to src/haive/core/graph/patterns/integration.py


def register_callable_processor():
    """Register the callable processor explicitly."""
    try:
        from haive.core.graph.node.processors import CallableNodeProcessor
        from haive.core.graph.node.registry import NodeTypeRegistry

        # Get registry
        registry = NodeTypeRegistry.get_instance()

        # Register callable processor
        registry.register_node_processor("callable", CallableNodeProcessor())

        logger.info("Registered callable proWScessor")
    except ImportError as e:
        logger.warning(f"Could not register callable processor: {e}")


def register_integrations():
    """Register all integrations."""
    register_node_factory_integration()
    register_dynamic_graph_integration()
    register_callable_processor()  # Add this line


# Uncomment to auto-register when module is imported
