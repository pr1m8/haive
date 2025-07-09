"""State graph registry for managing graph model instances.

This module provides a singleton registry for managing state graph models
in the Haive framework.
"""
from typing import Any, ClassVar, Dict, List, Optional

from haive.core.graph.models.graph_model import GraphModel
from haive.core.registry.base import AbstractRegistry


class GraphRegistry(AbstractRegistry[GraphModel]):
    """Singleton registry for managing state graph models.

    This registry provides centralized management of GraphModel instances,
    allowing registration, retrieval, and lifecycle management of graph models
    throughout the application.

    Example:
        >>> registry = GraphRegistry.get_instance()
        >>> graph = GraphModel(name="my_graph", id="graph_123")
        >>> registry.register(graph)
        >>> retrieved = registry.get(None, "my_graph")
    """

    _instance: ClassVar[Optional["GraphRegistry"]] = None

    @classmethod
    def get_instance(cls) -> "GraphRegistry":
        """Get the singleton instance of the registry.

        Returns:
            GraphRegistry: The singleton instance.
        """
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        """Initialize the registry with empty graph collections."""
        self.graphs: Dict[str, GraphModel] = {}
        self.graph_ids: Dict[str, GraphModel] = {}

    def register(self, item: GraphModel) -> GraphModel:
        """Register a graph model in the registry.

        Args:
            item: The GraphModel instance to register.

        Returns:
            GraphModel: The registered graph model.
        """
        self.graphs[item.name] = item
        self.graph_ids[item.id] = item
        return item

    def get(self, item_type: Any, name: str) -> Optional[GraphModel]:
        """Get a graph model by name.

        Args:
            item_type: Not used in this implementation.
            name: The name of the graph to retrieve.

        Returns:
            Optional[GraphModel]: The graph model if found, None otherwise.
        """
        return self.graphs.get(name)

    def find_by_id(self, id: str) -> Optional[GraphModel]:
        """Find a graph model by its unique identifier.

        Args:
            id: The unique identifier of the graph.

        Returns:
            Optional[GraphModel]: The graph model if found, None otherwise.
        """
        return self.graph_ids.get(id)

    def list(self, item_type: Any) -> List[str]:
        """List all registered graph names.

        Args:
            item_type: Not used in this implementation.

        Returns:
            List[str]: List of all graph names.
        """
        return list(self.graphs.keys())

    def get_all(self, item_type: Any) -> Dict[str, GraphModel]:
        """Get all registered graph models.

        Args:
            item_type: Not used in this implementation.

        Returns:
            Dict[str, GraphModel]: Dictionary of all graph models by name.
        """
        return self.graphs

    def clear(self) -> None:
        """Clear all registered graph models from the registry.""\
        self.graphs.clear()
        self.graph_ids.clear()
