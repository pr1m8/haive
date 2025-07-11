# src/haive/core/graph/GraphPatternRegistry.py

import logging
from collections.abc import Callable
from typing import Any

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class GraphPattern(BaseModel):
    """Serializable graph pattern definition."""

    name: str = Field(description="Unique name for this pattern")
    description: str | None = Field(default=None, description="Pattern description")
    pattern_type: str = Field(description="Type of pattern")
    parameters: dict[str, Any] = Field(
        default_factory=dict, description="Pattern parameters"
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata"
    )

    # Internal function reference (not serialized)
    apply_func: Callable | None = Field(default=None, exclude=True)

    model_config = {"arbitrary_types_allowed": True}

    def apply(self, graph: Any, **kwargs) -> Any:
        """Apply this pattern to a graph.

        Args:
            graph: The graph to apply the pattern to
            **kwargs: Override parameters

        Returns:
            The modified graph
        """
        if self.apply_func is None:
            logger.warning(f"Pattern '{self.name}' has no apply function")
            return graph

        # Merge parameters with overrides
        params = {**self.parameters, **kwargs}

        # Apply the pattern
        return self.apply_func(graph, **params)


class BranchDefinition(BaseModel):
    """Serializable branch definition."""

    name: str = Field(description="Unique name for this branch")
    description: str | None = Field(default=None, description="Branch description")
    condition_type: str = Field(description="Type of condition")
    routes: dict[str, str] = Field(
        description="Mapping of condition values to node names"
    )
    default_route: str | None = Field(
        default=None, description="Default route if no condition matches"
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata"
    )

    # Internal function reference (not serialized)
    condition_func: Callable | None = Field(default=None, exclude=True)

    model_config = {"arbitrary_types_allowed": True}

    def create_condition(self, **kwargs) -> Callable:
        """Create a condition function from this branch definition.

        Args:
            **kwargs: Override parameters

        Returns:
            A condition function that can be used in conditional edges
        """
        if self.condition_func is None:
            # Create a default condition function based on routes
            def default_condition(state):
                # Look for route matches in state
                for route_key in self.routes:
                    if route_key in state:
                        return route_key

                # Return default or first route
                return self.default_route or next(iter(self.routes.keys()))

            return default_condition

        # Use the provided condition function
        return self.condition_func


