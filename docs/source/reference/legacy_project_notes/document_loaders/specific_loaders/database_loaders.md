# Database Loaders in Haive Framework

This document outlines the implementation of database document loaders in the Haive framework.

## Database Loader Options

LangChain provides several database loader implementations, each targeting different database systems:

| Loader              | Database Type | Features                       | Dependencies               |
| ------------------- | ------------- | ------------------------------ | -------------------------- |
| SQLDatabaseLoader   | SQL (generic) | Loads tables, executes queries | sqlalchemy                 |
| MongodbLoader       | MongoDB       | NoSQL document loading         | pymongo                    |
| SnowflakeLoader     | Snowflake     | Data warehouse loading         | snowflake-connector-python |
| BigQueryLoader      | BigQuery      | Google's data warehouse        | google-cloud-bigquery      |
| AstraDBLoader       | AstraDB       | Cassandra-based vector DB      | astrapy                    |
| KineticaLoader      | Kinetica      | GPU-accelerated DB             | gpudb                      |
| SurrealDBLoader     | SurrealDB     | Multi-model database           | surreal-db                 |
| AthenaLoader        | Amazon Athena | AWS query service              | pyathena                   |
| CassandraLoader     | Cassandra     | Wide-column store              | cassandra-driver           |
| CouchbaseLoader     | Couchbase     | NoSQL document DB              | couchbase                  |
| ElasticsearchLoader | Elasticsearch | Search engine DB               | elasticsearch              |
| TiDBLoader          | TiDB          | MySQL-compatible DB            | pymysql                    |
| OracleLoader        | Oracle        | Enterprise database            | oracledb                   |

## Implementation Strategy

Our approach is to create a hierarchy of database sources with a base `DatabaseSource` and specialized sources for specific database types:

```python
@auto_source
class DatabaseSource(RemoteSource):
    """Base class for database sources."""
    connection_string: str
    query: Optional[str] = None
    table_name: Optional[str] = None

    class Config:
        scheme_patterns = [
            'postgresql', 'mysql', 'sqlite', 'mongodb', 'snowflake',
            'bigquery', 'astra', 'oracle', 'elasticsearch'
        ]
```

### Specialized Database Sources

```python
@auto_source(scheme_patterns=["postgresql", "postgres"])
class PostgreSQLSource(DatabaseSource):
    """PostgreSQL database source."""

    class Config:
        loader_strategies = {
            'sql': {
                'class': 'SQLDatabaseLoader',
                'speed': 'medium',
                'quality': 'high',
                'best_for': ['tables', 'queries'],
                'requires_auth': True,
                'required_credentials': ['postgres_credentials']
            }
        }
        required_credentials = ['postgres_credentials']

@auto_source(scheme_patterns=["mongodb", "mongo"])
class MongoDBSource(DatabaseSource):
    """MongoDB database source."""
    collection_name: Optional[str] = None
    filter_criteria: Optional[Dict[str, Any]] = None

    class Config:
        loader_strategies = {
            'mongo': {
                'class': 'MongodbLoader',
                'speed': 'medium',
                'quality': 'high',
                'best_for': ['documents', 'collections'],
                'requires_auth': True,
                'required_credentials': ['mongodb_credentials']
            }
        }
        required_credentials = ['mongodb_credentials']

@auto_source(scheme_patterns=["snowflake"])
class SnowflakeSource(DatabaseSource):
    """Snowflake database source."""

    class Config:
        loader_strategies = {
            'snowflake': {
                'class': 'SnowflakeLoader',
                'speed': 'medium',
                'quality': 'high',
                'best_for': ['data_warehouse'],
                'requires_auth': True,
                'required_credentials': ['snowflake_credentials']
            }
        }
        required_credentials = ['snowflake_credentials']

@auto_source(scheme_patterns=["bigquery"])
class BigQuerySource(DatabaseSource):
    """Google BigQuery database source."""
    project_id: str
    dataset_id: str

    class Config:
        loader_strategies = {
            'bigquery': {
                'class': 'BigQueryLoader',
                'speed': 'slow',
                'quality': 'high',
                'best_for': ['data_warehouse', 'analytics'],
                'requires_auth': True,
                'required_credentials': ['gcp_credentials']
            }
        }
        required_credentials = ['gcp_credentials']
```

## Connection String Parsing

We need to parse different connection string formats:

```python
def parse_connection_string(self):
    """Parse the connection string to extract components."""
    parsed = urlparse(self.connection_string)

    components = {
        'scheme': parsed.scheme,
        'username': parsed.username,
        'password': parsed.password,
        'hostname': parsed.hostname,
        'port': parsed.port,
        'path': parsed.path.lstrip('/'),  # Usually the database name
        'query_params': dict(parse_qsl(parsed.query))
    }

    # Special handling for SQLite
    if parsed.scheme in ['sqlite', 'sqlite3']:
        if parsed.path:
            # Local file path
            components['database_path'] = parsed.path
        else:
            # In-memory database
            components['database_path'] = ':memory:'

    return components
```

## Loader Implementation Details

### SQLDatabaseLoader

```python
def create_sql_loader(self):
    """Create an SQLDatabaseLoader instance."""
    # Import here to avoid dependency issues
    from langchain_community.document_loaders import SQLDatabaseLoader
    from sqlalchemy import create_engine

    # Parse connection components
    components = self.parse_connection_string()

    # Get credentials if needed
    username = components['username']
    password = components['password']

    if not username or not password:
        if self.credential_manager:
            credential_name = f"{components['scheme']}_credentials"
            creds = self.credential_manager.get_credential(credential_name)
            if creds:
                username = creds.get('username', username)
                password = creds.get('password', password)

    # Build engine URL based on database type
    if components['scheme'] in ['sqlite', 'sqlite3']:
        engine_url = f"sqlite:///{components['database_path']}"
    else:
        # Standard SQL databases
        port_str = f":{components['port']}" if components['port'] else ""
        auth_str = f"{username}:{password}@" if username and password else ""
        db_name = components['path'] or ""

        engine_url = f"{components['scheme']}://{auth_str}{components['hostname']}{port_str}/{db_name}"

    # Create SQLAlchemy engine
    engine = create_engine(engine_url)

    # Create loader with query if provided
    if self.query:
        return SQLDatabaseLoader(
            engine=engine,
            query=self.query
        )
    elif self.table_name:
        # Generate query for a specific table
        return SQLDatabaseLoader(
            engine=engine,
            query=f"SELECT * FROM {self.table_name}"
        )
    else:
        # Default behavior: list all tables
        return SQLDatabaseLoader(engine=engine)
```

### MongoDBLoader

```python
def create_mongodb_loader(self):
    """Create a MongoDBLoader instance."""
    # Import here to avoid dependency issues
    from langchain_community.document_loaders import MongodbLoader

    # Parse connection components
    components = self.parse_connection_string()

    # Get credentials if needed
    username = components['username']
    password = components['password']

    if not username or not password:
        if self.credential_manager:
            creds = self.credential_manager.get_credential('mongodb_credentials')
            if creds:
                username = creds.get('username', username)
                password = creds.get('password', password)

    # Build connection string
    auth_str = f"{username}:{password}@" if username and password else ""
    port_str = f":{components['port']}" if components['port'] else ""
    db_name = components['path'] or ""

    connection_string = f"mongodb://{auth_str}{components['hostname']}{port_str}"

    # Create loader
    return MongodbLoader(
        connection_string=connection_string,
        db_name=db_name,
        collection_name=self.collection_name,
        filter_criteria=self.filter_criteria
    )
```

## Database Schema Analysis

We'll implement analysis functions to understand the database structure:

