"""Database and Cloud Storage Loaders for Haive Framework

This module implements various database loaders (MongoDB, BigQuery) and
cloud storage loaders (GCS, Azure Blob) following the established patterns.
"""

import logging
from typing import Any
from urllib.parse import parse_qsl, urlparse

from ..source_implementation import (
    CloudSource,
    CredentialManager,
    DatabaseSource,
    auto_source,
)

logger = logging.getLogger(__name__)

# =============================================================================
# DATABASE LOADERS
# =============================================================================


@auto_source(scheme_patterns=["mongodb", "mongo"])
class MongoDBSource(DatabaseSource):
    """MongoDB database source."""

    connection_string: str
    database_name: str | None = None
    collection_name: str | None = None
    filter_criteria: dict[str, Any] | None = None
    projection: dict[str, Any] | None = None
    limit: int | None = None

    class Config:
        loader_strategies = {
            "mongodb": {
                "class": "MongodbLoader",
                "speed": "medium",
                "quality": "high",
                "best_for": ["documents", "collections"],
                "requires_auth": True,
                "required_credentials": ["mongodb_credentials"],
            }
        }
        required_credentials = ["mongodb_credentials"]

    def create_mongodb_loader(self):
        """Create a MongoDBLoader instance."""
        try:
            from langchain_community.document_loaders import MongodbLoader

            # Parse connection components
            components = self._parse_connection_string()

            # Get credentials if needed
            username = components.get("username")
            password = components.get("password")

            if not (username and password) and self.credential_manager:
                creds = self.credential_manager.get_credential("mongodb_credentials")
                if creds:
                    username = creds.get("username", username)
                    password = creds.get("password", password)

            # Build connection string if needed
            if not (username and password) and "://" in self.connection_string:
                # Use connection string as is
                connection_uri = self.connection_string
            else:
                # Build connection string with credentials
                auth_str = f"{username}:{password}@" if username and password else ""
                host = components.get("hostname", "localhost")
                port_str = (
                    f":{components.get('port', 27017)}"
                    if components.get("port")
                    else ""
                )

                connection_uri = f"mongodb://{auth_str}{host}{port_str}"

            # Get database name
            db_name = self.database_name or components.get("path", "").lstrip("/")

            if not db_name:
                raise ValueError("Database name is required")

            # Create loader
            return MongodbLoader(
                connection_string=connection_uri,
                db_name=db_name,
                collection_name=self.collection_name,
                filter_criteria=self.filter_criteria or {},
                projection=self.projection,
            )
        except ImportError:
            logger.warning(
                "MongodbLoader not available. Install with: pip install pymongo"
            )
            # Return mock loader for testing
            return {
                "connection_string": "mongodb://[REDACTED]",
                "db_name": db_name,
                "collection_name": self.collection_name,
                "filter_criteria": self.filter_criteria or {},
                "projection": self.projection,
            }

    def create_loader(self, strategy_name: str | None = None) -> Any:
        """Create a loader with the specified strategy."""
        if strategy_name == "mongodb" or not strategy_name:
            return self.create_mongodb_loader()
        raise ValueError(f"Unsupported strategy: {strategy_name}")

    def authenticate(self, credential_manager: CredentialManager | None = None) -> bool:
        """Authenticate the MongoDB source."""
        self.credential_manager = credential_manager

        if not credential_manager:
            return False

        creds = credential_manager.get_credential("mongodb_credentials")
        if not creds:
            self.is_authenticated = False
            return False

        # Store credentials
        self.is_authenticated = True
        return True

    def _parse_connection_string(self) -> dict[str, Any]:
        """Parse the MongoDB connection string."""
        if "://" not in self.connection_string:
            # Handle simple hostname format
            return {
                "scheme": "mongodb",
                "hostname": self.connection_string,
                "port": 27017,
                "path": self.database_name or "",
            }

        parsed = urlparse(self.connection_string)
        components = {
            "scheme": parsed.scheme,
            "username": parsed.username,
            "password": parsed.password,
            "hostname": parsed.hostname or "localhost",
            "port": parsed.port or 27017,
            "path": parsed.path.lstrip("/"),
            "query_params": dict(parse_qsl(parsed.query)),
        }

        return components

    def analyze_mongodb_schema(self) -> dict[str, Any]:
        """Analyze MongoDB schema to understand structure."""
        try:
            import pymongo

            # Parse connection and get credentials
            components = self._parse_connection_string()

            # Get credentials if needed
            username = components.get("username")
            password = components.get("password")

            if not (username and password) and self.credential_manager:
                creds = self.credential_manager.get_credential("mongodb_credentials")
                if creds:
                    username = creds.get("username", username)
                    password = creds.get("password", password)

            # Build connection string
            auth_str = f"{username}:{password}@" if username and password else ""
            host = components.get("hostname", "localhost")
            port_str = (
                f":{components.get('port', 27017)}" if components.get("port") else ""
            )

            connection_uri = f"mongodb://{auth_str}{host}{port_str}"

            # Get database name
            db_name = self.database_name or components.get("path", "").lstrip("/")

            if not db_name:
                raise ValueError("Database name is required")

            # Connect to MongoDB
            client = pymongo.MongoClient(connection_uri)
            db = client[db_name]

            # Initialize analysis results
            analysis = {
                "database_type": "mongodb",
                "database_name": db_name,
                "collections": [],
                "collections_count": 0,
                "estimated_total_documents": 0,
            }

            # Get collections
            collection_names = db.list_collection_names()
            analysis["collections_count"] = len(collection_names)

            # Analyze each collection
            collection_info = []
            for collection_name in collection_names:
                collection = db[collection_name]

                # Get document count
                doc_count = collection.count_documents({})

                # Sample a document to infer schema
                sample_doc = collection.find_one()

                # Extract field names and types
                fields = []
                if sample_doc:
                    for key, value in sample_doc.items():
                        if key != "_id":  # Skip the ID field
                            fields.append({"name": key, "type": type(value).__name__})

                # Add to collections list
                collection_info.append(
                    {
                        "name": collection_name,
                        "document_count": doc_count,
                        "fields": fields,
                    }
                )

                # Update total documents
                analysis["estimated_total_documents"] += doc_count

            # Sort collections by document count
            collection_info.sort(key=lambda x: x["document_count"], reverse=True)
            analysis["collections"] = collection_info

            # Get largest collections
            analysis["largest_collections"] = [c["name"] for c in collection_info[:5]]

            return analysis

        except Exception as e:
            return {
                "error": str(e),
                "database_type": "mongodb",
                "database_name": self.database_name or "unknown",
            }


