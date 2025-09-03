
haive.core.persistence.postgres_config
======================================

.. py:module:: haive.core.persistence.postgres_config

.. autoapi-nested-parse::

   PostgreSQL-based persistence implementation for the Haive framework.

   This module provides a PostgreSQL-backed checkpoint persistence implementation that
   stores state data in a PostgreSQL database. This allows for durable, reliable state
   persistence across application restarts and deployments.

   The PostgreSQL implementation offers advanced features including connection pooling,
   automatic retry with exponential backoff, comprehensive error handling, and support
   for both synchronous and asynchronous operation modes. It integrates with LangGraph's
   checkpoint system while adding enhanced robustness and configurability.

   For production deployments, the PostgreSQL implementation is generally recommended
   over in-memory or SQLite options due to its scalability, reliability, and
   concurrent access capabilities.







Classes
-------

* :py:class:`PostgresCheckpointerConfig` - Configuration for PostgreSQL-based checkpoint persistence.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/persistence/postgres_config/PostgresCheckpointerConfig

Package Contents
----------------

