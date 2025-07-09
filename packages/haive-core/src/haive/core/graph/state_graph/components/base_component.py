"""Base component interface for BaseGraph modular architecture.

This module provides the abstract base class that all BaseGraph components
must inherit from, ensuring consistent interfaces and proper lifecycle management.
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Dict, Optional

if TYPE_CHECKING:
    from haive.core.graph.state_graph.base_graph2 import BaseGraph


class BaseGraphComponent(ABC):
    """Abstract base class for all BaseGraph components.

    This class provides the foundation for all modular components in the BaseGraph
    architecture, following composition-over-inheritance principles from the coding
    style guide.

    Args:
        graph: Reference to the parent BaseGraph instance

    Attributes:
        graph: The parent BaseGraph instance
        component_name: Unique identifier for this component type

    Example:
        Creating a custom component::

            class MyCustomComponent(BaseGraphComponent):
                component_name = "custom"

                def __init__(self, graph: "BaseGraph"):
                    super().__init__(graph)
                    self._my_data = {}

                def initialize(self) -> None:
                    # Component-specific initialization
                    pass

                def cleanup(self) -> None:
                    # Component-specific cleanup
                    self._my_data.clear()
    """

    component_name: str = "base"

    def __init__(self, graph: "BaseGraph") -> None:
        """Initialize component with reference to parent graph.

        Args:
            graph: The parent BaseGraph instance

        Raises:
            ValueError: If graph is None
        """
        if graph is None:
            raise ValueError("Graph reference cannot be None")

        self._graph = graph
        self._initialized = False

    @property
    def graph(self) -> "BaseGraph":
        """Get reference to parent graph."""
        return self._graph

    @property
    def is_initialized(self) -> bool:
        """Check if component has been initialized."""
        return self._initialized

    def initialize(self) -> None:
        """Initialize the component.

        This method is called after the component is created and attached
        to the graph. Subclasses should override this method to perform
        any component-specific initialization.

        Note:
            This method should be idempotent - calling it multiple times
            should have the same effect as calling it once.
        """
        self._initialized = True

    def cleanup(self) -> None:
        """Clean up component resources.

        This method is called when the graph is being destroyed or
        when components need to be reset. Subclasses should override
        this method to perform any component-specific cleanup.
        """
        self._initialized = False

    def validate_state(self) -> list[str]:
        """Validate the component's current state.

        Returns:
            List of validation error messages. Empty list if valid.

        Note:
            Subclasses should override this method to implement
            component-specific validation logic.
        """
        errors = []

        if not self._initialized:
            errors.append(f"Component '{self.component_name}' not initialized")

        return errors

    def get_component_info(self) -> Dict[str, Any]:
        """Get component metadata and status information.

        Returns:
            Dictionary containing component information including:
            - component_name: The component's identifier
            - initialized: Whether the component is initialized
            - class_name: The component's class name

        Example:
            >>> component.get_component_info()
            {
                'component_name': 'node_manager',
                'initialized': True,
                'class_name': 'NodeManager'
            }
        """
        return {
            "component_name": self.component_name,
            "initialized": self._initialized,
            "class_name": self.__class__.__name__,
        }

    def __repr__(self) -> str:
        """String representation of the component."""
        return f"{self.__class__.__name__}(component_name='{self.component_name}', initialized={self._initialized})"


class ComponentRegistry:
    """Registry for managing graph components.

    This class manages the lifecycle and registration of all components
    in a BaseGraph instance, ensuring proper initialization order and
    cleanup.

    Example:
        Using the component registry::

            registry = ComponentRegistry()

            # Register components
            registry.register("nodes", NodeManager(graph))
            registry.register("edges", EdgeManager(graph))

            # Initialize all components
            registry.initialize_all()

            # Access components
            node_manager = registry.get("nodes")

            # Cleanup
            registry.cleanup_all()
    """

    def __init__(self) -> None:
        """Initialize empty component registry."""
        self._components: Dict[str, BaseGraphComponent] = {}
        self._initialization_order: list[str] = []

    def register(self, name: str, component: BaseGraphComponent) -> None:
        """Register a component with the registry.

        Args:
            name: Unique name for the component
            component: The component instance to register

        Raises:
            ValueError: If component name is already registered
            TypeError: If component is not a BaseGraphComponent
        """
        if name in self._components:
            raise ValueError(f"Component '{name}' already registered")

        if not isinstance(component, BaseGraphComponent):
            raise TypeError(
                f"Component must be instance of BaseGraphComponent, got {type(component)}"
            )

        self._components[name] = component
        self._initialization_order.append(name)

    def get(self, name: str) -> Optional[BaseGraphComponent]:
        """Get a registered component by name.

        Args:
            name: Name of the component to retrieve

        Returns:
            The component instance, or None if not found
        """
        return self._components.get(name)

    def get_all(self) -> Dict[str, BaseGraphComponent]:
        """Get all registered components.

        Returns:
            Dictionary mapping component names to instances
        """
        return self._components.copy()

    def initialize_all(self) -> None:
        """Initialize all registered components in order."""
        for name in self._initialization_order:
            component = self._components[name]
            if not component.is_initialized:
                component.initialize()

    def cleanup_all(self) -> None:
        """Clean up all registered components in reverse order."""
        for name in reversed(self._initialization_order):
            component = self._components[name]
            if component.is_initialized:
                component.cleanup()

    def validate_all(self) -> Dict[str, list[str]]:
        """Validate all registered components.

        Returns:
            Dictionary mapping component names to lists of validation errors
        """
        validation_results = {}

        for name, component in self._components.items():
            errors = component.validate_state()
            if errors:
                validation_results[name] = errors

        return validation_results

    def get_registry_info(self) -> Dict[str, Any]:
        """Get registry status and component information.

        Returns:
            Dictionary containing registry metadata and component info
        """
        return {
            "total_components": len(self._components),
            "initialization_order": self._initialization_order.copy(),
            "components": {
                name: component.get_component_info()
                for name, component in self._components.items()
            },
        }
