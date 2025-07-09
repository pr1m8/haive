import inspect
import json
from typing import Any, Optional

from pydantic import BaseModel


def stringify_pydantic_model(
    model: BaseModel,
    pretty: bool = False,
    exclude: Optional[set] = None,
    include: Optional[set] = None,
    indent: int = 2,
) -> str:
    """
    Universal stringifier for any Pydantic model.

    Args:
        model: The Pydantic model to stringify
        pretty: Whether to format with indentation
        exclude: Fields to exclude from serialization
        include: Fields to include in serialization
        indent: Number of spaces for indentation if pretty=True

    Returns:
        String representation of the model
    """
    if hasattr(model, "model_dump_json"):
        # Pydantic v2
        if pretty:
            return model.model_dump_json(
                indent=indent, exclude=exclude, include=include
            )
        else:
            return model.model_dump_json(exclude=exclude, include=include)
    elif hasattr(model, "json"):
        # Pydantic v1 fallback
        if pretty:
            return model.json(indent=indent, exclude=exclude, include=include)
        else:
            return model.json(exclude=exclude, include=include)
    else:
        # Fallback to string representation
        return str(model)


def ensure_json_serializable(obj: Any) -> Any:
    """
    Ensure object is JSON serializable, converting non-serializable objects.

    Args:
        obj: The object to make JSON serializable

    Returns:
        A JSON serializable version of the object
    """
    try:
        json.dumps(obj)
        return obj
    except (TypeError, OverflowError):
        if isinstance(obj, BaseModel):
            return obj.model_dump() if hasattr(obj, "model_dump") else obj.dict()
        if inspect.isfunction(obj) or inspect.ismethod(obj) or callable(obj):
            # Handle function objects by converting to string representation
            if hasattr(obj, "__name__"):
                return f"<function {obj.__name__}>"
            return "<callable object>"
        if isinstance(obj, dict):
            return {k: ensure_json_serializable(v) for k, v in obj.items()}
        if isinstance(obj, (list, tuple)):
            return [ensure_json_serializable(v) for v in obj]
        if hasattr(obj, "__dict__"):
            return ensure_json_serializable(vars(obj))
        if hasattr(obj, "__str__"):
            return str(obj)
        return "Unserializable Object"
