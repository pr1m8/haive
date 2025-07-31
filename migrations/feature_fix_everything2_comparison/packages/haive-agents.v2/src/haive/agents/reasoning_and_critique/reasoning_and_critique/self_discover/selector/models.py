"""Models for the Self-Discover Selector Agent."""

from pydantic import BaseModel, Field


class SelectedModule(BaseModel):
    """A reasoning module selected for the task."""

    module_number: int = Field(
        ..., description="The number of the module from the available list"
    )
    module_name: str = Field(..., description="The name/type of the reasoning module")
    relevance_explanation: str = Field(
        ..., description="Why this module is relevant for the task"
    )
    contribution: str = Field(
        ..., description="How this module will contribute to solving the task"
    )


class ModuleSelection(BaseModel):
    """The complete module selection for a task."""

    task_summary: str = Field(
        ..., description="Brief summary of the task being analyzed"
    )
    selected_modules: list[SelectedModule] = Field(
        ...,
        description="List of selected reasoning modules (3-5 modules)",
        min_length=3,
        max_length=5,
    )
    selection_rationale: str = Field(
        ..., description="Overall rationale for the module selection"
    )
