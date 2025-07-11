"""State schema module with modular mixins.

This module provides the base StateSchema class broken down into focused mixins:

- base: Core StateSchema base class
- engine: Engine management capabilities
- serialization: JSON/dict conversion methods
- manipulation: State update and comparison methods
- visualization: Rich display and debugging tools
"""

# from haive.core.schema.state.base_state import BaseStateSchema
# from haive.core.schema.state.engine.engine_state_mixin import EngineStateMixin
# from haive.core.schema.state.manipulation.state_manipulation_mixin import (
#    StateManipulationMixin,
# )
# from haive.core.schema.state.serialization.serialization_mixin import SerializationMixin

# Re-export the full StateSchema for backward compatibility
from haive.core.schema.state_schema import StateSchema

__all__ = [
    # "BaseStateSchema",
    # "EngineStateMixin",
    # "SerializationMixin",
    # "StateManipulationMixin",
    "StateSchema",  # Backward compatibility
]
