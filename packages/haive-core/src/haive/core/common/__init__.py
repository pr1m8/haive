"""
Haive Core Common Module.

This module provides common utilities, models, types, and mixins used throughout the Haive
framework. It contains foundational components that enable consistent behavior across
different parts of the system.

Key Components:
    - Mixins: Reusable component behaviors through mixin classes
    - Models: Common data structures and models
    - Types: Type definitions and protocol interfaces
    - Structures: Collection structures with enhanced functionality
    - Logging: Centralized logging configuration

Typical usage example:
    ```python
    from haive.core.common.mixins import IdentifierMixin, TimestampMixin
    from haive.core.common.types import JsonType, DictStrAny
    from haive.core.common.logging_config import configure_logging

    # Use mixins in your class
    class MyComponent(IdentifierMixin, TimestampMixin):
        def __init__(self, name: str):
            super().__init__()
            self.name = name

    # Configure logging
    configure_logging(level="INFO")
    ```
"""

# Import common mixins
from haive.core.common.mixins import (
    IdentifierMixin as IDMixin,  # Alias for backward compatibility
)
from haive.core.common.mixins import (
    MetadataMixin,
    RichLoggerMixin,
    SerializationMixin,
    TimestampMixin,
    VersionMixin,
)

# Import common models
from haive.core.common.models import DynamicChoiceModel, NamedList

# Import common types
from haive.core.common.types import DictStrAny, JsonType, StrOrPath

# Export all these symbols when using star imports
__all__ = [
    # Types
    "JsonType",
    "DictStrAny",
    "StrOrPath",
    # Mixins
    "IDMixin",
    "TimestampMixin",
    "VersionMixin",
    "SerializationMixin",
    "MetadataMixin",
    "RichLoggerMixin",
    # Models
    "DynamicChoiceModel",
    "NamedList",
]
