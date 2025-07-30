"""Models model module.

This module provides models functionality for the Haive framework.

Classes:
    SelectedModule: SelectedModule implementation.
    ModuleSelectionResult: ModuleSelectionResult implementation.
    AdaptedModule: AdaptedModule implementation.

Functions:
    format_for_next_stage: Format For Next Stage functionality.
    validate_modules: Validate Modules functionality.
    format_for_next_stage: Format For Next Stage functionality.
"""

# src/haive/agents/selfdiscover/models.py

from typing import Any

from pydantic import BaseModel, Field, field_validator


class SelectedModule(BaseModel):
    """A reasoning module selected for a specific problem."""

    module_id: str = Field(
        description="Identifier for the module (e.g., '1', '4', '10')"
    )
    module_name: str = Field(description="Name or brief description of the module")
    rationale: str = Field(
        description="Explanation of why this module is relevant for the task"
    )


class ModuleSelectionResult(BaseModel):
    """Result of the module selection stage."""

    selected_modules: list[SelectedModule] = Field(
        description="List of selected reasoning modules"
    )

    def format_for_next_stage(self) -> str:
        """Format the selected modules for the adaptation stage."""
        formatted = "SELECTED MODULES:\n\n"
        for module in self.selected_modules:
            formatted += f"Module {module.module_id}: {module.module_name}\n"
            formatted += f"Rationale: {module.rationale}\n\n"
        return formatted

    @field_validator("selected_modules")
    @classmethod
    def validate_modules(cls, modules) -> Any:
        """Ensure we have a reasonable number of modules."""
        if len(modules) < 1:
            raise ValueError("At least one module must be selected")
        if len(modules) > 7:
            raise ValueError("Too many modules selected (maximum 7)")
        return modules


class AdaptedModule(BaseModel):
    """An adapted version of a reasoning module for a specific task."""

    original_module_id: str = Field(description="Reference to the original module ID")
    adapted_description: str = Field(
        description="Customized description for this specific task"
    )
    application_strategy: str = Field(
        description="How to apply this module to the specific task"
    )


class ModuleAdaptationResult(BaseModel):
    """Result of the module adaptation stage."""

    adapted_modules: list[AdaptedModule] = Field(
        description="List of adapted reasoning modules"
    )

    def format_for_next_stage(self) -> str:
        """Format the adapted modules for the structure stage."""
        formatted = "ADAPTED MODULES:\n\n"
        for module in self.adapted_modules:
            formatted += f"Module {module.original_module_id} (Adapted):\n"
            formatted += f"{module.adapted_description}\n"
            formatted += f"Application: {module.application_strategy}\n\n"
        return formatted


class ReasoningStep(BaseModel):
    """A step in the reasoning plan."""

    step_id: str = Field(description="Identifier for the step (e.g., 'step1', 'step2')")
    description: str = Field(
        description="Description of what to determine in this step"
    )
    related_module_ids: list[str] | None = Field(
        default=None, description="IDs of related modules"
    )


class ReasoningStructure(BaseModel):
    """A structured reasoning plan."""

    steps: list[ReasoningStep] = Field(
        description="List of steps in the reasoning plan"
    )

    def format_for_next_stage(self) -> str:
        """Format the reasoning structure as JSON for the reasoning stage."""
        formatted = "{\n"
        for step in self.steps:
            formatted += f'  "{step.step_id}": "{step.description}",\n'
        # Remove the last comma and add closing brace
        formatted = formatted.rstrip(",\n") + "\n}"
        return formatted

    @field_validator("steps")
    @classmethod
    def validate_steps(cls, steps) -> Any:
        """Ensure we have a reasonable number of steps."""
        if len(steps) < 1:
            raise ValueError("At least one step must be included")
        return steps


class ReasoningOutputStep(BaseModel):
    """A completed step in the reasoning process."""

    step_id: str = Field(description="Identifier for the step")
    reasoning: str = Field(description="Detailed reasoning for this step")
    result: Any | None = Field(
        default=None, description="Result of this step (if applicable)"
    )


class ReasoningOutput(BaseModel):
    """Complete reasoning output with all steps and final answer."""

    completed_steps: list[ReasoningOutputStep] = Field(
        description="List of completed reasoning steps"
    )
    final_answer: str = Field(description="Final answer to the problem")
    confidence: float | None = Field(
        default=None, description="Confidence in the answer (0-1)"
    )

    def format_complete_reasoning(self) -> str:
        """Format the complete reasoning process."""
        formatted = "STEP-BY-STEP REASONING:\n\n"
        for step in self.completed_steps:
            formatted += f"**{step.step_id}**\n"
            formatted += f"{step.reasoning}\n\n"

        formatted += f"**FINAL ANSWER**: {self.final_answer}\n"

        if self.confidence is not None:
            formatted += f"Confidence: {self.confidence * 100:.0f}%\n"

        return formatted
