"""Pattern configuration for agent composition.

This module provides pattern-related configuration classes for the agent system,
enabling declarative, pattern-based agent composition with proper validation
and integration with the GraphPatternRegistry.
"""

import logging
from typing import Any

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class PatternConfig(BaseModel):
    """Configuration for a pattern to be applied to an agent.

    This allows detailed configuration of pattern application,
    including parameters, application order, and conditions.
    """

    name: str = Field(description="Name of the pattern to apply")
    parameters: dict[str, Any] = Field(
        default_factory=dict, description="Parameters for pattern application"
    )
    order: int | None = Field(
        default=None, description="Order to apply pattern (lower numbers first)"
    )
    condition: str | None = Field(
        default=None, description="Condition for pattern application"
    )
    enabled: bool = Field(default=True, description="Whether this pattern is enabled")
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata"
    )

    model_config = {"arbitrary_types_allowed": True}

    def merge_with(self, other: "PatternConfig") -> "PatternConfig":
        """Merge this pattern configuration with another.

        Args:
            other: The other pattern config to merge with

        Returns:
            New merged pattern config
        """
        # Start with a copy of this config
        merged_params = self.parameters.copy()

        # Update with other parameters
        merged_params.update(other.parameters)

        # Create new config with merged parameters
        return PatternConfig(
            name=self.name,
            parameters=merged_params,
            order=other.order if other.order is not None else self.order,
            condition=(
                other.condition if other.condition is not None else self.condition
            ),
            enabled=other.enabled,
            metadata={**self.metadata, **other.metadata},
        )


