"""General-purpose mixins providing basic functionality for Haive components.

This package contains fundamental mixins that provide core functionality
like ID management, serialization, state tracking, and versioning. These
mixins are designed to be lightweight and composable, making them suitable
for inclusion in a wide variety of components.

Available mixins:
- IdMixin: Basic ID generation and management
- MetadataMixin: Key-value metadata storage
- SerializationMixin: Enhanced serialization capabilities
- StateMixin: State tracking and validation
- TimestampMixin: Creation and modification timestamp tracking
- VersionMixin: Version tracking and compatibility checking

Usage:
    ```python
    from pydantic import BaseModel
    from haive.core.common.mixins.general import (
        IdMixin, TimestampMixin, VersionMixin
    )

    class MyComponent(IdMixin, TimestampMixin, VersionMixin, BaseModel):
        name: str

        def __init__(self, **data):
            super().__init__(**data)
            # Now the component has ID, timestamp, and version capabilities
    ```
"""

from haive.core.common.mixins.general.id import IdMixin
from haive.core.common.mixins.general.metadata import MetadataMixin
from haive.core.common.mixins.general.serialization import SerializationMixin
from haive.core.common.mixins.general.state import StateMixin
from haive.core.common.mixins.general.timestamp import TimestampMixin
from haive.core.common.mixins.general.version import VersionMixin

__all__ = [
    "IdMixin",
    "MetadataMixin",
    "SerializationMixin",
    "StateMixin",
    "TimestampMixin",
    "VersionMixin",
]
