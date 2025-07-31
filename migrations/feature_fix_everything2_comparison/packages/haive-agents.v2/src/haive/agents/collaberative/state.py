"""State core module.

This module provides state functionality for the Haive framework.

Classes:
    CollaborativeState: CollaborativeState implementation.

Functions:
    merge_document_sections: Merge Document Sections functionality.
    merge_contribution_counts: Merge Contribution Counts functionality.
"""

# src/haive/agents/conversation/collaborative/state.py
"""State for collaborative conversation agents."""

import operator
from typing import Literal

from pydantic import Field

from haive.agents.conversation.base.state import ConversationState


def merge_document_sections(
    current: dict[str, str], update: dict[str, str]
) -> dict[str, str]:
    """Merge document sections, preserving existing content."""
    result = current.copy()
    for section, content in update.items():
        if section in result:
            # Append to existing content if there's already content
            if result[section] and content:
                result[section] = result[section].rstrip() + "\n" + content
            elif content:  # Only update if new content is non-empty
                result[section] = content
        else:
            result[section] = content
    return result


def merge_contribution_counts(
    current: dict[str, int], update: dict[str, int]
) -> dict[str, int]:
    """Merge contribution counts by summing values."""
    result = current.copy()
    for contributor, count in update.items():
        result[contributor] = result.get(contributor, 0) + count
    return result


class CollaborativeState(ConversationState):
    """Extended state for collaborative conversations."""

    # Shared document/artifact
    shared_document: str = Field(default="")
    document_sections: dict[str, str] = Field(default_factory=dict)

    # Contribution tracking
    contributions: list[tuple[str, str, str]] = Field(
        default_factory=list,
        description="List of (contributor, section, content) tuples",
    )
    contribution_count: dict[str, int] = Field(default_factory=dict)

    # Collaboration flow
    current_section: str | None = Field(default=None)
    sections_order: list[str] = Field(default_factory=list)
    completed_sections: list[str] = Field(default_factory=list)

    # Review and consensus
    pending_reviews: list[tuple[str, str]] = Field(
        default_factory=list, description="List of (section, content) pending review"
    )
    approvals: dict[str, list[str]] = Field(
        default_factory=dict, description="Section -> list of approvers"
    )

    # Output format
    output_format: Literal["markdown", "code", "outline", "report"] = Field(
        default="markdown"
    )

    # Add custom reducers for proper merging
    __reducer_fields__ = {
        **ConversationState.__reducer_fields__,
        "contributions": operator.add,  # Accumulate contributions
        "document_sections": merge_document_sections,  # Merge sections properly
        "contribution_count": merge_contribution_counts,  # Sum contribution counts
        "completed_sections": operator.add,  # Accumulate completed sections
    }
