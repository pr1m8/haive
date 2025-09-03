
haive.core.utils.debugkit.analysis.static
=========================================

.. py:module:: haive.core.utils.debugkit.analysis.static

.. autoapi-nested-parse::

   Static analysis orchestrator for integrating multiple Python analysis tools.

   This module provides a unified interface for running and coordinating multiple
   static analysis tools including type checkers, linters, complexity analyzers,
   and code quality tools. It orchestrates tools like mypy, pyright, radon, vulture,
   and many others from the development toolchain.

   The orchestrator handles tool execution, result parsing, and provides
   unified reporting across all analysis tools.







Classes
-------

* :py:class:`AnalysisType` - Types of static analysis.* :py:class:`Severity` - Analysis finding severity levels.* :py:class:`AnalysisFinding` - A single finding from static analysis.* :py:class:`AnalysisResult` - Results from running a static analysis tool.* :py:class:`ToolAnalyzer` - Base class for individual tool analyzers.* :py:class:`MypyAnalyzer` - Mypy static type checker analyzer.* :py:class:`RadonAnalyzer` - Radon complexity analyzer.* :py:class:`VultureAnalyzer` - Vulture dead code analyzer.* :py:class:`PyflakesAnalyzer` - Pyflakes code quality analyzer.* :py:class:`StaticAnalysisOrchestrator` - Orchestrator for running multiple static analysis tools.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/utils/debugkit/analysis/static/AnalysisType   /api_clean/haive/core/utils/debugkit/analysis/static/Severity   /api_clean/haive/core/utils/debugkit/analysis/static/AnalysisFinding   /api_clean/haive/core/utils/debugkit/analysis/static/AnalysisResult   /api_clean/haive/core/utils/debugkit/analysis/static/ToolAnalyzer   /api_clean/haive/core/utils/debugkit/analysis/static/MypyAnalyzer   /api_clean/haive/core/utils/debugkit/analysis/static/RadonAnalyzer   /api_clean/haive/core/utils/debugkit/analysis/static/VultureAnalyzer   /api_clean/haive/core/utils/debugkit/analysis/static/PyflakesAnalyzer   /api_clean/haive/core/utils/debugkit/analysis/static/StaticAnalysisOrchestrator

Package Contents
----------------

