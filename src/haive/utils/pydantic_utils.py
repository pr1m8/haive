import json
from typing import Any
from pydantic import BaseModel

def ensure_json_serializable(obj: Any) -> Any:
    """Ensure object is JSON serializable, converting non-serializable objects."""
    try:
        json.dumps(obj)
        return obj
    except (TypeError, OverflowError):
        if isinstance(obj, BaseModel):
            return obj.model_dump()
        elif isinstance(obj, dict):
            return {k: ensure_json_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [ensure_json_serializable(v) for v in obj]
        elif isinstance(obj, tuple):
            return [ensure_json_serializable(v) for v in obj]
        elif hasattr(obj, "__dict__"):
            return ensure_json_serializable(vars(obj))
        elif hasattr(obj, "__str__"):
            return str(obj)
        else:
            return "Unserializable Object"
