
haive.core.common.mixins.general.state
======================================

.. py:module:: haive.core.common.mixins.general.state

.. autoapi-nested-parse::

   State management mixin for tracking object state changes with history.

   This module provides a Pydantic-based mixin for adding state tracking capabilities
   to any BaseModel. It maintains a current state string and a complete history
   of all state changes with timestamps and optional reasons.

   Usage:
       ```python
       from pydantic import BaseModel
       from haive.core.common.mixins.general.state import StateMixin

       class MyComponent(StateMixin, BaseModel):
           name: str

       # Create component and change states
       component = MyComponent(name="test")
       component.change_state("processing", "Starting work")
       component.change_state("complete", "Finished successfully")

       # Check current state
       if component.is_in_state("complete"):
           print("Component is done!")

       # Review state history
       for change in component.get_state_changes():
           print(f"{change['timestamp']}: {change['from_state']} -> {change['to_state']}")
       ```







Classes
-------

* :py:class:`StateMixin` - Mixin for state tracking with validation and comprehensive history.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/common/mixins/general/state/StateMixin

Package Contents
----------------

