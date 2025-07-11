"""State interface mixin for managing state access in components.

This module provides a mixin class that adds state management configuration
to Pydantic models, allowing components to specify whether they use state
and which key they access in the state store.

Usage:
    ```python
    from pydantic import BaseModel
    from haive.core.common.mixins import StateInterfaceMixin

    class MyStatefulComponent(StateInterfaceMixin, BaseModel):
        # Other fields
        name: str

        def process(self, inputs, state=None):
            if self.use_state and state:
                # Access state using the configured key
                component_state = state.get(self.state_key, {})
                # Update state
                component_state["visits"] = component_state.get("visits", 0) + 1
                state[self.state_key] = component_state
            return {"result": f"Processed {self.name}"}
    ```
"""

from pydantic import BaseModel, Field


class StateInterfaceMixin(BaseModel):
    """Mixin that adds state management configuration to any Pydantic model.

    This mixin allows components to declare whether they use a state store
    and which key they use to access their portion of the state. This is
    commonly used in stateful nodes within a processing graph.

    Attributes:
        use_state: Boolean flag indicating whether this component uses state.
        state_key: The key used to access this component's state in the state store.
    """

    use_state: bool = Field(
        default=False, description="Whether to use the state for the tool node"
    )
    state_key: str = Field(default="state", description="The key to use for the state")
