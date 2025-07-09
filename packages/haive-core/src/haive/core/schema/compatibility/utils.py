"""
Utility functions for the schema compatibility module.
"""

from __future__ import annotations

import difflib
import hashlib
import inspect
import json
from functools import wraps
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Set,
    Tuple,
    Type,
    TypeVar,
    Union,
)

from pydantic import BaseModel

from haive.core.schema.compatibility.types import FieldInfo, SchemaInfo

T = TypeVar("T")


def calculate_similarity(str1: str, str2: str) -> float:
    """
    Calculate similarity between two strings (0-1).

    Uses sequence matcher for basic similarity.
    """
    return difflib.SequenceMatcher(None, str1.lower(), str2.lower()).ratio()


def find_similar_fields(
    target_field: str,
    source_fields: List[str],
    threshold: float = 0.6,
) -> List[Tuple[str, float]]:
    """
    Find similar field names with scores.

    Returns list of (field_name, similarity_score) tuples.
    """
    similarities = []

    for source_field in source_fields:
        score = calculate_similarity(target_field, source_field)
        if score >= threshold:
            similarities.append((source_field, score))

    # Sort by score descending
    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities


def extract_type_name(type_hint: Type) -> str:
    """Extract a readable name from a type hint."""
    if hasattr(type_hint, "__name__"):
        return type_hint.__name__

    # Handle generic types
    if hasattr(type_hint, "__origin__"):
        origin = type_hint.__origin__
        args = getattr(type_hint, "__args__", ())

        origin_name = getattr(origin, "__name__", str(origin))
        if args:
            arg_names = [extract_type_name(arg) for arg in args]
            return f"{origin_name}[{', '.join(arg_names)}]"
        return origin_name

    # Fallback to string representation
    return str(type_hint).replace("typing.", "")


def generate_schema_hash(schema: Union[Type[BaseModel], SchemaInfo]) -> str:
    """Generate a hash for schema comparison."""
    if isinstance(schema, type) and issubclass(schema, BaseModel):
        # Hash based on fields
        field_data = []
        for name, field in schema.model_fields.items():
            field_data.append(
                {
                    "name": name,
                    "type": extract_type_name(field.annotation),
                    "required": field.is_required(),
                }
            )
        data_str = json.dumps(field_data, sort_keys=True)
    else:
        # SchemaInfo
        field_data = []
        for name, field in schema.fields.items():
            field_data.append(
                {
                    "name": name,
                    "type": extract_type_name(field.type_info.type_hint),
                    "required": field.is_required,
                }
            )
        data_str = json.dumps(field_data, sort_keys=True)

    return hashlib.md5(data_str.encode()).hexdigest()


def flatten_nested_dict(
    data: Dict[str, Any],
    parent_key: str = "",
    separator: str = ".",
) -> Dict[str, Any]:
    """
    Flatten nested dictionary.

    Example:
        {"user": {"name": "John", "age": 30}}
        becomes
        {"user.name": "John", "user.age": 30}
    """
    items = []

    for key, value in data.items():
        new_key = f"{parent_key}{separator}{key}" if parent_key else key

        if isinstance(value, dict):
            items.extend(flatten_nested_dict(value, new_key, separator).items())
        else:
            items.append((new_key, value))

    return dict(items)


def unflatten_dict(
    data: Dict[str, Any],
    separator: str = ".",
) -> Dict[str, Any]:
    """
    Unflatten a dictionary.

    Example:
        {"user.name": "John", "user.age": 30}
        becomes
        {"user": {"name": "John", "age": 30}}
    """
    result = {}

    for key, value in data.items():
        parts = key.split(separator)
        current = result

        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]

        current[parts[-1]] = value

    return result


def extract_path_value(
    data: Dict[str, Any],
    path: str,
    separator: str = ".",
    default: Any = None,
) -> Any:
    """
    Extract value from nested dict using path.

    Supports:
    - Dot notation: "user.profile.name"
    - Array indices: "items[0].name"
    - Wildcards: "items[*].name"
    """
    if not path:
        return data

    # Handle array notation
    import re

    array_pattern = re.compile(r"(\w+)\[(\d+|\*)\]")

    parts = path.split(separator)
    current = data

    for part in parts:
        if current is None:
            return default

        # Check for array access
        match = array_pattern.match(part)
        if match:
            field_name = match.group(1)
            index = match.group(2)

            if isinstance(current, dict) and field_name in current:
                array = current[field_name]
                if isinstance(array, list):
                    if index == "*":
                        # Return all items
                        return [
                            extract_path_value(
                                item, separator.join(parts[parts.index(part) + 1 :])
                            )
                            for item in array
                        ]
                    else:
                        idx = int(index)
                        if 0 <= idx < len(array):
                            current = array[idx]
                        else:
                            return default
                else:
                    return default
            else:
                return default
        else:
            # Normal field access
            if isinstance(current, dict):
                current = current.get(part, default)
            elif hasattr(current, part):
                current = getattr(current, part, default)
            else:
                return default

    return current


def merge_dicts(
    *dicts: Dict[str, Any],
    deep: bool = True,
    list_strategy: str = "extend",
) -> Dict[str, Any]:
    """
    Merge multiple dictionaries.

    Args:
        *dicts: Dictionaries to merge
        deep: Whether to deep merge nested dicts
        list_strategy: How to handle lists ("extend", "replace", "unique")
    """
    result = {}

    for d in dicts:
        for key, value in d.items():
            if key in result and deep:
                # Handle nested merge
                if isinstance(result[key], dict) and isinstance(value, dict):
                    result[key] = merge_dicts(result[key], value, deep=True)
                elif isinstance(result[key], list) and isinstance(value, list):
                    if list_strategy == "extend":
                        result[key].extend(value)
                    elif list_strategy == "replace":
                        result[key] = value
                    elif list_strategy == "unique":
                        result[key] = list(set(result[key] + value))
                else:
                    result[key] = value
            else:
                result[key] = value

    return result


