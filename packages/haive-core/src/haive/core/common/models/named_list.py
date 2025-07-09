# ============================================================================
# NAMED LIST TYPE
# ============================================================================

from typing import (
    Any,
    Dict,
    Generic,
    Iterator,
    List,
    Optional,
    Sequence,
    TypeVar,
    Union,
    get_args,
    get_origin,
)

from pydantic import BaseModel, Field, field_validator, model_validator
from pydantic._internal._typing_extra import eval_type_lenient

T = TypeVar("T")


class NamedList(BaseModel, Generic[T]):
    """
    A list that can contain instances, string references, or mixed.

    Supports multiple input formats:
    - [instance1, instance2] - direct instances
    - ["name1", "name2"] - string references
    - {"name1": instance1, "name2": "ref2"} - mixed dict
    - [instance1, "ref2", instance3] - mixed list

    Automatically resolves string references to actual instances.
    """

    items: Sequence[T] = Field(default_factory=list, description="The resolved items")
    names: List[str] = Field(
        default_factory=list, description="Names of items (in order)"
    )
    name_map: Dict[str, T] = Field(
        default_factory=dict, description="Name to instance mapping"
    )

    # Reference resolution
    registry: Optional[Dict[str, T]] = Field(
        default=None, exclude=True, description="Registry for resolving references"
    )
    allow_unresolved: bool = Field(
        default=False, description="Allow unresolved references"
    )

    # Track what needs resolution
    unresolved_refs: List[str] = Field(default_factory=list, exclude=True)
    input_format: str = Field(default="list", exclude=True)

    @field_validator("items", mode="before")
    @classmethod
    def validate_items(cls, v, info):
        """Handle various input formats and normalize to instances."""
        if v is None:
            return []

        # Store original for processing in model_validator
        return v

    @model_validator(mode="after")
    def process_input(self):
        """Process the input and resolve references."""
        if not self.items:
            return self

        # Determine input format and process accordingly
        original_items = self.items

        # Reset collections
        self.items = []
        self.names = []
        self.name_map = {}
        self.unresolved_refs = []

        if isinstance(original_items, dict):
            self.process_dict_input(original_items)
        elif isinstance(original_items, (list, tuple)):
            self.process_list_input(original_items)
        else:
            # Single item
            self.process_single_item(original_items, "item_0")

        # Resolve any string references
        self.resolve_references()

        return self

    def process_dict_input(self, items_dict: Dict[str, Union[T, str]]) -> None:
        """Process dictionary input format."""
        self.input_format = "dict"

        for name, item in items_dict.items():
            if isinstance(item, str):
                # String reference - store for later resolution
                self.unresolved_refs.append(item)
                self.names.append(name)
                # Placeholder for now
                self.items.append(None)
            else:
                # Actual instance
                self.items.append(item)
                self.names.append(name)
                self.name_map[name] = item

    def process_list_input(self, items_list: Sequence[Union[T, str]]) -> None:
        """Process list/tuple input format."""
        self.input_format = "list"

        for i, item in enumerate(items_list):
            if isinstance(item, str):
                # String reference
                self.unresolved_refs.append(item)
                name = item  # Use the reference as the name
                self.names.append(name)
                self.items.append(None)  # Placeholder
            else:
                # Actual instance - generate name
                name = self.generate_name(item, i)
                self.items.append(item)
                self.names.append(name)
                self.name_map[name] = item

    def process_single_item(self, item: Union[T, str], default_name: str) -> None:
        """Process single item input."""
        if isinstance(item, str):
            self.unresolved_refs.append(item)
            self.names.append(item)
            self.items.append(None)
        else:
            name = self.generate_name(item, 0)
            self.items.append(item)
            self.names.append(name)
            self.name_map[name] = item

    def generate_name(self, item: T, index: int) -> str:
        """Generate a name for an item."""
        # Try to get name from item
        if hasattr(item, "name") and item.name:
            return str(item.name)
        elif hasattr(item, "id") and item.id:
            return str(item.id)
        elif hasattr(item, "__name__"):
            return item.__name__
        else:
            # Fallback to class name + index
            class_name = item.__class__.__name__.lower()
            return f"{class_name}_{index}"

    def resolve_references(self) -> None:
        """Resolve string references to actual instances."""
        if not self.unresolved_refs or not self.registry:
            if self.unresolved_refs and not self.allow_unresolved:
                raise ValueError(
                    f"Unresolved references: {self.unresolved_refs} (no registry provided)"
                )
            return

        # Resolve each reference
        for i, item in enumerate(self.items):
            if item is None and i < len(self.unresolved_refs):
                ref_name = (
                    self.unresolved_refs[i]
                    if i < len(self.unresolved_refs)
                    else self.names[i]
                )

                if ref_name in self.registry:
                    resolved_item = self.registry[ref_name]
                    self.items[i] = resolved_item
                    self.name_map[self.names[i]] = resolved_item
                elif not self.allow_unresolved:
                    raise ValueError(f"Could not resolve reference: '{ref_name}'")

        # Clear unresolved refs for successfully resolved items
        self.unresolved_refs = [
            ref
            for i, ref in enumerate(self.unresolved_refs)
            if i < len(self.items) and self.items[i] is None
        ]

    def set_registry(self, registry: Dict[str, T]) -> "NamedList[T]":
        """Set the registry for resolving references and attempt resolution."""
        self.registry = registry
        self.resolve_references()
        return self

    def resolve_with_registry(self, registry: Dict[str, T]) -> "NamedList[T]":
        """Resolve references using provided registry (convenience method)."""
        return self.set_registry(registry)

    # ========================================================================
    # LIST-LIKE INTERFACE
    # ========================================================================

    def __len__(self) -> int:
        return len([item for item in self.items if item is not None])

    def __iter__(self) -> Iterator[T]:
        return iter([item for item in self.items if item is not None])

    def __getitem__(self, key: Union[int, str]) -> T:
        if isinstance(key, str):
            # Access by name
            if key in self.name_map:
                return self.name_map[key]
            raise KeyError(f"No item with name '{key}'")
        else:
            # Access by index (skip None items)
            valid_items = [item for item in self.items if item is not None]
            return valid_items[key]

    def __setitem__(self, key: Union[int, str], value: T) -> None:
        if isinstance(key, str):
            # Set by name
            if key in self.names:
                index = self.names.index(key)
                self.items[index] = value
                self.name_map[key] = value
            else:
                # Add new item
                self.append(value, name=key)
        else:
            # Set by index
            valid_indices = [i for i, item in enumerate(self.items) if item is not None]
            if 0 <= key < len(valid_indices):
                actual_index = valid_indices[key]
                self.items[actual_index] = value
                name = self.names[actual_index]
                self.name_map[name] = value

    def append(self, item: T, name: Optional[str] = None) -> None:
        """Add an item to the list."""
        if name is None:
            name = self._generate_name(item, len(self.items))

        self.items.append(item)
        self.names.append(name)
        self.name_map[name] = item

    def remove(self, item: Union[T, str]) -> None:
        """Remove an item by instance or name."""
        if isinstance(item, str):
            # Remove by name
            if item in self.name_map:
                instance = self.name_map[item]
                index = self.names.index(item)
                del self.items[index]
                del self.names[index]
                del self.name_map[item]
            else:
                raise ValueError(f"No item with name '{item}'")
        else:
            # Remove by instance
            try:
                index = self.items.index(item)
                name = self.names[index]
                del self.items[index]
                del self.names[index]
                del self.name_map[name]
            except ValueError:
                raise ValueError("Item not in list")

    def get(self, name: str, default: Optional[T] = None) -> Optional[T]:
        """Get item by name with default."""
        return self.name_map.get(name, default)

    def keys(self) -> List[str]:
        """Get all names."""
        return [name for i, name in enumerate(self.names) if self.items[i] is not None]

    def values(self) -> List[T]:
        """Get all instances."""
        return [item for item in self.items if item is not None]

    def to_dict(self) -> Dict[str, T]:
        """Convert to dictionary mapping names to instances."""
        return {name: item for name, item in self.name_map.items() if item is not None}

    def to_list(self) -> List[T]:
        """Convert to simple list of instances."""
        return self.values()

    def has_unresolved_references(self) -> bool:
        """Check if there are unresolved references."""
        return len(self.unresolved_refs) > 0 or any(item is None for item in self.items)

    def get_unresolved_references(self) -> List[str]:
        """Get list of unresolved references."""
        return self.unresolved_refs.copy()

    # ========================================================================
    # PYDANTIC INTEGRATION
    # ========================================================================

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        """Custom Pydantic core schema for validation."""
        from pydantic_core import core_schema

        # Accept various input formats
        return core_schema.no_info_before_validator_function(
            cls.validate_input, handler(source_type)
        )

    @classmethod
    def validate_input(cls, v):
        """Validate input for Pydantic."""
        if isinstance(v, cls):
            return v

        # Create new instance with the input
        return cls(items=v)

    def __repr__(self) -> str:
        resolved_count = len(self.values())
        total_count = len(self.items)
        unresolved = self.get_unresolved_references()

        if unresolved:
            return f"NamedList({resolved_count}/{total_count} resolved, unresolved: {unresolved})"
        else:
            return f"NamedList({self.keys()})"

    def __str__(self) -> str:
        return f"NamedList({list(self.keys())})"


