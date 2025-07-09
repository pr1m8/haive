"""Messaging and social media source registrations.

This module implements comprehensive messaging and social media loaders from
langchain_community including Discord, Slack, Twitter, Reddit, WhatsApp,
Telegram, email systems, and other communication platforms.
"""

from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import Field, validator

from .enhanced_registry import (
    enhanced_registry,
    register_bulk_source,
    register_source,
)
from .source_types import (
    CredentialType,
    LoaderCapability,
    RemoteSource,
    SourceCategory,
)


class MessagingPlatform(str, Enum):
    """Messaging and social media platforms."""

    # Team Communication
    DISCORD = "discord"
    SLACK = "slack"
    MICROSOFT_TEAMS = "teams"
    MATTERMOST = "mattermost"

    # Social Media
    TWITTER = "twitter"
    REDDIT = "reddit"
    FACEBOOK = "facebook"
    LINKEDIN = "linkedin"
    MASTODON = "mastodon"

    # Messaging Apps
    WHATSAPP = "whatsapp"
    TELEGRAM = "telegram"
    SIGNAL = "signal"

    # Email and Forums
    EMAIL = "email"
    IMAP = "imap"
    GMAIL = "gmail"
    OUTLOOK = "outlook"


class ContentType(str, Enum):
    """Types of content to extract from messaging platforms."""

    MESSAGES = "messages"
    THREADS = "threads"
    CHANNELS = "channels"
    POSTS = "posts"
    COMMENTS = "comments"
    REACTIONS = "reactions"
    ATTACHMENTS = "attachments"
    METADATA = "metadata"


class DateRange(str, Enum):
    """Predefined date ranges for content filtering."""

    LAST_DAY = "last_day"
    LAST_WEEK = "last_week"
    LAST_MONTH = "last_month"
    LAST_YEAR = "last_year"
    ALL_TIME = "all_time"
    CUSTOM = "custom"


# =============================================================================
# Base Messaging Source
# =============================================================================


class MessagingSource(RemoteSource):
    """Base class for messaging and social media sources."""

    platform: MessagingPlatform = Field(..., description="Messaging platform type")

    # Content filtering
    content_types: List[ContentType] = Field(
        default=[ContentType.MESSAGES], description="Types of content to extract"
    )

    # Date filtering
    date_range: DateRange = Field(
        DateRange.LAST_MONTH, description="Date range for content"
    )
    start_date: Optional[datetime] = Field(None, description="Custom start date")
    end_date: Optional[datetime] = Field(None, description="Custom end date")

    # Content limits
    max_messages: Optional[int] = Field(
        None, ge=1, description="Maximum messages to retrieve"
    )
    max_channels: Optional[int] = Field(
        None, ge=1, description="Maximum channels to process"
    )

    # Processing options
    include_attachments: bool = Field(False, description="Include file attachments")
    include_reactions: bool = Field(False, description="Include reactions/emojis")
    include_metadata: bool = Field(True, description="Include message metadata")

    # Filtering
    user_filter: Optional[List[str]] = Field(
        None, description="Filter by specific users"
    )
    keyword_filter: Optional[List[str]] = Field(None, description="Filter by keywords")
    exclude_bots: bool = Field(True, description="Exclude bot messages")

    @validator("start_date", "end_date")
    def validate_dates(cls, v, values):
        """Validate date ranges."""
        if v and "date_range" in values and values["date_range"] != DateRange.CUSTOM:
            raise ValueError("Custom dates only allowed when date_range is 'custom'")
        return v

    def get_date_filter(self) -> Dict[str, Any]:
        """Get date filtering configuration."""
        if self.date_range == DateRange.CUSTOM:
            return {"start_date": self.start_date, "end_date": self.end_date}

        # Calculate predefined ranges
        now = datetime.now()
        ranges = {
            DateRange.LAST_DAY: timedelta(days=1),
            DateRange.LAST_WEEK: timedelta(weeks=1),
            DateRange.LAST_MONTH: timedelta(days=30),
            DateRange.LAST_YEAR: timedelta(days=365),
        }

        if self.date_range in ranges:
            return {"start_date": now - ranges[self.date_range], "end_date": now}

        return {}  # All time

    def get_loader_kwargs(self) -> Dict[str, Any]:
        """Get loader arguments for messaging sources."""
        kwargs = super().get_loader_kwargs()

        # Add messaging-specific configuration
        kwargs.update(
            {
                "platform": self.platform.value,
                "content_types": [ct.value for ct in self.content_types],
                "include_attachments": self.include_attachments,
                "include_reactions": self.include_reactions,
                "include_metadata": self.include_metadata,
                "exclude_bots": self.exclude_bots,
            }
        )

        # Add date filtering
        date_filter = self.get_date_filter()
        if date_filter:
            kwargs.update(date_filter)

        # Add limits
        if self.max_messages:
            kwargs["max_messages"] = self.max_messages
        if self.max_channels:
            kwargs["max_channels"] = self.max_channels

        # Add filters
        if self.user_filter:
            kwargs["user_filter"] = self.user_filter
        if self.keyword_filter:
            kwargs["keyword_filter"] = self.keyword_filter

        return kwargs


