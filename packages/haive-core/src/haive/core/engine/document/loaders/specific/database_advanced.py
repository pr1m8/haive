"""Advanced Database Loaders for Document Engine.

This module implements advanced database loaders including BigQuery and other
specialized database sources.
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


class BigQuerySource(DatabaseSource):
    """Google BigQuery database source."""

    def __init__(
        self,
        project_id: str,
        dataset_id: Optional[str] = None,
        table_id: Optional[str] = None,
        query: Optional[str] = None,
        page_content_columns: Optional[List[str]] = None,
        metadata_columns: Optional[List[str]] = None,
        **kwargs,
    ):
        bq_uri = f"bigquery://{project_id}"
        if dataset_id:
            bq_uri += f"/{dataset_id}"
            if table_id:
                bq_uri += f"/{table_id}"

        super().__init__(source_path=bq_uri, **kwargs)
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.table_id = table_id
        self.query = query
        self.page_content_columns = page_content_columns
        self.metadata_columns = metadata_columns

    def can_handle(self, path: str) -> bool:
        """Check if this is a BigQuery URI."""
        try:
            parsed = urlparse(path)
            return parsed.scheme == "bigquery"
        except Exception:
            return False

    def get_confidence_score(self, path: str) -> float:
        """Get confidence score for BigQuery URIs."""
        if not self.can_handle(path):
            return 0.0
        return 0.9

    def requires_authentication(self) -> bool:
        """BigQuery requires authentication."""
        return True

    def get_credential_requirements(self) -> List[CredentialType]:
        """BigQuery needs service account credentials."""
        return [CredentialType.SERVICE_ACCOUNT]

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a BigQuery loader."""
        try:
            from langchain_community.document_loaders import BigQueryLoader

            # Get credentials
            credentials_path = None
            if self.credential_manager:
                cred = self.credential_manager.get_credential("bigquery")
                if cred and cred.credential_type == CredentialType.SERVICE_ACCOUNT:
                    credentials_path = cred.value

            # Build query if not provided
            if not self.query:
                if self.table_id and self.dataset_id:
                    self.query = f"SELECT * FROM `{self.project_id}.{self.dataset_id}.{self.table_id}`"
                else:
                    raise ValueError("Either query or table_id must be provided")

            return BigQueryLoader(
                query=self.query,
                project=self.project_id,
                credentials_path=credentials_path,
                page_content_columns=self.page_content_columns,
                metadata_columns=self.metadata_columns,
            )

        except ImportError:
            logger.warning(
                "BigQueryLoader not available. Install with: pip install google-cloud-bigquery"
            )
            return None
        except Exception as e:
            logger.error(f"Failed to create BigQuery loader: {e}")
            return None

    def analyze_schema(self) -> Optional[Dict[str, Any]]:
        """Analyze BigQuery table schema."""
        try:
            from google.cloud import bigquery

            # Get credentials
            credentials_path = None
            if self.credential_manager:
                cred = self.credential_manager.get_credential("bigquery")
                if cred and cred.credential_type == CredentialType.SERVICE_ACCOUNT:
                    credentials_path = cred.value

            # Create client
            if credentials_path:
                client = bigquery.Client.from_service_account_json(credentials_path)
            else:
                client = bigquery.Client(project=self.project_id)

            if self.dataset_id and self.table_id:
                # Get table schema
                table_ref = client.dataset(self.dataset_id).table(self.table_id)
                table = client.get_table(table_ref)

                schema_info = {
                    "project_id": self.project_id,
                    "dataset_id": self.dataset_id,
                    "table_id": self.table_id,
                    "num_rows": table.num_rows,
                    "created": str(table.created),
                    "modified": str(table.modified),
                    "schema": [],
                }

                for field in table.schema:
                    schema_info["schema"].append(
                        {
                            "name": field.name,
                            "type": field.field_type,
                            "mode": field.mode,
                            "description": field.description,
                        }
                    )

                return schema_info

            elif self.dataset_id:
                # Get dataset info
                dataset = client.get_dataset(self.dataset_id)
                tables = list(client.list_tables(dataset))

                return {
                    "project_id": self.project_id,
                    "dataset_id": self.dataset_id,
                    "location": dataset.location,
                    "created": str(dataset.created),
                    "tables": [table.table_id for table in tables],
                }

            else:
                # Get project datasets
                datasets = list(client.list_datasets())
                return {
                    "project_id": self.project_id,
                    "datasets": [dataset.dataset_id for dataset in datasets],
                }

        except Exception as e:
            logger.error(f"Failed to analyze BigQuery schema: {e}")
            return None