@auto_source(scheme_patterns=["bigquery"])
class BigQuerySource(DatabaseSource):
    """Google BigQuery database source."""

    project_id: str
    dataset_id: str
    table_id: str | None = None
    query: str | None = None
    max_results: int | None = 1000

    class Config:
        loader_strategies = {
            "bigquery": {
                "class": "BigQueryLoader",
                "speed": "slow",
                "quality": "high",
                "best_for": ["data_warehouse", "analytics"],
                "requires_auth": True,
                "required_credentials": ["gcp_credentials"],
            }
        }
        required_credentials = ["gcp_credentials"]

    def create_bigquery_loader(self):
        """Create a BigQueryLoader instance."""
        try:
            from langchain_community.document_loaders import BigQueryLoader

            # Check if credentials are available
            if not self.is_authenticated and self.credential_manager:
                self.authenticate(self.credential_manager)

            # Build query if not provided
            query = self.query
            if not query and self.table_id:
                query = f"SELECT * FROM `{self.project_id}.{self.dataset_id}.{self.table_id}` LIMIT {self.max_results}"
            elif not query:
                # Default to listing tables if no specific table/query
                query = f"SELECT table_name FROM `{self.project_id}.{self.dataset_id}.INFORMATION_SCHEMA.TABLES`"

            # Get credentials
            credentials_path = None
            credentials_json = None

            if self.credential_manager:
                creds = self.credential_manager.get_credential("gcp_credentials")
                if creds:
                    if "file_path" in creds:
                        credentials_path = creds["file_path"]
                    elif "json" in creds:
                        credentials_json = creds["json"]

            # Create loader with appropriate credentials
            if credentials_path:
                return BigQueryLoader(
                    query=query,
                    project_id=self.project_id,
                    credentials_path=credentials_path,
                )
            if credentials_json:
                import json
                from tempfile import NamedTemporaryFile

                # Create temporary credentials file
                with NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
                    json.dump(credentials_json, f)
                    temp_creds_path = f.name

                return BigQueryLoader(
                    query=query,
                    project_id=self.project_id,
                    credentials_path=temp_creds_path,
                )
            # Try to use default credentials
            return BigQueryLoader(query=query, project_id=self.project_id)

        except ImportError:
            logger.warning(
                "BigQueryLoader not available. Install with: pip install google-cloud-bigquery"
            )
            # Return mock loader for testing
            return {
                "query": query,
                "project_id": self.project_id,
                "dataset_id": self.dataset_id,
            }

    def create_loader(self, strategy_name: str | None = None) -> Any:
        """Create a loader with the specified strategy."""
        if strategy_name == "bigquery" or not strategy_name:
            return self.create_bigquery_loader()
        raise ValueError(f"Unsupported strategy: {strategy_name}")

    def authenticate(self, credential_manager: CredentialManager | None = None) -> bool:
        """Authenticate the BigQuery source."""
        self.credential_manager = credential_manager

        if not credential_manager:
            return False

        creds = credential_manager.get_credential("gcp_credentials")
        if not creds:
            self.is_authenticated = False
            return False

        # Check if credentials have the necessary parts
        if not ("file_path" in creds or "json" in creds):
            logger.warning("GCP credentials missing file_path or json")
            self.is_authenticated = False
            return False

        # Store credentials
        self.is_authenticated = True
        return True

    def analyze_bigquery_schema(self) -> dict[str, Any]:
        """Analyze BigQuery schema to understand structure."""
        try:
            from google.cloud import bigquery

            # Get credentials
            credentials_path = None
            credentials_json = None

            if self.credential_manager:
                creds = self.credential_manager.get_credential("gcp_credentials")
                if creds:
                    if "file_path" in creds:
                        credentials_path = creds["file_path"]
                    elif "json" in creds:
                        credentials_json = creds["json"]

            # Create client with appropriate credentials
            client = None
            if credentials_path:
                client = bigquery.Client.from_service_account_json(credentials_path)
            elif credentials_json:
                import json
                from tempfile import NamedTemporaryFile

                # Create temporary credentials file
                with NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
                    json.dump(credentials_json, f)
                    temp_creds_path = f.name

                client = bigquery.Client.from_service_account_json(temp_creds_path)
            else:
                # Try to use default credentials
                client = bigquery.Client(project=self.project_id)

            # Initialize analysis results
            analysis = {
                "database_type": "bigquery",
                "project_id": self.project_id,
                "dataset_id": self.dataset_id,
                "tables": [],
                "tables_count": 0,
                "estimated_total_rows": 0,
            }

            # Get dataset reference
            dataset_ref = client.dataset(self.dataset_id)

            # List tables in the dataset
            tables = list(client.list_tables(dataset_ref))
            analysis["tables_count"] = len(tables)

            # Analyze each table
            table_info = []
            for table in tables:
                # Get table metadata
                table_ref = dataset_ref.table(table.table_id)
                table_obj = client.get_table(table_ref)

                # Extract schema information
                schema_fields = []
                for field in table_obj.schema:
                    schema_fields.append(
                        {
                            "name": field.name,
                            "type": field.field_type,
                            "mode": field.mode,
                        }
                    )

                # Add to tables list
                table_info.append(
                    {
                        "name": table.table_id,
                        "rows": table_obj.num_rows,
                        "size_bytes": table_obj.num_bytes,
                        "schema": schema_fields,
                        "created": (
                            table_obj.created.isoformat() if table_obj.created else None
                        ),
                        "modified": (
                            table_obj.modified.isoformat()
                            if table_obj.modified
                            else None
                        ),
                    }
                )

                # Update total rows
                analysis["estimated_total_rows"] += table_obj.num_rows

            # Sort tables by row count
            table_info.sort(key=lambda x: x["rows"], reverse=True)
            analysis["tables"] = table_info

            # Get largest tables
            analysis["largest_tables"] = [t["name"] for t in table_info[:5]]

            return analysis

        except Exception as e:
            return {
                "error": str(e),
                "database_type": "bigquery",
                "project_id": self.project_id,
                "dataset_id": self.dataset_id,
            }


