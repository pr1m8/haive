# Usage example
# stringified = stringify_pydantic_model(model, pretty=True)
from typing import Any, Dict, List

from pydantic import BaseModel, Field


def create_sync_properties(field_names: List[str], target_attr: str = "engine_config"):
    """Create properties that sync with an attribute of the instance (e.g. engine_config)."""

    def decorator(cls):
        for field_name in field_names:

            def make_property(fname):
                def getter(self):
                    return getattr(getattr(self, target_attr), fname)

                def setter(self, value):
                    setattr(getattr(self, target_attr), fname, value)

                return property(getter, setter)

            setattr(cls, field_name, make_property(field_name))
        return cls

    return decorator
