# src/haive/core/registry/memory.py

import logging
from typing import Dict, List, Optional, TypeVar

from haive.core.engine.base import Engine
from haive.core.engine.base.types import EngineType
from haive.core.registry.base import AbstractRegistry

E = TypeVar("E", bound=Engine)


class MemoryRegistry(AbstractRegistry[E]):
    """In-memory implementation of the registry."""

    def __init__(self):
        """Initialize the registry."""
        self.engines = {engine_type: {} for engine_type in EngineType}
        self.engine_ids = {}  # id -> engine mapping

    def register(self, engine: E) -> E:
        """Register an engine in the registry."""
        self.engines[engine.engine_type][engine.name] = engine
        self.engine_ids[engine.id] = engine
        logging.debug(
            f"Registered engine {engine.name} (id: {engine.id}) of type {engine.engine_type}"
        )
        return engine

    def get(self, engine_type: EngineType, name: str) -> Optional[E]:
        """Get an engine by type and name."""
        return self.engines[engine_type].get(name)

    def find_by_id(self, id: str) -> Optional[E]:
        """Find an engine by ID."""
        return self.engine_ids.get(id)

    def find(self, name_or_id: str) -> Optional[E]:
        """Find an engine by name or ID across all engine types."""
        # Check ID first (faster lookup)
        if engine := self.engine_ids.get(name_or_id):
            return engine

        # Search through all engine types by name
        for engine_type in EngineType:
            if engine := self.get(engine_type, name_or_id):
                return engine

        return None

    def list(self, engine_type: EngineType) -> List[str]:
        """List all engines of a type."""
        return list(self.engines[engine_type].keys())

    def get_all(self, engine_type: EngineType) -> Dict[str, E]:
        """Get all engines of a type."""
        return self.engines[engine_type]

    def clear(self) -> None:
        """Clear the registry."""
        self.engines = {engine_type: {} for engine_type in EngineType}
        self.engine_ids = {}