# ========================================================================
# CONVENIENCE FUNCTIONS
# ========================================================================


def create_named_list(
    items: Union[List[T], Dict[str, T], T],
    registry: Optional[Dict[str, T]] = None,
    allow_unresolved: bool = False,
) -> NamedList[T]:
    """Convenience function to create a NamedList."""
    return NamedList(items=items, registry=registry, allow_unresolved=allow_unresolved)


# ========================================================================
# USAGE EXAMPLES
# ========================================================================
"""
if __name__ == "__main__":
    # Example with mock Agent class
    class MockAgent:
        def __init__(self, name: str):
            self.name = name
        def __repr__(self):
            return f"Agent({self.name})"

    # Create some agents
    rag_agent = MockAgent("rag")
    answer_agent = MockAgent("answer")
    format_agent = MockAgent("format")
    
    # Registry for resolution
    registry = {
        "rag": rag_agent,
        "answer": answer_agent,
        "format": format_agent
    }

    # Test different input formats
    print("=== List of instances ===")
    agents1 = NamedList[MockAgent](items=[rag_agent, answer_agent])
    print(f"agents1: {agents1}")
    print(f"Values: {agents1.values()}")
    print(f"Keys: {agents1.keys()}")

    print("\n=== List of references ===")
    agents2 = NamedList[MockAgent](items=["rag", "answer"], registry=registry)
    print(f"agents2: {agents2}")
    print(f"Values: {agents2.values()}")

    print("\n=== Dict format ===")
    agents3 = NamedList[MockAgent](items={"first": rag_agent, "second": "answer"}, registry=registry)
    print(f"agents3: {agents3}")
    print(f"Access by name: {agents3['first']}")

    print("\n=== Mixed format ===")
    agents4 = NamedList[MockAgent](items=[rag_agent, "answer", format_agent], registry=registry)
    print(f"agents4: {agents4}")
    print(f"Access by index: {agents4[1]}")
"""
