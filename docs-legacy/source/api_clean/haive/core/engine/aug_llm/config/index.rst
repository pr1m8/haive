
haive.core.engine.aug_llm.config
================================

.. py:module:: haive.core.engine.aug_llm.config

.. autoapi-nested-parse::

   AugLLM configuration system for enhanced LLM chains.

   from typing import Any, Dict
   This module provides a comprehensive configuration system for creating and
   managing enhanced LLM chains within the Haive framework. The AugLLMConfig class
   serves as a central configuration point that integrates prompts, tools, output
   parsers, and structured output models with extensive validation and debugging
   capabilities.

   Key features:
   - Flexible prompt template creation and management with support for few-shot learning
   - Comprehensive tool integration with automatic discovery and configuration
   - Structured output handling via two approaches (v1: parser-based, v2: tool-based)
   - Rich debugging and validation to ensure proper configuration
   - Pre/post processing hooks for customizing input and output
   - Support for both synchronous and asynchronous execution

   The configuration system is designed to be highly customizable while providing
   sensible defaults and automatic detection of configuration requirements.






Functions
---------

   debug_print
.. autofunction:: debug_print

Classes
-------

* :py:class:`StructuredOutputMixin` - Class* :py:class:`AugLLMConfig` - Configuration for creating enhanced LLM chains with flexible message handling.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/aug_llm/config/StructuredOutputMixin   /api_clean/haive/core/engine/aug_llm/config/AugLLMConfig

Package Contents
----------------

