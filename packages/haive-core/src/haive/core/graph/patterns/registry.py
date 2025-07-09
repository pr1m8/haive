import inspect
import logging
from collections.abc import Callable
from typing import Any, Callable, Dict, List, Optional, TypeVar, Union

from haive.core.graph.patterns.base import (
    BranchDefinition,
    GraphPattern,
    ParameterDefinition,
    PatternMetadata,
)
from haive.core.registry.base import AbstractRegistry

# Define pattern type
P = TypeVar("P", bound=Union[GraphPattern, BranchDefinition])

logger = logging.getLogger(__name__)


class GraphPatternRegistry(AbstractRegistry[P]):
    """Registry for graph patterns and branch definitions."""

    _instance = None

    @classmethod
    def get_instance(cls) -> "GraphPatternRegistry":
        """Get the singleton instance of the registry."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        """Initialize the pattern registry."""
        self.patterns = {}  # name -> GraphPattern
        self.branches = {}  # name -> BranchDefinition
        self.pattern_categories = {}  # type -> [pattern names]
        self.branch_categories = {}  # type -> [branch names]

    def register(self, item: P) -> P:
        """Register a pattern or branch in the registry."""
        if isinstance(item, GraphPattern):
            pattern_name = item.metadata.name
            self.patterns[pattern_name] = item

            # Track category
            category = item.metadata.pattern_type
            if category not in self.pattern_categories:
                self.pattern_categories[category] = []
            if pattern_name not in self.pattern_categories[category]:
                self.pattern_categories[category].append(pattern_name)

        elif isinstance(item, BranchDefinition):
            branch_name = item.name
            self.branches[branch_name] = item

            # Track category
            category = item.condition_type
            if category not in self.branch_categories:
                self.branch_categories[category] = []
            if branch_name not in self.branch_categories[category]:
                self.branch_categories[category].append(branch_name)

        else:
            raise TypeError(f"Unsupported item type: {type(item)}")

        return item

    def get(self, item_type: Any, name: str) -> Optional[P]:
        """Get a pattern or branch by type and name."""
        if item_type == "pattern":
            return self.patterns.get(name)
        elif item_type == "branch":
            return self.branches.get(name)
        return None

    def find_by_id(self, id: str) -> Optional[P]:
        """Find a pattern or branch by ID (name)."""
        # Try patterns first
        if id in self.patterns:
            return self.patterns[id]
        # Then branches
        if id in self.branches:
            return self.branches[id]
        return None

    def list(self, item_type: Any) -> List[str]:
        """List all patterns or branches of a type."""
        if item_type == "pattern":
            return list(self.patterns.keys())
        elif item_type == "branch":
            return list(self.branches.keys())
        elif item_type in self.pattern_categories:
            return self.pattern_categories[item_type]
        elif item_type in self.branch_categories:
            return self.branch_categories[item_type]
        return []

    def get_all(self, item_type: Any) -> Dict[str, P]:
        """Get all patterns or branches of a type."""
        if item_type == "pattern":
            return self.patterns
        elif item_type == "branch":
            return self.branches
        # For category types, create a filtered dict
        result = {}
        if item_type in self.pattern_categories:
            for name in self.pattern_categories[item_type]:
                result[name] = self.patterns[name]
        elif item_type in self.branch_categories:
            for name in self.branch_categories[item_type]:
                result[name] = self.branches[name]
        return result

    def clear(self) -> None:
        """Clear the registry."""
        self.patterns = {}
        self.branches = {}
        self.pattern_categories = {}
        self.branch_categories = {}

    # Helper methods to maintain compatibility
    def get_pattern(self, name: str) -> Optional[GraphPattern]:
        """Get a pattern by name."""
        return self.patterns.get(name)

    def get_branch(self, name: str) -> Optional[BranchDefinition]:
        """Get a branch by name."""
        return self.branches.get(name)

    def list_patterns(self, pattern_type: Optional[str] = None) -> List[str]:
        """List pattern names, optionally filtered by type."""
        if pattern_type:
            return self.pattern_categories.get(pattern_type, [])
        return list(self.patterns.keys())

    def list_branches(self, condition_type: Optional[str] = None) -> List[str]:
        """List branch names, optionally filtered by type."""
        if condition_type:
            return self.branch_categories.get(condition_type, [])
        return list(self.branches.keys())

    # Register pattern methods with compatibility for different input types
    def register_pattern(
        self,
        pattern: Union[GraphPattern, Dict[str, Any], Callable],
        name: str = None,
        pattern_type: str = None,
        description: str = None,
        metadata: Dict[str, Any] = None,
        **pattern_params,
    ) -> GraphPattern:
        """Register a pattern directly without requiring decorator usage."""
        # Convert to GraphPattern if needed
        pattern_obj = self._convert_to_pattern(
            pattern, name, pattern_type, description, metadata, **pattern_params
        )
        return self.register(pattern_obj)

    def _convert_to_pattern(
        self,
        pattern,
        name=None,
        pattern_type=None,
        description=None,
        metadata=None,
        **pattern_params,
    ):
        """Convert to GraphPattern."""
        if isinstance(pattern, GraphPattern):
            pattern_obj = pattern

            # Override metadata if provided
            if name or pattern_type or description or metadata:
                # Create updated metadata
                metadata_dict = (
                    pattern_obj.metadata.model_dump()
                    if hasattr(pattern_obj.metadata, "model_dump")
                    else pattern_obj.metadata.dict()
                )

                if name:
                    metadata_dict["name"] = name
                if pattern_type:
                    metadata_dict["pattern_type"] = pattern_type
                if description:
                    metadata_dict["description"] = description
                if metadata:
                    metadata_dict.update(metadata)

                # Update pattern with new metadata
                pattern_obj.metadata = PatternMetadata(**metadata_dict)

        elif isinstance(pattern, dict):
            # Create from dictionary
            if "metadata" not in pattern:
                # Create metadata from parameters
                metadata_dict = {
                    "name": name
                    or pattern.get("name", f"pattern_{len(self.patterns)}"),
                    "description": description or pattern.get("description", ""),
                    "pattern_type": pattern_type
                    or pattern.get("pattern_type", "undefined"),
                    "parameters": pattern.get("parameters", {}),
                }

                # Add additional metadata
                if metadata:
                    metadata_dict.update(metadata)

                pattern["metadata"] = PatternMetadata(**metadata_dict)

            # Create pattern object
            pattern_obj = GraphPattern(**pattern)

        elif callable(pattern):
            # Create from function
            if not name:
                name = getattr(pattern, "__name__", f"pattern_{len(self.patterns)}")
                if isinstance(name, tuple):  # Fix for tuple name
                    name = name[0]

            if not description:
                description = getattr(pattern, "__doc__", "")

            if not pattern_type:
                pattern_type = "undefined"

            # Create metadata
            metadata_dict = {
                "name": name,
                "description": description,
                "pattern_type": pattern_type,
                "parameters": {},
            }

            # Extract parameter info from function signature
            sig = inspect.signature(pattern)
            for param_name, param in sig.parameters.items():
                if param_name == "graph" or param_name == "self":
                    continue

                param_type = "Any"
                if param.annotation != inspect.Parameter.empty:
                    param_type = str(param.annotation)

                default = None
                required = param.default == inspect.Parameter.empty
                if not required:
                    default = param.default

                # Add parameter definition
                metadata_dict["parameters"][param_name] = (
                    ParameterDefinition(
                        type=param_type,
                        default=default,
                        description=f"Parameter {param_name}",
                        required=required,
                    ).model_dump()
                    if hasattr(ParameterDefinition, "model_dump")
                    else ParameterDefinition(
                        type=param_type,
                        default=default,
                        description=f"Parameter {param_name}",
                        required=required,
                    ).dict()
                )

            # Add additional metadata
            if metadata:
                metadata_dict.update(metadata)

            # Create pattern object
            pattern_obj = GraphPattern(
                metadata=PatternMetadata(**metadata_dict), apply_func=pattern
            )

        else:
            raise ValueError(f"Unsupported pattern type: {type(pattern)}")

        return pattern_obj

    def register_branch(
        self,
        branch: Union[BranchDefinition, Dict[str, Any], Callable],
        name: str = None,
        condition_type: str = None,
        description: str = None,
        routes: Dict[str, str] = None,
        default_route: str = None,
        **branch_params,
    ) -> BranchDefinition:
        """Register a branch definition directly."""
        # Convert to BranchDefinition if needed
        branch_obj = self._convert_to_branch(
            branch,
            name,
            condition_type,
            description,
            routes,
            default_route,
            **branch_params,
        )
        return self.register(branch_obj)

    def _convert_to_branch(
        self,
        branch,
        name=None,
        condition_type=None,
        description=None,
        routes=None,
        default_route=None,
        **branch_params,
    ):
        """Convert to BranchDefinition."""
        if isinstance(branch, BranchDefinition):
            branch_obj = branch

            # Override fields if provided
            if name:
                branch_obj.name = name
            if condition_type:
                branch_obj.condition_type = condition_type
            if description:
                branch_obj.description = description
            if routes:
                branch_obj.routes = routes
            if default_route:
                branch_obj.default_route = default_route

        elif isinstance(branch, dict):
            # Create from dictionary
            branch_dict = branch.copy()

            # Add overrides
            if name:
                branch_dict["name"] = name
            if condition_type:
                branch_dict["condition_type"] = condition_type
            if description:
                branch_dict["description"] = description
            if routes:
                branch_dict["routes"] = routes
            if default_route:
                branch_dict["default_route"] = default_route

            # Create branch object
            branch_obj = BranchDefinition(**branch_dict)

        elif callable(branch):
            # Create from function
            if not name:
                name = getattr(branch, "__name__", f"branch_{len(self.branches)}")

            if not description:
                description = getattr(branch, "__doc__", "")

            if not condition_type:
                condition_type = "undefined"

            # Create branch definition
            branch_obj = BranchDefinition(
                name=name,
                description=description,
                condition_type=condition_type,
                routes=routes or {},
                default_route=default_route or "END",
                condition_func=branch,
            )

            # Add parameters from function signature
            sig = inspect.signature(branch)
            parameters = {}

            for param_name, param in sig.parameters.items():
                if param_name == "state" or param_name == "self":
                    continue

                param_type = "Any"
                if param.annotation != inspect.Parameter.empty:
                    param_type = str(param.annotation)

                default = None
                required = param.default == inspect.Parameter.empty
                if not required:
                    default = param.default

                # Add parameter definition
                parameters[param_name] = ParameterDefinition(
                    type=param_type,
                    default=default,
                    description=f"Parameter {param_name}",
                    required=required,
                )

            branch_obj.parameters = parameters

        else:
            raise ValueError(f"Unsupported branch type: {type(branch)}")

        return branch_obj
