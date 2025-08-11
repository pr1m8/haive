
:py:mod:`haive.core.config`
========================

.. py:module:: haive.core.config

.. autoapi-nested-parse::

   Configuration management module for the Haive framework.

   This module provides utilities for creating, managing, and manipulating runtime
   configurations for Haive engines and runnables. It handles parameter management,
   metadata tracking, configuration merging, and authentication.

   The configuration system supports both runtime configuration of engines and
   persistent configuration management across the framework.

   Key Components:
       RunnableConfigManager: Utility class for managing runnable configurations
       HaiveRunnableConfigManager: Haive-specific configuration with auth and persistence
       Configuration protocols and constants

   Features:
       - Runtime parameter management
       - Thread and user tracking
       - Configuration merging and inheritance
       - Authentication integration
       - Metadata and tags management
       - Engine-specific configuration
       - Configuration validation

   .. admonition:: Examples

      Basic configuration creation::
      
          from haive.core.config import RunnableConfigManager
      
          # Create config with tracking
          config = RunnableConfigManager.create(
              thread_id="thread_123",
              user_id="user_456",
              tags=["production", "api_v1"]
          )
      
          # Add engine configuration
          config = RunnableConfigManager.add_engine_config(
              config,
              engine_name="my_llm",
              temperature=0.7,
              max_tokens=1000
          )
      
      Configuration with authentication::
      
          from haive.core.config import HaiveRunnableConfigManager
      
          # Create authenticated config
          auth_config = HaiveRunnableConfigManager.create_with_auth(
              supabase_user_id="auth0|1234567890",
              username="john.doe",
              email="john.doe@example.com"
          )
      
      Configuration merging::
      
          # Merge configurations
          base_config = RunnableConfigManager.create(thread_id="123")
          override_config = {"temperature": 0.8}
      
          final_config = RunnableConfigManager.merge_configs(
              base_config,
              override_config
          )

   .. seealso::

      - LangChain RunnableConfig documentation
      - Engine configuration guides
      - Authentication and security docs





Submodules
----------

.. autosummary::
   :nosignatures:
   :template: autosummary/module.rst
   :toctree: .

   haive.core.config.auth_runnable   haive.core.config.constants   haive.core.config.protocols   haive.core.config.runnable
.. toctree::
   :maxdepth: 1
   :hidden:

   /api_clean/haive/core/config/auth_runnable/index   /api_clean/haive/core/config/constants/index   /api_clean/haive/core/config/protocols/index   /api_clean/haive/core/config/runnable/index





Package Contents
----------------

.. rubric:: haive.core.config.__all__

.. autosummary::
   :nosignatures:

   haive.core.config.CACHE_DIR   haive.core.config.RESOURCES_DIR   haive.core.config.ROOT_DIR   haive.core.config.ConfigurableProtocol   haive.core.config.HaiveRunnableConfigManager   haive.core.config.RunnableConfigManager

.. automodule:: haive.core.config
   :members:
   :undoc-members:
   :show-inheritance: