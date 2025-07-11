from collections.abc import Iterable
from typing import Any, Dict, Generic, List, Optional, TypeVar, Union

from pydantic import BaseModel, Field, model_validator

from haive.core.common.mixins.getter_mixin import GetterMixin

T = TypeVar("T")


class NamedDict(BaseModel, Generic[T], GetterMixin[T]):
    """A dictionary that automatically builds keys from object names.

    This class combines dictionary-like access with attributes extraction
    and rich lookup capabilities from GetterMixin.
    """

    values: dict[str, T] = Field(default_factory=dict)
    name_attrs: list[str] = Field(default=["name", "__name__"])

    model_config = {"arbitrary_types_allowed": True}

    @model_validator(mode="before")
    @classmethod
    def convert_input(cls, data: Any) -> Any:
        """Process input data into the expected format."""
        # Already a dictionary with values
        if isinstance(data, dict) and "values" in data:
            return data

        # Plain dictionary without 'values'
        if isinstance(data, dict) and "values" not in data:
            return {"values": data}

        # Convert list/iterable to dictionary
        if isinstance(data, list | tuple | set):
            # Get name attributes from data if available
            name_attrs = (
                data.get("name_attrs", ["name", "__name__"])
                if isinstance(data, dict)
                else ["name", "__name__"]
            )

            # Convert each item to name-based entry
            result = {}
            for item in data:
                # Extract key from object
                key = cls._extract_key(item, name_attrs)

                # If key found, add to result
                if key:
                    result[key] = item

            return {"values": result}

        return data

    @staticmethod
    def _extract_key(obj: Any, attrs: list[str]) -> str | None:
        """Extract a key from an object using the specified attributes.

        Args:
            obj: Object to extract key from
            attrs: Attribute names to try

        Returns:
            Extracted key as string or None if no key found
        """
        # Handle direct string value
        if isinstance(obj, str):
            return obj

        # Dictionary lookup
        if isinstance(obj, dict):
            for attr in attrs:
                if attr in obj:
                    return str(obj[attr])
            return None

        # Object attribute lookup
        for attr in attrs:
            if hasattr(obj, attr):
                value = getattr(obj, attr)
                # Skip methods (but allow __name__)
                if callable(value) and attr != "__name__":
                    continue
                return str(value)

        return None

    # Dictionary-like access methods
    def __getitem__(self, key: str) -> T:
        """Get item by key."""
        return self.values[key]

    def __setitem__(self, key: str, value: T) -> None:
        """Set item by key."""
        self.values[key] = value

    def __delitem__(self, key: str) -> None:
        """Delete item by key."""
        del self.values[key]

    def __contains__(self, key: str) -> bool:
        """Check if key exists."""
        return key in self.values

    def __len__(self) -> int:
        """Get number of items."""
        return len(self.values)

    def __iter__(self):
        """Iterate through values."""
        return iter(self.values.values())

    # Implement GetterMixin abstract method
    def _get_items(self) -> list[T]:
        """Get all items in the dictionary."""
        return list(self.values.values())

    # Enhanced accessor methods
    def get(self, key: str, default: Any = None) -> Any:
        """Get an item with a default value."""
        if key in self.values:
            return self.values[key]
        return default

    def add(self, item: T, key: str | None = None) -> str:
        """Add an item with automatic or explicit key.

        Args:
            item: Item to add
            key: Optional explicit key

        Returns:
            Key used to store the item
        """
        if key is None:
            # Try to extract key
            key = self._extract_key(item, self.name_attrs)

            # If no key found, generate UUID
            if not key:
                import uuid

                key = str(uuid.uuid4())

        self.values[key] = item
        return key

    def update(self, items: dict[str, T] | Iterable[T]) -> None:
        """Update with dictionary or iterable.

        Args:
            items: Dictionary or iterable of items to add
        """
        if isinstance(items, dict):
            self.values.update(items)
        else:
            for item in items:
                self.add(item)

    def keys(self) -> list[str]:
        """Get all keys."""
        return list(self.values.keys())

    def items(self):
        """Get all key-value pairs."""
        return self.values.items()

    def values_list(self) -> list[T]:
        """Get all values as a list."""
        return list(self.values.values())

    def pop(self, key: str, default: Any = None) -> Any:
        """Remove and return an item with default value."""
        return self.values.pop(key, default)

    def clear(self) -> None:
        """Clear all items."""
        self.values.clear()

    # Attribute access
    def __getattr__(self, name: str) -> Any:
        """Allow attribute access for keys.

        Also supports dynamic get_by_X methods.
        """
        if name in self.values:
            return self.values[name]

        # Dynamic get_by_X methods
        if name.startswith("get_by_"):
            attr_name = name[7:]  # Remove "get_by_"

            def getter_method(value, default=None):
                return self.get_by_attr(attr_name, value, default)

            return getter_method

        raise AttributeError(f"{self.__class__.__name__} has no attribute '{name}'")

    def to_dict(self) -> dict[str, T]:
        """Convert to plain dictionary."""
        return dict(self.values)
