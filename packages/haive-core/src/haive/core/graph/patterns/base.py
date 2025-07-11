"""Base pattern definitions for the Haive framework.

This module provides the core classes for pattern definition, registration,
and application in graph-based workflows.
"""

import logging
from collections.abc import Callable
from typing import Any, Literal

from langgraph.graph import END
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

# Type aliases for clarity
ComponentType = Literal[
    "engine", "processor", "retriever", "llm", "embeddings", "vectorstore", "tool"
]


class ComponentRequirement(BaseModel):
    """Defines a requirement for a component needed by a pattern.

    Component requirements can specify types, capabilities, and other attributes
    that must be present for a pattern to be applied successfully.
    """

    type: ComponentType = Field(description="Type of component required")
    count: int = Field(
        default=1,
        ge=1,
        description="Minimum number of components of this type required",
    )
    optional: bool = Field(
        default=False, description="Whether this component is optional"
    )
    capabilities: list[str] = Field(
        default_factory=list, description="Specific capabilities required"
    )
    name: str | None = Field(
        default=None, description="Specific component name (if required)"
    )
    description: str | None = Field(
        default=None, description="Description of how this component is used"
    )

    def validate_component(self, component: Any) -> bool:
        """Validate if a component meets this requirement.

        Args:
            component: Component to validate

        Returns:
            True if the component meets this requirement
        """
        # Basic type check (simplified - real implementation would be more thorough)
        if hasattr(component, "engine_type"):
            component_type = component.engine_type.value
            if component_type == self.type:
                return True

        # For string component types
        if isinstance(component, str) and component == self.type:
            return True

        # For dict component types
        return bool(isinstance(component, dict) and component.get("type") == self.type)


