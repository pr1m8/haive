# src/haive/core/registry/base.py

from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, List, Optional, TypeVar

T = TypeVar("T")


class AbstractRegistry(ABC, Generic[T]):
    """Abstract registry for any component type."""

    @abstractmethod
    def register(self, item: T) -> T:
        """Register an item in the registry."""

    @abstractmethod
    def get(self, item_type: Any, name: str) -> T | None:
        """Get an item by type and name."""

    @abstractmethod
    def find_by_id(self, id: str) -> T | None:
        """Find an item by ID."""

    @abstractmethod
    def list(self, item_type: Any) -> list[str]:
        """List all items of a type."""

    @abstractmethod
    def get_all(self, item_type: Any) -> dict[str, T]:
        """Get all items of a type."""

    @abstractmethod
    def clear(self) -> None:
        """Clear the registry."""
