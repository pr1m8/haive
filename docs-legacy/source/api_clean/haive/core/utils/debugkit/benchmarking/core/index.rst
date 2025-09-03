
haive.core.utils.debugkit.benchmarking.core
===========================================

.. py:module:: haive.core.utils.debugkit.benchmarking.core

.. autoapi-nested-parse::

   Benchmarking and Performance Testing Utilities

   A unified interface for timing benchmarks, load testing, and performance analysis.
   This module provides clean, focused tools for comprehensive performance testing.

   .. admonition:: Examples

      Basic timing benchmark:
          >>> from haive.core.utils.dev.benchmarking import benchmark
          >>>
          >>> def my_function():
          ...     return sum(i**2 for i in range(1000))
          >>>
          >>> result = benchmark.timing.time_it(my_function, iterations=1000)
      
      Load testing:
          >>> def api_call():
          ...     # Simulate API call
          ...     time.sleep(0.1)
          ...     return "response"
          >>>
          >>> result = benchmark.load.load_test(
          ...     api_call,
          ...     concurrent_users=10,
          ...     duration_seconds=30
          ... )
      
      Function comparison:
          >>> def bubble_sort(arr): ...
          >>> def quick_sort(arr): ...
          >>>
          >>> results = benchmark.timing.compare_functions(
          ...     [bubble_sort, quick_sort],
          ...     test_data
          ... )







Classes
-------

* :py:class:`BenchmarkUtilities` - Unified interface for all benchmarking utilities.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/utils/debugkit/benchmarking/core/BenchmarkUtilities

Package Contents
----------------

