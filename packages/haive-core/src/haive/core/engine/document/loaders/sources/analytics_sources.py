"""Data processing and analytics platform source registrations.

This module implements data processing, analytics, and ETL platform loaders including:
- Data processing frameworks (Spark, Databricks, Snowflake)
- Analytics platforms (Tableau, Power BI, Looker)
- ETL/ELT tools (Fivetran, Stitch, Apache Airflow)
- Time series databases (InfluxDB, TimescaleDB, Prometheus)
- Log analytics (Elasticsearch, Splunk, Datadog)
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import Field

from .enhanced_registry import enhanced_registry, register_bulk_source, register_source
from .source_types import CredentialType, LoaderCapability, RemoteSource, SourceCategory


class AnalyticsPlatform(str, Enum):
    """Analytics and data processing platforms."""

    # Data Warehouses
    SNOWFLAKE = "snowflake"
    BIGQUERY = "bigquery"
    REDSHIFT = "redshift"
    DATABRICKS = "databricks"

    # Analytics Platforms
    TABLEAU = "tableau"
    POWER_BI = "power_bi"
    LOOKER = "looker"
    METABASE = "metabase"
    SUPERSET = "superset"

    # ETL/ELT Tools
    FIVETRAN = "fivetran"
    STITCH = "stitch"
    AIRFLOW = "airflow"
    DAGSTER = "dagster"
    PREFECT = "prefect"

    # Time Series Databases
    INFLUXDB = "influxdb"
    TIMESCALEDB = "timescaledb"
    PROMETHEUS = "prometheus"
    GRAPHITE = "graphite"

    # Log Analytics
    ELASTICSEARCH = "elasticsearch"
    SPLUNK = "splunk"
    DATADOG = "datadog"
    NEW_RELIC = "new_relic"
    SUMO_LOGIC = "sumo_logic"

    # Stream Processing
    KAFKA = "kafka"
    KINESIS = "kinesis"
    PULSAR = "pulsar"
    REDIS_STREAMS = "redis_streams"


class QueryType(str, Enum):
    """Types of analytical queries."""

    SQL = "sql"
    NOSQL = "nosql"
    TIMESERIES = "timeseries"
    LOGS = "logs"
    METRICS = "metrics"
    TRACES = "traces"
    EVENTS = "events"
    STREAMING = "streaming"


class DataFormat(str, Enum):
    """Data export formats."""

    CSV = "csv"
    JSON = "json"
    PARQUET = "parquet"
    AVRO = "avro"
    ORC = "orc"
    ARROW = "arrow"
    EXCEL = "excel"
    XML = "xml"


# =============================================================================
# Data Warehouse Sources
# =============================================================================


@register_source(
    name="snowflake",
    category=SourceCategory.ANALYTICS,
    loaders={
        "snowflake": {
            "class": "SnowflakeLoader",
            "speed": "fast",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["snowflake-connector-python"],
        }
    },
    default_loader="snowflake",
    description="Snowflake data warehouse loader",
    requires_credentials=True,
    credential_type=CredentialType.PASSWORD,
    capabilities=[
        LoaderCapability.STRUCTURED_DATA,
        LoaderCapability.QUERY_BASED,
        LoaderCapability.BULK_LOADING,
        LoaderCapability.TIME_TRAVEL,
    ],
    priority=10,
)
class SnowflakeSource(RemoteSource):
    """Snowflake data warehouse source."""

    source_type: str = "snowflake"
    category: SourceCategory = SourceCategory.ANALYTICS
    platform: AnalyticsPlatform = AnalyticsPlatform.SNOWFLAKE

    # Snowflake configuration
    account: str = Field(..., description="Snowflake account identifier")
    username: Optional[str] = Field(None, description="Username")
    password: Optional[str] = Field(None, description="Password")

    # Database options
    database: str = Field(..., description="Database name")
    schema: str = Field("PUBLIC", description="Schema name")
    warehouse: str = Field(..., description="Warehouse name")
    role: Optional[str] = Field(None, description="Role to use")

    # Query options
    query: Optional[str] = Field(None, description="SQL query")
    table: Optional[str] = Field(None, description="Table name")

    # Time travel
    at_timestamp: Optional[datetime] = Field(None, description="Query at timestamp")
    before_timestamp: Optional[datetime] = Field(
        None, description="Query before timestamp"
    )

    # Export options
    export_format: DataFormat = Field(DataFormat.JSON, description="Export format")
    limit: Optional[int] = Field(None, description="Row limit")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update(
            {
                "account": self.account,
                "user": self.username,
                "password": self.password,
                "database": self.database,
                "schema": self.schema,
                "warehouse": self.warehouse,
            }
        )

        if self.role:
            kwargs["role"] = self.role

        if self.query:
            kwargs["query"] = self.query
        elif self.table:
            kwargs["query"] = f"SELECT * FROM {self.schema}.{self.table}"
            if self.limit:
                kwargs["query"] += f" LIMIT {self.limit}"

        # Add time travel
        if self.at_timestamp:
            kwargs["at_timestamp"] = self.at_timestamp
        elif self.before_timestamp:
            kwargs["before_timestamp"] = self.before_timestamp

        return kwargs


@register_source(
    name="databricks",
    category=SourceCategory.ANALYTICS,
    loaders={
        "databricks": {
            "class": "DatabricksLoader",
            "speed": "fast",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["databricks-sql-connector"],
        }
    },
    default_loader="databricks",
    description="Databricks SQL warehouse loader",
    requires_credentials=True,
    credential_type=CredentialType.API_KEY,
    capabilities=[
        LoaderCapability.STRUCTURED_DATA,
        LoaderCapability.QUERY_BASED,
        LoaderCapability.BULK_LOADING,
        LoaderCapability.DELTA_SUPPORT,
    ],
    priority=10,
)
class DatabricksSource(RemoteSource):
    """Databricks SQL warehouse source."""

    source_type: str = "databricks"
    category: SourceCategory = SourceCategory.ANALYTICS
    platform: AnalyticsPlatform = AnalyticsPlatform.DATABRICKS

    # Databricks configuration
    server_hostname: str = Field(..., description="Server hostname")
    http_path: str = Field(..., description="HTTP path to SQL warehouse")
    access_token: Optional[str] = Field(None, description="Personal access token")

    # Query options
    catalog: str = Field("hive_metastore", description="Catalog name")
    schema: str = Field("default", description="Schema name")
    query: Optional[str] = Field(None, description="SQL query")
    table: Optional[str] = Field(None, description="Table name")

    # Processing options
    fetch_size: int = Field(10000, description="Fetch size for results")
    max_rows: Optional[int] = Field(None, description="Maximum rows to fetch")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update(
            {
                "server_hostname": self.server_hostname,
                "http_path": self.http_path,
                "access_token": (
                    self.access_token or self.get_api_key()
                    if hasattr(self, "get_api_key")
                    else None
                ),
                "catalog": self.catalog,
                "schema": self.schema,
            }
        )

        if self.query:
            kwargs["query"] = self.query
        elif self.table:
            kwargs["table"] = self.table

        kwargs["arraysize"] = self.fetch_size
        if self.max_rows:
            kwargs["max_rows"] = self.max_rows

        return kwargs


@register_bulk_source(
    name="bigquery",
    category=SourceCategory.ANALYTICS,
    loaders={
        "bigquery": {
            "class": "BigQueryLoader",
            "speed": "fast",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["google-cloud-bigquery"],
        }
    },
    default_loader="bigquery",
    description="Google BigQuery data warehouse loader",
    requires_credentials=True,
    credential_type=CredentialType.SERVICE_ACCOUNT,
    capabilities=[
        LoaderCapability.STRUCTURED_DATA,
        LoaderCapability.QUERY_BASED,
        LoaderCapability.BULK_LOADING,
        LoaderCapability.PARTITIONED_DATA,
    ],
    supports_scrape_all=True,
    priority=10,
)
class BigQuerySource(RemoteSource):
    """Google BigQuery data warehouse source."""

    source_type: str = "bigquery"
    category: SourceCategory = SourceCategory.ANALYTICS
    platform: AnalyticsPlatform = AnalyticsPlatform.BIGQUERY

    # BigQuery configuration
    project_id: str = Field(..., description="GCP project ID")
    dataset_id: str = Field(..., description="Dataset ID")
    credentials_path: Optional[str] = Field(
        None, description="Service account JSON path"
    )

    # Query options
    query: Optional[str] = Field(None, description="SQL query")
    table_id: Optional[str] = Field(None, description="Table ID")

    # Partition options
    partition_field: Optional[str] = Field(None, description="Partition field")
    start_date: Optional[datetime] = Field(
        None, description="Start date for partitions"
    )
    end_date: Optional[datetime] = Field(None, description="End date for partitions")

    # Export options
    page_size: int = Field(10000, description="Page size for results")
    max_results: Optional[int] = Field(None, description="Maximum results")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update(
            {
                "project": self.project_id,
                "dataset": self.dataset_id,
                "page_size": self.page_size,
            }
        )

        if self.credentials_path:
            kwargs["credentials_path"] = self.credentials_path

        if self.query:
            kwargs["query"] = self.query
        elif self.table_id:
            kwargs["table"] = self.table_id

        if self.max_results:
            kwargs["max_results"] = self.max_results

        return kwargs

    def scrape_all(self) -> Dict[str, Any]:
        """Scrape entire dataset or table."""
        return {
            "dataset_id": self.dataset_id,
            "include_views": True,
            "include_routines": False,
            "export_format": "json",
        }


# =============================================================================
# Analytics Platform Sources
# =============================================================================


@register_source(
    name="tableau",
    category=SourceCategory.ANALYTICS,
    loaders={
        "tableau": {
            "class": "TableauLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["tableauserverclient"],
        }
    },
    default_loader="tableau",
    description="Tableau Server/Online workbook and data source loader",
    requires_credentials=True,
    credential_type=CredentialType.API_KEY,
    capabilities=[
        LoaderCapability.METADATA_EXTRACTION,
        LoaderCapability.VISUALIZATION,
        LoaderCapability.BULK_LOADING,
    ],
    priority=9,
)
class TableauSource(RemoteSource):
    """Tableau analytics platform source."""

    source_type: str = "tableau"
    category: SourceCategory = SourceCategory.ANALYTICS
    platform: AnalyticsPlatform = AnalyticsPlatform.TABLEAU

    # Tableau configuration
    server_url: str = Field(..., description="Tableau Server URL")
    site_id: str = Field("", description="Site ID (empty for default)")
    username: Optional[str] = Field(None, description="Username")
    password: Optional[str] = Field(None, description="Password")
    token_name: Optional[str] = Field(None, description="Personal access token name")
    token_value: Optional[str] = Field(None, description="Personal access token value")

    # Content options
    include_workbooks: bool = Field(True, description="Include workbooks")
    include_datasources: bool = Field(True, description="Include data sources")
    include_views: bool = Field(True, description="Include views")

    # Filtering
    project_name: Optional[str] = Field(None, description="Filter by project")
    tags: Optional[List[str]] = Field(None, description="Filter by tags")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update({"server": self.server_url, "site_id": self.site_id})

        # Authentication
        if self.token_name and self.token_value:
            kwargs["token_name"] = self.token_name
            kwargs["token_value"] = self.token_value
        else:
            kwargs["username"] = self.username
            kwargs["password"] = self.password

        kwargs.update(
            {
                "include_workbooks": self.include_workbooks,
                "include_datasources": self.include_datasources,
                "include_views": self.include_views,
            }
        )

        if self.project_name:
            kwargs["project_name"] = self.project_name
        if self.tags:
            kwargs["tags"] = self.tags

        return kwargs


@register_source(
    name="power_bi",
    category=SourceCategory.ANALYTICS,
    loaders={
        "powerbi": {
            "class": "PowerBILoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["msal", "requests"],
        }
    },
    default_loader="powerbi",
    description="Microsoft Power BI report and dataset loader",
    requires_credentials=True,
    credential_type=CredentialType.OAUTH,
    capabilities=[
        LoaderCapability.METADATA_EXTRACTION,
        LoaderCapability.VISUALIZATION,
        LoaderCapability.BULK_LOADING,
    ],
    priority=9,
)
class PowerBISource(RemoteSource):
    """Microsoft Power BI source."""

    source_type: str = "power_bi"
    category: SourceCategory = SourceCategory.ANALYTICS
    platform: AnalyticsPlatform = AnalyticsPlatform.POWER_BI

    # Power BI configuration
    tenant_id: str = Field(..., description="Azure AD tenant ID")
    client_id: str = Field(..., description="Application client ID")
    client_secret: Optional[str] = Field(None, description="Client secret")

    # Content selection
    workspace_id: Optional[str] = Field(None, description="Workspace ID")
    dataset_id: Optional[str] = Field(None, description="Dataset ID")
    report_id: Optional[str] = Field(None, description="Report ID")

    # Options
    include_datasets: bool = Field(True, description="Include datasets")
    include_reports: bool = Field(True, description="Include reports")
    include_dashboards: bool = Field(True, description="Include dashboards")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update(
            {
                "tenant_id": self.tenant_id,
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            }
        )

        if self.workspace_id:
            kwargs["workspace_id"] = self.workspace_id
        if self.dataset_id:
            kwargs["dataset_id"] = self.dataset_id
        if self.report_id:
            kwargs["report_id"] = self.report_id

        kwargs.update(
            {
                "include_datasets": self.include_datasets,
                "include_reports": self.include_reports,
                "include_dashboards": self.include_dashboards,
            }
        )

        return kwargs


# =============================================================================
# Time Series Database Sources
# =============================================================================


@register_source(
    name="influxdb",
    category=SourceCategory.ANALYTICS,
    loaders={
        "influx": {
            "class": "InfluxDBLoader",
            "speed": "fast",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["influxdb-client"],
        }
    },
    default_loader="influx",
    description="InfluxDB time series database loader",
    requires_credentials=True,
    credential_type=CredentialType.API_KEY,
    capabilities=[
        LoaderCapability.TIMESERIES_DATA,
        LoaderCapability.QUERY_BASED,
        LoaderCapability.STREAMING,
        LoaderCapability.REAL_TIME,
    ],
    priority=9,
)
class InfluxDBSource(RemoteSource):
    """InfluxDB time series source."""

    source_type: str = "influxdb"
    category: SourceCategory = SourceCategory.ANALYTICS
    platform: AnalyticsPlatform = AnalyticsPlatform.INFLUXDB

    # InfluxDB configuration
    url: str = Field(..., description="InfluxDB URL")
    token: Optional[str] = Field(None, description="API token")
    org: str = Field(..., description="Organization")

    # Query options
    bucket: str = Field(..., description="Bucket name")
    measurement: Optional[str] = Field(None, description="Measurement name")
    flux_query: Optional[str] = Field(None, description="Flux query")

    # Time range
    start_time: Union[str, datetime] = Field("-1h", description="Start time")
    stop_time: Union[str, datetime] = Field("now()", description="Stop time")

    # Aggregation
    window_period: Optional[str] = Field(None, description="Window period (e.g., 5m)")
    aggregation_method: Optional[str] = Field(None, description="Aggregation method")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update(
            {
                "url": self.url,
                "token": (
                    self.token or self.get_api_key()
                    if hasattr(self, "get_api_key")
                    else None
                ),
                "org": self.org,
                "bucket": self.bucket,
            }
        )

        if self.flux_query:
            kwargs["query"] = self.flux_query
        else:
            # Build query from parameters
            query_parts = [f'from(bucket: "{self.bucket}")']
            query_parts.append(
                f"|> range(start: {self.start_time}, stop: {self.stop_time})"
            )

            if self.measurement:
                query_parts.append(
                    f'|> filter(fn: (r) => r["_measurement"] == "{self.measurement}")'
                )

            if self.window_period and self.aggregation_method:
                query_parts.append(
                    f"|> aggregateWindow(every: {self.window_period}, fn: {self.aggregation_method})"
                )

            kwargs["query"] = "\n".join(query_parts)

        return kwargs


@register_source(
    name="prometheus",
    category=SourceCategory.ANALYTICS,
    loaders={
        "prometheus": {
            "class": "PrometheusLoader",
            "speed": "fast",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["prometheus-api-client"],
        }
    },
    default_loader="prometheus",
    description="Prometheus metrics database loader",
    requires_credentials=False,
    capabilities=[
        LoaderCapability.TIMESERIES_DATA,
        LoaderCapability.QUERY_BASED,
        LoaderCapability.REAL_TIME,
        LoaderCapability.ALERTING,
    ],
    priority=8,
)
class PrometheusSource(RemoteSource):
    """Prometheus metrics source."""

    source_type: str = "prometheus"
    category: SourceCategory = SourceCategory.ANALYTICS
    platform: AnalyticsPlatform = AnalyticsPlatform.PROMETHEUS

    # Prometheus configuration
    url: str = Field(..., description="Prometheus server URL")

    # Query options
    query: str = Field(..., description="PromQL query")
    start_time: datetime = Field(..., description="Start time")
    end_time: datetime = Field(..., description="End time")
    step: str = Field("1m", description="Query resolution step")

    # Additional options
    timeout: int = Field(30, description="Query timeout in seconds")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update(
            {
                "url": self.url,
                "query": self.query,
                "start": self.start_time,
                "end": self.end_time,
                "step": self.step,
                "timeout": self.timeout,
            }
        )

        return kwargs


# =============================================================================
# Log Analytics Sources
# =============================================================================


@register_bulk_source(
    name="elasticsearch",
    category=SourceCategory.ANALYTICS,
    loaders={
        "elastic": {
            "class": "ElasticsearchLoader",
            "speed": "fast",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["elasticsearch"],
        }
    },
    default_loader="elastic",
    description="Elasticsearch log and document search loader",
    requires_credentials=True,
    credential_type=CredentialType.API_KEY,
    capabilities=[
        LoaderCapability.FULL_TEXT_SEARCH,
        LoaderCapability.QUERY_BASED,
        LoaderCapability.BULK_LOADING,
        LoaderCapability.REAL_TIME,
    ],
    supports_scrape_all=True,
    priority=10,
)
class ElasticsearchSource(RemoteSource):
    """Elasticsearch log analytics source."""

    source_type: str = "elasticsearch"
    category: SourceCategory = SourceCategory.ANALYTICS
    platform: AnalyticsPlatform = AnalyticsPlatform.ELASTICSEARCH

    # Elasticsearch configuration
    url: str = Field(..., description="Elasticsearch URL")
    cloud_id: Optional[str] = Field(None, description="Elastic Cloud ID")
    api_key: Optional[str] = Field(None, description="API key")
    username: Optional[str] = Field(None, description="Username")
    password: Optional[str] = Field(None, description="Password")

    # Query options
    index: str = Field(..., description="Index pattern")
    query: Optional[Dict[str, Any]] = Field(None, description="Elasticsearch query DSL")

    # Time range
    start_time: Optional[datetime] = Field(None, description="Start time")
    end_time: Optional[datetime] = Field(None, description="End time")

    # Pagination
    size: int = Field(100, description="Number of results per page")
    scroll_time: str = Field("5m", description="Scroll timeout")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update(
            {
                "url": self.url,
                "index_name": self.index,
                "body": self.query or {"query": {"match_all": {}}},
            }
        )

        if self.cloud_id:
            kwargs["cloud_id"] = self.cloud_id
        if self.api_key:
            kwargs["api_key"] = self.api_key
        elif self.username and self.password:
            kwargs["username"] = self.username
            kwargs["password"] = self.password

        # Add time range to query if specified
        if self.start_time or self.end_time:
            range_query = {"@timestamp": {}}
            if self.start_time:
                range_query["@timestamp"]["gte"] = self.start_time.isoformat()
            if self.end_time:
                range_query["@timestamp"]["lte"] = self.end_time.isoformat()

            if "bool" not in kwargs["body"]["query"]:
                kwargs["body"]["query"] = {"bool": {"must": [kwargs["body"]["query"]]}}
            kwargs["body"]["query"]["bool"]["filter"] = {"range": range_query}

        return kwargs

    def scrape_all(self) -> Dict[str, Any]:
        """Scrape entire index."""
        return {
            "index": self.index,
            "scroll": self.scroll_time,
            "size": self.size,
            "query": {"match_all": {}},
        }


@register_source(
    name="splunk",
    category=SourceCategory.ANALYTICS,
    loaders={
        "splunk": {
            "class": "SplunkLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["splunk-sdk"],
        }
    },
    default_loader="splunk",
    description="Splunk enterprise log search and analytics loader",
    requires_credentials=True,
    credential_type=CredentialType.API_KEY,
    capabilities=[
        LoaderCapability.FULL_TEXT_SEARCH,
        LoaderCapability.QUERY_BASED,
        LoaderCapability.REAL_TIME,
        LoaderCapability.ALERTING,
    ],
    priority=9,
)
class SplunkSource(RemoteSource):
    """Splunk log analytics source."""

    source_type: str = "splunk"
    category: SourceCategory = SourceCategory.ANALYTICS
    platform: AnalyticsPlatform = AnalyticsPlatform.SPLUNK

    # Splunk configuration
    host: str = Field(..., description="Splunk host")
    port: int = Field(8089, description="Management port")
    username: Optional[str] = Field(None, description="Username")
    password: Optional[str] = Field(None, description="Password")
    token: Optional[str] = Field(None, description="Authentication token")

    # Search options
    search_query: str = Field(..., description="SPL search query")
    earliest_time: str = Field("-1h", description="Earliest time")
    latest_time: str = Field("now", description="Latest time")

    # Output options
    output_mode: str = Field("json", description="Output mode")
    max_count: int = Field(1000, description="Maximum results")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update(
            {
                "host": self.host,
                "port": self.port,
                "query": self.search_query,
                "earliest_time": self.earliest_time,
                "latest_time": self.latest_time,
                "output_mode": self.output_mode,
                "count": self.max_count,
            }
        )

        if self.token:
            kwargs["token"] = self.token
        else:
            kwargs["username"] = self.username
            kwargs["password"] = self.password

        return kwargs


# =============================================================================
# Stream Processing Sources
# =============================================================================


@register_source(
    name="kafka",
    category=SourceCategory.ANALYTICS,
    loaders={
        "kafka": {
            "class": "KafkaLoader",
            "speed": "fast",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["kafka-python"],
        }
    },
    default_loader="kafka",
    description="Apache Kafka message stream loader",
    requires_credentials=False,
    capabilities=[
        LoaderCapability.STREAMING,
        LoaderCapability.REAL_TIME,
        LoaderCapability.PARTITIONED_DATA,
    ],
    priority=9,
)
class KafkaSource(RemoteSource):
    """Apache Kafka streaming source."""

    source_type: str = "kafka"
    category: SourceCategory = SourceCategory.ANALYTICS
    platform: AnalyticsPlatform = AnalyticsPlatform.KAFKA

    # Kafka configuration
    bootstrap_servers: List[str] = Field(..., description="Kafka broker addresses")
    topics: List[str] = Field(..., description="Topics to consume")
    group_id: str = Field(..., description="Consumer group ID")

    # Consumer options
    auto_offset_reset: str = Field("latest", description="Offset reset policy")
    max_poll_records: int = Field(500, description="Max records per poll")
    session_timeout_ms: int = Field(10000, description="Session timeout")

    # Processing options
    value_deserializer: str = Field("json", description="Value deserializer type")
    key_deserializer: str = Field("string", description="Key deserializer type")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update(
            {
                "bootstrap_servers": self.bootstrap_servers,
                "topics": self.topics,
                "group_id": self.group_id,
                "auto_offset_reset": self.auto_offset_reset,
                "max_poll_records": self.max_poll_records,
                "session_timeout_ms": self.session_timeout_ms,
                "value_deserializer": self.value_deserializer,
                "key_deserializer": self.key_deserializer,
            }
        )

        return kwargs


# =============================================================================
# ETL/ELT Platform Sources
# =============================================================================


@register_source(
    name="airflow",
    category=SourceCategory.ANALYTICS,
    loaders={
        "airflow": {
            "class": "AirflowLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["apache-airflow-client"],
        }
    },
    default_loader="airflow",
    description="Apache Airflow DAG and task loader",
    requires_credentials=True,
    credential_type=CredentialType.API_KEY,
    capabilities=[
        LoaderCapability.METADATA_EXTRACTION,
        LoaderCapability.WORKFLOW,
        LoaderCapability.MONITORING,
    ],
    priority=8,
)
class AirflowSource(RemoteSource):
    """Apache Airflow ETL platform source."""

    source_type: str = "airflow"
    category: SourceCategory = SourceCategory.ANALYTICS
    platform: AnalyticsPlatform = AnalyticsPlatform.AIRFLOW

    # Airflow configuration
    base_url: str = Field(..., description="Airflow webserver URL")
    username: Optional[str] = Field(None, description="Username")
    password: Optional[str] = Field(None, description="Password")

    # Content options
    include_dags: bool = Field(True, description="Include DAG definitions")
    include_dag_runs: bool = Field(True, description="Include DAG run history")
    include_task_instances: bool = Field(True, description="Include task instances")
    include_logs: bool = Field(False, description="Include task logs")

    # Filtering
    dag_id_pattern: Optional[str] = Field(None, description="DAG ID pattern filter")
    start_date: Optional[datetime] = Field(None, description="Filter by start date")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update(
            {
                "base_url": self.base_url,
                "username": self.username,
                "password": self.password,
                "include_dags": self.include_dags,
                "include_dag_runs": self.include_dag_runs,
                "include_task_instances": self.include_task_instances,
                "include_logs": self.include_logs,
            }
        )

        if self.dag_id_pattern:
            kwargs["dag_id_pattern"] = self.dag_id_pattern
        if self.start_date:
            kwargs["start_date"] = self.start_date

        return kwargs


# =============================================================================
# Utility Functions
# =============================================================================


def get_analytics_sources_statistics() -> Dict[str, Any]:
    """Get statistics about analytics sources."""
    registry = enhanced_registry

    # Count by platform type
    platform_counts = {}
    for platform in AnalyticsPlatform:
        count = len(
            [
                name
                for name, reg in registry._sources.items()
                if hasattr(reg, "platform")
                and getattr(reg, "platform", None) == platform
            ]
        )
        if count > 0:
            platform_counts[platform.value] = count

    # Category statistics
    analytics_sources = registry.find_sources_by_category(SourceCategory.ANALYTICS)

    # Query-based sources
    query_based = len(
        [
            name
            for name in analytics_sources
            if registry._sources[name].capabilities
            and LoaderCapability.QUERY_BASED in registry._sources[name].capabilities
        ]
    )

    # Real-time sources
    real_time = len(
        [
            name
            for name in analytics_sources
            if registry._sources[name].capabilities
            and LoaderCapability.REAL_TIME in registry._sources[name].capabilities
        ]
    )

    return {
        "total_analytics_sources": len(analytics_sources),
        "platform_breakdown": platform_counts,
        "query_based_sources": query_based,
        "real_time_sources": real_time,
        "query_types": len(QueryType),
        "data_formats": len(DataFormat),
    }


def validate_analytics_sources() -> bool:
    """Validate analytics source registrations."""
    registry = enhanced_registry

    required_sources = [
        "snowflake",
        "databricks",
        "bigquery",
        "tableau",
        "influxdb",
        "elasticsearch",
        "kafka",
        "airflow",
    ]

    missing = []
    for source_name in required_sources:
        if source_name not in registry._sources:
            missing.append(source_name)

    if missing:
        print(f"Missing analytics sources: {missing}")
        return False

    print("✅ All essential analytics sources registered!")
    return True


def detect_analytics_platform(url_or_identifier: str) -> Optional[AnalyticsPlatform]:
    """Auto-detect analytics platform from URL or identifier."""
    lower = url_or_identifier.lower()

    patterns = {
        AnalyticsPlatform.SNOWFLAKE: [".snowflakecomputing.com", "snowflake://"],
        AnalyticsPlatform.DATABRICKS: [".databricks.com", "databricks://"],
        AnalyticsPlatform.BIGQUERY: ["bigquery://", "bigquery.googleapis.com"],
        AnalyticsPlatform.TABLEAU: ["tableau.com", "tableau://"],
        AnalyticsPlatform.ELASTICSEARCH: [":9200", "elastic://", "elasticsearch://"],
        AnalyticsPlatform.SPLUNK: [":8089", "splunk://"],
        AnalyticsPlatform.KAFKA: [":9092", "kafka://"],
        AnalyticsPlatform.INFLUXDB: [":8086", "influx://"],
    }

    for platform, keywords in patterns.items():
        if any(keyword in lower for keyword in keywords):
            return platform

    return None


# Auto-validate on import
if __name__ == "__main__":
    validate_analytics_sources()
    stats = get_analytics_sources_statistics()
    print(f"Analytics Sources Statistics: {stats}")
