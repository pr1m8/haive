# In haive/core/utils/serialization.py
from typing import Any


def ensure_json_serializable(data: Any) -> Any:
    """Ensure data is JSON serializable by handling special types."""
    if data is None:
        return None

    if isinstance(data, (str, int, float, bool)):
        return data

    if isinstance(data, dict):
        return {k: ensure_json_serializable(v) for k, v in data.items()}

    if isinstance(data, (list, tuple)):
        return [ensure_json_serializable(item) for item in data]

    if callable(data) and hasattr(data, "__name__"):
        # Convert functions to a serializable representation
        return {
            "__type__": "function",
            "name": data.__name__,
            "module": data.__module__,
            "doc": data.__doc__,
        }

    # For other objects, try to convert to dict if possible
    if hasattr(data, "model_dump"):
        return ensure_json_serializable(data.model_dump())

    if hasattr(data, "__dict__"):
        return ensure_json_serializable(data.__dict__)

    # Last resort: convert to string
    return str(data)