# =============================================================================
# CLOUD STORAGE LOADERS
# =============================================================================


@auto_source(scheme_patterns=["gs", "gcs"])
class GCSSource(CloudSource):
    """Google Cloud Storage source."""

    bucket_name: str
    object_key: str | None = None
    prefix: str | None = None
    is_directory: bool = False

    class Config:
        loader_strategies = {
            "file": {
                "class": "GCSFileLoader",
                "speed": "medium",
                "quality": "high",
                "best_for": ["single_file"],
                "requires_auth": True,
                "required_credentials": ["gcp_credentials"],
            },
            "directory": {
                "class": "GCSDirectoryLoader",
                "speed": "slow",
                "quality": "high",
                "best_for": ["multiple_files", "directory"],
                "requires_auth": True,
                "required_credentials": ["gcp_credentials"],
            },
        }
        required_credentials = ["gcp_credentials"]

    def create_file_loader(self):
        """Create a GCSFileLoader instance."""
        try:
            from langchain_community.document_loaders import GCSFileLoader

            # Check if credentials are available
            if not self.is_authenticated and self.credential_manager:
                self.authenticate(self.credential_manager)

            # Get credentials
            credentials_path = None
            credentials_json = None

            if self.credential_manager:
                creds = self.credential_manager.get_credential("gcp_credentials")
                if creds:
                    if "file_path" in creds:
                        credentials_path = creds["file_path"]
                    elif "json" in creds:
                        credentials_json = creds["json"]

            # Create loader with appropriate credentials
            if credentials_path:
                return GCSFileLoader(
                    project_name=None,  # Will be inferred from credentials
                    bucket=self.bucket_name,
                    blob=self.object_key,
                    google_credentials_path=credentials_path,
                )
            if credentials_json:
                import json
                from tempfile import NamedTemporaryFile

                # Create temporary credentials file
                with NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
                    json.dump(credentials_json, f)
                    temp_creds_path = f.name

                return GCSFileLoader(
                    project_name=None,  # Will be inferred from credentials
                    bucket=self.bucket_name,
                    blob=self.object_key,
                    google_credentials_path=temp_creds_path,
                )
            # Try to use default credentials
            return GCSFileLoader(
                project_name=None,  # Will be inferred from environment
                bucket=self.bucket_name,
                blob=self.object_key,
            )

        except ImportError:
            logger.warning(
                "GCSFileLoader not available. Install with: pip install google-cloud-storage"
            )
            # Return mock loader for testing
            return {"bucket": self.bucket_name, "blob": self.object_key}

    def create_directory_loader(self):
        """Create a GCSDirectoryLoader instance."""
        try:
            from langchain_community.document_loaders import GCSDirectoryLoader

            # Check if credentials are available
            if not self.is_authenticated and self.credential_manager:
                self.authenticate(self.credential_manager)

            # Get credentials
            credentials_path = None
            credentials_json = None

            if self.credential_manager:
                creds = self.credential_manager.get_credential("gcp_credentials")
                if creds:
                    if "file_path" in creds:
                        credentials_path = creds["file_path"]
                    elif "json" in creds:
                        credentials_json = creds["json"]

            # Determine prefix to use
            prefix = self.prefix or self.object_key or ""

            # Create loader with appropriate credentials
            if credentials_path:
                return GCSDirectoryLoader(
                    project_name=None,  # Will be inferred from credentials
                    bucket=self.bucket_name,
                    prefix=prefix,
                    google_credentials_path=credentials_path,
                )
            if credentials_json:
                import json
                from tempfile import NamedTemporaryFile

                # Create temporary credentials file
                with NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
                    json.dump(credentials_json, f)
                    temp_creds_path = f.name

                return GCSDirectoryLoader(
                    project_name=None,  # Will be inferred from credentials
                    bucket=self.bucket_name,
                    prefix=prefix,
                    google_credentials_path=temp_creds_path,
                )
            # Try to use default credentials
            return GCSDirectoryLoader(
                project_name=None,  # Will be inferred from environment
                bucket=self.bucket_name,
                prefix=prefix,
            )

        except ImportError:
            logger.warning(
                "GCSDirectoryLoader not available. Install with: pip install google-cloud-storage"
            )
            # Return mock loader for testing
            return {
                "bucket": self.bucket_name,
                "prefix": self.prefix or self.object_key or "",
            }

    def create_loader(self, strategy_name: str | None = None) -> Any:
        """Create a loader with the specified strategy."""
        if not strategy_name:
            # Auto-select based on is_directory flag
            strategy_name = "directory" if self.is_directory else "file"

        if strategy_name == "file":
            return self.create_file_loader()
        if strategy_name == "directory":
            return self.create_directory_loader()
        raise ValueError(f"Unsupported strategy: {strategy_name}")

    def authenticate(self, credential_manager: CredentialManager | None = None) -> bool:
        """Authenticate the GCS source."""
        self.credential_manager = credential_manager

        if not credential_manager:
            return False

        creds = credential_manager.get_credential("gcp_credentials")
        if not creds:
            self.is_authenticated = False
            return False

        # Check if credentials have the necessary parts
        if not ("file_path" in creds or "json" in creds):
            logger.warning("GCP credentials missing file_path or json")
            self.is_authenticated = False
            return False

        # Store credentials
        self.is_authenticated = True
        return True


