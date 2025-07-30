"""State core module.

This module provides state functionality for the Haive framework.

Classes:
    SocialMediaState: SocialMediaState implementation.
"""

import logging
from typing import Literal

from pydantic import Field

from haive.agents.conversation.base.state import ConversationState

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)


class SocialMediaState(ConversationState):
    """Extended state for social media conversations."""

    # Social metrics
    likes: dict[str, int] = Field(default_factory=dict)
    replies: dict[str, list[str]] = Field(default_factory=dict)
    shares: dict[str, int] = Field(default_factory=dict)
    followers: dict[str, set[str]] = Field(default_factory=dict)

    # Posting metrics
    posts_count: dict[str, int] = Field(default_factory=dict)
    engagement_rate: dict[str, float] = Field(default_factory=dict)

    # Viral mechanics
    viral_threshold: int = Field(default=10)
    trending_topics: list[str] = Field(default_factory=list)
    viral_posts: list[tuple[str, str]] = Field(
        default_factory=list
    )  # (author, content)

    # Platform state
    platform_type: Literal["twitter", "instagram", "tiktok", "generic"] = Field(
        default="generic"
    )
    hashtags_used: dict[str, list[str]] = Field(default_factory=dict)