class PatternManager:
    """Manager for pattern application and tracking.

    This class handles pattern ordering, validation, parameter resolution,
    and application tracking.
    """

    def __init__(self):
        """Initialize the pattern manager."""
        self.patterns: list[PatternConfig] = []
        self.pattern_parameters: dict[str, dict[str, Any]] = {}
        self._applied_patterns: set[str] = set()

    def add_pattern(
        self,
        pattern_name: str,
        parameters: dict[str, Any] | None = None,
        order: int | None = None,
        condition: str | None = None,
        enabled: bool = True,
    ) -> None:
        """Add a pattern to be applied.

        Args:
            pattern_name: Name of the pattern in the registry
            parameters: Parameters for pattern application
            order: Application order (lower numbers first)
            condition: Optional condition for pattern application
            enabled: Whether this pattern is enabled
        """
        # Check if pattern exists in registry
        try:
            from haive.core.graph.patterns.registry import GraphPatternRegistry

            registry = GraphPatternRegistry.get_instance()
            if not registry.get_pattern(pattern_name):
                logger.warning(f"Pattern '{pattern_name}' not found in registry")
        except ImportError:
            logger.warning("Pattern registry not available")

        # Check if we already have this pattern
        existing_pattern = None
        for pattern in self.patterns:
            if pattern.name == pattern_name:
                existing_pattern = pattern
                break

        if existing_pattern:
            # Update existing pattern
            new_pattern = PatternConfig(
                name=pattern_name,
                parameters=parameters or {},
                order=order,
                condition=condition,
                enabled=enabled,
            )

            # Replace with merged configuration
            self.patterns.remove(existing_pattern)
            self.patterns.append(existing_pattern.merge_with(new_pattern))
        else:
            # Add new pattern
            self.patterns.append(
                PatternConfig(
                    name=pattern_name,
                    parameters=parameters or {},
                    order=order,
                    condition=condition,
                    enabled=enabled,
                )
            )

    def set_pattern_parameters(self, pattern_name: str, **parameters) -> None:
        """Set global parameters for a pattern.

        Args:
            pattern_name: Name of the pattern
            **parameters: Parameter values
        """
        if pattern_name not in self.pattern_parameters:
            self.pattern_parameters[pattern_name] = {}

        # Update parameters
        self.pattern_parameters[pattern_name].update(parameters)

        # Update any existing pattern configs
        for pattern in self.patterns:
            if pattern.name == pattern_name:
                for key, value in parameters.items():
                    if key not in pattern.parameters:
                        pattern.parameters[key] = value

    def disable_pattern(self, pattern_name: str) -> None:
        """Disable a pattern.

        Args:
            pattern_name: Name of the pattern to disable
        """
        for pattern in self.patterns:
            if pattern.name == pattern_name:
                pattern.enabled = False
                break

    def enable_pattern(self, pattern_name: str) -> None:
        """Enable a pattern.

        Args:
            pattern_name: Name of the pattern to enable
        """
        for pattern in self.patterns:
            if pattern.name == pattern_name:
                pattern.enabled = True
                break

    def get_pattern_order(self) -> list[str]:
        """Get ordered list of patterns to apply.

        Returns:
            List of pattern names in application order
        """
        # Sort patterns by order (None values last)
        sorted_patterns = sorted(
            self.patterns, key=lambda p: (p.order is None, p.order or 999999)
        )

        # Filter enabled patterns
        return [p.name for p in sorted_patterns if p.enabled]

    def get_pattern_parameters(self, pattern_name: str) -> dict[str, Any]:
        """Get combined parameters for a pattern.

        Args:
            pattern_name: Name of the pattern

        Returns:
            Combined parameters from pattern config and global parameters
        """
        # Start with global parameters
        combined = self.pattern_parameters.get(pattern_name, {}).copy()

        # Add pattern-specific parameters (overriding globals)
        for pattern in self.patterns:
            if pattern.name == pattern_name:
                combined.update(pattern.parameters)
                break

        return combined

    def is_pattern_applied(self, pattern_name: str) -> bool:
        """Check if a pattern has been applied.

        Args:
            pattern_name: Name of the pattern to check

        Returns:
            True if the pattern has been applied
        """
        return pattern_name in self._applied_patterns

    def mark_pattern_applied(self, pattern_name: str) -> None:
        """Mark a pattern as applied.

        Args:
            pattern_name: Name of the pattern to mark
        """
        self._applied_patterns.add(pattern_name)

    def patterns_as_list(self) -> list[PatternConfig]:
        """Get all pattern configurations as a list.

        Returns:
            List of pattern configurations
        """
        return self.patterns.copy()

    def parameters_as_dict(self) -> dict[str, dict[str, Any]]:
        """Get all pattern parameters as a dictionary.

        Returns:
            Dictionary mapping pattern names to parameter dictionaries
        """
        return self.pattern_parameters.copy()

    def applied_patterns_as_set(self) -> set[str]:
        """Get all applied patterns as a set.

        Returns:
            Set of applied pattern names
        """
        return self._applied_patterns.copy()

    def validate_patterns(self) -> list[str]:
        """Validate that all patterns exist in the registry.

        Returns:
            List of invalid pattern names
        """
        invalid_patterns = []

        try:
            from haive.core.graph.patterns.registry import GraphPatternRegistry

            registry = GraphPatternRegistry.get_instance()

            for pattern in self.patterns:
                if not registry.get_pattern(pattern.name):
                    invalid_patterns.append(pattern.name)
        except ImportError:
            logger.warning("Pattern registry not available for validation")

        return invalid_patterns

    def get_required_components(self) -> list[Any]:
        """Get components required by patterns.

        Returns:
            List of component requirements
        """
        components = []

        try:
            from haive.core.graph.patterns.registry import GraphPatternRegistry

            registry = GraphPatternRegistry.get_instance()

            for pattern in self.patterns:
                if not pattern.enabled:
                    continue

                pattern_obj = registry.get_pattern(pattern.name)
                if pattern_obj:
                    # Extract requirements from pattern metadata
                    for req in pattern_obj.metadata.required_components:
                        components.append(req)
        except ImportError:
            logger.warning("Pattern registry not available for component extraction")

        return components

    def to_dict(self) -> dict[str, Any]:
        """Convert to a dictionary for serialization.

        Returns:
            Dictionary representation
        """
        return {
            "patterns": [
                (
                    pattern.model_dump()
                    if hasattr(pattern, "model_dump")
                    else pattern.dict()
                )
                for pattern in self.patterns
            ],
            "pattern_parameters": self.pattern_parameters,
            "applied_patterns": list(self._applied_patterns),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PatternManager":
        """Create from a dictionary representation.

        Args:
            data: Dictionary representation

        Returns:
            New PatternManager instance
        """
        manager = cls()

        # Load patterns
        for pattern_data in data.get("patterns", []):
            manager.patterns.append(PatternConfig(**pattern_data))

        # Load pattern parameters
        manager.pattern_parameters = data.get("pattern_parameters", {})

        # Load applied patterns
        manager._applied_patterns = set(data.get("applied_patterns", []))

        return manager
