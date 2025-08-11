
haive.core.common.mixins.engine_mixin
=====================================

.. py:module:: haive.core.common.mixins.engine_mixin

.. autoapi-nested-parse::

   Engine management mixin for tracking and accessing Haive engines.

   This module provides a sophisticated mixin for managing different types of
   engines within the Haive framework. It enables tracking engines by name and type,
   collecting usage statistics, and provides rich visualization capabilities.

   Usage:
       ```python
       from pydantic import BaseModel
       from haive.core.common.mixins import EngineStateMixin
       from haive.core.engine.llm import LLMEngine

       class MyState(EngineStateMixin, BaseModel):
           # Other fields
           pass

       # Create state and add engines
       state = MyState()

       # Add an LLM engine
       llm = LLMEngine(name="my_llm", model="gpt-4", provider="openai")
       state.add_engine(llm)

       # Later, retrieve the engine
       retrieved_llm = state.get_engine("my_llm")

       # Get all LLM engines
       all_llms = state.get_llms()

       # Display engine information
       state.display_engines()
       ```







Classes
-------

* :py:class:`EngineStateMixin` - Mixin providing comprehensive engine management capabilities with validation.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/common/mixins/engine_mixin/EngineStateMixin

Package Contents
----------------

