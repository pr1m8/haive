"""Business and CRM platform source registrations.

This module implements comprehensive business platform loaders from langchain_community
including CRM systems (HubSpot, Salesforce), e-commerce (Shopify), productivity tools
(Notion, Airtable), enterprise platforms (Jira, Confluence), and data integration tools.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import Field

from .enhanced_registry import enhanced_registry, register_source
from .source_types import CredentialType, LoaderCapability, RemoteSource, SourceCategory


class BusinessPlatform(str, Enum):
    """Business and CRM platforms."""

    # CRM Systems
    HUBSPOT = "hubspot"
    SALESFORCE = "salesforce"
    PIPEDRIVE = "pipedrive"
    ZOHO_CRM = "zoho_crm"

    # E-commerce
    SHOPIFY = "shopify"
    WOOCOMMERCE = "woocommerce"
    MAGENTO = "magento"

    # Productivity Tools
    NOTION = "notion"
    AIRTABLE = "airtable"
    MONDAY = "monday"
    ASANA = "asana"
    TRELLO = "trello"

    # Enterprise Platforms
    JIRA = "jira"
    CONFLUENCE = "confluence"
    SERVICENOW = "servicenow"

    # Data Integration
    AIRBYTE = "airbyte"
    ZAPIER = "zapier"

    # Analytics
    GOOGLE_ANALYTICS = "google_analytics"
    MIXPANEL = "mixpanel"


class BusinessDataType(str, Enum):
    """Types of business data to extract."""

    # CRM Data
    CONTACTS = "contacts"
    LEADS = "leads"
    OPPORTUNITIES = "opportunities"
    ACCOUNTS = "accounts"
    DEALS = "deals"

    # E-commerce Data
    PRODUCTS = "products"
    ORDERS = "orders"
    CUSTOMERS = "customers"
    INVENTORY = "inventory"

    # Project Management
    TASKS = "tasks"
    PROJECTS = "projects"
    ISSUES = "issues"
    TICKETS = "tickets"

    # Content
    PAGES = "pages"
    DOCUMENTS = "documents"
    KNOWLEDGE_BASE = "knowledge_base"

    # Analytics
    REPORTS = "reports"
    METRICS = "metrics"
    EVENTS = "events"


class SyncMode(str, Enum):
    """Data synchronization modes."""

    FULL_REFRESH = "full_refresh"
    INCREMENTAL = "incremental"
    APPEND_ONLY = "append_only"
    DEDUPED = "deduped"


# =============================================================================
# Base Business Source
# =============================================================================


class BusinessSource(RemoteSource):
    """Base class for business and CRM platform sources."""

    platform: BusinessPlatform = Field(..., description="Business platform type")

    # Data selection
    data_types: List[BusinessDataType] = Field(
        default=[BusinessDataType.CONTACTS], description="Types of data to extract"
    )

    # Sync configuration
    sync_mode: SyncMode = Field(SyncMode.FULL_REFRESH, description="Data sync mode")
    last_sync_date: Optional[datetime] = Field(None, description="Last sync timestamp")

    # Data limits
    max_records: Optional[int] = Field(
        None, ge=1, description="Maximum records to retrieve"
    )
    page_size: int = Field(100, ge=1, le=1000, description="Page size for API requests")

    # Filtering
    custom_fields: Optional[List[str]] = Field(
        None, description="Specific fields to include"
    )
    filter_query: Optional[str] = Field(
        None, description="Platform-specific filter query"
    )

    # Performance
    batch_processing: bool = Field(True, description="Enable batch processing")
    parallel_streams: int = Field(
        3, ge=1, le=10, description="Number of parallel data streams"
    )

    def get_sync_params(self) -> Dict[str, Any]:
        """Get synchronization parameters."""
        params = {"sync_mode": self.sync_mode.value, "page_size": self.page_size}

        if self.sync_mode == SyncMode.INCREMENTAL and self.last_sync_date:
            params["start_date"] = self.last_sync_date.isoformat()

        if self.max_records:
            params["max_records"] = self.max_records

        return params

    def get_loader_kwargs(self) -> Dict[str, Any]:
        """Get loader arguments for business sources."""
        kwargs = super().get_loader_kwargs()

        # Add business-specific configuration
        kwargs.update(
            {
                "platform": self.platform.value,
                "data_types": [dt.value for dt in self.data_types],
                "batch_processing": self.batch_processing,
                "parallel_streams": self.parallel_streams,
            }
        )

        # Add sync parameters
        kwargs.update(self.get_sync_params())

        # Add filtering
        if self.custom_fields:
            kwargs["fields"] = self.custom_fields
        if self.filter_query:
            kwargs["filter"] = self.filter_query

        return kwargs


# =============================================================================
# CRM Platform Sources
# =============================================================================


@register_source(
    name="hubspot",
    category=SourceCategory.BUSINESS,
    loaders={
        "hubspot": {
            "class": "HubSpotLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["hubspot-api-client"],
        }
    },
    default_loader="hubspot",
    description="HubSpot CRM data loader with contacts, deals, and companies",
    requires_credentials=True,
    credential_type=CredentialType.API_KEY,
    capabilities=[
        LoaderCapability.BULK_LOADING,
        LoaderCapability.FILTERING,
        LoaderCapability.RATE_LIMITED,
    ],
    priority=9,
)
class HubSpotSource(BusinessSource):
    """HubSpot CRM data source."""

    platform: BusinessPlatform = BusinessPlatform.HUBSPOT

    # HubSpot-specific options
    api_key: Optional[str] = Field(None, description="HubSpot API key")
    portal_id: Optional[str] = Field(None, description="HubSpot portal ID")

    # Object types
    include_contacts: bool = Field(True, description="Include contacts")
    include_companies: bool = Field(True, description="Include companies")
    include_deals: bool = Field(True, description="Include deals")
    include_tickets: bool = Field(False, description="Include support tickets")

    # Properties
    contact_properties: Optional[List[str]] = Field(
        None, description="Specific contact properties"
    )
    company_properties: Optional[List[str]] = Field(
        None, description="Specific company properties"
    )

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update(
            {
                "api_key": (
                    self.api_key or self.get_api_key()
                    if hasattr(self, "get_api_key")
                    else None
                ),
                "portal_id": self.portal_id,
                "include_contacts": self.include_contacts,
                "include_companies": self.include_companies,
                "include_deals": self.include_deals,
                "include_tickets": self.include_tickets,
            }
        )

        if self.contact_properties:
            kwargs["contact_properties"] = self.contact_properties
        if self.company_properties:
            kwargs["company_properties"] = self.company_properties

        return kwargs


@register_source(
    name="salesforce",
    category=SourceCategory.BUSINESS,
    loaders={
        "salesforce": {
            "class": "SalesforceLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["simple-salesforce"],
        }
    },
    default_loader="salesforce",
    description="Salesforce CRM loader with SOQL query support",
    requires_credentials=True,
    credential_type=CredentialType.OAUTH,
    capabilities=[
        LoaderCapability.BULK_LOADING,
        LoaderCapability.FILTERING,
        LoaderCapability.RATE_LIMITED,
    ],
    priority=10,
)
class SalesforceSource(BusinessSource):
    """Salesforce CRM data source."""

    platform: BusinessPlatform = BusinessPlatform.SALESFORCE

    # Salesforce authentication
    username: Optional[str] = Field(None, description="Salesforce username")
    password: Optional[str] = Field(None, description="Salesforce password")
    security_token: Optional[str] = Field(None, description="Salesforce security token")
    domain: str = Field("login", description="Salesforce domain (login/test)")

    # Query options
    soql_query: Optional[str] = Field(None, description="SOQL query string")
    object_types: List[str] = Field(
        default=["Account", "Contact", "Lead", "Opportunity"],
        description="Salesforce object types to query",
    )

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update(
            {
                "username": self.username,
                "password": self.password,
                "security_token": self.security_token,
                "domain": self.domain,
            }
        )

        if self.soql_query:
            kwargs["soql_query"] = self.soql_query
        else:
            kwargs["object_types"] = self.object_types

        return kwargs


@register_source(
    name="pipedrive",
    category=SourceCategory.BUSINESS,
    loaders={
        "pipedrive": {
            "class": "PipedriveLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["pipedrive-python"],
        }
    },
    default_loader="pipedrive",
    description="Pipedrive CRM loader for deals, contacts, and activities",
    requires_credentials=True,
    credential_type=CredentialType.API_KEY,
    capabilities=[
        LoaderCapability.BULK_LOADING,
        LoaderCapability.FILTERING,
        LoaderCapability.RATE_LIMITED,
    ],
    priority=8,
)
class PipedriveSource(BusinessSource):
    """Pipedrive CRM data source."""

    platform: BusinessPlatform = BusinessPlatform.PIPEDRIVE

    # Pipedrive configuration
    api_token: Optional[str] = Field(None, description="Pipedrive API token")
    company_domain: str = Field(..., description="Pipedrive company domain")

    # Data selection
    include_persons: bool = Field(True, description="Include persons")
    include_organizations: bool = Field(True, description="Include organizations")
    include_deals: bool = Field(True, description="Include deals")
    include_activities: bool = Field(False, description="Include activities")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update(
            {
                "api_token": (
                    self.api_token or self.get_api_key()
                    if hasattr(self, "get_api_key")
                    else None
                ),
                "company_domain": self.company_domain,
                "include_persons": self.include_persons,
                "include_organizations": self.include_organizations,
                "include_deals": self.include_deals,
                "include_activities": self.include_activities,
            }
        )

        return kwargs


# =============================================================================
# E-commerce Platform Sources
# =============================================================================


@register_source(
    name="shopify",
    category=SourceCategory.BUSINESS,
    loaders={
        "shopify": {
            "class": "ShopifyLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["shopifyapi"],
        }
    },
    default_loader="shopify",
    description="Shopify e-commerce data loader for products, orders, and customers",
    requires_credentials=True,
    credential_type=CredentialType.API_KEY,
    capabilities=[
        LoaderCapability.BULK_LOADING,
        LoaderCapability.FILTERING,
        LoaderCapability.RATE_LIMITED,
    ],
    priority=9,
)
class ShopifySource(BusinessSource):
    """Shopify e-commerce data source."""

    platform: BusinessPlatform = BusinessPlatform.SHOPIFY

    # Shopify configuration
    shop_domain: str = Field(..., description="Shopify shop domain")
    api_key: Optional[str] = Field(None, description="Shopify API key")
    api_secret: Optional[str] = Field(None, description="Shopify API secret")
    api_version: str = Field("2024-01", description="Shopify API version")

    # Data selection
    include_products: bool = Field(True, description="Include products")
    include_orders: bool = Field(True, description="Include orders")
    include_customers: bool = Field(True, description="Include customers")
    include_inventory: bool = Field(False, description="Include inventory")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update(
            {
                "shop_domain": self.shop_domain,
                "api_key": (
                    self.api_key or self.get_api_key()
                    if hasattr(self, "get_api_key")
                    else None
                ),
                "api_secret": self.api_secret,
                "api_version": self.api_version,
                "include_products": self.include_products,
                "include_orders": self.include_orders,
                "include_customers": self.include_customers,
                "include_inventory": self.include_inventory,
            }
        )

        return kwargs


# =============================================================================
# Productivity Tool Sources
# =============================================================================


@register_source(
    name="notion",
    category=SourceCategory.BUSINESS,
    loaders={
        "notion": {
            "class": "NotionDBLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["notion-client"],
        }
    },
    default_loader="notion",
    description="Notion workspace and database loader",
    requires_credentials=True,
    credential_type=CredentialType.API_KEY,
    capabilities=[
        LoaderCapability.BULK_LOADING,
        LoaderCapability.FILTERING,
        LoaderCapability.RECURSIVE,
    ],
    priority=9,
)
class NotionSource(BusinessSource):
    """Notion workspace data source."""

    platform: BusinessPlatform = BusinessPlatform.NOTION

    # Notion configuration
    integration_token: Optional[str] = Field(
        None, description="Notion integration token"
    )
    database_id: Optional[str] = Field(None, description="Specific database ID")
    workspace_id: Optional[str] = Field(None, description="Workspace ID")

    # Content options
    include_pages: bool = Field(True, description="Include pages")
    include_databases: bool = Field(True, description="Include databases")
    include_comments: bool = Field(False, description="Include comments")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update(
            {
                "integration_token": (
                    self.integration_token or self.get_api_key()
                    if hasattr(self, "get_api_key")
                    else None
                ),
                "database_id": self.database_id,
                "workspace_id": self.workspace_id,
                "include_pages": self.include_pages,
                "include_databases": self.include_databases,
                "include_comments": self.include_comments,
            }
        )

        return kwargs


@register_source(
    name="airtable",
    category=SourceCategory.BUSINESS,
    loaders={
        "airtable": {
            "class": "AirtableLoader",
            "speed": "fast",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["pyairtable"],
        }
    },
    default_loader="airtable",
    description="Airtable base and table data loader",
    requires_credentials=True,
    credential_type=CredentialType.API_KEY,
    capabilities=[LoaderCapability.BULK_LOADING, LoaderCapability.FILTERING],
    priority=8,
)
class AirtableSource(BusinessSource):
    """Airtable data source."""

    platform: BusinessPlatform = BusinessPlatform.AIRTABLE

    # Airtable configuration
    api_key: Optional[str] = Field(None, description="Airtable API key")
    base_id: str = Field(..., description="Airtable base ID")
    table_name: str = Field(..., description="Table name")

    # Query options
    view: Optional[str] = Field(None, description="Specific view to use")
    formula: Optional[str] = Field(None, description="Airtable formula filter")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update(
            {
                "api_key": (
                    self.api_key or self.get_api_key()
                    if hasattr(self, "get_api_key")
                    else None
                ),
                "base_id": self.base_id,
                "table_name": self.table_name,
            }
        )

        if self.view:
            kwargs["view"] = self.view
        if self.formula:
            kwargs["formula"] = self.formula

        return kwargs


@register_source(
    name="trello",
    category=SourceCategory.BUSINESS,
    loaders={
        "trello": {
            "class": "TrelloLoader",
            "speed": "fast",
            "quality": "medium",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["py-trello"],
        }
    },
    default_loader="trello",
    description="Trello board and card loader",
    requires_credentials=True,
    credential_type=CredentialType.API_KEY,
    capabilities=[LoaderCapability.BULK_LOADING, LoaderCapability.FILTERING],
    priority=7,
)
class TrelloSource(BusinessSource):
    """Trello board data source."""

    platform: BusinessPlatform = BusinessPlatform.TRELLO

    # Trello configuration
    api_key: Optional[str] = Field(None, description="Trello API key")
    api_token: Optional[str] = Field(None, description="Trello API token")
    board_id: str = Field(..., description="Trello board ID")

    # Content options
    include_cards: bool = Field(True, description="Include cards")
    include_checklists: bool = Field(True, description="Include checklists")
    include_comments: bool = Field(False, description="Include comments")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update(
            {
                "api_key": (
                    self.api_key or self.get_api_key()
                    if hasattr(self, "get_api_key")
                    else None
                ),
                "api_token": self.api_token,
                "board_id": self.board_id,
                "include_cards": self.include_cards,
                "include_checklists": self.include_checklists,
                "include_comments": self.include_comments,
            }
        )

        return kwargs


# =============================================================================
# Enterprise Platform Sources
# =============================================================================


@register_source(
    name="jira",
    category=SourceCategory.BUSINESS,
    loaders={
        "jira": {
            "class": "JiraLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["jira"],
        }
    },
    default_loader="jira",
    description="Jira issue and project data loader",
    requires_credentials=True,
    credential_type=CredentialType.API_KEY,
    capabilities=[
        LoaderCapability.BULK_LOADING,
        LoaderCapability.FILTERING,
        LoaderCapability.RATE_LIMITED,
    ],
    priority=9,
)
class JiraSource(BusinessSource):
    """Jira issue tracking data source."""

    platform: BusinessPlatform = BusinessPlatform.JIRA

    # Jira configuration
    server_url: str = Field(..., description="Jira server URL")
    username: Optional[str] = Field(None, description="Jira username")
    api_token: Optional[str] = Field(None, description="Jira API token")

    # Query options
    jql_query: Optional[str] = Field(None, description="JQL query string")
    project_key: Optional[str] = Field(None, description="Specific project key")

    # Content options
    include_attachments: bool = Field(False, description="Include attachments")
    include_comments: bool = Field(True, description="Include comments")
    include_history: bool = Field(False, description="Include issue history")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update(
            {
                "server": self.server_url,
                "username": self.username,
                "api_token": (
                    self.api_token or self.get_api_key()
                    if hasattr(self, "get_api_key")
                    else None
                ),
            }
        )

        if self.jql_query:
            kwargs["jql"] = self.jql_query
        elif self.project_key:
            kwargs["jql"] = f"project = {self.project_key}"

        kwargs.update(
            {
                "include_attachments": self.include_attachments,
                "include_comments": self.include_comments,
                "include_history": self.include_history,
            }
        )

        return kwargs


@register_source(
    name="confluence",
    category=SourceCategory.BUSINESS,
    loaders={
        "confluence": {
            "class": "ConfluenceLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["atlassian-python-api"],
        }
    },
    default_loader="confluence",
    description="Confluence space and page content loader",
    requires_credentials=True,
    credential_type=CredentialType.API_KEY,
    capabilities=[
        LoaderCapability.BULK_LOADING,
        LoaderCapability.FILTERING,
        LoaderCapability.RECURSIVE,
    ],
    priority=9,
)
class ConfluenceSource(BusinessSource):
    """Confluence knowledge base source."""

    platform: BusinessPlatform = BusinessPlatform.CONFLUENCE

    # Confluence configuration
    server_url: str = Field(..., description="Confluence server URL")
    username: Optional[str] = Field(None, description="Confluence username")
    api_token: Optional[str] = Field(None, description="Confluence API token")

    # Content selection
    space_key: Optional[str] = Field(None, description="Specific space key")
    page_ids: Optional[List[str]] = Field(None, description="Specific page IDs")

    # Options
    include_attachments: bool = Field(False, description="Include attachments")
    include_comments: bool = Field(False, description="Include comments")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update(
            {
                "url": self.server_url,
                "username": self.username,
                "api_key": (
                    self.api_token or self.get_api_key()
                    if hasattr(self, "get_api_key")
                    else None
                ),
            }
        )

        if self.space_key:
            kwargs["space_key"] = self.space_key
        if self.page_ids:
            kwargs["page_ids"] = self.page_ids

        kwargs.update(
            {
                "include_attachments": self.include_attachments,
                "include_comments": self.include_comments,
            }
        )

        return kwargs


# =============================================================================
# Data Integration Sources
# =============================================================================


@register_source(
    name="airbyte",
    category=SourceCategory.BUSINESS,
    loaders={
        "airbyte": {
            "class": "AirbyteLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["airbyte-cdk"],
        }
    },
    default_loader="airbyte",
    description="Airbyte connector for 300+ data sources",
    requires_credentials=True,
    credential_type=CredentialType.API_KEY,
    capabilities=[
        LoaderCapability.BULK_LOADING,
        LoaderCapability.FILTERING,
        LoaderCapability.RATE_LIMITED,
    ],
    priority=10,
)
class AirbyteSource(BusinessSource):
    """Airbyte data integration source."""

    platform: BusinessPlatform = BusinessPlatform.AIRBYTE

    # Airbyte configuration
    connection_id: str = Field(..., description="Airbyte connection ID")
    api_key: Optional[str] = Field(None, description="Airbyte API key")
    api_url: str = Field("http://localhost:8000", description="Airbyte API URL")

    # Sync options
    stream_name: Optional[str] = Field(None, description="Specific stream to sync")
    namespace: Optional[str] = Field(None, description="Stream namespace")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update(
            {
                "connection_id": self.connection_id,
                "api_key": (
                    self.api_key or self.get_api_key()
                    if hasattr(self, "get_api_key")
                    else None
                ),
                "api_url": self.api_url,
            }
        )

        if self.stream_name:
            kwargs["stream_name"] = self.stream_name
        if self.namespace:
            kwargs["namespace"] = self.namespace

        return kwargs


# =============================================================================
# Analytics Platform Sources
# =============================================================================


@register_source(
    name="google_analytics",
    category=SourceCategory.BUSINESS,
    loaders={
        "ga": {
            "class": "GoogleAnalyticsLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["google-analytics-data"],
        }
    },
    default_loader="ga",
    description="Google Analytics data loader for metrics and reports",
    requires_credentials=True,
    credential_type=CredentialType.OAUTH,
    capabilities=[
        LoaderCapability.BULK_LOADING,
        LoaderCapability.FILTERING,
        LoaderCapability.RATE_LIMITED,
    ],
    priority=8,
)
class GoogleAnalyticsSource(BusinessSource):
    """Google Analytics data source."""

    platform: BusinessPlatform = BusinessPlatform.GOOGLE_ANALYTICS

    # GA configuration
    property_id: str = Field(..., description="Google Analytics property ID")
    credentials_path: Optional[str] = Field(
        None, description="Path to credentials JSON"
    )

    # Report options
    dimensions: List[str] = Field(
        default=["date", "country"], description="Report dimensions"
    )
    metrics: List[str] = Field(
        default=["sessions", "users"], description="Report metrics"
    )
    date_ranges: List[Dict[str, str]] = Field(
        default=[{"start_date": "7daysAgo", "end_date": "today"}],
        description="Date ranges for reports",
    )

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update(
            {
                "property_id": self.property_id,
                "credentials_path": self.credentials_path,
                "dimensions": self.dimensions,
                "metrics": self.metrics,
                "date_ranges": self.date_ranges,
            }
        )

        return kwargs


# =============================================================================
# Utility Functions
# =============================================================================


def get_business_sources_statistics() -> Dict[str, Any]:
    """Get statistics about business sources."""
    registry = enhanced_registry

    # Find business sources by category
    business_sources = len(registry.find_sources_by_category(SourceCategory.BUSINESS))

    # Find platform-specific counts
    platform_counts = {}
    for platform in BusinessPlatform:
        platform_sources = [
            name
            for name, registration in registry._sources.items()
            if hasattr(registration, "platform") and registration.platform == platform
        ]
        if platform_sources:
            platform_counts[platform.value] = len(platform_sources)

    # Find capability-based statistics
    oauth_sources = len(
        [
            name
            for name, registration in registry._sources.items()
            if registration.requires_credentials
            and registration.credential_type == CredentialType.OAUTH
        ]
    )

    bulk_business = len(
        [
            name
            for name in registry._sources.keys()
            if any(keyword in name for keyword in ["airbyte", "salesforce", "hubspot"])
        ]
    )

    return {
        "total_business_sources": business_sources,
        "platform_breakdown": platform_counts,
        "oauth_authenticated_sources": oauth_sources,
        "bulk_sync_sources": bulk_business,
        "supported_platforms": len(BusinessPlatform),
        "data_types": len(BusinessDataType),
        "sync_modes": len(SyncMode),
    }


def validate_business_sources() -> bool:
    """Validate business source registrations."""
    registry = enhanced_registry

    required_business_sources = [
        "hubspot",
        "salesforce",
        "shopify",
        "notion",
        "airtable",
        "jira",
        "confluence",
        "airbyte",
    ]

    missing = []
    for source_name in required_business_sources:
        if source_name not in registry._sources:
            missing.append(source_name)

    if missing:
        print(f"Missing business sources: {missing}")
        return False

    print(
        f"✅ All {len(required_business_sources)} essential business sources registered!"
    )
    return True


def detect_business_platform(url_or_id: str) -> Optional[BusinessPlatform]:
    """Auto-detect business platform from URL or identifier."""
    url_lower = url_or_id.lower()

    # Platform detection patterns
    patterns = {
        BusinessPlatform.HUBSPOT: ["hubspot", "hs-", "hubapi"],
        BusinessPlatform.SALESFORCE: ["salesforce", "force.com", "lightning"],
        BusinessPlatform.SHOPIFY: ["shopify", "myshopify.com"],
        BusinessPlatform.NOTION: ["notion.so", "notion.site"],
        BusinessPlatform.AIRTABLE: ["airtable.com", "airtbl"],
        BusinessPlatform.JIRA: ["jira", "atlassian.net/jira"],
        BusinessPlatform.CONFLUENCE: ["confluence", "atlassian.net/wiki"],
    }

    for platform, keywords in patterns.items():
        if any(keyword in url_lower for keyword in keywords):
            return platform

    return None


# Auto-validate on import
if __name__ == "__main__":
    validate_business_sources()
    stats = get_business_sources_statistics()
    print(f"Business Sources Statistics: {stats}")