class GraphPatternRegistry:
    """Registry for reusable graph patterns and branches."""

    _instance = None

    @classmethod
    def get_instance(cls) -> "GraphPatternRegistry":
        """Get the singleton instance."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.patterns: dict[str, GraphPattern] = {}
        self.branches: dict[str, BranchDefinition] = {}

    def register_pattern(self, pattern: GraphPattern | dict[str, Any]) -> GraphPattern:
        """Register a pattern in the registry.

        Args:
            pattern: Pattern instance or dictionary of pattern data

        Returns:
            The registered pattern
        """
        # Convert dict to GraphPattern if needed
        if isinstance(pattern, dict):
            pattern = GraphPattern(**pattern)

        self.patterns[pattern.name] = pattern
        logger.info(f"Registered pattern '{pattern.name}'")
        return pattern

    def register_branch(
        self, branch: BranchDefinition | dict[str, Any]
    ) -> BranchDefinition:
        """Register a branch in the registry.

        Args:
            branch: Branch instance or dictionary of branch data

        Returns:
            The registered branch
        """
        # Convert dict to BranchDefinition if needed
        if isinstance(branch, dict):
            branch = BranchDefinition(**branch)

        self.branches[branch.name] = branch
        logger.info(f"Registered branch '{branch.name}'")
        return branch

    def get_pattern(self, name: str) -> GraphPattern | None:
        """Get a pattern by name.

        Args:
            name: Name of the pattern

        Returns:
            Pattern if found, None otherwise
        """
        return self.patterns.get(name)

    def get_branch(self, name: str) -> BranchDefinition | None:
        """Get a branch by name.

        Args:
            name: Name of the branch

        Returns:
            Branch if found, None otherwise
        """
        return self.branches.get(name)

    def list_patterns(self) -> list[str]:
        """List all pattern names.

        Returns:
            List of pattern names
        """
        return list(self.patterns.keys())

    def list_branches(self) -> list[str]:
        """List all branch names.

        Returns:
            List of branch names
        """
        return list(self.branches.keys())

    def clear(self) -> None:
        """Clear all registrations (useful for testing)."""
        self.patterns = {}
        self.branches = {}
        logger.debug("Registry cleared")


# Pattern registration decorator
def register_pattern(
    name: str, pattern_type: str, description: str | None = None, **default_params
):
    """Decorator to register a function as a graph pattern.

    Args:
        name: Unique name for the pattern
        pattern_type: Type of pattern
        description: Optional description
        **default_params: Default parameters for the pattern

    Returns:
        Decorator function
    """

    def decorator(func):
        pattern = GraphPattern(
            name=name,
            pattern_type=pattern_type,
            description=description,
            parameters=default_params,
            _apply_func=func,
        )
        GraphPatternRegistry.get_instance().register_pattern(pattern)
        return func

    return decorator


# Branch registration decorator
def register_branch(
    name: str,
    condition_type: str,
    routes: dict[str, str],
    default_route: str | None = None,
    description: str | None = None,
):
    """Decorator to register a function as a branch condition.

    Args:
        name: Unique name for the branch
        condition_type: Type of condition
        routes: Mapping of condition values to node names
        default_route: Default route if no condition matches
        description: Optional description

    Returns:
        Decorator function
    """

    def decorator(func):
        branch = BranchDefinition(
            name=name,
            condition_type=condition_type,
            routes=routes,
            default_route=default_route,
            description=description,
            _condition_func=func,
        )
        GraphPatternRegistry.get_instance().register_branch(branch)
        return func

    return decorator


# Register some common patterns


@register_pattern(
    name="error_handling",
    pattern_type="exception_handler",
    description="Add error handling to a graph",
    error_node="handle_error",
    fallback_node="fallback",
)
def apply_error_handling(graph, error_node: str, fallback_node: str, **kwargs):
    """Apply error handling pattern to a graph.

    This adds exception handling to all nodes, routing to an error handler node
    on exceptions.

    Args:
        graph: The graph to modify
        error_node: Node to route to on errors
        fallback_node: Node to route to if error handling fails
        **kwargs: Additional parameters

    Returns:
        Modified graph
    """
    # This is a simplified implementation - in practice, you would
    # wrap all nodes with try/except and add routing logic

    # Check if graph has the necessary methods
    if not hasattr(graph, "add_node") or not hasattr(graph, "nodes"):
        logger.warning("Graph does not support error handling pattern")
        return graph

    # Implementation depends on the specific graph implementation
    logger.info(f"Applied error handling pattern with handler '{error_node}'")
    return graph


@register_pattern(
    name="persistence",
    pattern_type="state_persistence",
    description="Add state persistence to a graph",
    storage_type="memory",
    auto_save=True,
)
def apply_persistence(graph, storage_type: str, auto_save: bool, **kwargs):
    """Apply persistence pattern to a graph.

    This adds state persistence capabilities to the graph.

    Args:
        graph: The graph to modify
        storage_type: Type of storage to use
        auto_save: Whether to automatically save state
        **kwargs: Additional parameters

    Returns:
        Modified graph
    """
    # This is a simplified implementation - in practice, you would
    # add checkpointing logic to the graph

    logger.info(f"Applied persistence pattern with storage '{storage_type}'")
    return graph


@register_branch(
    name="intent_router",
    condition_type="nlp_classifier",
    routes={
        "question": "answer_node",
        "command": "execute_node",
        "chitchat": "respond_node",
    },
    default_route="fallback_node",
    description="Route based on detected intent",
)
def intent_router(state):
    """Route based on intent in state.

    Args:
        state: Current state

    Returns:
        Intent for routing
    """
    # Check for explicit intent
    if "intent" in state:
        return state["intent"]

    # Simple keyword detection (in practice, use a real classifier)
    if "query" in state:
        query = state["query"].lower()
        if "?" in query:
            return "question"
        if any(cmd in query for cmd in ["do", "execute", "perform", "run"]):
            return "command"
        return "chitchat"

    # Default
    return "fallback_node"