# =============================================================================
# Team Communication Sources
# =============================================================================


@register_source(
    name="discord",
    category=SourceCategory.MESSAGING,
    loaders={
        "discord": {
            "class": "DiscordChatLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["discord.py"],
        }
    },
    default_loader="discord",
    description="Discord chat and server content loader",
    requires_credentials=True,
    credential_type=CredentialType.API_KEY,
    capabilities=[
        LoaderCapability.BULK_LOADING,
        LoaderCapability.FILTERING,
        LoaderCapability.RATE_LIMITED,
    ],
    priority=9,
)
class DiscordSource(MessagingSource):
    """Discord chat and server content source."""

    platform: MessagingPlatform = MessagingPlatform.DISCORD

    # Discord-specific options
    server_id: Optional[str] = Field(None, description="Discord server/guild ID")
    channel_ids: Optional[List[str]] = Field(None, description="Specific channel IDs")

    # Authentication
    bot_token: Optional[str] = Field(None, description="Discord bot token")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update(
            {
                "discord_token": (
                    self.bot_token or self.get_api_key()
                    if hasattr(self, "get_api_key")
                    else None
                ),
                "guild_id": self.server_id,
                "channel_ids": self.channel_ids,
            }
        )

        return kwargs


@register_source(
    name="slack",
    category=SourceCategory.MESSAGING,
    loaders={
        "slack": {
            "class": "SlackDirectoryLoader",
            "speed": "fast",
            "quality": "high",
            "module": "langchain_community.document_loaders",
        },
        "slack_api": {
            "class": "SlackChatLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["slack_sdk"],
        },
    },
    default_loader="slack",
    description="Slack workspace and channel content loader",
    requires_credentials=True,
    credential_type=CredentialType.API_KEY,
    capabilities=[
        LoaderCapability.BULK_LOADING,
        LoaderCapability.FILTERING,
        LoaderCapability.RATE_LIMITED,
    ],
    priority=9,
)
class SlackSource(MessagingSource):
    """Slack workspace and channel content source."""

    platform: MessagingPlatform = MessagingPlatform.SLACK

    # Slack-specific options
    workspace_url: Optional[str] = Field(None, description="Slack workspace URL")
    slack_token: Optional[str] = Field(None, description="Slack API token")

    # Content options
    zip_path: Optional[str] = Field(None, description="Path to Slack export ZIP file")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        if self.zip_path:
            # Use directory loader for exports
            kwargs.update({"zip_path": self.zip_path})
        else:
            # Use API loader
            kwargs.update(
                {
                    "slack_token": (
                        self.slack_token or self.get_api_key()
                        if hasattr(self, "get_api_key")
                        else None
                    ),
                    "workspace_url": self.workspace_url,
                }
            )

        return kwargs


@register_source(
    name="microsoft_teams",
    category=SourceCategory.MESSAGING,
    loaders={
        "teams": {
            "class": "MicrosoftTeamsLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["msal"],
        }
    },
    default_loader="teams",
    description="Microsoft Teams chat and channel content loader",
    requires_credentials=True,
    credential_type=CredentialType.API_KEY,
    capabilities=[
        LoaderCapability.BULK_LOADING,
        LoaderCapability.FILTERING,
        LoaderCapability.RATE_LIMITED,
    ],
    priority=8,
)
class MicrosoftTeamsSource(MessagingSource):
    """Microsoft Teams content source."""

    platform: MessagingPlatform = MessagingPlatform.MICROSOFT_TEAMS

    # Teams-specific options
    tenant_id: str = Field(..., description="Microsoft tenant ID")
    team_id: Optional[str] = Field(None, description="Specific team ID")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update({"tenant_id": self.tenant_id, "team_id": self.team_id})

        return kwargs


