
haive.core.engine.document.loaders.sources.database_sources
===========================================================

.. py:module:: haive.core.engine.document.loaders.sources.database_sources

.. autoapi-nested-parse::

   Database source registrations with connection string auto-detection.

   This module implements comprehensive database loaders from langchain_community
   including SQL, NoSQL, Graph databases, and Data Warehouses with intelligent
   connection string detection and query optimization.






Functions
---------

   detect_database_type   extract_database_metadata   get_database_sources_statistics   validate_database_sources   test_connection_string_detection
.. autofunction:: detect_database_type
.. autofunction:: extract_database_metadata
.. autofunction:: get_database_sources_statistics
.. autofunction:: validate_database_sources
.. autofunction:: test_connection_string_detection

Classes
-------

* :py:class:`DatabaseType` - Database types supported.* :py:class:`QueryType` - Query types for database sources.* :py:class:`LoadingStrategy` - Loading strategies for documents.* :py:class:`TextSplitterType` - Text splitter types for load_and_split.* :py:class:`DatabaseSource` - Base class for database sources.* :py:class:`PostgreSQLSource` - PostgreSQL database source.* :py:class:`MySQLSource` - MySQL database source.* :py:class:`SQLiteSource` - SQLite database source.* :py:class:`MongoDBSource` - MongoDB database source.* :py:class:`CassandraSource` - Cassandra database source.* :py:class:`ElasticsearchSource` - Elasticsearch source.* :py:class:`Neo4jSource` - Neo4j graph database source.* :py:class:`ArangoDBSource` - ArangoDB multi-model database source.* :py:class:`BigQuerySource` - Google BigQuery data warehouse source.* :py:class:`SnowflakeSource` - Snowflake cloud data warehouse source.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/document/loaders/sources/database_sources/DatabaseType   /api_clean/haive/core/engine/document/loaders/sources/database_sources/QueryType   /api_clean/haive/core/engine/document/loaders/sources/database_sources/LoadingStrategy   /api_clean/haive/core/engine/document/loaders/sources/database_sources/TextSplitterType   /api_clean/haive/core/engine/document/loaders/sources/database_sources/DatabaseSource   /api_clean/haive/core/engine/document/loaders/sources/database_sources/PostgreSQLSource   /api_clean/haive/core/engine/document/loaders/sources/database_sources/MySQLSource   /api_clean/haive/core/engine/document/loaders/sources/database_sources/SQLiteSource   /api_clean/haive/core/engine/document/loaders/sources/database_sources/MongoDBSource   /api_clean/haive/core/engine/document/loaders/sources/database_sources/CassandraSource   /api_clean/haive/core/engine/document/loaders/sources/database_sources/ElasticsearchSource   /api_clean/haive/core/engine/document/loaders/sources/database_sources/Neo4jSource   /api_clean/haive/core/engine/document/loaders/sources/database_sources/ArangoDBSource   /api_clean/haive/core/engine/document/loaders/sources/database_sources/BigQuerySource   /api_clean/haive/core/engine/document/loaders/sources/database_sources/SnowflakeSource

Package Contents
----------------