@auto_source(scheme_patterns=["azure", "azblob"])
class AzureBlobSource(CloudSource):
    """Azure Blob Storage source."""

    container_name: str
    blob_name: str | None = None
    prefix: str | None = None
    is_container: bool = False

    class Config:
        loader_strategies = {
            "file": {
                "class": "AzureBlobStorageFileLoader",
                "speed": "medium",
                "quality": "high",
                "best_for": ["single_file"],
                "requires_auth": True,
                "required_credentials": ["azure_storage_credentials"],
            },
            "container": {
                "class": "AzureBlobStorageContainerLoader",
                "speed": "slow",
                "quality": "high",
                "best_for": ["multiple_files", "container"],
                "requires_auth": True,
                "required_credentials": ["azure_storage_credentials"],
            },
        }
        required_credentials = ["azure_storage_credentials"]

    def create_file_loader(self):
        """Create an AzureBlobStorageFileLoader instance."""
        try:
            from langchain_community.document_loaders import AzureBlobStorageFileLoader

            # Check if credentials are available
            if not self.is_authenticated and self.credential_manager:
                self.authenticate(self.credential_manager)

            # Get connection string or credentials
            conn_string = None
            account_url = None
            account_key = None
            sas_token = None

            if self.credential_manager:
                creds = self.credential_manager.get_credential(
                    "azure_storage_credentials"
                )
                if creds:
                    conn_string = creds.get("connection_string")
                    account_url = creds.get("account_url")
                    account_key = creds.get("account_key")
                    sas_token = creds.get("sas_token")

            # Create loader with appropriate credentials
            if conn_string:
                return AzureBlobStorageFileLoader(
                    conn_str=conn_string,
                    container=self.container_name,
                    blob=self.blob_name,
                )
            if account_url and (account_key or sas_token):
                return AzureBlobStorageFileLoader(
                    container=self.container_name,
                    blob=self.blob_name,
                    account_url=account_url,
                    credential=account_key or sas_token,
                )
            raise ValueError(
                "Azure credentials missing connection_string or account_url with credential"
            )

        except ImportError:
            logger.warning(
                "AzureBlobStorageFileLoader not available. Install with: pip install azure-storage-blob"
            )
            # Return mock loader for testing
            return {"container": self.container_name, "blob": self.blob_name}

    def create_container_loader(self):
        """Create an AzureBlobStorageContainerLoader instance."""
        try:
            from langchain_community.document_loaders import (
                AzureBlobStorageContainerLoader,
            )

            # Check if credentials are available
            if not self.is_authenticated and self.credential_manager:
                self.authenticate(self.credential_manager)

            # Get connection string or credentials
            conn_string = None
            account_url = None
            account_key = None
            sas_token = None

            if self.credential_manager:
                creds = self.credential_manager.get_credential(
                    "azure_storage_credentials"
                )
                if creds:
                    conn_string = creds.get("connection_string")
                    account_url = creds.get("account_url")
                    account_key = creds.get("account_key")
                    sas_token = creds.get("sas_token")

            # Determine prefix to use
            prefix = self.prefix or ""

            # Create loader with appropriate credentials
            if conn_string:
                return AzureBlobStorageContainerLoader(
                    conn_str=conn_string, container=self.container_name, prefix=prefix
                )
            if account_url and (account_key or sas_token):
                return AzureBlobStorageContainerLoader(
                    container=self.container_name,
                    prefix=prefix,
                    account_url=account_url,
                    credential=account_key or sas_token,
                )
            raise ValueError(
                "Azure credentials missing connection_string or account_url with credential"
            )

        except ImportError:
            logger.warning(
                "AzureBlobStorageContainerLoader not available. Install with: pip install azure-storage-blob"
            )
            # Return mock loader for testing
            return {"container": self.container_name, "prefix": self.prefix or ""}

    def create_loader(self, strategy_name: str | None = None) -> Any:
        """Create a loader with the specified strategy."""
        if not strategy_name:
            # Auto-select based on is_container flag
            strategy_name = "container" if self.is_container else "file"

        if strategy_name == "file":
            return self.create_file_loader()
        if strategy_name == "container":
            return self.create_container_loader()
        raise ValueError(f"Unsupported strategy: {strategy_name}")

    def authenticate(self, credential_manager: CredentialManager | None = None) -> bool:
        """Authenticate the Azure Blob source."""
        self.credential_manager = credential_manager

        if not credential_manager:
            return False

        creds = credential_manager.get_credential("azure_storage_credentials")
        if not creds:
            self.is_authenticated = False
            return False

        # Check if credentials have the necessary parts
        has_conn_string = "connection_string" in creds
        has_account_url = "account_url" in creds
        has_auth = "account_key" in creds or "sas_token" in creds

        if not (has_conn_string or (has_account_url and has_auth)):
            logger.warning("Azure credentials missing required parameters")
            self.is_authenticated = False
            return False

        # Store credentials
        self.is_authenticated = True
        return True


