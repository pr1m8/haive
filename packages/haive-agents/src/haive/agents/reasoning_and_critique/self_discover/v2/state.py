# src/haive/agents/self_discovery/state.py
"""
State schema for Self-Discovery reasoning system.
"""

from typing import Any, Dict, List, Optional

from haive.core.schema.prebuilt.messages.messages_state import MessagesState
from pydantic import Field


class SelfDiscoveryState(MessagesState):
    """State for self-discovery reasoning workflow."""

    # Input fields
    reasoning_modules: str = Field(
        description="All available reasoning module descriptions"
    )
    task_description: str = Field(description="The task to be solved")

    # Intermediate fields
    selected_modules: Optional[List[str]] = Field(
        default=None, description="Selected reasoning modules for the task"
    )
    adapted_modules: Optional[List[Dict[str, str]]] = Field(
        default=None, description="Adapted modules specific to the task"
    )
    reasoning_structure: Optional[Dict[str, Any]] = Field(
        default=None, description="Step-by-step reasoning structure"
    )

    # Output field
    answer: Optional[str] = Field(default=None, description="Final answer to the task")

    # Shared fields for LangGraph
    __shared_fields__ = [
        "messages",
        "reasoning_modules",
        "task_description",
        "selected_modules",
        "adapted_modules",
        "reasoning_structure",
        "answer",
    ]