class SQLiteSource(DatabaseSource):
    """SQLite database source."""

    def __init__(
        self,
        database_path: str,
        query: Optional[str] = None,
        table_name: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(source_path=f"sqlite:///{database_path}", **kwargs)
        self.database_path = database_path
        self.query = query
        self.table_name = table_name

    def can_handle(self, path: str) -> bool:
        """Check if this is a SQLite database."""
        try:
            parsed = urlparse(path)
            return (
                parsed.scheme == "sqlite"
                or path.endswith(".db")
                or path.endswith(".sqlite")
            )
        except Exception:
            return False

    def get_confidence_score(self, path: str) -> float:
        """Get confidence score for SQLite databases."""
        if not self.can_handle(path):
            return 0.0
        return 0.9

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a SQLite loader."""
        try:
            from langchain_community.document_loaders.sql_database import (
                SQLDatabaseLoader,
            )
            from sqlalchemy import create_engine

            # Create engine
            engine = create_engine(f"sqlite:///{self.database_path}")

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
            )

        except ImportError:
            logger.warning(
                "SQLDatabaseLoader not available. Install with: pip install sqlalchemy"
            )
            return None
        except Exception as e:
            logger.error(f"Failed to create SQLite loader: {e}")
            return None


class MySQLSource(DatabaseSource):
    """MySQL database source."""

    def __init__(
        self,
        host: str,
        database: str,
        port: int = 3306,
        query: Optional[str] = None,
        table_name: Optional[str] = None,
        **kwargs,
    ):
        mysql_uri = f"mysql://{host}:{port}/{database}"
        super().__init__(source_path=mysql_uri, **kwargs)
        self.host = host
        self.port = port
        self.database = database
        self.query = query
        self.table_name = table_name

    def can_handle(self, path: str) -> bool:
        """Check if this is a MySQL connection string."""
        try:
            parsed = urlparse(path)
            return parsed.scheme in ["mysql", "mysql+pymysql"]
        except Exception:
            return False

    def get_confidence_score(self, path: str) -> float:
        """Get confidence score for MySQL connections."""
        if not self.can_handle(path):
            return 0.0
        return 0.9

    def requires_authentication(self) -> bool:
        """MySQL requires authentication."""
        return True

    def get_credential_requirements(self) -> List[CredentialType]:
        """MySQL needs username/password."""
        return [CredentialType.USERNAME_PASSWORD]

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a MySQL loader."""
        try:
            from langchain_community.document_loaders.sql_database import (
                SQLDatabaseLoader,
            )
            from sqlalchemy import create_engine

            # Get credentials
            username = None
            password = None

            if self.credential_manager:
                cred = self.credential_manager.get_credential("mysql")
                if cred and cred.credential_type == CredentialType.USERNAME_PASSWORD:
                    if ":" in cred.value:
                        username, password = cred.value.split(":", 1)

            # Build connection URL
            if username and password:
                connection_url = f"mysql+pymysql://{username}:{password}@{self.host}:{self.port}/{self.database}"
            else:
                connection_url = (
                    f"mysql+pymysql://{self.host}:{self.port}/{self.database}"
                )

            # Create engine
            engine = create_engine(connection_url)

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
            )

        except ImportError:
            logger.warning(
                "MySQL loader dependencies not available. Install with: pip install sqlalchemy pymysql"
            )
            return None
        except Exception as e:
            logger.error(f"Failed to create MySQL loader: {e}")
            return None


# Export advanced database sources
__all__ = [
    "BigQuerySource",
    "SQLiteSource",
    "MySQLSource",
]
