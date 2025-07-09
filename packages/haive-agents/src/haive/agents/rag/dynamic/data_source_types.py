from enum import Enum


class DataSourceType(str, Enum):
    """Types of data sources available."""

    VECTOR_DB = "vector_db"
    GRAPH_DB = "graph_db"
    WEB_SEARCH = "web_search"
    SQL_DB = "sql_db"
    API = "api"
    DOCUMENT_STORE = "document_store"
