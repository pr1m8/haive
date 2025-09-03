
haive.core.utils.debugkit.analysis.types
========================================

.. py:module:: haive.core.utils.debugkit.analysis.types

.. autoapi-nested-parse::

   Advanced type analysis for Python functions and modules.

   This module provides comprehensive type analysis capabilities including:
   - Type annotation coverage analysis
   - Type error detection using mypy
   - Generic type complexity scoring
   - Runtime type validation support
   - Module-wide type analysis

   The type analyzer integrates with multiple type checkers and provides
   actionable insights for improving type safety in Python codebases.






Functions
---------

   get_args
.. autofunction:: get_args

Classes
-------

* :py:class:`TypeComplexity` - Type complexity levels for classification.* :py:class:`TypeInfo` - Detailed type information for a variable, parameter, or return value.* :py:class:`FunctionTypeAnalysis` - Complete type analysis results for a function.* :py:class:`TypeAnalyzer` - Advanced type analyzer for Python functions and modules.* :py:class:`FunctionFinder` - AST visitor to find all function definitions in a module.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/utils/debugkit/analysis/types/TypeComplexity   /api_clean/haive/core/utils/debugkit/analysis/types/TypeInfo   /api_clean/haive/core/utils/debugkit/analysis/types/FunctionTypeAnalysis   /api_clean/haive/core/utils/debugkit/analysis/types/TypeAnalyzer   /api_clean/haive/core/utils/debugkit/analysis/types/FunctionFinder

Package Contents
----------------

