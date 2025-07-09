"""Tests for business and CRM platform source loaders.

This module tests the business platform loaders including CRM systems,
e-commerce platforms, productivity tools, and enterprise integrations.
"""

from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from unittest.mock import MagicMock, Mock, patch

import pytest

from haive.core.engine.document.loaders.sources.business_sources import (
    BusinessDataType,
    BusinessPlatform,
    BusinessSource,
    HubSpotSource,
    JiraSource,
    NotionSource,
    SalesforceSource,
    ShopifySource,
    SyncMode,
    detect_business_platform,
    get_business_sources_statistics,
    validate_business_sources,
)
from haive.core.engine.document.loaders.sources.source_types import (
    CredentialType,
    LoaderCapability,
    SourceCategory,
)


@pytest.fixture
def mock_registry():
    """Create a mock registry for testing."""
    registry = MagicMock()
    registry._sources = {}
    registry.find_sources_by_category = MagicMock(return_value=[])
    return registry


@pytest.fixture
def business_source_config() -> Dict[str, Any]:
    """Create a basic business source configuration."""
    return {
        "platform": BusinessPlatform.HUBSPOT,
        "source_id": "test-business-001",
        "category": SourceCategory.BUSINESS,
        "data_types": [BusinessDataType.CONTACTS, BusinessDataType.DEALS],
        "sync_mode": SyncMode.INCREMENTAL,
        "max_records": 1000,
        "page_size": 100,
    }


@pytest.fixture
def hubspot_source() -> HubSpotSource:
    """Create a test HubSpot source instance."""
    return HubSpotSource(
        source_id="hubspot-test-001",
        category=SourceCategory.BUSINESS,
        api_key="test-api-key",
        portal_id="123456",
        include_contacts=True,
        include_deals=True,
    )


@pytest.fixture
def salesforce_source() -> SalesforceSource:
    """Create a test Salesforce source instance."""
    return SalesforceSource(
        source_id="salesforce-test-001",
        category=SourceCategory.BUSINESS,
        username="test@example.com",
        password="testpass",
        security_token="testtoken",
        domain="login",
        object_types=["Account", "Contact", "Lead"],
    )


class TestBusinessPlatformDetection:
    """Test suite for business platform detection."""

    def test_detect_hubspot_from_url(self):
        """Test detecting HubSpot from various URL patterns."""
        test_urls = [
            "https://app.hubspot.com/contacts/123456",
            "https://api.hubapi.com/crm/v3/objects",
            "hs-123456",
        ]

        for url in test_urls:
            result = detect_business_platform(url)
            assert result == BusinessPlatform.HUBSPOT

    def test_detect_salesforce_from_url(self):
        """Test detecting Salesforce from various URL patterns."""
        test_urls = [
            "https://mycompany.my.salesforce.com",
            "https://mycompany.force.com",
            "https://mycompany.lightning.force.com",
        ]

        for url in test_urls:
            result = detect_business_platform(url)
            assert result == BusinessPlatform.SALESFORCE

    def test_detect_unknown_platform(self):
        """Test handling of unknown platform URLs."""
        result = detect_business_platform("https://unknown-platform.com")
        assert result is None

    @pytest.mark.parametrize(
        "url,expected",
        [
            ("https://mystore.myshopify.com", BusinessPlatform.SHOPIFY),
            ("https://notion.so/workspace", BusinessPlatform.NOTION),
            ("https://airtable.com/appXXX", BusinessPlatform.AIRTABLE),
            ("https://company.atlassian.net/jira", BusinessPlatform.JIRA),
            ("https://company.atlassian.net/wiki", BusinessPlatform.CONFLUENCE),
        ],
    )
    def test_detect_various_platforms(self, url: str, expected: BusinessPlatform):
        """Test detecting various business platforms."""
        result = detect_business_platform(url)
        assert result == expected


