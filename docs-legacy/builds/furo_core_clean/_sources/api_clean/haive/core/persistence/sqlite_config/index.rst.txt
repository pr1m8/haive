
haive.core.persistence.sqlite_config
====================================

.. py:module:: haive.core.persistence.sqlite_config

.. autoapi-nested-parse::

   SQLite-based persistence implementation for the Haive framework.

   from typing import Any, Dict
   This module provides a SQLite-backed checkpoint persistence implementation that
   stores state data in a local SQLite database file. This allows for durable state
   persistence without requiring external database services, making it ideal for
   local development, testing, and single-instance deployments.

   The SQLite implementation strikes a balance between the simplicity of in-memory
   storage and the durability of full database solutions like PostgreSQL. It offers
   file-based persistence with minimal setup, while still providing basic thread
   tracking and checkpoint management capabilities.

   Key advantages of the SQLite implementation include:
   - No external dependencies beyond the Python standard library
   - Simple file-based storage requiring no separate database service
   - Compatibility with both synchronous and asynchronous operations
   - Support for both full history and shallow (latest-only) storage modes
   - Automatic schema creation and management







Classes
-------

* :py:class:`SQLiteSaver` - A LangGraph-compatible checkpointer implementation using SQLite.* :py:class:`SQLiteCheckpointerConfig` - Configuration for SQLite-based checkpoint persistence.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/persistence/sqlite_config/SQLiteSaver   /api_clean/haive/core/persistence/sqlite_config/SQLiteCheckpointerConfig

Package Contents
----------------