# =============================================================================
# Social Media Sources
# =============================================================================


@register_source(
    name="twitter",
    category=SourceCategory.MESSAGING,
    loaders={
        "twitter": {
            "class": "TwitterTweetLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["tweepy"],
        }
    },
    default_loader="twitter",
    description="Twitter/X tweets and thread loader",
    requires_credentials=True,
    credential_type=CredentialType.API_KEY,
    capabilities=[
        LoaderCapability.BULK_LOADING,
        LoaderCapability.FILTERING,
        LoaderCapability.RATE_LIMITED,
    ],
    priority=9,
)
class TwitterSource(MessagingSource):
    """Twitter/X tweets and content source."""

    platform: MessagingPlatform = MessagingPlatform.TWITTER

    # Twitter-specific options
    bearer_token: Optional[str] = Field(None, description="Twitter Bearer token")

    # Search options
    search_query: Optional[str] = Field(None, description="Twitter search query")
    hashtags: Optional[List[str]] = Field(None, description="Hashtags to search")
    usernames: Optional[List[str]] = Field(None, description="Specific usernames")

    # Content options
    include_retweets: bool = Field(False, description="Include retweets")
    include_replies: bool = Field(False, description="Include replies")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update(
            {
                "bearer_token": (
                    self.bearer_token or self.get_api_key()
                    if hasattr(self, "get_api_key")
                    else None
                ),
                "search_query": self.search_query,
                "hashtags": self.hashtags,
                "usernames": self.usernames,
                "include_retweets": self.include_retweets,
                "include_replies": self.include_replies,
            }
        )

        return kwargs


@register_source(
    name="reddit",
    category=SourceCategory.MESSAGING,
    loaders={
        "reddit": {
            "class": "RedditPostsLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["praw"],
        }
    },
    default_loader="reddit",
    description="Reddit posts and comments loader",
    requires_credentials=True,
    credential_type=CredentialType.API_KEY,
    capabilities=[
        LoaderCapability.BULK_LOADING,
        LoaderCapability.FILTERING,
        LoaderCapability.RATE_LIMITED,
    ],
    priority=9,
)
class RedditSource(MessagingSource):
    """Reddit posts and comments source."""

    platform: MessagingPlatform = MessagingPlatform.REDDIT

    # Reddit-specific options
    client_id: Optional[str] = Field(None, description="Reddit client ID")
    client_secret: Optional[str] = Field(None, description="Reddit client secret")
    user_agent: str = Field("haive-document-loader", description="User agent string")

    # Search options
    subreddits: Optional[List[str]] = Field(None, description="Specific subreddits")
    search_query: Optional[str] = Field(None, description="Search query")
    sort_by: str = Field("hot", description="Sort posts by: hot, new, top, rising")

    # Content options
    include_comments: bool = Field(True, description="Include post comments")
    max_comments: int = Field(100, ge=1, description="Maximum comments per post")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update(
            {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "user_agent": self.user_agent,
                "subreddits": self.subreddits,
                "search_query": self.search_query,
                "sort_by": self.sort_by,
                "include_comments": self.include_comments,
                "max_comments": self.max_comments,
            }
        )

        return kwargs


@register_source(
    name="mastodon",
    category=SourceCategory.MESSAGING,
    loaders={
        "mastodon": {
            "class": "MastodonTootsLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["Mastodon.py"],
        }
    },
    default_loader="mastodon",
    description="Mastodon toots and timeline loader",
    requires_credentials=True,
    credential_type=CredentialType.API_KEY,
    capabilities=[LoaderCapability.BULK_LOADING, LoaderCapability.FILTERING],
    priority=7,
)
class MastodonSource(MessagingSource):
    """Mastodon toots and content source."""

    platform: MessagingPlatform = MessagingPlatform.MASTODON

    # Mastodon-specific options
    instance_url: str = Field(..., description="Mastodon instance URL")
    access_token: Optional[str] = Field(None, description="Mastodon access token")

    # Content options
    timeline_type: str = Field(
        "home", description="Timeline type: home, local, federated"
    )

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update(
            {
                "api_base_url": self.instance_url,
                "access_token": (
                    self.access_token or self.get_api_key()
                    if hasattr(self, "get_api_key")
                    else None
                ),
                "timeline": self.timeline_type,
            }
        )

        return kwargs


# =============================================================================
# Email and Communication Sources
# =============================================================================


