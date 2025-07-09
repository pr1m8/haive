"""Database source registrations with connection string auto-detection.

This module implements comprehensive database loaders from langchain_community
including SQL, NoSQL, Graph databases, and Data Warehouses with intelligent
connection string detection and query optimization.
"""

from enum import Enum
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

from pydantic import Field, validator

from .enhanced_registry import (
    enhanced_registry,
    register_database_source,
)
from .source_types import BaseSource, LoaderCapability


class DatabaseType(str, Enum):
    """Database types supported."""

    # SQL Databases
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
    SQLITE = "sqlite"
    MSSQL = "mssql"
    ORACLE = "oracle"

    # NoSQL Databases
    MONGODB = "mongodb"
    CASSANDRA = "cassandra"
    COUCHBASE = "couchbase"
    ELASTICSEARCH = "elasticsearch"

    # Graph Databases
    NEO4J = "neo4j"
    ARANGODB = "arangodb"
    TIGERGRAPH = "tigergraph"
    NEPTUNE = "neptune"

    # Data Warehouses
    BIGQUERY = "bigquery"
    SNOWFLAKE = "snowflake"
    REDSHIFT = "redshift"
    DATABRICKS = "databricks"


class QueryType(str, Enum):
    """Query types for database sources."""

    SELECT = "select"
    AGGREGATE = "aggregate"
    JOIN = "join"
    PROCEDURE = "procedure"
    CUSTOM = "custom"


class LoadingStrategy(str, Enum):
    """Loading strategies for documents."""

    LOAD = "load"  # Standard load() method
    LOAD_AND_SPLIT = "load_and_split"  # Load and split into chunks
    LAZY_LOAD = "lazy_load"  # Lazy loading with iterator
    FETCH_ALL = "fetch_all"  # Fetch all tables/collections
    SCRAPE_ALL = "scrape_all"  # Comprehensive database scraping


class TextSplitterType(str, Enum):
    """Text splitter types for load_and_split."""

    RECURSIVE_CHARACTER = "recursive_character"
    CHARACTER = "character"
    TOKEN = "token"
    MARKDOWN = "markdown"
    PYTHON_CODE = "python_code"
    HTML = "html"
    CUSTOM = "custom"


# =============================================================================
# Connection String Analysis
# =============================================================================


def detect_database_type(connection_string: str) -> Optional[DatabaseType]:
    """Auto-detect database type from connection string."""
    connection_patterns = {
        # SQL databases
        "postgresql://": DatabaseType.POSTGRESQL,
        "postgres://": DatabaseType.POSTGRESQL,
        "mysql://": DatabaseType.MYSQL,
        "mysql+pymysql://": DatabaseType.MYSQL,
        "sqlite:///": DatabaseType.SQLITE,
        "sqlite://": DatabaseType.SQLITE,
        "mssql://": DatabaseType.MSSQL,
        "oracle://": DatabaseType.ORACLE,
        # NoSQL databases
        "mongodb://": DatabaseType.MONGODB,
        "mongodb+srv://": DatabaseType.MONGODB,
        "cassandra://": DatabaseType.CASSANDRA,
        "couchbase://": DatabaseType.COUCHBASE,
        "elasticsearch://": DatabaseType.ELASTICSEARCH,
        # Graph databases
        "neo4j://": DatabaseType.NEO4J,
        "neo4j+s://": DatabaseType.NEO4J,
        "bolt://": DatabaseType.NEO4J,
        "http+arangodb://": DatabaseType.ARANGODB,
        "tigergraph://": DatabaseType.TIGERGRAPH,
        "neptune://": DatabaseType.NEPTUNE,
        # Data warehouses
        "bigquery://": DatabaseType.BIGQUERY,
        "snowflake://": DatabaseType.SNOWFLAKE,
        "redshift://": DatabaseType.REDSHIFT,
        "databricks://": DatabaseType.DATABRICKS,
    }

    connection_lower = connection_string.lower()
    for pattern, db_type in connection_patterns.items():
        if connection_lower.startswith(pattern):
            return db_type

    return None


