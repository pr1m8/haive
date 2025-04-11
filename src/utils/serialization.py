"""
Serialization utilities for the registry system.

Helper functions to ensure objects can be properly serialized to JSON.
"""

import json
import datetime
import decimal
import uuid
from typing import Any, Dict, List, Union, Optional


def serialize_object(obj: Any) -> Any:
    """
    Recursively serialize an object to ensure it's JSON-serializable.
    
    Args:
        obj: Any Python object
        
    Returns:
        JSON-serializable version of the object
    """
    if isinstance(obj, (str, int, float, bool, type(None))):
        return obj
    elif isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)
    elif isinstance(obj, uuid.UUID):
        return str(obj)
    elif isinstance(obj, bytes):
        return obj.decode('utf-8', errors='replace')
    elif isinstance(obj, (list, tuple, set)):
        return [serialize_object(item) for item in obj]
    elif isinstance(obj, dict):
        return {str(key): serialize_object(value) for key, value in obj.items()}
    elif hasattr(obj, '__dict__'):
        # Handle objects with __dict__ attribute
        return serialize_object(obj.__dict__)
    elif hasattr(obj, 'dict') and callable(getattr(obj, 'dict')):
        # Handle Pydantic models
        return serialize_object(obj.dict())
    elif hasattr(obj, 'model_dump') and callable(getattr(obj, 'model_dump')):
        # Handle Pydantic v2 models
        return serialize_object(obj.model_dump())
    else:
        # Try converting to string as a last resort
        try:
            return str(obj)
        except Exception:
            return "[Object could not be serialized]"


def json_dumps(obj: Any, indent: Optional[int] = 2, **kwargs) -> str:
    """
    Serialize object to JSON string, handling non-serializable types.
    
    Args:
        obj: Object to serialize
        indent: Indentation level
        **kwargs: Additional arguments for json.dumps
        
    Returns:
        JSON string
    """
    serialized = serialize_object(obj)
    return json.dumps(serialized, indent=indent, **kwargs)


def json_loads(json_str: str, **kwargs) -> Any:
    """
    Deserialize JSON string to Python object.
    
    Args:
        json_str: JSON string
        **kwargs: Additional arguments for json.loads
        
    Returns:
        Deserialized Python object
    """
    try:
        return json.loads(json_str, **kwargs)
    except json.JSONDecodeError as e:
        # Try to strip any non-JSON content around the JSON
        # (e.g., if someone copied JSON with extra text)
        try:
            # Find the first '{' and the last '}'
            start = json_str.find('{')
            end = json_str.rfind('}')
            
            if start >= 0 and end > start:
                cleaned_json = json_str[start:end+1]
                return json.loads(cleaned_json, **kwargs)
            
            # Try finding array format as well
            start = json_str.find('[')
            end = json_str.rfind(']')
            
            if start >= 0 and end > start:
                cleaned_json = json_str[start:end+1]
                return json.loads(cleaned_json, **kwargs)
                
            # If we got here, give up and raise the original error
            raise e
        except Exception:
            # If any error occurs in the recovery attempt, raise the original error
            raise e