class TestBusinessSource:
    """Test suite for base BusinessSource functionality."""

    def test_business_source_initialization(self, business_source_config):
        """Test creating a business source with valid configuration."""
        source = BusinessSource(**business_source_config)

        assert source.platform == BusinessPlatform.HUBSPOT
        assert source.sync_mode == SyncMode.INCREMENTAL
        assert source.max_records == 1000
        assert len(source.data_types) == 2

    def test_sync_params_full_refresh(self):
        """Test sync parameters for full refresh mode."""
        source = BusinessSource(
            platform=BusinessPlatform.HUBSPOT,
            source_id="test-001",
            category=SourceCategory.BUSINESS,
            sync_mode=SyncMode.FULL_REFRESH,
            page_size=200,
        )

        params = source.get_sync_params()

        assert params["sync_mode"] == "full_refresh"
        assert params["page_size"] == 200
        assert "start_date" not in params

    def test_sync_params_incremental_with_date(self):
        """Test sync parameters for incremental mode with last sync date."""
        last_sync = datetime.now() - timedelta(days=7)
        source = BusinessSource(
            platform=BusinessPlatform.SALESFORCE,
            source_id="test-002",
            category=SourceCategory.BUSINESS,
            sync_mode=SyncMode.INCREMENTAL,
            last_sync_date=last_sync,
        )

        params = source.get_sync_params()

        assert params["sync_mode"] == "incremental"
        assert "start_date" in params
        assert params["start_date"] == last_sync.isoformat()

    def test_loader_kwargs_with_filters(self):
        """Test loader kwargs generation with custom filters."""
        source = BusinessSource(
            platform=BusinessPlatform.NOTION,
            source_id="test-003",
            category=SourceCategory.BUSINESS,
            custom_fields=["name", "email", "company"],
            filter_query="status = 'active'",
            batch_processing=True,
            parallel_streams=5,
        )

        kwargs = source.get_loader_kwargs()

        assert kwargs["platform"] == "notion"
        assert kwargs["fields"] == ["name", "email", "company"]
        assert kwargs["filter"] == "status = 'active'"
        assert kwargs["batch_processing"] is True
        assert kwargs["parallel_streams"] == 5

    @pytest.mark.parametrize(
        "sync_mode,expected",
        [
            (SyncMode.FULL_REFRESH, "full_refresh"),
            (SyncMode.INCREMENTAL, "incremental"),
            (SyncMode.APPEND_ONLY, "append_only"),
            (SyncMode.DEDUPED, "deduped"),
        ],
    )
    def test_sync_mode_values(self, sync_mode: SyncMode, expected: str):
        """Test sync mode enum values."""
        assert sync_mode.value == expected


class TestHubSpotSource:
    """Test suite for HubSpot source functionality."""

    def test_hubspot_source_initialization(self, hubspot_source):
        """Test HubSpot source initialization."""
        assert hubspot_source.platform == BusinessPlatform.HUBSPOT
        assert hubspot_source.api_key == "test-api-key"
        assert hubspot_source.portal_id == "123456"
        assert hubspot_source.include_contacts is True
        assert hubspot_source.include_deals is True

    def test_hubspot_loader_kwargs(self, hubspot_source):
        """Test HubSpot-specific loader kwargs."""
        kwargs = hubspot_source.get_loader_kwargs()

        assert kwargs["api_key"] == "test-api-key"
        assert kwargs["portal_id"] == "123456"
        assert kwargs["include_contacts"] is True
        assert kwargs["include_companies"] is True  # Default
        assert kwargs["include_deals"] is True
        assert kwargs["include_tickets"] is False  # Default

    def test_hubspot_with_custom_properties(self):
        """Test HubSpot with custom property selection."""
        source = HubSpotSource(
            source_id="hubspot-test-002",
            category=SourceCategory.BUSINESS,
            contact_properties=["email", "firstname", "lastname", "custom_score"],
            company_properties=["name", "domain", "industry"],
        )

        kwargs = source.get_loader_kwargs()

        assert "contact_properties" in kwargs
        assert len(kwargs["contact_properties"]) == 4
        assert "company_properties" in kwargs
        assert len(kwargs["company_properties"]) == 3

    @patch(
        "haive.core.engine.document.loaders.sources.business_sources.HubSpotSource.get_api_key"
    )
    def test_hubspot_api_key_fallback(self, mock_get_api_key):
        """Test HubSpot API key fallback to secure config."""
        mock_get_api_key.return_value = "secure-api-key"

        source = HubSpotSource(
            source_id="hubspot-test-003",
            category=SourceCategory.BUSINESS,
            api_key=None,  # No direct API key
        )

        kwargs = source.get_loader_kwargs()

        assert kwargs["api_key"] == "secure-api-key"
        mock_get_api_key.assert_called_once()