def extract_database_metadata(connection_string: str) -> Dict[str, Any]:
    """Extract metadata from database connection string."""
    try:
        parsed = urlparse(connection_string)
        return {
            "scheme": parsed.scheme,
            "host": parsed.hostname,
            "port": parsed.port,
            "database": parsed.path.lstrip("/") if parsed.path else None,
            "username": parsed.username,
            "has_password": bool(parsed.password),
            "query_params": dict(
                param.split("=") for param in parsed.query.split("&") if "=" in param
            ),
        }
    except Exception:
        return {"raw_connection": connection_string}


# =============================================================================
# Base Database Source
# =============================================================================


class DatabaseSource(BaseSource):
    """Base class for database sources."""

    connection_string: str = Field(..., description="Database connection string")
    query: Optional[str] = Field(None, description="SQL query to execute")
    table_name: Optional[str] = Field(None, description="Table name to query")

    # Query configuration
    query_type: QueryType = QueryType.SELECT
    limit: Optional[int] = Field(None, ge=1, description="Maximum rows to return")

    # Processing options
    include_columns: Optional[List[str]] = Field(None, description="Columns to include")
    exclude_columns: Optional[List[str]] = Field(None, description="Columns to exclude")

    # Loading strategy
    loading_strategy: LoadingStrategy = Field(
        LoadingStrategy.LOAD, description="Document loading strategy"
    )
    lazy_load: bool = Field(False, description="Enable lazy loading for large datasets")

    # Bulk/fetch all configuration
    fetch_all_tables: bool = Field(
        False, description="Fetch all tables in database (for fetch_all strategy)"
    )
    fetch_all_collections: bool = Field(
        False, description="Fetch all collections (for NoSQL)"
    )
    include_system_tables: bool = Field(
        False, description="Include system/metadata tables"
    )
    table_pattern: Optional[str] = Field(
        None, description="Regex pattern for table names to include"
    )
    exclude_tables: List[str] = Field(
        default_factory=list, description="Tables to exclude from bulk operations"
    )
    max_tables: Optional[int] = Field(
        None, ge=1, description="Maximum number of tables to process"
    )

    # Text splitting configuration (for load_and_split)
    text_splitter_type: TextSplitterType = Field(
        TextSplitterType.RECURSIVE_CHARACTER, description="Text splitter type"
    )
    chunk_size: int = Field(1000, ge=100, description="Chunk size for text splitting")
    chunk_overlap: int = Field(
        200, ge=0, description="Chunk overlap for text splitting"
    )
    separators: Optional[List[str]] = Field(
        None, description="Custom separators for splitting"
    )

    # Connection options
    timeout: int = Field(30, ge=1, description="Query timeout in seconds")
    retry_attempts: int = Field(3, ge=1, description="Number of retry attempts")

    @validator("connection_string")
    def validate_connection_string(cls, v):
        """Validate connection string format."""
        if not v or not isinstance(v, str):
            raise ValueError("Connection string must be a non-empty string")

        # Check for basic URL format
        if "://" not in v:
            raise ValueError("Connection string must contain '://' protocol separator")

        return v

    @property
    def database_type(self) -> Optional[DatabaseType]:
        """Auto-detect database type from connection string."""
        return detect_database_type(self.connection_string)

    @property
    def database_metadata(self) -> Dict[str, Any]:
        """Extract metadata from connection string."""
        return extract_database_metadata(self.connection_string)

    def get_text_splitter_config(self) -> Dict[str, Any]:
        """Get text splitter configuration for load_and_split."""
        config = {"chunk_size": self.chunk_size, "chunk_overlap": self.chunk_overlap}

        # Add custom separators if provided
        if self.separators:
            config["separators"] = self.separators

        # Add splitter-specific configuration
        if self.text_splitter_type == TextSplitterType.TOKEN:
            config["encoding_name"] = "cl100k_base"  # Default for OpenAI
        elif self.text_splitter_type == TextSplitterType.MARKDOWN:
            config["strip_headers"] = False
        elif self.text_splitter_type == TextSplitterType.PYTHON_CODE:
            config["language"] = "python"

        return config

    def get_loading_method(self) -> str:
        """Get the appropriate loading method based on strategy."""
        if self.loading_strategy == LoadingStrategy.LOAD_AND_SPLIT:
            return "load_and_split"
        elif self.loading_strategy == LoadingStrategy.LAZY_LOAD:
            return "lazy_load"
        elif self.loading_strategy == LoadingStrategy.FETCH_ALL:
            return "fetch_all"
        elif self.loading_strategy == LoadingStrategy.SCRAPE_ALL:
            return "scrape_all"
        else:
            return "load"

    def get_fetch_all_config(self) -> Dict[str, Any]:
        """Get configuration for fetch_all/scrape_all operations."""
        config = {
            "fetch_all_tables": self.fetch_all_tables,
            "fetch_all_collections": self.fetch_all_collections,
            "include_system_tables": self.include_system_tables,
            "max_tables": self.max_tables,
        }

        if self.table_pattern:
            config["table_pattern"] = self.table_pattern

        if self.exclude_tables:
            config["exclude_tables"] = self.exclude_tables

        return config

    def get_loader_kwargs(self) -> Dict[str, Any]:
        """Get loader arguments for database sources."""
        kwargs = {"connection_string": self.connection_string, "timeout": self.timeout}

        # Add query or table
        if self.query:
            kwargs["query"] = self.query
        elif self.table_name:
            kwargs["table_name"] = self.table_name

        # Add column filtering
        if self.include_columns:
            kwargs["include_columns"] = self.include_columns
        if self.exclude_columns:
            kwargs["exclude_columns"] = self.exclude_columns

        # Add limit
        if self.limit:
            kwargs["limit"] = self.limit

        # Add loading strategy configuration
        kwargs["loading_method"] = self.get_loading_method()
        kwargs["lazy_load"] = self.lazy_load

        # Add text splitter configuration for load_and_split
        if self.loading_strategy == LoadingStrategy.LOAD_AND_SPLIT:
            kwargs["text_splitter_config"] = self.get_text_splitter_config()
            kwargs["text_splitter_type"] = self.text_splitter_type.value

        # Add fetch_all/scrape_all configuration
        if self.loading_strategy in [
            LoadingStrategy.FETCH_ALL,
            LoadingStrategy.SCRAPE_ALL,
        ]:
            kwargs.update(self.get_fetch_all_config())

        return kwargs


