"""Configuration for SequentialAgent that connects components in a linear workflow.

This module defines the configuration class for SequentialAgent, which
automates the process of connecting multiple engine components in a sequence.
"""

import logging
import uuid
from typing import Any

from haive.core.engine.agent.config import AgentConfig
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.schema.state_schema import StateSchema
from pydantic import BaseModel, Field, field_validator, model_validator

logger = logging.getLogger(__name__)


class StepConfig(BaseModel):
    """Configuration for a single step in a sequential workflow."""

    # Step identification
    name: str = Field(description="Name for this step")
    component: Any = Field(
        description="Component to use for this step (typically AugLLMConfig or other Engine)"
    )

    # Mapping configuration
    input_mapping: dict[str, str] | None = Field(
        default=None,
        description="Map from state fields to component input fields (None for auto-derive)",
    )

    output_mapping: dict[str, str] | None = Field(
        default=None,
        description="Map from component output fields to state fields (None for auto-derive)",
    )

    # Optional description for visualization
    description: str | None = Field(
        default=None, description="Description of this step for documentation"
    )

    model_config = {"arbitrary_types_allowed": True}


class SequentialAgentConfig(AgentConfig):
    """Configuration for a SequentialAgent that connects components linearly.

    This agent automates the process of connecting engine components in a sequence,
    handling the data flow between them through the state schema.

    Components can be any engine types, particularly AugLLMConfig instances
    for chaining language model steps.
    """

    # Sequential workflow steps
    steps: list[StepConfig] = Field(
        description="Ordered list of steps in the sequential workflow"
    )

    # Optional initial step
    entry_point: str | None = Field(
        default=None,
        description="Name of the entry point step (defaults to first step)",
    )

    # Visualization settings
    visualize: bool = Field(default=True, description="Whether to visualize the graph")

    # Schema definitions
    state_schema: type[StateSchema] | None = Field(
        default=None, description="Schema for the agent state (None for auto-derive)"
    )

    input_schema: type[BaseModel] | None = Field(
        default=None, description="Schema for agent inputs (None for auto-derive)"
    )

    output_schema: type[BaseModel] | None = Field(
        default=None, description="Schema for agent outputs (None for auto-derive)"
    )

    # Override components field to include step components
    components: list[Any] = Field(
        default_factory=list, description="Additional components for schema derivation"
    )

    model_config = {"arbitrary_types_allowed": True}

    @field_validator("steps")
    def validate_steps(cls, v):
        """Ensure we have at least one step."""
        if not v or len(v) == 0:
            raise ValueError("SequentialAgent must have at least one step")
        return v

    @model_validator(mode="after")
    def setup_components(self):
        """Collect all step components into the components list for schema derivation."""
        # Collect step components
        step_components = [step.component for step in self.steps]

        # Add to components list if not already there
        for component in step_components:
            if component not in self.components:
                self.components.append(component)

        # Validate entry point
        if self.entry_point is not None:
            # Check that entry point exists in steps
            step_names = [step.name for step in self.steps]
            if self.entry_point not in step_names:
                raise ValueError(f"Entry point '{self.entry_point}' not found in steps")

        return self

    def get_step_by_name(self, name: str) -> StepConfig | None:
        """Get a step configuration by name."""
        for step in self.steps:
            if step.name == name:
                return step
        return None

    def build_agent(self):
        """Build and return a SequentialAgent instance."""
        from haive.agents.sequential.agent import SequentialAgent

        return SequentialAgent(self)

    @classmethod
    def from_steps(
        cls,
        steps: list[StepConfig],
        name: str | None = None,
        id: str | None = None,
        entry_point: str | None = None,
        state_schema: type[StateSchema] | None = None,
        **kwargs,
    ) -> "SequentialAgentConfig":
        """Create a SequentialAgentConfig from a list of steps.

        Args:
            steps: List of step configurations
            name: Optional agent name
            id: Optional unique identifier
            entry_point: Optional entry point step name
            state_schema: Optional state schema
            **kwargs: Additional configuration parameters

        Returns:
            SequentialAgentConfig instance
        """
        # Generate default name if not provided
        if name is None:
            name = f"sequential_agent_{uuid.uuid4().hex[:8]}"

        # Generate default ID if not provided
        if id is None:
            id = f"agent_{uuid.uuid4().hex[:8]}"

        return cls(
            id=id,
            name=name,
            steps=steps,
            entry_point=entry_point,
            state_schema=state_schema,
            **kwargs,
        )

    @classmethod
    def from_components(
        cls,
        components: list[Any],
        name: str | None = None,
        id: str | None = None,
        state_schema: type[StateSchema] | None = None,
        step_names: list[str] | None = None,
        **kwargs,
    ) -> "SequentialAgentConfig":
        """Create a SequentialAgentConfig from a list of components.

        This automatically creates step configurations for each component.

        Args:
            components: List of components to use as steps (AugLLMConfig, Engine, etc.)
            name: Optional agent name
            id: Optional unique identifier
            state_schema: Optional state schema
            step_names: Optional list of step names (must match length of components)
            **kwargs: Additional configuration parameters

        Returns:
            SequentialAgentConfig instance
        """
        # Check we have components
        if not components:
            raise ValueError("Must provide at least one component")

        # Generate step names if not provided
        if step_names is None:
            step_names = []
            for i, component in enumerate(components):
                # Try to use component name if available
                if hasattr(component, "name"):
                    step_names.append(f"step_{component.name}")
                else:
                    step_names.append(f"step_{i+1}")

        # Validate step names length
        if len(step_names) != len(components):
            raise ValueError("Number of step names must match number of components")

        # Create step configs
        steps = []
        for name, component in zip(step_names, components, strict=False):
            steps.append(
                StepConfig(
                    name=name,
                    component=component,
                    description=f"Step using {component.__class__.__name__}",
                )
            )

        # Create the sequential agent config
        return cls.from_steps(
            steps=steps, name=name, id=id, state_schema=state_schema, **kwargs
        )

    @classmethod
    def from_aug_llms(
        cls,
        aug_llms: list[AugLLMConfig],
        name: str | None = None,
        id: str | None = None,
        state_schema: type[StateSchema] | None = None,
        **kwargs,
    ) -> "SequentialAgentConfig":
        """Create a SequentialAgentConfig from a list of AugLLMConfig instances.

        Convenience method for the common case of chaining LLM steps.

        Args:
            aug_llms: List of AugLLMConfig instances
            name: Optional agent name
            id: Optional unique identifier
            state_schema: Optional state schema
            **kwargs: Additional configuration parameters

        Returns:
            SequentialAgentConfig instance
        """
        # Use the generic from_components method
        return cls.from_components(
            components=aug_llms,
            name=name or f"llm_chain_{uuid.uuid4().hex[:8]}",
            id=id,
            state_schema=state_schema,
            **kwargs,
        )
