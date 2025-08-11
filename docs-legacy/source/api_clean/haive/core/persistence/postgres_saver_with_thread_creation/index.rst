
haive.core.persistence.postgres_saver_with_thread_creation
==========================================================

.. py:module:: haive.core.persistence.postgres_saver_with_thread_creation

.. autoapi-nested-parse::

   PostgreSQL Saver with automatic thread creation.

   This module provides a PostgreSQL checkpointer that automatically creates
   threads before saving checkpoints, preventing foreign key constraint violations.






Functions
---------

   create_postgres_saver_with_thread_creation   create_async_postgres_saver_with_thread_creation
.. autofunction:: create_postgres_saver_with_thread_creation
.. autofunction:: create_async_postgres_saver_with_thread_creation

Classes
-------

* :py:class:`PostgresSaverWithThreadCreation` - PostgreSQL checkpointer that ensures threads exist before saving checkpoints.* :py:class:`AsyncPostgresSaverWithThreadCreation` - Async version of PostgresSaver with thread creation.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/persistence/postgres_saver_with_thread_creation/PostgresSaverWithThreadCreation   /api_clean/haive/core/persistence/postgres_saver_with_thread_creation/AsyncPostgresSaverWithThreadCreation

Package Contents
----------------