# =============================================================================
# SQL Database Sources
# =============================================================================


@register_database_source(
    name="postgresql",
    database_type=DatabaseType.POSTGRESQL,
    loaders={
        "sql": {
            "class": "SQLDatabaseLoader",
            "speed": "fast",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["psycopg2-binary"],
        },
        "fetch_all": {
            "class": "SQLDatabaseLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["psycopg2-binary"],
            "supports_fetch_all": True,
        },
    },
    default_loader="sql",
    description="PostgreSQL database loader with fetch-all-tables support",
    capabilities=[LoaderCapability.BULK_LOADING, LoaderCapability.FILTERING],
    priority=9,
)
class PostgreSQLSource(DatabaseSource):
    """PostgreSQL database source."""

    # PostgreSQL-specific options
    schema_name: Optional[str] = Field(None, description="Database schema name")
    use_prepared_statements: bool = Field(True, description="Use prepared statements")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        if self.schema_name:
            kwargs["schema"] = self.schema_name

        kwargs.update({"use_prepared_statements": self.use_prepared_statements})

        return kwargs


@register_database_source(
    name="mysql",
    database_type=DatabaseType.MYSQL,
    loaders={
        "sql": {
            "class": "SQLDatabaseLoader",
            "speed": "fast",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["PyMySQL"],
        }
    },
    default_loader="sql",
    description="MySQL database loader with optimization features",
    capabilities=[LoaderCapability.BULK_LOADING, LoaderCapability.FILTERING],
    priority=9,
)
class MySQLSource(DatabaseSource):
    """MySQL database source."""

    # MySQL-specific options
    charset: str = Field("utf8mb4", description="Character set")
    autocommit: bool = Field(True, description="Auto-commit transactions")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()
        kwargs.update({"charset": self.charset, "autocommit": self.autocommit})
        return kwargs


