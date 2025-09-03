
haive.core.common.mixins.state_interface_mixin
==============================================

.. py:module:: haive.core.common.mixins.state_interface_mixin

.. autoapi-nested-parse::

   State interface mixin for managing state access in components.

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







Classes
-------

* :py:class:`StateInterfaceMixin` - Mixin that adds state management configuration to any Pydantic model.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/common/mixins/state_interface_mixin/StateInterfaceMixin

Package Contents
----------------