class ParameterDefinition(BaseModel):
    """Definition of a parameter for patterns and branches.

    Includes type information, validation rules, and documentation.
    """

    type: str = Field(description="Parameter type (str, int, bool, etc.)")
    default: Any = Field(default=None, description="Default value for the parameter")
    description: str = Field(description="Description of the parameter")
    required: bool = Field(
        default=False, description="Whether this parameter is required"
    )
    choices: list[Any] | None = Field(
        default=None, description="Valid choices for this parameter (if applicable)"
    )
    min_value: Any | None = Field(
        default=None, description="Minimum value (for numeric parameters)"
    )
    max_value: Any | None = Field(
        default=None, description="Maximum value (for numeric parameters)"
    )

    def validate_value(self, value: Any) -> tuple[bool, str | None]:
        """Validate a parameter value against this definition.

        Args:
            value: Value to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check required
        if self.required and value is None:
            return False, "Required parameter missing"

        # If value is None and not required, it's valid
        if value is None and not self.required:
            return True, None

        # Check type (basic check - could be enhanced)
        expected_type = eval(self.type) if isinstance(self.type, str) else self.type
        if not isinstance(value, expected_type):
            return False, f"Expected type {self.type}, got {type(value).__name__}"

        # Check choices
        if self.choices is not None and value not in self.choices:
            return False, f"Value must be one of {self.choices}"

        # Check numeric constraints
        if isinstance(value, int | float):
            if self.min_value is not None and value < self.min_value:
                return False, f"Value must be >= {self.min_value}"
            if self.max_value is not None and value > self.max_value:
                return False, f"Value must be <= {self.max_value}"

        return True, None


class PatternMetadata(BaseModel):
    """Enhanced metadata for graph patterns.

    Provides comprehensive information about a pattern, including its
    requirements, parameters, and documentation.
    """

    name: str = Field(description="Unique pattern identifier")
    description: str = Field(description="Description of what the pattern does")
    version: str = Field(default="1.0.0", description="Semantic version")
    pattern_type: str = Field(description="Category/type of pattern")

    # Component requirements
    required_components: list[ComponentRequirement] = Field(
        default_factory=list, description="Components required for this pattern"
    )

    # Parameter definitions with validation
    parameters: dict[str, ParameterDefinition] = Field(
        default_factory=dict,
        description="Parameter definitions with types and validation",
    )

    # Dependencies
    dependencies: list[str] = Field(
        default_factory=list, description="Other patterns this pattern depends on"
    )

    # Application constraints
    constraints: dict[str, Any] = Field(
        default_factory=dict, description="Constraints on pattern application"
    )

    # Documentation
    examples: list[dict[str, Any]] = Field(
        default_factory=list, description="Usage examples"
    )
    tags: list[str] = Field(default_factory=list, description="Tags for categorization")

    def check_required_components(self, components: list[Any]) -> list[str]:
        """Check if the required components are available.

        Args:
            components: List of available components

        Returns:
            List of missing component requirements
        """
        missing = []

        # Check each requirement
        for req in self.required_components:
            if req.optional:
                continue

            # Count matching components
            count = sum(1 for comp in components if req.validate_component(comp))

            if count < req.count:
                missing.append(f"{req.type} (need {req.count}, found {count})")

        return missing

    def validate_parameters(self, params: dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate parameter values against their definitions.

        Args:
            params: Parameter values to validate

        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []

        # Check each parameter
        for name, definition in self.parameters.items():
            value = params.get(name)

            # Validate the value
            is_valid, error = definition.validate_value(value)
            if not is_valid:
                errors.append(f"Parameter '{name}': {error}")

        # Check for unknown parameters
        unknown = [key for key in params if key not in self.parameters]
        if unknown:
            errors.append(f"Unknown parameters: {', '.join(unknown)}")

        return len(errors) == 0, errors


class GraphPattern(BaseModel):
    """Defines a reusable graph pattern."""

    metadata: PatternMetadata = Field(description="Pattern metadata")
    apply_func: Callable | None = Field(
        default=None,
        exclude=True,
        description="Function that applies this pattern to a graph",
    )

    model_config = {"arbitrary_types_allowed": True}

    @property
    def name(self) -> str:
        """Get the pattern name from metadata."""
        return self.metadata.name

    def apply(self, graph: Any, **kwargs) -> Any:
        """Apply this pattern to a graph."""
        # Check if this is an instance method override
        # Compare the actual function objects using __func__
        instance_method = getattr(self.__class__, "apply", None)
        base_method = getattr(GraphPattern, "apply", None)

        if (
            instance_method is not base_method
            and instance_method.__func__ is not base_method.__func__
        ):
            # This is an instance that has overridden the apply method
            # so we should use the instance method directly
            logger.debug(f"Using overridden apply method for pattern {self.name}")
            try:
                result = instance_method(self, graph, **kwargs)
                # Track pattern application
                if (
                    hasattr(graph, "applied_patterns")
                    and self.name not in graph.applied_patterns
                ):
                    graph.applied_patterns.append(self.name)
                return result
            except Exception as e:
                logger.exception(
                    f"Error in overridden apply method for {self.name}: {e}"
                )
                raise

        if self.apply_func is None:
            raise ValueError(f"Pattern {self.name} has no implementation")

        # Rest of implementation...
        components = getattr(graph, "components", [])
        is_valid, errors = self.validate_for_application(components, kwargs)
        if not is_valid:
            error_msg = f"Cannot apply pattern {self.name}: {', '.join(errors)}"
            logger.error(error_msg)
            raise ValueError(error_msg)

        try:
            result = self.apply_func(graph, **kwargs)
            if (
                hasattr(graph, "applied_patterns")
                and self.name not in graph.applied_patterns
            ):
                graph.applied_patterns.append(self.name)
            return result
        except Exception as e:
            logger.exception(f"Error applying pattern {self.name}: {e}")
            raise

    def to_dict(self) -> dict[str, Any]:
        """Convert to a serializable dictionary.

        Returns:
            Dictionary representation
        """
        if hasattr(self, "model_dump"):
            # Pydantic v2
            result = self.model_dump(exclude={"apply_func"})
        else:
            # Pydantic v1
            result = self.dict(exclude={"apply_func"})

        # Add function name if available
        if self.apply_func:
            result["apply_func_name"] = getattr(self.apply_func, "__name__", None)
            result["apply_func_module"] = getattr(self.apply_func, "__module__", None)

        return result

    @classmethod
    def from_dict(
        cls, data: dict[str, Any], func_resolver: Callable | None = None
    ) -> "GraphPattern":
        """Create from a serialized dictionary.

        Args:
            data: Dictionary representation
            func_resolver: Optional function to resolve function references

        Returns:
            New GraphPattern instance
        """
        # Create a copy of the data
        pattern_data = data.copy()

        # Handle apply_func reference
        apply_func = None
        if "apply_func_name" in pattern_data and "apply_func_module" in pattern_data:
            if func_resolver:
                # Use the provided resolver
                apply_func = func_resolver(
                    pattern_data["apply_func_module"], pattern_data["apply_func_name"]
                )
            else:
                # Try to import directly
                try:
                    module = __import__(
                        pattern_data["apply_func_module"], fromlist=[""]
                    )
                    apply_func = getattr(module, pattern_data["apply_func_name"])
                except (ImportError, AttributeError) as e:
                    logger.warning(f"Could not resolve function: {e}")

        # Remove function reference fields
        if "apply_func_name" in pattern_data:
            del pattern_data["apply_func_name"]
        if "apply_func_module" in pattern_data:
            del pattern_data["apply_func_module"]

        # Create pattern
        pattern = cls(**pattern_data)

        # Set apply_func if resolved
        if apply_func:
            pattern.apply_func = apply_func

        return pattern

    def create_node_config(self, node_name: str, **kwargs) -> Any:
        """Create a NodeConfig based on this pattern.

        Args:
            node_name: Name for the node
            **kwargs: Configuration parameters

        Returns:
            NodeConfig instance
        """
        # This requires importing NodeConfig which might create circular imports
        # The actual implementation would need to handle this properly
        raise NotImplementedError("This method should be implemented by subclasses")

    def validate_for_application(
        self, components: list[Any], params: dict[str, Any]
    ) -> tuple[bool, list[str]]:
        """Validate that a pattern can be applied with the provided components and parameters.

        Args:
            components: List of components to check requirements against
            params: Parameter values to validate

        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []

        # Check component requirements
        component_errors = self.metadata.check_required_components(components)
        if component_errors:
            errors.extend(component_errors)

        # Check parameter values
        param_valid, param_errors = self.metadata.validate_parameters(params)
        if not param_valid:
            errors.extend(param_errors)

        return len(errors) == 0, errors