@register_database_source(
    name="sqlite",
    database_type=DatabaseType.SQLITE,
    loaders={
        "sql": {
            "class": "SQLDatabaseLoader",
            "speed": "fast",
            "quality": "high",
            "module": "langchain_community.document_loaders",
        }
    },
    default_loader="sql",
    description="SQLite database loader for local databases",
    capabilities=[LoaderCapability.BULK_LOADING, LoaderCapability.FILTERING],
    priority=8,
)
class SQLiteSource(DatabaseSource):
    """SQLite database source."""

    # SQLite-specific options
    check_same_thread: bool = Field(False, description="Check same thread")
    isolation_level: Optional[str] = Field(None, description="Isolation level")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()
        kwargs.update(
            {
                "check_same_thread": self.check_same_thread,
                "isolation_level": self.isolation_level,
            }
        )
        return kwargs


# =============================================================================
# NoSQL Database Sources
# =============================================================================


@register_database_source(
    name="mongodb",
    database_type=DatabaseType.MONGODB,
    loaders={
        "mongo": {
            "class": "MongodbLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["pymongo"],
        },
        "fetch_all": {
            "class": "MongodbLoader",
            "speed": "slow",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["pymongo"],
            "supports_fetch_all": True,
        },
    },
    default_loader="mongo",
    description="MongoDB document database loader with fetch-all-collections support",
    capabilities=[LoaderCapability.BULK_LOADING, LoaderCapability.FILTERING],
    priority=9,
)
class MongoDBSource(DatabaseSource):
    """MongoDB database source."""

    # MongoDB-specific options
    collection_name: str = Field(..., description="Collection name")
    filter_criteria: Optional[Dict[str, Any]] = Field(
        None, description="MongoDB filter"
    )
    field_names: Optional[List[str]] = Field(None, description="Fields to include")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        # Replace generic query with MongoDB-specific parameters
        kwargs.pop("query", None)
        kwargs.pop("table_name", None)

        kwargs.update(
            {
                "collection_name": self.collection_name,
                "filter_criteria": self.filter_criteria or {},
                "field_names": self.field_names,
            }
        )

        return kwargs


@register_database_source(
    name="cassandra",
    database_type=DatabaseType.CASSANDRA,
    loaders={
        "cassandra": {
            "class": "CassandraLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["cassandra-driver"],
        }
    },
    default_loader="cassandra",
    description="Apache Cassandra database loader",
    capabilities=[LoaderCapability.BULK_LOADING, LoaderCapability.FILTERING],
    priority=8,
)
class CassandraSource(DatabaseSource):
    """Cassandra database source."""

    # Cassandra-specific options
    keyspace: str = Field(..., description="Keyspace name")
    consistency_level: str = Field("ONE", description="Consistency level")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()
        kwargs.update(
            {"keyspace": self.keyspace, "consistency_level": self.consistency_level}
        )
        return kwargs


@register_database_source(
    name="elasticsearch",
    database_type=DatabaseType.ELASTICSEARCH,
    loaders={
        "elasticsearch": {
            "class": "ElasticsearchLoader",
            "speed": "fast",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["elasticsearch"],
        }
    },
    default_loader="elasticsearch",
    description="Elasticsearch search engine loader",
    capabilities=[
        LoaderCapability.BULK_LOADING,
        LoaderCapability.FILTERING,
        LoaderCapability.ASYNC_PROCESSING,
    ],
    priority=9,
)
class ElasticsearchSource(DatabaseSource):
    """Elasticsearch source."""

    # Elasticsearch-specific options
    index_name: str = Field(..., description="Index name")
    query_body: Optional[Dict[str, Any]] = Field(
        None, description="Elasticsearch query body"
    )
    scroll_size: int = Field(1000, ge=1, description="Scroll size for pagination")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        # Replace generic query with Elasticsearch-specific parameters
        kwargs.pop("query", None)
        kwargs.pop("table_name", None)

        kwargs.update(
            {
                "index_name": self.index_name,
                "query": self.query_body or {"match_all": {}},
                "scroll_size": self.scroll_size,
            }
        )

        return kwargs


