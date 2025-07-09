"""Automatic tree structure generator for Pydantic BaseModels with Union type support.

This module provides the AutoTree class that automatically wraps any BaseModel
in a tree structure, handling complex type relationships including Union types.
It enables hierarchical visualization and analysis of nested BaseModel structures.

The AutoTree automatically detects fields containing BaseModels (including those
in Union types) and creates child tree nodes, making it perfect for visualizing
complex data structures like plans with mixed content types.

Usage:
    ```python
    from pydantic import BaseModel, Field
    from typing import List, Union
    from haive.core.common.structures.tree import AutoTree

    class Step(BaseModel):
        name: str
        duration_hours: float = 1.0

    class Plan(BaseModel):
        name: str
        # Can contain either Steps OR other Plans
        items: List[Union[Step, 'Plan']] = Field(default_factory=list)

    # Create nested structure
    main_plan = Plan(name="Project Alpha")
    main_plan.items.append(Step(name="Setup", duration_hours=2))

    sub_plan = Plan(name="Development Phase")
    sub_plan.items.append(Step(name="Code", duration_hours=40))
    main_plan.items.append(sub_plan)

    # Visualize as tree
    tree = AutoTree(main_plan)
    print(tree.visualize())
    ```
"""

import json
from typing import (
    Any,
    Dict,
    Generic,
    List,
    Optional,
    Type,
    TypeVar,
    Union,
    get_args,
    get_origin,
    get_type_hints,
)

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T", bound=BaseModel)