class TestSalesforceSource:
    """Test suite for Salesforce source functionality."""

    def test_salesforce_source_initialization(self, salesforce_source):
        """Test Salesforce source initialization."""
        assert salesforce_source.platform == BusinessPlatform.SALESFORCE
        assert salesforce_source.username == "test@example.com"
        assert salesforce_source.password == "testpass"
        assert salesforce_source.security_token == "testtoken"
        assert salesforce_source.domain == "login"

    def test_salesforce_with_soql_query(self):
        """Test Salesforce with custom SOQL query."""
        source = SalesforceSource(
            source_id="sf-test-001",
            category=SourceCategory.BUSINESS,
            username="test@example.com",
            password="testpass",
            security_token="token",
            soql_query="SELECT Id, Name FROM Account WHERE Industry = 'Technology'",
        )

        kwargs = source.get_loader_kwargs()

        assert "soql_query" in kwargs
        assert "SELECT" in kwargs["soql_query"]
        assert "object_types" not in kwargs  # Should not include when SOQL provided

    def test_salesforce_with_object_types(self, salesforce_source):
        """Test Salesforce with object type selection."""
        kwargs = salesforce_source.get_loader_kwargs()

        assert "object_types" in kwargs
        assert len(kwargs["object_types"]) == 3
        assert "Account" in kwargs["object_types"]
        assert "soql_query" not in kwargs


class TestShopifySource:
    """Test suite for Shopify source functionality."""

    def test_shopify_source_initialization(self):
        """Test Shopify source initialization."""
        source = ShopifySource(
            source_id="shopify-test-001",
            category=SourceCategory.BUSINESS,
            shop_domain="mystore.myshopify.com",
            api_key="shop-api-key",
            api_secret="shop-api-secret",
            api_version="2024-01",
        )

        assert source.platform == BusinessPlatform.SHOPIFY
        assert source.shop_domain == "mystore.myshopify.com"
        assert source.api_version == "2024-01"

    def test_shopify_data_selection(self):
        """Test Shopify data type selection."""
        source = ShopifySource(
            source_id="shopify-test-002",
            category=SourceCategory.BUSINESS,
            shop_domain="test.myshopify.com",
            include_products=True,
            include_orders=True,
            include_customers=False,
            include_inventory=True,
        )

        kwargs = source.get_loader_kwargs()

        assert kwargs["include_products"] is True
        assert kwargs["include_orders"] is True
        assert kwargs["include_customers"] is False
        assert kwargs["include_inventory"] is True


class TestNotionSource:
    """Test suite for Notion source functionality."""

    def test_notion_source_initialization(self):
        """Test Notion source initialization."""
        source = NotionSource(
            source_id="notion-test-001",
            category=SourceCategory.BUSINESS,
            integration_token="notion-token",
            database_id="db-123",
            workspace_id="ws-456",
        )

        assert source.platform == BusinessPlatform.NOTION
        assert source.integration_token == "notion-token"
        assert source.database_id == "db-123"
        assert source.workspace_id == "ws-456"

    def test_notion_content_options(self):
        """Test Notion content inclusion options."""
        source = NotionSource(
            source_id="notion-test-002",
            category=SourceCategory.BUSINESS,
            include_pages=True,
            include_databases=True,
            include_comments=True,
        )

        kwargs = source.get_loader_kwargs()

        assert kwargs["include_pages"] is True
        assert kwargs["include_databases"] is True
        assert kwargs["include_comments"] is True


class TestJiraSource:
    """Test suite for Jira source functionality."""

    def test_jira_source_initialization(self):
        """Test Jira source initialization."""
        source = JiraSource(
            source_id="jira-test-001",
            category=SourceCategory.BUSINESS,
            server_url="https://company.atlassian.net",
            username="jira@example.com",
            api_token="jira-token",
        )

        assert source.platform == BusinessPlatform.JIRA
        assert source.server_url == "https://company.atlassian.net"
        assert source.username == "jira@example.com"

    def test_jira_with_jql_query(self):
        """Test Jira with JQL query."""
        source = JiraSource(
            source_id="jira-test-002",
            category=SourceCategory.BUSINESS,
            server_url="https://company.atlassian.net",
            username="test",
            jql_query="project = PROJ AND status = Open",
            include_attachments=True,
            include_history=True,
        )

        kwargs = source.get_loader_kwargs()

        assert kwargs["jql"] == "project = PROJ AND status = Open"
        assert kwargs["include_attachments"] is True
        assert kwargs["include_history"] is True

    def test_jira_with_project_key(self):
        """Test Jira with project key instead of JQL."""
        source = JiraSource(
            source_id="jira-test-003",
            category=SourceCategory.BUSINESS,
            server_url="https://company.atlassian.net",
            username="test",
            project_key="PROJ",
        )

        kwargs = source.get_loader_kwargs()

        assert kwargs["jql"] == "project = PROJ"


