
haive.core.config.runnable
==========================

.. py:module:: haive.core.config.runnable

.. autoapi-nested-parse::

   Configuration management for Haive runnables.

   This module provides utilities for creating, managing, and manipulating runtime configurations
   for Haive engines and runnables. It handles parameter management, metadata tracking, and
   configuration merging.

   The main class RunnableConfigManager provides a comprehensive set of static methods for
   working with RunnableConfig objects, which are used to configure the behavior of engines
   at runtime.

   Classes:
       RunnableConfigManager: Static utility class for managing runnable configurations

   .. admonition:: Example

      ```python
      # Create a basic config with thread tracking
      config = RunnableConfigManager.create(
          thread_id="123",
          user_id="user_456"
      )
      
      # Add engine-specific configuration
      config = RunnableConfigManager.add_engine_config(
          config,
          "my_llm",
          temperature=0.7,
          max_tokens=100
      )
      ```







Classes
-------

* :py:class:`RunnableConfigManager` - Enhanced manager for creating and manipulating RunnableConfig objects.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/config/runnable/RunnableConfigManager

Package Contents
----------------