@register_source(
    name="email_imap",
    category=SourceCategory.MESSAGING,
    loaders={
        "imap": {
            "class": "IMAPEmailLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
        }
    },
    default_loader="imap",
    description="IMAP email server loader",
    requires_credentials=True,
    credential_type=CredentialType.USERNAME_PASSWORD,
    capabilities=[LoaderCapability.BULK_LOADING, LoaderCapability.FILTERING],
    priority=8,
)
class IMAPEmailSource(MessagingSource):
    """IMAP email server source."""

    platform: MessagingPlatform = MessagingPlatform.IMAP

    # IMAP configuration
    imap_server: str = Field(..., description="IMAP server hostname")
    port: int = Field(993, description="IMAP server port")
    use_ssl: bool = Field(True, description="Use SSL connection")

    # Authentication
    username: str = Field(..., description="Email username")
    password: Optional[str] = Field(None, description="Email password")

    # Email filtering
    folder: str = Field("INBOX", description="Email folder to read")
    search_criteria: Optional[str] = Field(None, description="IMAP search criteria")

    # Processing options
    include_attachments: bool = Field(False, description="Process email attachments")
    max_emails: Optional[int] = Field(
        None, ge=1, description="Maximum emails to process"
    )

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update(
            {
                "mail_server": self.imap_server,
                "mail_port": self.port,
                "mail_use_ssl": self.use_ssl,
                "mail_username": self.username,
                "mail_password": self.password,
                "folder": self.folder,
                "search_criteria": self.search_criteria,
                "include_attachments": self.include_attachments,
            }
        )

        if self.max_emails:
            kwargs["max_emails"] = self.max_emails

        return kwargs


@register_source(
    name="gmail_api",
    category=SourceCategory.MESSAGING,
    loaders={
        "gmail": {
            "class": "GmailLoader",
            "speed": "fast",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": [
                "google-auth",
                "google-auth-oauthlib",
                "google-auth-httplib2",
                "google-api-python-client",
            ],
        }
    },
    default_loader="gmail",
    description="Gmail API loader with OAuth authentication",
    requires_credentials=True,
    credential_type=CredentialType.OAUTH,
    capabilities=[
        LoaderCapability.BULK_LOADING,
        LoaderCapability.FILTERING,
        LoaderCapability.RATE_LIMITED,
    ],
    priority=9,
)
class GmailSource(MessagingSource):
    """Gmail API source with OAuth."""

    platform: MessagingPlatform = MessagingPlatform.GMAIL

    # Gmail API configuration
    credentials_path: Optional[str] = Field(
        None, description="Path to Google credentials JSON"
    )
    token_path: Optional[str] = Field(None, description="Path to OAuth token file")

    # Search options
    query: Optional[str] = Field(None, description="Gmail search query")
    label_ids: Optional[List[str]] = Field(
        None, description="Gmail label IDs to filter"
    )

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update(
            {
                "credentials_path": self.credentials_path,
                "token_path": self.token_path,
                "query": self.query,
                "label_ids": self.label_ids,
            }
        )

        return kwargs


# =============================================================================
# Messaging Apps Sources
# =============================================================================


@register_source(
    name="whatsapp_export",
    category=SourceCategory.MESSAGING,
    loaders={
        "whatsapp": {
            "class": "WhatsAppChatLoader",
            "speed": "fast",
            "quality": "medium",
            "module": "langchain_community.document_loaders",
        }
    },
    default_loader="whatsapp",
    description="WhatsApp chat export loader",
    requires_credentials=False,
    capabilities=[LoaderCapability.BULK_LOADING, LoaderCapability.FILTERING],
    priority=7,
)
class WhatsAppSource(MessagingSource):
    """WhatsApp chat export source."""

    platform: MessagingPlatform = MessagingPlatform.WHATSAPP

    # WhatsApp-specific options
    chat_export_path: str = Field(..., description="Path to WhatsApp chat export file")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update({"path": self.chat_export_path})

        return kwargs


@register_source(
    name="telegram_export",
    category=SourceCategory.MESSAGING,
    loaders={
        "telegram": {
            "class": "TelegramChatLoader",
            "speed": "fast",
            "quality": "medium",
            "module": "langchain_community.document_loaders",
        }
    },
    default_loader="telegram",
    description="Telegram chat export loader",
    requires_credentials=False,
    capabilities=[LoaderCapability.BULK_LOADING, LoaderCapability.FILTERING],
    priority=7,
)
class TelegramSource(MessagingSource):
    """Telegram chat export source."""

    platform: MessagingPlatform = MessagingPlatform.TELEGRAM

    # Telegram-specific options
    chat_export_path: str = Field(..., description="Path to Telegram chat export JSON")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update({"chat_file": self.chat_export_path})

        return kwargs


