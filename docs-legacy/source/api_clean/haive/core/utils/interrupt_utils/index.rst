
haive.core.utils.interrupt_utils
================================

.. py:module:: haive.core.utils.interrupt_utils

.. autoapi-nested-parse::

   Utilities for detecting whether a callable uses `pause_for_human(...)` to pause execution.

   This wraps LangGraph's `interrupt(...)` signal and provides AST-based static analysis to detect
   if a function or callable object may yield control for human input.






Functions
---------

   pause_for_human   uses_pause   is_interruptible
.. autofunction:: pause_for_human
.. autofunction:: uses_pause
.. autofunction:: is_interruptible



Package Contents
----------------

