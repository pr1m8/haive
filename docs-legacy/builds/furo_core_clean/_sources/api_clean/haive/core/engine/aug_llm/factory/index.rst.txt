
haive.core.engine.aug_llm.factory
=================================

.. py:module:: haive.core.engine.aug_llm.factory

.. autoapi-nested-parse::

   Factory for creating LLM chain runnables from AugLLMConfig.

   from typing import Any
   This module provides a specialized factory implementation that transforms
   AugLLMConfig configurations into executable LLM chain runnables. It enforces
   a clean separation between configuration (AugLLMConfig) and runtime creation
   (AugLLMFactory), allowing for runtime overrides and specialized handling.

   Key features:
   - Runtime configuration overrides for flexible deployment
   - Structured output handling with multiple approaches (v1/v2)
   - Comprehensive tool binding with graceful fallbacks
   - Chain composition with preprocessing and postprocessing
   - Detailed logging for debugging and monitoring

   The factory handles the complex process of assembling different components
   (LLMs, prompts, tools, parsers) into a cohesive, executable chain while
   respecting the configuration specifications from AugLLMConfig.







Classes
-------

* :py:class:`AugLLMFactory` - Factory for creating structured LLM runnables from AugLLMConfig with flexible message handling.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/aug_llm/factory/AugLLMFactory

Package Contents
----------------

