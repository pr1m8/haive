
haive.core.persistence.postgres_saver_override
==============================================

.. py:module:: haive.core.persistence.postgres_saver_override

.. autoapi-nested-parse::

   PostgreSQL persistence utilities with Pydantic support.

   This module provides utilities for handling Pydantic models in PostgreSQL
   persistence. The main functionality is the JSON encoder configuration that
   ensures Pydantic models are properly serialized to JSONB columns.

   The override classes are kept for backward compatibility and as a fallback
   when using connection strings directly. However, the preferred approach is
   to configure the connection pool with the configure parameter.






Functions
---------

   pydantic_aware_json_dumps   configure_postgres_json
.. autofunction:: pydantic_aware_json_dumps
.. autofunction:: configure_postgres_json

Classes
-------

* :py:class:`PostgresSaverNoPreparedStatements` - PostgresSaver that disables prepared statements and handles Pydantic models.* :py:class:`AsyncPostgresSaverNoPreparedStatements` - Async PostgresSaver with proper configuration.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/persistence/postgres_saver_override/PostgresSaverNoPreparedStatements   /api_clean/haive/core/persistence/postgres_saver_override/AsyncPostgresSaverNoPreparedStatements

Package Contents
----------------

