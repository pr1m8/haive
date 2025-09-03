
haive.core.engine.vectorstore.providers.SupabaseVectorStoreConfig
=================================================================

.. py:module:: haive.core.engine.vectorstore.providers.SupabaseVectorStoreConfig

.. autoapi-nested-parse::

   Supabase Vector Store implementation for the Haive framework.

   This module provides a configuration class for the Supabase vector store,
   which is a managed PostgreSQL service with built-in pgvector support.

   Supabase provides:
   1. Managed PostgreSQL with pgvector extension
   2. Real-time subscriptions for vector data changes
   3. Built-in authentication and row-level security
   4. Edge functions for vector processing
   5. Dashboard for database management
   6. Global CDN and auto-scaling

   This vector store is particularly useful when:
   - You want managed PostgreSQL without infrastructure overhead
   - Need real-time capabilities with vector data
   - Want built-in authentication and security
   - Building full-stack applications with vector search
   - Need global distribution and edge compute

   The implementation integrates with LangChain's Supabase while providing
   a consistent Haive configuration interface.







Classes
-------

* :py:class:`SupabaseVectorStoreConfig` - Configuration for Supabase vector store in the Haive framework.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/vectorstore/providers/SupabaseVectorStoreConfig/SupabaseVectorStoreConfig

Package Contents
----------------

