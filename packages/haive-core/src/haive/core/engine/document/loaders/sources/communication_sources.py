"""Communication and collaboration platform source registrations.

This module implements the final comprehensive set of communication, collaboration,
and productivity platform loaders including:
- Additional messaging platforms (Matrix, XMPP, IRC)
- International social media (WeChat, LINE, Kakao)
- Video conferencing platforms (Zoom, Teams, Meet)
- Collaboration tools (Miro, Figma, Canva)
- Documentation platforms (Gitiles, Bookstack, Outline)
- Regional platforms and specialized services
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import Field

from .enhanced_registry import enhanced_registry, register_bulk_source, register_source
from .source_types import CredentialType, LoaderCapability, RemoteSource, SourceCategory


class CommunicationPlatform(str, Enum):
    """Communication and collaboration platforms."""

    # Advanced Messaging
    MATRIX = "matrix"
    XMPP = "xmpp"
    IRC = "irc"
    ROCKETCHAT = "rocketchat"
    MATTERMOST = "mattermost"

    # International Social Media
    WECHAT = "wechat"
    LINE = "line"
    KAKAO = "kakao"
    VIBER = "viber"
    SIGNAL = "signal"

    # Video Conferencing
    ZOOM = "zoom"
    TEAMS = "teams"
    GOOGLE_MEET = "google_meet"
    WEBEX = "webex"
    GOTO_MEETING = "goto_meeting"

    # Design & Collaboration
    FIGMA = "figma"
    MIRO = "miro"
    CANVA = "canva"
    SKETCH = "sketch"
    INVISION = "invision"

    # Documentation Platforms
    GITILES = "gitiles"
    BOOKSTACK = "bookstack"
    OUTLINE = "outline"
    SLAB = "slab"
    TETTRA = "tettra"

    # Regional Platforms
    DINGTALK = "dingtalk"  # China
    LARK = "lark"  # ByteDance
    SLACK_CONNECT = "slack_connect"
    DISCORD_STAGE = "discord_stage"

    # Specialized
    INTERCOM = "intercom"
    ZENDESK_CHAT = "zendesk_chat"
    FRESHCHAT = "freshchat"
    DRIFT = "drift"


class ContentType(str, Enum):
    """Types of communication content."""

    MESSAGES = "messages"
    THREADS = "threads"
    CHANNELS = "channels"
    DIRECT_MESSAGES = "direct_messages"
    FILES = "files"
    RECORDINGS = "recordings"
    TRANSCRIPTS = "transcripts"
    DESIGNS = "designs"
    COMMENTS = "comments"
    REACTIONS = "reactions"
    PRESENCE = "presence"
    ANALYTICS = "analytics"


class ExportFormat(str, Enum):
    """Export formats for communication data."""

    JSON = "json"
    CSV = "csv"
    HTML = "html"
    XML = "xml"
    MBOX = "mbox"
    EML = "eml"
    PDF = "pdf"
    MARKDOWN = "markdown"


# =============================================================================
# Advanced Messaging Platforms
# =============================================================================


@register_bulk_source(
    name="matrix",
    category=SourceCategory.COMMUNICATION,
    loaders={
        "matrix": {
            "class": "MatrixLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["matrix-client"],
        }
    },
    default_loader="matrix",
    description="Matrix decentralized chat protocol loader",
    requires_credentials=True,
    credential_type=CredentialType.API_KEY,
    capabilities=[
        LoaderCapability.BULK_LOADING,
        LoaderCapability.REAL_TIME,
        LoaderCapability.ENCRYPTION_SUPPORT,
        LoaderCapability.FEDERATION,
    ],
    supports_scrape_all=True,
    priority=8,
)
class MatrixSource(RemoteSource):
    """Matrix decentralized messaging source."""

    source_type: str = "matrix"
    category: SourceCategory = SourceCategory.COMMUNICATION
    platform: CommunicationPlatform = CommunicationPlatform.MATRIX

    # Matrix configuration
    homeserver_url: str = Field(..., description="Matrix homeserver URL")
    access_token: Optional[str] = Field(None, description="Access token")
    username: Optional[str] = Field(None, description="Username")
    password: Optional[str] = Field(None, description="Password")

    # Room selection
    room_ids: Optional[List[str]] = Field(None, description="Specific room IDs")
    room_aliases: Optional[List[str]] = Field(None, description="Room aliases")

    # Content options
    include_media: bool = Field(True, description="Include media files")
    include_redacted: bool = Field(False, description="Include redacted messages")
    decrypt_events: bool = Field(True, description="Decrypt encrypted events")

    # Time range
    start_date: Optional[datetime] = Field(None, description="Start date")
    end_date: Optional[datetime] = Field(None, description="End date")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update(
            {
                "homeserver": self.homeserver_url,
                "access_token": (
                    self.access_token or self.get_api_key()
                    if hasattr(self, "get_api_key")
                    else None
                ),
                "include_media": self.include_media,
                "include_redacted": self.include_redacted,
                "decrypt_events": self.decrypt_events,
            }
        )

        if not self.access_token and self.username and self.password:
            kwargs["username"] = self.username
            kwargs["password"] = self.password

        if self.room_ids:
            kwargs["room_ids"] = self.room_ids
        elif self.room_aliases:
            kwargs["room_aliases"] = self.room_aliases

        if self.start_date:
            kwargs["start_timestamp"] = int(self.start_date.timestamp() * 1000)
        if self.end_date:
            kwargs["end_timestamp"] = int(self.end_date.timestamp() * 1000)

        return kwargs

    def scrape_all(self) -> Dict[str, Any]:
        """Scrape all accessible rooms."""
        return {
            "include_joined_rooms": True,
            "include_invited_rooms": False,
            "include_media": self.include_media,
            "export_format": "json",
        }


@register_source(
    name="rocketchat",
    category=SourceCategory.COMMUNICATION,
    loaders={
        "rocketchat": {
            "class": "RocketChatLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["rocketchat-api"],
        }
    },
    default_loader="rocketchat",
    description="Rocket.Chat team collaboration platform loader",
    requires_credentials=True,
    credential_type=CredentialType.API_KEY,
    capabilities=[
        LoaderCapability.BULK_LOADING,
        LoaderCapability.REAL_TIME,
        LoaderCapability.THREADING,
    ],
    priority=8,
)
class RocketChatSource(RemoteSource):
    """Rocket.Chat collaboration source."""

    source_type: str = "rocketchat"
    category: SourceCategory = SourceCategory.COMMUNICATION
    platform: CommunicationPlatform = CommunicationPlatform.ROCKETCHAT

    # RocketChat configuration
    server_url: str = Field(..., description="Rocket.Chat server URL")
    username: Optional[str] = Field(None, description="Username")
    password: Optional[str] = Field(None, description="Password")
    user_id: Optional[str] = Field(None, description="User ID")
    auth_token: Optional[str] = Field(None, description="Auth token")

    # Channel/Room selection
    channels: Optional[List[str]] = Field(None, description="Channel names")
    private_groups: Optional[List[str]] = Field(None, description="Private group names")
    direct_messages: bool = Field(False, description="Include direct messages")

    # Content options
    include_attachments: bool = Field(True, description="Include file attachments")
    include_threads: bool = Field(True, description="Include message threads")
    include_reactions: bool = Field(True, description="Include reactions")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update(
            {
                "server_url": self.server_url,
                "include_attachments": self.include_attachments,
                "include_threads": self.include_threads,
                "include_reactions": self.include_reactions,
            }
        )

        # Authentication
        if self.user_id and self.auth_token:
            kwargs["user_id"] = self.user_id
            kwargs["auth_token"] = self.auth_token
        else:
            kwargs["username"] = self.username
            kwargs["password"] = self.password

        # Content selection
        if self.channels:
            kwargs["channels"] = self.channels
        if self.private_groups:
            kwargs["private_groups"] = self.private_groups
        kwargs["direct_messages"] = self.direct_messages

        return kwargs


@register_source(
    name="mattermost",
    category=SourceCategory.COMMUNICATION,
    loaders={
        "mattermost": {
            "class": "MattermostLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["mattermostdriver"],
        }
    },
    default_loader="mattermost",
    description="Mattermost team messaging platform loader",
    requires_credentials=True,
    credential_type=CredentialType.API_KEY,
    capabilities=[
        LoaderCapability.BULK_LOADING,
        LoaderCapability.THREADING,
        LoaderCapability.FILE_ATTACHMENTS,
    ],
    priority=8,
)
class MattermostSource(RemoteSource):
    """Mattermost team messaging source."""

    source_type: str = "mattermost"
    category: SourceCategory = SourceCategory.COMMUNICATION
    platform: CommunicationPlatform = CommunicationPlatform.MATTERMOST

    # Mattermost configuration
    url: str = Field(..., description="Mattermost server URL")
    token: Optional[str] = Field(None, description="Personal access token")
    login_id: Optional[str] = Field(None, description="Login ID")
    password: Optional[str] = Field(None, description="Password")

    # Team and channel selection
    team_name: str = Field(..., description="Team name")
    channel_names: Optional[List[str]] = Field(None, description="Specific channels")
    include_direct_messages: bool = Field(False, description="Include DMs")
    include_group_messages: bool = Field(False, description="Include group messages")

    # Content options
    include_files: bool = Field(True, description="Include file attachments")
    include_deleted: bool = Field(False, description="Include deleted messages")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update(
            {
                "url": self.url,
                "team_name": self.team_name,
                "include_files": self.include_files,
                "include_deleted": self.include_deleted,
                "include_direct_messages": self.include_direct_messages,
                "include_group_messages": self.include_group_messages,
            }
        )

        if self.token:
            kwargs["token"] = self.token
        else:
            kwargs["login_id"] = self.login_id
            kwargs["password"] = self.password

        if self.channel_names:
            kwargs["channel_names"] = self.channel_names

        return kwargs


# =============================================================================
# International Social Media Platforms
# =============================================================================


@register_source(
    name="wechat",
    category=SourceCategory.COMMUNICATION,
    loaders={
        "wechat": {
            "class": "WeChatLoader",
            "speed": "slow",
            "quality": "medium",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["itchat"],
        }
    },
    default_loader="wechat",
    description="WeChat messaging platform loader (China)",
    requires_credentials=True,
    credential_type=CredentialType.OAUTH,
    capabilities=[
        LoaderCapability.QR_CODE_AUTH,
        LoaderCapability.MEDIA_CONTENT,
        LoaderCapability.CONTACT_SYNC,
    ],
    priority=7,
)
class WeChatSource(RemoteSource):
    """WeChat messaging source."""

    source_type: str = "wechat"
    category: SourceCategory = SourceCategory.COMMUNICATION
    platform: CommunicationPlatform = CommunicationPlatform.WECHAT

    # WeChat options
    include_contacts: bool = Field(True, description="Include contact information")
    include_groups: bool = Field(True, description="Include group chats")
    include_moments: bool = Field(False, description="Include WeChat Moments")

    # Media options
    download_media: bool = Field(False, description="Download media files")
    media_types: List[str] = Field(
        default=["image", "video", "file"], description="Media types to include"
    )

    # Time range
    days_back: int = Field(30, description="Number of days to go back")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update(
            {
                "include_contacts": self.include_contacts,
                "include_groups": self.include_groups,
                "include_moments": self.include_moments,
                "download_media": self.download_media,
                "media_types": self.media_types,
                "days_back": self.days_back,
            }
        )

        return kwargs


@register_source(
    name="line",
    category=SourceCategory.COMMUNICATION,
    loaders={
        "line": {
            "class": "LineLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["linebot-sdk"],
        }
    },
    default_loader="line",
    description="LINE messaging platform loader (Asia)",
    requires_credentials=True,
    credential_type=CredentialType.API_KEY,
    capabilities=[
        LoaderCapability.WEBHOOK_INTEGRATION,
        LoaderCapability.RICH_MESSAGING,
        LoaderCapability.STICKERS,
    ],
    priority=7,
)
class LineSource(RemoteSource):
    """LINE messaging source."""

    source_type: str = "line"
    category: SourceCategory = SourceCategory.COMMUNICATION
    platform: CommunicationPlatform = CommunicationPlatform.LINE

    # LINE configuration
    channel_access_token: Optional[str] = Field(
        None, description="Channel access token"
    )
    channel_secret: Optional[str] = Field(None, description="Channel secret")

    # Content options
    include_text_messages: bool = Field(True, description="Include text messages")
    include_stickers: bool = Field(True, description="Include sticker messages")
    include_images: bool = Field(True, description="Include image messages")
    include_videos: bool = Field(False, description="Include video messages")
    include_audio: bool = Field(False, description="Include audio messages")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update(
            {
                "channel_access_token": (
                    self.channel_access_token or self.get_api_key()
                    if hasattr(self, "get_api_key")
                    else None
                ),
                "channel_secret": self.channel_secret,
                "include_text_messages": self.include_text_messages,
                "include_stickers": self.include_stickers,
                "include_images": self.include_images,
                "include_videos": self.include_videos,
                "include_audio": self.include_audio,
            }
        )

        return kwargs


# =============================================================================
# Video Conferencing Platforms
# =============================================================================


@register_source(
    name="zoom",
    category=SourceCategory.COMMUNICATION,
    loaders={
        "zoom": {
            "class": "ZoomLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["zoomus"],
        }
    },
    default_loader="zoom",
    description="Zoom video conferencing platform loader",
    requires_credentials=True,
    credential_type=CredentialType.JWT,
    capabilities=[
        LoaderCapability.MEETING_RECORDINGS,
        LoaderCapability.TRANSCRIPTS,
        LoaderCapability.CHAT_LOGS,
        LoaderCapability.ANALYTICS,
    ],
    priority=9,
)
class ZoomSource(RemoteSource):
    """Zoom video conferencing source."""

    source_type: str = "zoom"
    category: SourceCategory = SourceCategory.COMMUNICATION
    platform: CommunicationPlatform = CommunicationPlatform.ZOOM

    # Zoom configuration
    api_key: Optional[str] = Field(None, description="JWT API key")
    api_secret: Optional[str] = Field(None, description="JWT API secret")
    jwt_token: Optional[str] = Field(None, description="JWT token")

    # Content selection
    include_meetings: bool = Field(True, description="Include meeting metadata")
    include_recordings: bool = Field(True, description="Include recordings")
    include_transcripts: bool = Field(True, description="Include transcripts")
    include_chat: bool = Field(True, description="Include chat messages")
    include_polls: bool = Field(False, description="Include poll results")
    include_participants: bool = Field(True, description="Include participant data")

    # Filtering
    user_id: Optional[str] = Field(None, description="Specific user ID")
    start_date: Optional[datetime] = Field(None, description="Start date filter")
    end_date: Optional[datetime] = Field(None, description="End date filter")
    meeting_type: str = Field("all", description="Meeting type filter")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update(
            {
                "api_key": (
                    self.api_key or self.get_api_key()
                    if hasattr(self, "get_api_key")
                    else None
                ),
                "api_secret": self.api_secret,
                "jwt_token": self.jwt_token,
                "include_meetings": self.include_meetings,
                "include_recordings": self.include_recordings,
                "include_transcripts": self.include_transcripts,
                "include_chat": self.include_chat,
                "include_polls": self.include_polls,
                "include_participants": self.include_participants,
                "meeting_type": self.meeting_type,
            }
        )

        if self.user_id:
            kwargs["user_id"] = self.user_id
        if self.start_date:
            kwargs["from_date"] = self.start_date.strftime("%Y-%m-%d")
        if self.end_date:
            kwargs["to_date"] = self.end_date.strftime("%Y-%m-%d")

        return kwargs


@register_source(
    name="teams",
    category=SourceCategory.COMMUNICATION,
    loaders={
        "teams": {
            "class": "TeamsLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["msal", "requests"],
        }
    },
    default_loader="teams",
    description="Microsoft Teams collaboration platform loader",
    requires_credentials=True,
    credential_type=CredentialType.OAUTH,
    capabilities=[
        LoaderCapability.CHANNEL_MESSAGES,
        LoaderCapability.MEETING_RECORDINGS,
        LoaderCapability.FILE_ATTACHMENTS,
        LoaderCapability.APPS_INTEGRATION,
    ],
    priority=9,
)
class TeamsSource(RemoteSource):
    """Microsoft Teams collaboration source."""

    source_type: str = "teams"
    category: SourceCategory = SourceCategory.COMMUNICATION
    platform: CommunicationPlatform = CommunicationPlatform.TEAMS

    # Teams configuration
    tenant_id: str = Field(..., description="Azure AD tenant ID")
    client_id: str = Field(..., description="Application client ID")
    client_secret: Optional[str] = Field(None, description="Client secret")

    # Team and channel selection
    team_id: Optional[str] = Field(None, description="Specific team ID")
    channel_ids: Optional[List[str]] = Field(None, description="Specific channel IDs")

    # Content options
    include_messages: bool = Field(True, description="Include channel messages")
    include_files: bool = Field(True, description="Include file attachments")
    include_meetings: bool = Field(True, description="Include meeting data")
    include_calls: bool = Field(False, description="Include call logs")
    include_apps: bool = Field(False, description="Include app interactions")

    # Time range
    start_date: Optional[datetime] = Field(None, description="Start date")
    end_date: Optional[datetime] = Field(None, description="End date")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update(
            {
                "tenant_id": self.tenant_id,
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "include_messages": self.include_messages,
                "include_files": self.include_files,
                "include_meetings": self.include_meetings,
                "include_calls": self.include_calls,
                "include_apps": self.include_apps,
            }
        )

        if self.team_id:
            kwargs["team_id"] = self.team_id
        if self.channel_ids:
            kwargs["channel_ids"] = self.channel_ids

        if self.start_date:
            kwargs["start_date"] = self.start_date.isoformat()
        if self.end_date:
            kwargs["end_date"] = self.end_date.isoformat()

        return kwargs


# =============================================================================
# Design & Collaboration Platforms
# =============================================================================


@register_source(
    name="figma",
    category=SourceCategory.COMMUNICATION,
    loaders={
        "figma": {
            "class": "FigmaLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["requests"],
        }
    },
    default_loader="figma",
    description="Figma design collaboration platform loader",
    requires_credentials=True,
    credential_type=CredentialType.API_KEY,
    capabilities=[
        LoaderCapability.COLLABORATIVE_EDITING,
        LoaderCapability.COMMENTS,
        LoaderCapability.TIME_TRAVEL,
        LoaderCapability.COLLABORATION_DATA,
    ],
    priority=8,
)
class FigmaSource(RemoteSource):
    """Figma design collaboration source."""

    source_type: str = "figma"
    category: SourceCategory = SourceCategory.COMMUNICATION
    platform: CommunicationPlatform = CommunicationPlatform.FIGMA

    # Figma configuration
    access_token: Optional[str] = Field(None, description="Personal access token")

    # File selection
    file_keys: Optional[List[str]] = Field(None, description="Specific file keys")
    team_id: Optional[str] = Field(None, description="Team ID for files")
    project_id: Optional[str] = Field(None, description="Project ID for files")

    # Content options
    include_comments: bool = Field(True, description="Include file comments")
    include_version_history: bool = Field(False, description="Include version history")
    include_components: bool = Field(True, description="Include component details")
    export_images: bool = Field(False, description="Export design images")

    # Export options
    image_format: str = Field("png", description="Image export format")
    image_scale: float = Field(1.0, description="Image scale factor")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update(
            {
                "access_token": (
                    self.access_token or self.get_api_key()
                    if hasattr(self, "get_api_key")
                    else None
                ),
                "include_comments": self.include_comments,
                "include_version_history": self.include_version_history,
                "include_components": self.include_components,
                "export_images": self.export_images,
            }
        )

        if self.file_keys:
            kwargs["file_keys"] = self.file_keys
        if self.team_id:
            kwargs["team_id"] = self.team_id
        if self.project_id:
            kwargs["project_id"] = self.project_id

        if self.export_images:
            kwargs["image_format"] = self.image_format
            kwargs["image_scale"] = self.image_scale

        return kwargs


@register_source(
    name="miro",
    category=SourceCategory.COMMUNICATION,
    loaders={
        "miro": {
            "class": "MiroLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["requests"],
        }
    },
    default_loader="miro",
    description="Miro online whiteboard collaboration platform loader",
    requires_credentials=True,
    credential_type=CredentialType.OAUTH,
    capabilities=[
        LoaderCapability.VISUALIZATION,
        LoaderCapability.COLLABORATION_DATA,
        LoaderCapability.REAL_TIME,
    ],
    priority=7,
)
class MiroSource(RemoteSource):
    """Miro whiteboard collaboration source."""

    source_type: str = "miro"
    category: SourceCategory = SourceCategory.COMMUNICATION
    platform: CommunicationPlatform = CommunicationPlatform.MIRO

    # Miro configuration
    access_token: Optional[str] = Field(None, description="OAuth access token")

    # Board selection
    board_ids: Optional[List[str]] = Field(None, description="Specific board IDs")
    team_id: Optional[str] = Field(None, description="Team ID for boards")

    # Content options
    include_widgets: bool = Field(True, description="Include board widgets")
    include_comments: bool = Field(True, description="Include comments")
    include_metadata: bool = Field(True, description="Include board metadata")
    export_format: ExportFormat = Field(ExportFormat.JSON, description="Export format")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update(
            {
                "access_token": (
                    self.access_token or self.get_api_key()
                    if hasattr(self, "get_api_key")
                    else None
                ),
                "include_widgets": self.include_widgets,
                "include_comments": self.include_comments,
                "include_metadata": self.include_metadata,
                "export_format": self.export_format.value,
            }
        )

        if self.board_ids:
            kwargs["board_ids"] = self.board_ids
        if self.team_id:
            kwargs["team_id"] = self.team_id

        return kwargs


# =============================================================================
# Documentation Platforms
# =============================================================================


@register_source(
    name="outline",
    category=SourceCategory.COMMUNICATION,
    loaders={
        "outline": {
            "class": "OutlineLoader",
            "speed": "fast",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["requests"],
        }
    },
    default_loader="outline",
    description="Outline team knowledge base loader",
    requires_credentials=True,
    credential_type=CredentialType.API_KEY,
    capabilities=[
        LoaderCapability.STRUCTURED_DATA,
        LoaderCapability.COLLABORATIVE_EDITING,
        LoaderCapability.TIME_TRAVEL,
    ],
    priority=8,
)
class OutlineSource(RemoteSource):
    """Outline knowledge base source."""

    source_type: str = "outline"
    category: SourceCategory = SourceCategory.COMMUNICATION
    platform: CommunicationPlatform = CommunicationPlatform.OUTLINE

    # Outline configuration
    api_token: Optional[str] = Field(None, description="API token")
    base_url: str = Field(..., description="Outline instance URL")

    # Content selection
    collection_ids: Optional[List[str]] = Field(
        None, description="Specific collections"
    )
    document_ids: Optional[List[str]] = Field(None, description="Specific documents")

    # Options
    include_archived: bool = Field(False, description="Include archived documents")
    include_drafts: bool = Field(True, description="Include draft documents")
    export_format: ExportFormat = Field(
        ExportFormat.MARKDOWN, description="Export format"
    )

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update(
            {
                "api_token": (
                    self.api_token or self.get_api_key()
                    if hasattr(self, "get_api_key")
                    else None
                ),
                "base_url": self.base_url,
                "include_archived": self.include_archived,
                "include_drafts": self.include_drafts,
                "export_format": self.export_format.value,
            }
        )

        if self.collection_ids:
            kwargs["collection_ids"] = self.collection_ids
        if self.document_ids:
            kwargs["document_ids"] = self.document_ids

        return kwargs


@register_source(
    name="bookstack",
    category=SourceCategory.COMMUNICATION,
    loaders={
        "bookstack": {
            "class": "BookStackLoader",
            "speed": "fast",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["requests"],
        }
    },
    default_loader="bookstack",
    description="BookStack self-hosted wiki platform loader",
    requires_credentials=True,
    credential_type=CredentialType.API_KEY,
    capabilities=[
        LoaderCapability.STRUCTURED_DATA,
        LoaderCapability.FULL_TEXT_SEARCH,
        LoaderCapability.ATTACHMENTS,
    ],
    priority=7,
)
class BookStackSource(RemoteSource):
    """BookStack wiki platform source."""

    source_type: str = "bookstack"
    category: SourceCategory = SourceCategory.COMMUNICATION
    platform: CommunicationPlatform = CommunicationPlatform.BOOKSTACK

    # BookStack configuration
    base_url: str = Field(..., description="BookStack instance URL")
    token_id: Optional[str] = Field(None, description="API token ID")
    token_secret: Optional[str] = Field(None, description="API token secret")

    # Content selection
    shelf_ids: Optional[List[int]] = Field(None, description="Specific shelf IDs")
    book_ids: Optional[List[int]] = Field(None, description="Specific book IDs")
    chapter_ids: Optional[List[int]] = Field(None, description="Specific chapter IDs")
    page_ids: Optional[List[int]] = Field(None, description="Specific page IDs")

    # Options
    include_attachments: bool = Field(True, description="Include attachments")
    include_images: bool = Field(True, description="Include images")
    export_format: ExportFormat = Field(ExportFormat.HTML, description="Export format")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update(
            {
                "base_url": self.base_url,
                "token_id": (
                    self.token_id or self.get_api_key()
                    if hasattr(self, "get_api_key")
                    else None
                ),
                "token_secret": self.token_secret,
                "include_attachments": self.include_attachments,
                "include_images": self.include_images,
                "export_format": self.export_format.value,
            }
        )

        if self.shelf_ids:
            kwargs["shelf_ids"] = self.shelf_ids
        if self.book_ids:
            kwargs["book_ids"] = self.book_ids
        if self.chapter_ids:
            kwargs["chapter_ids"] = self.chapter_ids
        if self.page_ids:
            kwargs["page_ids"] = self.page_ids

        return kwargs


# =============================================================================
# Customer Support Platforms
# =============================================================================


@register_source(
    name="intercom",
    category=SourceCategory.COMMUNICATION,
    loaders={
        "intercom": {
            "class": "IntercomLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["python-intercom"],
        }
    },
    default_loader="intercom",
    description="Intercom customer messaging platform loader",
    requires_credentials=True,
    credential_type=CredentialType.API_KEY,
    capabilities=[
        LoaderCapability.CHAT_LOGS,
        LoaderCapability.CONTACT_SYNC,
        LoaderCapability.AUTOMATION_LOGS,
    ],
    priority=8,
)
class IntercomSource(RemoteSource):
    """Intercom customer messaging source."""

    source_type: str = "intercom"
    category: SourceCategory = SourceCategory.COMMUNICATION
    platform: CommunicationPlatform = CommunicationPlatform.INTERCOM

    # Intercom configuration
    access_token: Optional[str] = Field(None, description="Access token")

    # Data selection
    include_conversations: bool = Field(True, description="Include conversations")
    include_users: bool = Field(True, description="Include user data")
    include_leads: bool = Field(True, description="Include lead data")
    include_events: bool = Field(False, description="Include event data")
    include_articles: bool = Field(True, description="Include help articles")

    # Filtering
    conversation_state: str = Field("all", description="Conversation state filter")
    date_range: Optional[int] = Field(30, description="Days to look back")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update(
            {
                "access_token": (
                    self.access_token or self.get_api_key()
                    if hasattr(self, "get_api_key")
                    else None
                ),
                "include_conversations": self.include_conversations,
                "include_users": self.include_users,
                "include_leads": self.include_leads,
                "include_events": self.include_events,
                "include_articles": self.include_articles,
                "conversation_state": self.conversation_state,
                "date_range": self.date_range,
            }
        )

        return kwargs


# =============================================================================
# Utility Functions
# =============================================================================


def get_communication_sources_statistics() -> Dict[str, Any]:
    """Get statistics about communication sources."""
    registry = enhanced_registry

    # Count by platform type
    platform_counts = {}
    for platform in CommunicationPlatform:
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
    comm_sources = registry.find_sources_by_category(SourceCategory.COMMUNICATION)

    # Real-time sources
    real_time = len(
        [
            name
            for name in comm_sources
            if registry._sources[name].capabilities
            and LoaderCapability.REAL_TIME in registry._sources[name].capabilities
        ]
    )

    # International platforms
    international = len(
        [
            name
            for name in ["wechat", "line", "kakao", "dingtalk"]
            if name in registry._sources
        ]
    )

    return {
        "total_communication_sources": len(comm_sources),
        "platform_breakdown": platform_counts,
        "real_time_sources": real_time,
        "international_platforms": international,
        "content_types": len(ContentType),
        "export_formats": len(ExportFormat),
    }


def validate_communication_sources() -> bool:
    """Validate communication source registrations."""
    registry = enhanced_registry

    required_sources = [
        "matrix",
        "rocketchat",
        "zoom",
        "teams",
        "figma",
        "outline",
        "intercom",
        "miro",
    ]

    missing = []
    for source_name in required_sources:
        if source_name not in registry._sources:
            missing.append(source_name)

    if missing:
        print(f"Missing communication sources: {missing}")
        return False

    print("✅ All essential communication sources registered!")
    return True


def detect_communication_platform(
    url_or_identifier: str,
) -> Optional[CommunicationPlatform]:
    """Auto-detect communication platform from URL or identifier."""
    lower = url_or_identifier.lower()

    patterns = {
        CommunicationPlatform.ZOOM: ["zoom.us", "zoom://"],
        CommunicationPlatform.TEAMS: ["teams.microsoft.com", "teams://"],
        CommunicationPlatform.FIGMA: ["figma.com"],
        CommunicationPlatform.MIRO: ["miro.com"],
        CommunicationPlatform.OUTLINE: ["getoutline.com"],
        CommunicationPlatform.INTERCOM: ["intercom.io", "intercom.com"],
        CommunicationPlatform.ROCKETCHAT: ["rocket.chat"],
        CommunicationPlatform.MATTERMOST: ["mattermost.com"],
    }

    for platform, keywords in patterns.items():
        if any(keyword in lower for keyword in keywords):
            return platform

    return None


# Auto-validate on import
if __name__ == "__main__":
    validate_communication_sources()
    stats = get_communication_sources_statistics()
    print(f"Communication Sources Statistics: {stats}")
