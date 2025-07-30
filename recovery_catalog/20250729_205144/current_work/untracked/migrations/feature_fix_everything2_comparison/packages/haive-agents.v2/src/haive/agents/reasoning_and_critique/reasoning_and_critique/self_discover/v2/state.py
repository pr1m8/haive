"""State core module.

This module provides state functionality for the Haive framework.

Classes:
    SelfDiscoveryState: SelfDiscoveryState implementation.
"""

# src/haive/agents/self_discovery/state.py
"""State schema for Self-Discovery reasoning system."""

from typing import Any

from haive.core.schema.prebuilt.messages.messages_state import MessagesState
from pydantic import Field


class SelfDiscoveryState(MessagesState):
    """State for self-discovery reasoning workflow."""

    # Input fields
    reasoning_modules: str = Field(
        default="",
        description="Available reasoning modules to choose from (formatted string)",
    )
    task_description: str = Field(
        default="", description="Description of the task to solve"
    )

    # Intermediate fields
    selected_modules: str | None = Field(
        default=None, description="Selected reasoning modules suitable for the task"
    )
    adapted_modules: str | None = Field(
        default=None,
        description="Customized versions of the selected modules for this task",
    )
    reasoning_structure: str | None = Field(
        default=None, description="Structured reasoning plan in JSON format"
    )

    # Output field
    answer: str | None = Field(
        default=None, description="Final solution to the problem"
    )

    # Error handling and metadata (from original version)
    error: str | None = Field(
        default=None, description="Error message if any step fails"
    )

    # Optional metadata fields
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata for the reasoning process",
    )

    # Shared fields for LangGraph
    __shared_fields__ = [
        "messages",
        "reasoning_modules",
        "task_description",
        "selected_modules",
        "adapted_modules",
        "reasoning_structure",
        "answer",
        "error",
        "metadata",
    ]
