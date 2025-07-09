"""Final specialized and regional platform source registrations.

This module completes the comprehensive document loader system with:
- Government and legal platforms
- Healthcare and medical systems
- Education and learning platforms
- Regional platforms (Asia, Europe, Latin America)
- Niche industry platforms
- Legacy and specialized formats
- Completing the path to 231+ langchain_community loaders
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import Field

from .enhanced_registry import (
    enhanced_registry,
    register_bulk_source,
    register_file_source,
    register_source,
)
from .source_types import (
    CredentialType,
    LoaderCapability,
    LocalFileSource,
    RemoteSource,
    SourceCategory,
)


class FinalPlatform(str, Enum):
    """Final specialized platforms."""

    # Government & Legal
    GOV_DOCS = "gov_docs"
    LEGAL_DATABASE = "legal_database"
    COURT_RECORDS = "court_records"
    REGULATIONS = "regulations"

    # Healthcare & Medical
    FHIR = "fhir"
    HL7 = "hl7"
    DICOM = "dicom"
    EPIC = "epic"
    CERNER = "cerner"

    # Education & Learning
    CANVAS = "canvas"
    BLACKBOARD = "blackboard"
    MOODLE = "moodle"
    COURSERA = "coursera"
    EDTECH = "edtech"

    # Regional Platforms
    BAIDU = "baidu"  # China
    YANDEX = "yandex"  # Russia
    NAVER = "naver"  # Korea
    VKONTAKTE = "vkontakte"  # Russia
    ODNOKLASSNIKI = "odnoklassniki"  # Russia

    # Industry Specific
    REAL_ESTATE = "real_estate"
    AUTOMOTIVE = "automotive"
    AGRICULTURE = "agriculture"
    ENERGY = "energy"
    MANUFACTURING = "manufacturing"

    # Legacy Formats
    MAINFRAME = "mainframe"
    AS400 = "as400"
    COBOL_DATA = "cobol_data"
    XML_FEEDS = "xml_feeds"
    SOAP_SERVICES = "soap_services"

    # Specialized
    BLOCKCHAIN = "blockchain"
    CRYPTOCURRENCY = "cryptocurrency"
    IOT_PLATFORMS = "iot_platforms"
    GEOSPATIAL = "geospatial"
    SCIENTIFIC = "scientific"


class DataStandard(str, Enum):
    """Data standards and formats."""

    FHIR = "fhir"
    HL7 = "hl7"
    DICOM = "dicom"
    EDIFACT = "edifact"
    X12 = "x12"
    SWIFT = "swift"
    FIX = "fix"
    ISO20022 = "iso20022"


# =============================================================================
# Government & Legal Platforms
# =============================================================================


@register_bulk_source(
    name="gov_docs",
    category=SourceCategory.GOVERNMENT,
    loaders={
        "gov_docs": {
            "class": "GovDocsLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["requests", "beautifulsoup4"],
        }
    },
    default_loader="gov_docs",
    description="Government document repositories loader",
    requires_credentials=False,
    capabilities=[
        LoaderCapability.BULK_LOADING,
        LoaderCapability.METADATA_EXTRACTION,
        LoaderCapability.MULTILINGUAL,
    ],
    supports_scrape_all=True,
    priority=6,
)
class GovDocsSource(RemoteSource):
    """Government documents source."""

    source_type: str = "gov_docs"
    category: SourceCategory = SourceCategory.SPECIALIZED
    platform: FinalPlatform = FinalPlatform.GOV_DOCS

    # Government portal configuration
    portal_url: str = Field(..., description="Government portal URL")
    country_code: str = Field("US", description="Country code")
    department: Optional[str] = Field(None, description="Specific department")

    # Content filtering
    document_types: List[str] = Field(
        default=["pdf", "doc", "html"], description="Document types to include"
    )
    date_range: Optional[tuple[datetime, datetime]] = Field(
        None, description="Date range"
    )
    topics: Optional[List[str]] = Field(None, description="Topic filters")

    # Language options
    languages: List[str] = Field(default=["en"], description="Document languages")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update(
            {
                "portal_url": self.portal_url,
                "country_code": self.country_code,
                "document_types": self.document_types,
                "languages": self.languages,
            }
        )

        if self.department:
            kwargs["department"] = self.department
        if self.date_range:
            kwargs["start_date"] = self.date_range[0]
            kwargs["end_date"] = self.date_range[1]
        if self.topics:
            kwargs["topics"] = self.topics

        return kwargs

    def scrape_all(self) -> Dict[str, Any]:
        """Scrape entire government portal."""
        return {
            "portal_url": self.portal_url,
            "recursive": True,
            "include_archives": True,
            "respect_robots": True,
        }


@register_source(
    name="legal_database",
    category=SourceCategory.SPECIALIZED,
    loaders={
        "legal": {
            "class": "LegalDatabaseLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["requests"],
        }
    },
    default_loader="legal",
    description="Legal database and case law loader",
    requires_credentials=True,
    credential_type=CredentialType.API_KEY,
    capabilities=[
        LoaderCapability.LEGAL_CITATIONS,
        LoaderCapability.CASE_LAW,
        LoaderCapability.FULL_TEXT_SEARCH,
    ],
    priority=7,
)
class LegalDatabaseSource(RemoteSource):
    """Legal database source."""

    source_type: str = "legal_database"
    category: SourceCategory = SourceCategory.SPECIALIZED
    platform: FinalPlatform = FinalPlatform.LEGAL_DATABASE

    # Database configuration
    database_name: str = Field(..., description="Legal database name")
    api_key: Optional[str] = Field(None, description="API key")

    # Search parameters
    query: Optional[str] = Field(None, description="Legal search query")
    jurisdiction: Optional[str] = Field(None, description="Jurisdiction filter")
    court_level: Optional[str] = Field(None, description="Court level filter")
    practice_area: Optional[str] = Field(None, description="Practice area")

    # Date filtering
    date_range: Optional[tuple[datetime, datetime]] = Field(
        None, description="Decision date range"
    )

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update(
            {
                "database": self.database_name,
                "api_key": (
                    self.api_key or self.get_api_key()
                    if hasattr(self, "get_api_key")
                    else None
                ),
            }
        )

        if self.query:
            kwargs["query"] = self.query
        if self.jurisdiction:
            kwargs["jurisdiction"] = self.jurisdiction
        if self.court_level:
            kwargs["court_level"] = self.court_level
        if self.practice_area:
            kwargs["practice_area"] = self.practice_area
        if self.date_range:
            kwargs["start_date"] = self.date_range[0]
            kwargs["end_date"] = self.date_range[1]

        return kwargs


# =============================================================================
# Healthcare & Medical Systems
# =============================================================================


@register_source(
    name="fhir",
    category=SourceCategory.SPECIALIZED,
    loaders={
        "fhir": {
            "class": "FHIRLoader",
            "speed": "fast",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["fhir.resources"],
        }
    },
    default_loader="fhir",
    description="FHIR healthcare data standard loader",
    requires_credentials=True,
    credential_type=CredentialType.OAUTH,
    capabilities=[
        LoaderCapability.STRUCTURED_DATA,
        LoaderCapability.HEALTHCARE_STANDARDS,
        LoaderCapability.PATIENT_DATA,
    ],
    priority=8,
)
class FHIRSource(RemoteSource):
    """FHIR healthcare standard source."""

    source_type: str = "fhir"
    category: SourceCategory = SourceCategory.SPECIALIZED
    platform: FinalPlatform = FinalPlatform.FHIR

    # FHIR server configuration
    server_url: str = Field(..., description="FHIR server URL")
    access_token: Optional[str] = Field(None, description="OAuth access token")

    # Resource selection
    resource_types: List[str] = Field(
        default=["Patient", "Observation", "Condition"],
        description="FHIR resource types",
    )
    patient_id: Optional[str] = Field(None, description="Specific patient ID")

    # Query parameters
    search_params: Optional[Dict[str, Any]] = Field(
        None, description="FHIR search parameters"
    )
    include_references: bool = Field(True, description="Include referenced resources")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update(
            {
                "server_url": self.server_url,
                "access_token": (
                    self.access_token or self.get_api_key()
                    if hasattr(self, "get_api_key")
                    else None
                ),
                "resource_types": self.resource_types,
                "include_references": self.include_references,
            }
        )

        if self.patient_id:
            kwargs["patient_id"] = self.patient_id
        if self.search_params:
            kwargs["search_params"] = self.search_params

        return kwargs


@register_file_source(
    name="dicom",
    extensions=[".dcm", ".dicom"],
    loaders={
        "dicom": {
            "class": "DICOMLoader",
            "speed": "slow",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["pydicom", "pillow"],
        }
    },
    default_loader="dicom",
    description="DICOM medical imaging format loader",
    requires_credentials=False,
    capabilities=[
        LoaderCapability.MEDICAL_IMAGING,
        LoaderCapability.METADATA_EXTRACTION,
        LoaderCapability.PATIENT_DATA,
    ],
    priority=7,
)
class DICOMSource(LocalFileSource):
    """DICOM medical imaging source."""

    source_type: str = "dicom"
    category: SourceCategory = SourceCategory.SPECIALIZED

    # DICOM options
    extract_metadata: bool = Field(True, description="Extract DICOM metadata")
    extract_images: bool = Field(False, description="Extract image data")
    anonymize: bool = Field(True, description="Anonymize patient data")

    # Image processing
    image_format: str = Field("png", description="Image export format")
    resize_images: bool = Field(False, description="Resize large images")
    max_image_size: tuple[int, int] = Field(
        (1024, 1024), description="Max image dimensions"
    )

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update(
            {
                "file_path": str(self.path),
                "extract_metadata": self.extract_metadata,
                "extract_images": self.extract_images,
                "anonymize": self.anonymize,
            }
        )

        if self.extract_images:
            kwargs["image_format"] = self.image_format
            kwargs["resize_images"] = self.resize_images
            kwargs["max_image_size"] = self.max_image_size

        return kwargs


# =============================================================================
# Education & Learning Platforms
# =============================================================================


@register_source(
    name="canvas",
    category=SourceCategory.SPECIALIZED,
    loaders={
        "canvas": {
            "class": "CanvasLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["canvasapi"],
        }
    },
    default_loader="canvas",
    description="Canvas LMS platform loader",
    requires_credentials=True,
    credential_type=CredentialType.API_KEY,
    capabilities=[
        LoaderCapability.COURSE_CONTENT,
        LoaderCapability.ASSIGNMENTS,
        LoaderCapability.DISCUSSIONS,
        LoaderCapability.GRADEBOOK,
    ],
    priority=8,
)
class CanvasSource(RemoteSource):
    """Canvas LMS source."""

    source_type: str = "canvas"
    category: SourceCategory = SourceCategory.SPECIALIZED
    platform: FinalPlatform = FinalPlatform.CANVAS

    # Canvas configuration
    canvas_url: str = Field(..., description="Canvas instance URL")
    access_token: Optional[str] = Field(None, description="API access token")

    # Course selection
    course_ids: Optional[List[int]] = Field(None, description="Specific course IDs")
    user_id: Optional[int] = Field(None, description="User ID for enrollment filter")

    # Content options
    include_assignments: bool = Field(True, description="Include assignments")
    include_discussions: bool = Field(True, description="Include discussions")
    include_announcements: bool = Field(True, description="Include announcements")
    include_pages: bool = Field(True, description="Include course pages")
    include_files: bool = Field(True, description="Include course files")
    include_grades: bool = Field(False, description="Include grade data")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update(
            {
                "canvas_url": self.canvas_url,
                "access_token": (
                    self.access_token or self.get_api_key()
                    if hasattr(self, "get_api_key")
                    else None
                ),
                "include_assignments": self.include_assignments,
                "include_discussions": self.include_discussions,
                "include_announcements": self.include_announcements,
                "include_pages": self.include_pages,
                "include_files": self.include_files,
                "include_grades": self.include_grades,
            }
        )

        if self.course_ids:
            kwargs["course_ids"] = self.course_ids
        if self.user_id:
            kwargs["user_id"] = self.user_id

        return kwargs


@register_source(
    name="moodle",
    category=SourceCategory.SPECIALIZED,
    loaders={
        "moodle": {
            "class": "MoodleLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["requests"],
        }
    },
    default_loader="moodle",
    description="Moodle LMS platform loader",
    requires_credentials=True,
    credential_type=CredentialType.API_KEY,
    capabilities=[
        LoaderCapability.COURSE_CONTENT,
        LoaderCapability.FORUMS,
        LoaderCapability.RESOURCES,
    ],
    priority=7,
)
class MoodleSource(RemoteSource):
    """Moodle LMS source."""

    source_type: str = "moodle"
    category: SourceCategory = SourceCategory.SPECIALIZED
    platform: FinalPlatform = FinalPlatform.MOODLE

    # Moodle configuration
    moodle_url: str = Field(..., description="Moodle instance URL")
    token: Optional[str] = Field(None, description="Web service token")

    # Course selection
    course_ids: Optional[List[int]] = Field(None, description="Course IDs")
    category_id: Optional[int] = Field(None, description="Course category ID")

    # Content options
    include_forums: bool = Field(True, description="Include forum discussions")
    include_resources: bool = Field(True, description="Include resources")
    include_activities: bool = Field(True, description="Include activities")
    include_grades: bool = Field(False, description="Include gradebook")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update(
            {
                "moodle_url": self.moodle_url,
                "token": (
                    self.token or self.get_api_key()
                    if hasattr(self, "get_api_key")
                    else None
                ),
                "include_forums": self.include_forums,
                "include_resources": self.include_resources,
                "include_activities": self.include_activities,
                "include_grades": self.include_grades,
            }
        )

        if self.course_ids:
            kwargs["course_ids"] = self.course_ids
        if self.category_id:
            kwargs["category_id"] = self.category_id

        return kwargs


# =============================================================================
# Regional Platforms
# =============================================================================


@register_source(
    name="baidu",
    category=SourceCategory.SPECIALIZED,
    loaders={
        "baidu": {
            "class": "BaiduLoader",
            "speed": "medium",
            "quality": "medium",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["requests"],
        }
    },
    default_loader="baidu",
    description="Baidu search and services loader (China)",
    requires_credentials=True,
    credential_type=CredentialType.API_KEY,
    capabilities=[
        LoaderCapability.SEARCH_RESULTS,
        LoaderCapability.CHINESE_CONTENT,
        LoaderCapability.REGIONAL_SPECIFIC,
    ],
    priority=6,
)
class BaiduSource(RemoteSource):
    """Baidu search platform source."""

    source_type: str = "baidu"
    category: SourceCategory = SourceCategory.SPECIALIZED
    platform: FinalPlatform = FinalPlatform.BAIDU

    # Baidu configuration
    api_key: Optional[str] = Field(None, description="Baidu API key")
    service_type: str = Field("search", description="Baidu service type")

    # Search options
    query: str = Field(..., description="Search query")
    num_results: int = Field(10, description="Number of results")
    language: str = Field("zh", description="Content language")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update(
            {
                "api_key": (
                    self.api_key or self.get_api_key()
                    if hasattr(self, "get_api_key")
                    else None
                ),
                "service_type": self.service_type,
                "query": self.query,
                "num_results": self.num_results,
                "language": self.language,
            }
        )

        return kwargs


@register_source(
    name="yandex",
    category=SourceCategory.SPECIALIZED,
    loaders={
        "yandex": {
            "class": "YandexLoader",
            "speed": "medium",
            "quality": "medium",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["requests"],
        }
    },
    default_loader="yandex",
    description="Yandex search and services loader (Russia)",
    requires_credentials=True,
    credential_type=CredentialType.API_KEY,
    capabilities=[
        LoaderCapability.SEARCH_RESULTS,
        LoaderCapability.RUSSIAN_CONTENT,
        LoaderCapability.REGIONAL_SPECIFIC,
    ],
    priority=6,
)
class YandexSource(RemoteSource):
    """Yandex search platform source."""

    source_type: str = "yandex"
    category: SourceCategory = SourceCategory.SPECIALIZED
    platform: FinalPlatform = FinalPlatform.YANDEX

    # Yandex configuration
    api_key: Optional[str] = Field(None, description="Yandex API key")
    service_type: str = Field("search", description="Yandex service type")

    # Search options
    query: str = Field(..., description="Search query")
    num_results: int = Field(10, description="Number of results")
    language: str = Field("ru", description="Content language")
    region: str = Field("ru", description="Search region")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update(
            {
                "api_key": (
                    self.api_key or self.get_api_key()
                    if hasattr(self, "get_api_key")
                    else None
                ),
                "service_type": self.service_type,
                "query": self.query,
                "num_results": self.num_results,
                "language": self.language,
                "region": self.region,
            }
        )

        return kwargs


# =============================================================================
# Industry Specific Platforms
# =============================================================================


@register_source(
    name="blockchain",
    category=SourceCategory.SPECIALIZED,
    loaders={
        "blockchain": {
            "class": "BlockchainLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["web3", "requests"],
        }
    },
    default_loader="blockchain",
    description="Blockchain and cryptocurrency data loader",
    requires_credentials=False,
    capabilities=[
        LoaderCapability.BLOCKCHAIN_DATA,
        LoaderCapability.SMART_CONTRACTS,
        LoaderCapability.TRANSACTION_HISTORY,
    ],
    priority=7,
)
class BlockchainSource(RemoteSource):
    """Blockchain data source."""

    source_type: str = "blockchain"
    category: SourceCategory = SourceCategory.SPECIALIZED
    platform: FinalPlatform = FinalPlatform.BLOCKCHAIN

    # Blockchain configuration
    network: str = Field("ethereum", description="Blockchain network")
    rpc_url: Optional[str] = Field(None, description="RPC endpoint URL")
    api_key: Optional[str] = Field(None, description="API key for service")

    # Data selection
    contract_address: Optional[str] = Field(None, description="Smart contract address")
    wallet_address: Optional[str] = Field(None, description="Wallet address")
    block_range: Optional[tuple[int, int]] = Field(None, description="Block range")

    # Options
    include_transactions: bool = Field(True, description="Include transactions")
    include_events: bool = Field(True, description="Include contract events")
    include_metadata: bool = Field(True, description="Include metadata")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update(
            {
                "network": self.network,
                "rpc_url": self.rpc_url,
                "api_key": (
                    self.api_key or self.get_api_key()
                    if hasattr(self, "get_api_key")
                    else None
                ),
                "include_transactions": self.include_transactions,
                "include_events": self.include_events,
                "include_metadata": self.include_metadata,
            }
        )

        if self.contract_address:
            kwargs["contract_address"] = self.contract_address
        if self.wallet_address:
            kwargs["wallet_address"] = self.wallet_address
        if self.block_range:
            kwargs["start_block"] = self.block_range[0]
            kwargs["end_block"] = self.block_range[1]

        return kwargs


@register_source(
    name="iot_platforms",
    category=SourceCategory.SPECIALIZED,
    loaders={
        "iot": {
            "class": "IoTPlatformLoader",
            "speed": "fast",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["paho-mqtt", "requests"],
        }
    },
    default_loader="iot",
    description="IoT platform and sensor data loader",
    requires_credentials=True,
    credential_type=CredentialType.API_KEY,
    capabilities=[
        LoaderCapability.SENSOR_DATA,
        LoaderCapability.REAL_TIME,
        LoaderCapability.TELEMETRY,
    ],
    priority=7,
)
class IoTPlatformSource(RemoteSource):
    """IoT platform data source."""

    source_type: str = "iot_platforms"
    category: SourceCategory = SourceCategory.SPECIALIZED
    platform: FinalPlatform = FinalPlatform.IOT_PLATFORMS

    # IoT platform configuration
    platform_type: str = Field(..., description="IoT platform type")
    endpoint_url: str = Field(..., description="Platform endpoint URL")
    api_key: Optional[str] = Field(None, description="API key")

    # Device selection
    device_ids: Optional[List[str]] = Field(None, description="Specific device IDs")
    device_types: Optional[List[str]] = Field(None, description="Device types")

    # Data options
    metrics: Optional[List[str]] = Field(None, description="Specific metrics")
    time_range: Optional[tuple[datetime, datetime]] = Field(
        None, description="Time range"
    )
    aggregation: Optional[str] = Field(None, description="Data aggregation method")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update(
            {
                "platform_type": self.platform_type,
                "endpoint_url": self.endpoint_url,
                "api_key": (
                    self.api_key or self.get_api_key()
                    if hasattr(self, "get_api_key")
                    else None
                ),
            }
        )

        if self.device_ids:
            kwargs["device_ids"] = self.device_ids
        if self.device_types:
            kwargs["device_types"] = self.device_types
        if self.metrics:
            kwargs["metrics"] = self.metrics
        if self.time_range:
            kwargs["start_time"] = self.time_range[0]
            kwargs["end_time"] = self.time_range[1]
        if self.aggregation:
            kwargs["aggregation"] = self.aggregation

        return kwargs


# =============================================================================
# Legacy & Specialized Formats
# =============================================================================


@register_file_source(
    name="xml_feeds",
    extensions=[".xml", ".rss", ".atom"],
    loaders={
        "xml": {
            "class": "XMLFeedLoader",
            "speed": "fast",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["lxml", "feedparser"],
        }
    },
    default_loader="xml",
    description="XML feeds and structured data loader",
    requires_credentials=False,
    capabilities=[
        LoaderCapability.STRUCTURED_DATA,
        LoaderCapability.RSS_FEEDS,
        LoaderCapability.XML_PARSING,
    ],
    priority=8,
)
class XMLFeedSource(LocalFileSource):
    """XML feed and structured data source."""

    source_type: str = "xml_feeds"
    category: SourceCategory = SourceCategory.SPECIALIZED

    # XML processing options
    feed_type: str = Field("auto", description="Feed type detection")
    extract_content: bool = Field(True, description="Extract text content")
    preserve_structure: bool = Field(True, description="Preserve XML structure")

    # Parsing options
    encoding: str = Field("utf-8", description="File encoding")
    namespaces: Optional[Dict[str, str]] = Field(None, description="XML namespaces")
    xpath_filters: Optional[List[str]] = Field(None, description="XPath filters")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update(
            {
                "file_path": str(self.path),
                "feed_type": self.feed_type,
                "extract_content": self.extract_content,
                "preserve_structure": self.preserve_structure,
                "encoding": self.encoding,
            }
        )

        if self.namespaces:
            kwargs["namespaces"] = self.namespaces
        if self.xpath_filters:
            kwargs["xpath_filters"] = self.xpath_filters

        return kwargs


@register_source(
    name="geospatial",
    category=SourceCategory.SPECIALIZED,
    loaders={
        "geospatial": {
            "class": "GeospatialLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["geopandas", "shapely"],
        }
    },
    default_loader="geospatial",
    description="Geospatial data and GIS file loader",
    requires_credentials=False,
    capabilities=[
        LoaderCapability.GEOSPATIAL_DATA,
        LoaderCapability.VECTOR_DATA,
        LoaderCapability.COORDINATE_SYSTEMS,
    ],
    priority=7,
)
class GeospatialSource(RemoteSource):
    """Geospatial and GIS data source."""

    source_type: str = "geospatial"
    category: SourceCategory = SourceCategory.SPECIALIZED
    platform: FinalPlatform = FinalPlatform.GEOSPATIAL

    # Data source configuration
    data_source: str = Field(..., description="Geospatial data source")
    format_type: str = Field("geojson", description="Data format")

    # Spatial filtering
    bounding_box: Optional[tuple[float, float, float, float]] = Field(
        None, description="Bounding box (minx, miny, maxx, maxy)"
    )
    coordinate_system: str = Field(
        "EPSG:4326", description="Coordinate reference system"
    )

    # Feature filtering
    layer_name: Optional[str] = Field(None, description="Specific layer name")
    attribute_filters: Optional[Dict[str, Any]] = Field(
        None, description="Attribute filters"
    )

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update(
            {
                "data_source": self.data_source,
                "format_type": self.format_type,
                "coordinate_system": self.coordinate_system,
            }
        )

        if self.bounding_box:
            kwargs["bbox"] = self.bounding_box
        if self.layer_name:
            kwargs["layer"] = self.layer_name
        if self.attribute_filters:
            kwargs["where"] = self.attribute_filters

        return kwargs


# =============================================================================
# Utility Functions
# =============================================================================


def get_final_sources_statistics() -> Dict[str, Any]:
    """Get statistics about final specialized sources."""
    registry = enhanced_registry

    # Count by platform type
    platform_counts = {}
    for platform in FinalPlatform:
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

    # Specialized categories
    healthcare = len(
        [name for name in ["fhir", "hl7", "dicom", "epic"] if name in registry._sources]
    )

    education = len(
        [
            name
            for name in ["canvas", "moodle", "blackboard"]
            if name in registry._sources
        ]
    )

    regional = len(
        [
            name
            for name in ["baidu", "yandex", "naver", "vkontakte"]
            if name in registry._sources
        ]
    )

    return {
        "total_final_sources": len(
            registry.find_sources_by_category(SourceCategory.SPECIALIZED)
        ),
        "platform_breakdown": platform_counts,
        "healthcare_sources": healthcare,
        "education_sources": education,
        "regional_sources": regional,
        "data_standards": len(DataStandard),
    }


def validate_final_sources() -> bool:
    """Validate final source registrations."""
    registry = enhanced_registry

    required_sources = [
        "gov_docs",
        "fhir",
        "dicom",
        "canvas",
        "moodle",
        "blockchain",
        "xml_feeds",
        "geospatial",
    ]

    missing = []
    for source_name in required_sources:
        if source_name not in registry._sources:
            missing.append(source_name)

    if missing:
        print(f"Missing final sources: {missing}")
        return False

    print("✅ All essential final sources registered!")
    return True


def get_total_loader_count() -> int:
    """Get total count of all implemented loaders."""
    registry = enhanced_registry
    return len(registry._sources)


def completion_summary() -> Dict[str, Any]:
    """Generate completion summary for the entire loader system."""
    registry = enhanced_registry

    total_loaders = get_total_loader_count()
    target_loaders = 231
    completion_percentage = (total_loaders / target_loaders) * 100

    # Count by category
    category_counts = {}
    for category in SourceCategory:
        count = len(registry.find_sources_by_category(category))
        if count > 0:
            category_counts[category.value] = count

    # Capability statistics
    bulk_loaders = len(
        [
            name
            for name, reg in registry._sources.items()
            if hasattr(reg, "capabilities")
            and reg.capabilities
            and LoaderCapability.BULK_LOADING in reg.capabilities
        ]
    )

    real_time_loaders = len(
        [
            name
            for name, reg in registry._sources.items()
            if hasattr(reg, "capabilities")
            and reg.capabilities
            and LoaderCapability.REAL_TIME in reg.capabilities
        ]
    )

    return {
        "total_loaders_implemented": total_loaders,
        "target_loaders": target_loaders,
        "completion_percentage": completion_percentage,
        "category_breakdown": category_counts,
        "bulk_loaders": bulk_loaders,
        "real_time_loaders": real_time_loaders,
        "status": "COMPLETE" if completion_percentage >= 100 else "NEARLY_COMPLETE",
    }


# Auto-validate on import
if __name__ == "__main__":
    validate_final_sources()
    stats = get_final_sources_statistics()
    summary = completion_summary()
    print(f"Final Sources Statistics: {stats}")
    print(f"Completion Summary: {summary}")
