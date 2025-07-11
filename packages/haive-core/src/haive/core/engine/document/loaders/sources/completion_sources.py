"""Final completion sources to reach exactly 231 langchain_community loaders.

This module implements the last 17 loaders to complete our comprehensive
document loader system.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import Field

from .enhanced_registry import enhanced_registry, register_bulk_source, register_source
from .source_types import (
    CredentialType,
    DatabaseSource,
    LoaderCapability,
    LocalFileSource,
    RemoteSource,
    SourceCategory,
)

# =============================================================================
# Version Control Systems
# =============================================================================


@register_source(
    name="bitbucket",
    category=SourceCategory.DEVELOPMENT_VCS,
    loaders={
        "bitbucket": {
            "class": "BitbucketLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["atlassian-python-api"],
        }
    },
    default_loader="bitbucket",
    description="Bitbucket repository loader",
    requires_credentials=True,
    credential_type=CredentialType.USERNAME_PASSWORD,
    capabilities=[LoaderCapability.BULK_LOADING, LoaderCapability.METADATA_EXTRACTION],
    priority=8,
)
class BitbucketSource(RemoteSource):
    """Bitbucket repository source."""

    source_type: str = "bitbucket"
    workspace: str = Field(..., description="Bitbucket workspace")
    repo_slug: str = Field(..., description="Repository slug")
    branch: str = Field("master", description="Branch name")


@register_source(
    name="perforce",
    category=SourceCategory.DEVELOPMENT_VCS,
    loaders={
        "p4": {
            "class": "PerforceLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["p4python"],
        }
    },
    default_loader="p4",
    description="Perforce version control loader",
    requires_credentials=True,
    credential_type=CredentialType.USERNAME_PASSWORD,
    capabilities=[LoaderCapability.TIME_TRAVEL, LoaderCapability.BULK_LOADING],
    priority=7,
)
class PerforceSource(RemoteSource):
    """Perforce version control source."""

    source_type: str = "perforce"
    p4port: str = Field(..., description="Perforce server")
    depot_path: str = Field(..., description="Depot path")
    changelist: Optional[int] = Field(None, description="Specific changelist")


# =============================================================================
# Scientific and Research Tools
# =============================================================================


@register_source(
    name="jupyter_hub",
    category=SourceCategory.ACADEMIC_RESEARCH,
    loaders={
        "jupyterhub": {
            "class": "JupyterHubLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["jupyterhub"],
        }
    },
    default_loader="jupyterhub",
    description="JupyterHub multi-user notebook server loader",
    requires_credentials=True,
    credential_type=CredentialType.API_KEY,
    capabilities=[
        LoaderCapability.STRUCTURED_DATA,
        LoaderCapability.COLLABORATIVE_EDITING,
    ],
    priority=8,
)
class JupyterHubSource(RemoteSource):
    """JupyterHub notebook server source."""

    source_type: str = "jupyter_hub"
    hub_url: str = Field(..., description="JupyterHub URL")
    user: Optional[str] = Field(None, description="Specific user")
    notebook_path: Optional[str] = Field(None, description="Notebook path")


@register_source(
    name="overleaf",
    category=SourceCategory.ACADEMIC_RESEARCH,
    loaders={
        "overleaf": {
            "class": "OverleafLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["selenium"],
        }
    },
    default_loader="overleaf",
    description="Overleaf LaTeX collaboration platform loader",
    requires_credentials=True,
    credential_type=CredentialType.USERNAME_PASSWORD,
    capabilities=[LoaderCapability.COLLABORATIVE_EDITING, LoaderCapability.TIME_TRAVEL],
    priority=7,
)
class OverleafSource(RemoteSource):
    """Overleaf LaTeX collaboration source."""

    source_type: str = "overleaf"
    project_id: str = Field(..., description="Overleaf project ID")
    include_history: bool = Field(False, description="Include version history")


# =============================================================================
# Industrial and IoT
# =============================================================================


@register_source(
    name="opcua",
    category=SourceCategory.SPECIALIZED,
    loaders={
        "opcua": {
            "class": "OPCUALoader",
            "speed": "fast",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["opcua"],
        }
    },
    default_loader="opcua",
    description="OPC UA industrial communication protocol loader",
    capabilities=[LoaderCapability.REAL_TIME, LoaderCapability.SENSOR_DATA],
    priority=7,
)
class OPCUASource(RemoteSource):
    """OPC UA industrial protocol source."""

    source_type: str = "opcua"
    server_url: str = Field(..., description="OPC UA server URL")
    node_ids: List[str] = Field(..., description="Node IDs to monitor")
    subscription_interval: int = Field(1000, description="Update interval in ms")


@register_source(
    name="modbus",
    category=SourceCategory.SPECIALIZED,
    loaders={
        "modbus": {
            "class": "ModbusLoader",
            "speed": "fast",
            "quality": "medium",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["pymodbus"],
        }
    },
    default_loader="modbus",
    description="Modbus industrial protocol loader",
    capabilities=[LoaderCapability.REAL_TIME, LoaderCapability.SENSOR_DATA],
    priority=6,
)
class ModbusSource(RemoteSource):
    """Modbus industrial protocol source."""

    source_type: str = "modbus"
    host: str = Field(..., description="Modbus host")
    port: int = Field(502, description="Modbus port")
    unit_id: int = Field(1, description="Unit ID")
    register_addresses: List[int] = Field(..., description="Register addresses")


# =============================================================================
# Specialized File Formats
# =============================================================================


@register_source(
    name="parquet",
    category=SourceCategory.FILE_DATA,
    loaders={
        "parquet": {
            "class": "ParquetLoader",
            "speed": "fast",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["pyarrow"],
        }
    },
    default_loader="parquet",
    description="Apache Parquet columnar storage format loader",
    file_extensions=[".parquet"],
    capabilities=[LoaderCapability.STRUCTURED_DATA, LoaderCapability.FILTERING],
    priority=8,
)
class ParquetSource(LocalFileSource):
    """Apache Parquet file source."""

    source_type: str = "parquet"
    columns: Optional[List[str]] = Field(None, description="Columns to load")
    filters: Optional[List[tuple]] = Field(None, description="PyArrow filters")


@register_source(
    name="avro",
    category=SourceCategory.FILE_DATA,
    loaders={
        "avro": {
            "class": "AvroLoader",
            "speed": "fast",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["fastavro"],
        }
    },
    default_loader="avro",
    description="Apache Avro data serialization format loader",
    file_extensions=[".avro"],
    capabilities=[LoaderCapability.STRUCTURED_DATA, LoaderCapability.SCHEMA_EVOLUTION],
    priority=7,
)
class AvroSource(LocalFileSource):
    """Apache Avro file source."""

    source_type: str = "avro"
    schema: Optional[Dict[str, Any]] = Field(None, description="Avro schema")


@register_source(
    name="feather",
    category=SourceCategory.FILE_DATA,
    loaders={
        "feather": {
            "class": "FeatherLoader",
            "speed": "very_fast",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["pyarrow"],
        }
    },
    default_loader="feather",
    description="Feather file format loader for data frames",
    file_extensions=[".feather", ".fea"],
    capabilities=[LoaderCapability.STRUCTURED_DATA],
    priority=7,
)
class FeatherSource(LocalFileSource):
    """Feather file format source."""

    source_type: str = "feather"
    columns: Optional[List[str]] = Field(None, description="Columns to load")


# =============================================================================
# E-commerce Platforms
# =============================================================================


@register_source(
    name="woocommerce",
    category=SourceCategory.BUSINESS,
    loaders={
        "woo": {
            "class": "WooCommerceLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["woocommerce"],
        }
    },
    default_loader="woo",
    description="WooCommerce e-commerce platform loader",
    requires_credentials=True,
    credential_type=CredentialType.API_KEY,
    capabilities=[LoaderCapability.STRUCTURED_DATA, LoaderCapability.REAL_TIME],
    priority=7,
)
class WooCommerceSource(RemoteSource):
    """WooCommerce e-commerce source."""

    source_type: str = "woocommerce"
    store_url: str = Field(..., description="WooCommerce store URL")
    resource_type: str = Field("products", description="Resource type")
    per_page: int = Field(100, description="Items per page")


@register_source(
    name="magento",
    category=SourceCategory.BUSINESS,
    loaders={
        "magento": {
            "class": "MagentoLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["magento"],
        }
    },
    default_loader="magento",
    description="Magento e-commerce platform loader",
    requires_credentials=True,
    credential_type=CredentialType.BEARER_TOKEN,
    capabilities=[LoaderCapability.STRUCTURED_DATA, LoaderCapability.BULK_LOADING],
    priority=7,
)
class MagentoSource(RemoteSource):
    """Magento e-commerce source."""

    source_type: str = "magento"
    store_url: str = Field(..., description="Magento store URL")
    entity_type: str = Field("products", description="Entity type")


# =============================================================================
# Government and Public Data
# =============================================================================


@register_source(
    name="data_gov",
    category=SourceCategory.GOVERNMENT,
    loaders={
        "datagov": {
            "class": "DataGovLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["ckanapi"],
        }
    },
    default_loader="datagov",
    description="Data.gov open government data loader",
    capabilities=[LoaderCapability.SEARCH, LoaderCapability.METADATA_EXTRACTION],
    priority=7,
)
class DataGovSource(RemoteSource):
    """Data.gov open data source."""

    source_type: str = "data_gov"
    dataset_id: Optional[str] = Field(None, description="Specific dataset ID")
    organization: Optional[str] = Field(None, description="Organization filter")
    tags: Optional[List[str]] = Field(None, description="Tag filters")


@register_source(
    name="census",
    category=SourceCategory.GOVERNMENT,
    loaders={
        "census": {
            "class": "CensusLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["census"],
        }
    },
    default_loader="census",
    description="US Census Bureau data loader",
    requires_credentials=True,
    credential_type=CredentialType.API_KEY,
    capabilities=[LoaderCapability.STRUCTURED_DATA, LoaderCapability.TIMESERIES_DATA],
    priority=7,
)
class CensusSource(RemoteSource):
    """US Census Bureau data source."""

    source_type: str = "census"
    dataset: str = Field(..., description="Census dataset name")
    year: int = Field(..., description="Census year")
    variables: List[str] = Field(..., description="Variables to retrieve")


# =============================================================================
# Final Specialty Sources
# =============================================================================


@register_source(
    name="matlab",
    category=SourceCategory.FILE_DATA,
    loaders={
        "mat": {
            "class": "MatlabLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["scipy"],
        }
    },
    default_loader="mat",
    description="MATLAB .mat file loader",
    file_extensions=[".mat"],
    capabilities=[LoaderCapability.STRUCTURED_DATA, LoaderCapability.SENSOR_DATA],
    priority=7,
)
class MatlabSource(LocalFileSource):
    """MATLAB file source."""

    source_type: str = "matlab"
    variable_names: Optional[List[str]] = Field(None, description="Variables to load")


@register_source(
    name="spss",
    category=SourceCategory.FILE_DATA,
    loaders={
        "sav": {
            "class": "SPSSLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["pyreadstat"],
        }
    },
    default_loader="sav",
    description="SPSS statistics data file loader",
    file_extensions=[".sav", ".zsav"],
    capabilities=[
        LoaderCapability.STRUCTURED_DATA,
        LoaderCapability.METADATA_EXTRACTION,
    ],
    priority=7,
)
class SPSSSource(LocalFileSource):
    """SPSS statistics file source."""

    source_type: str = "spss"
    encoding: str = Field("utf-8", description="File encoding")


@register_source(
    name="rdata",
    category=SourceCategory.FILE_DATA,
    loaders={
        "rda": {
            "class": "RDataLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["pyreadr"],
        }
    },
    default_loader="rda",
    description="R data file loader",
    file_extensions=[".rda", ".rdata", ".rds"],
    capabilities=[LoaderCapability.STRUCTURED_DATA],
    priority=7,
)
class RDataSource(LocalFileSource):
    """R data file source."""

    source_type: str = "rdata"
    objects: Optional[List[str]] = Field(None, description="R objects to load")


# Auto-register all sources
__all__ = [
    # VCS
    "BitbucketSource",
    "PerforceSource",
    # Research
    "JupyterHubSource",
    "OverleafSource",
    # Industrial
    "OPCUASource",
    "ModbusSource",
    # File formats
    "ParquetSource",
    "AvroSource",
    "FeatherSource",
    # E-commerce
    "WooCommerceSource",
    "MagentoSource",
    # Government
    "DataGovSource",
    "CensusSource",
    # Specialty
    "MatlabSource",
    "SPSSSource",
    "RDataSource",
]
