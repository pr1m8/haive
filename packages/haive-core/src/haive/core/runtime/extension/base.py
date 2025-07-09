# src/haive/core/runtime/extensions/base.py

import uuid
from typing import Any, Dict, Generic, Optional, TypeVar

from pydantic import BaseModel, ConfigDict, Field

from haive.core.engine.base.protocols import ExtensibleProtocol
from haive.core.runtime.extension.protocols import ExtensionProtocol

T = TypeVar("T")  # Target type


class Extension(BaseModel, Generic[T], ExtensionProtocol[T]):
    """Base class for component extensions."""

    id: str = Field(default_factory=lambda: f"ext_{uuid.uuid4().hex[:8]}")
    name: str
    description: Optional[str] = Field(default=None)
    config: Dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def apply_to(self, target: T) -> T:
        """Apply this extension to a target object."""
        if isinstance(target, ExtensibleProtocol):
            target.apply_extensions([self])
        return target

    def apply(self, target: T) -> None:
        """Apply extension to target. Override in subclasses."""
        pass