class AutoTree(BaseModel, Generic[T]):
    """Automatically wraps any BaseModel in a tree structure with Union type support.

    This generic class creates a tree representation of any BaseModel by automatically
    detecting fields that contain other BaseModels (including those in Union types)
    and creating child tree nodes for them.

    The tree structure enables easy navigation, visualization, and analysis of
    complex nested data structures. It's particularly useful for handling
    self-referential or polymorphic data structures.

    Attributes:
        content: The wrapped BaseModel instance.
        _children: List of child AutoTree nodes.
        _parent: Reference to parent AutoTree node (if any).
        _field_source: Name of the field this node came from in its parent.

    Args:
        content: The BaseModel instance to wrap in the tree.
        parent: Optional parent AutoTree node.
        field_source: Optional name of the field this content came from.

    Example:
        >>> class Step(BaseModel):
        ...     name: str
        >>> class Plan(BaseModel):
        ...     name: str
        ...     items: List[Union[Step, 'Plan']] = []
        >>> plan = Plan(name="Main", items=[Step(name="Task1")])
        >>> tree = AutoTree(plan)
        >>> print(tree.visualize())
    """

    content: T
    _children: List["AutoTree"] = []
    _parent: Optional["AutoTree"] = None
    _field_source: Optional[str] = None

    model_config = ConfigDict(arbitrary_types_allowed=True, validate_assignment=True)

    def __init__(
        self,
        content: T,
        parent: Optional["AutoTree"] = None,
        field_source: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(content=content, **kwargs)
        self._parent = parent
        self._field_source = field_source
        self._build_children()

    def _is_basemodel_type(self, type_hint: Any) -> bool:
        """Check if a type hint represents a BaseModel or Union containing BaseModels.

        This method analyzes type hints to determine if they represent BaseModel
        types, either directly or within Union types. It's used to identify
        fields that should be converted to child tree nodes.

        Args:
            type_hint: The type annotation to analyze.

        Returns:
            True if the type hint represents BaseModel(s), False otherwise.
        """
        # Direct BaseModel subclass
        if isinstance(type_hint, type) and issubclass(type_hint, BaseModel):
            return True

        # Check Union types
        origin = get_origin(type_hint)
        if origin is Union:
            # Check if any of the Union members are BaseModels
            args = get_args(type_hint)
            return any(
                isinstance(arg, type) and issubclass(arg, BaseModel)
                for arg in args
                if arg is not type(None)  # Exclude Optional's None
            )

        return False

    def _extract_basemodel_types(self, type_hint: Any) -> List[Type[BaseModel]]:
        """Extract all BaseModel types from a type hint (including from Unions)."""
        types = []

        # Direct BaseModel
        if isinstance(type_hint, type) and issubclass(type_hint, BaseModel):
            types.append(type_hint)

        # Union types
        origin = get_origin(type_hint)
        if origin is Union:
            args = get_args(type_hint)
            for arg in args:
                if (
                    arg is not type(None)
                    and isinstance(arg, type)
                    and issubclass(arg, BaseModel)
                ):
                    types.append(arg)

        return types

    def _build_children(self):
        """Auto-detect all fields containing BaseModels and create child tree nodes.

        This method scans all fields in the wrapped content, identifies those
        containing BaseModels (including within lists and Union types), and
        creates corresponding child AutoTree nodes.

        The method handles:
        - Direct BaseModel fields
        - Lists of BaseModels
        - Union types containing BaseModels
        - Nested combinations of the above

        Child nodes are automatically linked with parent references and
        field source information for navigation.
        """
        self._children.clear()

        # Get type hints to understand Union types
        try:
            hints = get_type_hints(self.content.__class__)
        except:
            hints = {}

        # Check each field in the content
        for field_name, field_value in self.content:
            if field_value is None:
                continue

            # Handle lists
            if isinstance(field_value, list):
                # Check type hint for this field
                field_type = hints.get(field_name)

                # Determine if list can contain BaseModels
                can_contain_basemodels = False
                if field_type:
                    origin = get_origin(field_type)
                    if origin in (list, List):
                        args = get_args(field_type)
                        if args:
                            can_contain_basemodels = self._is_basemodel_type(args[0])

                # Process list items
                for item in field_value:
                    if isinstance(item, BaseModel):
                        child_tree = AutoTree(
                            content=item, parent=self, field_source=field_name
                        )
                        self._children.append(child_tree)
                    elif not can_contain_basemodels and not isinstance(item, BaseModel):
                        # If we don't have type hints, still check if it's a BaseModel
                        pass

            # Handle single BaseModel fields
            elif isinstance(field_value, BaseModel):
                child_tree = AutoTree(
                    content=field_value, parent=self, field_source=field_name
                )
                self._children.append(child_tree)

    @property
    def node_name(self) -> str:
        """Get display name - tries common fields first."""
        for attr in ["name", "id", "title", "label", "key", "value", "type"]:
            if hasattr(self.content, attr):
                value = getattr(self.content, attr)
                if value is not None:
                    return str(value)

        class_name = self.content.__class__.__name__
        if hasattr(self.content, "id"):
            return f"{class_name}#{getattr(self.content, 'id')}"
        return class_name

    @property
    def node_type(self) -> str:
        """Get the type name of the content."""
        return self.content.__class__.__name__

    @property
    def children(self) -> List["AutoTree"]:
        """Get child trees."""
        return self._children

    @property
    def children_by_field(self) -> Dict[str, List["AutoTree"]]:
        """Get children grouped by their source field."""
        grouped = {}
        for child in self._children:
            field = child._field_source or "unknown"
            if field not in grouped:
                grouped[field] = []
            grouped[field].append(child)
        return grouped

    @property
    def children_by_type(self) -> Dict[str, List["AutoTree"]]:
        """Get children grouped by their type."""
        grouped = {}
        for child in self._children:
            child_type = child.node_type
            if child_type not in grouped:
                grouped[child_type] = []
            grouped[child_type].append(child)
        return grouped

    def visualize(
        self,
        show_field: bool = True,
        show_type: bool = True,
        max_depth: Optional[int] = None,
    ) -> str:
        """Generate a visual tree representation with customizable display options.

        Creates a text-based tree visualization using Unicode box-drawing characters
        to show the hierarchical structure. The display can be customized to include
        or exclude field names, type information, and can be limited to a specific depth.

        Args:
            show_field: Whether to show the source field name for each node.
            show_type: Whether to show the BaseModel class name for each node.
            max_depth: Maximum depth to display (None for unlimited).

        Returns:
            String representation of the tree structure with appropriate indentation
            and connectors.

        Example:
            >>> tree.visualize(show_field=True, show_type=True, max_depth=2)
            'MainPlan <Plan>\\n├── [items] Setup <Step>\\n└── [items] Development <Plan>'
        """
        return self._visualize_recursive(
            0, "", True, show_field, show_type, max_depth, 0
        )

    def _visualize_recursive(
        self,
        indent: int,
        prefix: str,
        is_last: bool,
        show_field: bool,
        show_type: bool,
        max_depth: Optional[int],
        current_depth: int,
    ) -> str:
        """Recursive visualization helper."""
        if max_depth is not None and current_depth > max_depth:
            return ""

        # Build node representation
        node_str = self.node_name

        # Add field source
        if show_field and self._field_source:
            node_str = f"[{self._field_source}] {node_str}"

        # Add type
        if show_type:
            node_str += f" <{self.node_type}>"

        # Root node
        if indent == 0:
            result = f"{node_str}\n"
        else:
            connector = "└── " if is_last else "├── "
            result = f"{prefix}{connector}{node_str}\n"

        # Check depth limit
        if max_depth is not None and current_depth >= max_depth:
            if self.children:
                result += f"{prefix}    └── ... ({len(self.children)} more)\n"
            return result

        # Prepare prefix for children
        if indent > 0:
            child_prefix = prefix + ("    " if is_last else "│   ")
        else:
            child_prefix = ""

        # Show all children
        for i, child in enumerate(self._children):
            is_last_child = i == len(self._children) - 1
            result += child._visualize_recursive(
                indent + 1,
                child_prefix,
                is_last_child,
                show_field,
                show_type,
                max_depth,
                current_depth + 1,
            )

        return result

    # ... (include all other methods from before)


# === EXAMPLE USAGE ===

# def example_union_types():
#     """Examples showing Union type handling."""

#     # Example 1: Plan/Step hierarchy where items can be either
#     class Step(BaseModel):
#         name: str
#         description: str = ""
#         duration_hours: float = 1.0

#     class Plan(BaseModel):
#         name: str
#         description: str = ""
#         # This is the key - items can be EITHER Step OR Plan!
#         items: List[Union[Step, 'Plan']] = Field(default_factory=list)

#     Plan.model_rebuild()

#     print("=== EXAMPLE 1: Plan with mixed Steps and sub-Plans ===\n")

#     # Create a master plan
#     master = Plan(name="Q1 2024 Roadmap")

#     # Add some direct steps
#     master.items.append(Step(name="Initial Planning", duration_hours=8))
#     master.items.append(Step(name="Resource Allocation", duration_hours=4))

#     # Add a sub-plan (same list!)
#     feature_plan = Plan(name="New Feature Development")
#     feature_plan.items = [
#         Step(name="Design", duration_hours=16),
#         Step(name="Implementation", duration_hours=40),
#         Step(name="Testing", duration_hours=20)
#     ]
#     master.items.append(feature_plan)

#     # Add another sub-plan with its own sub-plans
#     infrastructure = Plan(name="Infrastructure Updates")

#     # This sub-plan has mixed items too
#     database_plan = Plan(name="Database Migration")
#     database_plan.items = [
#         Step(name="Backup Current DB", duration_hours=2),
#         Step(name="Schema Migration", duration_hours=8),
#         Step(name="Data Migration", duration_hours=16)
#     ]

#     infrastructure.items = [
#         Step(name="Server Upgrade", duration_hours=6),
#         database_plan,  # Plan inside a plan!
#         Step(name="Security Patches", duration_hours=4)
#     ]

#     master.items.append(infrastructure)

#     # Add a final direct step
#     master.items.append(Step(name="Q1 Review", duration_hours=4))

#     # Create tree and visualize
#     tree = AutoTree(master)
#     print(tree.visualize())

#     # Show analysis
#     print("\n=== ANALYSIS ===")
#     stats = tree.stats()
#     print(f"Total nodes: {stats['total_nodes']}")
#     print(f"Type distribution: {stats['type_distribution']}")
#     print(f"Max depth: {stats['height']}")

#     # Find all steps
#     all_steps = tree.find_by_type(Step)
#     total_hours = sum(step.content.duration_hours for step in all_steps)
#     print(f"\nTotal hours for all steps: {total_hours}")

#     # Example 2: More complex Union types
#     print("\n\n=== EXAMPLE 2: Complex Union Types ===\n")

#     class Person(BaseModel):
#         name: str
#         role: str = "person"

#     class Team(BaseModel):
#         name: str
#         # Members can be either Person OR another Team!
#         members: List[Union[Person, 'Team']] = Field(default_factory=list)

#     Team.model_rebuild()

#     # Create organization structure
#     company = Team(name="TechCorp")

#     # Engineering team with sub-teams
#     engineering = Team(name="Engineering")

#     backend_team = Team(name="Backend Team")
#     backend_team.members = [
#         Person(name="Alice", role="Senior Backend Dev"),
#         Person(name="Bob", role="Backend Dev"),
#         Person(name="Charlie", role="DevOps")
#     ]

#     frontend_team = Team(name="Frontend Team")
#     frontend_team.members = [
#         Person(name="Diana", role="Frontend Lead"),
#         Person(name="Eve", role="UI/UX Designer"),
#         Person(name="Frank", role="Frontend Dev")
#     ]

#     # Engineering has both sub-teams and direct members
#     engineering.members = [
#         Person(name="Grace", role="CTO"),
#         backend_team,
#         frontend_team,
#         Person(name="Henry", role="QA Lead")  # Direct member among teams
#     ]

#     # Sales team is flat
#     sales = Team(name="Sales")
#     sales.members = [
#         Person(name="Iris", role="Sales Director"),
#         Person(name="Jack", role="Sales Rep"),
#         Person(name="Kate", role="Sales Rep")
#     ]

#     company.members = [engineering, sales]

#     # Visualize
#     tree = AutoTree(company)
#     print(tree.visualize())

#     # Find all people across all teams
#     all_people = tree.find_by_type(Person)
#     print(f"\nTotal employees: {len(all_people)}")
#     print(f"Employees: {[p.content.name for p in all_people]}")

#     # Find all teams
#     all_teams = tree.find_by_type(Team)
#     print(f"\nTotal teams: {len(all_teams)}")
#     print(f"Teams: {[t.content.name for t in all_teams]}")


# if __name__ == "__main__":
#     example_union_types()