class BranchDefinition(BaseModel):
    """Enhanced branch definition with metadata.

    Defines a reusable branch condition that can be applied to graphs.
    """

    name: str = Field(description="Unique branch identifier")
    description: str = Field(description="What this branch condition does")
    condition_type: str = Field(description="Type of condition logic")

    # Enhanced routing
    routes: dict[str, str] = Field(
        description="Mapping of condition values to node names"
    )
    default_route: str = Field(
        default="END", description="Default route if no condition matches"
    )

    # Parameter template for customization
    parameters: dict[str, ParameterDefinition] = Field(
        default_factory=dict, description="Parameters for condition configuration"
    )

    # Branch function factory
    condition_factory: Callable | None = Field(
        default=None,
        exclude=True,
        description="Function that creates condition functions",
    )

    # Condition implementation
    condition_func: Callable | None = Field(
        default=None, exclude=True, description="Actual condition function"
    )

    # Metadata
    tags: list[str] = Field(default_factory=list, description="Tags for categorization")
    version: str = Field(default="1.0.0", description="Semantic version")

    model_config = {"arbitrary_types_allowed": True}

    def create_condition(self, **kwargs) -> Callable:
        """Create a condition function with parameters.

        Args:
            **kwargs: Parameter values

        Returns:
            Configured condition function
        """
        if self.condition_factory:
            return self.condition_factory(**kwargs)
        if self.condition_func:
            return self.condition_func
        raise ValueError(f"Branch {self.name} has no implementation")

    def validate_parameters(self, params: dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate parameter values against their definitions.

        Args:
            params: Parameter values to validate

        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []

        # Check each parameter
        for name, definition in self.parameters.items():
            value = params.get(name)

            # Validate the value
            is_valid, error = definition.validate_value(value)
            if not is_valid:
                errors.append(f"Parameter '{name}': {error}")

        # Check for unknown parameters
        unknown = [key for key in params if key not in self.parameters]
        if unknown:
            errors.append(f"Unknown parameters: {', '.join(unknown)}")

        return len(errors) == 0, errors

    def apply_to_graph(self, graph: Any, source_node: str, **kwargs) -> Any:
        """Apply this branch directly to a graph.

        Args:
            graph: Graph to add branch to
            source_node: Source node for branching
            **kwargs: Parameter values

        Returns:
            Modified graph
        """
        # Validate parameters
        is_valid, errors = self.validate_parameters(kwargs)
        if not is_valid:
            error_msg = f"Cannot apply branch {self.name}: {', '.join(errors)}"
            logger.error(error_msg)
            raise ValueError(error_msg)

        # Create condition with parameters
        condition = self.create_condition(**kwargs)

        # Apply routes (with END handling)
        normalized_routes = {}
        for key, value in self.routes.items():
            if value == "END":
                normalized_routes[key] = END
            else:
                normalized_routes[key] = value

        # Add to graph
        if hasattr(graph, "add_conditional_edges"):
            graph.add_conditional_edges(source_node, condition, normalized_routes)

            # Log application
            logger.info(f"Applied branch {self.name} to node {source_node}")

            return graph
        raise ValueError("Graph does not support add_conditional_edges")

    def to_dict(self) -> dict[str, Any]:
        """Convert to a serializable dictionary.

        Returns:
            Dictionary representation
        """
        if hasattr(self, "model_dump"):
            # Pydantic v2
            result = self.model_dump(exclude={"condition_factory", "condition_func"})
        else:
            # Pydantic v1
            result = self.dict(exclude={"condition_factory", "condition_func"})

        # Add function names if available
        if self.condition_factory:
            result["condition_factory_name"] = getattr(
                self.condition_factory, "__name__", None
            )
            result["condition_factory_module"] = getattr(
                self.condition_factory, "__module__", None
            )

        if self.condition_func:
            result["condition_func_name"] = getattr(
                self.condition_func, "__name__", None
            )
            result["condition_func_module"] = getattr(
                self.condition_func, "__module__", None
            )

        return result

    @classmethod
    def from_dict(
        cls, data: dict[str, Any], func_resolver: Callable | None = None
    ) -> "BranchDefinition":
        """Create from a serialized dictionary.

        Args:
            data: Dictionary representation
            func_resolver: Optional function to resolve function references

        Returns:
            New BranchDefinition instance
        """
        # Create a copy of the data
        branch_data = data.copy()

        # Handle function references
        condition_factory = None
        condition_func = None

        # Resolve condition factory
        if (
            "condition_factory_name" in branch_data
            and "condition_factory_module" in branch_data
        ):
            if func_resolver:
                condition_factory = func_resolver(
                    branch_data["condition_factory_module"],
                    branch_data["condition_factory_name"],
                )
            else:
                try:
                    module = __import__(
                        branch_data["condition_factory_module"], fromlist=[""]
                    )
                    condition_factory = getattr(
                        module, branch_data["condition_factory_name"]
                    )
                except (ImportError, AttributeError) as e:
                    logger.warning(f"Could not resolve condition factory: {e}")

        # Resolve condition function
        if (
            "condition_func_name" in branch_data
            and "condition_func_module" in branch_data
        ):
            if func_resolver:
                condition_func = func_resolver(
                    branch_data["condition_func_module"],
                    branch_data["condition_func_name"],
                )
            else:
                try:
                    module = __import__(
                        branch_data["condition_func_module"], fromlist=[""]
                    )
                    condition_func = getattr(module, branch_data["condition_func_name"])
                except (ImportError, AttributeError) as e:
                    logger.warning(f"Could not resolve condition function: {e}")

        # Remove function reference fields
        for field in [
            "condition_factory_name",
            "condition_factory_module",
            "condition_func_name",
            "condition_func_module",
        ]:
            if field in branch_data:
                del branch_data[field]

        # Create branch
        branch = cls(**branch_data)

        # Set functions if resolved
        if condition_factory:
            branch.condition_factory = condition_factory
        if condition_func:
            branch.condition_func = condition_func

        return branch