```python
def analyze_sql_database(self):
    """Analyze an SQL database to understand its structure."""
    # Import required libraries
    from sqlalchemy import create_engine, inspect

    # Parse connection components
    components = self.parse_connection_string()

    # Build engine URL
    if components['scheme'] in ['sqlite', 'sqlite3']:
        engine_url = f"sqlite:///{components['database_path']}"
    else:
        # Standard SQL databases (use credentials from self if available)
        username = getattr(self, 'username', components['username'])
        password = getattr(self, 'password', components['password'])
        port_str = f":{components['port']}" if components['port'] else ""
        auth_str = f"{username}:{password}@" if username and password else ""
        db_name = components['path'] or ""

        engine_url = f"{components['scheme']}://{auth_str}{components['hostname']}{port_str}/{db_name}"

    # Create SQLAlchemy engine
    engine = create_engine(engine_url)

    # Initialize analysis results
    analysis = {
        "database_type": components['scheme'],
        "database_name": components['path'],
        "tables": [],
        "has_relationships": False,
        "tables_count": 0,
        "estimated_total_rows": 0,
        "largest_tables": []
    }

    try:
        # Create inspector
        inspector = inspect(engine)

        # Get all table names
        table_names = inspector.get_table_names()
        analysis["tables_count"] = len(table_names)

        # Analyze each table
        table_info = []
        for table_name in table_names:
            # Get columns
            columns = inspector.get_columns(table_name)

            # Get primary key
            pk = inspector.get_pk_constraint(table_name)

            # Get foreign keys
            fks = inspector.get_foreign_keys(table_name)
            if fks:
                analysis["has_relationships"] = True

            # Get row count (approximate)
            row_count = 0
            try:
                result = engine.execute(f"SELECT COUNT(*) FROM {table_name}")
                row_count = result.scalar()
            except:
                pass

            # Add to tables list
            table_info.append({
                "name": table_name,
                "columns_count": len(columns),
                "column_names": [col['name'] for col in columns],
                "primary_key": pk['constrained_columns'] if pk else [],
                "foreign_keys": [fk['constrained_columns'] for fk in fks],
                "references": [fk['referred_table'] for fk in fks],
                "row_count": row_count
            })

            # Update total rows
            analysis["estimated_total_rows"] += row_count

        # Sort tables by row count
        table_info.sort(key=lambda x: x["row_count"], reverse=True)
        analysis["tables"] = table_info

        # Get largest tables
        analysis["largest_tables"] = [t["name"] for t in table_info[:5]]

        return analysis

    except Exception as e:
        return {
            "error": str(e),
            "database_type": components['scheme'],
            "database_name": components['path']
        }
```

## Query Generation

For SQL databases, we'll implement query generation based on the schema:

```python
def generate_table_query(self, table_name, limit=100):
    """Generate a query for a table with intelligent column selection."""
    # Import required libraries
    from sqlalchemy import create_engine, inspect

    # Parse connection and create engine
    components = self.parse_connection_string()

    # Build engine URL (simplified from above)
    engine_url = self._build_engine_url(components)
    engine = create_engine(engine_url)

    # Inspect the table
    inspector = inspect(engine)
    columns = inspector.get_columns(table_name)

    # Intelligent column selection
    selected_columns = []

    # Always include primary key
    pk = inspector.get_pk_constraint(table_name)
    pk_columns = pk['constrained_columns'] if pk else []
    selected_columns.extend(pk_columns)

    # Add other important columns based on name patterns
    important_patterns = [
        'name', 'title', 'description', 'content', 'text',
        'date', 'time', 'created', 'modified', 'updated',
        'id', 'code', 'type', 'status', 'category'
    ]

    for col in columns:
        col_name = col['name'].lower()
        if any(pattern in col_name for pattern in important_patterns):
            if col['name'] not in selected_columns:
                selected_columns.append(col['name'])

    # Add remaining columns if needed (up to a reasonable limit)
    max_columns = 20
    for col in columns:
        if len(selected_columns) >= max_columns:
            break
        if col['name'] not in selected_columns:
            selected_columns.append(col['name'])

    # Build the query
    columns_str = ", ".join(selected_columns)
    query = f"SELECT {columns_str} FROM {table_name} LIMIT {limit}"

    return query
```

## Authentication Handling

Database connections require careful credential management:

```python
def authenticate_sql(self, credential_manager):
    """Authenticate for SQL database access."""
    if not credential_manager:
        return False

    # Parse connection to determine database type
    components = self.parse_connection_string()
    db_type = components['scheme']

    # Get credentials for this database type
    credential_name = f"{db_type}_credentials"
    creds = credential_manager.get_credential(credential_name)

    if not creds:
        return False

    # Store credentials
    self.username = creds.get('username')
    self.password = creds.get('password')
    self.is_authenticated = bool(self.username and self.password)

    return self.is_authenticated
```

