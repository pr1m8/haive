
haive.core.engine.vectorstore.providers.CassandraVectorStoreConfig
==================================================================

.. py:module:: haive.core.engine.vectorstore.providers.CassandraVectorStoreConfig

.. autoapi-nested-parse::

   Cassandra Vector Store implementation for the Haive framework.

   This module provides a configuration class for the Cassandra vector store,
   which provides distributed vector storage with Apache Cassandra.

   Cassandra provides:
   1. Distributed vector storage across multiple nodes
   2. High availability and fault tolerance
   3. Linear scalability for vector workloads
   4. Native vector search capabilities
   5. Integration with DataStax Astra DB
   6. ACID transactions with vector operations

   This vector store is particularly useful when:
   - You need distributed vector storage at scale
   - Want high availability for vector data
   - Building applications requiring linear scalability
   - Need integration with existing Cassandra infrastructure
   - Require fault-tolerant vector operations

   The implementation integrates with LangChain's Cassandra while providing
   a consistent Haive configuration interface.







Classes
-------

* :py:class:`CassandraVectorStoreConfig` - Configuration for Cassandra vector store in the Haive framework.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/vectorstore/providers/CassandraVectorStoreConfig/CassandraVectorStoreConfig

Package Contents
----------------