# =============================================================================
# Bulk Messaging Sources
# =============================================================================


@register_bulk_source(
    name="multi_chat_export",
    category=SourceCategory.MESSAGING,
    loaders={
        "multi_chat": {
            "class": "DirectoryLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
        }
    },
    default_loader="multi_chat",
    description="Bulk chat export processor for multiple platforms",
    max_concurrent=4,
    capabilities=[
        LoaderCapability.BULK_LOADING,
        LoaderCapability.FILTERING,
        LoaderCapability.RECURSIVE,
    ],
    priority=8,
)
class MultiChatExportSource(MessagingSource):
    """Bulk chat export processor."""

    platform: MessagingPlatform = MessagingPlatform.DISCORD  # Default, will auto-detect

    # Bulk processing options
    export_directory: str = Field(..., description="Directory containing chat exports")
    auto_detect_platform: bool = Field(
        True, description="Auto-detect chat platform from files"
    )
    supported_formats: List[str] = Field(
        default=["json", "txt", "csv", "html"], description="Supported export formats"
    )

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update(
            {
                "path": self.export_directory,
                "glob": f"**/*.{{{','.join(self.supported_formats)}}}",
                "recursive": True,
                "auto_detect": self.auto_detect_platform,
            }
        )

        return kwargs


# =============================================================================
# Utility Functions
# =============================================================================


def get_messaging_sources_statistics() -> Dict[str, Any]:
    """Get statistics about messaging sources."""
    registry = enhanced_registry

    # Find messaging sources by category
    messaging_sources = len(registry.find_sources_by_category(SourceCategory.MESSAGING))

    # Find platform-specific counts
    platform_counts = {}
    for platform in MessagingPlatform:
        platform_sources = [
            name
            for name, registration in registry._sources.items()
            if hasattr(registration, "platform") and registration.platform == platform
        ]
        if platform_sources:
            platform_counts[platform.value] = len(platform_sources)

    # Find capability-based statistics
    api_sources = len(
        [
            name
            for name, registration in registry._sources.items()
            if registration.requires_credentials
            and registration.credential_type == CredentialType.API_KEY
        ]
    )

    bulk_messaging = len(
        [
            name
            for name in registry._sources.keys()
            if any(keyword in name for keyword in ["multi", "bulk", "export"])
        ]
    )

    return {
        "total_messaging_sources": messaging_sources,
        "platform_breakdown": platform_counts,
        "api_authenticated_sources": api_sources,
        "bulk_export_sources": bulk_messaging,
        "supported_platforms": len(MessagingPlatform),
        "content_types": len(ContentType),
        "date_range_options": len(DateRange),
    }


def validate_messaging_sources() -> bool:
    """Validate messaging source registrations."""
    registry = enhanced_registry

    required_messaging_sources = [
        "discord",
        "slack",
        "twitter",
        "reddit",
        "email_imap",
        "gmail_api",
        "whatsapp_export",
        "telegram_export",
    ]

    missing = []
    for source_name in required_messaging_sources:
        if source_name not in registry._sources:
            missing.append(source_name)

    if missing:
        print(f"Missing messaging sources: {missing}")
        return False

    print(
        f"✅ All {len(required_messaging_sources)} essential messaging sources registered!"
    )
    return True


def detect_chat_platform(file_path: str) -> Optional[MessagingPlatform]:
    """Auto-detect chat platform from export file."""
    file_path_lower = file_path.lower()

    # Platform detection patterns
    patterns = {
        MessagingPlatform.DISCORD: ["discord", "guild", "channel"],
        MessagingPlatform.SLACK: ["slack", "workspace"],
        MessagingPlatform.WHATSAPP: ["whatsapp", "wa_", "_chat.txt"],
        MessagingPlatform.TELEGRAM: ["telegram", "result.json"],
        MessagingPlatform.TWITTER: ["twitter", "tweet", "x.com"],
        MessagingPlatform.REDDIT: ["reddit", "subreddit"],
    }

    for platform, keywords in patterns.items():
        if any(keyword in file_path_lower for keyword in keywords):
            return platform

    return None


# Auto-validate on import
if __name__ == "__main__":
    validate_messaging_sources()
    stats = get_messaging_sources_statistics()
    print(f"Messaging Sources Statistics: {stats}")