## Connection Pooling and Management

For efficiency, we'll implement connection pooling:

```python
class ConnectionManager:
    """Manages database connections with pooling."""

    # Class-level connection pools
    _engine_pools = {}

    @classmethod
    def get_engine(cls, connection_string, credentials=None):
        """Get or create a database engine with connection pooling."""
        from sqlalchemy import create_engine
        from sqlalchemy.pool import QueuePool

        # Build a key for the connection
        conn_key = connection_string
        if credentials:
            conn_key += str(hash(frozenset(credentials.items())))

        # Return existing engine if available
        if conn_key in cls._engine_pools:
            return cls._engine_pools[conn_key]

        # Parse connection string
        components = cls._parse_connection_string(connection_string)

        # Build engine URL with credentials
        engine_url = cls._build_engine_url(components, credentials)

        # Create engine with connection pooling
        engine = create_engine(
            engine_url,
            poolclass=QueuePool,
            pool_size=5,
            max_overflow=10,
            pool_timeout=30,
            pool_recycle=1800  # Recycle connections after 30 minutes
        )

        # Store in pool
        cls._engine_pools[conn_key] = engine

        return engine

    @classmethod
    def close_all(cls):
        """Close all connection pools."""
        for engine in cls._engine_pools.values():
            engine.dispose()
        cls._engine_pools.clear()

    @staticmethod
    def _parse_connection_string(connection_string):
        """Parse a connection string into components."""
        # Implementation as above

    @staticmethod
    def _build_engine_url(components, credentials=None):
        """Build an SQLAlchemy engine URL from components and credentials."""
        # Implementation as above
```

## Full Implementation

The complete database loader implementation will include:

1. Base `DatabaseSource` class
2. Specialized sources for different database types
3. Connection string parsing
4. Schema analysis capabilities
5. Query generation
6. Authentication handling
7. Connection pooling

This provides a robust and flexible approach to database loading that can adapt to different database systems.

## Usage Examples

### Basic SQL Usage

```python
from haive.document_loaders import PostgreSQLSource, CredentialManager

# Create a credential manager
credential_manager = CredentialManager()

# Add PostgreSQL credentials
credential_manager.store_credential(
    "postgres_credentials",
    {
        "type": "database",
        "username": "user",
        "password": "pass"
    }
)

# Create PostgreSQL source
pg_source = PostgreSQLSource(
    connection_string="postgresql://localhost:5432/mydb",
    table_name="customers"
)

# Authenticate
pg_source.authenticate(credential_manager)

# Load table data
documents = pg_source.load_documents()
```

### With Custom Query

```python
# With a specific query
pg_source = PostgreSQLSource(
    connection_string="postgresql://localhost:5432/mydb",
    query="SELECT id, name, email, created_at FROM customers WHERE status = 'active'"
)

# Authenticate and load
pg_source.authenticate(credential_manager)
documents = pg_source.load_documents()
```

### MongoDB Example

```python
from haive.document_loaders import MongoDBSource

# Create MongoDB source
mongo_source = MongoDBSource(
    connection_string="mongodb://localhost:27017/mydb",
    collection_name="products",
    filter_criteria={"category": "electronics"}
)

# Authenticate and load
mongo_source.authenticate(credential_manager)
documents = mongo_source.load_documents()
```

### Schema Analysis

```python
# Analyze database schema
schema = pg_source.analyze_sql_database()

# Generate queries based on schema
for table in schema["largest_tables"]:
    query = pg_source.generate_table_query(table, limit=50)
    print(f"Query for {table}: {query}")
```

## Conclusion

This implementation provides a comprehensive approach to database loading that leverages all available LangChain loaders while adding intelligent schema analysis, query generation, and connection management capabilities.

## Status

- ⬜ Core `DatabaseSource` implementation
- ⬜ Specialized database sources
- ⬜ Connection string parsing
- ⬜ Schema analysis functions
- ⬜ Query generation
- ⬜ Authentication handling
- ⬜ Connection pooling
- ⬜ Testing and validation
