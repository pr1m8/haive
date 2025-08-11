
:py:mod:`haive.core.persistence`
========================

.. py:module:: haive.core.persistence

.. autoapi-nested-parse::

   Persistence module for state management and checkpointing in the Haive framework.

   This module provides a comprehensive system for persisting agent state across sessions,
   allowing for stateful agents that can continue conversations and maintain context
   over time. It offers multiple storage backends and configuration options to balance
   performance, durability, and scalability.

   Key components:
   - CheckpointerConfig: Base configuration for all persistence providers
   - MemoryCheckpointerConfig: In-memory persistence for development and testing
   - PostgresCheckpointerConfig: PostgreSQL-backed persistence for production
   - SQLiteCheckpointerConfig: SQLite-backed persistence for local development
   - SupabaseCheckpointerConfig: Supabase-backed persistence for cloud deployments

   The module integrates with LangGraph's checkpoint system while providing enhanced
   features like connection pooling, automatic retry with exponential backoff, and
   thread registration for tracking agent sessions.

   Usage:
       ```python
       from haive.core.persistence import MemoryCheckpointerConfig

       # Create a memory-based checkpointer
       config = MemoryCheckpointerConfig()
       checkpointer = config.create_checkpointer()

       # Use in an agent configuration
       agent_config = AgentConfig(
           persistence=config,
           # other configuration...
       )
       ```

   For more advanced usage with PostgreSQL:
       ```python
       from haive.core.persistence import PostgresCheckpointerConfig
       from haive.core.persistence.types import CheckpointerMode, CheckpointStorageMode

       # Create a PostgreSQL checkpointer
       postgres_config = PostgresCheckpointerConfig(
           mode=CheckpointerMode.ASYNC,  # Use async operations
           storage_mode=CheckpointStorageMode.SHALLOW,  # Only store latest state
           db_host="localhost",
           db_port=5432,
           db_name="haive",
           db_user="postgres",
           db_pass="password"
       )

       # For async usage
       async def setup():
           async_checkpointer = await postgres_config.create_async_checkpointer()
           # Use the checkpointer...
       ```

   This module is designed to work seamlessly with both synchronous and asynchronous
   code, providing appropriate interfaces for each context.




Subpackages
-----------

.. autosummary::
   :nosignatures:
   :template: autosummary/module.rst
   :toctree: .

   haive.core.persistence.store
.. toctree::
   :maxdepth: 2
   :hidden:

   /api_clean/haive/core/persistence/store/index

Submodules
----------

.. autosummary::
   :nosignatures:
   :template: autosummary/module.rst
   :toctree: .

   haive.core.persistence.base   haive.core.persistence.factory   haive.core.persistence.handlers   haive.core.persistence.memory   haive.core.persistence.postgres_config   haive.core.persistence.postgres_saver_override   haive.core.persistence.postgres_saver_with_thread_creation   haive.core.persistence.serializers   haive.core.persistence.sqlite_config   haive.core.persistence.supabase_config   haive.core.persistence.types   haive.core.persistence.utils
.. toctree::
   :maxdepth: 1
   :hidden:

   /api_clean/haive/core/persistence/base/index   /api_clean/haive/core/persistence/factory/index   /api_clean/haive/core/persistence/handlers/index   /api_clean/haive/core/persistence/memory/index   /api_clean/haive/core/persistence/postgres_config/index   /api_clean/haive/core/persistence/postgres_saver_override/index   /api_clean/haive/core/persistence/postgres_saver_with_thread_creation/index   /api_clean/haive/core/persistence/serializers/index   /api_clean/haive/core/persistence/sqlite_config/index   /api_clean/haive/core/persistence/supabase_config/index   /api_clean/haive/core/persistence/types/index   /api_clean/haive/core/persistence/utils/index





Package Contents
----------------

.. rubric:: haive.core.persistence.__all__

.. autosummary::
   :nosignatures:

   haive.core.persistence.CheckpointStorageMode   haive.core.persistence.CheckpointerConfig   haive.core.persistence.CheckpointerMode   haive.core.persistence.CheckpointerType   haive.core.persistence.MemoryCheckpointerConfig   haive.core.persistence.PostgresCheckpointerConfig   haive.core.persistence.SQLiteCheckpointerConfig   haive.core.persistence.acreate_postgres_checkpointer   haive.core.persistence.create_postgres_checkpointer   haive.core.persistence.setup_checkpointer

.. automodule:: haive.core.persistence
   :members:
   :undoc-members:
   :show-inheritance: