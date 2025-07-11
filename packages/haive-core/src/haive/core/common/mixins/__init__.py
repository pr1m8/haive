"""Mixins package providing reusable functionality for Haive components.

This package contains a collection of mixins that provide common functionality
that can be composed into classes through multiple inheritance. Mixins help
avoid code duplication and promote consistent behavior across the codebase.

The mixins are organized into several categories:
- General purpose mixins (ID, state, versioning, etc.)
- Engine integration mixins
- Tool management mixins
- Configuration mixins
- State management mixins

Usage:
    ```python
    from haive.core.common.mixins import IdentifierMixin, StateMixin

    class MyComponent(IdentifierMixin, StateMixin):
        def __init__(self, id: str = None):
            super().__init__(id=id)
            # Now the class has ID management and state management capabilities
    ```
"""

from haive.core.common.mixins.checkpointer_mixin import CheckpointerMixin
from haive.core.common.mixins.engine_mixin import EngineStateMixin as EngineMixin

# Import general mixins
from haive.core.common.mixins.general import (
    IdMixin,
    MetadataMixin,
    SerializationMixin,
    StateMixin,
    TimestampMixin,
    VersionMixin,
)
from haive.core.common.mixins.getter_mixin import GetterMixin
from haive.core.common.mixins.identifier import IdentifierMixin
from haive.core.common.mixins.mcp_mixin import MCPMixin
from haive.core.common.mixins.rich_logger_mixin import RichLoggerMixin
from haive.core.common.mixins.secure_config import SecureConfigMixin
from haive.core.common.mixins.state_interface_mixin import StateInterfaceMixin
from haive.core.common.mixins.structured_output_mixin import StructuredOutputMixin
from haive.core.common.mixins.tool_list_mixin import ToolListMixin
from haive.core.common.mixins.tool_route_mixin import ToolRouteMixin

__all__ = [
    # Main mixins
    "CheckpointerMixin",
    "EngineMixin",
    "GetterMixin",
    # General mixins
    "IdMixin",
    "IdentifierMixin",
    "MCPMixin",
    "MetadataMixin",
    "RichLoggerMixin",
    "SecureConfigMixin",
    "SerializationMixin",
    "StateInterfaceMixin",
    "StateMixin",
    "StructuredOutputMixin",
    "TimestampMixin",
    "ToolListMixin",
    "ToolRouteMixin",
    "VersionMixin",
]
