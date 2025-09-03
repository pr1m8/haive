
haive.core.config.auth_runnable
===============================

.. py:module:: haive.core.config.auth_runnable

.. autoapi-nested-parse::

   Haive-specific extension of runnable config management with PostgreSQL integration.

   from typing import Any
   This module extends RunnableConfigManager to provide both Supabase authentication
   integration and PostgreSQL persistence support for the Haive framework. It creates
   a unified configuration system that handles authentication, session management,
   and database persistence in a cohesive manner.

   The HaiveRunnableConfigManager inherits all functionality from the base RunnableConfigManager
   while adding specialized methods for Supabase user authentication, thread persistence,
   and PostgreSQL integration. This design ensures proper user context is maintained
   throughout conversation threads and persisted correctly in PostgreSQL.

   Classes:
       HaiveRunnableConfigManager: Extended config manager with Supabase auth and PostgreSQL integration

   .. admonition:: Example

      ```python
      # Create a config with Supabase authentication
      config = HaiveRunnableConfigManager.create_with_auth(
          supabase_user_id="auth0|1234567890",
          username="john.doe",
          email="john.doe@example.com"
      )
      
      # Add PostgreSQL persistence information
      config = HaiveRunnableConfigManager.add_persistence_info(
          config,
          db_session_id="pgsql-session-123",
          persistence_type="postgres"
      )
      
      # Add engine-specific configuration
      config = HaiveRunnableConfigManager.add_engine_config(
          config,
          "my_llm_engine",
          temperature=0.7
      )
      ```







Classes
-------

* :py:class:`HaiveRunnableConfigManager` - Enhanced runnable config manager with Supabase authentication and PostgreSQL integration.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/config/auth_runnable/HaiveRunnableConfigManager

Package Contents
----------------

