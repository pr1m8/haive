from typing import Any, ClassVar, Optional

from haive.core.registry.base import AbstractRegistry


class PatternRegistry(AbstractRegistry[PatternDefinition]):
    """Registry for graph patterns."""

    _instance: ClassVar[Optional["PatternRegistry"]] = None

    @classmethod
    def get_instance(cls) -> "PatternRegistry":
        """Get the singleton instance of the registry."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        """Initialize the registry."""
        self.patterns: dict[str, PatternDefinition] = {}
        self.pattern_ids: dict[str, PatternDefinition] = {}
        self.pattern_types: dict[str, list[str]] = {}

    def register(self, item: PatternDefinition) -> PatternDefinition:
        """Register a pattern in the registry."""
        self.patterns[item.name] = item
        self.pattern_ids[item.id] = item

        # Register by type
        if item.pattern_type not in self.pattern_types:
            self.pattern_types[item.pattern_type] = []
        self.pattern_types[item.pattern_type].append(item.name)

        return item

    def get(self, item_type: Any, name: str) -> PatternDefinition | None:
        """Get a pattern by name."""
        return self.patterns.get(name)

    def find_by_id(self, id: str) -> PatternDefinition | None:
        """Find a pattern by ID."""
        return self.pattern_ids.get(id)

    def list(self, item_type: Any) -> list[str]:
        """List all pattern names."""
        return list(self.patterns.keys())

    def get_all(self, item_type: Any) -> dict[str, PatternDefinition]:
        """Get all patterns."""
        return self.patterns

    def clear(self) -> None:
        """Clear the registry."""
        self.patterns.clear()
        self.pattern_ids.clear()
        self.pattern_types.clear()

    def list_by_type(self, pattern_type: str) -> builtins.list[str]:
        """List patterns of a specific type."""
        return self.pattern_types.get(pattern_type, [])

    def get_by_type(self, pattern_type: str) -> dict[str, PatternDefinition]:
        """Get all patterns of a specific type."""
        return {
            name: self.patterns[name]
            for name in self.pattern_types.get(pattern_type, [])
        }