class TestBusinessDataTypes:
    """Test suite for business data type enumerations."""

    @pytest.mark.parametrize(
        "data_type,expected",
        [
            (BusinessDataType.CONTACTS, "contacts"),
            (BusinessDataType.LEADS, "leads"),
            (BusinessDataType.OPPORTUNITIES, "opportunities"),
            (BusinessDataType.PRODUCTS, "products"),
            (BusinessDataType.ORDERS, "orders"),
            (BusinessDataType.TASKS, "tasks"),
            (BusinessDataType.PAGES, "pages"),
            (BusinessDataType.REPORTS, "reports"),
        ],
    )
    def test_business_data_type_values(
        self, data_type: BusinessDataType, expected: str
    ):
        """Test business data type enum values."""
        assert data_type.value == expected

    def test_data_type_categorization(self):
        """Test data type categories are properly defined."""
        crm_types = [
            BusinessDataType.CONTACTS,
            BusinessDataType.LEADS,
            BusinessDataType.OPPORTUNITIES,
            BusinessDataType.DEALS,
        ]
        ecommerce_types = [
            BusinessDataType.PRODUCTS,
            BusinessDataType.ORDERS,
            BusinessDataType.CUSTOMERS,
            BusinessDataType.INVENTORY,
        ]

        # Ensure no overlap between categories
        overlap = set(crm_types) & set(ecommerce_types)
        assert len(overlap) == 0


class TestBusinessUtilityFunctions:
    """Test suite for business source utility functions."""

    @patch(
        "haive.core.engine.document.loaders.sources.business_sources.enhanced_registry"
    )
    def test_get_business_sources_statistics(self, mock_registry):
        """Test business sources statistics calculation."""
        # Mock registry responses
        mock_registry.find_sources_by_category.return_value = ["hubspot", "salesforce"]
        mock_registry._sources = {
            "hubspot": MagicMock(
                requires_credentials=True, credential_type=CredentialType.API_KEY
            ),
            "salesforce": MagicMock(
                requires_credentials=True, credential_type=CredentialType.OAUTH
            ),
        }

        stats = get_business_sources_statistics()

        assert "total_business_sources" in stats
        assert "platform_breakdown" in stats
        assert "oauth_authenticated_sources" in stats

    @patch(
        "haive.core.engine.document.loaders.sources.business_sources.enhanced_registry"
    )
    def test_validate_business_sources_success(self, mock_registry):
        """Test successful validation of business sources."""
        # Mock all required sources as present
        mock_registry._sources = {
            "hubspot": MagicMock(),
            "salesforce": MagicMock(),
            "shopify": MagicMock(),
            "notion": MagicMock(),
            "airtable": MagicMock(),
            "jira": MagicMock(),
            "confluence": MagicMock(),
            "airbyte": MagicMock(),
        }

        result = validate_business_sources()
        assert result is True

    @patch(
        "haive.core.engine.document.loaders.sources.business_sources.enhanced_registry"
    )
    def test_validate_business_sources_missing(self, mock_registry):
        """Test validation failure when sources are missing."""
        # Mock only some sources as present
        mock_registry._sources = {"hubspot": MagicMock(), "salesforce": MagicMock()}

        result = validate_business_sources()
        assert result is False


@pytest.mark.integration
class TestBusinessSourceIntegration:
    """Integration tests for business sources with mock loaders."""

    @patch("langchain_community.document_loaders.HubSpotLoader")
    async def test_hubspot_loader_integration(self, mock_loader_class, hubspot_source):
        """Test HubSpot source integration with mock loader."""
        # Mock the loader instance
        mock_loader = MagicMock()
        mock_loader.load.return_value = [
            {"content": "Contact 1", "metadata": {"type": "contact"}},
            {"content": "Deal 1", "metadata": {"type": "deal"}},
        ]
        mock_loader_class.return_value = mock_loader

        # Get loader kwargs
        kwargs = hubspot_source.get_loader_kwargs()

        # Simulate loader creation
        loader = mock_loader_class(**kwargs)
        documents = loader.load()

        assert len(documents) == 2
        assert documents[0]["metadata"]["type"] == "contact"
        mock_loader_class.assert_called_once()

    @pytest.mark.parametrize(
        "platform,loader_class",
        [
            (BusinessPlatform.HUBSPOT, "HubSpotLoader"),
            (BusinessPlatform.SALESFORCE, "SalesforceLoader"),
            (BusinessPlatform.SHOPIFY, "ShopifyLoader"),
            (BusinessPlatform.NOTION, "NotionDBLoader"),
            (BusinessPlatform.JIRA, "JiraLoader"),
        ],
    )
    def test_platform_loader_mapping(
        self, platform: BusinessPlatform, loader_class: str
    ):
        """Test that each platform maps to the correct loader class."""
        # This test verifies the loader class names match expected conventions
        assert (
            loader_class.lower().startswith(platform.value)
            or platform.value in loader_class.lower()
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
