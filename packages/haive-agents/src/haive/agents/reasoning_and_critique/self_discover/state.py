# src/haive/agents/selfdiscover/state.py

from collections.abc import Sequence
from typing import Annotated, Any

from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages
from pydantic import BaseModel, Field


class SelfDiscoverState(BaseModel):
    """State schema for the SelfDiscover agent.

    This schema tracks all information needed for the SelfDiscover process:
    - messages: Conversation history
    - reasoning_modules: Available reasoning modules
    - task_description: The problem to solve
    - selected_modules: Modules chosen for this task
    - adapted_modules: Customized modules for this task
    - reasoning_structure: JSON plan for solving the task
    - answer: Final solution
    """

    # Communication and tracking fields
    messages: Annotated[Sequence[BaseMessage], add_messages] = Field(
        default_factory=list, description="Messages in the conversation"
    )

    error: str | None = Field(
        default=None, description="Error message if any step fails"
    )

    # Core SelfDiscover fields
    reasoning_modules: str = Field(
        default="",
        description="Available reasoning modules to choose from (formatted string)",
    )

    task_description: str = Field(
        default="", description="Description of the task to solve"
    )

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

    answer: str | None = Field(
        default=None, description="Final solution to the problem"
    )

    # Optional metadata fields
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata for the reasoning process",
    )
