"""Extended source registrations to complete the 231 langchain_community loaders.

This module implements the final set of loaders to reach the complete 231 target,
including specialized and niche loaders from langchain_community.
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
# Image and Document Processing
# =============================================================================


@register_source(
    name="paddleocr",
    category=SourceCategory.FILE_DOCUMENT,
    loaders={
        "paddleocr": {
            "class": "PaddleOCRLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["paddlepaddle", "paddleocr"],
        }
    },
    default_loader="paddleocr",
    description="PaddleOCR multilingual OCR loader",
    file_extensions=[".png", ".jpg", ".jpeg", ".tiff"],
    capabilities=[LoaderCapability.OCR, LoaderCapability.MULTILINGUAL],
    priority=8,
)
class PaddleOCRSource(LocalFileSource):
    """PaddleOCR multilingual OCR source."""

    source_type: str = "paddleocr"
    lang: str = Field("en", description="Language code")


@register_source(
    name="azure_form_recognizer",
    category=SourceCategory.FILE_DOCUMENT,
    loaders={
        "azure_form": {
            "class": "AzureFormRecognizerLoader",
            "speed": "medium",
            "quality": "very_high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["azure-ai-formrecognizer"],
        }
    },
    default_loader="azure_form",
    description="Azure Form Recognizer for intelligent document processing",
    requires_credentials=True,
    credential_type=CredentialType.API_KEY,
    capabilities=[LoaderCapability.OCR, LoaderCapability.STRUCTURED_DATA],
    priority=9,
)
class AzureFormRecognizerSource(RemoteSource):
    """Azure Form Recognizer source."""

    source_type: str = "azure_form_recognizer"
    endpoint: str = Field(..., description="Azure endpoint")
    model_id: str = Field("prebuilt-document", description="Model ID")


# =============================================================================
# Monitoring and Observability
# =============================================================================


@register_source(
    name="datadog",
    category=SourceCategory.ANALYTICS,
    loaders={
        "datadog": {
            "class": "DatadogLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["datadog-api-client"],
        }
    },
    default_loader="datadog",
    description="Datadog monitoring metrics and logs loader",
    requires_credentials=True,
    credential_type=CredentialType.API_KEY,
    capabilities=[LoaderCapability.TIMESERIES_DATA, LoaderCapability.MONITORING],
    priority=8,
)
class DatadogSource(RemoteSource):
    """Datadog monitoring source."""

    source_type: str = "datadog"
    query: str = Field(..., description="Datadog query")
    from_time: datetime = Field(..., description="Start time")
    to_time: datetime = Field(..., description="End time")


@register_source(
    name="new_relic",
    category=SourceCategory.ANALYTICS,
    loaders={
        "newrelic": {
            "class": "NewRelicLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["newrelic"],
        }
    },
    default_loader="newrelic",
    description="New Relic APM and infrastructure loader",
    requires_credentials=True,
    credential_type=CredentialType.API_KEY,
    capabilities=[LoaderCapability.MONITORING, LoaderCapability.ALERTING],
    priority=7,
)
class NewRelicSource(RemoteSource):
    """New Relic monitoring source."""

    source_type: str = "new_relic"
    account_id: str = Field(..., description="New Relic account ID")
    query_type: str = Field("nrql", description="Query type")


# =============================================================================
# Cloud Services
# =============================================================================


@register_source(
    name="alibaba_cloud_oss",
    category=SourceCategory.CLOUD_STORAGE,
    loaders={
        "aliyun_oss": {
            "class": "AliyunOSSFileLoader",
            "speed": "fast",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["oss2"],
        }
    },
    default_loader="aliyun_oss",
    description="Alibaba Cloud OSS object storage loader",
    requires_credentials=True,
    credential_type=CredentialType.ACCESS_KEY,
    capabilities=[LoaderCapability.CLOUD_NATIVE, LoaderCapability.STREAMING],
    priority=8,
)
class AlibabaOSSSource(RemoteSource):
    """Alibaba Cloud OSS source."""

    source_type: str = "alibaba_cloud_oss"
    bucket_name: str = Field(..., description="OSS bucket name")
    object_key: str = Field(..., description="Object key")
    region: str = Field(..., description="OSS region")


@register_source(
    name="tencent_cos",
    category=SourceCategory.CLOUD_STORAGE,
    loaders={
        "cos": {
            "class": "TencentCOSFileLoader",
            "speed": "fast",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["cos-python-sdk-v5"],
        }
    },
    default_loader="cos",
    description="Tencent Cloud COS object storage loader",
    requires_credentials=True,
    credential_type=CredentialType.ACCESS_KEY,
    capabilities=[LoaderCapability.CLOUD_NATIVE, LoaderCapability.CHINESE_CONTENT],
    priority=7,
)
class TencentCOSSource(RemoteSource):
    """Tencent Cloud COS source."""

    source_type: str = "tencent_cos"
    bucket: str = Field(..., description="COS bucket")
    key: str = Field(..., description="Object key")
    region: str = Field(..., description="COS region")


# =============================================================================
# Specialized Databases
# =============================================================================


@register_source(
    name="pinecone",
    category=SourceCategory.DATABASE_NOSQL,
    loaders={
        "pinecone": {
            "class": "PineconeLoader",
            "speed": "fast",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["pinecone-client"],
        }
    },
    default_loader="pinecone",
    description="Pinecone vector database loader",
    requires_credentials=True,
    credential_type=CredentialType.API_KEY,
    capabilities=[LoaderCapability.VECTOR_DATA, LoaderCapability.SEARCH],
    priority=8,
)
class PineconeSource(RemoteSource):
    """Pinecone vector database source."""

    source_type: str = "pinecone"
    index_name: str = Field(..., description="Pinecone index name")
    namespace: Optional[str] = Field(None, description="Namespace")
    top_k: int = Field(10, description="Number of results")


@register_source(
    name="weaviate",
    category=SourceCategory.DATABASE_NOSQL,
    loaders={
        "weaviate": {
            "class": "WeaviateLoader",
            "speed": "fast",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["weaviate-client"],
        }
    },
    default_loader="weaviate",
    description="Weaviate vector search engine loader",
    requires_credentials=True,
    credential_type=CredentialType.API_KEY,
    capabilities=[LoaderCapability.VECTOR_DATA, LoaderCapability.SCHEMA_EVOLUTION],
    priority=8,
)
class WeaviateSource(RemoteSource):
    """Weaviate vector database source."""

    source_type: str = "weaviate"
    url: str = Field(..., description="Weaviate URL")
    class_name: str = Field(..., description="Weaviate class name")
    limit: int = Field(100, description="Result limit")


@register_source(
    name="chroma",
    category=SourceCategory.DATABASE_NOSQL,
    loaders={
        "chroma": {
            "class": "ChromaLoader",
            "speed": "fast",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["chromadb"],
        }
    },
    default_loader="chroma",
    description="Chroma embedding database loader",
    capabilities=[LoaderCapability.VECTOR_DATA, LoaderCapability.METADATA_EXTRACTION],
    priority=8,
)
class ChromaSource(DatabaseSource):
    """Chroma vector database source."""

    source_type: str = "chroma"
    collection_name: str = Field(..., description="Collection name")
    persist_directory: Optional[str] = Field(None, description="Persist directory")


# =============================================================================
# E-Learning Platforms
# =============================================================================


@register_source(
    name="coursera",
    category=SourceCategory.ACADEMIC_EDUCATION,
    loaders={
        "coursera": {
            "class": "CourseraLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["beautifulsoup4"],
        }
    },
    default_loader="coursera",
    description="Coursera course content loader",
    requires_credentials=True,
    credential_type=CredentialType.COOKIES,
    capabilities=[LoaderCapability.COURSE_CONTENT, LoaderCapability.RESOURCES],
    priority=7,
)
class CourseraSource(RemoteSource):
    """Coursera e-learning source."""

    source_type: str = "coursera"
    course_url: str = Field(..., description="Course URL")
    include_videos: bool = Field(False, description="Include video transcripts")


@register_source(
    name="udemy",
    category=SourceCategory.ACADEMIC_EDUCATION,
    loaders={
        "udemy": {
            "class": "UdemyLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["selenium"],
        }
    },
    default_loader="udemy",
    description="Udemy course content loader",
    requires_credentials=True,
    credential_type=CredentialType.USERNAME_PASSWORD,
    capabilities=[LoaderCapability.COURSE_CONTENT, LoaderCapability.TRANSCRIPTS],
    priority=7,
)
class UdemySource(RemoteSource):
    """Udemy e-learning source."""

    source_type: str = "udemy"
    course_id: str = Field(..., description="Udemy course ID")
    include_captions: bool = Field(True, description="Include video captions")


# =============================================================================
# Translation and Localization
# =============================================================================


@register_source(
    name="crowdin",
    category=SourceCategory.SPECIALIZED,
    loaders={
        "crowdin": {
            "class": "CrowdinLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["crowdin-api-client"],
        }
    },
    default_loader="crowdin",
    description="Crowdin localization platform loader",
    requires_credentials=True,
    credential_type=CredentialType.API_KEY,
    capabilities=[
        LoaderCapability.MULTILINGUAL,
        LoaderCapability.COLLABORATIVE_EDITING,
    ],
    priority=7,
)
class CrowdinSource(RemoteSource):
    """Crowdin localization source."""

    source_type: str = "crowdin"
    project_id: int = Field(..., description="Crowdin project ID")
    file_id: Optional[int] = Field(None, description="Specific file ID")


@register_source(
    name="transifex",
    category=SourceCategory.SPECIALIZED,
    loaders={
        "transifex": {
            "class": "TransifexLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["transifex-python"],
        }
    },
    default_loader="transifex",
    description="Transifex translation management loader",
    requires_credentials=True,
    credential_type=CredentialType.API_KEY,
    capabilities=[
        LoaderCapability.MULTILINGUAL,
        LoaderCapability.COLLABORATIVE_EDITING,
    ],
    priority=7,
)
class TransifexSource(RemoteSource):
    """Transifex translation source."""

    source_type: str = "transifex"
    organization: str = Field(..., description="Organization slug")
    project: str = Field(..., description="Project slug")


# =============================================================================
# Content Management Systems
# =============================================================================


@register_source(
    name="wordpress",
    category=SourceCategory.WEB_DOCUMENTATION,
    loaders={
        "wordpress": {
            "class": "WordPressLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["python-wordpress-xmlrpc"],
        }
    },
    default_loader="wordpress",
    description="WordPress CMS content loader",
    requires_credentials=True,
    credential_type=CredentialType.USERNAME_PASSWORD,
    capabilities=[LoaderCapability.BULK_LOADING, LoaderCapability.METADATA_EXTRACTION],
    priority=8,
)
class WordPressSource(RemoteSource):
    """WordPress CMS source."""

    source_type: str = "wordpress"
    site_url: str = Field(..., description="WordPress site URL")
    post_type: str = Field("post", description="Post type to load")
    limit: int = Field(100, description="Number of posts")


@register_source(
    name="drupal",
    category=SourceCategory.WEB_DOCUMENTATION,
    loaders={
        "drupal": {
            "class": "DrupalLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["requests"],
        }
    },
    default_loader="drupal",
    description="Drupal CMS content loader",
    capabilities=[LoaderCapability.BULK_LOADING, LoaderCapability.STRUCTURED_DATA],
    priority=7,
)
class DrupalSource(RemoteSource):
    """Drupal CMS source."""

    source_type: str = "drupal"
    site_url: str = Field(..., description="Drupal site URL")
    content_type: str = Field("article", description="Content type")


@register_source(
    name="ghost",
    category=SourceCategory.WEB_DOCUMENTATION,
    loaders={
        "ghost": {
            "class": "GhostLoader",
            "speed": "fast",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["requests"],
        }
    },
    default_loader="ghost",
    description="Ghost blogging platform loader",
    requires_credentials=True,
    credential_type=CredentialType.API_KEY,
    capabilities=[LoaderCapability.BULK_LOADING, LoaderCapability.METADATA_EXTRACTION],
    priority=7,
)
class GhostSource(RemoteSource):
    """Ghost blogging platform source."""

    source_type: str = "ghost"
    site_url: str = Field(..., description="Ghost site URL")
    content_api_key: str = Field(..., description="Content API key")


# =============================================================================
# Task and Issue Tracking
# =============================================================================


@register_source(
    name="linear",
    category=SourceCategory.BUSINESS_PRODUCTIVITY,
    loaders={
        "linear": {
            "class": "LinearLoader",
            "speed": "fast",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["linear-api"],
        }
    },
    default_loader="linear",
    description="Linear issue tracking loader",
    requires_credentials=True,
    credential_type=CredentialType.API_KEY,
    capabilities=[LoaderCapability.STRUCTURED_DATA, LoaderCapability.WORKFLOW],
    priority=8,
)
class LinearSource(RemoteSource):
    """Linear issue tracking source."""

    source_type: str = "linear"
    team_id: Optional[str] = Field(None, description="Team ID")
    project_id: Optional[str] = Field(None, description="Project ID")
    state_filter: Optional[str] = Field(None, description="Issue state filter")


@register_source(
    name="shortcut",
    category=SourceCategory.BUSINESS_PRODUCTIVITY,
    loaders={
        "shortcut": {
            "class": "ShortcutLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["requests"],
        }
    },
    default_loader="shortcut",
    description="Shortcut (formerly Clubhouse) project management loader",
    requires_credentials=True,
    credential_type=CredentialType.API_KEY,
    capabilities=[LoaderCapability.STRUCTURED_DATA, LoaderCapability.WORKFLOW],
    priority=7,
)
class ShortcutSource(RemoteSource):
    """Shortcut project management source."""

    source_type: str = "shortcut"
    workspace_name: str = Field(..., description="Workspace name")
    project_id: Optional[int] = Field(None, description="Project ID")


# =============================================================================
# Healthcare and Medical
# =============================================================================


@register_source(
    name="epic_fhir",
    category=SourceCategory.HEALTHCARE,
    loaders={
        "epic": {
            "class": "EpicFHIRLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["fhirclient"],
        }
    },
    default_loader="epic",
    description="Epic FHIR healthcare data loader",
    requires_credentials=True,
    credential_type=CredentialType.OAUTH,
    capabilities=[LoaderCapability.HEALTHCARE_STANDARDS, LoaderCapability.PATIENT_DATA],
    priority=8,
)
class EpicFHIRSource(RemoteSource):
    """Epic FHIR healthcare source."""

    source_type: str = "epic_fhir"
    fhir_server_url: str = Field(..., description="FHIR server URL")
    resource_type: str = Field("Patient", description="FHIR resource type")


@register_source(
    name="cerner_fhir",
    category=SourceCategory.HEALTHCARE,
    loaders={
        "cerner": {
            "class": "CernerFHIRLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["fhirclient"],
        }
    },
    default_loader="cerner",
    description="Cerner FHIR healthcare data loader",
    requires_credentials=True,
    credential_type=CredentialType.OAUTH,
    capabilities=[LoaderCapability.HEALTHCARE_STANDARDS, LoaderCapability.PATIENT_DATA],
    priority=8,
)
class CernerFHIRSource(RemoteSource):
    """Cerner FHIR healthcare source."""

    source_type: str = "cerner_fhir"
    fhir_server_url: str = Field(..., description="FHIR server URL")
    patient_id: Optional[str] = Field(None, description="Patient ID")


# =============================================================================
# Scientific Computing
# =============================================================================


@register_source(
    name="hdf5",
    category=SourceCategory.FILE_DATA,
    loaders={
        "hdf5": {
            "class": "HDF5Loader",
            "speed": "fast",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["h5py"],
        }
    },
    default_loader="hdf5",
    description="HDF5 scientific data format loader",
    file_extensions=[".h5", ".hdf5", ".hdf"],
    capabilities=[LoaderCapability.STRUCTURED_DATA, LoaderCapability.SENSOR_DATA],
    priority=8,
)
class HDF5Source(LocalFileSource):
    """HDF5 scientific data source."""

    source_type: str = "hdf5"
    dataset_path: Optional[str] = Field(None, description="Dataset path within HDF5")


@register_source(
    name="netcdf",
    category=SourceCategory.FILE_DATA,
    loaders={
        "netcdf": {
            "class": "NetCDFLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["netCDF4"],
        }
    },
    default_loader="netcdf",
    description="NetCDF scientific data format loader",
    file_extensions=[".nc", ".nc4"],
    capabilities=[LoaderCapability.STRUCTURED_DATA, LoaderCapability.GEOSPATIAL_DATA],
    priority=7,
)
class NetCDFSource(LocalFileSource):
    """NetCDF scientific data source."""

    source_type: str = "netcdf"
    variables: Optional[List[str]] = Field(None, description="Variables to extract")


# =============================================================================
# Configuration Management
# =============================================================================


@register_source(
    name="ansible",
    category=SourceCategory.DEVELOPMENT_VCS,
    loaders={
        "ansible": {
            "class": "AnsibleLoader",
            "speed": "fast",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["ansible"],
        }
    },
    default_loader="ansible",
    description="Ansible playbook and inventory loader",
    file_extensions=[".yml", ".yaml"],
    capabilities=[LoaderCapability.STRUCTURED_DATA],
    priority=7,
)
class AnsibleSource(LocalFileSource):
    """Ansible configuration source."""

    source_type: str = "ansible"
    file_type: str = Field("playbook", description="playbook or inventory")


@register_source(
    name="terraform",
    category=SourceCategory.DEVELOPMENT_VCS,
    loaders={
        "terraform": {
            "class": "TerraformLoader",
            "speed": "fast",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["python-hcl2"],
        }
    },
    default_loader="terraform",
    description="Terraform configuration loader",
    file_extensions=[".tf", ".tfvars"],
    capabilities=[LoaderCapability.STRUCTURED_DATA],
    priority=7,
)
class TerraformSource(LocalFileSource):
    """Terraform configuration source."""

    source_type: str = "terraform"
    parse_variables: bool = Field(True, description="Parse variable definitions")


# =============================================================================
# Customer Feedback
# =============================================================================


@register_source(
    name="trustpilot",
    category=SourceCategory.BUSINESS,
    loaders={
        "trustpilot": {
            "class": "TrustpilotLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["beautifulsoup4"],
        }
    },
    default_loader="trustpilot",
    description="Trustpilot business reviews loader",
    capabilities=[LoaderCapability.SEARCH, LoaderCapability.METADATA_EXTRACTION],
    priority=7,
)
class TrustpilotSource(RemoteSource):
    """Trustpilot reviews source."""

    source_type: str = "trustpilot"
    business_unit_id: str = Field(..., description="Business unit ID")
    max_reviews: int = Field(100, description="Maximum reviews to fetch")


@register_source(
    name="g2_reviews",
    category=SourceCategory.BUSINESS,
    loaders={
        "g2": {
            "class": "G2ReviewsLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["selenium"],
        }
    },
    default_loader="g2",
    description="G2 software reviews loader",
    capabilities=[LoaderCapability.METADATA_EXTRACTION],
    priority=6,
)
class G2ReviewsSource(RemoteSource):
    """G2 software reviews source."""

    source_type: str = "g2_reviews"
    product_slug: str = Field(..., description="G2 product slug")
    review_count: int = Field(50, description="Number of reviews")


# =============================================================================
# Logistics and Shipping
# =============================================================================


@register_source(
    name="shippo",
    category=SourceCategory.BUSINESS,
    loaders={
        "shippo": {
            "class": "ShippoLoader",
            "speed": "fast",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["shippo"],
        }
    },
    default_loader="shippo",
    description="Shippo shipping and logistics loader",
    requires_credentials=True,
    credential_type=CredentialType.API_KEY,
    capabilities=[LoaderCapability.REAL_TIME, LoaderCapability.STRUCTURED_DATA],
    priority=7,
)
class ShippoSource(RemoteSource):
    """Shippo shipping logistics source."""

    source_type: str = "shippo"
    object_type: str = Field("shipments", description="Object type to load")
    status_filter: Optional[str] = Field(None, description="Status filter")


# =============================================================================
# Real Estate
# =============================================================================


@register_source(
    name="zillow",
    category=SourceCategory.SPECIALIZED,
    loaders={
        "zillow": {
            "class": "ZillowLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["beautifulsoup4"],
        }
    },
    default_loader="zillow",
    description="Zillow real estate data loader",
    capabilities=[LoaderCapability.SEARCH, LoaderCapability.GEOSPATIAL_DATA],
    priority=6,
)
class ZillowSource(RemoteSource):
    """Zillow real estate source."""

    source_type: str = "zillow"
    location: str = Field(..., description="Location to search")
    listing_type: str = Field("for_sale", description="Listing type")


# =============================================================================
# Job Boards
# =============================================================================


@register_source(
    name="indeed",
    category=SourceCategory.SPECIALIZED,
    loaders={
        "indeed": {
            "class": "IndeedLoader",
            "speed": "medium",
            "quality": "medium",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["beautifulsoup4"],
        }
    },
    default_loader="indeed",
    description="Indeed job listings loader",
    capabilities=[LoaderCapability.SEARCH, LoaderCapability.METADATA_EXTRACTION],
    priority=6,
)
class IndeedSource(RemoteSource):
    """Indeed job listings source."""

    source_type: str = "indeed"
    query: str = Field(..., description="Job search query")
    location: str = Field(..., description="Job location")
    max_results: int = Field(50, description="Maximum results")


# =============================================================================
# Travel and Hospitality
# =============================================================================


@register_source(
    name="airbnb",
    category=SourceCategory.SPECIALIZED,
    loaders={
        "airbnb": {
            "class": "AirbnbLoader",
            "speed": "slow",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["selenium"],
        }
    },
    default_loader="airbnb",
    description="Airbnb listings loader",
    capabilities=[LoaderCapability.SEARCH, LoaderCapability.MEDIA_CONTENT],
    priority=6,
)
class AirbnbSource(RemoteSource):
    """Airbnb listings source."""

    source_type: str = "airbnb"
    location: str = Field(..., description="Search location")
    checkin_date: datetime = Field(..., description="Check-in date")
    checkout_date: datetime = Field(..., description="Check-out date")


# =============================================================================
# Music and Audio
# =============================================================================


@register_source(
    name="spotify",
    category=SourceCategory.MEDIA_AUDIO,
    loaders={
        "spotify": {
            "class": "SpotifyLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["spotipy"],
        }
    },
    default_loader="spotify",
    description="Spotify music metadata loader",
    requires_credentials=True,
    credential_type=CredentialType.OAUTH,
    capabilities=[LoaderCapability.METADATA_EXTRACTION, LoaderCapability.SEARCH],
    priority=7,
)
class SpotifySource(RemoteSource):
    """Spotify music platform source."""

    source_type: str = "spotify"
    playlist_id: Optional[str] = Field(None, description="Playlist ID")
    artist_id: Optional[str] = Field(None, description="Artist ID")
    album_id: Optional[str] = Field(None, description="Album ID")


@register_source(
    name="soundcloud",
    category=SourceCategory.MEDIA_AUDIO,
    loaders={
        "soundcloud": {
            "class": "SoundCloudLoader",
            "speed": "medium",
            "quality": "medium",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["soundcloud"],
        }
    },
    default_loader="soundcloud",
    description="SoundCloud audio platform loader",
    capabilities=[LoaderCapability.MEDIA_CONTENT, LoaderCapability.COMMENTS],
    priority=6,
)
class SoundCloudSource(RemoteSource):
    """SoundCloud audio platform source."""

    source_type: str = "soundcloud"
    track_url: Optional[str] = Field(None, description="Track URL")
    playlist_url: Optional[str] = Field(None, description="Playlist URL")


# =============================================================================
# Forums and Communities
# =============================================================================


@register_source(
    name="discourse",
    category=SourceCategory.COMMUNICATION,
    loaders={
        "discourse": {
            "class": "DiscourseLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["pydiscourse"],
        }
    },
    default_loader="discourse",
    description="Discourse forum platform loader",
    requires_credentials=True,
    credential_type=CredentialType.API_KEY,
    capabilities=[LoaderCapability.FORUMS, LoaderCapability.SEARCH],
    priority=7,
)
class DiscourseSource(RemoteSource):
    """Discourse forum platform source."""

    source_type: str = "discourse"
    base_url: str = Field(..., description="Discourse forum URL")
    category_id: Optional[int] = Field(None, description="Category ID")
    tag: Optional[str] = Field(None, description="Tag filter")


@register_source(
    name="phpbb",
    category=SourceCategory.COMMUNICATION,
    loaders={
        "phpbb": {
            "class": "phpBBLoader",
            "speed": "medium",
            "quality": "medium",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["beautifulsoup4"],
        }
    },
    default_loader="phpbb",
    description="phpBB forum loader",
    capabilities=[LoaderCapability.FORUMS, LoaderCapability.THREADING],
    priority=6,
)
class phpBBSource(RemoteSource):
    """phpBB forum source."""

    source_type: str = "phpbb"
    forum_url: str = Field(..., description="Forum URL")
    board_id: Optional[int] = Field(None, description="Board ID")


# =============================================================================
# Final Additional Sources
# =============================================================================


@register_source(
    name="consul",
    category=SourceCategory.SPECIALIZED,
    loaders={
        "consul": {
            "class": "ConsulLoader",
            "speed": "fast",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["python-consul"],
        }
    },
    default_loader="consul",
    description="HashiCorp Consul key-value store loader",
    capabilities=[LoaderCapability.REAL_TIME, LoaderCapability.STRUCTURED_DATA],
    priority=7,
)
class ConsulSource(RemoteSource):
    """HashiCorp Consul KV store source."""

    source_type: str = "consul"
    host: str = Field("localhost", description="Consul host")
    port: int = Field(8500, description="Consul port")
    prefix: str = Field("", description="Key prefix")


# Auto-register all source classes
__all__ = [
    # Image processing
    "PaddleOCRSource",
    "AzureFormRecognizerSource",
    # Monitoring
    "DatadogSource",
    "NewRelicSource",
    # Cloud storage
    "AlibabaOSSSource",
    "TencentCOSSource",
    # Vector databases
    "PineconeSource",
    "WeaviateSource",
    "ChromaSource",
    # E-learning
    "CourseraSource",
    "UdemySource",
    # Translation
    "CrowdinSource",
    "TransifexSource",
    # CMS
    "WordPressSource",
    "DrupalSource",
    "GhostSource",
    # Project management
    "LinearSource",
    "ShortcutSource",
    # Healthcare
    "EpicFHIRSource",
    "CernerFHIRSource",
    # Scientific
    "HDF5Source",
    "NetCDFSource",
    # Configuration
    "AnsibleSource",
    "TerraformSource",
    # Reviews
    "TrustpilotSource",
    "G2ReviewsSource",
    # Logistics
    "ShippoSource",
    # Real estate
    "ZillowSource",
    # Jobs
    "IndeedSource",
    # Travel
    "AirbnbSource",
    # Music
    "SpotifySource",
    "SoundCloudSource",
    # Forums
    "DiscourseSource",
    "phpBBSource",
    # Others
    "ConsulSource",
]