# =============================================================================
# USAGE EXAMPLES
# =============================================================================


def mongodb_example():
    """Example usage of MongoDB loader."""
    from ..source_implementation import CredentialManager

    # Create a credential manager
    credential_manager = CredentialManager()

    # Add MongoDB credentials
    credential_manager.store_credential(
        "mongodb_credentials",
        {"type": "database", "username": "user", "password": "pass"},
    )

    # Create MongoDB source
    mongo_source = MongoDBSource(
        connection_string="mongodb://localhost:27017/mydb", collection_name="products"
    )

    # Authenticate
    mongo_source.authenticate(credential_manager)

    # Create loader
    loader = mongo_source.create_loader()

    # Load documents
    # documents = loader.load()

    # Analyze MongoDB schema
    # schema = mongo_source.analyze_mongodb_schema()

    return loader


def bigquery_example():
    """Example usage of BigQuery loader."""
    from ..source_implementation import CredentialManager

    # Create a credential manager
    credential_manager = CredentialManager()

    # Add GCP credentials
    credential_manager.store_credential(
        "gcp_credentials",
        {"type": "service_account", "file_path": "/path/to/credentials.json"},
    )

    # Create BigQuery source
    bq_source = BigQuerySource(
        project_id="my-project", dataset_id="my_dataset", table_id="my_table"
    )

    # Authenticate
    bq_source.authenticate(credential_manager)

    # Create loader
    loader = bq_source.create_loader()

    # Load documents
    # documents = loader.load()

    # Analyze BigQuery schema
    # schema = bq_source.analyze_bigquery_schema()

    return loader


