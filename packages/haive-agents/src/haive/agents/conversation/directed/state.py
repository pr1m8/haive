# src/haive/agents/conversation/directed.py
"""Directed conversation agent where participants respond to mentions and direct questions."""


from haive.core.logging.rich_logger import LogLevel, get_logger
from pydantic import Field

from haive.agents.conversation.base.state import ConversationState

logger = get_logger(__name__)
logger.set_level(LogLevel.WARNING)


class DirectedState(ConversationState):
    """Extended state for directed conversations."""

    # Track who was mentioned
    mentioned_speakers: list[str] = Field(default_factory=list)
    pending_speakers: list[str] = Field(default_factory=list)
    # Track interaction patterns
    interaction_count: dict[str, dict[str, int]] = Field(
        default_factory=dict, description="Track who mentions whom"
    )
