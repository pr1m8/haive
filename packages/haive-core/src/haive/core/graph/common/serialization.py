"""
Utilities for serialization and deserialization.
"""

import json
import logging
import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Optional, Type

logger = logging.getLogger(__name__)


def ensure_serializable(obj: Any) -> Any:
    """
    Ensure an object can be serialized to JSON.

    Args:
        obj: Object to make serializable

    Returns:
        JSON-serializable version of the object
    """
    if obj is None or isinstance(obj, (str, int, float, bool)):
        return obj

    if isinstance(obj, (list, tuple, set)):
        return [ensure_serializable(item) for item in obj]

    if isinstance(obj, dict):
        return {str(k): ensure_serializable(v) for k, v in obj.items()}

    if isinstance(obj, Enum):
        return obj.value

    if isinstance(obj, datetime):
        return obj.isoformat()

    if isinstance(obj, uuid.UUID):
        return str(obj)

    # Handle Pydantic models
    if hasattr(obj, "model_dump"):
        # Pydantic v2
        return ensure_serializable(obj.model_dump())
    if hasattr(obj, "dict"):
        # Pydantic v1
        return ensure_serializable(obj.dict())

    # Try to get __dict__
    if hasattr(obj, "__dict__"):
        return ensure_serializable(obj.__dict__)

    # Last resort: convert to string
    return str(obj)


def to_json(obj: Any, **kwargs) -> str:
    """
    Convert an object to a JSON string.

    Args:
        obj: Object to serialize
        **kwargs: Additional arguments for json.dumps

    Returns:
        JSON string
    """
    serializable = ensure_serializable(obj)
    return json.dumps(serializable, **kwargs)


def from_json(json_str: str, target_cls: Optional[Type] = None) -> Any:
    """
    Convert a JSON string to an object.

    Args:
        json_str: JSON string to deserialize
        target_cls: Optional target class

    Returns:
        Deserialized object
    """
    data = json.loads(json_str)

    if target_cls:
        # Handle Pydantic models
        if hasattr(target_cls, "model_validate"):
            # Pydantic v2
            return target_cls.model_validate(data)
        if hasattr(target_cls, "parse_obj"):
            # Pydantic v1
            return target_cls.parse_obj(data)

        # Handle simple classes
        if hasattr(target_cls, "__init__"):
            try:
                return target_cls(**data)
            except (TypeError, ValueError):
                pass

    return data
