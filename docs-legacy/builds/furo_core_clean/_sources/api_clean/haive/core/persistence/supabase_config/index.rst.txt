
haive.core.persistence.supabase_config
======================================

.. py:module:: haive.core.persistence.supabase_config

.. autoapi-nested-parse::

   Supabase-based persistence implementation for the Haive framework.

   This module provides a Supabase-backed checkpoint persistence implementation that
   stores state data in a Supabase Postgres database. This allows for cloud-based,
   scalable state persistence with built-in security features like Row Level Security
   (RLS) policies.

   Supabase offers a fully-managed Postgres database service with authentication,
   realtime features, and other cloud infrastructure benefits. This implementation
   leverages these capabilities to provide a production-ready persistence solution
   with proper relational design and security policies.

   Key advantages of the Supabase implementation include:
   - Cloud-hosted and fully-managed database with high availability
   - Built-in authentication and security features
   - Realtime capabilities for live state updates
   - Compatibility with both synchronous and asynchronous operations
   - Support for both full history and shallow storage modes
   - Automatic schema creation and management with migrations






Functions
---------

   get_supabase_client   sanitize_sql
.. autofunction:: get_supabase_client
.. autofunction:: sanitize_sql

Classes
-------

* :py:class:`SupabaseSaver` - A LangGraph-compatible checkpointer implementation using Supabase.* :py:class:`SupabaseCheckpointerConfig` - Configuration for Supabase-based checkpoint persistence.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/persistence/supabase_config/SupabaseSaver   /api_clean/haive/core/persistence/supabase_config/SupabaseCheckpointerConfig

Package Contents
----------------