def create_schema_diff(
    schema1: SchemaInfo,
    schema2: SchemaInfo,
) -> Dict[str, Any]:
    """
    Create a diff between two schemas.

    Returns dict with:
    - added_fields: Fields in schema2 but not schema1
    - removed_fields: Fields in schema1 but not schema2
    - modified_fields: Fields with different types/properties
    - unchanged_fields: Fields that are the same
    """
    diff = {
        "added_fields": {},
        "removed_fields": {},
        "modified_fields": {},
        "unchanged_fields": [],
    }

    schema1_fields = set(schema1.fields.keys())
    schema2_fields = set(schema2.fields.keys())

    # Added fields
    for field in schema2_fields - schema1_fields:
        diff["added_fields"][field] = {
            "type": extract_type_name(schema2.fields[field].type_info.type_hint),
            "required": schema2.fields[field].is_required,
        }

    # Removed fields
    for field in schema1_fields - schema2_fields:
        diff["removed_fields"][field] = {
            "type": extract_type_name(schema1.fields[field].type_info.type_hint),
            "required": schema1.fields[field].is_required,
        }

    # Check common fields
    for field in schema1_fields & schema2_fields:
        field1 = schema1.fields[field]
        field2 = schema2.fields[field]

        changes = {}

        # Check type
        if field1.type_info.type_hint != field2.type_info.type_hint:
            changes["type"] = {
                "from": extract_type_name(field1.type_info.type_hint),
                "to": extract_type_name(field2.type_info.type_hint),
            }

        # Check required
        if field1.is_required != field2.is_required:
            changes["required"] = {
                "from": field1.is_required,
                "to": field2.is_required,
            }

        # Check default
        if field1.default_value != field2.default_value:
            changes["default"] = {
                "from": field1.default_value,
                "to": field2.default_value,
            }

        if changes:
            diff["modified_fields"][field] = changes
        else:
            diff["unchanged_fields"].append(field)

    return diff


def memoize(func: Callable[..., T]) -> Callable[..., T]:
    """Simple memoization decorator."""
    cache = {}

    @wraps(func)
    def wrapper(*args, **kwargs):
        # Create cache key
        key = (args, tuple(sorted(kwargs.items())))

        if key not in cache:
            cache[key] = func(*args, **kwargs)

        return cache[key]

    wrapper.cache = cache
    wrapper.clear_cache = cache.clear

    return wrapper


def get_all_subclasses(cls: Type) -> Set[Type]:
    """Get all subclasses of a class recursively."""
    subclasses = set()

    for subclass in cls.__subclasses__():
        subclasses.add(subclass)
        subclasses.update(get_all_subclasses(subclass))

    return subclasses


def format_type_path(types: List[Type]) -> str:
    """Format a type conversion path for display."""
    names = [extract_type_name(t) for t in types]
    return " → ".join(names)


def validate_field_name(name: str) -> bool:
    """Validate that a field name is valid Python identifier."""
    return name.isidentifier() and not name.startswith("_")


def suggest_field_name(invalid_name: str) -> str:
    """Suggest a valid field name from invalid one."""
    # Replace invalid characters
    import re

    # Replace non-alphanumeric with underscore
    suggested = re.sub(r"[^a-zA-Z0-9_]", "_", invalid_name)

    # Ensure doesn't start with number
    if suggested and suggested[0].isdigit():
        suggested = f"field_{suggested}"

    # Ensure not empty
    if not suggested:
        suggested = "field"

    # Avoid Python keywords
    import keyword

    if keyword.iskeyword(suggested):
        suggested = f"{suggested}_field"

    return suggested


def create_example_value(type_hint: Type) -> Any:
    """Create an example value for a type hint."""
    # Handle common types
    if type_hint == str:
        return "example"
    elif type_hint == int:
        return 42
    elif type_hint == float:
        return 3.14
    elif type_hint == bool:
        return True
    elif type_hint == list or getattr(type_hint, "__origin__", None) == list:
        return []
    elif type_hint == dict or getattr(type_hint, "__origin__", None) == dict:
        return {}
    elif type_hint == set or getattr(type_hint, "__origin__", None) == set:
        return set()
    elif hasattr(type_hint, "__origin__") and type_hint.__origin__ == Union:
        # For Optional, return None
        args = type_hint.__args__
        if type(None) in args:
            return None
        # Otherwise return example of first type
        return create_example_value(args[0])
    else:
        # For classes, try to instantiate
        try:
            if inspect.isclass(type_hint):
                return type_hint()
        except:
            pass

        return None


def estimate_memory_usage(schema: SchemaInfo) -> int:
    """Estimate memory usage of a schema instance in bytes."""
    # Base overhead
    overhead = 100

    # Add per-field estimates
    field_size = 0
    for field in schema.fields.values():
        type_hint = field.type_info.type_hint

        # Estimate based on type
        if type_hint == str:
            field_size += 50  # Average string
        elif type_hint == int:
            field_size += 28  # PyLong overhead
        elif type_hint == float:
            field_size += 24  # PyFloat
        elif type_hint == bool:
            field_size += 28  # PyBool
        elif type_hint == list or getattr(type_hint, "__origin__", None) == list:
            field_size += 88  # Empty list overhead
        elif type_hint == dict or getattr(type_hint, "__origin__", None) == dict:
            field_size += 280  # Empty dict overhead
        else:
            field_size += 50  # Generic estimate

    return overhead + field_size
