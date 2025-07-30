"""State core module.

This module provides state functionality for the Haive framework.

Classes:
    DirectedState: DirectedState implementation.
"""

# src/haive/agents/conversation/directed.py
"""Directed conversation agent where participants respond to mentions and direct questions."""


import logging

from pydantic import Field

from haive.agents.conversation.base.state import ConversationState

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)


class DirectedState(ConversationState):
    """Extended state for directed conversations."""

    # Track who was mentioned
    mentioned_speakers: list[str] = Field(default_factory=list)
    pending_speakers: list[str] = Field(default_factory=list)
    # Track interaction patterns
    interaction_count: dict[str, dict[str, int]] = Field(
        default_factory=dict, description="Track who mentions whom"
    )