# =============================================================================
# Graph Database Sources
# =============================================================================


@register_database_source(
    name="neo4j",
    database_type=DatabaseType.NEO4J,
    loaders={
        "neo4j": {
            "class": "Neo4jLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["neo4j"],
        }
    },
    default_loader="neo4j",
    description="Neo4j graph database loader with Cypher support",
    capabilities=[LoaderCapability.BULK_LOADING, LoaderCapability.FILTERING],
    priority=9,
)
class Neo4jSource(DatabaseSource):
    """Neo4j graph database source."""

    # Neo4j-specific options
    cypher_query: Optional[str] = Field(None, description="Cypher query")
    node_label: Optional[str] = Field(None, description="Node label to query")
    relationship_type: Optional[str] = Field(None, description="Relationship type")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        # Use Cypher query if provided, otherwise generic query
        if self.cypher_query:
            kwargs["query"] = self.cypher_query
        elif self.node_label:
            kwargs["query"] = f"MATCH (n:{self.node_label}) RETURN n"

        return kwargs


@register_database_source(
    name="arangodb",
    database_type=DatabaseType.ARANGODB,
    loaders={
        "arango": {
            "class": "ArangoDBLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["python-arango"],
        }
    },
    default_loader="arango",
    description="ArangoDB multi-model database loader",
    capabilities=[LoaderCapability.BULK_LOADING, LoaderCapability.FILTERING],
    priority=8,
)
class ArangoDBSource(DatabaseSource):
    """ArangoDB multi-model database source."""

    # ArangoDB-specific options
    database_name: str = Field(..., description="Database name")
    collection_name: Optional[str] = Field(None, description="Collection name")
    aql_query: Optional[str] = Field(None, description="AQL query")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update(
            {
                "database_name": self.database_name,
                "collection_name": self.collection_name,
            }
        )

        if self.aql_query:
            kwargs["query"] = self.aql_query

        return kwargs


# =============================================================================
# Data Warehouse Sources
# =============================================================================


@register_database_source(
    name="bigquery",
    database_type=DatabaseType.BIGQUERY,
    loaders={
        "bigquery": {
            "class": "BigQueryLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["google-cloud-bigquery"],
        }
    },
    default_loader="bigquery",
    description="Google BigQuery data warehouse loader",
    capabilities=[
        LoaderCapability.BULK_LOADING,
        LoaderCapability.FILTERING,
        LoaderCapability.ASYNC_PROCESSING,
    ],
    priority=9,
)
class BigQuerySource(DatabaseSource):
    """Google BigQuery data warehouse source."""

    # BigQuery-specific options
    project_id: str = Field(..., description="Google Cloud project ID")
    dataset_id: Optional[str] = Field(None, description="Dataset ID")
    use_legacy_sql: bool = Field(False, description="Use legacy SQL")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update(
            {
                "project": self.project_id,
                "dataset": self.dataset_id,
                "use_legacy_sql": self.use_legacy_sql,
            }
        )

        return kwargs


