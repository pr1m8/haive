
haive.core.utils.debugkit.debugging
===================================

.. py:module:: haive.core.utils.debugkit.debugging

.. autoapi-nested-parse::

   Enhanced Debugging Utilities

   A unified interface for all debugging capabilities including enhanced print debugging,
   interactive debugging, decorators, and inspection utilities.

   .. admonition:: Examples

      Enhanced debugging (icecream replacement):
          >>> from haive.core.utils.dev.debugging import debug
          >>> debug.ice("Hello", variable=42)
      
      Interactive debugging:
          >>> debug.pdb()  # Enhanced pdb
          >>> debug.web(port=8080)  # Web-based debugging
          >>> debug.visual()  # Visual debugging with pudb
      
      Automatic exception debugging:
          >>> @debug.breakpoint_on_exception
          ... def risky_function():
          ...     # Will auto-debug on exceptions
          ...     pass
      
      Call tracing:
          >>> @debug.trace_calls
          ... def tracked_function():
          ...     # Will show call trace
          ...     pass
      
      Variable inspection:
          >>> debug.locals_inspect()  # See local variables
          >>> debug.stack_trace()     # See call stack







Classes
-------

* :py:class:`DebugUtilities` - Unified interface for all debugging utilities.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/utils/debugkit/debugging/DebugUtilities

Package Contents
----------------

