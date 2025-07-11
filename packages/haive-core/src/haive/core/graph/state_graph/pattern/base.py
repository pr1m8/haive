import logging
from abc import ABC
from typing import Any, ClassVar, Dict, List, Optional, Tuple, Type

from langgraph.graph import END, START
from pydantic import Field

from haive.core.graph.common.types import NodeLike
from haive.core.graph.state_graph.base_graph2 import BaseGraph

logger = logging.getLogger(__name__)


class GraphPattern(BaseGraph, ABC):
    """Abstract base class for graph patterns built on BaseGraph.

    GraphPattern provides a foundation for creating reusable graph structures
    with automatic inheritance of nodes, edges, and conditional branches.
    """

    # Pattern structure to be defined in subclasses - renamed to avoid conflicts
    pattern_nodes: ClassVar[dict[str, NodeLike | None]] = {}
    pattern_edges: ClassVar[list[tuple[str, str]]] = []
    pattern_conditionals: ClassVar[list[dict[str, Any]]] = []

    # Registry for pattern classes
    _registry: ClassVar[dict[str, type["GraphPattern"]]] = {}

    # Add implementations field as a proper Pydantic field
    implementations: dict[str, Any] = Field(default_factory=dict)

    def __init__(self, name=None, description=None, **kwargs):
        """Initialize the pattern with default name and description.

        Args:
            name: Optional name (defaults to class name in snake_case)
            description: Optional description
            **kwargs: Additional parameters for BaseGraph
        """
        # Use class name as default
        pattern_name = name or self.__class__.__name__.lower().replace("pattern", "")
        pattern_desc = description or f"{self.__class__.__name__} graph pattern"

        # Initialize the base graph
        super().__init__(name=pattern_name, description=pattern_desc, **kwargs)

    def set_implementation(self, node_name: str, implementation: Any) -> "GraphPattern":
        """Set implementation for a node in the pattern.

        Args:
            node_name: Name of the node
            implementation: Implementation object/function

        Returns:
            Self for method chaining
        """
        self.implementations[node_name] = implementation
        return self

    def build(self):
        """Build the pattern with structure from class hierarchy.

        This automatically:
        1. Collects nodes/edges from parent classes
        2. Adds them to the graph in proper order
        3. Calls _build for pattern-specific logic

        Returns:
            Self for method chaining
        """
        # Process parent classes first (inheritance chain)
        processed_classes = set()

        # Process in MRO order (parent first)
        for cls in reversed(self.__class__.__mro__):
            # Skip non-pattern classes and already processed ones
            if (
                cls is GraphPattern
                or cls is BaseGraph
                or cls is ABC
                or not issubclass(cls, GraphPattern)
                or cls in processed_classes
            ):
                continue

            # Add nodes from this class first
            self._add_class_nodes(cls)
            processed_classes.add(cls)

        # Now add edges from all classes
        for cls in reversed(self.__class__.__mro__):
            if (
                cls is GraphPattern
                or cls is BaseGraph
                or cls is ABC
                or not issubclass(cls, GraphPattern)
            ):
                continue

            # Add edges and conditionals
            self._add_class_edges(cls)
            self._add_class_conditionals(cls)

        # Call implementation-specific build method
        self._build()

        return self

    def _build(self):
        """Implementation-specific build logic.

        Override this method in subclasses to add custom build logic.
        """

    def _add_class_nodes(self, cls):
        """Add nodes from a class to this graph instance."""
        # Look for pattern_nodes in the class (renamed from nodes)
        for name, default_impl in getattr(cls, "pattern_nodes", {}).items():
            # Check if we already have this node
            if name not in self.nodes:
                try:
                    # Use instance-specific implementation if available, otherwise use default
                    implementation = self.implementations.get(name, default_impl)
                    self.add_node(name, implementation)
                except Exception as e:
                    logger.warning(f"Error adding node {name}: {e}")

    def _add_class_edges(self, cls):
        """Add edges from a class to this graph instance."""
        # Look for pattern_edges in the class (renamed from edges)
        for source, target in getattr(cls, "pattern_edges", []):
            try:
                # Add edge if it doesn't exist yet
                if not any(e == (source, target) for e in self.edges):
                    self.add_edge(source, target)
            except Exception as e:
                logger.warning(f"Error adding edge {source} -> {target}: {e}")

    def _add_class_conditionals(self, cls):
        """Add conditional branches from a class to this graph instance."""
        # Look for pattern_conditionals in the class (renamed from conditionals)
        for branch_def in getattr(cls, "pattern_conditionals", []):
            try:
                source = branch_def.get("source")
                condition = branch_def.get("condition")
                destinations = branch_def.get("destinations", {})
                default = branch_def.get("default", END)

                if source and condition and destinations:
                    # Check if we already have a conditional from this source
                    existing_branches = self.get_branches_for_node(source)

                    # Only add if we don't already have a branch with the same condition function
                    if not any(
                        getattr(branch, "function", None) is condition
                        for branch in existing_branches
                    ):
                        self.add_conditional_edges(
                            source, condition, destinations, default
                        )
            except Exception as e:
                logger.warning(f"Error adding conditional branch: {e}")

    def get_source_nodes(self):
        """Get nodes that have no incoming edges from regular nodes (excluding START).

        Returns:
            List of source node names
        """
        # Track nodes with incoming edges from regular nodes
        has_incoming_from_regular = set()

        # Check direct edges
        for src, dst in self.edges:
            if src != START:
                has_incoming_from_regular.add(dst)

        # Check branches
        for branch in self.branches.values():
            if branch.source_node != START:
                for dst in branch.destinations.values():
                    has_incoming_from_regular.add(dst)

                # Include default destination
                if branch.default:
                    has_incoming_from_regular.add(branch.default)

        # Return nodes that only have incoming edges from START
        return [node for node in self.nodes if node not in has_incoming_from_regular]

    @classmethod
    def register(cls, pattern_name: str | None = None):
        """Decorator for registering pattern classes.

        Args:
            pattern_name: Optional name for the pattern

        Returns:
            Decorator function
        """

        def decorator(pattern_class):
            name = pattern_name or pattern_class.__name__
            cls._registry[name] = pattern_class
            logger.info(f"Registered pattern: {name}")
            return pattern_class

        return decorator

    @classmethod
    def get_pattern(cls, pattern_name: str) -> type["GraphPattern"]:
        """Get a pattern class by name.

        Args:
            pattern_name: Name of the pattern

        Returns:
            Pattern class

        Raises:
            ValueError: If pattern not found
        """
        if pattern_name not in cls._registry:
            raise ValueError(f"Pattern not found: {pattern_name}")
        return cls._registry[pattern_name]

    @classmethod
    def list_patterns(cls) -> list[str]:
        """List all registered patterns.

        Returns:
            List of pattern names
        """
        return list(cls._registry.keys())

    @classmethod
    def create(cls, pattern_name: str, **kwargs) -> "GraphPattern":
        """Create a pattern instance from the registry.

        Args:
            pattern_name: Name of the pattern
            **kwargs: Parameters for initialization

        Returns:
            Built pattern instance
        """
        pattern_class = cls.get_pattern(pattern_name)
        return pattern_class(**kwargs).build()
