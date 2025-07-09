# VectorStore Module Changelog

## 2025-06-19: Enhanced Vector Store Providers

### Added

- Added 12 new vector store providers to the VectorStoreProvider enum:
  - PGVECTOR: PostgreSQL with pgvector extension
  - ELASTICSEARCH: Elasticsearch vector search
  - REDIS: Redis vector database
  - SUPABASE: Supabase vector store
  - MONGODB_ATLAS: MongoDB Atlas vector search
  - AZURE_SEARCH: Azure Cognitive Search
  - OPENSEARCH: OpenSearch vector search
  - CASSANDRA: Apache Cassandra vector store
  - CLICKHOUSE: ClickHouse vector database
  - TYPESENSE: Typesense vector search
  - LANCEDB: LanceDB vector database
  - NEO4J: Neo4j vector search

- Added corresponding import implementations in the \_get_vectorstore_class method for all new providers

- Added comprehensive test suite for vector store providers:
  - Tests for provider enum values
  - Tests for provider registry
  - Tests for custom provider registration
  - Tests for provider factory functions

- Updated documentation to include the new providers in the README.md

### Fixed

- Fixed import issues in the main engine module to ensure all vector store functions are properly exported

### Future Improvements

- Add specific configuration models for each vector store provider
- Implement dedicated testing for each provider type
- Add examples for the new vector store providers
- Enhance error handling for provider-specific issues
