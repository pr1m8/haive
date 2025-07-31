"""Models for the Self-Discover Adapter Agent."""

from pydantic import BaseModel, Field


class AdaptedModule(BaseModel):
    """A reasoning module adapted for the specific task."""

    original_module: str = Field(
        ..., description="The original module name/description"
    )
    task_specific_adaptation: str = Field(
        ..., description="The module adapted specifically for this task"
    )
    concrete_steps: list[str] = Field(
        ...,
        description="Concrete steps or questions for applying this module",
        min_length=2,
    )
    expected_insights: str = Field(
        ..., description="What insights this adapted module should provide"
    )


class AdaptedModules(BaseModel):
    """Collection of task-adapted reasoning modules."""

    task_context: str = Field(
        ..., description="Brief context about the task these are adapted for"
    )
    adapted_modules: list[AdaptedModule] = Field(
        ..., description="List of adapted reasoning modules"
    )
    integration_strategy: str = Field(
        ..., description="How these adapted modules work together"
    )
