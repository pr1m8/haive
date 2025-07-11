"""Database Loaders for Document Engine.

This module implements database loaders for MongoDB, PostgreSQL, and other databases
adapted for the document engine framework.
"""

import logging
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

from langchain_core.document_loaders.base import BaseLoader

from haive.core.engine.document.loaders.sources.implementation import (
    CredentialType,
    DatabaseSource,
)

logger = logging.getLogger(__name__)


class MongoDBSource(DatabaseSource):
    """MongoDB database source implementation."""

    def __init__(
        self,
        connection_string: str,
        database_name: Optional[str] = None,
        collection_name: Optional[str] = None,
        filter_criteria: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        super().__init__(source_path=connection_string, **kwargs)
        self.connection_string = connection_string
        self.database_name = database_name
        self.collection_name = collection_name
        self.filter_criteria = filter_criteria or {}

    def can_handle(self, path: str) -> bool:
        """Check if this is a MongoDB connection string."""
        try:
            parsed = urlparse(path)
            return parsed.scheme in ["mongodb", "mongo"]
        except Exception:
            return False

    def get_confidence_score(self, path: str) -> float:
        """Get confidence score for MongoDB connections."""
        if not self.can_handle(path):
            return 0.0
        return 0.9

    def requires_authentication(self) -> bool:
        """MongoDB typically requires authentication."""
        return True

    def get_credential_requirements(self) -> List[CredentialType]:
        """MongoDB needs connection credentials."""
        return [CredentialType.USERNAME_PASSWORD, CredentialType.CONNECTION_STRING]

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a MongoDB loader."""
        try:
            from langchain_community.document_loaders import MongodbLoader

            # Parse connection components
            parsed = urlparse(self.connection_string)

            # Get credentials if needed
            username = parsed.username
            password = parsed.password

            if not (username and password) and self.credential_manager:
                cred = self.credential_manager.get_credential("mongodb")
                if cred and cred.credential_type == CredentialType.USERNAME_PASSWORD:
                    # Assume format "username:password"
                    if ":" in cred.value:
                        username, password = cred.value.split(":", 1)

            # Build connection URI
            if username and password:
                netloc = f"{username}:{password}@{parsed.hostname}"
                if parsed.port:
                    netloc += f":{parsed.port}"
            else:
                netloc = parsed.netloc

            connection_uri = f"{parsed.scheme}://{netloc}"

            # Get database name
            db_name = self.database_name or parsed.path.lstrip("/")
            if not db_name:
                raise ValueError("Database name is required")

            return MongodbLoader(
                connection_string=connection_uri,
                db_name=db_name,
                collection_name=self.collection_name,
                filter_criteria=self.filter_criteria,
            )

        except ImportError:
            logger.warning(
                "MongodbLoader not available. Install with: pip install pymongo"
            )
            return None
        except Exception as e:
            logger.error(f"Failed to create MongoDB loader: {e}")
            return None


class PostgreSQLSource(DatabaseSource):
    """PostgreSQL database source implementation."""

    def __init__(
        self,
        connection_string: str,
        query: Optional[str] = None,
        table_name: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(source_path=connection_string, **kwargs)
        self.connection_string = connection_string
        self.query = query
        self.table_name = table_name

    def can_handle(self, path: str) -> bool:
        """Check if this is a PostgreSQL connection string."""
        try:
            parsed = urlparse(path)
            return parsed.scheme in ["postgresql", "postgres"]
        except Exception:
            return False

    def get_confidence_score(self, path: str) -> float:
        """Get confidence score for PostgreSQL connections."""
        if not self.can_handle(path):
            return 0.0
        return 0.9

    def requires_authentication(self) -> bool:
        """PostgreSQL typically requires authentication."""
        return True

    def get_credential_requirements(self) -> List[CredentialType]:
        """PostgreSQL needs connection credentials."""
        return [CredentialType.USERNAME_PASSWORD, CredentialType.CONNECTION_STRING]

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a PostgreSQL loader."""
        try:
            from langchain_community.document_loaders.sql_database import (
                SQLDatabaseLoader,
            )
            from sqlalchemy import create_engine

            # Get credentials if needed
            parsed = urlparse(self.connection_string)
            username = parsed.username
            password = parsed.password

            if not (username and password) and self.credential_manager:
                cred = self.credential_manager.get_credential("postgresql")
                if cred and cred.credential_type == CredentialType.USERNAME_PASSWORD:
                    if ":" in cred.value:
                        username, password = cred.value.split(":", 1)

            # Build connection URI
            if username and password:
                netloc = f"{username}:{password}@{parsed.hostname}"
                if parsed.port:
                    netloc += f":{parsed.port}"
            else:
                netloc = parsed.netloc

            connection_uri = f"{parsed.scheme}://{netloc}{parsed.path}"

            # Create engine
            engine = create_engine(connection_uri)

            # Build query
            if self.query:
                query = self.query
            elif self.table_name:
                query = f"SELECT * FROM {self.table_name}"
            else:
                raise ValueError("Either query or table_name must be provided")

            return SQLDatabaseLoader(
                query=query,
                db=engine,
                page_content_columns=None,  # Use all columns
            )

        except ImportError:
            logger.warning(
                "SQLDatabaseLoader not available. Install with: pip install sqlalchemy"
            )
            return None
        except Exception as e:
            logger.error(f"Failed to create PostgreSQL loader: {e}")
            return None


# Export database sources
__all__ = [
    "MongoDBSource",
    "PostgreSQLSource",
]
