
:py:mod:`haive.core.utils.debugkit`
========================

.. py:module:: haive.core.utils.debugkit

.. autoapi-nested-parse::

   Unified development utilities for Python debugging, profiling, and analysis.

   This package provides a comprehensive suite of development tools including:
   - Enhanced debugging with multiple debugger integrations
   - Rich logging with structured output and context management
   - Advanced code tracing and execution analysis
   - Performance profiling with multiple profiler backends
   - Comprehensive static analysis orchestration
   - Code complexity and type analysis
   - Benchmarking and load testing utilities

   All utilities are designed to work together seamlessly and provide
   both simple interfaces for quick debugging and advanced features
   for comprehensive code analysis.

   .. admonition:: Examples

      Quick start with unified interface::
      
          from haive.core.utils.debugkit import debugkit
      
          # Enhanced debugging
          debugkit.ice("Debug variable", value=42)
      
          # Rich logging with context
          with debugkit.context("operation") as ctx:
              ctx.log("Starting process")
              # ... work ...
              ctx.log("Process complete")
      
          # Complete analysis
          @debugkit.instrument(analyze=True, profile=True)
          def my_function(data: List[str]) -> Dict[str, int]:
              return process_data(data)
      
      Individual component usage::
      
          from haive.core.utils.debugkit import debug, log, trace, profile
      
          # Use specific components
          debug.ice("Variable inspection", data=my_data)
          log.info("Process started", context={"user": "alice"})
      
          @trace.calls
          @profile.time
          def traced_function():
              return complex_operation()
      
      Advanced analysis::
      
          from haive.core.utils.debugkit import debugkit
      
          # Analyze code quality
          analysis = debugkit.analyze_code(my_function)
          print(f"Type coverage: {analysis.type_analysis.type_coverage:.1%}")
          print(f"Complexity grade: {analysis.complexity_analysis.complexity_grade}")
      
          # Run static analysis
          results = debugkit.static_analysis.analyze_file(Path("module.py"))
          report = debugkit.static_analysis.generate_report(results)




Subpackages
-----------

.. autosummary::
   :nosignatures:
   :template: autosummary/module.rst
   :toctree: .

   haive.core.utils.debugkit.analysis   haive.core.utils.debugkit.benchmarking   haive.core.utils.debugkit.core   haive.core.utils.debugkit.debug   haive.core.utils.debugkit.logging   haive.core.utils.debugkit.profiling   haive.core.utils.debugkit.tracing
.. toctree::
   :maxdepth: 2
   :hidden:

   /api_clean/haive/core/utils/debugkit/analysis/index   /api_clean/haive/core/utils/debugkit/benchmarking/index   /api_clean/haive/core/utils/debugkit/core/index   /api_clean/haive/core/utils/debugkit/debug/index   /api_clean/haive/core/utils/debugkit/logging/index   /api_clean/haive/core/utils/debugkit/profiling/index   /api_clean/haive/core/utils/debugkit/tracing/index

Submodules
----------

.. autosummary::
   :nosignatures:
   :template: autosummary/module.rst
   :toctree: .

   haive.core.utils.debugkit.config   haive.core.utils.debugkit.debugging   haive.core.utils.debugkit.fallbacks
.. toctree::
   :maxdepth: 1
   :hidden:

   /api_clean/haive/core/utils/debugkit/config/index   /api_clean/haive/core/utils/debugkit/debugging/index   /api_clean/haive/core/utils/debugkit/fallbacks/index





Package Contents
----------------

.. rubric:: haive.core.utils.debugkit.__all__

.. autosummary::
   :nosignatures:

   haive.core.utils.debugkit.debugkit   haive.core.utils.debugkit.debug   haive.core.utils.debugkit.log   haive.core.utils.debugkit.trace   haive.core.utils.debugkit.profile   haive.core.utils.debugkit.benchmark   haive.core.utils.debugkit.config   haive.core.utils.debugkit.DevConfig   haive.core.utils.debugkit.DevContext   haive.core.utils.debugkit.CodeAnalysisReport   haive.core.utils.debugkit.UnifiedDev   haive.core.utils.debugkit.Environment   haive.core.utils.debugkit.LogLevel   haive.core.utils.debugkit.StorageBackend

.. automodule:: haive.core.utils.debugkit
   :members:
   :undoc-members:
   :show-inheritance: