"""
Registry management for Haive engines.

This module provides a centralized registry for all engine instances in the Haive system.
The registry allows engines to be registered, retrieved, and managed through a singleton
pattern, ensuring consistent access across the application.
"""

import logging
from typing import Dict, List, Optional

from haive.core.engine.base.base import Engine
from haive.core.engine.base.types import EngineType
from haive.core.registry.base import AbstractRegistry

logger = logging.getLogger(__name__)


class EngineRegistry(AbstractRegistry[Engine]):
    """
    Central registry for all engines in the Haive system.

    This class implements a singleton pattern to ensure a single point of access
    for all engine registrations and lookups. Engines are organized by their type
    and can be accessed by name or by their unique ID.

    Attributes:
        engines (Dict[EngineType, Dict[str, Engine]]): Nested dictionary storing
            engines by their type and name.
        engine_ids (Dict[str, Engine]): Dictionary mapping engine IDs to engine instances.
    """

    _instance = None

    @classmethod
    def get_instance(cls) -> "EngineRegistry":
        """
        Get the singleton instance of the engine registry.

        This method ensures that only one instance of the registry exists
        throughout the application lifecycle.

        Returns:
            EngineRegistry: The singleton instance of the registry.

        Examples:
            >>> registry = EngineRegistry.get_instance()
            >>> # All subsequent calls return the same instance
            >>> registry2 = EngineRegistry.get_instance()
            >>> registry is registry2
            True
        """
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        """
        Initialize the registry with empty dictionaries.

        Creates an empty registry structure with dictionaries for each engine type
        and an empty ID mapping dictionary.
        """
        self.engines = {engine_type: {} for engine_type in EngineType}
        self.engine_ids = {}  # id -> engine mapping

    def register(self, item: Engine) -> Engine:
        """
        Register an engine in the registry.

        Adds the provided engine to the registry, indexed by both its type/name
        and its unique ID.

        Args:
            item (Engine): The engine instance to register.

        Returns:
            Engine: The registered engine instance (same as input).

        Examples:
            >>> from haive.core.engine.base.base import Engine
            >>> registry = EngineRegistry.get_instance()
            >>> engine = Engine(name="my_engine", engine_type=EngineType.LLM)
            >>> registry.register(engine)
            >>> registry.find("my_engine") is engine
            True
        """
        self.engines[item.engine_type][item.name] = item
        self.engine_ids[item.id] = item
        logger.debug(
            f"Registered engine {item.name} (id: {item.id}) of type {item.engine_type}"
        )
        return item

    def get(self, item_type: EngineType, name: str) -> Optional[Engine]:
        """
        Get an engine by its type and name.

        Retrieves an engine instance from the registry using its type and name.

        Args:
            item_type (EngineType): The type of engine to retrieve.
            name (str): The name of the engine to retrieve.

        Returns:
            Optional[Engine]: The requested engine instance, or None if not found.

        Examples:
            >>> registry = EngineRegistry.get_instance()
            >>> engine = registry.get(EngineType.LLM, "gpt-4")
            >>> if engine:
            ...     print(f"Found engine: {engine.name}")
            ... else:
            ...     print("Engine not found")
        """
        return self.engines[item_type].get(name)

    def find_by_id(self, id: str) -> Optional[Engine]:
        """
        Find an engine by its unique ID.

        Retrieves an engine instance from the registry using its unique ID.

        Args:
            id (str): The unique ID of the engine to find.

        Returns:
            Optional[Engine]: The requested engine instance, or None if not found.

        Examples:
            >>> registry = EngineRegistry.get_instance()
            >>> engine = registry.find_by_id("550e8400-e29b-41d4-a716-446655440000")
            >>> if engine:
            ...     print(f"Found engine: {engine.name}")
        """
        return self.engine_ids.get(id)

    def find(self, name_or_id: str) -> Optional[Engine]:
        """
        Find an engine by name or ID across all engine types.

        Searches for an engine by first checking the ID registry (faster) and
        then searching through all engine types by name.

        Args:
            name_or_id (str): The name or ID of the engine to find.

        Returns:
            Optional[Engine]: The requested engine instance, or None if not found.

        Examples:
            >>> registry = EngineRegistry.get_instance()
            >>> # Can find by ID
            >>> engine1 = registry.find("550e8400-e29b-41d4-a716-446655440000")
            >>> # Or by name
            >>> engine2 = registry.find("gpt-4")
        """
        # Check ID first (faster lookup)
        if engine := self.engine_ids.get(name_or_id):
            return engine

        # Search through all engine types by name
        for engine_type in EngineType:
            if engine := self.get(engine_type, name_or_id):
                return engine

        return None

    def list(self, item_type: EngineType) -> List[str]:
        """
        List all engines of a specific type.

        Returns a list of names of all engines registered for the given type.

        Args:
            item_type (EngineType): The type of engines to list.

        Returns:
            List[str]: A list of engine names of the specified type.

        Examples:
            >>> registry = EngineRegistry.get_instance()
            >>> llm_engines = registry.list(EngineType.LLM)
            >>> print(f"Available LLM engines: {', '.join(llm_engines)}")
        """
        return list(self.engines[item_type].keys())

    def get_all(self, item_type: EngineType) -> Dict[str, Engine]:
        """
        Get all engines of a specific type.

        Returns a dictionary mapping names to engines for the given type.

        Args:
            item_type (EngineType): The type of engines to retrieve.

        Returns:
            Dict[str, Engine]: A dictionary of engine names to engine instances.

        Examples:
            >>> registry = EngineRegistry.get_instance()
            >>> all_llms = registry.get_all(EngineType.LLM)
            >>> for name, engine in all_llms.items():
            ...     print(f"LLM: {name}, ID: {engine.id}")
        """
        return self.engines[item_type]

    def clear(self) -> None:
        """
        Clear the registry.

        Removes all engines from the registry, resetting it to an empty state.
        Useful for testing or when reloading configurations.

        Examples:
            >>> registry = EngineRegistry.get_instance()
            >>> # After operations that registered engines
            >>> registry.clear()
            >>> assert len(registry.list(EngineType.LLM)) == 0
        """
        self.engines = {engine_type: {} for engine_type in EngineType}
        self.engine_ids = {}
