
haive.core.utils.debugkit.fallbacks
===================================

.. py:module:: haive.core.utils.debugkit.fallbacks

.. autoapi-nested-parse::

   Fallback implementations for development utilities when dependencies are missing.

   This module provides minimal fallback implementations that allow the development
   utilities to function even when optional dependencies (like rich, icecream, etc.)
   are not available. The fallbacks maintain the same API but with reduced functionality.







Classes
-------

* :py:class:`FallbackDebug` - Minimal debug implementation when icecream and other debuggers are unavailable.* :py:class:`FallbackLog` - Minimal logging implementation when rich and loguru are unavailable.* :py:class:`FallbackLogContext` - Context manager for fallback logging.* :py:class:`FallbackTrace` - Minimal tracing implementation when advanced tracers are unavailable.* :py:class:`FallbackProfile` - Minimal profiling implementation when advanced profilers are unavailable.* :py:class:`FallbackBenchmark` - Minimal benchmarking implementation when advanced benchmarking tools are unavailable.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/utils/debugkit/fallbacks/FallbackDebug   /api_clean/haive/core/utils/debugkit/fallbacks/FallbackLog   /api_clean/haive/core/utils/debugkit/fallbacks/FallbackLogContext   /api_clean/haive/core/utils/debugkit/fallbacks/FallbackTrace   /api_clean/haive/core/utils/debugkit/fallbacks/FallbackProfile   /api_clean/haive/core/utils/debugkit/fallbacks/FallbackBenchmark

Package Contents
----------------

