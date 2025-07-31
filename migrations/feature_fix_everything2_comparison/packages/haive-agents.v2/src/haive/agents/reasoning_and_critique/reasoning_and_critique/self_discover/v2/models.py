"""Models model module.

This module provides models functionality for the Haive framework.

Classes:
    SelectedModules: SelectedModules implementation.
    AdaptedModules: AdaptedModules implementation.
    Config: Config implementation.
"""

# src/haive/agents/self_discovery/models.py
"""Structured output models for Self-Discovery reasoning system."""

from typing import Any

from pydantic import BaseModel, Field


class SelectedModules(BaseModel):
    """Selected reasoning modules for the task."""

    selected_modules: list[str] = Field(
        description="List of selected reasoning modules that are crucial for solving the task"
    )
    rationale: str | None = Field(
        default=None, description="Explanation for why these modules were selected"
    )


class AdaptedModules(BaseModel):
    """Adapted reasoning modules tailored to the specific task."""

    adapted_modules: list[dict[str, str]] = Field(
        description="List of adapted modules with 'module' and 'adaptation' keys"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "adapted_modules": [
                    {
                        "module": "Critical Thinking",
                        "adaptation": "Analyze SVG path commands to understand shape formation",
                    }
                ]
            }
        }


class ReasoningStructure(BaseModel):
    """Step-by-step reasoning structure for solving the task."""

    reasoning_structure: dict[str, Any] = Field(
        description="JSON structure defining the step-by-step reasoning plan"
    )
    steps: list[str] = Field(
        default_factory=list, description="Ordered list of reasoning steps to follow"
    )


class FinalAnswer(BaseModel):
    """Final answer with reasoning."""

    answer: str = Field(description="The final answer to the task")
    reasoning_steps: dict[str, str] = Field(
        default_factory=dict,
        description="Filled out reasoning structure with specific values",
    )
    confidence: float | None = Field(
        default=None, ge=0.0, le=1.0, description="Confidence level in the answer (0-1)"
    )