@register_database_source(
    name="snowflake",
    database_type=DatabaseType.SNOWFLAKE,
    loaders={
        "snowflake": {
            "class": "SnowflakeLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["snowflake-connector-python"],
        }
    },
    default_loader="snowflake",
    description="Snowflake cloud data warehouse loader",
    capabilities=[LoaderCapability.BULK_LOADING, LoaderCapability.FILTERING],
    priority=9,
)
class SnowflakeSource(DatabaseSource):
    """Snowflake cloud data warehouse source."""

    # Snowflake-specific options
    account: str = Field(..., description="Snowflake account")
    warehouse: Optional[str] = Field(None, description="Warehouse name")
    database: Optional[str] = Field(None, description="Database name")
    schema: Optional[str] = Field(None, description="Schema name")
    role: Optional[str] = Field(None, description="Role name")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update(
            {
                "account": self.account,
                "warehouse": self.warehouse,
                "database": self.database,
                "schema": self.schema,
                "role": self.role,
            }
        )

        return kwargs


# =============================================================================
# Utility Functions
# =============================================================================


def get_database_sources_statistics() -> Dict[str, Any]:
    """Get statistics about database sources."""
    registry = enhanced_registry

    # Count by database type
    sql_sources = 0
    nosql_sources = 0
    graph_sources = 0
    warehouse_sources = 0

    for _name, registration in registry._sources.items():
        if hasattr(registration, "database_type"):
            db_type = registration.database_type
            if db_type in [
                DatabaseType.POSTGRESQL,
                DatabaseType.MYSQL,
                DatabaseType.SQLITE,
            ]:
                sql_sources += 1
            elif db_type in [
                DatabaseType.MONGODB,
                DatabaseType.CASSANDRA,
                DatabaseType.ELASTICSEARCH,
            ]:
                nosql_sources += 1
            elif db_type in [DatabaseType.NEO4J, DatabaseType.ARANGODB]:
                graph_sources += 1
            elif db_type in [DatabaseType.BIGQUERY, DatabaseType.SNOWFLAKE]:
                warehouse_sources += 1

    return {
        "sql_sources": sql_sources,
        "nosql_sources": nosql_sources,
        "graph_sources": graph_sources,
        "warehouse_sources": warehouse_sources,
        "total_database_sources": sql_sources
        + nosql_sources
        + graph_sources
        + warehouse_sources,
        "connection_auto_detection": True,
        "supported_database_types": len(DatabaseType),
        "bulk_loading_support": len(
            registry.find_sources_with_capability(LoaderCapability.BULK_LOADING)
        ),
    }


def validate_database_sources() -> bool:
    """Validate database source registrations."""
    registry = enhanced_registry

    required_database_sources = [
        "postgresql",
        "mysql",
        "sqlite",
        "mongodb",
        "cassandra",
        "elasticsearch",
        "neo4j",
        "bigquery",
        "snowflake",
    ]

    missing = []
    for source_name in required_database_sources:
        if source_name not in registry._sources:
            missing.append(source_name)

    if missing:
        print(f"Missing database sources: {missing}")
        return False

    print(
        f"✅ All {len(required_database_sources)} essential database sources registered!"
    )
    return True


def test_connection_string_detection():
    """Test connection string auto-detection."""
    test_connections = {
        "postgresql://user:pass@host:5432/db": DatabaseType.POSTGRESQL,
        "mysql://user:pass@host:3306/db": DatabaseType.MYSQL,
        "sqlite:///path/to/db.sqlite": DatabaseType.SQLITE,
        "mongodb://user:pass@host:27017/db": DatabaseType.MONGODB,
        "neo4j://user:pass@host:7687": DatabaseType.NEO4J,
        "bigquery://project/dataset": DatabaseType.BIGQUERY,
        "snowflake://account/database": DatabaseType.SNOWFLAKE,
    }

    print("🔍 Testing connection string detection:")
    for conn_str, expected_type in test_connections.items():
        detected = detect_database_type(conn_str)
        status = "✅" if detected == expected_type else "❌"
        print(f"  {status} {conn_str} → {detected}")

    return all(
        detect_database_type(conn) == expected
        for conn, expected in test_connections.items()
    )


# Auto-validate on import
if __name__ == "__main__":
    validate_database_sources()
    stats = get_database_sources_statistics()
    print(f"Database Sources Statistics: {stats}")
    test_connection_string_detection()