def gcs_example():
    """Example usage of GCS loader."""
    from ..source_implementation import CredentialManager

    # Create a credential manager
    credential_manager = CredentialManager()

    # Add GCP credentials
    credential_manager.store_credential(
        "gcp_credentials",
        {"type": "service_account", "file_path": "/path/to/credentials.json"},
    )

    # Create GCS file source
    gcs_file_source = GCSSource(
        bucket_name="my-bucket", object_key="path/to/document.pdf"
    )

    # Create GCS directory source
    gcs_dir_source = GCSSource(
        bucket_name="my-bucket", prefix="documents/", is_directory=True
    )

    # Authenticate
    gcs_file_source.authenticate(credential_manager)
    gcs_dir_source.authenticate(credential_manager)

    # Create loaders
    file_loader = gcs_file_source.create_loader()
    dir_loader = gcs_dir_source.create_loader()

    # Load documents
    # file_documents = file_loader.load()
    # dir_documents = dir_loader.load()

    return (file_loader, dir_loader)


def azure_blob_example():
    """Example usage of Azure Blob Storage loader."""
    from ..source_implementation import CredentialManager

    # Create a credential manager
    credential_manager = CredentialManager()

    # Add Azure Storage credentials with connection string
    credential_manager.store_credential(
        "azure_storage_credentials",
        {
            "type": "storage",
            "connection_string": "DefaultEndpointsProtocol=https;AccountName=mystorageaccount;AccountKey=mykey;EndpointSuffix=core.windows.net",
        },
    )

    # Alternative: Add Azure Storage credentials with account URL and key
    credential_manager.store_credential(
        "azure_storage_credentials",
        {
            "type": "storage",
            "account_url": "https://mystorageaccount.blob.core.windows.net",
            "account_key": "mykey",
        },
    )

    # Create Azure Blob file source
    azure_file_source = AzureBlobSource(
        container_name="mycontainer", blob_name="path/to/document.pdf"
    )

    # Create Azure Blob container source
    azure_container_source = AzureBlobSource(
        container_name="mycontainer", prefix="documents/", is_container=True
    )

    # Authenticate
    azure_file_source.authenticate(credential_manager)
    azure_container_source.authenticate(credential_manager)

    # Create loaders
    file_loader = azure_file_source.create_loader()
    container_loader = azure_container_source.create_loader()

    # Load documents
    # file_documents = file_loader.load()
    # container_documents = container_loader.load()

    return (file_loader, container_loader)
