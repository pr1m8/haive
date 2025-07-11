"""Utility functions for working with branches."""

import inspect
import logging
import re
from typing import Any, Set

logger = logging.getLogger(__name__)


def extract_field(state: Any, field_path: str) -> Any:
    """Extract a field value from state using a path.

    Supports:
    - Simple keys: "fieldname"
    - Nested paths: "nested.field.path"
    - Array indexing: "array.0.field"
    - Special paths: "messages.last.content"

    Args:
        state: State object
        field_path: Path to the field

    Returns:
        Extracted value or None if not found
    """
    if field_path is None:
        return None

    # Handle special keys
    if field_path == "messages.last.content":
        messages = get_field_value(state, "messages")
        if not messages or not isinstance(messages, list | tuple) or not messages:
            return None
        last_message = messages[-1]
        return get_field_value(last_message, "content")

    # Handle dot notation
    if "." in field_path:
        parts = field_path.split(".")
        current = state

        for part in parts:
            # Try to convert numeric indices
            if part.isdigit():
                part = int(part)
            elif part == "last" and isinstance(current, list | tuple) and current:
                part = -1

            # Get next level
            current = get_field_value(current, part)
            if current is None:
                return None

        return current

    # Simple key
    return get_field_value(state, field_path)


def get_field_value(obj: Any, key: Any) -> Any:
    """Get a field value using various access methods.

    Args:
        obj: Object to extract from
        key: Key or index to extract

    Returns:
        Extracted value or None if not found
    """
    # Handle indexing for lists and tuples
    if isinstance(obj, list | tuple):
        try:
            if isinstance(key, int) and (
                0 <= key < len(obj) or (key < 0 and abs(key) <= len(obj))
            ):
                return obj[key]
        except (IndexError, TypeError):
            return None

    # Try attribute access (for objects and Pydantic models)
    if hasattr(obj, key):
        return getattr(obj, key)

    # Try dictionary access
    try:
        return obj[key]
    except (KeyError, TypeError, AttributeError):
        pass

    # Try get method for dictionaries
    if hasattr(obj, "get") and callable(obj.get):
        try:
            return obj.get(key)
        except Exception:
            pass

    return None


def extract_fields_from_function(func: callable) -> set[str]:
    """Extract field references from a function.

    Args:
        func: Function to analyze

    Returns:
        Set of field names referenced
    """
    fields = set()

    if not func:
        return fields

    try:
        source = inspect.getsource(func)
        # Look for state["field"] or state.field patterns
        dict_refs = re.findall(r'state\[[\'"]([\w]+)[\'"]', source)
        attr_refs = re.findall(r"state\.([\w]+)", source)

        fields.update(dict_refs)
        fields.update(attr_refs)
    except (OSError, TypeError):
        pass

    return fields


def extract_base_field(field_path: str) -> str:
    """Extract the base field from a path."""
    if not field_path:
        return field_path
    return field_path.split(".")[0] if "." in field_path else field_path
