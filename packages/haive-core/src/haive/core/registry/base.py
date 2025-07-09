# src/haive/core/registry/base.py

from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, List, Optional, TypeVar

T = TypeVar("T")


class AbstractRegistry(ABC, Generic[T]):
    """Abstract registry for any component type."""

    @abstractmethod
    def register(self, item: T) -> T:
        """Register an item in the registry."""
        pass

    @abstractmethod
    def get(self, item_type: Any, name: str) -> Optional[T]:
        """Get an item by type and name."""
        pass

    @abstractmethod
    def find_by_id(self, id: str) -> Optional[T]:
        """Find an item by ID."""
        pass

    @abstractmethod
    def list(self, item_type: Any) -> List[str]:
        """List all items of a type."""
        pass

    @abstractmethod
    def get_all(self, item_type: Any) -> Dict[str, T]:
        """Get all items of a type."""
        pass

    @abstractmethod
    def clear(self) -> None:
        """Clear the registry."""
        pass
